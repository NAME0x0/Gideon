import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

# This approach draws inspiration from layered morphable models and particle–based evolution,
# as described in advanced research papers on facial modeling.
# We construct a 3D face by stacking horizontal 2D slices defined in polar coordinates.

# Number of vertical layers and angular resolution per layer
num_layers = 40       # More layers yield finer vertical detail.
num_points = 150      # Angular resolution for each layer.

# Vertical coordinate: z ranges from chin (-1) to forehead (1)
z_layers = np.linspace(-1, 1, num_layers)
theta = np.linspace(0, 2*np.pi, num_points)
Theta, Z = np.meshgrid(theta, z_layers)

# Base radius function (inspired by golden ratio proportions):
# We assume the maximum width is at mid-face (z = 0) and taper off smoothly.
A_max = 0.9   # maximum half–width at mid–face.
A_min = 0.5   # minimum half–width at chin/forehead.
base_radius = A_max - (A_max - A_min) * (np.abs(Z))**2

# Define a function to modify the radius for each layer based on both theta and z.
def feature_modulation(theta, z):
    mod = 0.0
    # Eyes: create depressions at about z ~ 0.4.
    # We place the eyes symmetrically around the horizontal axis.
    # Left eye: centered near theta ~ 2.2 rad, right eye: near theta ~ 4.1 rad.
    mod += -0.15 * np.exp(-((theta - 2.2)**2)/0.05 - ((z - 0.4)**2)/0.02)
    mod += -0.15 * np.exp(-((theta - 4.1)**2)/0.05 - ((z - 0.4)**2)/0.02)
    
    # Nose: a central protrusion at z ~ 0.0, affecting a broad angular region.
    mod += 0.12 * np.exp(-((theta - np.pi)**2)/0.3 - ((z - 0.0)**2)/0.03)
    
    # Mouth: a depression at about z ~ -0.3, centered around theta ~ np.pi.
    mod += -0.18 * np.exp(-((theta - np.pi)**2)/0.3 - ((z + 0.3)**2)/0.03)
    
    # Cheeks: subtle bumps near z ~ 0.0 for added contour,
    # one on each side (approximately at theta ~ 1.0 and theta ~ 5.3).
    mod += 0.08 * np.exp(-((theta - 1.0)**2)/0.1 - ((z - 0.0)**2)/0.02)
    mod += 0.08 * np.exp(-((theta - 5.3)**2)/0.1 - ((z - 0.0)**2)/0.02)
    
    # Forehead: a gentle bump at z ~ 0.8 over most angles.
    mod += 0.06 * np.exp(-((z - 0.8)**2)/0.04)
    
    # Chin: a slight depression at z ~ -0.9.
    mod += -0.05 * np.exp(-((z + 0.9)**2)/0.04)
    
    return mod

# Compute the total radial distance for each (z, theta)
R = base_radius + feature_modulation(Theta, Z)

# Convert from polar to Cartesian coordinates
X = R * np.cos(Theta)
Y = R * np.sin(Theta)
# Z remains the same from the layering

# Set up the figure and 3D axes with a dark, holographic background
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Create a colormap based on the z coordinate (or the computed R) to simulate depth and shading.
norm = plt.Normalize(Z.min(), Z.max())
facecolors = plt.cm.coolwarm(norm(Z))

# Plot the 3D surface using the stacked layers
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, rstride=1, cstride=1,
                       linewidth=0, antialiased=True)

# Set initial view parameters and axis limits for a balanced frontal presentation
ax.view_init(elev=25, azim=0)
ax.set_box_aspect([1,1,1])
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

def update(frame):
    # For the animation, apply a gentle rotation while preserving the frontal view.
    ax.collections.clear()
    ax.view_init(elev=25, azim=frame)
    facecolors = plt.cm.coolwarm(norm(Z))
    ax.plot_surface(X, Y, Z, facecolors=facecolors, rstride=1, cstride=1,
                    linewidth=0, antialiased=True)
    return ax,

try:
    # Animate a subtle rotation from -30° to 30° azimuth.
    anim = animation.FuncAnimation(fig, update, frames=np.linspace(-30, 30, 60),
                                   interval=50, blit=False)
    output_file = 'female_face_layers.gif'
    anim.save(output_file, writer='pillow', fps=30, savefig_kwargs={'facecolor': 'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print("Error during animation generation:", e)
    raise
finally:
    plt.close()
