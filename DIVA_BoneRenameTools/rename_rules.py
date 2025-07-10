import bpy
import re
from os.path import commonprefix

def strip_number_suffix(name: str) -> str:
    """'.001' のような複製識別子を除去する"""
    return re.sub(r"\.\d{3}$", "", name)

def replace_bone_names_by_rule(context, source, target):
    """選択中のボーン名から source を target に置き換え（部分一致）"""
    obj = context.object
    if not obj or obj.type != 'ARMATURE':
        return False, False, "アーマチュアを選択してください"

    # モード別に選択されたボーンのみを取得
    if context.mode == 'POSE':
        selected_bones = [b for b in obj.data.bones if b.select]
    elif context.mode == 'EDIT_ARMATURE':
        selected_bones = [b for b in obj.data.edit_bones if b.select]
    else:
        return False, False, "対応モードは Pose または Edit モードです"

    matched = 0
    total_selected = len(selected_bones)

    for bone in selected_bones:
        print(f"Checking: {bone.name} → contains '{source}'? {'YES' if source in bone.name else 'NO'}")
        if source in bone.name:
            new_name = bone.name.replace(source, target)
            if context.scene.brt_remove_number_suffix:
                new_name = strip_number_suffix(new_name)
            bone.name = new_name
            matched += 1

    if matched == 0:
        return False, False, "選択したボーン名と置換前の名前の設定を確認してください"
    elif matched < total_selected:
        return True, True, "一部置き換えできませんでした。ボーン名を確認してください"
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