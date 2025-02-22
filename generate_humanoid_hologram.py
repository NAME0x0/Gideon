import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import os

# Load the STL file (ensure face.stl is in the repository root)
mesh = trimesh.load('face.stl')

# Extract vertices and faces from the mesh
vertices = mesh.vertices
faces = mesh.faces

# Create a new figure with a black background for the holographic effect
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')
ax.set_box_aspect([1, 1, 1])

# Build a list of face vertices for the Poly3DCollection
poly3d = [vertices[face] for face in faces]

# Create the 3D polygon collection with a translucent, cyan-like color
face_collection = Poly3DCollection(poly3d, alpha=0.7)
face_collection.set_edgecolor('none')
face_collection.set_facecolor('cyan')
ax.add_collection3d(face_collection)

# Set axis limits based on the mesh's bounding box
x_min, y_min, z_min = mesh.bounds[0]
x_max, y_max, z_max = mesh.bounds[1]
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)

# Function to update the view angle for the animation
def update(angle):
    ax.view_init(elev=30, azim=angle)
    return ax,

# Create the animation (rotating a full 360 degrees)
anim = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, blit=False)

# Save the animation as a GIF using Pillow
output_file = 'hologram_face.gif'
anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor': 'black'})

if not os.path.exists(output_file):
    raise FileNotFoundError(f"Failed to create {output_file}")

plt.close()
