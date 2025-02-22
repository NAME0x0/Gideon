import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

def create_parametric_face(u, v):
    # Base ellipsoid for head shape
    x = 1.5 * np.cos(u) * np.cos(v)
    y = np.sin(u) * np.cos(v)
    z = 0.8 * np.sin(v)
    
    # Add facial features through mathematical deformations
    # Nose bridge and tip
    nose = 0.2 * np.exp(-((x)**2 + (y-0.5)**2) / 0.05) * (z > -0.2) * (z < 0.2)
    
    # Eye sockets
    left_eye = -0.1 * np.exp(-((x+0.4)**2 + (y-0.1)**2) / 0.02) * (z > -0.1) * (z < 0.1)
    right_eye = -0.1 * np.exp(-((x-0.4)**2 + (y-0.1)**2) / 0.02) * (z > -0.1) * (z < 0.1)
    
    # Mouth curve
    mouth = -0.1 * np.exp(-((x)**2 + (y+0.3)**2) / 0.04) * (z > -0.1) * (z < 0.1)
    
    # Combine all features
    z = z + nose + left_eye + right_eye + mouth
    
    return x, y, z

# Create figure and 3D axes
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Generate the parametric surface
u = np.linspace(-np.pi, np.pi, 100)
v = np.linspace(-np.pi/2, np.pi/2, 100)
U, V = np.meshgrid(u, v)
X, Y, Z = create_parametric_face(U, V)

# Initial surface plot
surf = ax.plot_surface(X, Y, Z, color='cyan', alpha=0.3, 
                      linewidth=0.5, antialiased=True)

# Set viewing angle and limits
ax.view_init(elev=0, azim=0)
ax.set_box_aspect([1, 1, 1])

def update(frame):
    # Clear previous frame
    ax.collections.clear()
    
    # Rotate the view
    ax.view_init(elev=20, azim=frame)
    
    # Update surface with flickering effect
    alpha = 0.3 + 0.1 * np.sin(frame * 0.1)
    surf = ax.plot_surface(X, Y, Z, color='cyan', alpha=alpha,
                          linewidth=0.5, antialiased=True)
    
    # Ensure proper aspect ratio
    ax.set_box_aspect([1, 1, 1])
    return surf,

try:
    # Create and save animation
    anim = animation.FuncAnimation(
        fig, update, frames=180, interval=50, blit=False
    )
    
    output_file = 'hologram_humanoid.gif'
    anim.save(
        output_file,
        writer='pillow',
        fps=30,
        savefig_kwargs={'facecolor': 'black'}
    )
    
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
        
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
