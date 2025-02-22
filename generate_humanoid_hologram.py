import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import pywavefront
import os

def create_default_face_mesh():
    # Create a simpler pyramid as fallback
    vertices = np.array([
        [0, 0, 2],  # top
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]  # base
    ])
    faces = np.array([
        [0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1],  # sides
        [1, 2, 3, 4]  # base
    ])
    return vertices, faces

try:
    if os.path.exists('gideon_face.obj'):
        scene = pywavefront.Wavefront('gideon_face.obj', collect_faces=True)
        vertices = np.array(scene.vertices)
        faces = []
        for mesh in scene.mesh_list:
            faces.extend([list(face) for face in mesh.faces])
        faces = np.array(faces)
    else:
        vertices, faces = create_default_face_mesh()
except Exception as e:
    print(f"Error loading mesh file: {e}")
    vertices, faces = create_default_face_mesh()

# Normalize vertices to [-1, 1] range
vertices = vertices - np.mean(vertices, axis=0)
max_range = np.max(np.abs(vertices))
vertices = vertices / max_range

# Create figure
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Create the collection with a single triangle first
verts = vertices[faces[0:1]]
collection = Poly3DCollection(verts, animated=True)
collection.set_edgecolor('cyan')
collection.set_facecolor('none')
collection.set_alpha(0.3)
ax.add_collection3d(collection)

# Set the plot limits
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

def update(frame):
    # Rotate vertices
    theta = np.radians(frame)
    c, s = np.cos(theta), np.sin(theta)
    rotation = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
    
    rotated_verts = vertices @ rotation
    collection.set_verts([rotated_verts[face] for face in faces])
    
    # Flickering effect
    alpha = 0.3 + 0.1 * np.sin(frame * 0.1)
    collection.set_alpha(alpha)
    return collection,

try:
    # Create and save animation with error handling
    anim = animation.FuncAnimation(
        fig, update, frames=180, interval=50, blit=True
    )
    
    # Save with multiple attempts if needed
    for attempt in range(3):
        try:
            anim.save(
                'hologram_humanoid.gif',
                writer='pillow',
                fps=30,
                savefig_kwargs={'facecolor': 'black'}
            )
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                raise
finally:
    plt.close()
