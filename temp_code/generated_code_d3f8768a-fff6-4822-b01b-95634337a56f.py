import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
        self.velocity = self.limit_speed(self.velocity)
        self.position += self.velocity
        
        self.position[0] %= 100
        self.position[1] %= 100

    def separate(self, boids):
        separation = np.zeros(2)
        for other in boids:
            if other != self:
                diff = self.position - other.position
                if np.linalg.norm(diff) < 2:
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
        center /= (len(boids) - 1)
        return center - self.position

    def limit_speed(self, velocity):
        speed = np.linalg.norm(velocity)
        if speed > 2:
            velocity = (velocity / speed) * 2
        return velocity

num_boids = 30
boids = [Boid(np.random.rand() * 100, np.random.rand() * 100, 
               np.random.randn(), np.random.randn()) for _ in range(num_boids)]

fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
scatter = ax.scatter([b.position[0] for b in boids], [b.position[1] for b in boids])

def update(frame):
    for boid in boids:
        boid.update(boids)
    scatter.set_offsets([b.position for b in boids])
    return scatter,

anim = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.close(fig)

# Save animation data to uploaded_datasets
positions = np.array([[b.position for b in boids] for _ in range(200)])
velocities = np.array([[b.velocity for b in boids] for _ in range(200)])

df_positions = pd.DataFrame(positions.reshape(-1, num_boids * 2))
df_velocities = pd.DataFrame(velocities.reshape(-1, num_boids * 2))

uploaded_datasets['boids_positions'] = df_positions
uploaded_datasets['boids_velocities'] = df_velocities