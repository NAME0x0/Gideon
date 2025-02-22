import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

def create_parametric_face(u, v):
    # Base ellipsoid for head shape (flattened and elongated)
    x = np.cos(u)*np.cos(v)
    y = 0.8*np.sin(u)*np.cos(v)
    z = 0.7*np.sin(v)
    
    # Nose: a small bump in the center upper region
    mask_nose = np.exp(-(((x)**2 + (y-0.1)**2)/0.02))
    z = z + 0.15 * mask_nose
    
    # Eyes: depressions on left and right
    mask_eye_left = np.exp(-(((x+0.4)**2 + (y-0.25)**2)/0.01))
    mask_eye_right = np.exp(-(((x-0.4)**2 + (y-0.25)**2)/0.01))
    z = z - 0.12 * (mask_eye_left + mask_eye_right)
    
    # Mouth: a depression lower down
    mask_mouth = np.exp(-((x)**2 + (y+0.3)**2)/0.02)
    z = z - 0.15 * mask_mouth
    
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

# Initial surface plot with desired styling
surf = ax.plot_surface(X, Y, Z, color='cyan', alpha=0.35, 
                         linewidth=0.5, antialiased=True)

# Set viewing angle and aspect ratio
ax.view_init(elev=0, azim=0)
ax.set_box_aspect([1,1,1])

def update(frame):
    # Clear previous collections to update the surface properly
    ax.collections.clear()
    ax.view_init(elev=20, azim=frame)
    
    # Apply a slight flickering effect on alpha
    alpha = 0.35 + 0.1 * np.sin(frame * 0.1)
    surf = ax.plot_surface(X, Y, Z, color='cyan', alpha=alpha, 
                           linewidth=0.5, antialiased=True)
    ax.set_box_aspect([1,1,1])
    return surf,

try:
    anim = animation.FuncAnimation(fig, update, frames=180, interval=50, blit=False)
    output_file = 'hologram_humanoid.gif'
    anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor':'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
