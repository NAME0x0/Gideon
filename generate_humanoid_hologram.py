import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

# Golden ratio constant (approximately 1.618)
phi = 1.618

def modify_face(x, y, z):
    # Define feature centers based on standard female facial proportions
    left_eye_center  = np.array([-0.25,  0.35,  0.1])
    right_eye_center = np.array([ 0.25,  0.35,  0.1])
    nose_center      = np.array([ 0.0,   0.0,   0.2])
    mouth_center     = np.array([ 0.0,  -0.3,   0.0])
    
    z_mod = 0.0
    point = np.array([x, y, z])
    
    # Compute distances from each feature center
    d_left  = np.linalg.norm(point - left_eye_center)
    d_right = np.linalg.norm(point - right_eye_center)
    d_nose  = np.linalg.norm(point - nose_center)
    d_mouth = np.linalg.norm(point - mouth_center)
    
    # Enhance facial features with stronger, more localized modifications:
    z_mod -= 0.3 * np.exp(-d_left**2 / 0.01)
    z_mod -= 0.3 * np.exp(-d_right**2 / 0.01)
    z_mod += 0.4 * np.exp(-d_nose**2 / 0.02)
    z_mod -= 0.4 * np.exp(-d_mouth**2 / 0.02)
    
    return z_mod

def create_parametric_face(u, v):
    # Base ellipsoid for head shape with anatomical proportions inspired by the golden ratio.
    a = 0.8   # horizontal (width) radius
    b = 0.8   # depth radius
    c = 1.3   # vertical (height) radius
    
    # Parametric equations for an ellipsoid using spherical coordinates:
    x = a * np.cos(u) * np.cos(v)
    y = b * np.sin(u) * np.cos(v)
    z0 = c * np.sin(v)
    
    # Apply localized deformations to create distinct facial features
    z = np.empty_like(z0)
    rows, cols = z0.shape
    for i in range(rows):
        for j in range(cols):
            z[i, j] = z0[i, j] + modify_face(x[i, j], y[i, j], z0[i, j])
    
    return x, y, z

# Set up figure and 3D axes with a dark background for a holographic effect
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Limit the parametric range to only the front side of the ellipsoid
u = np.linspace(-np.pi/2, np.pi/2, 120)
v = np.linspace(-np.pi/2, np.pi/2, 120)
U, V = np.meshgrid(u, v)
X, Y, Z = create_parametric_face(U, V)

# Set up shading using a colormap based on Z values
norm = plt.Normalize(Z.min(), Z.max())
facecolors = plt.cm.coolwarm(norm(Z))

# Plot the initial surface
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                       linewidth=0, antialiased=True)

# Set initial view parameters and axis limits
ax.view_init(elev=10, azim=0)
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])

def update(frame):
    # Update view angle for a subtle rotation within the front view range
    ax.collections.clear()  # Remove the previous surface
    ax.view_init(elev=10, azim=frame)
    facecolors = plt.cm.coolwarm(norm(Z))
    surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                           linewidth=0, antialiased=True)
    ax.set_box_aspect([1, 1, 1])
    return surf,

try:
    # Rotate between -30° and 30° to maintain focus on the front side of the face
    anim = animation.FuncAnimation(fig, update, frames=np.linspace(-30, 30, 60), interval=50, blit=False)
    output_file = 'hologram_humanoid.gif'
    anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor': 'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
