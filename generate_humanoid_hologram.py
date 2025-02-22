import pywavefront
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import numpy as np

# Load the realistic 3D face mesh from the FBX file
# Note: If you experience issues, ensure that you have installed any additional dependencies
# (such as pyassimp) to support FBX format.
scene = pywavefront.Wavefront('gideon_face.fbx')

# Create a figure and a 3D axes instance
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')

# Extract vertices and faces from the mesh
vertices = mesh.vertices
faces = mesh.faces

# Create a 3D polygon collection from the mesh faces
face_collection = Poly3DCollection(vertices[faces], alpha=0.7)
face_collection.set_edgecolor('none')
face_collection.set_facecolor('cyan')  # Holographic color palette
ax.add_collection3d(face_collection)

# Set axis limits based on the mesh bounds for proper scaling
x_bounds, y_bounds, z_bounds = mesh.bounds.T
ax.set_xlim(x_bounds.min(), x_bounds.max())
ax.set_ylim(y_bounds.min(), y_bounds.max())
ax.set_zlim(z_bounds.min(), z_bounds.max())

# Define the rotation function to update the view angle
def update(angle):
    ax.view_init(elev=30, azim=angle)
    return fig,

# Create an animation rotating the view a full 360 degrees
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)

# Save the animation as a GIF (ensure ImageMagick is installed on the runner)
ani.save('hologram_humanoid.gif', writer='imagemagick', fps=30)
