"""
Sklearn and Statsmodels Tools - Adapted from MCP server for the Dash UI
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# sklearn imports
import sklearn
from sklearn import (
    preprocessing, decomposition, ensemble, linear_model,
    svm, tree, neural_network, cluster, metrics, 
    feature_selection, model_selection, pipeline
)

# statsmodels imports
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import (
    correlation_tools, outliers_influence, diagnostic,
    weightstats, proportion, power, multitest
)
from statsmodels.tsa import stattools, arima, statespace
from scipy import stats

from tools.base import EnhancedBaseTool, FlexibleToolOutput, ToolInput
from pydantic import Field, BaseModel
from core.models import Job

# Global storage for fitted models and data
_session_data = {}
_fitted_models = {}

class SklearnToolInput(ToolInput):
    """Base input for sklearn tools"""
    data: Union[List[List[float]], str] = Field(description="Input data as array or data key")
    target: Optional[Union[List[float], str]] = Field(default=None, description="Target variable")

class PreprocessingScaleInput(SklearnToolInput):
    """Input for scaling tools"""
    scaler_type: str = Field(description="Type of scaler: StandardScaler, MinMaxScaler, RobustScaler, Normalizer")
    feature_range: Optional[tuple] = Field(default=(0, 1), description="Range for MinMaxScaler")

class ModelInput(SklearnToolInput):
    """Input for model tools"""
    model_type: str = Field(description="Type of model")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Model parameters")

class StatsTestInput(ToolInput):
    """Input for statistical tests"""
    data: Union[List[float], str] = Field(description="Data for testing")
    test_type: str = Field(description="Type of test")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Test parameters")

class CorrelationInput(ToolInput):
    """Input for correlation analysis"""
    data: Union[List[List[float]], str] = Field(description="Data for correlation")
    method: str = Field(default="pearson", description="Correlation method: pearson, spearman, kendall")
    x_column: Optional[str] = Field(default=None, description="X variable column name")
    y_column: Optional[str] = Field(default=None, description="Y variable column name")

# Preprocessing Tools
class PreprocessingScaleTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "preprocessing.scale"
    
    @property
    def name(self) -> str:
        return "scale_data"
    
    @property
    def description(self) -> str:
        return "Scale/normalize data using various sklearn scalers"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return PreprocessingScaleInput
    
    def _execute_analysis(self, job_id: str, inputs: PreprocessingScaleInput) -> Any:
        """Execute scaling operation"""
        
        # Get data
        data = self._get_data(inputs.data)
        
        # Select scaler
        scalers = {
            "StandardScaler": preprocessing.StandardScaler(),
            "MinMaxScaler": preprocessing.MinMaxScaler(feature_range=inputs.feature_range),
            "RobustScaler": preprocessing.RobustScaler(),
            "Normalizer": preprocessing.Normalizer()
        }
        
        if inputs.scaler_type not in scalers:
            raise ValueError(f"Unknown scaler type: {inputs.scaler_type}")
        
        scaler = scalers[inputs.scaler_type]
        
        self.update_progress(job_id, 30, f"Fitting {inputs.scaler_type}...")
        
        # Fit and transform
        scaled_data = scaler.fit_transform(data)
        
        self.update_progress(job_id, 80, "Storing results...")
        
        # Store results
        data_key = self._store_data(scaled_data, f"Scaled with {inputs.scaler_type}")
        model_key = self._store_model(scaler, f"{inputs.scaler_type}_scaler")
        
        return {
            "scaler_type": inputs.scaler_type,
            "data_key": data_key,
            "model_key": model_key,
            "original_shape": data.shape,
            "scaled_shape": scaled_data.shape,
            "scaler_params": scaler.get_params()
        }
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        return FlexibleToolOutput(
            summary={
                "scaler": raw_result["scaler_type"],
                "shape": raw_result["scaled_shape"],
                "data_key": raw_result["data_key"]
            },
            statistics={
                "original_features": raw_result["original_shape"][1] if len(raw_result["original_shape"]) > 1 else 1,
                "scaled_features": raw_result["scaled_shape"][1] if len(raw_result["scaled_shape"]) > 1 else 1
            },
            interpretation=f"Successfully scaled data using {raw_result['scaler_type']}",
            next_steps=[
                "Use the scaled data for machine learning models",
                "Check the distribution of scaled features",
                "Apply the same scaler to test data"
            ]
        )

# Model Tools
class ModelTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "models.sklearn"
    
    @property
    def name(self) -> str:
        return "train_model"
    
    @property
    def description(self) -> str:
        return "Train various sklearn models (classification, regression, clustering)"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return ModelInput
    
    def _execute_analysis(self, job_id: str, inputs: ModelInput) -> Any:
        """Execute model training"""
        
        # Get data
        data = self._get_data(inputs.data)
        target = self._get_data(inputs.target) if inputs.target else None
        
        # Model registry
        models = {
            # Classification
            "LogisticRegression": linear_model.LogisticRegression,
            "RandomForestClassifier": ensemble.RandomForestClassifier,
            "SVC": svm.SVC,
            
            # Regression
            "LinearRegression": linear_model.LinearRegression,
            "RandomForestRegressor": ensemble.RandomForestRegressor,
            "Ridge": linear_model.Ridge,
            "Lasso": linear_model.Lasso,
            
            # Clustering
            "KMeans": cluster.KMeans,
            "DBSCAN": cluster.DBSCAN,
            "AgglomerativeClustering": cluster.AgglomerativeClustering,
        }
        
        if inputs.model_type not in models:
            raise ValueError(f"Unknown model type: {inputs.model_type}")
        
        self.update_progress(job_id, 20, f"Initializing {inputs.model_type}...")
        
        # Create and train model
        model_class = models[inputs.model_type]
        model = model_class(**inputs.parameters)
        
        self.update_progress(job_id, 50, "Training model...")
        
        if target is not None:
            # Supervised learning
            model.fit(data, target)
        else:
            # Unsupervised learning
            model.fit(data)
        
        self.update_progress(job_id, 80, "Storing model...")
        
        # Store model
        model_key = self._store_model(model, f"{inputs.model_type}_model")
        
        # Get model-specific results
        results = {
            "model_type": inputs.model_type,
            "model_key": model_key,
            "parameters": inputs.parameters,
            "data_shape": data.shape
        }
        
        # Add model-specific metrics
        if hasattr(model, 'feature_importances_'):
            results["feature_importances"] = model.feature_importances_.tolist()
        
        if hasattr(model, 'coef_'):
            results["coefficients"] = model.coef_.tolist()
        
        if hasattr(model, 'score') and target is not None:
            results["score"] = model.score(data, target)
        
        if hasattr(model, 'labels_'):  # Clustering
            results["labels"] = model.labels_.tolist()
            results["n_clusters"] = len(np.unique(model.labels_))
        
        return results
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        interpretation = f"Successfully trained {raw_result['model_type']} model"
        
        if "score" in raw_result:
            interpretation += f" with score: {raw_result['score']:.3f}"
        
        if "n_clusters" in raw_result:
            interpretation += f" found {raw_result['n_clusters']} clusters"
        
        return FlexibleToolOutput(
            summary={
                "model": raw_result["model_type"],
                "model_key": raw_result["model_key"],
                "data_shape": raw_result["data_shape"]
            },
            statistics={k: v for k, v in raw_result.items() if k in ["score", "n_clusters"]},
            interpretation=interpretation,
            next_steps=[
                "Evaluate model performance",
                "Make predictions on new data",
                "Tune hyperparameters if needed"
            ]
        )

# Statistical Tests Tool
class StatisticalTestsTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "stats.tests"
    
    @property
    def name(self) -> str:
        return "hypothesis_test"
    
    @property
    def description(self) -> str:
        return "Perform various statistical hypothesis tests"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return StatsTestInput
    
    def _execute_analysis(self, job_id: str, inputs: StatsTestInput) -> Any:
        """Execute statistical test"""
        
        data = self._get_data(inputs.data)
        
        # Test registry
        tests = {
            "ttest_1samp": stats.ttest_1samp,
            "ttest_ind": stats.ttest_ind,
            "ttest_rel": stats.ttest_rel,
            "anova_oneway": stats.f_oneway,
            "kruskal": stats.kruskal,
            "mannwhitneyu": stats.mannwhitneyu,
            "chi2_test": stats.chi2_contingency,
            "normality_test": stats.normaltest,
            "levene_test": stats.levene,
            "shapiro": stats.shapiro,
            "anderson": stats.anderson
        }
        
        if inputs.test_type not in tests:
            raise ValueError(f"Unknown test type: {inputs.test_type}")
        
        self.update_progress(job_id, 50, f"Running {inputs.test_type}...")
        
        test_func = tests[inputs.test_type]
        
        # Execute test with parameters
        if inputs.test_type == "ttest_1samp":
            popmean = inputs.parameters.get("popmean", 0)
            statistic, pvalue = test_func(data, popmean)
        else:
            result = test_func(data, **inputs.parameters)
            if isinstance(result, tuple) and len(result) >= 2:
                statistic, pvalue = result[0], result[1]
            else:
                statistic, pvalue = result, None
        
        # Interpret results
        interpretation = self._interpret_test(pvalue) if pvalue is not None else "Test completed"
        
        return {
            "test_type": inputs.test_type,
            "statistic": float(statistic),
            "p_value": float(pvalue) if pvalue is not None else None,
            "interpretation": interpretation,
            "parameters": inputs.parameters
        }
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        return FlexibleToolOutput(
            summary={
                "test": raw_result["test_type"],
                "statistic": raw_result["statistic"],
                "p_value": raw_result["p_value"]
            },
            statistics={
                "test_statistic": raw_result["statistic"],
                "p_value": raw_result["p_value"]
            },
            interpretation=raw_result["interpretation"],
            next_steps=[
                "Check test assumptions",
                "Consider effect size",
                "Validate with additional tests"
            ]
        )

# Correlation Analysis Tool
class CorrelationAnalysisTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "stats.correlation"
    
    @property
    def name(self) -> str:
        return "correlation_analysis"
    
    @property
    def description(self) -> str:
        return "Perform correlation analysis using various methods"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return CorrelationInput
    
    def _execute_analysis(self, job_id: str, inputs: CorrelationInput) -> Any:
        """Execute correlation analysis"""
        
        data = self._get_data(inputs.data)
        
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
        
        self.update_progress(job_id, 30, f"Computing {inputs.method} correlation...")
        
        if inputs.x_column and inputs.y_column:
            # Pairwise correlation
            x = df[inputs.x_column]
            y = df[inputs.y_column]
            
            if inputs.method == "pearson":
                corr, pvalue = stats.pearsonr(x, y)
            elif inputs.method == "spearman":
                corr, pvalue = stats.spearmanr(x, y)
            elif inputs.method == "kendall":
                corr, pvalue = stats.kendalltau(x, y)
            else:
                raise ValueError(f"Unknown correlation method: {inputs.method}")
            
            result = {
                "type": "pairwise",
                "method": inputs.method,
                "correlation": float(corr),
                "p_value": float(pvalue),
                "variables": [inputs.x_column, inputs.y_column],
                "interpretation": self._interpret_correlation(corr, pvalue)
            }
        else:
            # Correlation matrix
            if inputs.method == "pearson":
                corr_matrix = df.corr(method="pearson")
            elif inputs.method == "spearman":
                corr_matrix = df.corr(method="spearman")
            elif inputs.method == "kendall":
                corr_matrix = df.corr(method="kendall")
            else:
                raise ValueError(f"Unknown correlation method: {inputs.method}")
            
            result = {
                "type": "matrix",
                "method": inputs.method,
                "matrix": corr_matrix.values.tolist(),
                "columns": list(corr_matrix.columns),
                "shape": corr_matrix.shape,
                "interpretation": f"Computed {inputs.method} correlation matrix"
            }
        
        return result
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        if raw_result["type"] == "pairwise":
            return FlexibleToolOutput(
                summary={
                    "correlation": raw_result["correlation"],
                    "p_value": raw_result["p_value"],
                    "method": raw_result["method"]
                },
                statistics={
                    "correlation_coefficient": raw_result["correlation"],
                    "p_value": raw_result["p_value"]
                },
                interpretation=raw_result["interpretation"],
                next_steps=[
                    "Visualize the relationship with a scatter plot",
                    "Check for non-linear relationships",
                    "Consider partial correlation"
                ]
            )
        else:
            return FlexibleToolOutput(
                summary={
                    "matrix_shape": raw_result["shape"],
                    "method": raw_result["method"],
                    "variables": len(raw_result["columns"])
                },
                tables=[{
                    "variable_1": raw_result["columns"][i],
                    "variable_2": raw_result["columns"][j],
                    "correlation": raw_result["matrix"][i][j]
                } for i in range(len(raw_result["columns"])) 
                  for j in range(i+1, len(raw_result["columns"]))],
                interpretation=raw_result["interpretation"],
                next_steps=[
                    "Identify strongest correlations",
                    "Create correlation heatmap",
                    "Check for multicollinearity"
                ]
            )

    # Helper methods
    def _get_data(self, data_input: Union[List, str, None]) -> np.ndarray:
        """Get data from input (array or stored key)"""
        if data_input is None:
            return None
        
        if isinstance(data_input, str):
            # Data key reference
            if data_input in _session_data:
                return _session_data[data_input]["data"]
            else:
                raise ValueError(f"Data key '{data_input}' not found")
        else:
            # Direct data
            return np.array(data_input)
    
    def _store_data(self, data: np.ndarray, description: str) -> str:
        """Store data and return key"""
        data_key = f"data_{len(_session_data)}"
        _session_data[data_key] = {
            "data": data,
            "shape": data.shape,
            "description": description
        }
        return data_key
    
    def _store_model(self, model: Any, description: str) -> str:
        """Store model and return key"""
        model_key = f"model_{len(_fitted_models)}"
        _fitted_models[model_key] = {
            "model": model,
            "description": description
        }
        return model_key
    
    def _interpret_correlation(self, corr: float, pvalue: float) -> str:
        """Interpret correlation results"""
        strength = ""
        if abs(corr) < 0.3:
            strength = "weak"
        elif abs(corr) < 0.7:
            strength = "moderate"
        else:
            strength = "strong"
        
        direction = "positive" if corr > 0 else "negative"
        significance = "significant" if pvalue < 0.05 else "not significant"
        
        return f"{strength} {direction} correlation, {significance} at α=0.05 (r={corr:.3f}, p={pvalue:.3f})"
    
    def _interpret_test(self, pvalue: float, alpha: float = 0.05) -> str:
        """Interpret hypothesis test results"""
        if pvalue < alpha:
            return f"Reject null hypothesis at α={alpha} (p={pvalue:.4f})"
        else:
            return f"Fail to reject null hypothesis at α={alpha} (p={pvalue:.4f})"

# Add the helper methods to all tool classes
for tool_class in [PreprocessingScaleTool, ModelTool, StatisticalTestsTool]:
    tool_class._get_data = CorrelationAnalysisTool._get_data
    tool_class._store_data = CorrelationAnalysisTool._store_data
    tool_class._store_model = CorrelationAnalysisTool._store_model
    tool_class._interpret_correlation = CorrelationAnalysisTool._interpret_correlation
    tool_class._interpret_test = CorrelationAnalysisTool._interpret_test 