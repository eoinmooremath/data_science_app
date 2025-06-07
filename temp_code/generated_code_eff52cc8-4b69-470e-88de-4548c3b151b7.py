import pandas as pd
import numpy as np
from tools.data_tools import uploaded_datasets

# List of US states and their abbreviations
states = [
    ('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'), ('California', 'CA'),
    ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'), ('Florida', 'FL'), ('Georgia', 'GA'),
    ('Hawaii', 'HI'), ('Idaho', 'ID'), ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'),
    ('Kansas', 'KS'), ('Kentucky', 'KY'), ('Louisiana', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'),
    ('Massachusetts', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Mississippi', 'MS'), ('Missouri', 'MO'),
    ('Montana', 'MT'), ('Nebraska', 'NE'), ('Nevada', 'NV'), ('New Hampshire', 'NH'), ('New Jersey', 'NJ'),
    ('New Mexico', 'NM'), ('New York', 'NY'), ('North Carolina', 'NC'), ('North Dakota', 'ND'), ('Ohio', 'OH'),
    ('Oklahoma', 'OK'), ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'),
    ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), ('Vermont', 'VT'),
    ('Virginia', 'VA'), ('Washington', 'WA'), ('West Virginia', 'WV'), ('Wisconsin', 'WI'), ('Wyoming', 'WY')
]

# Create DataFrame
df = pd.DataFrame(states, columns=['State', 'Abbreviation'])

# Add random metric values
df['Metric'] = np.random.randint(0, 101, size=len(df))

# Save DataFrame to uploaded_datasets
uploaded_datasets['us_state_data'] = df