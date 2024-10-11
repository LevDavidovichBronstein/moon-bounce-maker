# moon-bounce-maker README

## Overview

**Moon-Bounce-Maker** is a script designed to generate 3D models of an array of parabolic dish antennas with helical feeds using Blender's Python API (`bpy`). The script creates complex antenna structures consisting of a parabolic reflector, an expanding helix, and a helical element, and organizes them into a customizable grid array. Each element in the array represents an individual antenna unit that can be replicated to form a larger system suitable for advanced RF applications, such as Earth-Moon-Earth (EME) communications, satellite communications, or radio astronomy.

The generated 3D models are useful for visualization, prototyping, and design validation of antenna configurations. The script includes parameters that can be adjusted to control the physical characteristics of the parabolic dish, helix, and the overall array, making it highly configurable. The goal is to create an affordable and accessible solution for EME communication enthusiasts by leveraging 3D printing.

## Features

- **Antenna Structure**: Each antenna consists of a parabolic dish reflector with a helical feed and an expanding transition helix. The structure allows for the modeling of high-gain antennas suitable for RF applications, including EME communication.
- **Customizable Array**: Users can create an array of antennas by specifying the dimensions of the array (e.g., 1x1, 2x2, 3x3). The antenna elements are organized and controlled via an empty Blender object, allowing easy manipulation of the entire array.
- **Configurable Parameters**: Various parameters are exposed for customization, including frequency, dish size, helix properties, array spacing, and more. This allows users to tailor the array for specific gain, directivity, or bandwidth requirements.
- **Blender Integration**: Built on Blender's `bpy` module, the script directly modifies the Blender scene, creating complex 3D antenna models that are useful for prototyping and design visualization.
- **3D Printing Ready**: The generated antenna models are optimized for 3D printing, providing a cost-effective solution for building functional RF antennas.

## Key Parameters

- **Frequency**: Frequency of operation is set in MHz, which determines the size of the helical and parabolic elements.
- **Array Configuration**: `stack_size` allows for defining the number of antennas in the X and Y directions.
- **Dish and Helix Properties**: Parameters such as `parabolic_focal_length_to_diameter_ratio`, `helix_circumference_factor`, `helix_pitch_angle`, and `transition_interpolation` allow for detailed control over the geometry of each antenna.
- **Parent Control**: The entire antenna array is parented to an empty object named "AntennaArray" for easy transformation of the whole array (e.g., translation, rotation).

## Usage

1. **Install Blender**: Ensure Blender is installed and the script is executed within Blender's scripting environment.
2. **Set Parameters**: Modify the configuration parameters at the top of the script to define the frequency, size of the array, dish and helix properties, etc.
3. **Run the Script**: Execute the script in Blender's scripting environment. The array of antennas will be generated in the 3D viewport.
4. **Manipulate the Array**: Use the "AntennaArray" empty object to translate, rotate, or scale the entire antenna array as needed.

## Example Parameters

- **Frequency**: 1300 MHz for typical RF applications.
- **Stack Size**: A 3x3 array (`stack_size = (3, 3)`) to create a total of 9 antennas.
- **Helical Feed**: Configured with 25 turns for high gain and a pitch angle of 14 degrees.
- **Transition Helix**: Uses an `ease_out` interpolation for smooth expansion from the dish focal point to the helical element.

## Areas for Improvement:

- **Error Handling: Currently, the script lacks robust error handling. For instance, when creating objects or applying modifiers, it could benefit from checks to ensure successful operations. Adding try/except blocks could improve stability.
- **Efficiency Considerations: The creation of detailed mesh objects, such as parabolic dishes and helical structures, might be computationally intensive, especially for large arrays. It might be beneficial to include options to simplify the mesh or create lower-resolution proxies for visualization purposes.
- **User Interface (UI) Integration: If intended for broader use, the script could be extended to include a Blender UI panel for adjusting parameters directly from the Blender interface. This would make it user-friendly for those who prefer not to modify scripts directly.


## Dependencies

- **Blender**: This script requires Blender ([https://www.blender.org/](https://www.blender.org/)) with the `bpy` module for generating 3D models.
- **Python**: Python knowledge is required for editing the script parameters.

## License

Feel free to use, modify, and distribute this script. Contributions are welcome.

## Contribution

If you find this script useful, consider contributing by suggesting improvements or creating a pull request. Contributions can include new features, bug fixes, or optimizations for better performance.

## Contact

For any questions, feedback, or contributions, please reach out via GitHub.

## Acknowledgements

This script is inspired by RF antenna design principles and aims to provide a simple yet effective way to visualize and prototype helical parabolic antenna arrays for various communication applications, including Earth-Moon-Earth communication.
