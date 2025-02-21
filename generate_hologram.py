import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Set up the figure and 3D axes
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Generate an ellipsoidal surface to represent the face
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 30)
x = 1.2 * np.outer(np.cos(u), np.sin(v))
y = 1.0 * np.outer(np.sin(u), np.sin(v))
z = 1.3 * np.outer(np.ones(np.size(u)), np.cos(v))

# Render the surface with a translucent, cool-toned colormap for a holographic feel
face = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=plt.cm.cool(0.6),
                       linewidth=0, antialiased=False, alpha=0.7)

# Add simple markers for eyes (two small spheres)
def add_eye(center):
    phi = np.linspace(0, 2*np.pi, 20)
    theta = np.linspace(0, np.pi, 20)
    r = 0.1
    eye_x = center[0] + r * np.outer(np.cos(phi), np.sin(theta))
    eye_y = center[1] + r * np.outer(np.sin(phi), np.sin(theta))
    eye_z = center[2] + r * np.outer(np.ones(np.size(phi)), np.cos(theta))
    ax.plot_surface(eye_x, eye_y, eye_z, color='cyan', alpha=0.9, linewidth=0)
    
# Coordinates chosen relative to the ellipsoid for the eyes
add_eye([0.5, 0.4, 0.5])
add_eye([-0.5, 0.4, 0.5])

# Optionally, add a simple line to indicate a mouth
mouth_x = np.linspace(-0.4, 0.4, 100)
mouth_y = 0.0 * mouth_x
mouth_z = -0.5 + 0.1 * np.sin(3 * np.pi * mouth_x)
ax.plot(mouth_x, mouth_y, mouth_z, color='cyan', linewidth=2)

# Function to update the view angle for rotation
def rotate(angle):
    ax.view_init(elev=30, azim=angle)
    return fig,

# Create an animation that rotates the view 360 degrees
ani = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, 2), interval=50)

# Save the animation as a GIF (ensure that ImageMagick is installed on the runner)
ani.save('hologram.gif', writer='imagemagick', fps=30)
