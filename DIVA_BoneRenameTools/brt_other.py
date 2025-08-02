# brt_other.py（旧rename_groups.py）

import bpy
import re

def rename_bones_and_vertex_groups():
    obj = bpy.context.object

    # `_r_` / `_l_` のパターンを先に処理
    for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                   else obj.vertex_groups if obj.type == 'MESH' else []):
        if "_r_" in target.name and not target.name.endswith(".R"):
            target.name += ".R"
        elif "_l_" in target.name and not target.name.endswith(".L"):
            target.name += ".L"

    # 限定された _r0 / _l0 パターンの処理
    for suffix in ["_r0", "_l0"]:
        for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                       else obj.vertex_groups if obj.type == 'MESH' else []):
            if suffix in target.name and not (target.name.endswith(".R") or target.name.endswith(".L")):
                if suffix.startswith("_r"):
                    target.name += ".R"
                else:
                    target.name += ".L"

    # 限定された _r1 / _l1 パターンの処理
    for suffix in ["_r1", "_l1"]:
        for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                       else obj.vertex_groups if obj.type == 'MESH' else []):
            if suffix in target.name and not (target.name.endswith(".R") or target.name.endswith(".L")):
                if suffix.startswith("_r"):
                    target.name += ".R"
                else:
                    target.name += ".L"

    print("Selective renaming (.R/.L) completed.")

def revert_renamed_names():
    obj = bpy.context.object

    # `.R` / `.L` を末尾から削除
    for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT' else obj.vertex_groups if obj.type == 'MESH' else []):
        if target.name.endswith(".R"):
            target.name = target.name[:-2]
        elif target.name.endswith(".L"):
            target.name = target.name[:-2]

    print("Reverting .R/.L suffixes completed.")


# 編集・POSEモード用付与関数
def rename_selected_bones():
    obj = bpy.context.object
    mode = bpy.context.mode

    if obj.type != 'ARMATURE':
        return False, 0

    bones = []
    if mode == 'EDIT_ARMATURE':
        bones = [b for b in obj.data.edit_bones if b.select]
    elif mode == 'POSE':
        bones = [pb.bone for pb in obj.pose.bones if pb.bone.select]

    renamed = 0
    for bone in bones:
        name = bone.name
        if "_r_" in name and not name.endswith(".R"):
            bone.name += ".R"
            renamed += 1
        elif "_l_" in name and not name.endswith(".L"):
            bone.name += ".L"
            renamed += 1
        elif any(s in name for s in ["_r0", "_r1"]) and not name.endswith(".R"):
            bone.name += ".R"
            renamed += 1
        elif any(s in name for s in ["_l0", "_l1"]) and not name.endswith(".L"):
            bone.name += ".L"
            renamed += 1

    return renamed

# 編集・POSEモード用除去関数
def revert_selected_bone_names():
    obj = bpy.context.object
    mode = bpy.context.mode

    if obj.type != 'ARMATURE':
        return 0

    bones = []
    if mode == 'EDIT_ARMATURE':
        bones = [b for b in obj.data.edit_bones if b.select]
    elif mode == 'POSE':
        bones = [pb.bone for pb in obj.pose.bones if pb.bone.select]

    reverted = 0
    for bone in bones:
        if bone.name.endswith(".R") or bone.name.endswith(".L"):
            bone.name = bone.name[:-2]
            reverted += 1

    return reverted