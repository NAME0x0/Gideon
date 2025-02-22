import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import pywavefront
import os

def create_default_face_mesh():
    # Create a simple cube as fallback
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ])
    faces = np.array([
        [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
        [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
    ])
    return vertices, faces

try:
    if os.path.exists('gideon_face.obj'):  # Changed to .obj format
        scene = pywavefront.Wavefront('gideon_face.obj', collect_faces=True)
        vertices = np.array(scene.vertices)
        faces = np.array([face for mesh in scene.mesh_list for face in mesh.faces])
    else:
        vertices, faces = create_default_face_mesh()
except Exception as e:
    print(f"Error loading mesh file: {e}")
    vertices, faces = create_default_face_mesh()

# Create figure with black background
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Create mesh collection
face_collection = Poly3DCollection(vertices[faces])
face_collection.set_edgecolor('cyan')
face_collection.set_facecolor('none')
face_collection.set_alpha(0.3)
ax.add_collection3d(face_collection)

# Center the plot
max_range = np.array([vertices[:,0].max()-vertices[:,0].min(),
                      vertices[:,1].max()-vertices[:,1].min(),
                      vertices[:,2].max()-vertices[:,2].min()]).max() / 2.0

mid_x = (vertices[:,0].max()+vertices[:,0].min()) * 0.5
mid_y = (vertices[:,1].max()+vertices[:,1].min()) * 0.5
mid_z = (vertices[:,2].max()+vertices[:,2].min()) * 0.5

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

def update(frame):
    ax.view_init(elev=20, azim=frame)
    # Add flickering effect
    alpha = 0.3 + 0.1 * np.sin(frame * 0.1)
    face_collection.set_alpha(alpha)
    return fig,

# Create animation
anim = animation.FuncAnimation(fig, update, frames=180, interval=50)

# Save with higher quality
anim.save('hologram_humanoid.gif', writer='pillow', fps=30)
plt.close()
