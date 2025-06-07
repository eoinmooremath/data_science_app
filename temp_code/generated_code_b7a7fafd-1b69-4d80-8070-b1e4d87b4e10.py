import pandas as pd
import matplotlib.pyplot as plt
from tools.data_tools import uploaded_datasets

# Retrieve the data from uploaded_datasets
df = uploaded_datasets['job_1']

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['x'], df['y'], alpha=0.5)

# Set title and labels
plt.title('Scatter Plot of 1000 Generated Data Points')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()