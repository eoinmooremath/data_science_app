import pandas as pd
import matplotlib.pyplot as plt
from tools.data_tools import uploaded_datasets

# Retrieve the data from uploaded_datasets
df = uploaded_datasets['job_1234']

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df.iloc[:, 0], df.iloc[:, 1], color='green')

# Set the title
plt.title('Scatter Plot of 1000 Generated Data Points (Green)')

# Set labels for x and y axes
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Display the plot
plt.grid(True)
plt.tight_layout()
plt.show()