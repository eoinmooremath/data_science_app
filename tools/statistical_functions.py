"""
Statistical Functions Tools - Unified system for scipy.stats and statsmodels

This module provides a unified interface to statistical functions from scipy.stats and statsmodels,
following the same pattern as the plotting tools with wrapper classes matching function arguments.

Hierarchical organization allows LLM to reason at different levels:
- "I need a t-test" → explores stats.tests.t_test.*
- "I need regression" → explores stats.regression.*
- "I need time series analysis" → explores stats.timeseries.*
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Union
from pydantic import Field, BaseModel

from tools.base import BaseTool
from core.models import ToolInput, Message, MessageType

# Import statistical libraries
try:
    import scipy.stats as scipy_stats
    import statsmodels.api as sm
    import statsmodels.stats.api as sms
    import statsmodels.tsa.api as tsa
    SCIPY_AVAILABLE = True
    STATSMODELS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Statistical libraries not available: {e}")
    SCIPY_AVAILABLE = False
    STATSMODELS_AVAILABLE = False


# =============================================================================
# BASE CLASSES FOR STATISTICAL TOOLS
# =============================================================================

class BaseStatisticalTool(BaseTool):
    """Base class for all statistical function tools"""
    
    def __init__(self, message_bus=None, job_manager=None):
        super().__init__(message_bus, job_manager)
        self._function = None
    
    @property
    def estimated_duration(self) -> float:
        return 3.0  # Most statistical tests are quick
    
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute the statistical function"""
        
        # Start progress
        self.update_progress(job_id, 0, f"Starting {self.name}...")
        time.sleep(0.2)
        
        try:
            # Get data from inputs
            data_dict = self._prepare_data(inputs)
            
            # Update progress
            self.update_progress(job_id, 30, "Preparing data...")
            time.sleep(0.3)
            
            # Execute the statistical function
            self.update_progress(job_id, 60, "Running statistical analysis...")
            result = self._execute_function(data_dict, inputs)
            time.sleep(0.3)
            
            # Process and format results
            self.update_progress(job_id, 90, "Processing results...")
            formatted_result = self._format_results(result, inputs)
            time.sleep(0.2)
            
            # Create visualization if applicable
            if hasattr(inputs, 'create_plot') and getattr(inputs, 'create_plot', False):
                self._create_visualization(job_id, result, inputs)
            
            # Complete
            self.update_progress(job_id, 100, "Analysis complete!")
            
            return formatted_result
            
        except Exception as e:
            self.update_progress(job_id, 100, f"Error: {str(e)}")
            return {"error": str(e), "success": False}
    
    def _prepare_data(self, inputs: ToolInput) -> Dict[str, Any]:
        """Prepare data for the statistical function"""
        data_dict = {}
        
        # Extract data from inputs
        for field_name, field_info in inputs.__fields__.items():
            value = getattr(inputs, field_name, None)
            if value is not None:
                data_dict[field_name] = value
        
        return data_dict
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: ToolInput) -> Any:
        """Execute the actual statistical function - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement _execute_function")
    
    def _format_results(self, result: Any, inputs: ToolInput) -> Dict[str, Any]:
        """Format results for return to Claude"""
        if hasattr(result, '_asdict'):  # Named tuple
            return result._asdict()
        elif isinstance(result, tuple):
            # Try to create meaningful names for tuple elements
            if len(result) == 2:
                return {"statistic": float(result[0]), "p_value": float(result[1])}
            elif len(result) == 3:
                return {"statistic": float(result[0]), "p_value": float(result[1]), "additional": result[2]}
            else:
                return {"result": result}
        elif isinstance(result, (int, float)):
            return {"result": float(result)}
        elif hasattr(result, 'summary'):  # Statsmodels result
            return {
                "summary": str(result.summary()),
                "params": result.params.to_dict() if hasattr(result, 'params') else None,
                "pvalues": result.pvalues.to_dict() if hasattr(result, 'pvalues') else None,
                "rsquared": getattr(result, 'rsquared', None),
                "aic": getattr(result, 'aic', None),
                "bic": getattr(result, 'bic', None)
            }
        else:
            return {"result": str(result)}
    
    def _create_visualization(self, job_id: str, result: Any, inputs: ToolInput):
        """Create visualization if applicable"""
        # This can be overridden by specific tools that support visualization
        pass


# =============================================================================
# SCIPY.STATS TOOLS
# =============================================================================

# Descriptive Statistics
class DescribeInput(ToolInput):
    data: List[float] = Field(description="Data array for descriptive statistics")
    axis: Optional[int] = Field(default=None, description="Axis along which to compute statistics")
    ddof: int = Field(default=1, description="Delta degrees of freedom")
    bias: bool = Field(default=True, description="If False, use unbiased estimators")
    nan_policy: str = Field(default='propagate', description="How to handle NaN values: 'propagate', 'raise', 'omit'")
    create_plot: bool = Field(default=False, description="Whether to create a visualization")

class DescribeTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_describe"
    
    @property
    def description(self) -> str:
        return "Compute descriptive statistics including mean, std, min, max, skewness, kurtosis"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return DescribeInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: DescribeInput) -> Any:
        data = np.array(data_dict['data'])
        return scipy_stats.describe(
            data,
            axis=data_dict.get('axis'),
            ddof=data_dict.get('ddof', 1),
            bias=data_dict.get('bias', True),
            nan_policy=data_dict.get('nan_policy', 'propagate')
        )


# T-Tests
class TTestInput(ToolInput):
    sample1: List[float] = Field(description="First sample data")
    sample2: Optional[List[float]] = Field(default=None, description="Second sample data (for two-sample test)")
    popmean: float = Field(default=0.0, description="Population mean for one-sample test")
    alternative: str = Field(default='two-sided', description="Alternative hypothesis: 'two-sided', 'less', 'greater'")
    equal_var: bool = Field(default=True, description="Assume equal variances for two-sample test")
    nan_policy: str = Field(default='propagate', description="How to handle NaN values")
    create_plot: bool = Field(default=False, description="Whether to create a visualization")

class TTestTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_ttest"
    
    @property
    def description(self) -> str:
        return "Perform one-sample or two-sample t-test"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return TTestInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: TTestInput) -> Any:
        sample1 = np.array(data_dict['sample1'])
        
        if data_dict.get('sample2') is not None:
            # Two-sample t-test
            sample2 = np.array(data_dict['sample2'])
            return scipy_stats.ttest_ind(
                sample1, sample2,
                equal_var=data_dict.get('equal_var', True),
                nan_policy=data_dict.get('nan_policy', 'propagate'),
                alternative=data_dict.get('alternative', 'two-sided')
            )
        else:
            # One-sample t-test
            return scipy_stats.ttest_1samp(
                sample1,
                popmean=data_dict.get('popmean', 0.0),
                nan_policy=data_dict.get('nan_policy', 'propagate'),
                alternative=data_dict.get('alternative', 'two-sided')
            )


# Chi-square tests
class ChiSquareInput(ToolInput):
    observed: List[float] = Field(description="Observed frequencies")
    expected: Optional[List[float]] = Field(default=None, description="Expected frequencies (if None, assumes uniform)")
    ddof: int = Field(default=0, description="Delta degrees of freedom")
    axis: Optional[int] = Field(default=None, description="Axis along which to compute test")
    create_plot: bool = Field(default=False, description="Whether to create a visualization")

class ChiSquareTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_chisquare"
    
    @property
    def description(self) -> str:
        return "Perform chi-square goodness of fit test"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return ChiSquareInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: ChiSquareInput) -> Any:
        observed = np.array(data_dict['observed'])
        expected = data_dict.get('expected')
        if expected is not None:
            expected = np.array(expected)
        
        return scipy_stats.chisquare(
            observed,
            f_exp=expected,
            ddof=data_dict.get('ddof', 0),
            axis=data_dict.get('axis')
        )


# Normality tests
class NormalityTestInput(ToolInput):
    data: List[float] = Field(description="Data to test for normality")
    test_type: str = Field(default='shapiro', description="Test type: 'shapiro', 'normaltest', 'jarque_bera', 'anderson'")
    nan_policy: str = Field(default='propagate', description="How to handle NaN values")
    create_plot: bool = Field(default=False, description="Whether to create a Q-Q plot")

class NormalityTestTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_normality_test"
    
    @property
    def description(self) -> str:
        return "Test data for normality using various tests (Shapiro-Wilk, D'Agostino, Jarque-Bera, Anderson-Darling)"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return NormalityTestInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: NormalityTestInput) -> Any:
        data = np.array(data_dict['data'])
        test_type = data_dict.get('test_type', 'shapiro')
        
        if test_type == 'shapiro':
            return scipy_stats.shapiro(data)
        elif test_type == 'normaltest':
            return scipy_stats.normaltest(data, nan_policy=data_dict.get('nan_policy', 'propagate'))
        elif test_type == 'jarque_bera':
            return scipy_stats.jarque_bera(data)
        elif test_type == 'anderson':
            return scipy_stats.anderson(data, dist='norm')
        else:
            raise ValueError(f"Unknown test type: {test_type}")


# Correlation tests
class CorrelationTestInput(ToolInput):
    x: List[float] = Field(description="First variable")
    y: List[float] = Field(description="Second variable")
    method: str = Field(default='pearson', description="Correlation method: 'pearson', 'spearman', 'kendalltau'")
    alternative: str = Field(default='two-sided', description="Alternative hypothesis")
    nan_policy: str = Field(default='propagate', description="How to handle NaN values")
    create_plot: bool = Field(default=False, description="Whether to create a scatter plot")

class CorrelationTestTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_correlation_test"
    
    @property
    def description(self) -> str:
        return "Test correlation between two variables using Pearson, Spearman, or Kendall's tau"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return CorrelationTestInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: CorrelationTestInput) -> Any:
        x = np.array(data_dict['x'])
        y = np.array(data_dict['y'])
        method = data_dict.get('method', 'pearson')
        
        if method == 'pearson':
            return scipy_stats.pearsonr(x, y, alternative=data_dict.get('alternative', 'two-sided'))
        elif method == 'spearman':
            return scipy_stats.spearmanr(x, y, alternative=data_dict.get('alternative', 'two-sided'),
                                       nan_policy=data_dict.get('nan_policy', 'propagate'))
        elif method == 'kendalltau':
            return scipy_stats.kendalltau(x, y, alternative=data_dict.get('alternative', 'two-sided'),
                                        nan_policy=data_dict.get('nan_policy', 'propagate'))
        else:
            raise ValueError(f"Unknown correlation method: {method}")


# =============================================================================
# STATSMODELS TOOLS
# =============================================================================

# Linear Regression
class LinearRegressionInput(ToolInput):
    y: List[float] = Field(description="Dependent variable")
    X: List[List[float]] = Field(description="Independent variables (2D array)")
    add_constant: bool = Field(default=True, description="Whether to add intercept term")
    method: str = Field(default='OLS', description="Regression method: 'OLS', 'WLS', 'GLS'")
    weights: Optional[List[float]] = Field(default=None, description="Weights for WLS regression")
    create_plot: bool = Field(default=False, description="Whether to create diagnostic plots")

class LinearRegressionTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_linear_regression"
    
    @property
    def description(self) -> str:
        return "Perform linear regression using OLS, WLS, or GLS"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return LinearRegressionInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0  # Regression takes a bit longer
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: LinearRegressionInput) -> Any:
        y = np.array(data_dict['y'])
        X = np.array(data_dict['X'])
        
        if data_dict.get('add_constant', True):
            X = sm.add_constant(X)
        
        method = data_dict.get('method', 'OLS')
        
        if method == 'OLS':
            model = sm.OLS(y, X)
        elif method == 'WLS':
            weights = data_dict.get('weights')
            if weights is None:
                raise ValueError("Weights required for WLS regression")
            model = sm.WLS(y, X, weights=np.array(weights))
        elif method == 'GLS':
            model = sm.GLS(y, X)
        else:
            raise ValueError(f"Unknown regression method: {method}")
        
        return model.fit()


# Logistic Regression
class LogisticRegressionInput(ToolInput):
    y: List[int] = Field(description="Binary dependent variable (0/1)")
    X: List[List[float]] = Field(description="Independent variables (2D array)")
    add_constant: bool = Field(default=True, description="Whether to add intercept term")
    method: str = Field(default='newton', description="Optimization method")
    create_plot: bool = Field(default=False, description="Whether to create diagnostic plots")

class LogisticRegressionTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_logistic_regression"
    
    @property
    def description(self) -> str:
        return "Perform logistic regression for binary outcomes"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return LogisticRegressionInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: LogisticRegressionInput) -> Any:
        y = np.array(data_dict['y'])
        X = np.array(data_dict['X'])
        
        if data_dict.get('add_constant', True):
            X = sm.add_constant(X)
        
        model = sm.Logit(y, X)
        return model.fit(method=data_dict.get('method', 'newton'))


# ANOVA
class ANOVAInput(ToolInput):
    groups: List[List[float]] = Field(description="List of groups for ANOVA")
    test_type: str = Field(default='one_way', description="ANOVA type: 'one_way', 'two_way'")
    alpha: float = Field(default=0.05, description="Significance level")
    create_plot: bool = Field(default=False, description="Whether to create box plots")

class ANOVATool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_anova"
    
    @property
    def description(self) -> str:
        return "Perform one-way or two-way ANOVA"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return ANOVAInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: ANOVAInput) -> Any:
        groups = [np.array(group) for group in data_dict['groups']]
        test_type = data_dict.get('test_type', 'one_way')
        
        if test_type == 'one_way':
            return scipy_stats.f_oneway(*groups)
        else:
            raise ValueError("Two-way ANOVA not yet implemented")


# Time Series Tests
class TimeSeriesTestInput(ToolInput):
    data: List[float] = Field(description="Time series data")
    test_type: str = Field(default='adf', description="Test type: 'adf' (Augmented Dickey-Fuller), 'kpss', 'ljungbox'")
    lags: Optional[int] = Field(default=None, description="Number of lags to include")
    regression: str = Field(default='c', description="Regression type for ADF: 'c', 'ct', 'ctt', 'nc'")
    create_plot: bool = Field(default=False, description="Whether to create time series plot")

class TimeSeriesTestTool(BaseStatisticalTool):
    @property
    def name(self) -> str:
        return "stats_timeseries_test"
    
    @property
    def description(self) -> str:
        return "Perform time series stationarity and autocorrelation tests"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return TimeSeriesTestInput
    
    def _execute_function(self, data_dict: Dict[str, Any], inputs: TimeSeriesTestInput) -> Any:
        data = np.array(data_dict['data'])
        test_type = data_dict.get('test_type', 'adf')
        
        if test_type == 'adf':
            return tsa.adfuller(
                data,
                maxlag=data_dict.get('lags'),
                regression=data_dict.get('regression', 'c')
            )
        elif test_type == 'kpss':
            return tsa.kpss(data, nlags=data_dict.get('lags'))
        elif test_type == 'ljungbox':
            from statsmodels.stats.diagnostic import acorr_ljungbox
            return acorr_ljungbox(data, lags=data_dict.get('lags', 10))
        else:
            raise ValueError(f"Unknown test type: {test_type}")


# =============================================================================
# TOOL REGISTRY
# =============================================================================

def create_statistical_tools(message_bus=None, job_manager=None) -> List[BaseStatisticalTool]:
    """Create all statistical function tools"""
    
    if not SCIPY_AVAILABLE or not STATSMODELS_AVAILABLE:
        print("Warning: Statistical libraries not available, skipping statistical tools")
        return []
    
    tools = [
        # Descriptive Statistics
        DescribeTool(message_bus, job_manager),
        
        # Statistical Tests
        TTestTool(message_bus, job_manager),
        ChiSquareTool(message_bus, job_manager),
        NormalityTestTool(message_bus, job_manager),
        CorrelationTestTool(message_bus, job_manager),
        ANOVATool(message_bus, job_manager),
        
        # Regression Models
        LinearRegressionTool(message_bus, job_manager),
        LogisticRegressionTool(message_bus, job_manager),
        
        # Time Series
        TimeSeriesTestTool(message_bus, job_manager),
    ]
    
    return tools


# =============================================================================
# HIERARCHICAL ORGANIZATION HELPERS
# =============================================================================

def get_statistical_categories() -> Dict[str, List[str]]:
    """Get hierarchical organization of statistical tools"""
    return {
        "descriptive": [
            "stats_describe"
        ],
        "tests": {
            "parametric": [
                "stats_ttest",
                "stats_anova"
            ],
            "nonparametric": [
                "stats_chisquare"
            ],
            "normality": [
                "stats_normality_test"
            ],
            "correlation": [
                "stats_correlation_test"
            ],
            "timeseries": [
                "stats_timeseries_test"
            ]
        },
        "regression": [
            "stats_linear_regression",
            "stats_logistic_regression"
        ]
    }


def get_tool_suggestions(query: str) -> List[str]:
    """Get tool suggestions based on query"""
    query_lower = query.lower()
    suggestions = []
    
    # Descriptive statistics
    if any(word in query_lower for word in ['describe', 'summary', 'mean', 'std', 'statistics']):
        suggestions.append("stats_describe")
    
    # T-tests
    if any(word in query_lower for word in ['t-test', 'ttest', 'compare means', 'mean difference']):
        suggestions.append("stats_ttest")
    
    # Chi-square
    if any(word in query_lower for word in ['chi-square', 'chisquare', 'goodness of fit', 'categorical']):
        suggestions.append("stats_chisquare")
    
    # Normality
    if any(word in query_lower for word in ['normal', 'normality', 'shapiro', 'gaussian']):
        suggestions.append("stats_normality_test")
    
    # Correlation
    if any(word in query_lower for word in ['correlation', 'pearson', 'spearman', 'kendall', 'relationship']):
        suggestions.append("stats_correlation_test")
    
    # Regression
    if any(word in query_lower for word in ['regression', 'linear model', 'predict']):
        if 'logistic' in query_lower or 'binary' in query_lower:
            suggestions.append("stats_logistic_regression")
        else:
            suggestions.append("stats_linear_regression")
    
    # ANOVA
    if any(word in query_lower for word in ['anova', 'analysis of variance', 'groups']):
        suggestions.append("stats_anova")
    
    # Time series
    if any(word in query_lower for word in ['time series', 'stationarity', 'adf', 'kpss', 'autocorrelation']):
        suggestions.append("stats_timeseries_test")
    
    return suggestions 