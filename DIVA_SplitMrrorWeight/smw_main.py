import os
import json
import bpy
import bmesh
from .smw_preferences import get_json_path

# ボーン識別子の読み込み（JSON）
def load_bone_patterns_to_preferences(prefs):
    path = get_json_path()
    prefs.bone_patterns.clear()

    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        unnamed_count = 1
        for entry in data:
            label = entry.get("label", "").strip()
            if not label:
                label = f"未定義セット{unnamed_count}"
                unnamed_count += 1

            pattern = prefs.bone_patterns.add()
            pattern.label = label

            for rule_data in entry.get("rules", []):
                rule = pattern.rules.add()
                rule.right = rule_data.get("right", "")
                rule.left = rule_data.get("left", "")
    except Exception as e:
        print(f"[DIVA] ⚠ JSON読み込みエラー: {e}")


# ラベルに対応するルールセットを取得
def get_selected_rules(label):
    addon = bpy.context.preferences.addons.get("DIVA_SplitMirrorWeight")
    if not addon:
        return []

    prefs = addon.preferences
    for p in prefs.bone_patterns:
        if p.label.strip() == label:
            return [
                {
                    "right": r.right,
                    "left": r.left,
                    "use_regex": getattr(r, "use_regex", False)
                }
                for r in p.rules
            ]
    return []


# 指定したX方向に頂点があるか調べる
def has_vertices_on_positive_x(obj, threshold=0.001):
    """+X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x > threshold for v in obj.data.vertices)

def has_vertices_on_negative_x(obj, threshold=0.001):
    """-X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x < -threshold for v in obj.data.vertices)

def detect_original_side(obj, threshold=0.001):
    """オブジェクトのオリジナル側を自動判定"""
    if not obj or obj.type != 'MESH':
        return None

    has_left = has_vertices_on_negative_x(obj, threshold)
    has_right = has_vertices_on_positive_x(obj, threshold)

    if has_left and not has_right:
        return 'LEFT'
    elif has_right and not has_left:
        return 'RIGHT'
    else:
        return None  # 両側にメッシュがあるため曖昧（手動選択必須）



# ミラーモディファイアをオフにする処理
def disable_mirror_modifier(obj):
    """対象メッシュのミラーモディファイアをオフにする"""
    for mod in obj.modifiers:
        if mod.type == 'MIRROR':
            mod.show_viewport = False
            mod.show_render = False

# オブジェクト複製＆ミラー適用
def duplicate_and_apply_mirror(obj, delete_side):
    """オリジナルオブジェクトを複製し、複製にミラーモディファイアを適用"""
    bpy.ops.object.select_all(action='DESELECT')  
    obj.select_set(True)
    bpy.ops.object.duplicate()
    mirrored_obj = bpy.context.selected_objects[0]  

    # **複製オブジェクトの名前をカスタムリネーム**
    if delete_side == 'RIGHT':
        mirrored_obj.name = f"{obj.name}_R"
    else:
        mirrored_obj.name = f"{obj.name}_L"

    # ミラーを追加＆適用
    bpy.context.view_layer.objects.active = mirrored_obj
    bpy.ops.object.modifier_add(type='MIRROR')
    mirror_mod = mirrored_obj.modifiers[-1]
    mirror_mod.use_axis[0] = True  

    bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
    return mirrored_obj

# X軸側メッシュ削除
def delete_x_side_mesh(obj, delete_positive_x=True):
    """選択された側のメッシュを削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    for vert in bm.verts:
        if (delete_positive_x and vert.co.x > 0) or (not delete_positive_x and vert.co.x < 0):
            bm.verts.remove(vert)

    bm.to_mesh(mesh)
    bm.free()

# 頂点グループリネーム処理
import re

def rename_symmetric_weight_groups(obj, rules, delete_side):
    """削除する側を考慮し、頂点グループを適切にリネーム（削除→改名を分離）"""
   
    for rule in rules:
        right = rule["right"]
        left = rule["left"]

        # --- Step 1: 削除処理（delete_side に対応する方を消す） ---
        pattern = right if delete_side == 'RIGHT' else left
        for vg in list(obj.vertex_groups):
            name = vg.name
            if pattern in name:
                print(f"[DIVA] 削除: {name}")
                obj.vertex_groups.remove(vg)

        # --- Step 2: リネーム処理（反対側の名前を変換する） ---
        source = left if delete_side == 'RIGHT' else right
        target = right if delete_side == 'RIGHT' else left

        for vg in list(obj.vertex_groups):
            name = vg.name
            if source in name:
                new_name = name.replace(source, target)
                if new_name != name:
                    # 衝突がある場合は先に削除
                    if obj.vertex_groups.get(new_name):
                        print(f"[DIVA] 衝突先削除: {new_name}")
                        obj.vertex_groups.remove(obj.vertex_groups.get(new_name))
                    print(f"[DIVA] リネーム: {name} → {new_name}")
                    vg.name = new_name