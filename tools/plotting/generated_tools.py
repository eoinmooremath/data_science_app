from tools.plotting.base import BasePlottingTool, ToolInput
from pydantic import Field
from typing import Optional, List, Dict, Any, Union
import plotly.express as px

class AreaInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positions; can be a list for wide-form Area plots.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positions; can be a list for wide-form Area plots.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in Area plots.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks based on values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycled when symbol is set.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use symbol names directly.")
    
    # === PATTERNS ===
    pattern_shape: Any = Field(default=None, description="[PATTERNS] Assigns pattern shapes to marks based on values.")
    pattern_shape_sequence: Any = Field(default=None, description="[PATTERNS] Sequence of plotly.js pattern shapes for categorical pattern mapping; cycled when pattern_shape is set.")
    pattern_shape_map: Any = Field(default=None, description="[PATTERNS] Map specific values to plotly.js pattern shapes, overriding pattern_shape_sequence; use 'identity' to use pattern names directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on the plot.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default is 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups data into separate lines in the Area plot.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    groupnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Normalize stacked values to 'fraction' or 'percent'; None stacks raw values.")
    line_shape: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Line shape: 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyAreaTool(BasePlottingTool):
    name = "plotting_area"
    description = "In a stacked area plot, each row of `data_frame` is represented as"
    input_model = AreaInput
    _plot_function = staticmethod(px.area)

class BarPolarInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    r: Any = Field(default=None, description="[CORE DATA] Values for radial axis positioning in BarPolar plot.")
    theta: Any = Field(default=None, description="[CORE DATA] Values for angular axis positioning in BarPolar plot.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use values as colors directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric color mapping; supports sequential, diverging, and cyclical color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale, overriding auto-scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === PATTERNS ===
    pattern_shape: Any = Field(default=None, description="[PATTERNS] Values used to assign pattern shapes to bars.")
    pattern_shape_sequence: Any = Field(default=None, description="[PATTERNS] Sequence of pattern shapes for categorical mapping; cycles through sequence for pattern_shape values.")
    pattern_shape_map: Any = Field(default=None, description="[PATTERNS] Map specific values to pattern shapes, overriding pattern_shape_sequence; use 'identity' to use values as pattern names directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === AXES ===
    range_r: Any = Field(default=None, description="[AXES] Sets custom range for the radial axis, overriding auto-scaling.")
    range_theta: Any = Field(default=None, description="[AXES] Sets custom range for the angular axis, overriding auto-scaling.")
    log_r: Any = Field(default=False, description="[AXES] If True, radial axis uses a logarithmic scale.")
    
    # === MAP & POLAR ===
    direction: Any = Field(default='clockwise', description="[MAP & POLAR] Sets angular axis direction: 'counterclockwise' or 'clockwise' (default).")
    start_angle: Any = Field(default=90, description="[MAP & POLAR] Sets starting angle for angular axis; 0 is east, 90 is north.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    base: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Values used to position the base of each bar.")
    barnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Normalizes bar values at each location as 'fraction', 'percent', or stacks all values if None.")
    barmode: Any = Field(default='relative', description="[PLOT-SPECIFIC OPTIONS] Sets bar arrangement: 'group' (side by side), 'overlay' (overlapping), or 'relative' (stacked).")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels; keys are column names.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign bars to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Values used for object constancy across animation frames; matching values treated as the same object.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyBarPolarTool(BasePlottingTool):
    name = "plotting_bar_polar"
    description = "In a polar bar plot, each row of `data_frame` is represented as a wedge"
    input_model = BarPolarInput
    _plot_function = staticmethod(px.bar_polar)

class BarInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positions; can be a single column or a list for wide-form data.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positions; can be a single column or a list for wide-form data.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors; overrides color_discrete_sequence.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color values.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the min and max range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, useful for diverging color schemes.")
    
    # === PATTERNS ===
    pattern_shape: Any = Field(default=None, description="[PATTERNS] Values used to assign pattern shapes to bars.")
    pattern_shape_sequence: Any = Field(default=None, description="[PATTERNS] Sequence of pattern shapes for categorical pattern mapping.")
    pattern_shape_map: Any = Field(default=None, description="[PATTERNS] Map specific categorical values to pattern shapes; overrides pattern_shape_sequence.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity (0 to 1).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on bars.")
    
    # === ERROR BARS ===
    error_x: Any = Field(default=None, description="[ERROR BARS] Values for x-axis error bar sizes; used for positive direction if error_x_minus is set.")
    error_x_minus: Any = Field(default=None, description="[ERROR BARS] Values for negative direction x-axis error bars; ignored if error_x is None.")
    error_y: Any = Field(default=None, description="[ERROR BARS] Values for y-axis error bar sizes; used for positive direction if error_y_minus is set.")
    error_y_minus: Any = Field(default=None, description="[ERROR BARS] Values for negative direction y-axis error bars; ignored if error_y is None.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns bars to facet rows (vertical subplots).")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns bars to facet columns (horizontal subplots).")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Sets x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Sets y-axis range, overriding auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    base: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Values to set the base position of each bar.")
    barmode: Any = Field(default='relative', description="[PLOT-SPECIFIC OPTIONS] Bar arrangement mode: 'group' (side-by-side), 'overlay' (overlapping), or 'relative' (stacked).")
    text_auto: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] If True or a format string, display values as text labels on bars with optional formatting.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns bars to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames using group values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyBarTool(BasePlottingTool):
    name = "plotting_bar"
    description = "In a bar plot, each row of `data_frame` is represented as a rectangular"
    input_model = BarInput
    _plot_function = staticmethod(px.bar)

class BoxInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positioning; can be a single column or list for wide-format Box plots.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positioning; can be a single column or list for wide-format Box plots.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for assigning colors to categorical values in Box plots.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use values as colors directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns Box plots to facet subplots vertically.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns Box plots to facet subplots horizontally.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row or marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows, in paper units; default is 0.03 (or 0.07 with facet_col_wrap).")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns, in paper units; default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] If True, use a log scale for the x-axis.")
    log_y: Any = Field(default=False, description="[AXES] If True, use a log scale for the y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range, overriding auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    boxmode: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Box arrangement mode: 'group' places boxes side by side; 'overlay' draws boxes on top of each other.")
    points: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Controls which sample points are shown: 'outliers', 'suspectedoutliers', 'all', or False (no points).")
    notched: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] If True, draw boxes with notches.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default axis, legend, and hover labels with a mapping of column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns Box plots to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyBoxTool(BasePlottingTool):
    name = "plotting_box"
    description = "In a box plot, rows of `data_frame` are grouped together into a"
    input_model = BoxInput
    _plot_function = staticmethod(px.box)

# class ChoroplethMapInput(ToolInput):
#     # === CORE DATA ===
#     data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
#     locations: Any = Field(default=None, description="[CORE DATA] Values to be mapped to geographic locations according to `locationmode`.")
    
#     # === COLORS ===
#     color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
#     color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
#     color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors; use 'identity' to apply color values directly.")
#     color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric data in continuous color mapping.")
#     range_color: Any = Field(default=None, description="[COLORS] Manually sets the min and max values for the continuous color scale.")
#     color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
#     # === OPACITY ===
#     opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity; value between 0 and 1.")
    
#     # === HOVER & TEXT ===
#     hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
#     hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
#     # === GEOGRAPHY ===
#     geojson: Any = Field(default=None, description="[GEOGRAPHY] GeoJSON Polygon feature collection with IDs referenced by `locations`.")
#     featureidkey: Any = Field(default=None, description="[GEOGRAPHY] Path in GeoJSON features to match with `locations` values, e.g., 'properties.<key>'.")
#     center: Any = Field(default=None, description="[GEOGRAPHY] Sets map center using a dict with 'lat' and 'lon'.")
    
#     # === MAP & POLAR ===
#     zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level; value between 0 and 20.")
#     map_style: Any = Field(default=None, description="[MAP & POLAR] Base map style; allowed values include 'basic', 'carto-darkmatter', 'carto-positron', 'open-street-map', 'satellite', etc.")
    
#     # === LAYOUT & STYLING ===
#     title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
#     subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
#     template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
#     width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
#     height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
#     # === DATA ORGANIZATION ===
#     category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
#     labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
#     # === ANIMATION ===
#     animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
#     animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group values.")
    
#     # === ADVANCED OPTIONS ===
#     custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
#     dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
# class PlotlyChoroplethMapTool(BasePlottingTool):
#     name = "plotting_choropleth_map"
#     description = "In a choropleth map, each row of `data_frame` is represented by a"
#     input_model = ChoroplethMapInput
#     _plot_function = staticmethod(px.choropleth_map)

class ChoroplethMapboxInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    locations: Any = Field(default=None, description="[CORE DATA] Values mapped to geographic features based on `locationmode` for positioning on the map.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Maps specific category values to CSS colors, overriding `color_discrete_sequence`; use `'identity'` to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric data, used to build continuous color gradients.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom min and max values for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === GEOGRAPHY ===
    geojson: Any = Field(default=None, description="[GEOGRAPHY] GeoJSON Polygon feature collection with IDs referenced by `locations`.")
    featureidkey: Any = Field(default=None, description="[GEOGRAPHY] Path to GeoJSON feature property used to match `locations` values, e.g., `'properties.<key>'`.")
    center: Any = Field(default=None, description="[GEOGRAPHY] Sets the map center using a dict with `'lat'` and `'lon'`.")
    
    # === MAP & POLAR ===
    zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level, from 0 (world view) to 20 (street view).")
    mapbox_style: Any = Field(default=None, description="[MAP & POLAR] Identifier of base map style, some of which require a Mapbox or Stadia Maps API token to be set using `plotly.express.set_mapbox_access_token()`. Allowed values which do not require a token are `'open-street-map'`, `'white-bg'`, `'carto- positron'`, `'carto-darkmatter'`. Allowed values which require a Mapbox API token are `'basic'`, `'streets'`, `'outdoors'`, `'light'`, `'dark'`, `'satellite'`, `'satellite-streets'`. Allowed values which require a Stadia Maps API token are `'stamen-terrain'`, `'stamen- toner'`, `'stamen-watercolor'`.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default column names for axis titles, legend, and hover labels using a dict mapping column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign data to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
class PlotlyChoroplethMapboxTool(BasePlottingTool):
    name = "plotting_choropleth_mapbox"
    description = "*choropleth_mapbox* is deprecated! Use *choropleth_map* instead."
    input_model = ChoroplethMapboxInput
    _plot_function = staticmethod(px.choropleth_mapbox)

class ChoroplethInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning regions on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning regions on the map.")
    locations: Any = Field(default=None, description="[CORE DATA] Region identifiers, interpreted by `locationmode` to map data to geographic areas.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific category values to CSS colors for discrete color assignment; use 'identity' to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric data, used for continuous color mapping.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the min and max values for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns regions to facet subplots vertically.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns regions to facet subplots horizontally.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row`/`marginal` is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (default 0.03, or 0.07 with `facet_col_wrap`).")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (default 0.02).")
    
    # === GEOGRAPHY ===
    locationmode: Any = Field(default=None, description="[GEOGRAPHY] Determines how `locations` values are matched to map regions: 'ISO-3', 'USA-states', or 'country names'.")
    geojson: Any = Field(default=None, description="[GEOGRAPHY] GeoJSON Polygon feature collection with IDs referenced by `locations`.")
    featureidkey: Any = Field(default=None, description="[GEOGRAPHY] Path to the GeoJSON property used to match `locations` values, e.g., 'properties.<key>'.")
    projection: Any = Field(default=None, description="[GEOGRAPHY] Map projection type (e.g., 'mercator', 'natural earth', 'albers usa'); default depends on `scope`.")
    scope: Any = Field(default=None, description="[GEOGRAPHY] Map area to display: 'world', 'usa', 'europe', 'asia', 'africa', 'north america', or 'south america'; default is 'world' unless using 'albers usa' projection.")
    center: Any = Field(default=None, description="[GEOGRAPHY] Sets the map center using a dict with 'lat' and 'lon' keys.")
    fitbounds: Any = Field(default=None, description="[GEOGRAPHY] Determines map bounds: `False`, `locations`, or `geojson`.")
    basemap_visible: Any = Field(default=None, description="[GEOGRAPHY] Controls visibility of the basemap layer.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default column names for axis titles, legends, and hovers using a dict of replacements.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns regions to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames by grouping rows with the same value.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
class PlotlyChoroplethTool(BasePlottingTool):
    name = "plotting_choropleth"
    description = "In a choropleth map, each row of `data_frame` is represented by a"
    input_model = ChoroplethInput
    _plot_function = staticmethod(px.choropleth)

class DensityContourInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positioning; can be a list for wide-form data.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positioning; can be a list for wide-form data.")
    z: Any = Field(default=None, description="[CORE DATA] Values used as input to `histfunc` for DensityContour plots.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors; use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === TRENDLINES ===
    trendline: Any = Field(default=None, description="[TRENDLINES] One of `'ols'`, `'lowess'`, `'rolling'`, `'expanding'` or `'ewm'`. If `'ols'`, an Ordinary Least Squares regression line will be drawn for each discrete-color/symbol group. If `'lowess`', a Locally Weighted Scatterplot Smoothing line will be drawn for each discrete-color/symbol group. If `'rolling`', a Rolling (e.g. rolling average, rolling median) line will be drawn for each discrete-color/symbol group. If `'expanding`', an Expanding (e.g. expanding average, expanding sum) line will be drawn for each discrete-color/symbol group. If `'ewm`', an Exponentially Weighted Moment (e.g. exponentially-weighted moving average) line will be drawn for each discrete-color/symbol group. See the docstrings for the functions in `plotly.express.trendline_functions` for more details on these functions and how to configure them with the `trendline_options` argument.")
    trendline_options: Any = Field(default=None, description="[TRENDLINES] Options passed to the trendline function specified by `trendline`.")
    trendline_color_override: Any = Field(default=None, description="[TRENDLINES] CSS color for all trendlines if set, overriding default trace colors.")
    trendline_scope: Any = Field(default='trace', description="[TRENDLINES] If `'trace'`, then one trendline is drawn per trace (i.e. per color, symbol, facet, animation frame etc) and if `'overall'` then one trendline is computed for the entire dataset, and replicated across all facets.")
    
    # === MARGINAL PLOTS ===
    marginal_x: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a horizontal subplot above the main plot to show x-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    marginal_y: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a vertical subplot to the right of the main plot to show y-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots based on values.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots based on values.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row`/`marginal` is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (in paper units); default is 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (in paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range, overriding auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    histfunc: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] One of `'count'`, `'sum'`, `'avg'`, `'min'`, or `'max'`. Function used to aggregate values for summarization (note: can be normalized with `histnorm`). The arguments to this function are the values of `z`.")
    histnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Normalization for histogram: 'percent', 'probability', 'density', or 'probability density'; None uses raw `histfunc` output.")
    nbinsx: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Number of bins along the x-axis (positive integer).")
    nbinsy: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Number of bins along the y-axis (positive integer).")
    text_auto: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show x, y, or z values as text; string values specify numeric formatting.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels; keys are column names.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assign marks to animation frames based on values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object-constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyDensityContourTool(BasePlottingTool):
    name = "plotting_density_contour"
    description = "In a density contour plot, rows of `data_frame` are grouped together"
    input_model = DensityContourInput
    _plot_function = staticmethod(px.density_contour)

class DensityHeatmapInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positioning; can be a single column or list for wide-form data.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positioning; can be a single column or list for wide-form data.")
    z: Any = Field(default=None, description="[CORE DATA] Values used as input to `histfunc` for bin aggregation in DensityHeatmap.")
    
    # === COLORS ===
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric data; accepts CSS color strings or Plotly color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Manually sets the color scale range, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint of the continuous color scale; recommended for diverging color scales.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Opacity of the heatmap, from 0 (transparent) to 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === MARGINAL PLOTS ===
    marginal_x: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a horizontal subplot above the main plot to show x-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    marginal_y: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a vertical subplot to the right of the main plot to show y-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns subplots in the vertical direction for faceting by row.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns subplots in the horizontal direction for faceting by column.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row` or a marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows, in paper units; default is 0.03 (or 0.07 with facet_col_wrap).")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns, in paper units; default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Logarithmic scaling for the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Logarithmic scaling for the y-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Sets the x-axis range, overriding automatic scaling.")
    range_y: Any = Field(default=None, description="[AXES] Sets the y-axis range, overriding automatic scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    histfunc: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] One of `'count'`, `'sum'`, `'avg'`, `'min'`, or `'max'`. Function used to aggregate values for summarization (note: can be normalized with `histnorm`). The arguments to this function are the values of `z`.")
    histnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Normalization mode for bin values: 'percent', 'probability', 'density', or 'probability density'; controls how `histfunc` output is scaled.")
    nbinsx: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Number of bins along the x-axis (positive integer).")
    nbinsy: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Number of bins along the y-axis (positive integer).")
    text_auto: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Displays bin values as text; accepts True or a format string (e.g., '.2f').")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Custom axis, legend, and hover labels; dict mapping column names to labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyDensityHeatmapTool(BasePlottingTool):
    name = "plotting_density_heatmap"
    description = "In a density heatmap, rows of `data_frame` are grouped together into"
    input_model = DensityHeatmapInput
    _plot_function = staticmethod(px.density_heatmap)

# class DensityMapInput(ToolInput):
#     # === CORE DATA ===
#     data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
#     lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning points on the map.")
#     lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning points on the map.")
#     z: Any = Field(default=None, description="[CORE DATA] Values used for density calculation or intensity in DensityMap plot.")
    
#     # === COLORS ===
#     color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric data; accepts CSS color strings or Plotly color scales.")
#     range_color: Any = Field(default=None, description="[COLORS] Sets the min and max range for the continuous color scale.")
#     color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
#     # === OPACITY ===
#     opacity: Any = Field(default=None, description="[OPACITY] Marker opacity; value between 0 (transparent) and 1 (opaque).")
    
#     # === HOVER & TEXT ===
#     hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
#     hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
#     # === GEOGRAPHY ===
#     center: Any = Field(default=None, description="[GEOGRAPHY] Sets the map center using a dict with 'lat' and 'lon' keys.")
    
#     # === MAP & POLAR ===
#     zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level; value between 0 and 20.")
#     map_style: Any = Field(default=None, description="[MAP & POLAR] Base map style; valid values include 'basic', 'carto-darkmatter', 'carto-positron', 'dark', 'light', 'open-street-map', 'satellite', and others.")
    
#     # === PLOT-SPECIFIC OPTIONS ===
#     radius: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Radius of influence for each point in the density calculation.")
    
#     # === LAYOUT & STYLING ===
#     title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
#     subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
#     template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
#     width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
#     height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
#     # === DATA ORGANIZATION ===
#     category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
#     labels: Any = Field(default=None, description="[DATA ORGANIZATION] Custom labels for axes, legend, and hover; keys are column names, values are display labels.")
    
#     # === ANIMATION ===
#     animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns points to animation frames for animated DensityMap plots.")
#     animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames by grouping rows with matching values.")
    
#     # === ADVANCED OPTIONS ===
#     custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
#     dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use for the plot.")
# class PlotlyDensityMapTool(BasePlottingTool):
#     name = "plotting_density_map"
#     description = "In a density map, each row of `data_frame` contributes to the intensity of"
#     input_model = DensityMapInput
#     _plot_function = staticmethod(px.density_map)

class DensityMapboxInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning points on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning points on the map.")
    z: Any = Field(default=None, description="[CORE DATA] Values used for density weighting or intensity in the DensityMapbox plot.")
    
    # === COLORS ===
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color mapping; accepts CSS color strings or Plotly color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the min and max range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === GEOGRAPHY ===
    center: Any = Field(default=None, description="[GEOGRAPHY] Sets the map center using a dictionary with 'lat' and 'lon' keys.")
    
    # === MAP & POLAR ===
    zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level, from 0 (world view) to 20 (street level).")
    mapbox_style: Any = Field(default=None, description="[MAP & POLAR] Identifier of base map style, some of which require a Mapbox or Stadia Maps API token to be set using `plotly.express.set_mapbox_access_token()`. Allowed values which do not require a token are `'open-street-map'`, `'white-bg'`, `'carto- positron'`, `'carto-darkmatter'`. Allowed values which require a Mapbox API token are `'basic'`, `'streets'`, `'outdoors'`, `'light'`, `'dark'`, `'satellite'`, `'satellite-streets'`. Allowed values which require a Stadia Maps API token are `'stamen-terrain'`, `'stamen- toner'`, `'stamen-watercolor'`.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    radius: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Radius of influence for each point, affecting density estimation.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Custom labels for axes, legend, and hover tooltips; keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns data to animation frames for animated DensityMapbox plots.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group identifiers.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
class PlotlyDensityMapboxTool(BasePlottingTool):
    name = "plotting_density_mapbox"
    description = "*density_mapbox* is deprecated! Use *density_map* instead."
    input_model = DensityMapboxInput
    _plot_function = staticmethod(px.density_mapbox)

class EcdfInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positioning; with 'h' orientation, plots cumulative sum instead of count. Accepts single or multiple columns for wide-format data.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positioning; with 'v' orientation, plots cumulative sum instead of count. Accepts single or multiple columns for wide-format data.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in Ecdf plot.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycled when symbol is set.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use symbol values directly.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels for marks in the Ecdf plot.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips for marks.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === MARGINAL PLOTS ===
    marginal: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a subplot ('rug', 'box', 'violin', or 'histogram') to show data distribution.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertically facetted subplots.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontally facetted subplots.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to new rows; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); defaults to 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Logarithmic scaling for x-axis.")
    log_y: Any = Field(default=False, description="[AXES] Logarithmic scaling for y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash-patterns to lines based on column values.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    lines: Any = Field(default=True, description="[PLOT-SPECIFIC OPTIONS] If `False`, lines are not drawn (forced to `True` if `markers` is `False`).")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for categorical dash mapping; cycled when line_dash is set.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific categorical values to plotly.js dash-patterns, overriding line_dash_sequence; use 'identity' to use dash values directly.")
    ecdfnorm: Any = Field(default='probability', description="[PLOT-SPECIFIC OPTIONS] Normalization for ECDF values: 'probability' (0–1), 'percent' (0–100), or None for raw counts/sums.")
    ecdfmode: Any = Field(default='standard', description="[PLOT-SPECIFIC OPTIONS] ECDF mode: 'standard' (at or below point), 'complementary' (above point), or 'reversed' (at or above point).")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels with custom names; keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group identifiers.")
    
    # === ADVANCED OPTIONS ===
    render_mode: Any = Field(default='auto', description="[ADVANCED OPTIONS] Rendering mode: 'auto', 'svg' (vector, <1000 points), or 'webgl' (raster, >1000 points).")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyEcdfTool(BasePlottingTool):
    name = "plotting_ecdf"
    description = "In a Empirical Cumulative Distribution Function (ECDF) plot, rows of `data_frame`"
    input_model = EcdfInput
    _plot_function = staticmethod(px.ecdf)

class FunnelAreaInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for categorical mapping of sectors, applied in order unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map of specific values to CSS colors for sectors; overrides `color_discrete_sequence`. Use `'identity'` to apply color values directly.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity; value must be between 0 and 1.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Column values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === HIERARCHY ===
    names: Any = Field(default=None, description="[HIERARCHY] Column values used as sector labels.")
    values: Any = Field(default=None, description="[HIERARCHY] Column values used to set sector sizes.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary to override default axis, legend, and hover labels for columns.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyFunnelAreaTool(BasePlottingTool):
    name = "plotting_funnel_area"
    description = "In a funnel area plot, each row of `data_frame` is represented as a"
    input_model = FunnelAreaInput
    _plot_function = staticmethod(px.funnel_area)

class FunnelInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Values for x-axis positioning in Funnel plot; can be a single column or list for wide-format data.")
    y: Any = Field(default=None, description="[CORE DATA] Values for y-axis positioning in Funnel plot; can be a single column or list for wide-format data.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in Funnel plot.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to assign colors directly from data.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity; value between 0 and 1.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in Funnel plot hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on the Funnel plot.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots based on column values.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots based on column values.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (in paper units); default is 0.03, or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (in paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range, overriding auto-scaling.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use for the Funnel plot.")
class PlotlyFunnelTool(BasePlottingTool):
    name = "plotting_funnel"
    description = "In a funnel plot, each row of `data_frame` is represented as a"
    input_model = FunnelInput
    _plot_function = staticmethod(px.funnel)

class GetTrendlineResultsInput(ToolInput):
    # === PLOT-SPECIFIC OPTIONS ===
    fig: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Plotly figure object to display trendline results.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title for GetTrendlineResults plot.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier for retrieving trendline results.")
class PlotlyGetTrendlineResultsTool(BasePlottingTool):
    name = "plotting_get_trendline_results"
    description = "Extracts fit statistics for trendlines (when applied to figures generated with"
    input_model = GetTrendlineResultsInput
    _plot_function = staticmethod(px.get_trendline_results)

class HistogramInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning or histogram input; supports wide or long format.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning or histogram input; supports wide or long format.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors; use 'identity' to use values as colors directly.")
    
    # === PATTERNS ===
    pattern_shape: Any = Field(default=None, description="[PATTERNS] Assigns pattern shapes to histogram bars based on column values.")
    pattern_shape_sequence: Any = Field(default=None, description="[PATTERNS] Sequence of pattern shapes for categorical mapping; cycles through values in order.")
    pattern_shape_map: Any = Field(default=None, description="[PATTERNS] Map specific values to pattern shapes; use 'identity' to use values as pattern names directly.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity (0 to 1).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === MARGINAL PLOTS ===
    marginal: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a subplot showing distribution as a 'rug', 'box', 'violin', or 'histogram'.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default is 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    barmode: Any = Field(default='relative', description="[PLOT-SPECIFIC OPTIONS] Bar arrangement mode: 'group' (side-by-side), 'overlay' (stacked), or 'relative' (stacked by sign).")
    barnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Bar normalization: 'fraction', 'percent', or None for stacking.")
    histnorm: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Histogram normalization: 'percent', 'probability', 'density', 'probability density', or None for raw counts.")
    histfunc: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] One of `'count'`, `'sum'`, `'avg'`, `'min'`, or `'max'`. Function used to aggregate values for summarization (note: can be normalized with `histnorm`). The arguments to this function are the values of `y` (`x`) if `orientation` is `'v'` (`'h'`).")
    cumulative: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] If True, histogram values are cumulative.")
    nbins: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Number of bins (positive integer).")
    text_auto: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show bar values as text; accepts True or a formatting string (e.g., '.2f').")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels; dict mapping column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID.")
class PlotlyHistogramTool(BasePlottingTool):
    name = "plotting_histogram"
    description = "In a histogram, rows of `data_frame` are grouped together into a"
    input_model = HistogramInput
    _plot_function = staticmethod(px.histogram)

class IcicleInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] color_continuous_scale: Continuous color scale for numeric color values in Icicle plot; accepts CSS color strings and supports sequential, diverging, and cyclical scales.")
    range_color: Any = Field(default=None, description="[COLORS] range_color: Sets custom range for the continuous color scale, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] color_continuous_midpoint: Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] color_discrete_sequence: CSS color sequence for categorical color mapping; assigns colors to unique values in the color column.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] color_discrete_map: Maps specific categorical values to CSS colors; use 'identity' to assign colors directly from data values.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] hover_name: Values displayed in bold in the hover tooltip for each sector.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === HIERARCHY ===
    names: Any = Field(default=None, description="[HIERARCHY] names: Labels for sectors in the Icicle plot.")
    values: Any = Field(default=None, description="[HIERARCHY] values: Numeric values associated with each sector, determining their size.")
    parents: Any = Field(default=None, description="[HIERARCHY] parents: Parent sector for each entry, defining the hierarchy.")
    path: Any = Field(default=None, description="[HIERARCHY] path: List of columns defining the hierarchy from root to leaves; cannot be used with ids or parents.")
    ids: Any = Field(default=None, description="[HIERARCHY] ids: Unique identifier for each sector.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    branchvalues: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] branchvalues: Determines how sector values are summed; 'total' treats values as totals including descendants, 'remainder' as the remainder after subtracting leaf values.")
    maxdepth: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] maxdepth: Maximum number of hierarchy levels to display; set to -1 to show all levels.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] title: Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] subtitle: Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] width: Plot width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] height: Plot height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] labels: Dictionary to override default column names for axis titles, legend entries, and hover labels.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] dataset_id: ID of the dataset used for the plot.")
class PlotlyIcicleTool(BasePlottingTool):
    name = "plotting_icicle"
    description = "An icicle plot represents hierarchial data with adjoined rectangular"
    input_model = IcicleInput
    _plot_function = staticmethod(px.icicle)

class Line3DInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning in Line3D plot.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning in Line3D plot.")
    z: Any = Field(default=None, description="[CORE DATA] Column values for z-axis positioning in Line3D plot.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in Line3D plot.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors for lines; use 'identity' to apply color values directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to markers based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycled when `symbol` is set.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols for markers; use 'identity' to apply symbol names directly.")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels for markers or lines in the plot.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips for markers or lines.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === ERROR BARS ===
    error_x: Any = Field(default=None, description="[ERROR BARS] Sizes x-axis error bars; if `error_x_minus` is not set, error bars are symmetrical.")
    error_x_minus: Any = Field(default=None, description="[ERROR BARS] Sizes x-axis error bars in the negative direction; ignored if `error_x` is not set.")
    error_y: Any = Field(default=None, description="[ERROR BARS] Sizes y-axis error bars; if `error_y_minus` is not set, error bars are symmetrical.")
    error_y_minus: Any = Field(default=None, description="[ERROR BARS] Sizes y-axis error bars in the negative direction; ignored if `error_y` is not set.")
    error_z: Any = Field(default=None, description="[ERROR BARS] Sizes z-axis error bars; if `error_z_minus` is not set, error bars are symmetrical.")
    error_z_minus: Any = Field(default=None, description="[ERROR BARS] Sizes z-axis error bars in the negative direction; ignored if `error_z` is not set.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    log_z: Any = Field(default=False, description="[AXES] Log-scale the z-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Set custom x-axis range; overrides auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Set custom y-axis range; overrides auto-scaling.")
    range_z: Any = Field(default=None, description="[AXES] Set custom z-axis range; overrides auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash-patterns to lines based on column values.")
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups rows into separate lines based on column values.")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for categorical line dashing; cycled when `line_dash` is set.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific categorical values to plotly.js dash-patterns for lines; use 'identity' to apply dash names directly.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels per column.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyLine3DTool(BasePlottingTool):
    name = "plotting_line_3d"
    description = "In a 3D line plot, each row of `data_frame` is represented as a vertex of"
    input_model = Line3DInput
    _plot_function = staticmethod(px.line_3d)

class LineGeoInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning marks on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning marks on the map.")
    locations: Any = Field(default=None, description="[CORE DATA] Location values interpreted by `locationmode` and mapped to map coordinates.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific values to CSS colors, overriding `color_discrete_sequence`; use 'identity' to use values as colors directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks for categorical differentiation.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific values to plotly.js symbols, overriding `symbol_sequence`; use 'identity' to use values as symbols directly.")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels displayed on the plot.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to facet subplots vertically.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to facet subplots horizontally.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row`/`marginal` is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default is 0.03 or 0.07 with `facet_col_wrap`.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === GEOGRAPHY ===
    locationmode: Any = Field(default=None, description="[GEOGRAPHY] Determines how `locations` values map to regions: 'ISO-3', 'USA-states', or 'country names'.")
    geojson: Any = Field(default=None, description="[GEOGRAPHY] GeoJSON Polygon feature collection with IDs referenced by `locations`.")
    featureidkey: Any = Field(default=None, description="[GEOGRAPHY] Path to GeoJSON feature property used to match `locations` values (e.g., 'properties.<key>').")
    projection: Any = Field(default=None, description="[GEOGRAPHY] Map projection type; options include 'equirectangular', 'mercator', 'orthographic', etc.; default depends on `scope`.")
    scope: Any = Field(default=None, description="[GEOGRAPHY] Map region scope; options: 'world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america'; default is 'world' unless `projection` is 'albers usa'.")
    center: Any = Field(default=None, description="[GEOGRAPHY] Center point of the map as a dict with 'lat' and 'lon' keys.")
    fitbounds: Any = Field(default=None, description="[GEOGRAPHY] Determines map bounds fitting: `False`, `locations`, or `geojson`.")
    basemap_visible: Any = Field(default=None, description="[GEOGRAPHY] Controls basemap visibility.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash-patterns to lines for categorical differentiation.")
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups data rows into separate lines.")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for categorical line dash mapping.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific values to plotly.js dash-patterns, overriding `line_dash_sequence`; use 'identity' to use values as dash-patterns directly.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default axis, legend, and hover labels; dict maps column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames by grouping rows with the same value.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
class PlotlyLineGeoTool(BasePlottingTool):
    name = "plotting_line_geo"
    description = "In a geographic line plot, each row of `data_frame` is represented as"
    input_model = LineGeoInput
    _plot_function = staticmethod(px.line_geo)

# class LineMapInput(ToolInput):
#     # === CORE DATA ===
#     data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
#     lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning lines on the map.")
#     lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning lines on the map.")
    
#     # === COLORS ===
#     color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
#     color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
#     color_discrete_map: Any = Field(default=None, description="[COLORS] Maps specific categorical values to CSS colors; use 'identity' to apply color values directly.")
    
#     # === HOVER & TEXT ===
#     text: Any = Field(default=None, description="[HOVER & TEXT] Text labels to display on the map.")
#     hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips.")
#     hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
#     # === GEOGRAPHY ===
#     center: Any = Field(default=None, description="[GEOGRAPHY] Sets map center using 'lat' and 'lon' keys.")
    
#     # === MAP & POLAR ===
#     zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level (0–20).")
#     map_style: Any = Field(default=None, description="[MAP & POLAR] Base map style; valid values include 'basic', 'carto-darkmatter', 'carto-positron', 'open-street-map', 'satellite', etc.")
    
#     # === PLOT-SPECIFIC OPTIONS ===
#     line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups rows into separate lines based on column values.")
    
#     # === LAYOUT & STYLING ===
#     title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
#     subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
#     template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
#     width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
#     height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
#     # === DATA ORGANIZATION ===
#     category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
#     labels: Any = Field(default=None, description="[DATA ORGANIZATION] Overrides default axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
#     # === ANIMATION ===
#     animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames for animated LineMap plots.")
#     animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames by grouping rows with matching values.")
    
#     # === ADVANCED OPTIONS ===
#     custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
#     dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
# class PlotlyLineMapTool(BasePlottingTool):
#     name = "plotting_line_map"
#     description = "In a line map, each row of `data_frame` is represented as"
#     input_model = LineMapInput
#     _plot_function = staticmethod(px.line_map)

class LineMapboxInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning lines on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning lines on the map.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors; overrides color_discrete_sequence. Use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels displayed on the map.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === GEOGRAPHY ===
    center: Any = Field(default=None, description="[GEOGRAPHY] Dictionary with 'lat' and 'lon' keys to set the map center.")
    
    # === MAP & POLAR ===
    zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level (0–20).")
    mapbox_style: Any = Field(default=None, description="[MAP & POLAR] Identifier of base map style, some of which require a Mapbox or Stadia Maps API token to be set using `plotly.express.set_mapbox_access_token()`. Allowed values which do not require a token are `'open-street-map'`, `'white-bg'`, `'carto- positron'`, `'carto-darkmatter'`. Allowed values which require a Mapbox API token are `'basic'`, `'streets'`, `'outdoors'`, `'light'`, `'dark'`, `'satellite'`, `'satellite-streets'`. Allowed values which require a Stadia Maps API token are `'stamen-terrain'`, `'stamen- toner'`, `'stamen-watercolor'`.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups data into separate lines based on column values.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary to override default axis, legend, and hover labels; keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns data to animation frames for animated maps.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyLineMapboxTool(BasePlottingTool):
    name = "plotting_line_mapbox"
    description = "*line_mapbox* is deprecated! Use *line_map* instead."
    input_model = LineMapboxInput
    _plot_function = staticmethod(px.line_mapbox)

class LinePolarInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    r: Any = Field(default=None, description="[CORE DATA] Radial axis values for positioning points in LinePolar plot.")
    theta: Any = Field(default=None, description="[CORE DATA] Angular axis values for positioning points in LinePolar plot.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in LinePolar plot.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors for marks; use 'identity' to apply color values directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols for marks; use 'identity' to apply symbol names directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values shown as text labels on the plot.")
    
    # === AXES ===
    range_r: Any = Field(default=None, description="[AXES] Sets custom range for the radial axis.")
    range_theta: Any = Field(default=None, description="[AXES] Sets custom range for the angular axis.")
    log_r: Any = Field(default=False, description="[AXES] If True, radial axis uses a logarithmic scale.")
    
    # === MAP & POLAR ===
    direction: Any = Field(default='clockwise', description="[MAP & POLAR] Sets angular axis direction: 'counterclockwise' or 'clockwise' (default).")
    start_angle: Any = Field(default=90, description="[MAP & POLAR] Sets starting angle for the angular axis; 0 is due east, 90 is due north.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash-patterns to lines based on column values.")
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups data into separate lines based on column values.")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for categorical line dash mapping.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific categorical values to plotly.js dash-patterns for lines; use 'identity' to apply dash names directly.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] If True, shows markers on lines.")
    line_close: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] If True, connects the last point to the first to close the line.")
    line_shape: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sets line shape: 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Overrides default axis, legend, and hover labels; dict keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    render_mode: Any = Field(default='auto', description="[ADVANCED OPTIONS] Drawing mode: 'auto', 'svg', or 'webgl'; affects rendering performance and output type.")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyLinePolarTool(BasePlottingTool):
    name = "plotting_line_polar"
    description = "In a polar line plot, each row of `data_frame` is represented as a"
    input_model = LinePolarInput
    _plot_function = staticmethod(px.line_polar)

class LineTernaryInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    a: Any = Field(default=None, description="[CORE DATA] Column values for a-axis positioning in ternary coordinates.")
    b: Any = Field(default=None, description="[CORE DATA] Column values for b-axis positioning in ternary coordinates.")
    c: Any = Field(default=None, description="[CORE DATA] Column values for c-axis positioning in ternary coordinates.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; used when color values are not numeric.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycled when symbol is set.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use symbol values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values appear in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values appear as text labels on the figure.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash-patterns to lines based on column values.")
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups rows into lines based on column values.")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for line dash mapping; cycled when line_dash is set.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific categorical values to plotly.js dash-patterns, overriding line_dash_sequence; use 'identity' to use dash-pattern values directly.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    line_shape: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Line shape: 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels; dict keys are column names.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyLineTernaryTool(BasePlottingTool):
    name = "plotting_line_ternary"
    description = "In a ternary line plot, each row of `data_frame` is represented as"
    input_model = LineTernaryInput
    _plot_function = staticmethod(px.line_ternary)

class LineInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning. Supports wide or long data formats.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning. Supports wide or long data formats.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for mapping categorical values to line colors.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding the color sequence. Use 'identity' to use values as colors directly.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to line markers based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping when using the symbol parameter.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding the symbol sequence. Use 'identity' to use values as symbols directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on the plot.")
    
    # === ERROR BARS ===
    error_x: Any = Field(default=None, description="[ERROR BARS] Sizes x-axis error bars; used for positive direction if error_x_minus is set, otherwise symmetrical.")
    error_x_minus: Any = Field(default=None, description="[ERROR BARS] Sizes x-axis error bars in the negative direction; ignored if error_x is None.")
    error_y: Any = Field(default=None, description="[ERROR BARS] Sizes y-axis error bars; used for positive direction if error_y_minus is set, otherwise symmetrical.")
    error_y_minus: Any = Field(default=None, description="[ERROR BARS] Sizes y-axis error bars in the negative direction; ignored if error_y is None.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns data to facet subplots vertically (rows).")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns data to facet subplots horizontally (columns).")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default is 0.03 or 0.07 if facet_col_wrap is used.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range, overriding auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    line_group: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Groups rows into separate lines based on column values.")
    line_dash: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Assigns dash patterns to lines based on column values.")
    line_dash_sequence: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Sequence of plotly.js dash-patterns for categorical dash mapping when using line_dash.")
    line_dash_map: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Map specific categorical values to plotly.js dash-patterns, overriding the dash sequence. Use 'identity' to use values as dash-patterns directly.")
    markers: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Show markers on lines if True.")
    line_shape: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Line shape: 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels using a dict mapping column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns data to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Ensures object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    render_mode: Any = Field(default='auto', description="[ADVANCED OPTIONS] Rendering mode: 'auto', 'svg', or 'webgl'. 'svg' for <1000 points (vector), 'webgl' for large datasets (rasterized), 'auto' selects automatically.")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyLineTool(BasePlottingTool):
    name = "plotting_line"
    description = "In a 2D line plot, each row of `data_frame` is represented as a vertex of"
    input_model = LineInput
    _plot_function = staticmethod(px.line)

class ParallelCategoriesInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color values; accepts valid CSS colors and supports sequential, diverging, and cyclical scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets manual min and max for the continuous color scale, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    dimensions: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Columns used as dimensions for the ParallelCategories plot.")
    dimensions_max_cardinality: Any = Field(default=50, description="[PLOT-SPECIFIC OPTIONS] Maximum unique values allowed in a column for automatic dimension selection; columns exceeding this are excluded.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Plot width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Plot height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Custom labels for axes, legend, and hover; keys are column names, values are display labels.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyParallelCategoriesTool(BasePlottingTool):
    name = "plotting_parallel_categories"
    description = "In a parallel categories (or parallel sets) plot, each row of"
    input_model = ParallelCategoriesInput
    _plot_function = staticmethod(px.parallel_categories)

class ParallelCoordinatesInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color mapping; accepts CSS color strings or Plotly color scales (sequential, diverging, cyclical).")
    range_color: Any = Field(default=None, description="[COLORS] Manually sets the min and max range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint value for the continuous color scale, recommended for diverging color scales.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    dimensions: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Columns used as axes for multidimensional visualization in the ParallelCoordinates plot.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Plot width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Plot height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Custom labels for axes, legends, and hovers; keys are column names, values are display labels.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyParallelCoordinatesTool(BasePlottingTool):
    name = "plotting_parallel_coordinates"
    description = "In a parallel coordinates plot, each row of `data_frame` is represented"
    input_model = ParallelCoordinatesInput
    _plot_function = staticmethod(px.parallel_coordinates)

class PieInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for assigning colors to categorical values in Pie sectors, following `category_orders` unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors for Pie sectors, overriding `color_discrete_sequence`. Use 'identity' to use values as colors directly.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity for Pie sectors (0 to 1).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Column values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns Pie plots to facet rows based on column values (vertical faceting).")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns Pie plots to facet columns based on column values (horizontal faceting).")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row`/`marginal` is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows in paper units; default is 0.03 (or 0.07 with `facet_col_wrap`).")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns in paper units; default is 0.02.")
    
    # === HIERARCHY ===
    names: Any = Field(default=None, description="[HIERARCHY] Labels for Pie sectors.")
    values: Any = Field(default=None, description="[HIERARCHY] Values determining the size of each Pie sector.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    hole: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Fraction of radius cut out from the center to create a donut chart.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary mapping column names to custom labels for axis titles, legend, and hover text.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
class PlotlyPieTool(BasePlottingTool):
    name = "plotting_pie"
    description = "In a pie plot, each row of `data_frame` is represented as a sector of a"
    input_model = PieInput
    _plot_function = staticmethod(px.pie)

class Scatter3DInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning in Scatter3D plot.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning in Scatter3D plot.")
    z: Any = Field(default=None, description="[CORE DATA] Column values for z-axis positioning in Scatter3D plot.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use values as colors directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric color mapping; supports sequential, diverging, and cyclical color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale, overriding auto-scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets midpoint for continuous color scale, recommended for diverging color scales.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns marker symbols based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycles through sequence.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use values as symbols directly.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Assigns marker sizes based on column values.")
    size_max: Any = Field(default=None, description="[SIZE] Sets maximum marker size when using size mapping.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity; value between 0 and 1.")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels for markers from column values.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips from column values.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === ERROR BARS ===
    error_x: Any = Field(default=None, description="[ERROR BARS] Values for x-axis error bars; symmetrical if error_x_minus is None, otherwise positive direction only.")
    error_x_minus: Any = Field(default=None, description="[ERROR BARS] Values for negative x-axis error bars; ignored if error_x is None.")
    error_y: Any = Field(default=None, description="[ERROR BARS] Values for y-axis error bars; symmetrical if error_y_minus is None, otherwise positive direction only.")
    error_y_minus: Any = Field(default=None, description="[ERROR BARS] Values for negative y-axis error bars; ignored if error_y is None.")
    error_z: Any = Field(default=None, description="[ERROR BARS] Values for z-axis error bars; symmetrical if error_z_minus is None, otherwise positive direction only.")
    error_z_minus: Any = Field(default=None, description="[ERROR BARS] Values for negative z-axis error bars; ignored if error_z is None.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis if True.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis if True.")
    log_z: Any = Field(default=False, description="[AXES] Log-scale the z-axis if True.")
    range_x: Any = Field(default=None, description="[AXES] Sets custom x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Sets custom y-axis range, overriding auto-scaling.")
    range_z: Any = Field(default=None, description="[AXES] Sets custom z-axis range, overriding auto-scaling.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels; keys are column names.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Provides object constancy across animation frames; matching values treated as same object.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatter3DTool(BasePlottingTool):
    name = "plotting_scatter_3d"
    description = "In a 3D scatter plot, each row of `data_frame` is represented by a"
    input_model = Scatter3DInput
    _plot_function = staticmethod(px.scatter_3d)

class ScatterGeoInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning marks on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning marks on the map.")
    locations: Any = Field(default=None, description="[CORE DATA] Location identifiers mapped to coordinates based on `locationmode`.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding `color_discrete_sequence`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color mapping.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns symbols to marks based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding `symbol_sequence`.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Assigns marker sizes based on column values.")
    size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using `size`.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 and 1.")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Text labels to display on the map.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Bold text in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to facet rows (vertical subplots).")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to facet columns (horizontal subplots).")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if `facet_row`/`marginal` is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (in paper units).")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (in paper units).")
    
    # === GEOGRAPHY ===
    locationmode: Any = Field(default=None, description="[GEOGRAPHY] Determines how `locations` values are matched to regions: 'ISO-3', 'USA-states', or 'country names'.")
    geojson: Any = Field(default=None, description="[GEOGRAPHY] GeoJSON Polygon feature collection with IDs referenced by `locations`.")
    featureidkey: Any = Field(default=None, description="[GEOGRAPHY] Path to GeoJSON feature property used to match `locations` values.")
    projection: Any = Field(default=None, description="[GEOGRAPHY] Map projection type; options include 'equirectangular', 'mercator', 'orthographic', etc.")
    scope: Any = Field(default=None, description="[GEOGRAPHY] Map region to display; options include 'world', 'usa', 'europe', etc.")
    center: Any = Field(default=None, description="[GEOGRAPHY] Sets the map center point using a dict with 'lat' and 'lon'.")
    fitbounds: Any = Field(default=None, description="[GEOGRAPHY] Determines how map bounds are fit: `False`, `locations`, or `geojson`.")
    basemap_visible: Any = Field(default=None, description="[GEOGRAPHY] Controls visibility of the basemap.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hovers with custom labels; dict keys are column names.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group identifiers.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatterGeoTool(BasePlottingTool):
    name = "plotting_scatter_geo"
    description = "In a geographic scatter plot, each row of `data_frame` is represented"
    input_model = ScatterGeoInput
    _plot_function = staticmethod(px.scatter_geo)

# class ScatterMapInput(ToolInput):
#     # === CORE DATA ===
#     data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
#     lat: Any = Field(default=None, description="[CORE DATA] Latitude values for marker positioning on the map.")
#     lon: Any = Field(default=None, description="[CORE DATA] Longitude values for marker positioning on the map.")
    
#     # === COLORS ===
#     color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
#     color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
#     color_discrete_map: Any = Field(default=None, description="[COLORS] Maps specific categorical values to CSS colors; overrides color_discrete_sequence. Use 'identity' to use color values directly.")
#     color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric color mapping; used for continuous color gradients.")
#     range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale.")
#     color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
#     # === SIZE ===
#     size: Any = Field(default=None, description="[SIZE] Values used to determine marker sizes.")
#     size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using size.")
    
#     # === OPACITY ===
#     opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 and 1.")
    
#     # === HOVER & TEXT ===
#     text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on the map.")
#     hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
#     hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
#     # === GEOGRAPHY ===
#     center: Any = Field(default=None, description="[GEOGRAPHY] Dict with 'lat' and 'lon' to set the map's center point.")
    
#     # === MAP & POLAR ===
#     zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level, between 0 and 20.")
#     map_style: Any = Field(default=None, description="[MAP & POLAR] Base map style; valid values include 'basic', 'carto-darkmatter', 'carto-positron', 'dark', 'light', 'open-street-map', 'satellite', 'streets', etc.")
    
#     # === LAYOUT & STYLING ===
#     title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
#     subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
#     template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
#     width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
#     height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
#     # === DATA ORGANIZATION ===
#     category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
#     labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dict mapping column names to custom axis, legend, or hover labels.")
    
#     # === ANIMATION ===
#     animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign markers to animation frames.")
#     animation_group: Any = Field(default=None, description="[ANIMATION] Values used for object constancy across animation frames; matching values represent the same object in each frame.")
    
#     # === ADVANCED OPTIONS ===
#     custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
#     dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] ID of the dataset to use.")
# class PlotlyScatterMapTool(BasePlottingTool):
#     name = "plotting_scatter_map"
#     description = "In a scatter map, each row of `data_frame` is represented by a"
#     input_model = ScatterMapInput
#     _plot_function = staticmethod(px.scatter_map)

class ScatterMapboxInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    lat: Any = Field(default=None, description="[CORE DATA] Latitude values for positioning marks on the map.")
    lon: Any = Field(default=None, description="[CORE DATA] Longitude values for positioning marks on the map.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for categorical color mapping; cycled according to `category_orders` unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding `color_discrete_sequence`; use `'identity'` to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] List of CSS colors for continuous color scale when `color` is numeric.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the min and max range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Values used to determine marker sizes.")
    size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using `size`.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Values shown as text labels on the map.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === GEOGRAPHY ===
    center: Any = Field(default=None, description="[GEOGRAPHY] Dictionary with `'lat'` and `'lon'` to set the map center.")
    
    # === MAP & POLAR ===
    zoom: Any = Field(default=8, description="[MAP & POLAR] Map zoom level, between 0 and 20.")
    mapbox_style: Any = Field(default=None, description="[MAP & POLAR] Identifier of base map style, some of which require a Mapbox or Stadia Maps API token to be set using `plotly.express.set_mapbox_access_token()`. Allowed values which do not require a token are `'open-street-map'`, `'white-bg'`, `'carto- positron'`, `'carto-darkmatter'`. Allowed values which require a Mapbox API token are `'basic'`, `'streets'`, `'outdoors'`, `'light'`, `'dark'`, `'satellite'`, `'satellite-streets'`. Allowed values which require a Stadia Maps API token are `'stamen-terrain'`, `'stamen- toner'`, `'stamen-watercolor'`.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary mapping column names to custom axis, legend, and hover labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Values used for object-constancy across animation frames; matching values are treated as the same object.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatterMapboxTool(BasePlottingTool):
    name = "plotting_scatter_mapbox"
    description = "*scatter_mapbox* is deprecated! Use *scatter_map* instead."
    input_model = ScatterMapboxInput
    _plot_function = staticmethod(px.scatter_mapbox)

class ScatterMatrixInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for categorical color mapping, applied in order of `category_orders` unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding `color_discrete_sequence`. Use `'identity'` to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] List of CSS colors to define the continuous color scale for numeric color columns.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom min and max range for the continuous color scale.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Column values used to assign marker symbols in the ScatterMatrix plot.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping, applied in order of `category_orders` unless overridden by `symbol_map`.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding `symbol_sequence`. Use `'identity'` to use symbol names directly.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Column values used to assign marker sizes in the ScatterMatrix plot.")
    size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using `size`.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Column values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    dimensions: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Columns used as dimensions for the multidimensional ScatterMatrix visualization.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary to override default axis, legend, and hover labels for columns.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier to use for the plot.")
class PlotlyScatterMatrixTool(BasePlottingTool):
    name = "plotting_scatter_matrix"
    description = "In a scatter plot matrix (or SPLOM), each row of `data_frame` is"
    input_model = ScatterMatrixInput
    _plot_function = staticmethod(px.scatter_matrix)

class ScatterPolarInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    r: Any = Field(default=None, description="[CORE DATA] Values for radial axis positioning in polar coordinates.")
    theta: Any = Field(default=None, description="[CORE DATA] Values for angular axis positioning in polar coordinates.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use values directly as colors.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for continuous numeric color mapping; supports sequential, diverging, and cyclical color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale, overriding auto-scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets midpoint for continuous color scale; recommended for diverging color scales.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Values used to assign marker symbols.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycles through sequence for symbol values.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use values directly as symbols.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Values used to assign marker sizes.")
    size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using size mapping.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, from 0 (transparent) to 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values shown as text labels on the plot.")
    
    # === AXES ===
    range_r: Any = Field(default=None, description="[AXES] Sets custom range for the radial axis, overriding auto-scaling.")
    range_theta: Any = Field(default=None, description="[AXES] Sets custom range for the angular axis, overriding auto-scaling.")
    log_r: Any = Field(default=False, description="[AXES] If True, radial axis uses a logarithmic scale.")
    
    # === MAP & POLAR ===
    direction: Any = Field(default='clockwise', description="[MAP & POLAR] Sets angular axis direction: 'clockwise' (default) or 'counterclockwise'.")
    start_angle: Any = Field(default=90, description="[MAP & POLAR] Sets starting angle for the angular axis; 0 is due east, 90 is due north.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels with custom names; keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Values used for object constancy across animation frames; matching values treated as the same object.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    render_mode: Any = Field(default='auto', description="[ADVANCED OPTIONS] Rendering mode: 'auto', 'svg' (vector, <1000 points), or 'webgl' (raster, >1000 points).")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatterPolarTool(BasePlottingTool):
    name = "plotting_scatter_polar"
    description = "In a polar scatter plot, each row of `data_frame` is represented by a"
    input_model = ScatterPolarInput
    _plot_function = staticmethod(px.scatter_polar)

class ScatterTernaryInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    a: Any = Field(default=None, description="[CORE DATA] Values for positioning marks along the a axis in ternary coordinates.")
    b: Any = Field(default=None, description="[CORE DATA] Values for positioning marks along the b axis in ternary coordinates.")
    c: Any = Field(default=None, description="[CORE DATA] Values for positioning marks along the c axis in ternary coordinates.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric color mapping; builds continuous color scale for numeric data.")
    range_color: Any = Field(default=None, description="[COLORS] Sets the range for the continuous color scale, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Values used to assign symbols to marks.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycles through sequence for symbol values.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific categorical values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use symbol values directly.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Values used to assign marker sizes.")
    size_max: Any = Field(default=None, description="[SIZE] Maximum marker size when using size mapping.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Marker opacity, between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    text: Any = Field(default=None, description="[HOVER & TEXT] Values displayed as text labels on the plot.")
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Figure subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis titles, legend entries, and hover labels with custom labels; keys are column names, values are display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Values used to assign marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Values providing object constancy across animation frames; matching groups are treated as the same object in each frame.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatterTernaryTool(BasePlottingTool):
    name = "plotting_scatter_ternary"
    description = "In a ternary scatter plot, each row of `data_frame` is represented by a"
    input_model = ScatterTernaryInput
    _plot_function = staticmethod(px.scatter_ternary)

class ScatterInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning in Scatter plot; supports wide or long data formats.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning in Scatter plot; supports wide or long data formats.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; cycles through sequence for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use values as colors directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] CSS color scale for numeric color mapping; supports sequential, diverging, or cyclical color scales.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for continuous color scales; recommended for diverging color scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale, overriding auto-scaling.")
    
    # === SYMBOLS/MARKERS ===
    symbol: Any = Field(default=None, description="[SYMBOLS/MARKERS] Assigns marker symbols based on column values.")
    symbol_sequence: Any = Field(default=None, description="[SYMBOLS/MARKERS] Sequence of plotly.js symbols for categorical symbol mapping; cycles through sequence for symbol values.")
    symbol_map: Any = Field(default=None, description="[SYMBOLS/MARKERS] Map specific values to plotly.js symbols, overriding symbol_sequence; use 'identity' to use values as symbols directly.")
    
    # === SIZE ===
    size: Any = Field(default=None, description="[SIZE] Assigns marker sizes based on column values.")
    size_max: Any = Field(default=None, description="[SIZE] Sets maximum marker size when using size mapping.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] Sets marker opacity; value between 0 and 1.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values appear in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] Values appear as text labels on the plot.")
    
    # === ERROR BARS ===
    error_x: Any = Field(default=None, description="[ERROR BARS] Sets x-axis error bar sizes; if error_x_minus is None, error bars are symmetrical, otherwise used for positive direction only.")
    error_x_minus: Any = Field(default=None, description="[ERROR BARS] Sets x-axis error bar sizes in the negative direction; ignored if error_x is None.")
    error_y: Any = Field(default=None, description="[ERROR BARS] Sets y-axis error bar sizes; if error_y_minus is None, error bars are symmetrical, otherwise used for positive direction only.")
    error_y_minus: Any = Field(default=None, description="[ERROR BARS] Sets y-axis error bar sizes in the negative direction; ignored if error_y is None.")
    
    # === TRENDLINES ===
    trendline: Any = Field(default=None, description="[TRENDLINES] One of `'ols'`, `'lowess'`, `'rolling'`, `'expanding'` or `'ewm'`. If `'ols'`, an Ordinary Least Squares regression line will be drawn for each discrete-color/symbol group. If `'lowess`', a Locally Weighted Scatterplot Smoothing line will be drawn for each discrete-color/symbol group. If `'rolling`', a Rolling (e.g. rolling average, rolling median) line will be drawn for each discrete-color/symbol group. If `'expanding`', an Expanding (e.g. expanding average, expanding sum) line will be drawn for each discrete-color/symbol group. If `'ewm`', an Exponentially Weighted Moment (e.g. exponentially-weighted moving average) line will be drawn for each discrete-color/symbol group. See the docstrings for the functions in `plotly.express.trendline_functions` for more details on these functions and how to configure them with the `trendline_options` argument.")
    trendline_options: Any = Field(default=None, description="[TRENDLINES] Options passed to the trendline function specified by trendline.")
    trendline_color_override: Any = Field(default=None, description="[TRENDLINES] Sets trendline color; overrides default trendline coloring.")
    trendline_scope: Any = Field(default='trace', description="[TRENDLINES] If `'trace'`, then one trendline is drawn per trace (i.e. per color, symbol, facet, animation frame etc) and if `'overall'` then one trendline is computed for the entire dataset, and replicated across all facets.")
    
    # === MARGINAL PLOTS ===
    marginal_x: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a horizontal subplot above the main plot to show x-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    marginal_y: Any = Field(default=None, description="[MARGINAL PLOTS] Adds a vertical subplot to the right of the main plot to show y-distribution; options: 'rug', 'box', 'violin', 'histogram'.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots based on column values.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots based on column values.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns; wraps columns into multiple rows if exceeded; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default 0.03, or 0.07 if facet_col_wrap is used.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] If True, x-axis uses logarithmic scale.")
    log_y: Any = Field(default=False, description="[AXES] If True, y-axis uses logarithmic scale.")
    range_x: Any = Field(default=None, description="[AXES] Sets custom x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Sets custom y-axis range, overriding auto-scaling.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default axis, legend, and hover labels; dict keys are column names, values are display labels.")
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Provides object-constancy across animation frames; matching values treated as same object in each frame.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    render_mode: Any = Field(default='auto', description="[ADVANCED OPTIONS] Sets rendering mode: 'auto', 'svg', or 'webgl'; 'svg' for <1000 points, 'webgl' for larger datasets.")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyScatterTool(BasePlottingTool):
    name = "plotting_scatter"
    description = "In a scatter plot, each row of `data_frame` is represented by a symbol"
    input_model = ScatterInput
    _plot_function = staticmethod(px.scatter)

class SetMapboxAccessTokenInput(ToolInput):
    # === PLOT-SPECIFIC OPTIONS ===
    token: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Mapbox access token for authenticating map tiles in SetMapboxAccessToken plot.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title displayed above the SetMapboxAccessToken plot.")
    
    # === ADVANCED OPTIONS ===
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Identifier for the dataset used in the SetMapboxAccessToken plot.")
class PlotlySetMapboxAccessTokenTool(BasePlottingTool):
    name = "plotting_set_mapbox_access_token"
    description = "Arguments:"
    input_model = SetMapboxAccessTokenInput
    _plot_function = staticmethod(px.set_mapbox_access_token)

class StripInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning; accepts single or multiple columns for wide or long data formats.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning; accepts single or multiple columns for wide or long data formats.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping; used when color values are non-numeric.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns marks to vertical facet subplots based on column values.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns marks to horizontal facet subplots based on column values.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows, in paper units; defaults to 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns, in paper units; default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range, overriding auto-scaling.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    stripmode: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Strip arrangement mode: 'overlay' draws strips on top of each other; 'group' places them side by side.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override default axis, legend, and hover labels using a dict mapping column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns marks to animation frames based on column values.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames using group identifiers.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyStripTool(BasePlottingTool):
    name = "plotting_strip"
    description = "In a strip plot each row of `data_frame` is represented as a jittered"
    input_model = StripInput
    _plot_function = staticmethod(px.strip)

class SunburstInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color values; accepts CSS color strings from Plotly color modules.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom range for continuous color scale, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint for the continuous color scale, recommended for diverging color scales.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for categorical color mapping; cycles through values when color is non-numeric.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Maps specific categorical values to CSS colors, overriding the discrete color sequence; use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values displayed in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === HIERARCHY ===
    names: Any = Field(default=None, description="[HIERARCHY] Labels for Sunburst sectors.")
    values: Any = Field(default=None, description="[HIERARCHY] Values used to determine the size of each sector.")
    parents: Any = Field(default=None, description="[HIERARCHY] Parent sector for each item, defining hierarchy in Sunburst.")
    path: Any = Field(default=None, description="[HIERARCHY] List of columns defining the hierarchical path from root to leaves; cannot be used with ids or parents.")
    ids: Any = Field(default=None, description="[HIERARCHY] Unique identifiers for each sector.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    branchvalues: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] 'total' treats each value as the sum of all descendants; 'remainder' treats branch values as the difference from the sum of their leaves.")
    maxdepth: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Maximum number of hierarchy levels to display; set to -1 to show all levels.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Plot width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Plot height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Dictionary to override default column names for axis titles, legend entries, and hovers.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier to use for the plot.")
class PlotlySunburstTool(BasePlottingTool):
    name = "plotting_sunburst"
    description = "A sunburst plot represents hierarchial data as sectors laid out over"
    input_model = SunburstInput
    _plot_function = staticmethod(px.sunburst)

class TimelineInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x_start: Any = Field(default=None, description="[CORE DATA] Either a name of a column in `data_frame`, or a pandas Series or array_like object. (required) Values from this column or array_like are used to position marks along the x axis in cartesian coordinates.")
    x_end: Any = Field(default=None, description="[CORE DATA] Either a name of a column in `data_frame`, or a pandas Series or array_like object. (required) Values from this column or array_like are used to position marks along the x axis in cartesian coordinates.")
    y: Any = Field(default=None, description="[CORE DATA] y: Column values for y-axis positioning in Timeline plot.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] color_discrete_sequence: CSS color sequence for categorical color mapping, cycled for non-numeric color values.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] color_discrete_map: Maps specific categorical values to CSS colors, overriding color_discrete_sequence; use 'identity' to use color values directly.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] color_continuous_scale: CSS color scale for numeric color mapping; supports sequential, diverging, and cyclical color scales.")
    range_color: Any = Field(default=None, description="[COLORS] range_color: Sets custom range for continuous color scale, overriding auto-scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] color_continuous_midpoint: Sets midpoint for continuous color scale, recommended for diverging color scales.")
    
    # === PATTERNS ===
    pattern_shape: Any = Field(default=None, description="[PATTERNS] pattern_shape: Column values used to assign pattern shapes to Timeline marks.")
    pattern_shape_sequence: Any = Field(default=None, description="[PATTERNS] pattern_shape_sequence: Sequence of pattern shapes assigned to categorical values, cycled as needed.")
    pattern_shape_map: Any = Field(default=None, description="[PATTERNS] pattern_shape_map: Maps specific values to pattern shapes, overriding pattern_shape_sequence; use 'identity' to use values directly.")
    
    # === OPACITY ===
    opacity: Any = Field(default=None, description="[OPACITY] opacity: Sets marker opacity; value between 0 (transparent) and 1 (opaque).")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] hover_name: Column values shown in bold in hover tooltips.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    text: Any = Field(default=None, description="[HOVER & TEXT] text: Column values displayed as text labels on the plot.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] facet_row: Assigns marks to vertical facet subplots based on column values.")
    facet_col: Any = Field(default=None, description="[FACETS] facet_col: Assigns marks to horizontal facet subplots based on column values.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] facet_col_wrap: Maximum number of facet columns before wrapping to a new row; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] facet_row_spacing: Spacing between facet rows (in paper units); default is 0.03, or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] facet_col_spacing: Spacing between facet columns (in paper units); default is 0.02.")
    
    # === AXES ===
    range_x: Any = Field(default=None, description="[AXES] range_x: Sets custom x-axis range, overriding auto-scaling.")
    range_y: Any = Field(default=None, description="[AXES] range_y: Sets custom y-axis range, overriding auto-scaling.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] title: Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] subtitle: Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] width: Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] height: Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] labels: Dictionary mapping column names to custom axis, legend, and hover labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] animation_frame: Column values used to assign marks to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] animation_group: Column values used for object constancy across animation frames.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] dataset_id: ID of the dataset used for the plot.")
class PlotlyTimelineTool(BasePlottingTool):
    name = "plotting_timeline"
    description = "In a timeline plot, each row of `data_frame` is represented as a rectangular"
    input_model = TimelineInput
    _plot_function = staticmethod(px.timeline)

class TreemapInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_continuous_scale: Any = Field(default=None, description="[COLORS] Continuous color scale for numeric color values; accepts CSS color strings and supports sequential, diverging, or cyclical scales.")
    range_color: Any = Field(default=None, description="[COLORS] Sets custom min and max for the continuous color scale, overriding automatic scaling.")
    color_continuous_midpoint: Any = Field(default=None, description="[COLORS] Sets the midpoint of the continuous color scale, recommended for diverging color scales.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] Sequence of CSS colors for mapping categorical color values; follows `category_orders` unless overridden by `color_discrete_map`.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Maps specific categorical values to CSS colors, overriding the discrete sequence; use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Column values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === HIERARCHY ===
    names: Any = Field(default=None, description="[HIERARCHY] Labels for Treemap sectors.")
    values: Any = Field(default=None, description="[HIERARCHY] Values assigned to sectors, determining their size.")
    parents: Any = Field(default=None, description="[HIERARCHY] Parent sector identifiers for defining the Treemap hierarchy.")
    ids: Any = Field(default=None, description="[HIERARCHY] Unique identifiers for each sector.")
    path: Any = Field(default=None, description="[HIERARCHY] List of columns defining the hierarchy from root to leaves; cannot be used with `ids` or `parents`.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    branchvalues: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Determines value summing: 'total' treats values as including all descendants; 'remainder' treats values as the difference from the sum of leaves.")
    maxdepth: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Maximum number of hierarchy levels to display; set to -1 to show all levels.")
    
    # === LAYOUT & STYLING ===
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Plot width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Plot height in pixels.")
    
    # === DATA ORGANIZATION ===
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Overrides default column names for axis titles, legend, and hover labels; keys are column names, values are display labels.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset identifier.")
class PlotlyTreemapTool(BasePlottingTool):
    name = "plotting_treemap"
    description = "A treemap plot represents hierarchial data as nested rectangular"
    input_model = TreemapInput
    _plot_function = staticmethod(px.treemap)

class ViolinInput(ToolInput):
    # === CORE DATA ===
    data_frame: Any = Field(default=None, description="[CORE DATA] This argument needs to be passed for column names (and not keyword names) to be used. Array-like and dict are transformed internally to a pandas DataFrame. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments.")
    x: Any = Field(default=None, description="[CORE DATA] Column values for x-axis positioning; supports wide or long data format.")
    y: Any = Field(default=None, description="[CORE DATA] Column values for y-axis positioning; supports wide or long data format.")
    
    # === COLORS ===
    color: Any = Field(default=None, description="[COLORS] Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column or array_like are used to assign color to marks. This argument is for mapping data values to colors. To set a single, uniform color for all points (e.g., 'red'), use the 'color_discrete_sequence' argument instead, like `color_discrete_sequence=['red']`.")
    color_discrete_sequence: Any = Field(default=None, description="[COLORS] CSS color sequence for categorical color mapping in Violin plot.")
    color_discrete_map: Any = Field(default=None, description="[COLORS] Map specific categorical values to CSS colors for Violin plot; use 'identity' to use color values directly.")
    
    # === HOVER & TEXT ===
    hover_name: Any = Field(default=None, description="[HOVER & TEXT] Values shown in bold in the hover tooltip.")
    hover_data: Any = Field(default=None, description="[HOVER & TEXT] Either a name or list of names of columns in `data_frame`, or pandas Series, or array_like objects or a dict with column names as keys, with values True (for default formatting) False (in order to remove this column from hover information), or a formatting string, for example ':.3f' or '|%a' or list-like data to appear in the hover tooltip or tuples with a bool or formatting string as first element, and list-like data to appear in hover as second element Values from these columns appear as extra data in the hover tooltip.")
    
    # === FACETS ===
    facet_row: Any = Field(default=None, description="[FACETS] Assigns violins to vertically faceted subplots.")
    facet_col: Any = Field(default=None, description="[FACETS] Assigns violins to horizontally faceted subplots.")
    facet_col_wrap: Any = Field(default=0, description="[FACETS] Maximum number of facet columns before wrapping to new rows; ignored if 0 or if facet_row/marginal is set.")
    facet_row_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet rows (paper units); default is 0.03 or 0.07 with facet_col_wrap.")
    facet_col_spacing: Any = Field(default=None, description="[FACETS] Spacing between facet columns (paper units); default is 0.02.")
    
    # === AXES ===
    log_x: Any = Field(default=False, description="[AXES] Log-scale the x-axis.")
    log_y: Any = Field(default=False, description="[AXES] Log-scale the y-axis.")
    range_x: Any = Field(default=None, description="[AXES] Manually set x-axis range.")
    range_y: Any = Field(default=None, description="[AXES] Manually set y-axis range.")
    
    # === PLOT-SPECIFIC OPTIONS ===
    violinmode: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] 'group' places violins side by side; 'overlay' draws violins on top of each other.")
    points: Any = Field(default=None, description="[PLOT-SPECIFIC OPTIONS] Controls which sample points are shown: 'outliers', 'suspectedoutliers', 'all', or False (none).")
    box: Any = Field(default=False, description="[PLOT-SPECIFIC OPTIONS] Draw boxes inside violins if True.")
    
    # === LAYOUT & STYLING ===
    orientation: Any = Field(default=None, description="[LAYOUT & STYLING] (default `'v'` if `x` and `y` are provided and both continuous or both categorical,  otherwise `'v'`(`'h'`) if `x`(`y`) is categorical and `y`(`x`) is continuous,  otherwise `'v'`(`'h'`) if only `x`(`y`) is provided)")
    title: Optional[str] = Field(default=None, description="[LAYOUT & STYLING] Plot title.")
    subtitle: Any = Field(default=None, description="[LAYOUT & STYLING] Plot subtitle.")
    template: Any = Field(default=None, description="[LAYOUT & STYLING] The figure template name (must be a key in plotly.io.templates) or definition.")
    width: Any = Field(default=None, description="[LAYOUT & STYLING] Figure width in pixels.")
    height: Any = Field(default=None, description="[LAYOUT & STYLING] Figure height in pixels.")
    
    # === DATA ORGANIZATION ===
    category_orders: Any = Field(default=None, description="[DATA ORGANIZATION] By default, in Python 3.6+, the order of categorical values in axes, legends and facets depends on the order in which these values are first encountered in `data_frame` (and no order is guaranteed by default in Python below 3.6). This parameter is used to force a specific ordering of values per column. The keys of this dict should correspond to column names, and the values should be lists of strings corresponding to the specific display order desired.")
    labels: Any = Field(default=None, description="[DATA ORGANIZATION] Override axis, legend, and hover labels with a dict mapping column names to display labels.")
    
    # === ANIMATION ===
    animation_frame: Any = Field(default=None, description="[ANIMATION] Assigns violins to animation frames.")
    animation_group: Any = Field(default=None, description="[ANIMATION] Maintains object constancy across animation frames by grouping rows with matching values.")
    
    # === ADVANCED OPTIONS ===
    custom_data: Any = Field(default=None, description="[ADVANCED OPTIONS] Either name or list of names of columns in `data_frame`, or pandas Series, or array_like objects Values from these columns are extra data, to be used in widgets or Dash callbacks for example. This data is not user-visible but is included in events emitted by the figure (lasso selection etc.)")
    dataset_id: Optional[str] = Field(default='generated', description="[ADVANCED OPTIONS] Dataset ID to use.")
class PlotlyViolinTool(BasePlottingTool):
    name = "plotting_violin"
    description = "In a violin plot, rows of `data_frame` are grouped together into a"
    input_model = ViolinInput
    _plot_function = staticmethod(px.violin)

