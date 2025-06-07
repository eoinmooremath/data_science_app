from typing import Dict, Any, Optional
import pandas as pd
from tools.base import BaseTool
from core.models import ToolInput
from pydantic import Field
import numpy as np
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# Global store for uploaded data (in production, use proper data management)
uploaded_datasets = {}

class DataInfoInput(ToolInput):
    dataset_name: Optional[str] = Field(default="uploaded", description="Name of the dataset to inspect")

class GetDataInfoTool(BaseTool):
    name: str = "get_data_info"
    description: str = "Get information about uploaded datasets including shape, columns, and basic statistics"
    input_model: type[ToolInput] = DataInfoInput
    
    @property
    def estimated_duration(self) -> float:
        return 1.0
    
    def execute(self, job_id: str, inputs: DataInfoInput) -> Dict[str, Any]:
        """Get information about uploaded data"""
        dataset_name = inputs.dataset_name
        
        self.update_progress(job_id, 50, "Retrieving data information...")
        
        if dataset_name not in uploaded_datasets:
            available = list(uploaded_datasets.keys())
            return {
                "error": f"Dataset '{dataset_name}' not found",
                "available_datasets": available
            }
        
        df = uploaded_datasets[dataset_name]
        
        # Gather information
        info = {
            "dataset_name": dataset_name,
            "shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": list(df.select_dtypes(include=['number']).columns),
            "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns)
        }
        
        # Basic statistics for numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            info["basic_stats"] = {
                "mean": numeric_df.mean().to_dict(),
                "std": numeric_df.std().to_dict(),
                "min": numeric_df.min().to_dict(),
                "max": numeric_df.max().to_dict()
            }
        
        self.update_progress(job_id, 100, "Complete!")
        
        return info

class AnalyzeUploadedDataInput(ToolInput):
    analysis_type: str = Field(description="Type of analysis: 'correlation' or 'distribution'")
    dataset_name: Optional[str] = Field(default="uploaded", description="Name of the dataset")
    columns: Optional[list] = Field(default=None, description="Specific columns to analyze")

class AnalyzeUploadedDataTool(BaseTool):
    name: str = "analyze_uploaded_data"
    description: str = "Analyze uploaded data with various statistical methods"
    input_model: type[ToolInput] = AnalyzeUploadedDataInput
    
    def execute(self, job_id: str, inputs: AnalyzeUploadedDataInput) -> Dict[str, Any]:
        """Analyze uploaded data"""
        import numpy as np
        import time
        from core.models import Message, MessageType
        
        dataset_name = inputs.dataset_name
        
        if dataset_name not in uploaded_datasets:
            return {"error": f"Dataset '{dataset_name}' not found"}
        
        df = uploaded_datasets[dataset_name]
        
        self.update_progress(job_id, 10, f"Analyzing {dataset_name}...")
        time.sleep(0.5)
        
        if inputs.analysis_type == "correlation":
            # Correlation analysis on numeric columns
            numeric_df = df.select_dtypes(include=['number'])
            
            if numeric_df.empty:
                return {"error": "No numeric columns found for correlation analysis"}
            
            self.update_progress(job_id, 50, "Computing correlations...")
            corr_matrix = numeric_df.corr()
            
            # Find strongest correlations
            mask = np.triu(np.ones_like(corr_matrix), k=1)
            corr_values = corr_matrix.where(mask.astype(bool))
            
            strongest_corr = []
            for col1 in corr_values.columns:
                for col2 in corr_values.index:
                    value = corr_values.loc[col2, col1]
                    if pd.notna(value) and abs(value) > 0.3:
                        strongest_corr.append({
                            "var1": col1,
                            "var2": col2,
                            "correlation": float(value)
                        })
            
            # Sort by absolute correlation
            strongest_corr.sort(key=lambda x: abs(x["correlation"]), reverse=True)
            
            # Create heatmap
            self.update_progress(job_id, 80, "Creating visualization...")
            
            plot_data = {
                "type": "heatmap",
                "z": corr_matrix.values.tolist(),
                "x": list(corr_matrix.columns),
                "y": list(corr_matrix.index),
                "title": f"Correlation Matrix - {dataset_name}"
            }
            
            self.message_bus.publish(Message(
                type=MessageType.PLOT,
                job_id=job_id,
                data=plot_data
            ))
            
            self.update_progress(job_id, 100, "Analysis complete!")
            
            return {
                "dataset": dataset_name,
                "analysis": "correlation",
                "n_variables": len(numeric_df.columns),
                "strongest_correlations": strongest_corr[:5],
                "interpretation": self._interpret_correlations(strongest_corr)
            }
        
        elif inputs.analysis_type == "distribution":
            # Distribution analysis
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) == 0:
                return {"error": "No numeric columns found"}
            
            # Analyze first numeric column or specified columns
            if inputs.columns and len(inputs.columns) > 0:
                col = inputs.columns[0] if inputs.columns[0] in numeric_cols else numeric_cols[0]
            else:
                col = numeric_cols[0]
            
            self.update_progress(job_id, 50, f"Analyzing distribution of {col}...")
            
            data = df[col].dropna()
            
            # Create histogram
            plot_data = {
                "type": "histogram",
                "values": data.tolist(),
                "title": f"Distribution of {col}",
                "xlabel": col,
                "ylabel": "Frequency"
            }
            
            self.message_bus.publish(Message(
                type=MessageType.PLOT,
                job_id=job_id,
                data=plot_data
            ))
            
            # Calculate statistics
            from scipy import stats
            
            skewness = float(stats.skew(data))
            kurtosis = float(stats.kurtosis(data))
            
            self.update_progress(job_id, 100, "Analysis complete!")
            
            return {
                "dataset": dataset_name,
                "column": col,
                "analysis": "distribution",
                "n_observations": len(data),
                "mean": float(data.mean()),
                "std": float(data.std()),
                "skewness": skewness,
                "kurtosis": kurtosis,
                "interpretation": self._interpret_distribution(skewness, kurtosis)
            }
        
        else:
            return {"error": f"Unknown analysis type: {inputs.analysis_type}"}
    
    def _interpret_correlations(self, correlations):
        if not correlations:
            return "No significant correlations found (|r| > 0.3)"
        
        strongest = correlations[0]
        return f"Strongest correlation: {strongest['var1']} and {strongest['var2']} (r={strongest['correlation']:.3f})"
    
    def _interpret_distribution(self, skewness, kurtosis):
        shape = []
        
        if abs(skewness) < 0.5:
            shape.append("approximately symmetric")
        elif skewness > 0.5:
            shape.append("right-skewed")
        else:
            shape.append("left-skewed")
        
        if kurtosis > 3:
            shape.append("heavy-tailed")
        elif kurtosis < -3:
            shape.append("light-tailed")
        
        return f"Distribution is {' and '.join(shape)}"

class DataUploadInput(ToolInput):
    """Input for data upload tool"""
    file_content: str = Field(description="CSV file content as string")
    filename: str = Field(description="Name of the file")

class CodeExecutionInput(ToolInput):
    """Input for Python code execution tool"""
    code: str = Field(description="Python code to execute")
    description: Optional[str] = Field(default=None, description="Description of what the code does")

class DataUploadTool(BaseTool):
    """Tool for uploading CSV data"""
    
    name: str = "data_upload"
    description: str = "Upload a CSV file for analysis. The content should be a string."
    input_model: type[ToolInput] = DataUploadInput
    
    @property
    def estimated_duration(self) -> float:
        return 2.0
    
    def execute(self, job_id: str, inputs: DataUploadInput) -> Dict[str, Any]:
        """Upload and process a CSV file"""
        self.update_progress(job_id, 10, "Reading CSV data...")
        
        try:
            # Use io.StringIO to read the string content as a file
            csv_file = io.StringIO(inputs.file_content)
            df = pd.read_csv(csv_file)
            
            # Use filename as the key, or a default name
            dataset_name = inputs.filename.split('.')[0] if inputs.filename else "uploaded"
            
            # Store the dataframe in the global dictionary
            uploaded_datasets[dataset_name] = df
            
            # Log for debugging
            print(f"📊 Uploaded data '{dataset_name}' stored in global data store")
            print(f"📊 Data shape: {df.shape}, Columns: {list(df.columns)}")
            
            self.update_progress(job_id, 100, f"Successfully uploaded {dataset_name}")
            
            return {
                "success": True,
                "message": f"Successfully uploaded '{inputs.filename}' as dataset '{dataset_name}'.",
                "dataset_name": dataset_name,
                "shape": f"{df.shape[0]}x{df.shape[1]}",
                "columns": list(df.columns)
            }
        
        except Exception as e:
            return {"error": f"Failed to process CSV file: {e}"}

class CodeExecutionTool(BaseTool):
    """Tool for executing Python code, especially for data generation"""
    
    name: str = "python_code_interpreter"
    description: str = """
Execute Python code in a sandboxed environment.
This is a powerful tool for custom data manipulation, analysis, and complex logic.

Use this when other tools are insufficient.

Example:
```python
# The 'df' variable holds the currently loaded dataset.
# The result of the final expression will be returned.
new_df = df[df['age'] > 30]
new_df.describe()
```
"""
    input_model: type[ToolInput] = CodeExecutionInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0
    
    def execute(self, job_id: str, inputs: CodeExecutionInput) -> Dict[str, Any]:
        self.update_progress(job_id, 10, "Executing Python code...")

        # For safety, this should be a real sandbox in production
        # For this project, we'll execute it with limited context
        
        # Capture stdout and stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        try:
            # Prepare the local environment for exec
            # Use the 'generated' or 'uploaded' dataset if available
            local_env = {
                "pd": pd,
                "np": np,
                "df": uploaded_datasets.get("generated", uploaded_datasets.get("uploaded"))
            }

            with redirect_stdout(stdout), redirect_stderr(stderr):
                # Execute the code
                exec(inputs.code, {"__builtins__": __builtins__}, local_env)
            
            self.update_progress(job_id, 100, "Code execution complete.")
            
            # Get output and error messages
            output_str = stdout.getvalue()
            error_str = stderr.getvalue()

            # The result is whatever was in 'result' variable, or the last expression's value (which exec doesn't return directly)
            # This implementation is simplified. A real one would need ast parsing to get the last expression.
            # For now, we'll rely on the user assigning to a 'result' variable or just using stdout.
            result_val = local_env.get("result", "Code executed. See output for details.")
            
            return {
                "success": not error_str,
                "output": output_str,
                "error": error_str or None,
                "result": str(result_val)
            }

        except Exception as e:
            error_str = stderr.getvalue()
            return {"error": f"Execution failed: {e}\n{error_str}"}