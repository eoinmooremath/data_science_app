import numpy as np
import matplotlib.pyplot as plt
from tools.data_tools import uploaded_datasets

class Boid:
    def __init__(self, x, y, vx, vy):
        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])

    def update(self, boids):
        separation = self.separate(boids)
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        
        self.velocity += separation * 0.05 + alignment * 0.05 + cohesion * 0.05
        self.velocity = self.velocity / np.linalg.norm(self.velocity) * 2
        self.position += self.velocity

    def separate(self, boids):
        separation = np.zeros(2)
        for other in boids:
            if other != self:
                diff = self.position - other.position
                if np.linalg.norm(diff) < 20:
                    separation += diff
        return separation

    def align(self, boids):
        alignment = np.zeros(2)
        for other in boids:
            if other != self:
                alignment += other.velocity
        return alignment / (len(boids) - 1) - self.velocity

    def cohere(self, boids):
        center = np.zeros(2)
        for other in boids:
            if other != self:
                center += other.position
        center = center / (len(boids) - 1)
        return (center - self.position) * 0.01

def create_boids(num_boids):
    return [Boid(np.random.uniform(0, 100), np.random.uniform(0, 100),
                 np.random.uniform(-1, 1), np.random.uniform(-1, 1))
            for _ in range(num_boids)]

num_boids = 30
iterations = 100

boids = create_boids(num_boids)

for _ in range(iterations):
    for boid in boids:
        boid.update(boids)

positions = np.array([boid.position for boid in boids])

plt.figure(figsize=(10, 10))
plt.scatter(positions[:, 0], positions[:, 1])
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title(f"Boids Simulation - {num_boids} birds after {iterations} iterations")
plt.savefig('boids_simulation.png')
plt.close()

final_positions = pd.DataFrame(positions, columns=['x', 'y'])
uploaded_datasets['boids_final_positions'] = final_positions