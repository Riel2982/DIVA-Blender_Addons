# rename_symmetry.py

import bpy
import re

def apply_mirrored_rename(context, pattern_name: str, *, duplicate=False, mirror=False):
    """
    選択中のボーンに対して、識別パターンに基づいて名前を反転リネーム。
    duplicate=True なら複製、mirror=True ならX軸ミラーも実行。
    """
    obj = context.object
    if not obj or obj.type != 'ARMATURE':
        return 0

    mode = context.mode
    if mode not in {'POSE', 'EDIT_ARMATURE'}:
        return 0

    # 1. ボーンの取得
    bones = []
    if mode == 'POSE':
        bones = [b for b in obj.pose.bones if b.bone.select]
    elif mode == 'EDIT_ARMATURE':
        bones = [b for b in obj.data.edit_bones if b.select]

    if not bones:
        return 0

    # 2. パターン情報の取得と変換辞書の用意
    mirror_map = get_pattern_map(pattern_name)
    if not mirror_map:
        return 0

    renamed = 0
    bpy.ops.object.mode_set(mode='EDIT')  # ミラーや複製はEDITモードで行う

    for bone in obj.data.edit_bones:
        if not bone.select:
            continue

        target = bone

        if duplicate:
            target = obj.data.edit_bones.new(bone.name + "_copy")
            target.head = bone.head
            target.tail = bone.tail
            target.roll = bone.roll
            target.use_connect = bone.use_connect
            target.parent = bone.parent
            renamed += 1

        if mirror:
            target.head[0] *= -1
            target.tail[0] *= -1

        new_name = apply_name_flip(target.name, mirror_map)
        target.name = new_name

    bpy.ops.object.mode_set(mode=mode)  # 元のモードに戻す
    return renamed


def get_pattern_map(name: str) -> dict:
    """
    指定されたパターン名に基づいて置換辞書を返す
    例: { "L": "R", "R": "L" }
    """
    # ここは後で Preferences のルールセットから動的に読み込めるようにする
    presets = {
        "L/R": {"_L": "_R", "_R": "_L"},
        "Left/Right": {"Left": "Right", "Right": "Left"},
    }
    return presets.get(name, {})


def apply_name_flip(name: str, mapping: dict) -> str:
    """
    ボーン名に対して左右識別子に基づく置換を適用
    """
    for a, b in mapping.items():
        if a in name:
            return name.replace(a, b)
    return name

# サフィックス除去関数
def strip_duplicate_suffix(name: str) -> str:
    """
    Blenderが自動で付ける `.001`, `.002` などを除去。
    例: 'Head_L.001' → 'Head_L'
    """
    return re.sub(r"\.\d{3}$", "", name)