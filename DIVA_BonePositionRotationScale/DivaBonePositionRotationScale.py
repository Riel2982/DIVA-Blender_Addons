import bpy
import mathutils

def format_vector(value):
    """Format the vector component to remove trailing zeros."""
    return f"{value:.6f}".rstrip('0').rstrip('.')  # Remove trailing zeros and possible decimal point

# 関数化
def get_bone_data():
    """アクティブなアーマチュアのボーン情報を文字列で取得する"""
    # Get the active armature object
    armature = bpy.context.active_object

    # Check if the active object is an armature
    if not armature or armature.type != 'ARMATURE':
        return None

    output_lines = []

    # Iterate through all bones in the armature
    for bone in armature.data.bones:
        # Get the bone's local transformation matrix
        bone_matrix_local = bone.matrix_local

        # Get the parent bone (if it exists)
        parent_bone = bone.parent
        parent_name = parent_bone.name if parent_bone else "None"

        # If there is a parent, get its local transformation matrix and combine
        if parent_bone:
            parent_matrix_local = parent_bone.matrix_local
            # Combine the parent's local matrix with the bone's local matrix to get the transformation in parent space
            bone_matrix_in_parent_space = parent_matrix_local.inverted() @ bone_matrix_local
        else:
            # If there's no parent, just use the bone's local matrix
            bone_matrix_in_parent_space = bone_matrix_local

        # Create permutation for converting X,Y,Z
        permutation_matrix = mathutils.Matrix((
            (0, 1, 0, 0),
            (1, 0, 0, 0),
            (0, 0, -1, 0),
            (0, 0, 0, 1)
        ))

        # Apply the permutation to convert X,Y,Z to Diva orientation
        converted_matrix = permutation_matrix @ bone_matrix_in_parent_space @ permutation_matrix.transposed()

        # Decompose the transformation into translation, rotation, and scale
        translation, rotation, scale = converted_matrix.decompose()

        # Normalize quaternion
        rotation.normalize()

        # Convert the quaternion to Euler angles (XYZ)
        rotation_euler = rotation.to_euler('XYZ')

        # Output the bone name and its position, rotation in Euler angles, and scale
        """PrintではなくOutputに変更"""
        output_lines.append(f"{bone.name}")
        output_lines.append(f"\tParentName: {parent_name}")
        output_lines.append(f"\tPosition: <{format_vector(translation.x)}, {format_vector(translation.y)}, {format_vector(translation.z)}>")
        output_lines.append(f"\tRotation: <{format_vector(rotation_euler.x)}, {format_vector(rotation_euler.y)}, {format_vector(rotation_euler.z)}>")
        output_lines.append(f"\tScale:    <{format_vector(scale.x)}, {format_vector(scale.y)}, {format_vector(scale.z)}>\n")

    return "\n".join(output_lines)