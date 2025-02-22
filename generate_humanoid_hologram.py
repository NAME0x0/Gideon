import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import os
import mpl_toolkits.mplot3d.art3d as art3d

def custom_do_3d_projection(self):
    try:
        retval = self._original_do_3d_projection()
    except Exception as e:
        print(f"Error during projection: {e}")
        try:
            facecolors = self.get_facecolor()
        except Exception:
            facecolors = None
        try:
            edgecolors = self.get_edgecolor()
        except Exception:
            edgecolors = None
        return ([], [], facecolors, edgecolors, None)
    # Ensure retval has 5 elements by padding missing values
    if isinstance(retval, tuple) and len(retval) < 5:
        ret0 = retval[0] if len(retval) >= 1 else []
        ret1 = retval[1] if len(retval) >= 2 else []
        try:
            facecolors2d = self._facecolors2d
        except AttributeError:
            facecolors2d = self.get_facecolor() if hasattr(self, 'get_facecolor') else None
        try:
            edgecolors2d = self._edgecolors2d
        except AttributeError:
            edgecolors2d = self.get_edgecolor() if hasattr(self, 'get_edgecolor') else None
        idxs = None
        retval = (ret0, ret1, facecolors2d, edgecolors2d, idxs)
    return retval

# Override the original method
art3d.Poly3DCollection._original_do_3d_projection = art3d.Poly3DCollection.do_3d_projection
art3d.Poly3DCollection.do_3d_projection = custom_do_3d_projection

def create_female_face_mesh():
    # Create a simple elliptical face outline
    t = np.linspace(0, 2*np.pi, 20, endpoint=False)
    a = 1.0   # horizontal radius
    b = 1.3   # vertical radius for a slightly elongated face
    outer = np.column_stack((a * np.cos(t), b * np.sin(t), np.zeros_like(t)))
    center = np.array([[0, 0, 0]])  # center vertex
    vertices = np.vstack((center, outer))
    # Triangulate using a fan from the center
    faces = []
    n = len(vertices)
    for i in range(1, n-1):
        faces.append([0, i, i+1])
    faces.append([0, n-1, 1])
    vertices = vertices.astype(np.float32)
    faces = np.array(faces, dtype=np.int32)
    # Add slight depth variation for 3D effect
    vertices[:,2] = 0.1 + 0.05 * np.sin(np.linspace(0, 2*np.pi, n))
    return vertices, faces

# Use our own generated female face mesh instead of loading an .obj file
vertices, faces = create_female_face_mesh()

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
    # Create and save animation
    anim = animation.FuncAnimation(
        fig, update, frames=180, interval=50, blit=True
    )
    
    output_file = 'hologram_humanoid.gif'
    anim.save(
        output_file,
        writer='pillow',
        fps=30,
        savefig_kwargs={'facecolor': 'black'}
    )
    
    # Verify file was created
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
        
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
