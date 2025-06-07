import pandas as pd
import plotly.express as px
from tools.data_tools import uploaded_datasets

# Retrieve the data from uploaded_datasets
df = uploaded_datasets['job_cc23b35e']

# Create the scatter plot
fig = px.scatter(df, x=df.columns[0], y=df.columns[1], 
                 title='Red Scatter Plot of Generated Data',
                 labels={'x': 'X-axis', 'y': 'Y-axis'},
                 color_discrete_sequence=['red'])

# Update layout for axis labels
fig.update_layout(
    xaxis_title='X-axis',
    yaxis_title='Y-axis'
)

# Show the plot
fig.show()