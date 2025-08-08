# brt_rename.py（旧rename_bones.py）

import bpy
import re
import uuid
from os.path import commonprefix

from .brt_debug import DEBUG_MODE   # デバッグ用

def get_depth(bone, depth=0):
    """ 再帰的に親ボーンの深さを取得する """
    return get_depth(bone.parent, depth + 1) if bone.parent else depth

def rename_selected_bones(prefix, start_number, suffix, rule):
    armature = bpy.context.object
    if DEBUG_MODE:
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
    
    if DEBUG_MODE:
        if not selected_bones:
            print("No bones selected.")
            return

        print(f"Renaming {len(selected_bones)} bones with prefix '{prefix}' and start number {start_number}")

    # 桁数を設定
    format_str = "{:03}" if rule == "000" else "{:02}"

    # 親子関係を基準に並べ替え
    sorted_bones = sorted(selected_bones, key=lambda b: get_depth(b))

    # 一時的な仮名を割り当てて重複回避
    temp_names = {}
    for bone in sorted_bones:
        temp_name = f"__TEMP_{uuid.uuid4().hex[:8]}"
        temp_names[bone] = temp_name
        bone.name = temp_name

    # リネーム処理
    for i, bone in enumerate(sorted_bones):
        new_name = f"{prefix}{format_str.format(start_number + i)}{suffix}"
        if DEBUG_MODE:
            print(f"Renaming {bone.name} → {new_name}")
        bone.name = new_name


def extract_rename_settings(bone_name, prefix_filter=None):
    """ 指定ボーン名から、開始番号・ルール（桁数）・末尾サフィックスを抽出 """
    name = bone_name.split(".")[0]
    # 優先度順（長い方が先）
    suffix_candidates = ["_wj_ex", "wj_ex", "_wj", "wj"]

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

# ボーンを増やす用
def find_terminal_bones(bones):
    """選択されたボーンの中から末端（子がいない）ボーンを検出"""
    selected_set = set(bones)
    terminals = [b for b in bones if not any(child.parent == b for child in selected_set)]
    return terminals


def extend_and_subdivide_bone(bone, segment_count):
    from mathutils import Vector

    direction = (bone.tail - bone.head).normalized()
    original_length = bone.length
    total_length = original_length * (segment_count + 1)
    bone.tail = bone.head + direction * total_length

    # 既存ボーン名を記録
    existing_names = set(bone.id_data.edit_bones.keys())

    bpy.ops.armature.select_all(action='DESELECT')
    bone.select = True
    bpy.ops.armature.subdivide(number_cuts=segment_count)

    # 分割後の新しいボーンにタグを付けて返す
    new_bones = [b for b in bone.id_data.edit_bones if b.name not in existing_names]
    for b in new_bones:
        b["brt_added"] = True  # ← 追加タグ

    # 新規ボーンを検出して返す
    return [b for b in bone.id_data.edit_bones if b.name not in existing_names]

# 末端ボーンの接続状態を判定する
def check_terminal_bone_connections(terminals):
    """  
    Returns:
        unsafe (List[str])   → 完全接続されており処理すべきでないボーン名
        warn_only (List[str]) → 接続はないが親として振る舞っているボーン名（警告対象）
    """
    bones = bpy.context.object.data.edit_bones
    unsafe = []
    warn_only = []

    for bone in terminals:
        for child in bones:
            if child.parent == bone:
                dist = (child.head - bone.tail).length
                if dist < 0.0001:
                    unsafe.append(bone.name)
                else:
                    warn_only.append(bone.name)
                break  # 子が1つでも接続されていれば判定対象

    return unsafe, warn_only