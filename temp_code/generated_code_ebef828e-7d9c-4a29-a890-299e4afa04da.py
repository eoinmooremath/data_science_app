import numpy as np
import pandas as pd
from tools.data_tools import uploaded_datasets

np.random.seed(42)

num_points = 50
num_frames = 100

# Initialize starting positions
positions = np.random.rand(num_points, 2) * 10

# Generate random directions
directions = np.random.rand(num_points, 2) * 2 - 1
directions /= np.linalg.norm(directions, axis=1)[:, np.newaxis]

# Create empty list to store data
data = []

for frame in range(num_frames):
    for point_id in range(num_points):
        x, y = positions[point_id]
        data.append({
            'frame': frame,
            'point_id': point_id,
            'x': x,
            'y': y
        })
    
    # Update positions
    positions += directions * 0.1
    
    # Bounce off edges
    out_of_bounds = (positions < 0) | (positions > 10)
    directions[out_of_bounds] *= -1
    positions = np.clip(positions, 0, 10)

# Create DataFrame
df = pd.DataFrame(data)

# Save to uploaded_datasets
uploaded_datasets['animated_points'] = df