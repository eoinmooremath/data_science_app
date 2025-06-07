# core/plot_manager.py
from typing import Optional, Dict, Any, Tuple
import plotly.graph_objects as go
from ui.components.plot_tabs import PlotHistoryManager

class GlobalPlotManager:
    """Global plot manager that provides access to plot history for tools"""
    
    def __init__(self):
        self._plot_history_manager: Optional[PlotHistoryManager] = None
    
    def set_plot_history_manager(self, plot_history_manager: PlotHistoryManager):
        """Set the plot history manager (called by the app)"""
        self._plot_history_manager = plot_history_manager
    
    def add_new_plot(self, plot_id: str, figure: Dict[str, Any], title: str):
        """Add a new plot to the history"""
        if self._plot_history_manager:
            plot_data = {
                "title": title,
                "figure": go.Figure(figure)
            }
            self._plot_history_manager.add_plot(plot_data, plot_id)
            print(f"✅ Plot for job '{plot_id}' added to history.")
        else:
            print("⚠️ Plot history manager not available. Plot not added.")
    
    def get_latest_plot(self) -> Tuple[Optional[go.Figure], Optional[Dict[str, Any]]]:
        """Get the most recent plot"""
        if not self._plot_history_manager:
            return None, None
        return self._plot_history_manager.get_latest_plot()
    
    def get_plot_by_id(self, plot_id: str) -> Tuple[Optional[go.Figure], Optional[Dict[str, Any]]]:
        """Get a specific plot by ID"""
        if not self._plot_history_manager:
            return None, None
        return self._plot_history_manager.get_plot_by_id(plot_id)
    
    def update_existing_plot(self, plot_id: str, new_figure: go.Figure, new_title: str = None) -> bool:
        """Update an existing plot in place"""
        if not self._plot_history_manager:
            return False
        return self._plot_history_manager.update_existing_plot(plot_id, new_figure, new_title)
    
    def get_all_plot_ids(self) -> list:
        """Get all available plot IDs with their titles"""
        if not self._plot_history_manager:
            return []
        return self._plot_history_manager.get_all_plot_ids()
    
    def is_available(self) -> bool:
        """Check if plot history is available"""
        return self._plot_history_manager is not None

# Global instance
global_plot_manager = GlobalPlotManager() 