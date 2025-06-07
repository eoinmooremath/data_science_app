"""
Dynamic Statistical Tool Generator

This module dynamically generates wrapper classes for statistical functions from:
- scipy.stats
- statsmodels.stats
- statsmodels.tsa

Following the same pattern as the plotting tools, it uses inspection and regex
to extract function signatures and create unified wrapper classes.
"""

import inspect
import re
from typing import Optional, List, Dict, Any, Union, get_type_hints
from pydantic import Field
from numpydoc.docscrape import NumpyDocString

from tools.base import BaseTool
from core.models import ToolInput

# Import statistical libraries
try:
    import scipy.stats as scipy_stats
    import statsmodels.api as sm
    import statsmodels.stats.api as sms
    import statsmodels.tsa.api as tsa
    import statsmodels.stats.diagnostic as smd
    import statsmodels.stats.weightstats as smw
    import statsmodels.stats.proportion as smp
    import statsmodels.stats.power as smpower
    SCIPY_AVAILABLE = True
    STATSMODELS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Statistical libraries not available: {e}")
    SCIPY_AVAILABLE = False
    STATSMODELS_AVAILABLE = False


def parse_docstring(docstring: str) -> Dict[str, str]:
    """Parse docstring using numpydoc to extract parameter descriptions."""
    if not docstring:
        return {}

    try:
        doc = NumpyDocString(docstring)
        params = {}
        for param in doc['Parameters']:
            description = " ".join(line.strip() for line in param.desc).strip()
            params[param.name.strip()] = description
        return params
    except Exception:
        # Fallback to simple parsing if numpydoc fails
        return parse_docstring_simple(docstring)


def parse_docstring_simple(docstring: str) -> Dict[str, str]:
    """Simple docstring parser as fallback."""
    params = {}
    if not docstring:
        return params
    
    # Look for Parameters section
    lines = docstring.split('\n')
    in_params = False
    current_param = None
    current_desc = []
    
    for line in lines:
        line = line.strip()
        if line.lower().startswith('parameters'):
            in_params = True
            continue
        elif line.lower().startswith(('returns', 'notes', 'examples', 'see also')):
            in_params = False
            if current_param:
                params[current_param] = ' '.join(current_desc).strip()
            break
        
        if in_params and line:
            # Check if this is a parameter definition
            if ':' in line and not line.startswith(' '):
                # Save previous parameter
                if current_param:
                    params[current_param] = ' '.join(current_desc).strip()
                
                # Start new parameter
                param_match = re.match(r'^(\w+)\s*:', line)
                if param_match:
                    current_param = param_match.group(1)
                    current_desc = [line.split(':', 1)[1].strip()]
                else:
                    current_param = None
                    current_desc = []
            elif current_param and line.startswith(' '):
                # Continuation of description
                current_desc.append(line.strip())
    
    # Save last parameter
    if current_param:
        params[current_param] = ' '.join(current_desc).strip()
    
    return params


def format_type(annotation: Any) -> str:
    """Convert Python type annotation to valid type hint string."""
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
        if not args: 
            return "List"
        formatted_args = ', '.join(format_type(arg) for arg in args)
        return f"List[{formatted_args}]"
        
    if origin in [dict, Dict]:
        if not args: 
            return "Dict"
        key_type, value_type = args
        return f"Dict[{format_type(key_type)}, {format_type(value_type)}]"

    if origin is tuple:
        if not args: 
            return "tuple"
        formatted_args = ', '.join(format_type(arg) for arg in args)
        return f"tuple[{formatted_args}]"

    if hasattr(annotation, '__name__'):
        return annotation.__name__
        
    return str(annotation).replace("typing.", "")


def categorize_function(module_name: str, func_name: str, docstring: str) -> str:
    """Categorize statistical function based on module and name patterns."""
    func_lower = func_name.lower()
    doc_lower = (docstring or "").lower()
    
    # Test functions
    if any(word in func_lower for word in ['test', 'pvalue', 'statistic']):
        if any(word in func_lower for word in ['normal', 'shapiro', 'jarque', 'anderson']):
            return "NORMALITY_TESTS"
        elif any(word in func_lower for word in ['ttest', 't_test']):
            return "T_TESTS"
        elif any(word in func_lower for word in ['chi', 'chisq']):
            return "CHI_SQUARE_TESTS"
        elif any(word in func_lower for word in ['anova', 'f_oneway']):
            return "ANOVA_TESTS"
        elif any(word in func_lower for word in ['correlation', 'pearson', 'spearman', 'kendall']):
            return "CORRELATION_TESTS"
        else:
            return "STATISTICAL_TESTS"
    
    # Descriptive statistics
    if any(word in func_lower for word in ['describe', 'mean', 'std', 'var', 'skew', 'kurtosis']):
        return "DESCRIPTIVE_STATS"
    
    # Regression models
    if any(word in func_lower for word in ['ols', 'gls', 'wls', 'logit', 'probit', 'regression']):
        return "REGRESSION_MODELS"
    
    # Time series
    if 'tsa' in module_name or any(word in func_lower for word in ['arima', 'var', 'adf', 'kpss', 'acf', 'pacf']):
        return "TIME_SERIES"
    
    # Power analysis
    if any(word in func_lower for word in ['power', 'sample_size']):
        return "POWER_ANALYSIS"
    
    # Distributions
    if any(word in func_lower for word in ['pdf', 'cdf', 'ppf', 'rvs', 'fit']):
        return "DISTRIBUTIONS"
    
    return "MISCELLANEOUS"


def should_include_function(func_name: str, func: callable) -> bool:
    """Determine if a function should be included in the tool generation."""
    # Skip private functions
    if func_name.startswith('_'):
        return False
    
    # Skip if not callable
    if not callable(func):
        return False
    
    # Skip classes (we want functions)
    if inspect.isclass(func):
        return False
    
    # Skip deprecated functions
    docstring = inspect.getdoc(func) or ""
    if 'deprecated' in docstring.lower():
        return False
    
    # Include common statistical functions
    include_patterns = [
        r'.*test.*',
        r'.*describe.*',
        r'.*correlation.*',
        r'.*regression.*',
        r'.*anova.*',
        r'.*ttest.*',
        r'.*chi.*',
        r'.*normal.*',
        r'.*power.*',
        r'.*sample.*',
        r'.*fit.*',
        r'.*adf.*',
        r'.*kpss.*',
        r'.*acf.*',
        r'.*pacf.*'
    ]
    
    for pattern in include_patterns:
        if re.match(pattern, func_name, re.IGNORECASE):
            return True
    
    return False


def generate_statistical_tool_classes():
    """Generate tool classes for statistical functions."""
    if not SCIPY_AVAILABLE or not STATSMODELS_AVAILABLE:
        print("Statistical libraries not available")
        return {}
    
    tool_classes = {}
    
    # Define modules to inspect
    modules_to_inspect = [
        ('scipy.stats', scipy_stats),
        ('statsmodels.stats', sms),
        ('statsmodels.tsa', tsa),
        ('statsmodels.stats.diagnostic', smd),
        ('statsmodels.stats.weightstats', smw),
        ('statsmodels.stats.proportion', smp),
        ('statsmodels.stats.power', smpower),
    ]
    
    for module_name, module in modules_to_inspect:
        print(f"Inspecting {module_name}...")
        
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not should_include_function(name, func):
                continue
            
            try:
                # Get function signature and docstring
                sig = inspect.signature(func)
                docstring = inspect.getdoc(func)
                doc_params = parse_docstring(docstring)
                
                # Create input model
                annotations = {}
                attributes = {}
                
                # Add common statistical tool parameters
                annotations['create_plot'] = Optional[bool]
                attributes['create_plot'] = Field(default=False, description="Whether to create a visualization of the results")
                
                annotations['alpha'] = Optional[float]
                attributes['alpha'] = Field(default=0.05, description="Significance level for statistical tests")
                
                # Process function parameters
                for param in sig.parameters.values():
                    if param.name in ['args', 'kwargs', 'self']:
                        continue
                    
                    param_name = param.name
                    
                    # Get description from docstring
                    description = doc_params.get(param.name, f"Parameter for {name} function")
                    
                    # Determine type annotation
                    if param.annotation != inspect.Parameter.empty:
                        annotations[param_name] = param.annotation
                    else:
                        # Infer type from parameter name and default value
                        if param.default != inspect.Parameter.empty:
                            if isinstance(param.default, bool):
                                annotations[param_name] = Optional[bool]
                            elif isinstance(param.default, int):
                                annotations[param_name] = Optional[int]
                            elif isinstance(param.default, float):
                                annotations[param_name] = Optional[float]
                            elif isinstance(param.default, str):
                                annotations[param_name] = Optional[str]
                            else:
                                annotations[param_name] = Any
                        else:
                            # Common parameter type inference
                            if 'data' in param_name or param_name in ['x', 'y', 'sample']:
                                annotations[param_name] = List[float]
                            elif param_name in ['axis', 'ddof', 'lags', 'nlags']:
                                annotations[param_name] = Optional[int]
                            elif param_name in ['alpha', 'beta', 'confidence']:
                                annotations[param_name] = Optional[float]
                            elif param_name in ['alternative', 'method', 'mode']:
                                annotations[param_name] = Optional[str]
                            else:
                                annotations[param_name] = Any
                    
                    # Set default value
                    if param.default != inspect.Parameter.empty:
                        default_value = param.default
                    else:
                        default_value = None
                    
                    attributes[param_name] = Field(default=default_value, description=description)
                
                # Create input class
                class_dict = {'__annotations__': annotations, **attributes}
                sanitized_name = ''.join(c for c in name.title().replace("_", "") if c.isalnum())
                input_class_name = f"{sanitized_name}Input"
                input_model = type(input_class_name, (ToolInput,), class_dict)
                
                # Create tool class
                category = categorize_function(module_name, name, docstring)
                main_description = (docstring or "Statistical function").strip().split('\n')[0]
                
                tool_class_name = f"Stats{sanitized_name}Tool"
                tool_name = f"stats_{name.lower()}"
                
                tool_class = type(
                    tool_class_name,
                    (BaseTool,),
                    {
                        'name': tool_name,
                        'description': main_description,
                        'input_model': input_model,
                        'category': category,
                        'estimated_duration': 3.0,
                        '_statistical_function': staticmethod(func),
                    }
                )
                
                tool_classes[tool_class.__name__] = tool_class
                print(f"  Generated: {tool_name}")
                
            except Exception as e:
                print(f"  Skipped {name}: {e}")
                continue
    
    return tool_classes


def write_statistical_tool_classes_to_file(tool_classes, file_path="tools/statistical/generated_tools.py"):
    """Write the dynamically generated statistical tool classes to a Python file."""
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# This file is dynamically generated. Do not edit manually.\n\n")
        f.write("from tools.statistical.base import BaseStatisticalTool\n")
        f.write("from core.models import ToolInput\n")
        f.write("from pydantic import Field\n")
        f.write("from typing import Optional, List, Dict, Any, Union\n")
        f.write("import time\n")
        f.write("import numpy as np\n\n")
        
        # Import statistical libraries
        f.write("try:\n")
        f.write("    import scipy.stats as scipy_stats\n")
        f.write("    import statsmodels.api as sm\n")
        f.write("    import statsmodels.stats.api as sms\n")
        f.write("    import statsmodels.tsa.api as tsa\n")
        f.write("    import statsmodels.stats.diagnostic as smd\n")
        f.write("    import statsmodels.stats.weightstats as smw\n")
        f.write("    import statsmodels.stats.proportion as smp\n")
        f.write("    import statsmodels.stats.power as smpower\n")
        f.write("except ImportError:\n")
        f.write("    pass\n\n")

        # Group tools by category
        categories = {}
        for name, tool_class in tool_classes.items():
            category = getattr(tool_class, 'category', 'MISCELLANEOUS')
            if category not in categories:
                categories[category] = []
            categories[category].append((name, tool_class))

        # Write tools grouped by category
        for category, tools in sorted(categories.items()):
            f.write(f"# === {category.replace('_', ' ').title()} ===\n\n")
            
            for name, tool_class in sorted(tools):
                input_model = tool_class.input_model
                
                # Write input class
                f.write(f"class {input_model.__name__}(ToolInput):\n")
                if not input_model.model_fields:
                    f.write("    pass\n\n")
                else:
                    for field_name, field_info in input_model.model_fields.items():
                        type_hint = format_type(field_info.annotation)
                        
                        default_val = field_info.default
                        is_pydantic_undefined = type(default_val).__name__ == 'PydanticUndefined'

                        if default_val is ... or is_pydantic_undefined:
                            default_repr = "None"
                        elif callable(default_val):
                            # Handle function objects
                            default_repr = "None"
                        elif isinstance(default_val, str):
                            # Escape strings properly
                            default_repr = repr(default_val)
                        else:
                            try:
                                default_repr = repr(default_val)
                            except:
                                default_repr = "None"
                        
                        description = (field_info.description or "").replace("\"", "\\\"").replace("\n", " ").strip()
                        # Clean problematic Unicode characters
                        description = description.encode('ascii', 'ignore').decode('ascii')
                        
                        f.write(f"    {field_name}: {type_hint} = Field(default={default_repr}, description=\"{description}\")\n")
                    f.write("\n")

                # Write tool class
                f.write(f"class {name}(BaseStatisticalTool):\n")
                f.write(f"    name = \"{tool_class.name}\"\n")
                description = (tool_class.description or "").replace("\"", "\\\"").replace("\n", " ").strip()
                # Clean problematic Unicode characters
                description = description.encode('ascii', 'ignore').decode('ascii')
                f.write(f"    description = \"{description}\"\n")
                f.write(f"    input_model = {input_model.__name__}\n")
                # Map module names to their imported aliases
                module_mapping = {
                    'scipy.stats._stats_py': 'scipy_stats',
                    'scipy.stats.contingency': 'scipy_stats',
                    'scipy.stats._fit': 'scipy_stats',
                    'statsmodels.stats.oneway': 'sms',
                    'statsmodels.stats.anova': 'sms', 
                    'statsmodels.stats.gof': 'sms',
                    'statsmodels.stats.diagnostic': 'smd',
                    'statsmodels.stats.weightstats': 'smw',
                    'statsmodels.stats.proportion': 'smp',
                    'statsmodels.stats.power': 'smpower',
                    'statsmodels.stats.rates': 'sms',
                    'statsmodels.tsa.stattools': 'tsa',
                    'statsmodels.tsa.arima_process': 'tsa'
                }
                
                func_module = tool_class._statistical_function.__module__
                func_name = tool_class._statistical_function.__name__
                
                # Use mapped module name or fallback to original
                if func_module in module_mapping:
                    module_ref = module_mapping[func_module]
                    f.write(f"    _statistical_function = staticmethod({module_ref}.{func_name})\n\n")
                else:
                    # For scipy.stats functions, use the direct reference
                    if 'scipy.stats' in func_module:
                        f.write(f"    _statistical_function = staticmethod(scipy_stats.{func_name})\n\n")
                    else:
                        f.write(f"    _statistical_function = staticmethod({func_module}.{func_name})\n\n")


if __name__ == "__main__":
    if SCIPY_AVAILABLE and STATSMODELS_AVAILABLE:
        generated_tools = generate_statistical_tool_classes()
        write_statistical_tool_classes_to_file(generated_tools)
        print(f"✅ Successfully generated {len(generated_tools)} statistical tool classes.")
    else:
        print("❌ Statistical libraries not available. Cannot generate tools.") 