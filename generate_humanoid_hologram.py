import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

# Golden ratio constant (approximately 1.618)
phi = 1.618

def modify_face(x, y, z):
    """
    Apply local deformations using a list of control points.
    Each control point is defined as:
      (x_center, y_center, z_center, strength, width)
    A positive strength creates a bump; a negative strength creates a depression.
    """
    control_points = [
        # Eye region (left eye: multiple points for smooth depression)
        (-0.25,  0.35,  0.1,  -0.3, 0.005),
        (-0.20,  0.35,  0.1,  -0.3, 0.005),
        # Eye region (right eye)
        ( 0.25,  0.35,  0.1,  -0.3, 0.005),
        ( 0.20,  0.35,  0.1,  -0.3, 0.005),
        # Nose region (bump)
        ( 0.0,   0.0,   0.2,   0.4, 0.01),
        ( 0.0,   0.05,  0.2,   0.4, 0.01),
        # Mouth region (depression)
        ( 0.0,  -0.3,   0.0,  -0.4, 0.01),
        (-0.1,  -0.3,   0.0,  -0.4, 0.01),
        ( 0.1,  -0.3,   0.0,  -0.4, 0.01),
        # Cheekbones (subtle bump to accentuate facial structure)
        (-0.5,   0.1,   0.1,   0.2, 0.02),
        ( 0.5,   0.1,   0.1,   0.2, 0.02),
        # Chin region (depression)
        ( 0.0,  -0.5,  -0.2,  -0.3, 0.015),
        # Forehead (bump)
        ( 0.0,   0.5,   0.3,   0.2, 0.015)
    ]
    
    z_mod = 0.0
    point = np.array([x, y, z])
    for cp in control_points:
        cp_point = np.array([cp[0], cp[1], cp[2]])
        strength = cp[3]
        width = cp[4]
        d = np.linalg.norm(point - cp_point)
        # Gaussian contribution for this control point
        z_mod += strength * np.exp(-d**2 / width)
    return z_mod

def create_parametric_face(u, v):
    """
    Create a parametric face surface based on a deformed ellipsoid.
    The base ellipsoid has dimensions defined by:
       a (width), b (depth), c (height)
    """
    a = 0.8   # horizontal (width) radius
    b = 0.8   # depth radius
    c = 1.3   # vertical (height) radius

    # Parametric equations for an ellipsoid using spherical coordinates:
    x = a * np.cos(u) * np.cos(v)
    y = b * np.sin(u) * np.cos(v)
    z0 = c * np.sin(v)
    
    # Apply local deformations to create detailed facial features
    z = np.empty_like(z0)
    rows, cols = z0.shape
    for i in range(rows):
        for j in range(cols):
            z[i, j] = z0[i, j] + modify_face(x[i, j], y[i, j], z0[i, j])
    return x, y, z

# Set up the figure and 3D axes with a dark background for a holographic look
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Limit the parametric range to only the front of the ellipsoid
# u in [-π/2, π/2] ensures we only generate the frontal half.
u = np.linspace(-np.pi/2, np.pi/2, 200)
v = np.linspace(-np.pi/2, np.pi/2, 200)
U, V = np.meshgrid(u, v)
X, Y, Z = create_parametric_face(U, V)

# Set up a colormap based on the Z values to simulate lighting and depth
norm = plt.Normalize(Z.min(), Z.max())
facecolors = plt.cm.coolwarm(norm(Z))

# Plot the initial surface
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                       linewidth=0, antialiased=True)

# Set initial view parameters and axis limits for a balanced, frontal view
ax.view_init(elev=10, azim=0)
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])

def update(frame):
    # Update the view angle for a slight rotation while keeping the face frontal
    ax.collections.clear()  # Remove the previous surface
    ax.view_init(elev=10, azim=frame)
    facecolors = plt.cm.coolwarm(norm(Z))
    surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                           linewidth=0, antialiased=True)
    ax.set_box_aspect([1, 1, 1])
    return surf,

try:
    # Restrict rotation to a narrow range (from -30° to 30°) to maintain a frontal perspective
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
