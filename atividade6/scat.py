import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.animation as animation

def rastrigin(*X, **kwargs):
    A = kwargs.get('A', 10)
    return A * len(X) + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X])

def read_data_from_file(filename):
    """
    Read data from a file and return as a numpy array.
    The file format should be: iteration;x;y;z
    """
    data = np.loadtxt(filename, delimiter=';', skiprows=0)
    return data

def update_scatter(num, data, scatter, points):
    # Update the scatter plot with new data
    current_data = data[data[:, 0] == num]
    new_x = current_data[:, 1]
    new_y = current_data[:, 2]
    new_z = current_data[:, 3]

    scatter._offsets3d = (new_x, new_y, new_z)
    
    # Update the stored points positions for drawing the movement path
    for i, pt in enumerate(points):
        if i < len(new_x):
            pt.set_data_3d([pt.get_data_3d()[0][-1], new_x[i]],
                           [pt.get_data_3d()[1][-1], new_y[i]],
                           [pt.get_data_3d()[2][-1], new_z[i]])

    return scatter, points

def create_animation(data, save_path=None):
    # Find unique iterations and the number of points
    unique_iterations = np.unique(data[:, 0])
    num_points = len(data[data[:, 0] == unique_iterations[0]])

    # Generate mesh grid for the Rastrigin function
    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)
    Z = rastrigin(X, Y, A=10)

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Plot the Rastrigin surface
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='YlGn', linewidth=0.08,
                    antialiased=True, alpha=0.2)

    # Initial scatter plot with first iteration data
    initial_data = data[data[:, 0] == unique_iterations[0]]
    scatter = ax.scatter(initial_data[:, 1], initial_data[:, 2], initial_data[:, 3], c='b', marker='o')

    # Create a list of line objects to trace the path of each point
    points = [ax.plot([x], [y], [z], color='m', linestyle='--', marker='.')[0] 
              for x, y, z in zip(initial_data[:, 1], initial_data[:, 2], initial_data[:, 3])]

    # Setting the Axes properties
    ax.set(xlim3d=(-5.12, 5.12), ylim3d=(-5.12, 5.12), zlim3d=(0, np.max(Z)))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Creating the Animation object
    ani = animation.FuncAnimation(
        fig, update_scatter, frames=unique_iterations, fargs=(data, scatter, points), interval=200, blit=False)

    

    if save_path:
        # Save the animation as a gif
        ani.save(save_path, writer='pillow', fps=30)
    else:
        plt.show()

# Read data from file
filename = 'testes/teste_grafico.txt'
data = read_data_from_file(filename)

# Create and show animation
create_animation(data, save_path='rastrigin_animation.gif')
