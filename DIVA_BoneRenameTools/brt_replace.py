# brt_replace.py（旧rename_rules.py）

import bpy
import re
from os.path import commonprefix

from bpy.app.translations import pgettext as _

from .brt_debug import DEBUG_MODE   # デバッグ用

# 重複識別子の削除
def strip_number_suffix(name: str) -> str:
    return re.sub(r"\.\d{3,}$", "", name)

# _copy（アドオン付与+.001含む）除去
def strip_copy_suffix(name: str) -> str:
    return re.sub(r"_copy(?:\.\d{3,})?$", "", name)


# 最後の処理として末尾の .001 などを除去（安全に）
def sanitize_duplicate_suffixes(bones):
    existing = {b.name for b in bones}
    for bone in bones:
        cleaned = strip_number_suffix(bone.name)    # bone.nameから重複識別子削除（対象がなくてもcleandに代入）
        cleaned = strip_copy_suffix(cleaned)  # 上記結果のcleandからcopy系を更に除去

        # すでに同名が存在していない場合のみ再設定
        if cleaned != bone.name and cleaned not in existing:
            try:
                bone.name = cleaned
                existing.add(cleaned)
            except Exception as e:
                if DEBUG_MODE:
                    print(f"⚠ Rename failed: {bone.name} → {cleaned} ({e})")

def replace_bone_names_by_rule(context, source, target):
    """選択中のボーン名から source を target に置き換え（部分一致）"""
    obj = context.object
    if not obj or obj.type != 'ARMATURE':
        return False, False, _("Please select an armature")

    # モード別に選択されたボーンのみを取得
    if context.mode == 'POSE':
        selected_bones = [b for b in obj.data.bones if b.select]
    elif context.mode == 'EDIT_ARMATURE':
        selected_bones = [b for b in obj.data.edit_bones if b.select]
    else:
        return False, False, _("Supported modes are Pose and Edit")

    matched = 0
    total_selected = len(selected_bones)

    for bone in selected_bones:
        if DEBUG_MODE:
            print(f"Checking: {bone.name} → contains '{source}'? {'YES' if source in bone.name else 'NO'}")
        if source in bone.name:
            new_name = bone.name.replace(source, target)
            if context.scene.brt_remove_number_suffix:
                new_name = strip_number_suffix(new_name)
            bone.name = new_name
            matched += 1

    # 実際に置き換えが発生したときのみ重複識別子を除去
    if matched > 0 and context.scene.brt_remove_number_suffix:
        sanitize_duplicate_suffixes(selected_bones)

    if matched == 0:
        return False, False, _("Please check the settings of the selected bone name and the name before replacement")    # 選択したボーン名と置換前の名前の設定を確認してください
    elif matched < total_selected:
        return True, True, _("Some bones could not be replaced. Please check the bone name")    # 一部のボーンが置き換えできませんでした。ボーン名を確認してください
    else:
        return True, False, ""



def detect_common_prefix(bones, suffix_enum=None, rule_enum=None):
    """複数ボーン名の共通部分を抽出（簡易版）"""
    if not bones:
        return ""
    cleaned_names = [clean_name(b.name) for b in bones]
    return commonprefix(cleaned_names)

def clean_name(name):
    """番号サフィックスやサフィックス表現を正規化"""
    base = name.split(".")[0]
    for suffix in ["_wj", "wj", "_wj_ex", "wj_ex"]:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    parts = base.split("_")
    if parts and parts[-1].isdigit() and len(parts[-1]) in (2, 3):
        parts.pop()
    return "_".join(parts)