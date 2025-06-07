import numpy as np
import matplotlib.pyplot as plt
from tools.data_tools import uploaded_datasets
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)

# Generate random positions for 50 boids
num_boids = 50
positions = np.random.rand(num_boids, 2)
positions[:, 0] *= 800  # Scale x-coordinates to 800
positions[:, 1] *= 600  # Scale y-coordinates to 600

# Plot the boids
ax.scatter(positions[:, 0], positions[:, 1], c='blue', s=20)

# Set labels and title
ax.set_xlabel('X position')
ax.set_ylabel('Y position')
ax.set_title('Initial Positions of 50 Boids')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Create a DataFrame with the boid positions
df = pd.DataFrame(positions, columns=['x', 'y'])

# Save the DataFrame to the uploaded_datasets dictionary
uploaded_datasets['boids_initial_positions'] = df

# Close the plot to free up memory
plt.close(fig)