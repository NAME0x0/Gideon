import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

# Golden ratio constant (approximately 1.618)
phi = 1.618

def modify_face(x, y, z):
    # Define feature centers based on facial proportions (relative to the face center)
    left_eye_center  = np.array([-0.3,  0.3,  0.0])
    right_eye_center = np.array([ 0.3,  0.3,  0.0])
    nose_center      = np.array([ 0.0,  0.0,  0.4])
    mouth_center     = np.array([ 0.0, -0.4, -0.1])
    
    # Initialize modification for z-coordinate
    z_mod = 0.0
    point = np.array([x, y, z])
    
    # Create depressions for the eyes
    d_left = np.linalg.norm(point - left_eye_center)
    d_right = np.linalg.norm(point - right_eye_center)
    z_mod -= 0.12 * np.exp(-d_left**2 / 0.02)
    z_mod -= 0.12 * np.exp(-d_right**2 / 0.02)
    
    # Create a bump for the nose
    d_nose = np.linalg.norm(point - nose_center)
    z_mod += 0.15 * np.exp(-d_nose**2 / 0.03)
    
    # Create a depression for the mouth
    d_mouth = np.linalg.norm(point - mouth_center)
    z_mod -= 0.15 * np.exp(-d_mouth**2 / 0.03)
    
    return z_mod

def create_parametric_face(u, v):
    # Base ellipsoid for head shape with anatomical proportions.
    # a and b define the horizontal dimensions and c defines the vertical dimension.
    # Here, the vertical dimension is chosen so that height/width is roughly phi (~1.618),
    # but slightly adjusted for a more natural female face shape.
    a = 0.8   # horizontal radius (width)
    b = 0.8   # depth radius
    c = 1.3   # vertical radius (height), yielding a ratio ~1.625
    
    # Parametric equations for an ellipsoid:
    x = a * np.cos(u) * np.cos(v)
    y = b * np.sin(u) * np.cos(v)
    z0 = c * np.sin(v)  # base vertical coordinate
    
    # Apply local deformations for facial features
    z = np.empty_like(z0)
    rows, cols = z0.shape
    for i in range(rows):
        for j in range(cols):
            z[i, j] = z0[i, j] + modify_face(x[i, j], y[i, j], z0[i, j])
    
    return x, y, z

# Set up figure and 3D axes with a dark background for a holographic feel
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Generate the parametric surface for the face
u = np.linspace(-np.pi, np.pi, 120)
v = np.linspace(-np.pi/2, np.pi/2, 120)
U, V = np.meshgrid(u, v)
X, Y, Z = create_parametric_face(U, V)

# Normalize Z for colormap shading and simulate lighting
norm = plt.Normalize(Z.min(), Z.max())
facecolors = plt.cm.coolwarm(norm(Z))

# Plot the initial surface
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                       linewidth=0, antialiased=True)

# Set initial view parameters and axis limits
ax.view_init(elev=10, azim=0)
ax.set_box_aspect([1,1,1])
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])

def update(frame):
    # Update view angle for rotation and replot the surface
    ax.collections.clear()  # Remove the previous surface
    ax.view_init(elev=10, azim=frame)
    # Reapply the same colormap; dynamic shading adjustments can be added here if desired
    facecolors = plt.cm.coolwarm(norm(Z))
    surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, shade=False,
                           linewidth=0, antialiased=True)
    ax.set_box_aspect([1,1,1])
    return surf,

try:
    # Create an animation rotating the face and save it as a GIF
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
