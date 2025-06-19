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