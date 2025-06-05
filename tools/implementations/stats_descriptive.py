import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, Union, List, Optional
from tools.base import EnhancedBaseTool, FlexibleToolOutput, ToolInput
from pydantic import Field
from core.models import Message, MessageType

class DescriptiveStatsInput(ToolInput):
    data: Union[list, str] = Field(description="Data array or dataset name")
    columns: Optional[List[str]] = Field(default=None, description="Specific columns to analyze")
    include_plots: bool = Field(default=True, description="Generate visualization suggestions")

class DescriptiveStatsTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "stats.descriptive.summary"
    
    @property
    def name(self) -> str:
        return "descriptive_statistics"
    
    @property
    def description(self) -> str:
        return "Comprehensive descriptive statistics including central tendency, dispersion, and distribution shape"
    
    @property
    def input_model(self) -> type[ToolInput]:
        """Required by BaseTool"""
        return DescriptiveStatsInput
    
    @property
    def output_format(self) -> str:
        return """Returns flexible format with:
        - summary: Key statistics (mean, median, std, etc.)
        - tables: Detailed breakdown by variable
        - statistics: All numerical measures
        - visualizations: Suggested plots (histogram, boxplot, QQ-plot)
        - interpretation: Plain language insights"""
    
    def _execute_analysis(self, job_id: str, inputs: DescriptiveStatsInput) -> Any:
        """Execute descriptive statistics analysis"""
        # Get data
        if isinstance(inputs.data, str):
            # Fetch from uploaded datasets
            from tools.data_tools import uploaded_datasets
            df = uploaded_datasets.get(inputs.data)
            if df is None:
                return {"error": "Dataset not found"}
            
            # If it's not a DataFrame, convert it
            if not isinstance(df, pd.DataFrame):
                df = pd.DataFrame(df)
        else:
            df = pd.DataFrame(inputs.data)
        
        self.update_progress(job_id, 20, "Calculating statistics...")
        
        # Select columns
        if inputs.columns:
            numeric_df = df[inputs.columns].select_dtypes(include=[np.number])
        else:
            numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"error": "No numeric columns found to analyze"}
        
        # Calculate comprehensive statistics
        results = {}
        for col in numeric_df.columns:
            data = numeric_df[col].dropna()
            
            if len(data) == 0:
                continue
                
            # Basic statistics
            col_stats = {
                "count": int(len(data)),
                "mean": float(data.mean()),
                "std": float(data.std()),
                "min": float(data.min()),
                "25%": float(data.quantile(0.25)),
                "50%": float(data.quantile(0.50)),
                "75%": float(data.quantile(0.75)),
                "max": float(data.max()),
                "variance": float(data.var()),
                "cv": float(data.std() / data.mean()) if data.mean() != 0 else None,
                "skewness": float(stats.skew(data)),
                "kurtosis": float(stats.kurtosis(data)),
                "shapiro_p": float(stats.shapiro(data)[1]) if len(data) >= 3 else None
            }
            
            results[str(col)] = col_stats
        
        self.update_progress(job_id, 60, "Generating insights...")
        
        # Generate visualizations if requested
        if inputs.include_plots and len(results) > 0:
            self.update_progress(job_id, 80, "Creating visualizations...")
            
            # Create a box plot for the first few columns
            for i, col in enumerate(list(numeric_df.columns)[:3]):  # Limit to first 3
                if col in results:
                    # Create box plot
                    plot_data = {
                        "type": "box",
                        "y": numeric_df[col].dropna().tolist(),
                        "name": str(col),
                        "title": f"Distribution of {col}"
                    }
                    
                    self.message_bus.publish(Message(
                        type=MessageType.PLOT,
                        job_id=job_id,
                        data=plot_data
                    ))
        
        self.update_progress(job_id, 100, "Analysis complete!")
        
        return results
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        """Format results flexibly"""
        if isinstance(raw_result, dict) and "error" in raw_result:
            return FlexibleToolOutput(
                summary={"error": raw_result["error"]},
                interpretation=raw_result["error"]
            )
        
        # Create summary
        summary = {}
        all_stats = []
        
        for col, stats in raw_result.items():
            summary[f"{col}_mean"] = stats["mean"]
            summary[f"{col}_std"] = stats["std"]
            
            # Check for normality
            if stats.get("shapiro_p") and stats["shapiro_p"] > 0.05:
                summary[f"{col}_distribution"] = "approximately normal"
            else:
                summary[f"{col}_distribution"] = "non-normal"
            
            all_stats.append({
                "variable": col,
                **stats
            })
        
        # Create interpretation
        interpretations = []
        for col, stats in raw_result.items():
            cv = stats.get("cv")
            if cv and cv > 1:
                interpretations.append(f"{col} has high variability (CV={cv:.2f})")
            
            skew = stats.get("skewness")
            if skew and abs(skew) > 1:
                interpretations.append(f"{col} is {'right' if skew > 0 else 'left'}-skewed")
        
        # Visualization suggestions
        viz_suggestions = [
            {"type": "histogram", "purpose": "Show distribution shape"},
            {"type": "boxplot", "purpose": "Identify outliers and quartiles"},
            {"type": "qq_plot", "purpose": "Check normality assumption"}
        ]
        
        return FlexibleToolOutput(
            summary=summary,
            tables=all_stats,
            statistics={"overall_n_variables": len(raw_result)},
            interpretation=" ".join(interpretations) if interpretations else "All variables appear well-behaved.",
            visualizations=viz_suggestions,
            next_steps=[
                "Check correlations between variables",
                "Test for outliers using IQR method",
                "Perform normality tests on key variables"
            ],
            raw=raw_result
        )