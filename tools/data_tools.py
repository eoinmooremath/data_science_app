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
    @property
    def name(self) -> str:
        return "get_data_info"
    
    @property
    def description(self) -> str:
        return "Get information about uploaded datasets including shape, columns, and basic statistics"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return DataInfoInput
    
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
    @property
    def name(self) -> str:
        return "analyze_uploaded_data"
    
    @property
    def description(self) -> str:
        return "Analyze uploaded data with various statistical methods"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return AnalyzeUploadedDataInput
    
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
    
    @property
    def name(self) -> str:
        return "upload_data"
    
    @property
    def description(self) -> str:
        return "Upload CSV data for analysis"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return DataUploadInput
    
    @property
    def estimated_duration(self) -> float:
        return 2.0
    
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute data upload"""
        try:
            # Parse CSV content
            df = pd.read_csv(io.StringIO(inputs.file_content))
            
            # Store in global datasets
            uploaded_datasets['uploaded'] = df
            
            # Send progress update
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 50, "status": "Parsing CSV data..."}
            ))
            
            # Analyze the data
            info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "sample": df.head().to_dict()
            }
            
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 100, "status": "Upload complete!"}
            ))
            
            return {
                "success": True,
                "filename": inputs.filename,
                "info": info,
                "message": f"Successfully uploaded {inputs.filename} with {df.shape[0]} rows and {df.shape[1]} columns"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to upload data: {str(e)}"
            }

class CodeExecutionTool(BaseTool):
    """Tool for executing Python code, especially for data generation"""
    
    @property
    def name(self) -> str:
        return "execute_python_code"
    
    @property
    def description(self) -> str:
        return """Execute Python code for data generation, analysis, or other tasks.
        
        Perfect for:
        - Generating complex datasets with specific statistical properties
        - Creating synthetic data with custom distributions
        - Data preprocessing and transformation
        - Statistical calculations
        
        The code has access to common libraries (pandas, numpy, scipy, etc.) and can store
        results in the global 'uploaded_datasets' dictionary for use by other tools."""
    
    @property
    def input_model(self) -> type[ToolInput]:
        return CodeExecutionInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0
    
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute Python code safely"""
        try:
            # Send progress update
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 20, "status": "Preparing code execution..."}
            ))
            
            # Prepare execution environment
            exec_globals = {
                # Standard libraries
                'pd': pd,
                'pandas': pd,
                'np': np,
                'numpy': np,
                
                # Data storage
                'uploaded_datasets': uploaded_datasets,
                
                # Common imports that might be needed
                '__builtins__': __builtins__,
            }
            
            # Try to import additional libraries that might be used
            try:
                import scipy
                import scipy.stats
                exec_globals['scipy'] = scipy
            except ImportError:
                pass
            
            try:
                import matplotlib.pyplot as plt
                exec_globals['plt'] = plt
            except ImportError:
                pass
            
            try:
                import seaborn as sns
                exec_globals['sns'] = sns
            except ImportError:
                pass
            
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 50, "status": "Executing code..."}
            ))
            
            # Capture stdout and stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Execute the code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(inputs.code, exec_globals)
            
            # Get captured output
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 80, "status": "Processing results..."}
            ))
            
            # Check what datasets were created/modified
            dataset_info = {}
            for name, df in uploaded_datasets.items():
                if isinstance(df, pd.DataFrame):
                    dataset_info[name] = {
                        "shape": df.shape,
                        "columns": df.columns.tolist(),
                        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                        "sample": df.head(3).to_dict() if len(df) > 0 else {}
                    }
            
            self.message_bus.publish(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                content={"progress": 100, "status": "Code execution complete!"}
            ))
            
            # Prepare result message
            result_parts = []
            if inputs.description:
                result_parts.append(f"**{inputs.description}**")
            
            if stdout_output.strip():
                result_parts.append(f"**Output:**\n```\n{stdout_output.strip()}\n```")
            
            if dataset_info:
                result_parts.append("**Datasets created/updated:**")
                for name, info in dataset_info.items():
                    result_parts.append(f"- `{name}`: {info['shape'][0]} rows × {info['shape'][1]} columns")
            
            if stderr_output.strip():
                result_parts.append(f"**Warnings:**\n```\n{stderr_output.strip()}\n```")
            
            return {
                "success": True,
                "code": inputs.code,
                "stdout": stdout_output,
                "stderr": stderr_output,
                "datasets": dataset_info,
                "message": "\n\n".join(result_parts) if result_parts else "Code executed successfully."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": inputs.code,
                "message": f"**Code execution failed:**\n```\n{str(e)}\n```\n\nPlease check your code and try again."
            }