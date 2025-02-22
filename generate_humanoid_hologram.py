import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

# Golden ratio constant (used for anatomical proportions)
phi = 1.618

def modify_face(x, y, z):
    # Define feature centers based on face dimensions and phi.
    # These positions were tuned so that (0,0,0) is the center.
    left_eye_center = np.array([-0.35,  0.25, 0.0])
    right_eye_center = np.array([ 0.35,  0.25, 0.0])
    nose_center = np.array([0.0, 0.05, 0.35])
    mouth_center = np.array([0.0, -0.30, -0.15])
    
    # For each point, compute modifications (using Gaussian modulations)
    point = np.array([x, y, z])
    z_mod = 0.0
    # Eyes depressions
    d_left = np.linalg.norm(point - left_eye_center)
    d_right = np.linalg.norm(point - right_eye_center)
    z_mod -= 0.1 * np.exp(-d_left**2 / 0.015)
    z_mod -= 0.1 * np.exp(-d_right**2 / 0.015)
    # Nose bump
    d_nose = np.linalg.norm(point - nose_center)
    z_mod += 0.08 * np.exp(-d_nose**2 / 0.02)
    # Mouth depression
    d_mouth = np.linalg.norm(point - mouth_center)
    z_mod -= 0.12 * np.exp(-d_mouth**2 / 0.02)
    return z_mod

def create_parametric_face(u, v):
    # Base ellipsoid for head shape (anatomical proportions inspired by phi)
    # Radii chosen so width and height relate roughly via the golden ratio.
    a = 1.0       # horizontal radius
    b = 1.0       # depth radius
    c = phi/phi   # vertical radius; here set to 1.0, but we will deform it
    # Standard ellipsoid using spherical coordinates:
    # u: azimuth in [-pi,pi], v: elevation in [-pi/2, pi/2]
    x = a * np.cos(u) * np.cos(v)
    y = b * np.sin(u) * np.cos(v)
    z0 = 1.0 * np.sin(v)  # base vertical shape
    
    # Apply local deformations to z using feature modifiers
    # Create a new Z that adds per-point modifications
    z = np.empty_like(z0)
    for i in range(z0.shape[0]):
        for j in range(z0.shape[1]):
            z[i, j] = z0[i, j] + modify_face(x[i, j], y[i, j], z0[i, j])
    
    return x, y, z

# Create figure and 3D axes with good lighting
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Generate the parametric surface
u = np.linspace(-np.pi, np.pi, 120)
v = np.linspace(-np.pi/2, np.pi/2, 120)
U, V = np.meshgrid(u, v)
X, Y, Z = create_parametric_face(U, V)

# Use a colormap to simulate shading (simulate a light from above)
# The intensity will be based on z-value differences.
norm = plt.Normalize(Z.min(), Z.max())
facecolors = plt.cm.coolwarm(norm(Z))

# Initial surface plot with lighting effect
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                         linewidth=0, antialiased=True)

ax.view_init(elev=10, azim=0)
ax.set_box_aspect([1,1,1])
ax.set_xlim([-1.5,1.5])
ax.set_ylim([-1.5,1.5])
ax.set_zlim([-1.5,1.5])

def update(frame):
    # Update view angle for rotation and recompute shading effect
    ax.collections.clear()  # remove old surface
    ax.view_init(elev=10, azim=frame)
    # Update facecolors based on current Z; (here it remains constant, but you could add flicker)
    facecolors = plt.cm.coolwarm(norm(Z))
    surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                           linewidth=0, antialiased=True)
    ax.set_box_aspect([1,1,1])
    return surf,

try:
    anim = animation.FuncAnimation(fig, update, frames=180, interval=50, blit=False)
    output_file = 'hologram_humanoid.gif'
    anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor': 'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print(f"Error during animation generation: {e}")
    raise
finally:
    plt.close()
