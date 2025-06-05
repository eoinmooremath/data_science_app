# tools/plotting/suggest.py
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from tools.base import BaseTool
from core.models import ToolInput
from .base import BasePlottingTool


class PlotSuggestionInput(BaseModel):
    """Input for plot suggestion tool"""
    analysis_goal: str = Field(description="What you want to analyze (e.g., 'relationship between variables', 'distribution of values', 'trends over time')")
    variables_of_interest: List[str] = Field(default=[], description="Specific columns you want to visualize (optional)")


class PlotSuggestionTool(BasePlottingTool):
    """Tool to suggest appropriate plot types based on data and analysis goals"""
    
    @property
    def name(self) -> str:
        return "plotting_suggest"
    
    @property
    def description(self) -> str:
        return "Suggest the best plot types for your data and analysis goals. Analyzes your dataset and recommends appropriate visualizations."
    
    @property
    def input_model(self) -> type[ToolInput]:
        return PlotSuggestionInput
    
    def get_plot_specific_parameters(self) -> List[str]:
        return ["analysis_goal", "variables_of_interest"]
    
    def create_figure(self, df, **params):
        """This tool doesn't create figures, it provides suggestions"""
        pass
    
    def execute(self, job_id: str, inputs: PlotSuggestionInput) -> Dict[str, Any]:
        """Execute plot suggestion analysis"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Analyzing your data...")
        
        # Get column information
        columns = self.available_columns
        
        if not columns["all"]:
            return {
                "error": "No data available. Please upload a dataset first.",
                "suggestions": []
            }
        
        # Progress: Analyze data structure
        self.update_progress(job_id, 30, "Analyzing data structure...")
        
        analysis_goal = inputs.analysis_goal.lower()
        variables = inputs.variables_of_interest
        
        # Progress: Generate suggestions
        self.update_progress(job_id, 60, "Generating plot suggestions...")
        
        suggestions = self._generate_suggestions(analysis_goal, variables, columns)
        
        # Progress: Complete
        self.update_progress(job_id, 100, "Plot suggestions ready!")
        
        return {
            "suggestions": suggestions,
            "data_summary": {
                "total_columns": len(columns["all"]),
                "numeric_columns": len(columns["numeric"]),
                "categorical_columns": len(columns["categorical"]),
                "datetime_columns": len(columns["datetime"])
            },
            "available_columns": columns,
            "message": f"Found {len(suggestions)} plot suggestions based on your analysis goal"
        }
    
    def _generate_suggestions(self, analysis_goal: str, variables: List[str], columns: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Generate plot suggestions based on analysis goal and data"""
        suggestions = []
        
        # Relationship analysis
        if any(keyword in analysis_goal for keyword in ["relationship", "correlation", "association", "compare"]):
            if len(columns["numeric"]) >= 2:
                suggestions.append({
                    "plot_type": "scatter",
                    "tool_name": "plotting_basic_scatter",
                    "title": "Scatter Plot - Explore Relationships",
                    "description": "Perfect for exploring relationships between two numeric variables",
                    "suggested_params": {
                        "x": columns["numeric"][0],
                        "y": columns["numeric"][1],
                        "color": columns["categorical"][0] if columns["categorical"] else None,
                        "trendline": "ols"
                    },
                    "use_case": "Identify correlations, outliers, and patterns between variables"
                })
            
            if columns["numeric"] and columns["categorical"]:
                suggestions.append({
                    "plot_type": "box",
                    "tool_name": "plotting_statistical_box",
                    "title": "Box Plot - Compare Groups",
                    "description": "Compare distributions across different categories",
                    "suggested_params": {
                        "x": columns["categorical"][0],
                        "y": columns["numeric"][0]
                    },
                    "use_case": "Compare medians, quartiles, and outliers across groups"
                })
        
        # Distribution analysis
        if any(keyword in analysis_goal for keyword in ["distribution", "spread", "frequency", "histogram"]):
            if columns["numeric"]:
                suggestions.append({
                    "plot_type": "histogram",
                    "tool_name": "plotting_basic_histogram",
                    "title": "Histogram - Data Distribution",
                    "description": "Show the distribution and frequency of numeric values",
                    "suggested_params": {
                        "x": columns["numeric"][0],
                        "color": columns["categorical"][0] if columns["categorical"] else None
                    },
                    "use_case": "Understand data distribution, identify skewness and outliers"
                })
                
                suggestions.append({
                    "plot_type": "violin",
                    "tool_name": "plotting_statistical_violin",
                    "title": "Violin Plot - Detailed Distribution",
                    "description": "Combine box plot with kernel density estimation",
                    "suggested_params": {
                        "x": columns["categorical"][0] if columns["categorical"] else None,
                        "y": columns["numeric"][0]
                    },
                    "use_case": "Detailed view of distribution shape and density"
                })
        
        # Time series analysis
        if any(keyword in analysis_goal for keyword in ["time", "trend", "temporal", "over time", "timeline"]):
            if columns["datetime"] and columns["numeric"]:
                suggestions.append({
                    "plot_type": "line",
                    "tool_name": "plotting_basic_line",
                    "title": "Line Plot - Time Series",
                    "description": "Track changes over time",
                    "suggested_params": {
                        "x": columns["datetime"][0],
                        "y": columns["numeric"][0],
                        "color": columns["categorical"][0] if columns["categorical"] else None
                    },
                    "use_case": "Identify trends, seasonality, and patterns over time"
                })
        
        # Categorical analysis
        if any(keyword in analysis_goal for keyword in ["category", "count", "frequency", "bar"]):
            if columns["categorical"]:
                suggestions.append({
                    "plot_type": "bar",
                    "tool_name": "plotting_basic_bar",
                    "title": "Bar Chart - Category Comparison",
                    "description": "Compare values across categories",
                    "suggested_params": {
                        "x": columns["categorical"][0],
                        "y": columns["numeric"][0] if columns["numeric"] else None
                    },
                    "use_case": "Compare quantities or counts across different categories"
                })
                
                if len(columns["categorical"]) >= 2:
                    suggestions.append({
                        "plot_type": "sunburst",
                        "tool_name": "plotting_hierarchical_sunburst",
                        "title": "Sunburst Chart - Hierarchical Categories",
                        "description": "Show hierarchical relationships between categories",
                        "suggested_params": {
                            "path": columns["categorical"][:3],  # Up to 3 levels
                            "values": columns["numeric"][0] if columns["numeric"] else None
                        },
                        "use_case": "Explore nested categorical relationships"
                    })
        
        # Composition analysis
        if any(keyword in analysis_goal for keyword in ["composition", "proportion", "percentage", "pie"]):
            if columns["categorical"] and columns["numeric"]:
                suggestions.append({
                    "plot_type": "pie",
                    "tool_name": "plotting_basic_pie",
                    "title": "Pie Chart - Composition",
                    "description": "Show proportions of a whole",
                    "suggested_params": {
                        "names": columns["categorical"][0],
                        "values": columns["numeric"][0]
                    },
                    "use_case": "Visualize parts of a whole, percentages"
                })
        
        # Geographic analysis
        if any(keyword in analysis_goal for keyword in ["geographic", "location", "map", "spatial"]):
            # Look for potential geographic columns
            geo_columns = [col for col in columns["all"] if any(geo_word in col.lower() 
                          for geo_word in ["lat", "lon", "longitude", "latitude", "country", "state", "city"])]
            
            if geo_columns:
                suggestions.append({
                    "plot_type": "scatter_map",
                    "tool_name": "plotting_geographic_scatter_map",
                    "title": "Geographic Scatter Plot",
                    "description": "Plot data points on a map",
                    "suggested_params": {
                        "lat": next((col for col in geo_columns if "lat" in col.lower()), None),
                        "lon": next((col for col in geo_columns if "lon" in col.lower()), None),
                        "color": columns["numeric"][0] if columns["numeric"] else None
                    },
                    "use_case": "Visualize geographic patterns and distributions"
                })
        
        # If no specific suggestions, provide general recommendations
        if not suggestions:
            suggestions.extend(self._get_general_suggestions(columns))
        
        # Sort suggestions by relevance (prioritize based on data types available)
        suggestions = self._rank_suggestions(suggestions, columns)
        
        return suggestions[:6]  # Return top 6 suggestions
    
    def _get_general_suggestions(self, columns: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Provide general suggestions when no specific analysis goal is identified"""
        suggestions = []
        
        if len(columns["numeric"]) >= 2:
            suggestions.append({
                "plot_type": "scatter",
                "tool_name": "plotting.basic.scatter",
                "title": "Scatter Plot - Explore Data",
                "description": "Start by exploring relationships between numeric variables",
                "suggested_params": {
                    "x": columns["numeric"][0],
                    "y": columns["numeric"][1]
                },
                "use_case": "General data exploration"
            })
        
        if columns["numeric"]:
            suggestions.append({
                "plot_type": "histogram",
                "tool_name": "plotting.basic.histogram",
                "title": "Histogram - Data Overview",
                "description": "Understand the distribution of your data",
                "suggested_params": {
                    "x": columns["numeric"][0]
                },
                "use_case": "Data quality assessment and distribution analysis"
            })
        
        return suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict[str, Any]], columns: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Rank suggestions based on data availability and usefulness"""
        def score_suggestion(suggestion):
            score = 0
            params = suggestion.get("suggested_params", {})
            
            # Score based on parameter availability
            for param, value in params.items():
                if value and value in columns["all"]:
                    score += 1
            
            # Bonus for commonly useful plots
            if suggestion["plot_type"] in ["scatter", "histogram", "bar"]:
                score += 2
            
            return score
        
        return sorted(suggestions, key=score_suggestion, reverse=True) 