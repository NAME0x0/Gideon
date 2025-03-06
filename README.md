# Advanced Humanoid Holographic AI Face

An interactive 3D holographic AI face visualization with dynamic particle effects. This project renders a 3D STL model as a futuristic hologram with animated particles and gradient effects.

![Humanoid Holographic AI Face](hologram_face.gif)

## Features

- **Advanced Particle System**: Dynamic particles that orbit and follow the facial structure
- **Red-Blue Gradient**: Sophisticated color gradient that transitions based on the Z-axis position
- **Dynamic Animation**: Particles move with simulated physics for a realistic holographic effect
- **Responsive Design**: Particles react to the rotation and adapt their movement accordingly
- **Pulsating Effects**: Both the mesh and particles feature subtle pulsating effects for added realism

## Technical Implementation

The hologram is generated using a combination of technologies:

- **Trimesh**: For loading and manipulating the 3D STL model
- **Matplotlib**: For rendering the 3D visualization and particle effects
- **NumPy**: For efficient mathematical operations and particle physics
- **GitHub Actions**: For automatic daily regeneration of the hologram animation

## Local Generation

For custom hologram generation, use the included `local_generate.py` script:

```bash
# Basic usage
python local_generate.py

# Generate with more particles
python local_generate.py --particles 5000

# Custom output with higher quality
python local_generate.py --quality 150 --output my_hologram.gif

# Color emphasis options
python local_generate.py --red-gradient
python local_generate.py --blue-gradient

# Complete example with custom settings
python local_generate.py --particles 4000 --frames 240 --quality 200 --fps 40 --output high_quality_hologram.gif
```

## Usage in Other Projects

This holographic system can be integrated into other projects by:

1. Including the STL model file in your project
2. Importing the generation script
3. Customizing parameters like particle count, colors, and animation speed

## Customization Options

The script offers several customization options:

- Adjust particle count via the `generate_particles()` function
- Modify the color scheme by changing the `colors_red_blue` array
- Tune physics parameters like velocity and dampening
- Configure animation frames and quality settings

## Automatic Updates

The hologram is automatically regenerated daily via GitHub Actions, ensuring the visualization remains current with any changes to the underlying model or rendering code.

## License

See the [LICENSE](LICENSE) file for details.
