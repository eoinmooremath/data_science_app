"""
Plotting tools package for Data Science UI

Provides hierarchical plotting tools using Plotly Express with:
- Automatic column discovery and validation
- Smart parameter management
- Consistent styling and interactivity
- Future support for plot modifications
"""

from .base import BasePlottingTool
from .suggest import PlotSuggestionTool
# from .edit import PlotEditTool # Temporarily disabled due to refactoring

__all__ = [
    "BasePlottingTool",
    "PlotSuggestionTool",
    # "PlotEditTool" # Temporarily disabled
] 