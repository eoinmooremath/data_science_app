import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tools.data_tools import uploaded_datasets

class Boid:
    def __init__(self, x, y, vx, vy):
        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])

class BoidSimulation:
    def __init__(self, num_boids, width, height, max_speed, perception_radius, separation_factor, alignment_factor, cohesion_factor):
        self.boids = [Boid(np.random.uniform(0, width), np.random.uniform(0, height),
                           np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for _ in range(num_boids)]
        self.width = width
        self.height = height
        self.max_speed = max_speed
        self.perception_radius = perception_radius
        self.separation_factor = separation_factor
        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor

    def update(self):
        for boid in self.boids:
            neighbors = self.get_neighbors(boid)
            
            separation = self.separation(boid, neighbors)
            alignment = self.alignment(boid, neighbors)
            cohesion = self.cohesion(boid, neighbors)
            
            boid.velocity += separation * self.separation_factor + \
                             alignment * self.alignment_factor + \
                             cohesion * self.cohesion_factor
            
            speed = np.linalg.norm(boid.velocity)
            if speed > self.max_speed:
                boid.velocity = (boid.velocity / speed) * self.max_speed
            
            boid.position += boid.velocity
            
            boid.position[0] = boid.position[0] % self.width
            boid.position[1] = boid.position[1] % self.height

    def get_neighbors(self, boid):
        return [b for b in self.boids if b != boid and np.linalg.norm(b.position - boid.position) < self.perception_radius]

    def separation(self, boid, neighbors):
        if not neighbors:
            return np.zeros(2)
        separation = np.zeros(2)
        for neighbor in neighbors:
            diff = boid.position - neighbor.position
            separation += diff / (np.linalg.norm(diff) ** 2)
        return separation

    def alignment(self, boid, neighbors):
        if not neighbors:
            return np.zeros(2)
        avg_velocity = np.mean([neighbor.velocity for neighbor in neighbors], axis=0)
        return avg_velocity - boid.velocity

    def cohesion(self, boid, neighbors):
        if not neighbors:
            return np.zeros(2)
        center_of_mass = np.mean([neighbor.position for neighbor in neighbors], axis=0)
        return center_of_mass - boid.position

# Set up the simulation
num_boids = 50
width, height = 800, 600
max_speed = 4
perception_radius = 100
separation_factor = 0.05
alignment_factor = 0.05
cohesion_factor = 0.005

simulation = BoidSimulation(num_boids, width, height, max_speed, perception_radius,
                            separation_factor, alignment_factor, cohesion_factor)

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 7.5))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
scatter = ax.scatter([boid.position[0] for boid in simulation.boids],
                     [boid.position[1] for boid in simulation.boids])

def update(frame):
    simulation.update()
    scatter.set_offsets([boid.position for boid in simulation.boids])
    return scatter,

# Create the animation
anim = FuncAnimation(fig, update, frames=200, interval=50, blit=True)

# Save the animation data
positions = np.array([[boid.position for boid in simulation.boids] for _ in range(200)])
velocities = np.array([[boid.velocity for boid in simulation.boids] for _ in range(200)])

uploaded_datasets['boid_positions'] = pd.DataFrame(positions.reshape(-1, num_boids * 2))
uploaded_datasets['boid_velocities'] = pd.DataFrame(velocities.reshape(-1, num_boids * 2))

plt.close(fig)