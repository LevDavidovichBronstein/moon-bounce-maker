import bpy
import math


# Speed of light in meters per second
speed_of_light = 299_792_458  # m/s

# Frequency of the antenna in Mhz
frequency_mhz = 1300

# Two dimensional size of the array of stacked antennas
# Example values:
#   (1, 1): A single antenna.
#   (1, 2): A vertical stack of 2 antennas.
#   (2, 2): A 2x2 grid of antennas.
stack_size = (3, 3)

# Spacing between stacked antennas is determined by stack_lambda
# 0.7 stack_lambda:
#   Pros: Lower side lobes, smoother radiation pattern.
#   Cons: Slightly broader main beam, resulting in lower directivity.
#   Best for: Applications where maintaining lower side lobe levels is crucial, such as when minimizing interference is important.
# 0.85 stack_lambda:
#   This is often seen as a good middle ground between directivity and side lobe control.
#   It provides a compromise with reasonably narrow beams and controlled side lobe levels.
#   It’s a versatile choice for applications like satellite communication or radar systems where a balance of high gain and low interference is needed.
# 1.0  stack_lambda:
#   Pros: Maximum directivity and narrowest beam, leading to high gain.
#   Cons: Higher side lobes and greater sensitivity to grating lobes.
#   Best for: Scenarios where achieving maximum gain is the top priority and side lobes are acceptable or can be managed, such as in long-range point-to-point communication.
stack_lambda = 1.0

# The base location for the array of antennas in the X, Y, Z directions
# Example values:
#   (0, 0, 0): Centered at the origin.
#   (10, 5, 2): Offset by 10 in X, 5 in Y, and 2 in Z.
stack_location = (0, 0, 0)

# The base rotation for the array of antennas in the X, Y, Z axis in degrees
# Example values:
#   (0, 0, 0): x, y, and z axis are 0 degrees
#   (0, 90, 90): rotated 90 degrees along y axis
stack_rotation = (0, 0, 0)

"""
 Parabolic Dish Parameters
"""
# Parabolic Focal Length to Diameter ratio determines the shape of the parabolic dish
# 0.6 parabolic_focal_length_to_diameter_ratio
#   Result in a shallower dish, which is more compact but might be less efficient.
# 0.25 parabolic_focal_length_to_diameter_ratio
#   Lower values result in a deeper dish, which can offer better focus but is physically larger.
parabolic_focal_length_to_diameter_ratio = 0.25

# Parabolic Grid Fraction is the fraction of a wavelength between grids of the parabolic dish.
# This should be significantly less than one wavelength to ensure the radio waves reflect off 
# the surface of the parabolic dish.  However, values to low could be hard to model
# 0.5 parabolic_grid_fraction:
#   Minimum possible value to reflect waves
# 0.25 parabolic_grid_fraction:
#   Reasonable balance beween the minimum and maximum than \lambda/2 (half of the wavelength) to ensure that the parabolic surface accurately reflects the waves.
# 0.1 parabolic_grid_fraction:
#   Maximum value offers great reflection but can be hard to model
parabolic_grid_fraction = 0.25  

# Grids of the parabolic dish need to be more than one wavelength apart
# The parabolic_grid_solidity ensures the waves are reflected
# 1 parabolic_grid_solidity:
#   Minimum value - with minimum material but less solidity
# 6 parabolic_grid_solidity:
#   Good balance over minimum
# 32 parabolic_grid_solidity:
#   Approaches a solid surface as values get higher depending on Mhz of antenna
parabolic_grid_solidity = 6

# The parabolic dish mesh width in meters.
# Verify that the parabolic_mesh_width is not too thin for the material strength
# as thin wireframes could break during printing, handling, or under a wind load.
# To thick a value creates more wind load and needs more material.
parabolic_mesh_width=0.0015


"""
 Helical Antenna parameters
"""
# The Helical Circumference Factor allows you to adjust the 
# circumference of the helix relative to the wavelength. 
# This can help fine-tune the diameter for impedance matching or other design considerations.
# Typical Values:
#   0.75 helix_circumference_factor: Results in a slightly smaller helix, which may be useful for compact designs.
#   1.0 helix_circumference_factor: Matches the guideline of lambda/pi, giving a good balance between performance and ease of design.
#   1.25 helix_circumference_factor: A larger helix diameter, which can adjust the impedance and potentially increase gain.
helix_circumference_factor = 1.0

# The Helix Pitch Angle has these Common Values for helical antennas range from 10° to 15°:
#   10°: Results in a tighter, more compact helix with more turns per unit length.
#   12° to 14°: Provides a good balance between gain and bandwidth.
#   15°: Creates a looser helix with fewer turns per unit length, potentially increasing the gain but making the antenna longer.    
helix_pitch_angle = 14
        
# The Number of turns in the helix.  Each doubling of the number of turns in the
# helix increases the db by about 3.   It may get unwieldy past 25 turns but this
# might be seen as close to the structural limit while providing the moast gain.
# It can be incrased beyond 25, indeed 25 itself is quite a lot, but structural 
# support is generally necessary behond this number.
helix_number_of_turns=25

# Thickness of the helical antenna element in meters.
# Some typical values are based on the following AWG - Diameter (meters)
# 4 : 0.005189
# 6 : 0.004115
# 8 : 0.003264
# 10 : 0.002588
# 12 : 0.002052
# 14 : 0.001628
# 16 : 0.00129
# 18 : 0.001024
# 20 : 0.000813
# 22 : 0.000643
helix_wire_thickness=0.002588

# The number of vertices per turn of the helix.
# The higher the number the smoother it will render,
# but smoothness may not be replicatable in 3D printing
# Ranges from 100 to 150 are a good starting point
helix_vertices_per_turn=150

"""
 Transitional Expanding Helix parameters
"""

# The transitional expanding helix consists of one wavelenth
# of an expanding helix from the focal point of the parabolic
# dish to the beginning of the rings of the helical antenna 
transition_number_of_turns=2

# Transition interpolation is how the element from the focal point
# to the rings of the helix is create.  Supported values:
#   linear: Linear interpolation means that the radius of the expanding helix increases uniformly 
#       from the start diameter to the end diameter.
#       This results in a straightforward, even transition, where each increment in the angle 
#       produces a corresponding equal increment in radius.
#   ease_in: the change in radius starts out slowly and then accelerates towards the end.
#       This type of interpolation can create a gradual start where the expansion is more subtle 
#       at the beginning but becomes more pronounced as it approaches the end diameter.
#   ease_out:the opposite of ease-in: it starts with a faster change and then slows down as it 
#       approaches the end.  This is useful if you want the expanding helix to quickly reach 
#       a larger radius and then smooth out as it approaches the end diameter.
transition_interpolation='ease_out'
    

def convert_frequency_to_hz():
    """
    Convert the operating frequency from megahertz (MHz) to hertz (Hz).

    This function is used to convert the user-defined frequency, which is
    specified in megahertz (MHz), into hertz (Hz) for use in 
    calculations involving wavelength, speed of light, and other RF 
    parameters that require frequency to be in hertz.

    Returns:
    - frequency_hz (float): The converted frequency in hertz (Hz).

    Example:
    --------
    If the input frequency is 1300 MHz, this function will return:
    1300 * 1e6 = 1,300,000,000 Hz or 1.3 GHz.

    Notes:
    ------
    1 MHz is equal to 1,000,000 Hz (1e6 Hz). Converting frequency to Hz 
    ensures compatibility with calculations that use the speed of light 
    (in meters per second) and require frequency in Hz.
    """
    return frequency_mhz * 1e6
 

def calculate_stack_distance(lambda_factor):
    """
    Calculate the stack distance between antennas based on frequency in MHz and lambda factor.

    Parameters:
    - lambda_factor (float): The multiplier for the wavelength to determine the spacing.
                             Typical values are between 0.7 and 1.0.

    Returns:
    - stack_distance (float): The calculated distance between antennas in meters.
    """

    # Convert frequency from MHz to Hz for the calculation
    frequency_hz = convert_frequency_to_hz()

    # Calculate the wavelength in meters
    wavelength = speed_of_light / frequency_hz

    # Calculate the stack distance as a fraction of the wavelength
    stack_distance = lambda_factor * wavelength

    return stack_distance




def calculate_parabolic_focal_length(diameter, f_to_d_ratio):
    """
    Calculate the focal length of a parabolic dish based on its diameter and f/D ratio.

    Parameters:
    - diameter (float): Diameter of the parabolic dish in meters.
    - f_to_d_ratio (float): The focal length to diameter ratio (f/D ratio).
                            Typical values range from 0.25 to 0.5.

    Returns:
    - focal_length (float): Calculated focal length in meters.
    """
    # Calculate the focal length using the given f/D ratio
    return f_to_d_ratio * diameter


def calculate_grid_spacing(wavelength_fraction):
    """
    Calculate the grid spacing for a parabolic dish based on the wavelength of the given frequency.

    Parameters:
    - wavelength_fraction (float): The fraction of the wavelength to be used for grid spacing.
                                   Typical values are 0.1 (λ/10), 0.25 (λ/4), or 0.5 (λ/2).

    Returns:
    - grid_spacing (float): The calculated grid spacing in meters.
    """
    # Convert frequency from MHz to Hz
    frequency_hz = convert_frequency_to_hz()

    # Calculate the wavelength in meters
    wavelength = speed_of_light / frequency_hz

    # Calculate the grid spacing as a fraction of the wavelength
    grid_spacing = wavelength_fraction * wavelength

    return grid_spacing


def calculate_parabolic_grid_segments(diameter, grid_spacing):
    """
    Calculate the number of grid segments for the parabolic dish based on the diameter and grid spacing.

    Parameters:
    - diameter (float): Diameter of the parabolic dish in meters.
    - grid_spacing (float): The spacing between grid points in meters.

    Returns:
    - grid_segments (int): Calculated number of segments for the outer ring.
    """
    # Calculate the radius of the parabolic dish
    radius = diameter / 2

    # Calculate the circumference of the outermost ring
    circumference = 2 * math.pi * radius

    # Calculate the minimum number of segments to maintain the grid spacing
    min_segments = int(circumference / grid_spacing)

    # Calculate the optimal number of segments to maintain the grid spacing
    grid_segments = min_segments * parabolic_grid_solidity

    # Ensure the minimum 
    return max(grid_segments, min_segments)


def calculate_helix_diameter(circumference_factor):
    """
    Calculate the diameter of a helical antenna based on its operating frequency.

    Parameters:
    - circumference_factor (float): A multiplier for the circumference of the helix relative to λ/π.
      Typical values are between 0.75 and 1.25, with 1.0 providing a balanced design.

    Returns:
    - helix_diameter (float): Calculated diameter of the helix in meters.
    """
    # Convert frequency from MHz to Hz
    frequency_hz = convert_frequency_to_hz()

    # Calculate the wavelength in meters
    wavelength = speed_of_light / frequency_hz

    # Calculate the helix diameter using the circumference factor
    helix_diameter = (wavelength / math.pi) * circumference_factor

    return helix_diameter


def calculate_helix_turn_spacing():
    """
    Calculate the turn spacing of a helical antenna based on its operating frequency and pitch angle.
ees.

    Returns:
    - turn_spacing (float): Calculated turn spacing in meters.
    """

    # Convert frequency from MHz to Hz
    frequency_hz = convert_frequency_to_hz()

    # Calculate the wavelength in meters
    wavelength = speed_of_light / frequency_hz

    # Convert the pitch angle from degrees to radians
    pitch_angle_rad = math.radians(helix_pitch_angle)

    # Calculate the turn spacing using the formula
    turn_spacing = (wavelength / math.pi) * math.tan(pitch_angle_rad)

    return turn_spacing


def create_parabolic_dish(
    base_x, base_y, base_z,
    rotation_x, rotation_y, rotation_z,
    parabolic_diameter,
    parabolic_focal_length,
    parabolic_grid_spacing,
    parabolic_grid_segments,
    parabolic_mesh_width
):
    """
    Creates a parabolic dish mesh in Blender at a specified location.

    The function generates a parabolic dish based on the given diameter, focal length, 
    and grid spacing parameters. The parabolic surface is approximated by vertices arranged 
    in concentric rings, with a wireframe modifier applied to simulate a mesh-like structure.

    Parameters:
    - base_x (float): The X-coordinate of the dish's base location.
    - base_y (float): The Y-coordinate of the dish's base location.
    - base_z (float): The Z-coordinate of the dish's base location.
    - parabolic_diameter (float): The diameter of the parabolic dish in meters.
                                  This defines the overall size of the dish.
    - parabolic_focal_length (float): The focal length of the parabolic dish in meters.
                                      Determines the curvature and focus of the dish.
    - parabolic_grid_spacing (float): The distance between grid points on the dish surface, 
                                      representing a fraction of the wavelength. 
                                      Lower values provide finer detail.
    - parabolic_grid_segments (int): The number of segments in each ring of the parabolic dish.
                                     A higher number results in a smoother dish surface.
    - parabolic_mesh_width (float): The thickness of the wireframe applied to the parabolic dish.
                                    Controls the physical width of the mesh wires.

    Returns:
    - None: The function directly modifies the Blender scene, creating and positioning 
            a new object named 'ParabolicDish' with the specified properties.

    Notes:
    - The parabolic dish is created as a mesh object and then converted to a wireframe 
      using Blender's wireframe modifier for a realistic mesh representation.
    - The dish is positioned at the specified base coordinates (base_x, base_y).
    - Adjusting the grid spacing and segments can significantly impact the appearance 
      and complexity of the dish.
    - This function assumes Blender's bpy module is already imported and that it is run 
      within a Blender Python environment.
    """
    
    print("Creating the parabolic dish...")
    bpy.ops.object.select_all(action='DESELECT')
    mesh = bpy.data.meshes.new('ParabolicDish')
    dish = bpy.data.objects.new('ParabolicDish', mesh)
    bpy.context.collection.objects.link(dish)

    verts = []
    faces = []
    rings = int(parabolic_diameter  * parabolic_grid_solidity/ parabolic_grid_spacing ) 

    for r in range(rings + 1):
        radius = (r / rings) * (parabolic_diameter / 2)
        z = (radius ** 2) / (4 * parabolic_focal_length)
        for seg in range(parabolic_grid_segments):
            angle = 2 * math.pi * (seg / parabolic_grid_segments)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            verts.append((x, y, z))

    for r in range(rings):
        for seg in range(parabolic_grid_segments):
            v1 = r * parabolic_grid_segments + seg
            v2 = r * parabolic_grid_segments + (seg + 1) % parabolic_grid_segments
            v3 = (r + 1) * parabolic_grid_segments + (seg + 1) % parabolic_grid_segments
            v4 = (r + 1) * parabolic_grid_segments + seg
            faces.append((v1, v2, v3, v4))

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    dish.select_set(True)
    bpy.context.view_layer.objects.active = dish
    bpy.ops.object.modifier_add(type='WIREFRAME')
    dish.modifiers['Wireframe'].thickness = parabolic_mesh_width
    dish.modifiers['Wireframe'].offset = 0
    dish.modifiers['Wireframe'].use_even_offset = True
    bpy.ops.object.modifier_apply(modifier="Wireframe")
    print("Wireframe modifier applied to the parabolic dish.")
    
    
    dish.location = (base_x, base_y, base_z)
    print("Parabolic dish with wireframe grid created successfully.")
    return dish;



def create_expanding_helix(
    base_x, base_y, base_z,
    parabolic_focal_length,
    helix_diameter,
    helix_turn_spacing,
    helix_wire_thickness,
    helix_vertices_per_turn,
    transition_number_of_turns,
    transition_interpolation
):
    """
    Creates an expanding helical structure in Blender, originating from the focal point of a parabolic dish.

    Parameters:
    - base_x, base_y, base_z (float): Coordinates of the base location for the expanding helix.
    - parabolic_focal_length (float): The focal length of the associated parabolic dish.
    - helix_diameter (float): Diameter of the helix at its final turn.
    - helix_turn_spacing (float): Spacing between each turn of the helix.
    - helix_wire_thickness (float): Thickness of the wire for the helical structure.
    - helix_vertices_per_turn (int): Number of vertices used per turn of the helix for smoothness.
    - transition_number_of_turns (int): Number of turns in the expanding helix.
    - transition_interpolation (str): Interpolation type for radius expansion ('linear', 'ease_in', 'ease_out').

    Returns:
    - total_height (float): Total height of the expanding helix.
    - curve_obj (bpy.types.Object): The Blender curve object representing the expanding helix.
    
    Notes:
    - The helix gradually expands from the focal point diameter to the specified helix diameter.
    - The transition interpolation determines how the radius changes over the length of the helix.
    """

    total_height = helix_turn_spacing * transition_number_of_turns
    verts = []
    edges = []

    start_diameter=0.0
    def interpolate_radius(t):
        if transition_interpolation == 'linear':
            return (start_diameter / 2) + t * (helix_diameter / 2 - start_diameter / 2)
        elif transition_interpolation == 'ease_in':
            return (start_diameter / 2) + (t ** 2) * (helix_diameter / 2 - start_diameter / 2)
        elif transition_interpolation == 'ease_out':
            return (start_diameter / 2) + (1 - (1 - t) ** 2) * (helix_diameter / 2 - start_diameter / 2)
        else:
            print(f"Invalid transition_interpolation method: {t}")
            raise ValueError("Invalid transition_interpolation method. Choose 'linear', 'ease_in', or 'ease_out'.")

    for i in range(transition_number_of_turns * helix_vertices_per_turn + 1):
        t = i / (transition_number_of_turns * helix_vertices_per_turn)
        angle = t * 2 * math.pi * transition_number_of_turns
        radius = interpolate_radius(t)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = t * total_height
        verts.append((x, y, z))
        if i > 0:
            edges.append((i - 1, i))

    mesh = bpy.data.meshes.new("ExpandingHelix")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("ExpandingHelix", mesh)
    bpy.context.collection.objects.link(obj)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='CURVE')
    curve_obj = bpy.context.active_object
    curve_obj.name = 'ExpandingHelix'
    curve_obj.data.bevel_depth = helix_wire_thickness / 2
    curve_obj.data.fill_mode = 'FULL'
    curve_obj.data.bevel_resolution = 4

    curve_obj.location = (0, 0, parabolic_focal_length)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)    
    print(f"Expanding helix with {transition_number_of_turns} turns created successfully using '{transition_interpolation}' transition_interpolation!")
    
    # Return both the total height and the curve object
    return total_height, curve_obj

def create_helix(
    base_x, base_y, base_z,
    transition_length,
    parabolic_focal_length,
    helix_diameter,
    helix_turn_spacing,
    helix_number_of_turns,
    helix_wire_thickness,
    helix_vertices_per_turn
):
    """
    Creates a helical antenna structure in Blender.

    Parameters:
    - base_x, base_y, base_z (float): Coordinates for the base location of the helix.
    - transition_length (float): Length of the expanding transition from the parabolic focal point to the start of the helix.
    - parabolic_focal_length (float): The focal length of the associated parabolic dish.
    - helix_diameter (float): Diameter of the helix.
    - helix_turn_spacing (float): Spacing between each turn of the helix.
    - helix_number_of_turns (int): Total number of turns for the helix.
    - helix_wire_thickness (float): Thickness of the wire for the helix.
    - helix_vertices_per_turn (int): Number of vertices used per turn of the helix for smoothness.

    Returns:
    - curve_obj (bpy.types.Object): The Blender curve object representing the helix.

    Notes:
    - The helix is created as a curve object in Blender to control its thickness and apply necessary transformations.
    - This function also positions the helix relative to the focal point of a parabolic dish for a complete antenna setup.
    """

    height = helix_turn_spacing * helix_number_of_turns
    verts = []
    edges = []

    for i in range(helix_number_of_turns * helix_vertices_per_turn + 1):
        angle = (i / helix_vertices_per_turn) * 2 * math.pi
        x = (helix_diameter / 2) * math.cos(angle)
        y = (helix_diameter / 2) * math.sin(angle)
        z = (i / helix_vertices_per_turn) * helix_turn_spacing
        verts.append((x, y, z))
        if i > 0:
            edges.append((i - 1, i))

    # Create the mesh
    mesh = bpy.data.meshes.new("Helix")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    # Create the object
    obj = bpy.data.objects.new("Helix", mesh)
    bpy.context.collection.objects.link(obj)

    # Convert to curve for thickness control
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='CURVE')
    curve_obj = bpy.context.active_object
    curve_obj.name = 'Helix'
    curve_obj.data.bevel_depth = helix_wire_thickness / 2
    curve_obj.data.fill_mode = 'FULL'
    curve_obj.data.bevel_resolution = 4

    curve_obj.location = (0, 0, parabolic_focal_length + transition_length)

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    print("Helix created successfully!")
    return curve_obj;
    
    
def create_antenna(
    base_x, base_y, base_z,
    rotation_x, rotation_y, rotation_z,
    parabolic_diameter,
    parabolic_focal_length,
    parabolic_grid_spacing,
    parabolic_grid_segments,
    parabolic_mesh_width,
    helix_diameter,
    helix_turn_spacing,
    helix_number_of_turns,
    helix_wire_thickness,
    helix_vertices_per_turn,
    transition_number_of_turns,
    transition_interpolation
):
    """
    Creates a complete antenna structure in Blender, consisting of a parabolic dish, an expanding helix, and a main helical element.

    Parameters:
    - base_x, base_y, base_z (float): Coordinates for the base location of the antenna.
    - rotation_x, rotation_y, rotation_z (float): Rotation angles for the antenna along the X, Y, and Z axes (in degrees).
    - parabolic_diameter (float): Diameter of the parabolic dish.
    - parabolic_focal_length (float): Focal length of the parabolic dish.
    - parabolic_grid_spacing (float): Spacing between grid points on the parabolic dish.
    - parabolic_grid_segments (int): Number of segments for the outer ring of the parabolic dish.
    - parabolic_mesh_width (float): Thickness of the wireframe applied to the parabolic dish.
    - helix_diameter (float): Diameter of the helical antenna.
    - helix_turn_spacing (float): Spacing between each turn of the helical antenna.
    - helix_number_of_turns (int): Number of turns in the helical antenna.
    - helix_wire_thickness (float): Thickness of the wire for the helical element.
    - helix_vertices_per_turn (int): Number of vertices used per turn of the helix for smoothness.
    - transition_number_of_turns (int): Number of turns for the expanding helix transition.
    - transition_interpolation (str): Type of interpolation for the expanding helix transition ('linear', 'ease_in', 'ease_out').

    Returns:
    - None: The function directly modifies the Blender scene, creating and positioning a new antenna structure.

    Notes:
    - The antenna consists of a parabolic dish, an expanding helix from the focal point, and a main helix.
    - The dish acts as the parent for both the expanding helix and the main helical element.
    - The entire structure is positioned and rotated based on the specified base coordinates and rotation angles.
    """

    dish = create_parabolic_dish(base_x=base_x, base_y=base_y, base_z=base_z, 
        rotation_x=rotation_x, rotation_y=rotation_y, rotation_z=rotation_z,
        parabolic_diameter=parabolic_diameter, parabolic_focal_length=parabolic_focal_length, 
        parabolic_grid_spacing=parabolic_grid_spacing,
        parabolic_grid_segments=parabolic_grid_segments, parabolic_mesh_width=parabolic_mesh_width
    )

    expanding_helix_height, expanding_helix  = create_expanding_helix(
        base_x=base_x, base_y=base_y, base_z=base_z,
        parabolic_focal_length=parabolic_focal_length,
        helix_diameter=helix_diameter,
        helix_turn_spacing=helix_turn_spacing,
        helix_wire_thickness=helix_wire_thickness,
        helix_vertices_per_turn=helix_vertices_per_turn,
        transition_number_of_turns=transition_number_of_turns,
        transition_interpolation=transition_interpolation
    )

            
    helix = create_helix(
        base_x=base_x, base_y=base_y, base_z=base_z,
        transition_length=expanding_helix_height,
        parabolic_focal_length=parabolic_focal_length,
        helix_diameter=helix_diameter,
        helix_turn_spacing=helix_turn_spacing,
        helix_number_of_turns=helix_number_of_turns,
        helix_wire_thickness=helix_wire_thickness,
        helix_vertices_per_turn=helix_vertices_per_turn
    )
    
    print(f"Helical antenna created at {base_x},{base_y},{base_z}")
    print(f"Helical antenna rotationat {rotation_x},{rotation_y},{rotation_z}")
    return dish, expanding_helix, helix

    
def create_antenna_array(
    array_elements_x, array_elements_y, 
    base_x, base_y, base_z,
    rotation_x, rotation_y, rotation_z,
    parabolic_diameter,
    parabolic_focal_length,
    parabolic_grid_spacing,
    parabolic_grid_segments,
    parabolic_mesh_width,
    helix_diameter,
    helix_turn_spacing,
    helix_number_of_turns,
    helix_wire_thickness,
    helix_vertices_per_turn,
    transition_number_of_turns,
    transition_interpolation
):
    """
    Creates an array of antenna structures in Blender, arranging multiple antennas in a grid layout.

    Parameters:
    - array_elements_x, array_elements_y (int): Number of antenna elements in the X and Y directions.
    - base_x, base_y, base_z (float): Coordinates for the base location of the antenna array.
    - rotation_x, rotation_y, rotation_z (float): Rotation angles for the antennas along the X, Y, and Z axes (in degrees).
    - parabolic_diameter (float): Diameter of the parabolic dish for each antenna.
    - parabolic_focal_length (float): Focal length of the parabolic dish for each antenna.
    - parabolic_grid_spacing (float): Spacing between grid points on the parabolic dish for each antenna.
    - parabolic_grid_segments (int): Number of segments for the outer ring of the parabolic dish for each antenna.
    - parabolic_mesh_width (float): Thickness of the wireframe applied to the parabolic dish for each antenna.
    - helix_diameter (float): Diameter of the helical antenna for each element.
    - helix_turn_spacing (float): Spacing between each turn of the helical antenna for each element.
    - helix_number_of_turns (int): Number of turns in the helical antenna for each element.
    - helix_wire_thickness (float): Thickness of the wire for the helical element for each antenna.
    - helix_vertices_per_turn (int): Number of vertices used per turn of the helix for smoothness for each element.
    - transition_number_of_turns (int): Number of turns for the expanding helix transition for each element.
    - transition_interpolation (str): Type of interpolation for the expanding helix transition ('linear', 'ease_in', 'ease_out').

    Returns:
    - None: The function directly modifies the Blender scene, creating and positioning an array of antenna structures.

    Notes:
    - The antennas are arranged in a grid based on the specified number of elements in the X and Y directions.
    - Each antenna in the array is created using the same parameters, and their positions are calculated to form a regular layout centered around the base coordinates.
    """

    # Create an empty 'Antenna' object to parent the entire array
    bpy.ops.object.select_all(action='DESELECT')
    array_parent = bpy.data.objects.new('AntennaArray', None)
    array_parent.empty_display_type = 'PLAIN_AXES'
    bpy.context.collection.objects.link(array_parent)
    array_parent.location = (base_x, base_y, base_z)
    array_parent.rotation_euler = (math.radians(rotation_x), math.radians(rotation_y), math.radians(rotation_z))
    
    print(f"Created 'AntennaArray' empty at base location: ({base_x}, {base_y}, {base_z}) with rotation ({rotation_x}, {rotation_y}, {rotation_z})")

    # Calculate the total width and height of the array
    total_width = (array_elements_x - 1) * parabolic_diameter
    total_height = (array_elements_y - 1) * parabolic_diameter

    # Calculate the starting position to center the array around base_x and base_y
    start_x = -total_width / 2
    start_y = -total_height / 2

    # Calculate the positions for each antenna and add them to the parent
    for i in range(array_elements_x):
        for j in range(array_elements_y):
            x = start_x + i * parabolic_diameter
            y = start_y + j * parabolic_diameter
            z = 0  # Offset relative to the parent

            # Create each antenna element
            dish, expanding_helix, helix = create_antenna(
                base_x=x, base_y=y, base_z=z,
                rotation_x=0, rotation_y=0, rotation_z=0,
                parabolic_diameter=parabolic_diameter,
                parabolic_focal_length=parabolic_focal_length,
                parabolic_grid_spacing=parabolic_grid_spacing,
                parabolic_grid_segments=parabolic_grid_segments,
                parabolic_mesh_width=parabolic_mesh_width,
                helix_diameter=helix_diameter,
                helix_turn_spacing=helix_turn_spacing,
                helix_number_of_turns=helix_number_of_turns,
                helix_wire_thickness=helix_wire_thickness,
                helix_vertices_per_turn=helix_vertices_per_turn,
                transition_number_of_turns=transition_number_of_turns,
                transition_interpolation=transition_interpolation
            )

            # Set the dish as the parent of both expanding helix and helix
            expanding_helix.parent = dish
            helix.parent = dish

            # Parent the entire dish structure to the empty 'AntennaArray' object
            dish.parent = array_parent

            print(f"Antenna element created at X: {x}, Y: {y}, Z: {z}")

    print("Antenna array created successfully!")




stack_distance = calculate_stack_distance(stack_lambda)
print(f"Stack distance for {frequency_mhz} MHz with lambda factor {stack_lambda}: {stack_distance:.4f} meters")

parabolic_focal_length= calculate_parabolic_focal_length(stack_distance, parabolic_focal_length_to_diameter_ratio)
print(f"Parabolic Focal Length for {frequency_mhz} MHz with focal length to diameter ratio (f/D ratio): {parabolic_focal_length_to_diameter_ratio}: {parabolic_focal_length:.4f} meters")

grid_spacing = calculate_grid_spacing(parabolic_grid_fraction)
print(f"Grid spacing for {frequency_mhz} MHz with a fraction {parabolic_grid_fraction}: {grid_spacing:.4f} meters")

grid_segments = calculate_parabolic_grid_segments(stack_distance, grid_spacing)
print(f"Calculated number of grid segments for diameter {stack_distance} meters with grid spacing {grid_spacing}: {grid_segments}")

diameter = calculate_helix_diameter(helix_circumference_factor)
print(f"Helix diameter for {frequency_mhz} MHz with circumference factor {helix_circumference_factor}: {diameter:.4f} meters")
# .073

turn_spacing = calculate_helix_turn_spacing()
print(f"Helix turn spacing for {frequency_mhz} MHz with pitch angle {helix_pitch_angle}°: {turn_spacing:.4f} meters")



create_antenna_array(
    array_elements_x=stack_size[0], array_elements_y=stack_size[1], 
    base_x=stack_location[0], base_y=stack_location[1], base_z=stack_location[2],
    rotation_x=stack_rotation[0],rotation_y=stack_rotation[1], rotation_z=stack_rotation[2],
    parabolic_diameter=stack_distance,
    parabolic_focal_length=parabolic_focal_length,
    parabolic_grid_spacing=grid_spacing,
    parabolic_grid_segments=grid_segments,
    parabolic_mesh_width=parabolic_mesh_width,
    helix_diameter=diameter,
    helix_turn_spacing=turn_spacing,
    helix_number_of_turns=helix_number_of_turns,
    helix_wire_thickness=helix_wire_thickness,
    helix_vertices_per_turn=helix_vertices_per_turn,
    transition_number_of_turns=transition_number_of_turns,
    transition_interpolation=transition_interpolation
   
)
