# ui/callbacks/plot_callbacks.py
from dash import Input, Output, State, html, dcc, callback_context
from dash.exceptions import PreventUpdate
from ui.state import UIStateManager
from ui.components.plot_tabs import PlotHistoryManager
from core.plot_manager import global_plot_manager
import plotly.graph_objects as go

def register_plot_callbacks(app, ui_state: UIStateManager):
    """Register plot-related callbacks with native Dash graphs"""
    
    # Create a fresh plot history manager for each app instance
    plot_history = PlotHistoryManager()
    
    # Store plot history in app for access
    app.plot_history = plot_history
    
    # Register plot history with global manager for tool access
    global_plot_manager.set_plot_history_manager(plot_history)
    
    print(f"🔄 Plot history manager initialized (fresh start) - {len(plot_history.plot_history)} plots")
    
    @app.callback(
        [Output("main-plots-tabs", "children"),
         Output("main-plots-tabs", "value")],
        [Input("update-interval", "n_intervals")],
        [State("main-plots-tabs", "value")],  # Use State instead of Input to avoid circular dependency
        prevent_initial_call=False  # Allow initial call to force reset
    )
    def update_plot_tabs(n_intervals, current_tab):
        """Update tabs and handle auto-switching to new plots"""
        print(f"🔄 update_plot_tabs called: n_intervals={n_intervals}, current_tab={current_tab}, plots={len(plot_history.plot_history)}")
        
        tabs = []
        for i, plot_info in enumerate(plot_history.plot_history):
            timestamp = plot_info["timestamp"].strftime("%H:%M:%S")
            plot_type = plot_info.get("plot_data", {}).get("type", "plot")
            
            tab_label = f"{plot_type.title()} [{timestamp}]"
            tabs.append(dcc.Tab(
                label=tab_label, 
                value=f"tab-{i}",
                style={"padding": "8px 16px"},
                selected_style={"padding": "8px 16px", "backgroundColor": "#007bff", "color": "white"}
            ))
        
        if not tabs:
            print("📝 No plots found, returning empty tab")
            tabs = [dcc.Tab(
                label="No plots yet", 
                value="tab-empty",
                style={"padding": "8px 16px", "color": "#6c757d"}
            )]
            return tabs, "tab-empty"
        
        print(f"📝 Found {len(tabs)} plot tabs")
        
        # Auto-switch to latest tab if no current tab or current tab is empty
        if len(tabs) > 0 and tabs[0].value != "tab-empty":
            latest_tab = f"tab-{len(tabs)-1}"
            
            if current_tab is None or current_tab == "tab-empty":
                print(f"🔄 Auto-switching to latest tab: {latest_tab}")
                return tabs, latest_tab
        
        # Keep current tab if it's valid
        print(f"🔄 Keeping current tab: {current_tab}")
        return tabs, current_tab or "tab-empty"
    
    @app.callback(
        Output("main-plots-content", "children"),
        [Input("main-plots-tabs", "value"),
         Input("update-interval", "n_intervals")],  # Add interval to catch plot updates
        prevent_initial_call=False  # Allow initial call
    )
    def update_plot_content(active_tab, n_intervals):
        """Update plot content using native Dash Graph component"""
        print(f"🎨 update_plot_content called: active_tab={active_tab}")
        
        if not active_tab or active_tab == "tab-empty":
            print("🎨 Showing empty state")
            return html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line", style={"fontSize": "48px", "color": "#dee2e6"}),
                    html.H5("No visualizations yet", className="mt-3 text-muted"),
                    html.P("Run an analysis to see interactive plots here", className="text-muted")
                ], className="text-center", style={"padding": "60px 20px"})
            ])
        
        try:
            tab_index = int(active_tab.split("-")[1])
            plot_info = plot_history.get_plot_by_index(tab_index)
            
            if plot_info:
                figure = plot_history.get_plot_figure(plot_info["id"])
                
                if figure:
                    print(f"🎨 Rendering plot: {plot_info['id']}")
                    return html.Div([
                        dcc.Graph(
                            figure=figure,
                            style={"height": "450px"},
                            config={
                                'displayModeBar': True,
                                'displaylogo': False,
                                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                                'toImageButtonOptions': {
                                    'format': 'png',
                                    'filename': f"plot_{plot_info['timestamp'].strftime('%Y%m%d_%H%M%S')}",
                                    'height': 500,
                                    'width': 700,
                                    'scale': 1
                                }
                            }
                        ),
                        html.Div([
                            html.Small([
                                html.I(className="fas fa-info-circle me-1"),
                                f"Generated: {plot_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | ",
                                f"Job ID: {plot_info['job_id']}"
                            ], className="text-muted")
                        ], className="mt-2 text-center")
                    ])
                else:
                    print(f"❌ No figure found for plot: {plot_info['id']}")
                    return html.Div([
                        html.Div([
                            html.I(className="fas fa-exclamation-triangle", style={"fontSize": "32px", "color": "#dc3545"}),
                            html.H6("Plot data not found", className="mt-2 text-danger"),
                            html.P("The plot data may have been cleared from cache", className="text-muted")
                        ], className="text-center", style={"padding": "40px 20px"})
                    ])
        except Exception as e:
            print(f"❌ Error in plot callback: {str(e)}")
            return html.Div([
                html.Div([
                    html.I(className="fas fa-bug", style={"fontSize": "32px", "color": "#dc3545"}),
                    html.H6("Error loading plot", className="mt-2 text-danger"),
                    html.P(f"Error: {str(e)}", className="text-muted small")
                ], className="text-center", style={"padding": "40px 20px"})
            ])
        
        return html.Div("Plot not found")