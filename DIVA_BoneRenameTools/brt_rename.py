# brt_rename.py（旧rename_bones.py）

import bpy

def get_depth(bone, depth=0):
    """ 再帰的に親ボーンの深さを取得する """
    return get_depth(bone.parent, depth + 1) if bone.parent else depth

def rename_selected_bones(prefix, start_number, suffix, rule):
    armature = bpy.context.object
    if not armature or armature.type != 'ARMATURE':
        print("No armature selected.")
        return
    
    if bpy.context.mode != 'EDIT_ARMATURE':
        print("Please enter Edit Mode first.")
        return

    # 共通部に "_" がついていない場合は補う
    if prefix and not prefix.endswith("_"):
        prefix += "_"

    selected_bones = [bone for bone in armature.data.edit_bones if bone.select]
    if not selected_bones:
        print("No bones selected.")
        return

    print(f"Renaming {len(selected_bones)} bones with prefix '{prefix}' and start number {start_number}")

    # 桁数を設定
    format_str = "{:03}" if rule == "000" else "{:02}"

    # 親子関係を基準に並べ替え
    sorted_bones = sorted(selected_bones, key=lambda b: get_depth(b))

    for i, bone in enumerate(sorted_bones):
        new_name = f"{prefix}{format_str.format(start_number + i)}{suffix}"
        print(f"Renaming {bone.name} → {new_name}")
        bone.name = new_name

    print("Bone renaming completed.")
