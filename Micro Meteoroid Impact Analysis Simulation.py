import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class MicroMeteoroid:
    def __init__(self, position, velocity, size):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.size = size
        self.impacted = False

class Shield:
    def __init__(self, size, thickness):
        self.size = size
        self.thickness = thickness
        self.damage = np.zeros(size)
        self.deformation = np.zeros(size)

class OrbitalDefenseSystem:
    def __init__(self, shield, micro_meteoroids, max_speed):
        self.shield = shield
        self.micro_meteoroids = micro_meteoroids
        self.max_speed = max_speed

class OrbitalDefenseSystemDispimport numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class MicroMeteoroid:
    def __init__(self, position, velocity, size):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.size = size
        self.impacted = False

class Shield:
    def __init__(self, size, thickness):
        self.size = size
        self.thickness = thickness
        self.damage = np.zeros(size)
        self.deformation = np.zeros(size)

class MicroMeteoroidImpactSimulation:
    def __init__(self, shield, micro_meteoroids, max_speed):
        self.shield = shield
        self.micro_meteoroids = micro_meteoroids
        self.max_speed = max_speed

class MicroMeteoroidImpactVisualization:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def update(self, frame):
        self.ax.clear()
        self.ax.set_xlim(0, self.simulation.shield.size[0])
        self.ax.set_ylim(0, self.simulation.shield.size[1])
        self.ax.set_zlim(0, self.simulation.shield.thickness)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Damage')
        
        for micro_meteoroid in self.simulation.micro_meteoroids:
            if micro_meteoroid.position[2] < self.simulation.shield.thickness and not micro_meteoroid.impacted:
                micro_meteoroid.position += micro_meteoroid.velocity
                micro_meteoroid.position[2] += 0.01  # Move micro meteoroid along z-axis (simulating impact depth)
                if (0 <= micro_meteoroid.position[0] < self.simulation.shield.size[0] and 
                    0 <= micro_meteoroid.position[1] < self.simulation.shield.size[1]):
                    impact_x = int(micro_meteoroid.position[0])
                    impact_y = int(micro_meteoroid.position[1])
                    self.simulation.shield.damage[impact_x, impact_y] += 0.01  # Simulate damage to shield
                    
                    # Simulate deflection or splattering of micro meteoroid upon impact
                    if self.simulation.shield.damage[impact_x, impact_y] >= micro_meteoroid.size:
                        micro_meteoroid.impacted = True
                        micro_meteoroid.position[2] = self.simulation.shield.thickness
                        self.simulation.shield.deformation[impact_x, impact_y] += micro_meteoroid.size
                        micro_meteoroid.velocity = np.random.normal(scale=0.01, size=3)  # Randomize micro meteoroid velocity after impact
                        # Create splatter micro meteoroids
                        for _ in range(np.random.randint(1, 5)):
                            splatter_size = max(0.01, np.random.normal(micro_meteoroid.size/2, 0.01))
                            splatter_velocity = np.random.normal(scale=0.05, size=3)
                            splatter_micro_meteoroid = MicroMeteoroid(position=micro_meteoroid.position, velocity=splatter_velocity, size=splatter_size)
                            self.simulation.micro_meteoroids.append(splatter_micro_meteoroid)
               
        self.ax.scatter([micro_meteoroid.position[0] for micro_meteoroid in self.simulation.micro_meteoroids],
                        [micro_meteoroid.position[1] for micro_meteoroid in self.simulation.micro_meteoroids],
                        [micro_meteoroid.position[2] for micro_meteoroid in self.simulation.micro_meteoroids],
                        s=[micro_meteoroid.size*100 for micro_meteoroid in self.simulation.micro_meteoroids], c='r', marker='o')  # Show micro meteoroids
        self.ax.plot_surface(*np.meshgrid(np.arange(self.simulation.shield.size[0]), np.arange(self.simulation.shield.size[1])), 
                             self.simulation.shield.damage, cmap='viridis', alpha=0.5)  # Show shield damage
        self.ax.plot_surface(*np.meshgrid(np.arange(self.simulation.shield.size[0]), np.arange(self.simulation.shield.size[1])), 
                             self.simulation.shield.deformation, cmap='coolwarm', alpha=0.5)  # Show shield deformation

def main_menu():
    print("Welcome to Micro Meteoroid Impact Analysis Simulation")
    print("----------------------------------------------------------")
    print("1. Start Simulation")
    print("2. Customize Simulation Parameters")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice

def customize_parameters():
    shield_width = int(input("Enter shield width [10]: ") or "10")
    shield_height = int(input("Enter shield height [10]: ") or "10")
    shield_thickness = float(input("Enter shield thickness [1]: ") or "1")
    num_micro_meteoroids = int(input("Enter number of micro meteoroids [1000]: ") or "1000")
    max_speed = float(input("Enter maximum micro meteoroid speed [0.1]: ") or "0.1")
    micro_meteoroid_size_mean = float(input("Enter mean micro meteoroid size [0.05]: ") or "0.05")
    micro_meteoroid_size_std = float(input("Enter micro meteoroid size standard deviation [0.02]: ") or "0.02")
    micro_meteoroid_velocity_mean = float(input("Enter mean micro meteoroid velocity [0.05]: ") or "0.05")
    micro_meteoroid_velocity_std = float(input("Enter micro meteoroid velocity standard deviation [0.02]: ") or "0.02")
    return shield_width, shield_height, shield_thickness, num_micro_meteoroids, max_speed, micro_meteoroid_size_mean, micro_meteoroid_size_std, micro_meteoroid_velocity_mean, micro_meteoroid_velocity_std

def initialize_simulation(shield_width=10, shield_height=10, shield_thickness=1, num_micro_meteoroids=1000, max_speed=0.1,
                          micro_meteoroid_size_mean=0.05, micro_meteoroid_size_std=0.02, micro_meteoroid_velocity_mean=0.05, micro_meteoroid_velocity_std=0.02):
    shield = Shield(size=(shield_width, shield_height), thickness=shield_thickness)
    micro_meteoroids = [MicroMeteoroid(position=np.random.rand(3) * shield.size[0], 
                          velocity=np.random.normal(micro_meteoroid_velocity_mean, micro_meteoroid_velocity_std, size=3), 
                          size=max(0.01, np.random.normal(micro_meteoroid_size_mean, micro_meteoroid_size_std))) for _ in range(num_micro_meteoroids)]
    simulation = MicroMeteoroidImpactSimulation(shield, micro_meteoroids, max_speed)
    return simulation

def start_simulation(simulation):
    visualization = MicroMeteoroidImpactVisualization(simulation)
    ani = animation.FuncAnimation(visualization.fig, visualization.update, frames=100, interval=50)
    plt.show()

if __name__ == "__main__":
    shield_width, shield_height, shield_thickness, num_micro_meteoroids, max_speed = 10, 10, 1, 1000, 0.1
    micro_meteoroid_size_mean, micro_meteoroid_size_std, micro_meteoroid_velocity_mean, micro_meteoroid_velocity_std = 0.05, 0.02, 0.05, 0.02

    while True:
        choice = main_menu()
        if choice == "1":
            simulation = initialize_simulation(shield_width, shield_height, shield_thickness, num_micro_meteoroids, max_speed,
                                                micro_meteoroid_size_mean, micro_meteoroid_size_std, micro_meteoroid_velocity_mean, micro_meteoroid_velocity_std)
            start_simulation(simulation)
        elif choice == "2":
            shield_width, shield_height, shield_thickness, num_micro_meteoroids, max_speed, \
            micro_meteoroid_size_mean, micro_meteoroid_size_std, micro_meteoroid_velocity_mean, micro_meteoroid_velocity_std = customize_parameters()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
