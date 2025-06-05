from typing import Dict, Any

class ResponseTemplates:
    """Templates for common response patterns"""
    
    @staticmethod
    def format_flexible_output(tool_namespace: str, output: Dict[str, Any]) -> str:
        """Format flexible tool output for chat display"""
        
        response_parts = []
        
        # Add interpretation first if available
        if output.get('interpretation'):
            response_parts.append(f"**Insights:** {output['interpretation']}")
        
        # Add key summary points
        if output.get('summary'):
            summary = output['summary']
            if not summary.get('error'):
                response_parts.append("\n**Key Results:**")
                for key, value in summary.items():
                    if isinstance(value, (int, float)):
                        response_parts.append(f"- {key}: {value:.4f}")
                    else:
                        response_parts.append(f"- {key}: {value}")
        
        # Add suggestions if present (for suggest_tool)
        if output.get('suggestions') and len(output['suggestions']) > 0:
            response_parts.append("\n**Detailed Results:**")
            for suggestion in output['suggestions']:
                if isinstance(suggestion, dict):
                    tool = suggestion.get('tool', 'Unknown')
                    reason = suggestion.get('reason', 'No reason provided')
                    response_parts.append(f"- tool: {tool}")
                    response_parts.append(f"- reason: {reason}")
        
        # Add tables if present (for other tools)
        elif output.get('tables') and len(output['tables']) > 0:
            response_parts.append("\n**Detailed Results:**")
            # Show first few rows
            for table in output['tables'][:2]:  # Limit to first 2 tables
                if isinstance(table, dict):
                    for k, v in list(table.items())[:5]:  # First 5 items
                        response_parts.append(f"- {k}: {v}")
                    if len(table) > 5:
                        response_parts.append("- ... (see Results panel for full details)")
        
        # Add visualization note if suggested
        if output.get('visualizations'):
            viz_types = [v.get('type', 'plot') for v in output['visualizations']]
            response_parts.append(f"\n📊 *Visualizations created: {', '.join(viz_types)}*")
        
        # Add next steps
        if output.get('next_steps'):
            response_parts.append("\n**Suggested next steps:**")
            for i, step in enumerate(output['next_steps'][:3], 1):
                response_parts.append(f"{i}. {step}")
        
        return "\n".join(response_parts)
    
    @staticmethod
    def analysis_starting_enhanced(tool_namespace: str, purpose: str) -> str:
        """Response when starting an enhanced analysis"""
        
        category = tool_namespace.split('.')[0]
        
        intros = {
            "stats": "I'll perform statistical analysis",
            "preprocessing": "I'll prepare your data",
            "models": "I'll build a model",
            "meta": "I'll help you explore available tools"
        }
        
        base = intros.get(category, "I'll analyze your data")
        return f"{base} using `{tool_namespace}`. {purpose} Starting now..."