"""
Statistical Tools Module

This module provides dynamically generated wrapper classes for statistical functions
from scipy.stats and statsmodels, following the same pattern as the plotting tools.
"""

from .base import BaseStatisticalTool

try:
    from .generated_tools import *
except (ImportError, FileNotFoundError):
    # Generated tools not available yet
    pass

__all__ = ['BaseStatisticalTool'] 