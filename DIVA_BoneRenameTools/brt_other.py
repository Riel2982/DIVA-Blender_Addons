# brt_other.py（旧rename_groups.py）

import bpy
import re


from .brt_debug import DEBUG_MODE   # デバッグ用


# --- オブジェクトモード用アーマチュア全体対象関数 --------------------------------------------------------------------------

# オブジェクトモード用全付与関数（not~endswithで重複付与は避ける）
def rename_bones_and_vertex_groups():
    obj = bpy.context.object

    renamed = 0     # リネームされた数
    skipped = 0     # すでに .R/.L が付いていたためスキップされた数

    # `_r_` / `_l_` のパターンを先に処理
    for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                   else obj.vertex_groups if obj.type == 'MESH' else []):

        if "_r_" in target.name:
            if not target.name.endswith(".R"):
                target.name += ".R"
                renamed += 1
            else:   #  _r_が含まれていて .R が末尾にある→スキップ
                skipped += 1
        elif "_l_" in target.name:
            if not target.name.endswith(".L"):
                target.name += ".L"
                renamed += 1
            else:   #  _l_が含まれていて .L が末尾にある→スキップ
                skipped += 1

    # 限定された _r0 / _l0 パターンの処理
    for suffix in ["_r0", "_l0"]:
        for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                       else obj.vertex_groups if obj.type == 'MESH' else []):
            if suffix in target.name :
                if not (target.name.endswith(".R") or target.name.endswith(".L")):
                    if suffix.startswith("_r"):
                        target.name += ".R"
                        renamed += 1
                    else:
                        target.name += ".L"
                        renamed += 1
                else:
                    skipped += 1

    # 限定された _r1 / _l1 パターンの処理
    for suffix in ["_r1", "_l1"]:
        for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT'
                       else obj.vertex_groups if obj.type == 'MESH' else []):
            if suffix in target.name :
                if not (target.name.endswith(".R") or target.name.endswith(".L")):
                    if suffix.startswith("_r"):
                        target.name += ".R"
                        renamed += 1
                    else:
                        target.name += ".L"
                        renamed += 1
                else:
                    skipped += 1

    if DEBUG_MODE:
        if renamed > 0:
            print(f"{renamed} 件の名前を変更しました。")
        elif skipped > 0:
            print(f"{skipped} 件はすでに .R/.L が付与されていたためスキップされました。")
        else:
            print("対象が見つかりませんでした。")
        print("Selective renaming (.R/.L) completed.")

    return renamed, skipped   # オペレーターにカウントを返す


# オブジェクトモード用全除去用関数
def revert_renamed_names():
    obj = bpy.context.object

    reverted = 0    # オペレーターカウント用

    # `.R` / `.L` を末尾から削除
    for target in (obj.data.bones if obj.type == 'ARMATURE' and bpy.context.mode == 'OBJECT' else obj.vertex_groups if obj.type == 'MESH' else []):
        if target.name.endswith(".R"):
            target.name = target.name[:-2]
            reverted += 1
        elif target.name.endswith(".L"):
            target.name = target.name[:-2]
            reverted += 1   
    if DEBUG_MODE:
        print("Reverting .R/.L suffixes completed.")

    return reverted     # オペレーターにカウントを返す



# --- 編集・ポーズモード用アーマチュア選択対象関数 --------------------------------------------------------------------------

# 編集・POSEモード用選択付与関数（not~endswithで重複付与は避ける）
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
    skipped = 0

    for bone in bones:
        name = bone.name
        if "_r_" in name :
            if not name.endswith(".R"):
                bone.name += ".R"
                renamed += 1
            else :
                skipped += 1
        elif "_l_" in name :
            if not name.endswith(".L"):
                bone.name += ".L"
                renamed += 1
            else:
                skipped += 1
        elif any(s in name for s in ["_r0", "_r1"]) :
            if not name.endswith(".R"):
                bone.name += ".R"
                renamed += 1
            else:
                skipped += 1
        elif any(s in name for s in ["_l0", "_l1"]) :
            if not name.endswith(".L"):
                bone.name += ".L"
                renamed += 1
            else:
                skipped += 1

    if DEBUG_MODE:
        if renamed > 0:
            print(f"{renamed} 件の名前を変更しました。")
        elif skipped > 0:
            print(f"{skipped} 件はすでに .R/.L が付与されていたためスキップされました。")
        else:
            print("対象が見つかりませんでした。")

    return renamed, skipped


# 編集・POSEモード用選択除去関数
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