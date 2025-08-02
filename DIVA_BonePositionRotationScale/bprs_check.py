# bprs_check.py

import bpy
from bpy.app.translations import pgettext as _
from . import DivaBonePositionRotationScale
# from . bprs_types import bprs_last_checked_armature

def get_bone_data_map():
    """文字列出力された補正ボーン情報をボーン名ごとの辞書に変換する"""
    raw_text = DivaBonePositionRotationScale.get_bone_data()
    blocks = raw_text.strip().split("\n\n")
    result = {}
    for block in blocks:
        lines = block.strip().split("\n")
        if not lines:
            continue
        bone_name = lines[0].strip()
        result[bone_name] = lines  # 補正情報の全行を格納
    return result


def parse_bone_data_string(data_string):
    """補正済みボーン情報の文字列を、ボーン名をキーとした行リスト辞書に変換する"""

    result = {}
    if not data_string:
        return result

    # ボーンごとのブロックを2行以上で構成（1行目がボーン名）
    for block in data_string.strip().split("\n\n"):
        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
        if len(lines) < 2:
            continue  # ボーン名と少なくとも1つの情報が必要

        bone_name = lines[0]
        result[bone_name] = lines  # 1行目:ボーン名, 2行目以降:情報リスト

    return result


def collect_correction_data(scene, armature, data_text):
    """表示対象ボーンから補正ラベルと値ペアを収集"""
    bone_data_map = parse_bone_data_string(data_text)
    result = []

    for item in scene.bprs_bones_data:
        if not item.show_info:
            continue

        bone_name = item.name
        info_lines = bone_data_map.get(bone_name)
        if not info_lines or len(info_lines) < 2:
            continue

        bone = armature.data.bones.get(bone_name)
        bone_length = bone.length if bone else 0.0

        # ラベルと値の整形
        entries = []
        for line in info_lines[1:]:
            parts = line.lstrip().split(": ", 1)
            if len(parts) == 2:
                label, value = parts
            else:
                label, value = "?", "[未取得]"
            entries.append((label.strip(), value.strip()))

        entries.append(("Length", format_number(bone_length)))
        result.append((bone_name, entries))

    return result

def format_number(value):
    """0.390000 → 0.39 のように末尾ゼロを省いた文字列に変換"""
    return ('%.6f' % float(value)).rstrip('0').rstrip('.') if value != 0 else '0'


def set_checked_armature_as_active(context):
    scene = context.scene
    checked_name = getattr(scene, "bprs_last_checked_armature", "")
    checked_obj = bpy.data.objects.get(checked_name) if checked_name else None

    if checked_obj and checked_obj.type == 'ARMATURE':
        # アクティブが違う or モードが違う場合は強制切り替え
        current_obj = context.active_object
        needs_switch = current_obj != checked_obj or checked_obj.mode != 'EDIT'

        if needs_switch:
            # 切り替え（.select_set(True) は不要だが入れても可）
            bpy.context.view_layer.objects.active = checked_obj
            bpy.ops.object.mode_set(mode='EDIT')
        return checked_obj

    return None

def set_checked_armature_as_active(context, operator=None):
    scene = context.scene
    checked_name = getattr(scene, "bprs_last_checked_armature", "")
    checked_obj = bpy.data.objects.get(checked_name) if checked_name else None

    if checked_obj and checked_obj.type == 'ARMATURE':
        # アクティブが違う or モードが違う場合は強制切り替え
        current_obj = context.active_object
        switched = False

        if current_obj != checked_obj:
            bpy.context.view_layer.objects.active = checked_obj
            switched = True

        if checked_obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
            switched = True

        # REPORTを表示（オペレーターが渡されていれば）
        if switched and operator:
            operator.report(
                {'INFO'},_("Editing armature switched to: {name}").format(name=checked_obj.name))

        return checked_obj

    return None