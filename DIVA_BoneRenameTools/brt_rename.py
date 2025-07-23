# brt_rename.py（旧rename_bones.py）

import bpy
import re
from os.path import commonprefix

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


def extract_rename_settings(bone_name, prefix_filter=None):
    """ 指定ボーン名から、開始番号・ルール（桁数）・末尾サフィックスを抽出 """
    name = bone_name.split(".")[0]
    suffix_candidates = {"_wj", "wj", "_wj_ex", "wj_ex"}

    # 末尾のサフィックスを抽出（あれば）
    suffix = next((s for s in suffix_candidates if name.endswith(s)), "_wj")

    # 数字部分の抽出（例: _002 → 2）
    match = re.search(r"_(\d{2,3})(?:_)?(wj|wj_ex)?$", name)
    if match:
        num_str = match.group(1)
        number = int(num_str)
        rule = "000" if len(num_str) == 3 else "00"
    else:
        number = 0
        rule = "000"

    return number, rule, suffix

def update_rename_settings_from_selection(scene):
    """現在選択中のボーンに応じてリネーム設定を更新する"""
    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        return

    bones = obj.data.edit_bones if bpy.context.mode == 'EDIT_ARMATURE' else obj.pose_bones
    selected = [b for b in bones if getattr(b, "select", False)]
    if not selected:
        return

    num, rule, suffix = extract_rename_settings(selected[0].name)
    scene.brt_rename_start_number = num
    scene.brt_rename_rule = rule
    scene.brt_rename_suffix = suffix



# 連番法則に反映する用
def get_linear_chain(bone_name, prefix_filter=None):
    from .brt_sub import clean_name
    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        return []

    mode = bpy.context.mode
    if mode == 'POSE':
        bones = obj.pose.bones
        get_name = lambda b: b.name
        get_parent = lambda b: b.parent
        get_children = lambda b: b.children
        is_valid = lambda b: b.bone
    elif mode == 'EDIT_ARMATURE':
        bones = obj.data.edit_bones
        get_name = lambda b: b.name
        get_parent = lambda b: b.parent
        get_children = lambda b: b.children
        is_valid = lambda b: True
    else:
        return []

    bone = bones.get(bone_name)
    if not bone or not is_valid(bone):
        return []

    # 親方向に一本道をさかのぼる
    current = bone
    while True:
        parent = get_parent(current)
        if not parent or len(get_children(parent)) != 1:
            break
        if prefix_filter and not clean_name(get_name(parent)).startswith(prefix_filter):

            break
        current = parent
    root = current

    # 子方向に一本道をたどる
    chain = []
    current = root
    while current:
        cname = clean_name(get_name(current))
        if prefix_filter and not cname.startswith(prefix_filter):
            break
        chain.append(current)
        children = get_children(current)
        if len(children) == 1:
            current = children[0]
        else:
            break

    return chain