# brt_invert.py（旧# rename_symmetry.py）

import bpy
import re
from typing import Optional


# 選択中のボーンに対して、識別パターンに基づいて名前を反転リネーム
def apply_mirrored_rename(context, pattern_name: str, *, duplicate=False, mirror=False, assign_identifier=False, suffix_enum="wj", rule_enum="000", rule_index=0):
    from .rename_detect import detect_common_prefix

    obj = context.object
    if not obj or obj.type != 'ARMATURE':
        return 0

    initial_mode = context.mode
    if initial_mode not in {'POSE', 'EDIT_ARMATURE'}:
        return 0

    # 対象ボーン収集（Pose or Edit）
    if initial_mode == 'POSE':
        bones = [b for b in obj.pose.bones if b.bone.select]
    elif initial_mode == 'EDIT_ARMATURE':
        bones = [b for b in obj.data.edit_bones if b.select]

    # デバック用
    print(f"▶ apply_mirrored_rename: mode = {initial_mode}")
    print(f"▶ 選択ボーン数: {len(bones)}")

    if not bones:
        return 0

    # 選ばれた識別子セットとルールに基づく辞書を取得
    rule_index = rule_index if assign_identifier else None
    mirror_map = get_pattern_map_from_prefs(context, pattern_name, rule_index)
    if not mirror_map:
        return 0

    # プレフィックスを抽出（必要なら）
    prefix = detect_common_prefix(bones, suffix_enum, rule_enum) if assign_identifier else None

    # デバック用
    print(f"▶ mirror_map: {mirror_map}")
    print(f"▶ prefix: {prefix}")

    renamed = 0
    bpy.ops.object.mode_set(mode='EDIT')  # ミラーや複製はEDITで実行

    bone_map = {}  # オリジナル名 → 複製ボーン を記録する辞書

    for bone in obj.data.edit_bones:
        if not bone.select:
            continue

        target = bone

        if duplicate:
            # _copyサフィックスを明示的に付与した新しいボーンを作成
            src_name = bone.name + "_copy"
            target = obj.data.edit_bones.new(src_name)
            target.head = bone.head.copy()
            target.tail = bone.tail.copy()
            target.roll = bone.roll
            target.use_connect = False
            target.parent = None
            renamed += 1
            bone_map[bone.name] = target

        if mirror:
            # X軸方向を反転してミラー
            target.head[0] *= -1
            target.tail[0] *= -1

        # コピー時の "_copy" を削除
        name = strip_copy_suffix(target.name)

        if assign_identifier and prefix:
            # 向きをもとに左右識別子を付与（常に target の向きを使う）
            actual_side = determine_side(target)
            identifier = (
                mirror_map.get("left") if actual_side == "L"
                else mirror_map.get("right") if actual_side == "R"
                else ""
            )
            if identifier:
                name = insert_identifier_after_prefix(name, identifier, prefix)

            # デバック用
            print(f"▶ 対象: {bone.name} → new: {target.name} / prefix: {prefix} / side: {actual_side} / ident: {identifier}")

        # 既存の識別子が含まれていれば左右反転
        new_name = apply_name_flip(name, mirror_map["flip"])
        print(f"▶ 名前変換: {name} → {new_name}")  # デバック用
        target.name = new_name

    # 複製したボーンに親子関係を復元する
    if duplicate:
        for orig_name, target in bone_map.items():
            orig_bone = obj.data.edit_bones.get(orig_name)
            if orig_bone and orig_bone.parent:
                parent_name = orig_bone.parent.name
                parent_target = bone_map.get(parent_name)
                if parent_target:
                    target.parent = parent_target

    # 編集完了後に元のモードに戻す（Blenderの仕様に準拠）
    if initial_mode == 'EDIT_ARMATURE':
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        bpy.ops.object.mode_set(mode=initial_mode)

    # デバック用
    print(f"▶ 処理完了: renamed = {renamed}")
    return renamed

# 指定されたパターン名に基づいて置換辞書を返す
def get_pattern_map_from_prefs(context, pattern_label: str, rule_index: Optional[int]) -> dict:
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    for p in prefs.bone_patterns:
        if p.label == pattern_label:

            # 🔧 assign_identifier=False → 全ルールからflipマップ構成
            if rule_index is None:
                flip_dict = {}
                for r in p.rules:
                    if r.left and r.right:
                        flip_dict[r.left] = r.right
                        flip_dict[r.right] = r.left
                return {
                    "left": "",   # 未使用でもキーとして必要
                    "right": "",
                    "flip": flip_dict
                }

            # 🔧 assign_identifier=True → 単一ルールだけ使う
            elif rule_index < len(p.rules):
                r = p.rules[rule_index]
                return {
                    "left": r.left,
                    "right": r.right,
                    "flip": {r.left: r.right, r.right: r.left}
                }

    return {}

# ボーン名に対して左右識別子に基づく置換を適用
def apply_name_flip(name: str, mapping: dict) -> str:
    for a, b in mapping.items():
        if a in name:
            return name.replace(a, b)
    return name

'''
# サフィックス除去関数（_copy式に変えたので使わない）
def strip_duplicate_suffix(name: str) -> str:
    """
    Blenderが自動で付ける `.001`, `.002` などを除去。
    例: 'Head_L.001' → 'Head_L'
    """
    return re.sub(r"\.\d{3}$", "", name)
'''
    
# _copy' で終わっていれば除去
def strip_copy_suffix(name: str) -> str:
    return name[:-5] if name.endswith("_copy") else name

# ボーンの左右側を判定（EDITモード・POSEモード兼用）
def determine_side(bone) -> str:
    """ bone.head.x が + なら 'R'、- なら 'L'、0に近い場合は 'C'（中央扱い）"""
    x = bone.head.x if hasattr(bone, "head") else 0
    if x > 0.0001:
        return "R"
    elif x < -0.0001:
        return "L"
    else:
        return "C"


def insert_identifier_after_prefix(name: str, identifier: str, prefix: str) -> str:
    if name.startswith(prefix):
        rest = name[len(prefix):]

        # アンダースコア重複を抑制
        if prefix.endswith("_") and identifier.startswith("_"):
            identifier = identifier.lstrip("_")
        if identifier.endswith("_") and rest.startswith("_"):
            identifier = identifier.rstrip("_")

        return prefix + identifier + rest
    return name
