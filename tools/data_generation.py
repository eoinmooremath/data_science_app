# tools/data_generation.py
import numpy as np
import pandas as pd
import plotly.express as px
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import time

from core.models import ToolInput
from tools.base import BaseTool


class DataGenerationInput(BaseModel):
    """Input model for data generation tool"""
    data_type: str = Field(description="Type of data to generate ('scatter', 'time_series', 'categorical', 'distribution', 'correlation')")
    n_points: int = Field(default=100, description="Number of data points to generate")
    
    # Distribution parameters
    distribution: Optional[str] = Field(default="normal", description="Distribution type ('normal', 'uniform', 'exponential', 'beta')")
    correlation: Optional[float] = Field(default=0.7, description="Correlation between variables (for scatter/correlation data)")
    
    # Variable names and properties
    x_name: Optional[str] = Field(default="x", description="Name for x variable")
    y_name: Optional[str] = Field(default="y", description="Name for y variable")
    category_name: Optional[str] = Field(default="category", description="Name for categorical variable")
    
    # Categorical data parameters
    n_categories: Optional[int] = Field(default=3, description="Number of categories to generate")
    category_names: Optional[List[str]] = Field(default=None, description="Custom category names")
    
    # Time series parameters
    trend: Optional[str] = Field(default="none", description="Trend type ('none', 'linear', 'exponential', 'seasonal')")
    noise_level: Optional[float] = Field(default=0.1, description="Amount of noise to add (0-1)")
    
    # Random seed for reproducibility
    random_seed: Optional[int] = Field(default=None, description="Random seed for reproducible data")


class DataGenerationTool(BaseTool):
    """Generate synthetic datasets for visualization and analysis"""
    
    @property
    def name(self) -> str:
        return "generate_data"
    
    @property
    def description(self) -> str:
        return """Generate synthetic datasets for visualization and analysis.
        
        Can create:
        - Scatter plot data with controllable correlation
        - Time series data with trends and seasonality
        - Categorical data with multiple groups
        - Various statistical distributions
        - Correlated multi-variable datasets
        
        Perfect for testing visualizations, demonstrations, or when you need sample data."""
    
    @property
    def input_model(self) -> type[ToolInput]:
        return DataGenerationInput
    
    @property
    def estimated_duration(self) -> float:
        return 1.0
    
    def execute(self, job_id: str, inputs: DataGenerationInput) -> Dict[str, Any]:
        """Execute data generation"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Setting up data generation...")
        
        # Set random seed if provided
        if inputs.random_seed is not None:
            np.random.seed(inputs.random_seed)
        
        # Progress: Generate data
        self.update_progress(job_id, 30, f"Generating {inputs.data_type} data...")
        
        try:
            if inputs.data_type == "scatter":
                df = self._generate_scatter_data(inputs)
            elif inputs.data_type == "time_series":
                df = self._generate_time_series_data(inputs)
            elif inputs.data_type == "categorical":
                df = self._generate_categorical_data(inputs)
            elif inputs.data_type == "distribution":
                df = self._generate_distribution_data(inputs)
            elif inputs.data_type == "correlation":
                df = self._generate_correlation_data(inputs)
            else:
                # Default to scatter
                df = self._generate_scatter_data(inputs)
            
            # Progress: Finalizing
            self.update_progress(job_id, 80, "Finalizing dataset...")
            
            # Store the generated data globally so plotting tools can access it
            self._store_generated_data(df)
            
            # Progress: Complete
            self.update_progress(job_id, 100, "Data generation completed!")
            
            return {
                "data_type": inputs.data_type,
                "n_points": len(df),
                "columns": list(df.columns),
                "data_summary": {
                    "shape": df.shape,
                    "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
                    "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns),
                    "sample_data": df.head().to_dict('records')
                },
                "message": f"Successfully generated {inputs.data_type} dataset with {len(df)} rows and {len(df.columns)} columns"
            }
            
        except Exception as e:
            error_msg = f"Error generating data: {str(e)}"
            return {"error": error_msg}
    
    def _generate_scatter_data(self, inputs: DataGenerationInput) -> pd.DataFrame:
        """Generate scatter plot data with controllable correlation"""
        n = inputs.n_points
        
        if inputs.distribution == "normal":
            x = np.random.normal(0, 1, n)
            # Create correlated y values
            y = inputs.correlation * x + np.sqrt(1 - inputs.correlation**2) * np.random.normal(0, 1, n)
        elif inputs.distribution == "uniform":
            x = np.random.uniform(-2, 2, n)
            y = inputs.correlation * x + np.sqrt(1 - inputs.correlation**2) * np.random.uniform(-1, 1, n)
        else:
            # Default to normal
            x = np.random.normal(0, 1, n)
            y = inputs.correlation * x + np.sqrt(1 - inputs.correlation**2) * np.random.normal(0, 1, n)
        
        df = pd.DataFrame({
            inputs.x_name: x,
            inputs.y_name: y
        })
        
        # Add some categorical data for color coding
        if inputs.n_categories and inputs.n_categories > 1:
            categories = inputs.category_names or [f"Group {i+1}" for i in range(inputs.n_categories)]
            df[inputs.category_name] = np.random.choice(categories[:inputs.n_categories], n)
        
        return df
    
    def _generate_time_series_data(self, inputs: DataGenerationInput) -> pd.DataFrame:
        """Generate time series data with trends and seasonality"""
        n = inputs.n_points
        
        # Create time index
        dates = pd.date_range(start='2023-01-01', periods=n, freq='D')
        
        # Base values
        values = np.zeros(n)
        
        # Add trend
        if inputs.trend == "linear":
            values += np.linspace(0, 10, n)
        elif inputs.trend == "exponential":
            values += np.exp(np.linspace(0, 2, n)) - 1
        elif inputs.trend == "seasonal":
            values += 5 * np.sin(2 * np.pi * np.arange(n) / 365.25) + 2 * np.sin(2 * np.pi * np.arange(n) / 30)
        
        # Add noise
        values += np.random.normal(0, inputs.noise_level * np.std(values) if np.std(values) > 0 else inputs.noise_level, n)
        
        df = pd.DataFrame({
            'date': dates,
            inputs.y_name: values
        })
        
        return df
    
    def _generate_categorical_data(self, inputs: DataGenerationInput) -> pd.DataFrame:
        """Generate categorical data with multiple groups"""
        n = inputs.n_points
        
        categories = inputs.category_names or [f"Category {i+1}" for i in range(inputs.n_categories)]
        
        # Generate categorical variable
        category_col = np.random.choice(categories, n)
        
        # Generate values that vary by category
        values = []
        for cat in category_col:
            cat_index = categories.index(cat)
            # Each category has a different mean
            mean_val = cat_index * 2
            values.append(np.random.normal(mean_val, 1))
        
        df = pd.DataFrame({
            inputs.category_name: category_col,
            inputs.y_name: values
        })
        
        return df
    
    def _generate_distribution_data(self, inputs: DataGenerationInput) -> pd.DataFrame:
        """Generate data from various statistical distributions"""
        n = inputs.n_points
        
        if inputs.distribution == "normal":
            values = np.random.normal(0, 1, n)
        elif inputs.distribution == "uniform":
            values = np.random.uniform(-2, 2, n)
        elif inputs.distribution == "exponential":
            values = np.random.exponential(1, n)
        elif inputs.distribution == "beta":
            values = np.random.beta(2, 5, n)
        else:
            values = np.random.normal(0, 1, n)
        
        df = pd.DataFrame({
            inputs.x_name: values
        })
        
        return df
    
    def _generate_correlation_data(self, inputs: DataGenerationInput) -> pd.DataFrame:
        """Generate multi-variable correlated data"""
        n = inputs.n_points
        
        # Create correlation matrix
        n_vars = 3
        corr_matrix = np.eye(n_vars)
        corr_matrix[0, 1] = corr_matrix[1, 0] = inputs.correlation
        corr_matrix[0, 2] = corr_matrix[2, 0] = inputs.correlation * 0.5
        corr_matrix[1, 2] = corr_matrix[2, 1] = inputs.correlation * 0.3
        
        # Generate correlated data
        data = np.random.multivariate_normal([0, 0, 0], corr_matrix, n)
        
        df = pd.DataFrame({
            'var1': data[:, 0],
            'var2': data[:, 1],
            'var3': data[:, 2]
        })
        
        return df
    
    def _store_generated_data(self, df: pd.DataFrame):
        """Store generated data so plotting tools can access it"""
        # Store in the global uploaded_datasets store so plotting tools can access it
        from tools.data_tools import uploaded_datasets
        
        # Store with a standard name that plotting tools can find
        uploaded_datasets['generated'] = df
        uploaded_datasets['uploaded'] = df  # Also store as 'uploaded' for default access
        
        print(f"📊 Generated data stored in global data store")
        print(f"📊 Data shape: {df.shape}, Columns: {list(df.columns)}")
        print(f"📊 Available datasets: {list(uploaded_datasets.keys())}") 