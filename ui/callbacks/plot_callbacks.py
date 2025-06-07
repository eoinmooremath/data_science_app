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
    
    # Track last rendered state to prevent unnecessary re-renders
    last_rendered_state = {"tab": None, "plot_count": 0, "last_update": None}
    
    # print(f"🔄 Plot history manager initialized (fresh start) - {len(plot_history.plot_history)} plots")
    
    @app.callback(
        [Output("main-plots-tabs", "children"),
         Output("main-plots-tabs", "value")],
        [Input("update-interval", "n_intervals")],
        [State("main-plots-tabs", "value")],  # Use State instead of Input to avoid circular dependency
        prevent_initial_call=False  # Allow initial call to force reset
    )
    def update_plot_tabs(n_intervals, current_tab):
        """Update tabs and handle auto-switching to new plots"""
        # print(f"🔄 update_plot_tabs called: n_intervals={n_intervals}, current_tab={current_tab}, plots={len(plot_history.plot_history)}")
        
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
            # print("📝 No plots found, returning empty tab")
            tabs = [dcc.Tab(
                label="No plots yet", 
                value="tab-empty",
                style={"padding": "8px 16px", "color": "#6c757d"}
            )]
            return tabs, "tab-empty"
        
        # print(f"📝 Found {len(tabs)} plot tabs")
        
        # Auto-switch to latest tab if no current tab or current tab is empty
        if len(tabs) > 0 and tabs[0].value != "tab-empty":
            latest_tab = f"tab-{len(tabs)-1}"
            
            if current_tab is None or current_tab == "tab-empty":
                # print(f"🔄 Auto-switching to latest tab: {latest_tab}")
                return tabs, latest_tab
        
        # Keep current tab if it's valid
        # print(f"🔄 Keeping current tab: {current_tab}")
        return tabs, current_tab or "tab-empty"
    
    @app.callback(
        Output("main-plots-content", "children"),
        [Input("main-plots-tabs", "value"),
         Input("update-interval", "n_intervals")],  # Keep as Input but add logic to prevent unnecessary updates
        prevent_initial_call=False  # Allow initial call
    )
    def update_plot_content(active_tab, n_intervals):
        """Update plot content using native Dash Graph component"""
        # print(f"🎨 update_plot_content called: active_tab={active_tab}")
        
        # Check if we need to update (only update if tab changed or plot was modified)
        current_plot_count = len(plot_history.plot_history)
        current_last_update = None
        has_animation = False
        
        if active_tab and active_tab != "tab-empty":
            try:
                tab_index = int(active_tab.split("-")[1])
                plot_info = plot_history.get_plot_by_index(tab_index)
                if plot_info:
                    current_last_update = plot_info.get("last_updated")
                    # Check if this plot has animation frames
                    figure = plot_history.get_plot_figure(plot_info["id"])
                    if figure and hasattr(figure, 'frames') and figure.frames:
                        has_animation = True
            except:
                pass
        
        # For animated plots, be more permissive with updates to ensure animation works
        # But still try to preserve state when possible
        if (last_rendered_state["tab"] == active_tab and 
            last_rendered_state["plot_count"] == current_plot_count and
            last_rendered_state["last_update"] == current_last_update and
            not has_animation):  # Only prevent update for non-animated plots
            # No change detected, prevent update to preserve zoom state
            raise PreventUpdate
        
        # Update our tracking state
        last_rendered_state["tab"] = active_tab
        last_rendered_state["plot_count"] = current_plot_count
        last_rendered_state["last_update"] = current_last_update
        
        if not active_tab or active_tab == "tab-empty":
            # print("🎨 Showing empty state")
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
                    # Check if this plot has animation frames
                    has_frames = hasattr(figure, 'frames') and figure.frames and len(figure.frames) > 0
                    
                    # print(f"🎨 Rendering plot: {plot_info['id']}, has_frames: {has_frames}")
                    
                    # Configure the graph based on whether it has animations
                    graph_config = {
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f"plot_{plot_info['timestamp'].strftime('%Y%m%d_%H%M%S')}",
                            'height': 500,
                            'width': 700,
                            'scale': 1
                        },
                        'responsive': True
                    }
                    
                    # For animated plots, add special handling
                    if has_frames:
                        graph_config.update({
                            'showTips': False,
                            'staticPlot': False,
                            # Remove some buttons that might interfere with animation
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'autoScale2d']
                        })
                    
                    graph_component = dcc.Graph(
                        id=f"plot-graph-{plot_info['id']}",  # Unique ID for each plot
                        figure=figure,
                        style={"height": "450px"},
                        config=graph_config
                    )
                    
                    # Add animation status info for debugging
                    animation_info = ""
                    if has_frames:
                        animation_info = f" | Animation: {len(figure.frames)} frames"
                    
                    components = [graph_component]
                    
                    # Add animation warning if present
                    if has_frames:
                        components.append(
                            html.Div([
                                html.Small([
                                    html.I(className="fas fa-play-circle me-1", style={"color": "#007bff"}),
                                    f"This plot contains {len(figure.frames)} animation frames. ",
                                    "Use the play button in the plot toolbar to start the animation. ",
                                    "Note: Animations may interfere with tab switching."
                                ], className="text-info")
                            ], className="mt-2 text-center")
                        )
                    
                    components.append(
                        html.Div([
                            html.Small([
                                html.I(className="fas fa-info-circle me-1"),
                                f"Generated: {plot_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | ",
                                f"Job ID: {plot_info['job_id']}{animation_info}"
                            ], className="text-muted")
                        ], className="mt-2 text-center")
                    )
                    
                    return html.Div(components)
                else:
                    # print(f"❌ No figure found for plot: {plot_info['id']}")
                    return html.Div([
                        html.Div([
                            html.I(className="fas fa-exclamation-triangle", style={"fontSize": "32px", "color": "#dc3545"}),
                            html.H6("Plot data not found", className="mt-2 text-danger"),
                            html.P("The plot data may have been cleared from cache", className="text-muted")
                        ], className="text-center", style={"padding": "40px 20px"})
                    ])
        except Exception as e:
            # print(f"❌ Error in plot callback: {str(e)}")
            return html.Div([
                html.Div([
                    html.I(className="fas fa-bug", style={"fontSize": "32px", "color": "#dc3545"}),
                    html.H6("Error loading plot", className="mt-2 text-danger"),
                    html.P(f"Error: {str(e)}", className="text-muted small")
                ], className="text-center", style={"padding": "40px 20px"})
            ])
        
        return html.Div("Plot not found")