import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
import pywavefront
import os
import mpl_toolkits.mplot3d.art3d as art3d

def custom_do_3d_projection(self):
    try:
        retval = self._original_do_3d_projection()
    except Exception as e:
        print(f"Error during projection: {e}")
        return ([], [], None, None, None)
    if isinstance(retval, tuple) and len(retval) < 5:
        # Pad the tuple with None to reach 5 elements
        retval = retval + (None,) * (5 - len(retval))
    return retval

# Override the original method
art3d.Poly3DCollection._original_do_3d_projection = art3d.Poly3DCollection.do_3d_projection
art3d.Poly3DCollection.do_3d_projection = custom_do_3d_projection

def create_default_face_mesh():
    # Create a triangulated pyramid as fallback
    vertices = np.array([
        [0, 0, 2],    # top
        [-1, -1, 0],  # base points
        [1, -1, 0],
        [1, 1, 0],
        [-1, 1, 0]
    ])
    # All faces as triangles
    faces = np.array([
        [0, 1, 2],  # side triangles
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1],
        [1, 2, 3],  # base triangles
        [1, 3, 4]
    ], dtype=np.int32)
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
