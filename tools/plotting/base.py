# tools/plotting/base.py
from abc import abstractmethod
import pandas as pd
import plotly.express as px
from typing import Dict, Any

from tools.base import BaseTool
from core.models import ToolInput
from core.plot_manager import global_plot_manager
from tools.data_tools import uploaded_datasets

class BasePlottingTool(BaseTool):
    """
    A base class for all plotting tools that use Plotly Express.
    This class handles the common logic for looking up data,
    validating columns, and publishing the plot.
    """

    _plot_function: staticmethod = None

    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """
        Standard execution pipeline for all plotting tools.
        """
        self.update_progress(job_id, 0, f"Initializing {self.name}...")

        # 1. Get the dataset
        dataset_id = getattr(inputs, 'dataset_id', 'generated')
        if dataset_id not in uploaded_datasets:
            return {"error": f"Dataset '{dataset_id}' not found."}
        df = uploaded_datasets[dataset_id]
        self.update_progress(job_id, 20, "Dataset found.")

        # 2. (Optional) Validate columns if the input model specifies them
        # The Pydantic model itself should handle the presence of x, y, etc.
        # Here, we just check if the named columns exist in the dataframe.
        for field in inputs.model_fields:
            if field.endswith("_column") or field in ['x', 'y', 'color', 'facet_row', 'facet_col', 'size', 'hover_data']:
                column_name = getattr(inputs, field)
                if column_name and column_name not in df.columns:
                    return {"error": f"Column '{column_name}' not found in dataset '{dataset_id}'. Available: {list(df.columns)}"}
        
        self.update_progress(job_id, 40, "Columns validated.")

        # 3. Create the figure using the subclass's _plot_function
        try:
            # Get the dynamically attached plot function
            plot_function = self._plot_function
            
            # Extract custom parameters that aren't native to Plotly Express
            marker_symbol = getattr(inputs, 'marker_symbol', None)
            marker_size = getattr(inputs, 'marker_size', None)
            
            # Prepare the arguments for the plotting function
            plot_args = inputs.model_dump(exclude={'dataset_id', 'title', 'marker_symbol', 'marker_size'}, exclude_none=True)
            
            # Rename back to 'color' and 'symbol' for the plotly call
            if 'color_by_column' in plot_args:
                plot_args['color'] = plot_args.pop('color_by_column')
            if 'symbol_by_column' in plot_args:
                plot_args['symbol'] = plot_args.pop('symbol_by_column')

            # The dataframe is passed separately, so remove it from kwargs
            plot_args.pop('data_frame', None)

            fig = plot_function(**plot_args, data_frame=df)
            
            # Set title if provided
            if hasattr(inputs, 'title') and inputs.title:
                fig.update_layout(title_text=inputs.title)

            # Handle our custom marker parameters
            if marker_symbol:
                fig.update_traces(marker_symbol=marker_symbol)
            if marker_size:
                fig.update_traces(marker_size=marker_size)
                
        except Exception as e:
            return {"error": f"Failed to create plot: {e}"}
            
        self.update_progress(job_id, 80, "Figure created, publishing...")

        # 4. Publish the plot
        fig_data = fig.to_dict()
        title = getattr(inputs, 'title', 'Untitled Plot')
        global_plot_manager.add_new_plot(job_id, fig_data, title)
        
        self.update_progress(job_id, 100, "Plotting complete.")
        
        return {
            "success": True,
            "message": f"Successfully generated a plot titled '{title}'.",
            "plot_id": job_id,
        } 