# tools/plotting/dynamic_tool_generator.py
import inspect
import plotly.express as px
from tools.plotting.base import BasePlottingTool, ToolInput
from pydantic import Field
import typing
from typing import Optional, List, Dict, Any, Union
from numpydoc.docscrape import NumpyDocString

def parse_docstring(docstring: str) -> Dict[str, str]:
    """Parses a docstring using numpydoc to extract parameter descriptions."""
    if not docstring:
        return {}

    doc = NumpyDocString(docstring)
    params = {}
    for param in doc['Parameters']:
        # Join the description lines and clean up whitespace
        description = " ".join(line.strip() for line in param.desc).strip()
        params[param.name.strip()] = description
        
    return params

def format_type(annotation: Any) -> str:
    """Converts a Python type annotation into a valid type hint string."""
    if annotation is Any or annotation is inspect.Parameter.empty:
        return "Any"
    if annotation is None or annotation is type(None):
        return "Any"
    
    origin = getattr(annotation, '__origin__', None)
    args = getattr(annotation, '__args__', ())

    if origin is Union and len(args) == 2 and type(None) in args:
        main_type = next(arg for arg in args if arg is not type(None))
        return f"Optional[{format_type(main_type)}]"
    
    if origin in [Union, list, List]:
        if not args: return "List"
        formatted_args = ', '.join(format_type(arg) for arg in args)
        return f"List[{formatted_args}]"
        
    if origin in [dict, Dict]:
        if not args: return "Dict"
        key_type, value_type = args
        return f"Dict[{format_type(key_type)}, {format_type(value_type)}]"

    if origin is tuple:
        if not args: return "tuple"
        formatted_args = ', '.join(format_type(arg) for arg in args)
        return f"tuple[{formatted_args}]"

    if hasattr(annotation, '__name__'):
        return annotation.__name__
        
    return str(annotation).replace("typing.", "")

def generate_plotly_tool_classes():
    """
    Inspects the plotly.express module and dynamically generates LangChain tool
    classes for each plotting function.
    """
    tool_classes = {}
    
    # List of functions to exclude (non-plotting helpers)
    exclude_list = ['imshow', 'data', 'colors', 'pd']

    # Iterate over all functions in the plotly.express module
    for name, func in inspect.getmembers(px, inspect.isfunction):
        if name.startswith("_") or name in exclude_list:
            continue

        # --- 1. Create the dynamic Input model ---
        sig = inspect.signature(func)
        docstring = inspect.getdoc(func)
        doc_params = parse_docstring(docstring)

        # Correctly prepare dictionaries for dynamic type creation
        annotations = {}
        attributes = {}

        # Add our custom arguments first for all plotting tools
        annotations['marker_symbol'] = Optional[str]
        attributes['marker_symbol'] = Field(default=None, description="Set a single symbol for all markers in the plot (e.g., 'circle', 'square', 'diamond', 'triangle-up').")
        
        annotations['marker_size'] = Optional[float]
        attributes['marker_size'] = Field(default=None, description="Set a uniform size for all markers in the plot (e.g., 10, 15, 20).")

        for param in sig.parameters.values():
            if param.name in ['args', 'kwargs', 'self']:
                continue

            param_name = param.name
            if param_name == 'color':
                param_name = 'color_by_column'
                description = doc_params.get(param.name, f"Plotly Express argument for the '{name}' function.")
                description += " This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`."
            elif param_name == 'symbol':
                param_name = 'symbol_by_column'
                description = doc_params.get(param.name, f"Plotly Express argument for the '{name}' function.")
                description += " This argument is for mapping data values to symbols. To set a single, uniform symbol for all points (e.g., 'square'), use the 'marker_symbol' argument instead."
            else:
                # Find the matching description from the parsed docstring
                description = f"Plotly Express argument for the '{name}' function." # Fallback
                for doc_param_name, doc_param_desc in doc_params.items():
                    if doc_param_name.startswith(param.name):
                        description = doc_param_desc
                        break

            annotations[param_name] = param.annotation
            default_value = '...' if param.default is inspect.Parameter.empty else repr(param.default)
            if 'PydanticUndefined' in str(default_value) or default_value == '...':
                default_value = 'None'

            attributes[param_name] = Field(default=eval(default_value), description=description)

        annotations['dataset_id'] = Optional[str]
        attributes['dataset_id'] = Field(default='generated', description="The ID of the dataset to use.")
        
        annotations['title'] = Optional[str]
        attributes['title'] = Field(default=None, description="The title of the plot.")
        
        class_dict = {'__annotations__': annotations, **attributes}
        
        # Sanitize class name to be a valid identifier
        sanitized_name = ''.join(c for c in name.title().replace("_", "") if c.isalnum())
        input_class_name = f"{sanitized_name}Input"

        input_model = type(input_class_name, (ToolInput,), class_dict)

        # --- 2. Create the dynamic Tool class ---
        main_description = (docstring or "No description available.").strip().split('\n')[0]
        
        tool_class_name = f"Plotly{sanitized_name}Tool"
        
        tool_class = type(
            tool_class_name,
            (BasePlottingTool,),
            {
                'name': f"plotting_{name}",
                'description': main_description,
                'input_model': input_model,
                '_plot_function': staticmethod(func),
            }
        )
        tool_classes[tool_class.__name__] = tool_class

    return tool_classes


def write_tool_classes_to_file(tool_classes, file_path="tools/plotting/generated_tools.py"):
    """
    Writes the dynamically generated tool classes to a Python file.
    """
    with open(file_path, "w") as f:
        f.write("# This file is dynamically generated. Do not edit manually.\n\n")
        f.write("from tools.plotting.base import BasePlottingTool, ToolInput\n")
        f.write("from pydantic import Field\n")
        f.write("from typing import Optional, List, Dict, Any, Union\n")
        f.write("import plotly.express as px\n\n")

        for name, tool_class in sorted(tool_classes.items()):
            input_model = tool_class.input_model
            
            f.write(f"class {input_model.__name__}(ToolInput):\n")
            if not input_model.model_fields:
                f.write("    pass\n\n")
            else:
                for field_name, field_info in input_model.model_fields.items():
                    type_hint = format_type(field_info.annotation)
                    
                    default_val = field_info.default
                    # Check for Pydantic's internal undefined type without importing it
                    is_pydantic_undefined = type(default_val).__name__ == 'PydanticUndefined'

                    if default_val is ... or is_pydantic_undefined:
                        default_repr = "None"
                    else:
                        default_repr = repr(default_val)
                    
                    description = (field_info.description or "").replace("\"", "\\\"").replace("\n", " ").strip()
                    
                    f.write(f"    {field_name}: {type_hint} = Field(default={default_repr}, description=\"{description}\")\n")
                f.write("\n")

            f.write(f"class {name}(BasePlottingTool):\n")
            f.write(f"    name = \"{tool_class.name}\"\n")
            description = (tool_class.description or "").replace("\"", "\\\"").replace("\n", " ").strip()
            f.write(f"    description = \"{description}\"\n")
            f.write(f"    input_model = {input_model.__name__}\n")
            f.write(f"    _plot_function = staticmethod(px.{tool_class._plot_function.__name__})\n\n")

if __name__ == "__main__":
    generated_tools = generate_plotly_tool_classes()
    write_tool_classes_to_file(generated_tools)
    print(f"✅ Successfully generated {len(generated_tools)} tool classes.") 