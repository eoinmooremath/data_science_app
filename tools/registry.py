from typing import Dict, List, Optional, Type, Any, Union
from tools.base import EnhancedBaseTool, BaseTool
import importlib
import inspect

class ToolRegistry:
    """Registry for namespace-based tool discovery"""
    
    def __init__(self):
        self.tools: Dict[str, Type[EnhancedBaseTool]] = {}
        self.regular_tools: Dict[str, BaseTool] = {}  # Store regular tool instances
        self.namespace_tree: Dict[str, Dict] = {}
        
    def register_tool(self, tool_class: Type[EnhancedBaseTool]):
        """Register a tool with its namespace"""
        tool_instance = tool_class(None, None)  # Temporary instance for metadata
        namespace = tool_instance.namespace
        
        # Register in flat dictionary
        self.tools[namespace] = tool_class
        
        # Build namespace tree
        parts = namespace.split('.')
        current = self.namespace_tree
        
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {}
            if i == len(parts) - 1:
                current[part]['_tool'] = tool_class
            else:
                current = current[part]
    
    def register_regular_tool(self, tool_instance: BaseTool):
        """Register a regular BaseTool instance"""
        self.regular_tools[tool_instance.name] = tool_instance
    
    def discover_tools(self, pattern: str) -> List[str]:
        """Discover tools matching a pattern"""
        # Combine both enhanced tools (by namespace) and regular tools (by name)
        all_tool_names = list(self.tools.keys()) + list(self.regular_tools.keys())
        
        if pattern.endswith('.*'):
            # List all tools in a namespace
            prefix = pattern[:-2]
            return [name for name in all_tool_names if name.startswith(prefix)]
        elif '*' in pattern:
            # Wildcard matching
            import fnmatch
            return [name for name in all_tool_names if fnmatch.fnmatch(name, pattern)]
        else:
            # Exact match
            return [pattern] if pattern in all_tool_names else []
    
    def get_namespace_info(self, namespace: str) -> Dict[str, Any]:
        """Get information about a namespace"""
        parts = namespace.split('.')
        current = self.namespace_tree
        
        for part in parts:
            if part in current:
                current = current[part]
            else:
                return {"error": f"Namespace {namespace} not found"}
        
        # Extract subcategories and tools
        subcategories = []
        tools = []
        
        for key, value in current.items():
            if key == '_tool':
                continue
            elif isinstance(value, dict):
                if '_tool' in value:
                    tools.append(key)
                else:
                    subcategories.append(key)
        
        return {
            "namespace": namespace,
            "subcategories": subcategories,
            "tools": tools
        }
    
    def auto_discover_and_register(self, module_path: str = "tools.implementations"):
        """Auto-discover and register all tools in a module"""
        try:
            module = importlib.import_module(module_path)
            
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, EnhancedBaseTool) and 
                    obj != EnhancedBaseTool):
                    self.register_tool(obj)
        except ImportError:
            pass

# Global registry
tool_registry = ToolRegistry()