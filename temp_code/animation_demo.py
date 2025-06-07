"""
Animation Demo Script

This script demonstrates the new animation capabilities in the Data Science UI,
inspired by the boids simulation example.
"""

import numpy as np
import pandas as pd
from tools.data_tools import uploaded_datasets

# Set random seed for reproducible results
np.random.seed(42)

print("Creating animation demo datasets...")

# 1. Create a simple time series animation dataset
print("Creating time series animation data...")
time_steps = 100
num_series = 5

time_data = []
for t in range(time_steps):
    for series_id in range(num_series):
        # Create different wave patterns for each series
        frequency = (series_id + 1) * 0.1
        phase = series_id * np.pi / 4
        amplitude = (series_id + 1) * 2
        
        value = amplitude * np.sin(frequency * t + phase) + np.random.normal(0, 0.1)
        
        time_data.append({
            'time': t,
            'series_id': series_id,
            'value': value,
            'series_name': f'Series_{series_id + 1}'
        })

time_series_df = pd.DataFrame(time_data)
uploaded_datasets['time_series_animation'] = time_series_df
print(f"Created time_series_animation dataset: {time_series_df.shape}")

# 2. Create a racing bar chart dataset
print("Creating racing bar chart data...")
categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
months = 24

racing_data = []
# Initialize starting values
values = {cat: np.random.uniform(10, 50) for cat in categories}

for month in range(months):
    for cat in categories:
        # Simulate growth with some randomness
        growth_rate = np.random.uniform(0.95, 1.15)
        values[cat] *= growth_rate
        
        # Add some seasonal variation
        seasonal = 1 + 0.2 * np.sin(2 * np.pi * month / 12)
        values[cat] *= seasonal
        
        racing_data.append({
            'month': month,
            'category': cat,
            'value': values[cat],
            'year': 2022 + month // 12,
            'quarter': f"Q{(month % 12) // 3 + 1}"
        })

racing_df = pd.DataFrame(racing_data)
uploaded_datasets['racing_bars'] = racing_df
print(f"Created racing_bars dataset: {racing_df.shape}")

# 3. Create a particle system dataset
print("Creating particle system data...")
num_particles = 30
num_frames = 150

particle_data = []
# Initialize particles with random positions and velocities
particles = []
for i in range(num_particles):
    particles.append({
        'x': np.random.uniform(-5, 5),
        'y': np.random.uniform(-5, 5),
        'vx': np.random.uniform(-0.2, 0.2),
        'vy': np.random.uniform(-0.2, 0.2),
        'mass': np.random.uniform(0.5, 2.0)
    })

for frame in range(num_frames):
    for i, particle in enumerate(particles):
        # Record current state
        particle_data.append({
            'frame': frame,
            'particle_id': i,
            'x': particle['x'],
            'y': particle['y'],
            'vx': particle['vx'],
            'vy': particle['vy'],
            'mass': particle['mass'],
            'size': particle['mass'] * 5,  # Size proportional to mass
            'energy': 0.5 * particle['mass'] * (particle['vx']**2 + particle['vy']**2)
        })
        
        # Update position
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        
        # Apply gravity toward center
        center_force = 0.001
        distance = np.sqrt(particle['x']**2 + particle['y']**2)
        if distance > 0:
            particle['vx'] -= center_force * particle['x'] / distance
            particle['vy'] -= center_force * particle['y'] / distance
        
        # Bounce off walls
        if abs(particle['x']) > 8:
            particle['vx'] *= -0.8
            particle['x'] = np.sign(particle['x']) * 8
        if abs(particle['y']) > 8:
            particle['vy'] *= -0.8
            particle['y'] = np.sign(particle['y']) * 8

particle_df = pd.DataFrame(particle_data)
uploaded_datasets['particle_system'] = particle_df
print(f"Created particle_system dataset: {particle_df.shape}")

# 4. Create a population growth dataset
print("Creating population growth data...")
countries = ['Country A', 'Country B', 'Country C', 'Country D']
years = list(range(1990, 2021))

population_data = []
# Initialize starting populations
populations = {country: np.random.uniform(10, 100) for country in countries}

for year in years:
    for country in countries:
        # Different growth patterns for each country
        if country == 'Country A':
            growth_rate = 1.02  # Steady growth
        elif country == 'Country B':
            growth_rate = 1.03 if year < 2010 else 1.01  # Slowing growth
        elif country == 'Country C':
            growth_rate = 1.01 + 0.01 * np.sin((year - 1990) * 0.3)  # Cyclical
        else:
            growth_rate = 1.015  # Moderate growth
        
        populations[country] *= growth_rate
        
        population_data.append({
            'year': year,
            'country': country,
            'population': populations[country],
            'decade': f"{(year // 10) * 10}s"
        })

population_df = pd.DataFrame(population_data)
uploaded_datasets['population_growth'] = population_df
print(f"Created population_growth dataset: {population_df.shape}")

print("\nAnimation Demo Datasets Created!")
print("\nAvailable datasets for animation:")
for name, df in uploaded_datasets.items():
    if 'animation' in name or name in ['racing_bars', 'particle_system', 'population_growth']:
        print(f"  - {name}: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"    Columns: {list(df.columns)}")

print("\nExample Animation Commands:")
print("\n1. Time Series Animation:")
print("   Create an animated line plot showing how multiple time series evolve")
print("   Dataset: time_series_animation")
print("   Frame column: time")
print("   X: time, Y: value, Color: series_name")

print("\n2. Racing Bar Chart:")
print("   Create an animated bar chart showing category values over time")
print("   Dataset: racing_bars") 
print("   Frame column: month")
print("   X: category, Y: value")

print("\n3. Particle System:")
print("   Create an animated scatter plot of particles moving in space")
print("   Dataset: particle_system")
print("   Frame column: frame")
print("   X: x, Y: y, Size: size, Color: energy")

print("\n4. Population Growth:")
print("   Create an animated visualization of population changes")
print("   Dataset: population_growth")
print("   Frame column: year")
print("   X: country, Y: population")

print("\n5. Boids Simulation:")
print("   Create a flocking simulation with realistic bird behavior")
print("   Use the BoidsSimulationTool with customizable parameters")

print("\nTry asking Claude to create these animations!")
print("Example: 'Create an animated scatter plot of the particle system data'")
print("Example: 'Generate a boids simulation with 30 birds'")
print("Example: 'Make a racing bar chart animation from the racing_bars data'") 