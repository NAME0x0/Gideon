import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

def gaussian(x, y, x0, y0, amplitude, sigma):
    """
    Returns a Gaussian function value for the point (x,y).
    amplitude: height (positive) or depth (negative) of the feature.
    sigma: controls the spread; smaller values yield sharper features.
    """
    return amplitude * np.exp(-(((x - x0)**2 + (y - y0)**2) / sigma))

# Define the face grid dimensions
x = np.linspace(-0.8, 0.8, 300)
y = np.linspace(-1.3, 1.3, 400)
X, Y = np.meshgrid(x, y)

# Define an elliptical mask to represent the face outline (golden ratio based)
mask = (X / 0.8)**2 + (Y / 1.3)**2 <= 1

# Start with a flat base surface
Z = np.zeros_like(X)

# Add detailed facial features using multiple Gaussian functions
# Forehead bump (upper third)
Z += gaussian(X, Y, 0.0, 0.8, 0.15, 0.05)
# Eyes depressions: positioned symmetrically above the midline
Z += gaussian(X, Y, -0.3, 0.4, -0.2, 0.02)
Z += gaussian(X, Y,  0.3, 0.4, -0.2, 0.02)
# Nose bump in the central region
Z += gaussian(X, Y, 0.0, 0.1, 0.25, 0.03)
# Mouth depression (lower third)
Z += gaussian(X, Y, 0.0, -0.3, -0.3, 0.05)
# Chin depression for a defined jawline
Z += gaussian(X, Y, 0.0, -0.8, -0.15, 0.05)
# Cheek bumps to enhance facial contour
Z += gaussian(X, Y, -0.5, 0.0, 0.1, 0.08)
Z += gaussian(X, Y,  0.5, 0.0, 0.1, 0.08)

# Set values outside the face mask to NaN so they are not plotted
Z[~mask] = np.nan

# Set up the figure and 3D axes with a dark (holographic) background
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# Use a colormap based on the Z values to simulate shading and depth
norm = plt.Normalize(np.nanmin(Z), np.nanmax(Z))
facecolors = plt.cm.coolwarm(norm(Z))

# Plot the surface
surf = ax.plot_surface(X, Y, Z, facecolors=facecolors, rstride=1, cstride=1,
                       linewidth=0, antialiased=True)

# Set initial view parameters and axis limits for a balanced, frontal view
ax.view_init(elev=20, azim=0)
ax.set_box_aspect([1, 1, 1])
ax.set_xlim([-0.8, 0.8])
ax.set_ylim([-1.3, 1.3])
ax.set_zlim([np.nanmin(Z) - 0.1, np.nanmax(Z) + 0.1])

def update(frame):
    # Clear the previous surface and update the view for a subtle rotation
    ax.collections.clear()
    ax.view_init(elev=20, azim=frame)
    facecolors = plt.cm.coolwarm(norm(Z))
    ax.plot_surface(X, Y, Z, facecolors=facecolors, rstride=1, cstride=1,
                    linewidth=0, antialiased=True)
    return ax,

try:
    # Animate with a narrow rotation range to keep the face frontal
    anim = animation.FuncAnimation(fig, update, frames=np.linspace(-30, 30, 60),
                                   interval=50, blit=False)
    output_file = 'female_face_hologram.gif'
    anim.save(output_file, writer='pillow', fps=30,
              savefig_kwargs={'facecolor': 'black'})
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Failed to create {output_file}")
except Exception as e:
    print("Error during animation generation:", e)
    raise
finally:
    plt.close()
