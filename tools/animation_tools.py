"""
Animation Tools for Data Science UI

Provides tools for creating real-time animated visualizations using Dash's interval components
and state management, inspired by successful boids simulation patterns.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from tools.base import ToolInput, BaseTool
from core.plot_manager import global_plot_manager


class AnimationFrameInput(ToolInput):
    """Input for creating animation frames from data"""
    
    # Core data
    data_source: str = Field(description="Name of the dataset to animate")
    frame_column: str = Field(description="Column name that defines animation frames (e.g., 'time', 'step', 'frame')")
    
    # Plot configuration
    plot_type: str = Field(default="scatter", description="Type of plot: 'scatter', 'line', 'bar', 'histogram'")
    x_column: str = Field(description="Column for x-axis")
    y_column: Optional[str] = Field(default=None, description="Column for y-axis (not needed for histogram)")
    
    # Animation settings
    frame_duration: int = Field(default=100, description="Duration of each frame in milliseconds")
    transition_duration: int = Field(default=50, description="Transition duration between frames in milliseconds")
    
    # Styling
    color_column: Optional[str] = Field(default=None, description="Column to color points/lines by")
    size_column: Optional[str] = Field(default=None, description="Column to size points by")
    title: str = Field(default="Animated Visualization", description="Plot title")
    
    # Advanced options
    group_column: Optional[str] = Field(default=None, description="Column for grouping objects across frames (for object constancy)")
    range_x: Optional[List[float]] = Field(default=None, description="Fixed x-axis range [min, max]")
    range_y: Optional[List[float]] = Field(default=None, description="Fixed y-axis range [min, max]")


class RealTimeAnimationInput(ToolInput):
    """Input for creating real-time animated simulations"""
    
    # Simulation parameters
    simulation_type: str = Field(description="Type of simulation: 'random_walk', 'oscillator', 'spiral', 'custom'")
    num_objects: int = Field(default=50, description="Number of animated objects")
    num_frames: int = Field(default=100, description="Number of frames to generate")
    
    # Animation settings
    frame_duration: int = Field(default=100, description="Duration of each frame in milliseconds")
    
    # Styling
    marker_size: int = Field(default=8, description="Size of markers")
    color_scheme: str = Field(default="viridis", description="Color scheme for objects")
    title: str = Field(default="Real-Time Animation", description="Plot title")
    
    # Bounds
    x_range: List[float] = Field(default=[-10, 10], description="X-axis range [min, max]")
    y_range: List[float] = Field(default=[-10, 10], description="Y-axis range [min, max]")


class AnimationFrameTool(BaseTool):
    """Create animated plots from existing data with frame columns"""
    
    name: str = "animation_frame"
    description: str = "Create animated plots from datasets with frame/time columns. Supports scatter, line, bar, and histogram animations with customizable timing and styling."
    input_model = AnimationFrameInput
    
    def execute(self, job_id: str, inputs: AnimationFrameInput) -> Dict[str, Any]:
        """Create an animated plot from data with frame information"""
        
        try:
            self.update_progress(job_id, 10, "Loading dataset...")
            
            # Import here to avoid circular imports
            from tools.data_tools import uploaded_datasets
            
            # Get the dataset
            if inputs.data_source not in uploaded_datasets:
                return {
                    "success": False,
                    "error": f"Dataset '{inputs.data_source}' not found. Available datasets: {list(uploaded_datasets.keys())}"
                }
            
            df = uploaded_datasets[inputs.data_source].copy()
            
            # Validate required columns
            required_cols = [inputs.frame_column, inputs.x_column]
            if inputs.y_column:
                required_cols.append(inputs.y_column)
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return {
                    "success": False,
                    "error": f"Missing columns: {missing_cols}. Available columns: {list(df.columns)}"
                }
            
            self.update_progress(job_id, 50, "Creating animated plot...")
            
            # Create the animated plot
            fig = self._create_animated_figure(df, inputs)
            
            self.update_progress(job_id, 80, "Storing plot...")
            
            # Store the plot
            plot_id = str(uuid.uuid4())
            plot_info = {
                "id": plot_id,
                "figure": fig,
                "timestamp": datetime.now(),
                "job_id": job_id,
                "plot_data": {
                    "type": f"animated_{inputs.plot_type}",
                    "title": inputs.title,
                    "frames": len(fig.frames) if hasattr(fig, 'frames') else 0
                }
            }
            
            global_plot_manager.add_plot(plot_info)
            
            self.update_progress(job_id, 100, "Animation created successfully!")
            
            return {
                "success": True,
                "plot_id": plot_id,
                "message": f"Created animated {inputs.plot_type} plot with {len(fig.frames)} frames",
                "frames": len(fig.frames),
                "frame_duration": inputs.frame_duration
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating animated plot: {str(e)}"
            }
    
    def _create_animated_figure(self, df: pd.DataFrame, input_data: AnimationFrameInput) -> go.Figure:
        """Create the animated figure based on plot type"""
        
        # Get unique frame values and sort them
        frames = sorted(df[input_data.frame_column].unique())
        
        if input_data.plot_type == "scatter":
            return self._create_animated_scatter(df, input_data, frames)
        elif input_data.plot_type == "line":
            return self._create_animated_line(df, input_data, frames)
        elif input_data.plot_type == "bar":
            return self._create_animated_bar(df, input_data, frames)
        elif input_data.plot_type == "histogram":
            return self._create_animated_histogram(df, input_data, frames)
        else:
            raise ValueError(f"Unsupported plot type: {input_data.plot_type}")
    
    def _create_animated_scatter(self, df: pd.DataFrame, input_data: AnimationFrameInput, frames: List) -> go.Figure:
        """Create animated scatter plot"""
        
        # Create the figure using plotly express with animation
        fig = px.scatter(
            df,
            x=input_data.x_column,
            y=input_data.y_column,
            color=input_data.color_column,
            size=input_data.size_column,
            title=input_data.title,
            animation_frame=input_data.frame_column,
            animation_group=input_data.group_column
        )
        
        # Update layout for animation
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": input_data.frame_duration, "redraw": True},
                            "transition": {"duration": input_data.transition_duration}
                        }]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }]
        )
        
        # Set fixed ranges if provided
        if input_data.range_x:
            fig.update_xaxes(range=input_data.range_x)
        if input_data.range_y:
            fig.update_yaxes(range=input_data.range_y)
        
        return fig
    
    def _create_animated_line(self, df: pd.DataFrame, input_data: AnimationFrameInput, frames: List) -> go.Figure:
        """Create animated line plot"""
        
        fig = px.line(
            df,
            x=input_data.x_column,
            y=input_data.y_column,
            color=input_data.color_column,
            title=input_data.title,
            animation_frame=input_data.frame_column,
            animation_group=input_data.group_column
        )
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": input_data.frame_duration}}]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                    }
                ]
            }]
        )
        
        return fig
    
    def _create_animated_bar(self, df: pd.DataFrame, input_data: AnimationFrameInput, frames: List) -> go.Figure:
        """Create animated bar plot"""
        
        fig = px.bar(
            df,
            x=input_data.x_column,
            y=input_data.y_column,
            color=input_data.color_column,
            title=input_data.title,
            animation_frame=input_data.frame_column,
            animation_group=input_data.group_column
        )
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": input_data.frame_duration}}]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                    }
                ]
            }]
        )
        
        return fig
    
    def _create_animated_histogram(self, df: pd.DataFrame, input_data: AnimationFrameInput, frames: List) -> go.Figure:
        """Create animated histogram"""
        
        fig = px.histogram(
            df,
            x=input_data.x_column,
            color=input_data.color_column,
            title=input_data.title,
            animation_frame=input_data.frame_column
        )
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": input_data.frame_duration}}]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                    }
                ]
            }]
        )
        
        return fig


class RealTimeAnimationTool(BaseTool):
    """Create real-time animated simulations"""
    
    name: str = "real_time_animation"
    description: str = "Generate real-time animated simulations including random walks, oscillators, and spiral patterns. Creates physics-based animations with customizable parameters."
    input_model = RealTimeAnimationInput
    
    def execute(self, job_id: str, inputs: RealTimeAnimationInput) -> Dict[str, Any]:
        """Create a real-time animated simulation"""
        
        try:
            self.update_progress(job_id, 20, "Generating simulation data...")
            
            # Generate simulation data
            df = self._generate_simulation_data(inputs)
            
            self.update_progress(job_id, 60, "Creating animated plot...")
            
            # Create the animated plot
            fig = self._create_real_time_figure(df, inputs)
            
            self.update_progress(job_id, 80, "Storing plot and data...")
            
            # Store the plot
            plot_id = str(uuid.uuid4())
            plot_info = {
                "id": plot_id,
                "figure": fig,
                "timestamp": datetime.now(),
                "job_id": job_id,
                "plot_data": {
                    "type": f"realtime_{inputs.simulation_type}",
                    "title": inputs.title,
                    "frames": inputs.num_frames,
                    "objects": inputs.num_objects
                }
            }
            
            global_plot_manager.add_plot(plot_info)
            
            # Also save the generated data for potential reuse
            from tools.data_tools import uploaded_datasets
            dataset_name = f"animation_data_{plot_id[:8]}"
            uploaded_datasets[dataset_name] = df
            
            self.update_progress(job_id, 100, "Real-time animation created!")
            
            return {
                "success": True,
                "plot_id": plot_id,
                "dataset_name": dataset_name,
                "message": f"Created real-time {inputs.simulation_type} animation with {inputs.num_objects} objects over {inputs.num_frames} frames",
                "frames": inputs.num_frames,
                "objects": inputs.num_objects
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating real-time animation: {str(e)}"
            }
    
    def _generate_simulation_data(self, input_data: RealTimeAnimationInput) -> pd.DataFrame:
        """Generate simulation data based on type"""
        
        np.random.seed(42)  # For reproducible results
        
        if input_data.simulation_type == "random_walk":
            return self._generate_random_walk(input_data)
        elif input_data.simulation_type == "oscillator":
            return self._generate_oscillator(input_data)
        elif input_data.simulation_type == "spiral":
            return self._generate_spiral(input_data)
        else:
            # Default to random walk
            return self._generate_random_walk(input_data)
    
    def _generate_random_walk(self, input_data: RealTimeAnimationInput) -> pd.DataFrame:
        """Generate random walk simulation data"""
        
        data = []
        
        # Initialize positions
        x_range = input_data.x_range
        y_range = input_data.y_range
        positions = np.random.uniform(
            [x_range[0], y_range[0]], 
            [x_range[1], y_range[1]], 
            (input_data.num_objects, 2)
        )
        
        for frame in range(input_data.num_frames):
            for obj_id in range(input_data.num_objects):
                x, y = positions[obj_id]
                data.append({
                    'frame': frame,
                    'object_id': obj_id,
                    'x': x,
                    'y': y,
                    'color_value': obj_id / input_data.num_objects  # For coloring
                })
            
            # Update positions with random walk
            step_size = 0.1
            steps = np.random.normal(0, step_size, (input_data.num_objects, 2))
            positions += steps
            
            # Bounce off boundaries
            positions[:, 0] = np.clip(positions[:, 0], x_range[0], x_range[1])
            positions[:, 1] = np.clip(positions[:, 1], y_range[0], y_range[1])
        
        return pd.DataFrame(data)
    
    def _generate_oscillator(self, input_data: RealTimeAnimationInput) -> pd.DataFrame:
        """Generate oscillator simulation data"""
        
        data = []
        
        for frame in range(input_data.num_frames):
            t = frame * 0.1
            
            for obj_id in range(input_data.num_objects):
                # Create different oscillation patterns for each object
                phase = (obj_id / input_data.num_objects) * 2 * np.pi
                amplitude_x = (input_data.x_range[1] - input_data.x_range[0]) * 0.3
                amplitude_y = (input_data.y_range[1] - input_data.y_range[0]) * 0.3
                
                x = amplitude_x * np.sin(t + phase)
                y = amplitude_y * np.cos(t + phase * 1.5)
                
                data.append({
                    'frame': frame,
                    'object_id': obj_id,
                    'x': x,
                    'y': y,
                    'color_value': obj_id / input_data.num_objects
                })
        
        return pd.DataFrame(data)
    
    def _generate_spiral(self, input_data: RealTimeAnimationInput) -> pd.DataFrame:
        """Generate spiral simulation data"""
        
        data = []
        
        for frame in range(input_data.num_frames):
            t = frame * 0.1
            
            for obj_id in range(input_data.num_objects):
                # Create spiral pattern
                phase = (obj_id / input_data.num_objects) * 2 * np.pi
                radius = t * 0.5 + obj_id * 0.1
                
                x = radius * np.cos(t + phase)
                y = radius * np.sin(t + phase)
                
                data.append({
                    'frame': frame,
                    'object_id': obj_id,
                    'x': x,
                    'y': y,
                    'color_value': obj_id / input_data.num_objects
                })
        
        return pd.DataFrame(data)
    
    def _create_real_time_figure(self, df: pd.DataFrame, input_data: RealTimeAnimationInput) -> go.Figure:
        """Create the real-time animated figure"""
        
        fig = px.scatter(
            df,
            x='x',
            y='y',
            color='color_value',
            animation_frame='frame',
            animation_group='object_id',
            title=input_data.title,
            color_continuous_scale=input_data.color_scheme,
            range_x=input_data.x_range,
            range_y=input_data.y_range
        )
        
        # Update marker size
        fig.update_traces(marker=dict(size=input_data.marker_size))
        
        # Add animation controls with custom frame duration
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": input_data.frame_duration, "redraw": True},
                            "transition": {"duration": 50}
                        }]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                "steps": [
                    {
                        "args": [[f], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        "label": str(f),
                        "method": "animate"
                    }
                    for f in range(input_data.num_frames)
                ],
                "active": 0,
                "transition": {"duration": 0},
                "x": 0.1,
                "len": 0.9
            }]
        )
        
        # Remove colorbar for cleaner look
        fig.update_layout(coloraxis_showscale=False)
        
        return fig


class BoidsSimulationInput(ToolInput):
    """Input for creating boids flocking simulation"""
    
    # Simulation parameters
    num_birds: int = Field(default=50, description="Number of birds in the flock")
    num_frames: int = Field(default=200, description="Number of animation frames")
    
    # Flocking behavior parameters
    avoid_factor: float = Field(default=3.0, description="How strongly birds avoid each other")
    match_factor: float = Field(default=3.0, description="How strongly birds align with neighbors")
    centering_factor: float = Field(default=3.0, description="How strongly birds move toward flock center")
    
    # Environment parameters
    vision_range: float = Field(default=150.0, description="How far birds can see neighbors")
    min_speed: float = Field(default=2.0, description="Minimum flying speed")
    max_speed: float = Field(default=4.0, description="Maximum flying speed")
    turn_factor: float = Field(default=0.01, description="How strongly birds turn away from edges")
    
    # World bounds
    world_width: float = Field(default=200.0, description="Width of the world")
    world_height: float = Field(default=300.0, description="Height of the world")
    margin: float = Field(default=10.0, description="Margin from edges where birds start turning")
    
    # Animation settings
    frame_duration: int = Field(default=70, description="Duration of each frame in milliseconds")
    marker_size: int = Field(default=10, description="Size of bird markers")
    color_scheme: str = Field(default="rainbow", description="Color scheme for birds")
    title: str = Field(default="Boids Flocking Simulation", description="Plot title")


class BoidsSimulationTool(BaseTool):
    """Create a boids flocking simulation with realistic bird behavior"""
    
    name: str = "boids_simulation"
    description: str = "Create a realistic boids flocking simulation with customizable bird behavior parameters. Implements avoid, align, and cohesion rules with vectorized physics calculations."
    input_model = BoidsSimulationInput
    
    def execute(self, job_id: str, inputs: BoidsSimulationInput) -> Dict[str, Any]:
        """Create a boids flocking simulation"""
        
        try:
            self.update_progress(job_id, 20, "Initializing boids simulation...")
            
            # Generate boids simulation data
            df = self._generate_boids_simulation(inputs)
            
            self.update_progress(job_id, 70, "Creating animated visualization...")
            
            # Create the animated plot
            fig = self._create_boids_figure(df, inputs)
            
            self.update_progress(job_id, 90, "Storing simulation data...")
            
            # Store the plot
            plot_id = str(uuid.uuid4())
            plot_info = {
                "id": plot_id,
                "figure": fig,
                "timestamp": datetime.now(),
                "job_id": job_id,
                "plot_data": {
                    "type": "boids_simulation",
                    "title": inputs.title,
                    "frames": inputs.num_frames,
                    "birds": inputs.num_birds
                }
            }
            
            global_plot_manager.add_plot(plot_info)
            
            # Also save the generated data
            from tools.data_tools import uploaded_datasets
            dataset_name = f"boids_data_{plot_id[:8]}"
            uploaded_datasets[dataset_name] = df
            
            self.update_progress(job_id, 100, "Boids simulation complete!")
            
            return {
                "success": True,
                "plot_id": plot_id,
                "dataset_name": dataset_name,
                "message": f"Created boids simulation with {inputs.num_birds} birds over {inputs.num_frames} frames",
                "frames": inputs.num_frames,
                "birds": inputs.num_birds,
                "behavior_summary": {
                    "avoid_factor": inputs.avoid_factor,
                    "match_factor": inputs.match_factor,
                    "centering_factor": inputs.centering_factor,
                    "vision_range": inputs.vision_range
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating boids simulation: {str(e)}"
            }
    
    def _generate_boids_simulation(self, input_data: BoidsSimulationInput) -> pd.DataFrame:
        """Generate boids simulation data using vectorized operations"""
        
        np.random.seed(42)  # For reproducible results
        
        # Initialize bird positions and velocities
        positions = self._initialize_birds(input_data)
        velocities = self._initialize_velocities(input_data)
        
        data = []
        
        for frame in range(input_data.num_frames):
            # Record current state
            for bird_id in range(input_data.num_birds):
                x, y = positions[bird_id]
                vx, vy = velocities[bird_id]
                
                # Calculate direction angle for arrow markers
                angle = np.degrees(np.arctan2(vy, vx))
                
                data.append({
                    'frame': frame,
                    'bird_id': bird_id,
                    'x': x,
                    'y': y,
                    'vx': vx,
                    'vy': vy,
                    'angle': angle,
                    'color_value': bird_id / input_data.num_birds,
                    'speed': np.sqrt(vx*vx + vy*vy)
                })
            
            # Update positions and velocities using boids rules
            velocities = self._update_velocities(positions, velocities, input_data)
            positions = positions + velocities
        
        return pd.DataFrame(data)
    
    def _initialize_birds(self, input_data: BoidsSimulationInput) -> np.ndarray:
        """Initialize bird positions"""
        edge = min(input_data.world_width, input_data.world_height) - input_data.margin
        positions = np.random.multivariate_normal(
            [0, 0], 
            np.identity(2) * edge, 
            input_data.num_birds
        )
        return positions
    
    def _initialize_velocities(self, input_data: BoidsSimulationInput) -> np.ndarray:
        """Initialize bird velocities"""
        mean_v = np.random.uniform(-input_data.max_speed, input_data.max_speed, 2)
        velocities = np.random.multivariate_normal(
            mean_v, 
            np.identity(2) * 0.2, 
            input_data.num_birds
        )
        
        # Normalize to speed range
        speeds = np.linalg.norm(velocities, axis=1)
        speeds = np.clip(speeds, input_data.min_speed, input_data.max_speed)
        velocities = velocities / np.linalg.norm(velocities, axis=1)[:, np.newaxis] * speeds[:, np.newaxis]
        
        return velocities
    
    def _can_see(self, positions: np.ndarray, vision_range: float) -> np.ndarray:
        """Calculate which birds can see each other"""
        x = positions[:, 0].reshape(1, -1)
        y = positions[:, 1].reshape(1, -1)
        delta_x = x - x.T
        delta_y = y - y.T
        distances = np.sqrt(delta_x**2 + delta_y**2)
        
        in_vision = np.full(distances.shape, True)
        if vision_range > 0:
            in_vision[distances > vision_range] = False
        
        return in_vision
    
    def _scale_factor(self, positions: np.ndarray) -> np.ndarray:
        """Calculate inverse square distance scaling"""
        x = positions[:, 0].reshape(1, -1)
        y = positions[:, 1].reshape(1, -1)
        delta_x = x - x.T
        delta_y = y - y.T
        distances_sq = delta_x**2 + delta_y**2
        
        scale = np.zeros_like(distances_sq, dtype=float)
        scale[distances_sq != 0] = 1 / distances_sq[distances_sq != 0]
        
        return scale
    
    def _force_avoid(self, positions: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Calculate avoidance force"""
        in_vision = self._can_see(positions, input_data.vision_range)
        scale = self._scale_factor(positions)
        
        fudge_factor = 15
        n_in_vision = np.sum(in_vision, axis=1).astype(float)
        mask = n_in_vision != 0
        n_in_vision[mask] = 1 / n_in_vision[mask]
        
        x = positions[:, 0].reshape(1, -1)
        y = positions[:, 1].reshape(1, -1)
        delta_x = -(x - x.T) * scale * in_vision
        delta_y = -(y - y.T) * scale * in_vision
        
        dx = np.sum(delta_x, axis=1)
        dy = np.sum(delta_y, axis=1)
        
        dv = np.stack((dx, dy), axis=1) * n_in_vision.reshape(-1, 1) * input_data.avoid_factor * fudge_factor
        
        return dv
    
    def _force_align(self, positions: np.ndarray, velocities: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Calculate alignment force"""
        in_vision = self._can_see(positions, input_data.vision_range)
        scale = self._scale_factor(positions)
        
        fudge_factor = 10.84
        n_in_vision = np.sum(in_vision, axis=1).astype(float)
        mask = n_in_vision != 0
        n_in_vision[mask] = 1 / n_in_vision[mask]
        
        vx = velocities[:, 0]
        vy = velocities[:, 1]
        n = len(vx)
        
        vx_block = np.tile(vx, (n, 1)) * scale * in_vision
        vy_block = np.tile(vy, (n, 1)) * scale * in_vision
        
        dvx = np.sum(vx_block, axis=1)
        dvy = np.sum(vy_block, axis=1)
        
        dv = np.stack((dvx, dvy), axis=1) * np.sqrt(n_in_vision).reshape(-1, 1) * input_data.match_factor * fudge_factor
        
        return dv
    
    def _force_cohesion(self, positions: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Calculate cohesion force"""
        in_vision = self._can_see(positions, input_data.vision_range)
        
        x = positions[:, 0]
        y = positions[:, 1]
        n = len(x)
        fudge_factor = 0.0166
        
        if n <= 1:
            return np.zeros((n, 2))
        
        x_block = np.tile(x, (n, 1)) * in_vision
        y_block = np.tile(y, (n, 1)) * in_vision
        np.fill_diagonal(x_block, 0)
        np.fill_diagonal(y_block, 0)
        
        x_ave = np.sum(x_block, axis=1) / np.maximum(1, n - 1)
        y_ave = np.sum(y_block, axis=1) / np.maximum(1, n - 1)
        
        dx = np.log(1 + np.abs(x_ave - x)) * np.sign(x_ave - x)
        dy = np.log(1 + np.abs(y_ave - y)) * np.sign(y_ave - y)
        
        dv = np.stack((dx, dy), axis=1) * input_data.centering_factor * fudge_factor
        
        return dv
    
    def _mind_edges(self, positions: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Calculate edge avoidance force"""
        fudge_factor = 1
        x = positions[:, 0]
        y = positions[:, 1]
        
        right = input_data.world_width - input_data.margin
        left = -right
        top = input_data.world_height - input_data.margin
        bot = -top
        
        n = len(x)
        dx = np.zeros(n)
        dy = np.zeros(n)
        
        dx[x < left] = left - x[x < left]
        dx[x > right] = right - x[x > right]
        dy[y < bot] = bot - y[y < bot]
        dy[y > top] = top - y[y > top]
        
        dv = np.stack((dx, dy), axis=1) * n * input_data.turn_factor * fudge_factor
        
        return dv
    
    def _limit_speed(self, velocities: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Limit bird speeds to min/max range"""
        speeds = np.linalg.norm(velocities, axis=1)
        directions = np.zeros(velocities.shape)
        
        mask = speeds != 0
        directions[mask] = velocities[mask] / speeds[mask, np.newaxis]
        
        speeds = np.clip(speeds, input_data.min_speed, input_data.max_speed)
        
        return directions * speeds[:, np.newaxis]
    
    def _update_velocities(self, positions: np.ndarray, velocities: np.ndarray, input_data: BoidsSimulationInput) -> np.ndarray:
        """Update velocities using all boids forces"""
        
        # Calculate all forces
        avoid_force = self._force_avoid(positions, input_data)
        align_force = self._force_align(positions, velocities, input_data)
        cohesion_force = self._force_cohesion(positions, input_data)
        edge_force = self._mind_edges(positions, input_data)
        
        # Apply forces
        new_velocities = velocities + avoid_force + align_force + cohesion_force + edge_force
        
        # Limit speeds
        new_velocities = self._limit_speed(new_velocities, input_data)
        
        return new_velocities
    
    def _create_boids_figure(self, df: pd.DataFrame, input_data: BoidsSimulationInput) -> go.Figure:
        """Create the boids animated figure"""
        
        fig = px.scatter(
            df,
            x='x',
            y='y',
            color='color_value',
            animation_frame='frame',
            animation_group='bird_id',
            title=input_data.title,
            color_continuous_scale=input_data.color_scheme,
            range_x=[-input_data.world_width, input_data.world_width],
            range_y=[-input_data.world_height, input_data.world_height]
        )
        
        # Update marker properties
        fig.update_traces(
            marker=dict(
                size=input_data.marker_size,
                symbol='arrow-up',  # Use arrow symbols for birds
                line=dict(width=1, color='white')
            )
        )
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": input_data.frame_duration, "redraw": True},
                            "transition": {"duration": 30}
                        }]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                "steps": [
                    {
                        "args": [[f], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        "label": str(f),
                        "method": "animate"
                    }
                    for f in range(input_data.num_frames)
                ],
                "active": 0,
                "transition": {"duration": 0},
                "x": 0.1,
                "len": 0.9
            }]
        )
        
        # Remove colorbar and add description
        fig.update_layout(
            coloraxis_showscale=False,
            annotations=[
                dict(
                    text=f"Boids Algorithm: {input_data.num_birds} birds following flocking rules<br>" +
                         f"Avoid: {input_data.avoid_factor}, Align: {input_data.match_factor}, " +
                         f"Center: {input_data.centering_factor}, Vision: {input_data.vision_range}",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="gray",
                    borderwidth=1,
                    font=dict(size=10)
                )
            ]
        )
        
        return fig


# Export the tools
# Tools are instantiated by create_all_tools() function, not here 