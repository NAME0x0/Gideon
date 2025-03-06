import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation, colors, cm
import os
from matplotlib.colors import LinearSegmentedColormap

# Load the STL file (ensure face.stl is in the repository root)
mesh = trimesh.load('face.stl')

# Extract vertices and faces from the mesh
vertices = mesh.vertices
faces = mesh.faces

# Create a vibrant red to blue colormap for the holographic effect
colors_red_blue = [(0.8, 0.1, 0.1), (0.6, 0.2, 0.4), (0.4, 0.4, 0.6), (0.2, 0.3, 0.8)]
cmap_name = 'RedBlueHologram'
cm_red_blue = LinearSegmentedColormap.from_list(cmap_name, colors_red_blue, N=100)

# Create a new figure with a black background for the holographic effect
fig = plt.figure(figsize=(12, 12), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')
ax.set_box_aspect([1, 1, 1])

# Get mesh bounds for normalization and particle generation
x_min, y_min, z_min = mesh.bounds[0]
x_max, y_max, z_max = mesh.bounds[1]
center = [(x_min + x_max)/2, (y_min + y_max)/2, (z_min + z_max)/2]
max_radius = max(x_max - x_min, y_max - y_min, z_max - z_min) / 2

# Generate particle system
def generate_particles(num_particles=1000):
    # Generate random particles near the mesh surface
    # Sample random points from the mesh surface
    surface_points, _ = trimesh.sample.sample_surface(mesh, num_particles // 2)
    
    # Generate additional random particles in a shell around the mesh
    theta = np.random.uniform(0, 2*np.pi, num_particles // 2)
    phi = np.random.uniform(0, np.pi, num_particles // 2)
    r = np.random.uniform(0.9 * max_radius, 1.1 * max_radius, num_particles // 2)
    
    shell_x = center[0] + r * np.sin(phi) * np.cos(theta)
    shell_y = center[1] + r * np.sin(phi) * np.sin(theta)
    shell_z = center[2] + r * np.cos(phi)
    
    shell_points = np.column_stack((shell_x, shell_y, shell_z))
    
    # Combine surface and shell particles
    particles = np.vstack((surface_points, shell_points))
    
    # Generate random sizes for particles
    sizes = np.random.uniform(5, 25, num_particles)
    
    # Generate colors based on height (z-coordinate)
    z_normalized = (particles[:, 2] - z_min) / (z_max - z_min)
    colors = cm_red_blue(z_normalized)
    
    return particles, sizes, colors

# Generate particles
particles, particle_sizes, particle_colors = generate_particles(3000)

# Initialize scatter plot for particles
particle_scatter = ax.scatter(
    particles[:, 0], particles[:, 1], particles[:, 2],
    s=particle_sizes, c=particle_colors, alpha=0.6, edgecolors='none'
)

# Build a list of face vertices for the Poly3DCollection
poly3d = [vertices[face] for face in faces]

# Calculate face centers for color mapping
face_centers = np.array([vertices[face].mean(axis=0) for face in faces])
z_normalized = (face_centers[:, 2] - z_min) / (z_max - z_min)
face_colors = cm_red_blue(z_normalized)

# Create the 3D polygon collection with translucent gradient colors
face_collection = Poly3DCollection(poly3d, alpha=0.4)
face_collection.set_edgecolor('none')
face_collection.set_facecolors(face_colors)
ax.add_collection3d(face_collection)

# Set axis limits based on the mesh's bounding box with some padding
padding = max_radius * 0.1
ax.set_xlim(x_min - padding, x_max + padding)
ax.set_ylim(y_min - padding, y_max + padding)
ax.set_zlim(z_min - padding, z_max + padding)

# Variable to track particle velocities
particle_velocities = np.random.uniform(-0.005, 0.005, (len(particles), 3))

# Function to update the view angle and particles for the animation
def update(frame):
    # Update rotation angle
    angle = frame % 360
    ax.view_init(elev=15 + 5 * np.sin(np.radians(frame)), azim=angle)
    
    # Update particles positions with slight movement
    global particles, particle_velocities
    
    # Apply velocities to particles
    particles += particle_velocities
    
    # Add some random perturbation to velocities
    particle_velocities += np.random.uniform(-0.001, 0.001, (len(particles), 3))
    
    # Dampen velocities to prevent particles from flying away too quickly
    particle_velocities *= 0.98
    
    # Bounce particles back if they go too far from the center
    distances = np.sqrt(np.sum((particles - center)**2, axis=1))
    too_far = distances > 1.3 * max_radius
    
    # Particles moving too far are attracted back to the center
    if np.any(too_far):
        directions = particles[too_far] - np.array(center)
        normalized_dirs = directions / np.linalg.norm(directions, axis=1)[:, np.newaxis]
        particle_velocities[too_far] -= normalized_dirs * 0.01
    
    # Update the scatter plot with new positions
    particle_scatter._offsets3d = (particles[:, 0], particles[:, 1], particles[:, 2])
    
    # Apply pulsating sizes for particles based on frame
    new_sizes = particle_sizes * (0.8 + 0.2 * np.sin(np.radians(frame * 2) + np.random.rand(len(particles))))
    particle_scatter.set_sizes(new_sizes)
    
    # Update colors based on new z positions
    z_normalized = (particles[:, 2] - z_min) / (z_max - z_min)
    new_colors = cm_red_blue(z_normalized)
    particle_scatter.set_color(new_colors)
    
    # Pulsating transparency effect for the mesh
    face_collection.set_alpha(0.3 + 0.1 * np.sin(np.radians(frame * 2)))
    
    return ax, particle_scatter, face_collection

# Create the animation (rotating a full 360 degrees)
frames = 180  # Reduced to 180 frames for a more manageable file size
anim = animation.FuncAnimation(
    fig, update, frames=np.arange(frames), 
    interval=50, blit=False
)

# Save the animation as a high-quality GIF
output_file = 'hologram_face.gif'
anim.save(
    output_file, 
    writer='pillow', 
    fps=30, 
    savefig_kwargs={'facecolor': 'black', 'dpi': 100}
)

print(f"Animation saved to {output_file}")

if not os.path.exists(output_file):
    raise FileNotFoundError(f"Failed to create {output_file}")

plt.close()
