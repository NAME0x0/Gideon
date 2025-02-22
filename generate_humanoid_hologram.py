import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_math_face_mesh():
    # Create a mesh grid over a square domain
    x = np.linspace(-1.5, 1.5, 40)
    y = np.linspace(-1.5, 1.5, 40)
    X, Y = np.meshgrid(x, y)
    # Base dome for the face
    Z = 0.2 * np.exp(-((X)**2 + (Y)**2) / 1.0)
    # Eyes: depressions (left and right)
    for (dx, dy) in [(-0.5, 0.3), (0.5, 0.3)]:
        Z -= 0.1 * np.exp(-(((X - dx)**2 + (Y - dy)**2) / 0.1))
    # Mouth: depression at lower center
    Z -= 0.07 * np.exp(-((X)**2 + (Y + 0.5)**2) / 0.1)
    
    # Flatten grid into vertices
    vertices = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))
    nrows, ncols = X.shape
    faces = []
    # Create faces (two triangles per grid cell)
    for i in range(nrows - 1):
        for j in range(ncols - 1):
            idx = i * ncols + j
            faces.append([idx, idx + 1, idx + ncols])
            faces.append([idx + 1, idx + ncols + 1, idx + ncols])
    return vertices, np.array(faces, dtype=np.int32)

# Generate the mathematical face mesh
vertices, faces = create_math_face_mesh()

# Normalize vertices to center and scale to [-1, 1]
vertices = vertices - np.mean(vertices, axis=0)
max_range = np.max(np.abs(vertices))
vertices = vertices / max_range

# Create figure and 3D axes
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')
ax.set_facecolor('black')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

# Create a Poly3DCollection for the mesh
# (Start with a placeholder using the first face)
collection = Poly3DCollection(vertices[faces[0:1]], animated=True,
                              edgecolor='cyan', facecolor='none', alpha=0.3)
ax.add_collection3d(collection)

def update(frame):
    # Rotate the mesh about the z-axis
    theta = np.radians(frame)
    rotation = np.array([[np.cos(theta), -np.sin(theta), 0],
                         [np.sin(theta),  np.cos(theta), 0],
                         [0,              0,             1]])
    rotated = vertices @ rotation
    collection.set_verts([rotated[face] for face in faces])
    # Add a flickering effect by varying alpha
    collection.set_alpha(0.3 + 0.1 * np.sin(frame * 0.1))
    return collection,

try:
    anim = animation.FuncAnimation(fig, update, frames=180, interval=50, blit=True)
    output_file = 'hologram_humanoid.gif'
    anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor': 'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
