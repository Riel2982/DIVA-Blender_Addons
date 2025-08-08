# mwr_reflector.py

import bpy
from typing import Optional
from .mwr_json import (
    get_json_path,
    load_json_data,
    save_json_data,
    DEFAULT_BONE_PATTERN,
    get_bone_pattern_items,
    get_rule_items,
)

from .mwr_sub import (
    apply_specific_modifiers,
)

from .mwr_debug import DEBUG_MODE   # デバッグ用


# ミラーモディファイアをオフにする処理
def disable_mirror_modifier(obj):
    """対象メッシュのミラーモディファイアをオフにする"""
    for mod in obj.modifiers:
        if mod.type == 'MIRROR':
            mod.show_viewport = False
            mod.show_render = False


# オブジェクト複製＆ミラー適用
def duplicate_and_apply_mirror(obj):
    """オリジナルオブジェクトを複製し、複製にミラーモディファイアを適用"""
    # オリジナルを複製
    bpy.ops.object.select_all(action='DESELECT')  
    obj.select_set(True)
    bpy.ops.object.duplicate()
    mirrored_obj = bpy.context.selected_objects[0]  

    # **複製オブジェクトの名前をカスタムリネーム**
    mirrored_obj.name = f"{obj.name}_Mirror"  # ← 一貫した命名に統一

    # 複製した方に各種モディファイア適用
    apply_specific_modifiers(mirrored_obj)      

    # ミラーを追加＆適用
    bpy.context.view_layer.objects.active = mirrored_obj
    bpy.ops.object.modifier_add(type='MIRROR')
    mirror_mod = mirrored_obj.modifiers[-1]
    mirror_mod.use_axis[0] = True  

    # ✅ 頂点マージを無効化
    mirror_mod.use_mirror_merge = False
    mirror_mod.merge_threshold = 0.0

    bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
    return mirrored_obj



# 頂点削除処理（インデックスベース）
def delete_vertices_by_index(obj, index_list):
    """
    指定された頂点インデックス群に基づいて、対象オブジェクトの頂点を削除する。
    完全にインデックス情報のみで判定し、座標（X軸など）や識別名には一切依存しない。
    選択操作は Edit モード内で Blender の標準オペレータを利用して安全に実行される。
    """
    mesh = obj.data

    # Step 1: Editモードで選択解除（安全初期化）
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Step 2: 対象インデックスだけ選択状態にする
    for idx in index_list:
        mesh.vertices[idx].select = True

    # Step 3: 選択頂点を削除
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')


# 指定されたパターン名に基づいて置換辞書を返す
def get_pattern_map_from_prefs(context, pattern_label: str, rule_index: Optional[int]) -> dict:
    prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
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


            elif rule_index < len(p.rules):
                r = p.rules[rule_index]

                # ★ flip辞書は全ルールから構成する（付与は指定の left/right のみ）
                full_flip = {}
                for rr in p.rules:
                    if rr.left and rr.right:
                        full_flip[rr.left] = rr.right
                        full_flip[rr.right] = rr.left

                return {
                    "left": r.left,       # 付与にはこのleftを使う
                    "right": r.right,     # 付与にはこのrightを使う
                    "flip": full_flip     # 反転には全識別子を使う
                }

            '''
            # 🔧 assign_identifier=True → 単一ルールだけ使う
            elif rule_index < len(p.rules):
                r = p.rules[rule_index]
                return {
                    "left": r.left,
                    "right": r.right,
                    "flip": {r.left: r.right, r.right: r.left}
                }
            '''

    return {}

# 双方向識別子変換
def apply_name_flip(name, flip_map):
    for left, right in flip_map.items():
        if right in name:
            return name.replace(right, left)
        elif left in name:
            return name.replace(left, right)
    return name  # flip対象なし



# 原点越えミラー処理：複製・削除・グループ整備の統合フロー
def process_origin_overlap(obj, pattern_map, duplicate_and_mirror, flip_map, merge_center_vertices=False):
    marge_center_vertices = False
    """
    原点越え対象メッシュを反転し、頂点グループ名をルールに基づいて整備する。
    一時状態は _MirrorL/_MirrorR の接尾辞で表し、flip_map により左右名称を反転。
    """

    # Step 1: 元頂点インデックスを記録
    disable_mirror_modifier(obj)
    original_indices = [v.index for v in obj.data.vertices]

    # Step 2: Mirror処理（複製あり／なし）
    if duplicate_and_mirror:    # オブジェクトを複製する
        mirrored_obj = duplicate_and_apply_mirror(obj)
    else:
        apply_specific_modifiers(obj)        # オリジナルに対して各種モディファイア適用
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='MIRROR')
        mirror_mod = obj.modifiers[-1]
        mirror_mod.use_axis[0] = True
        # ✅ 頂点マージを無効化
        mirror_mod.use_mirror_merge = False
        mirror_mod.merge_threshold = 0.0
        bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
        mirrored_obj = obj

    # Step 3: 元側頂点を削除（インデックス指定）
    delete_vertices_by_index(mirrored_obj, original_indices)

    # Step 4: 一時接尾辞 "_MirrorL"/"_MirrorR" を付与（識別子に基づく）
    for vg in mirrored_obj.vertex_groups:
        for rule in pattern_map:
            if rule["left"] in vg.name:
                vg.name += "_MirrorL"
                break
            elif rule["right"] in vg.name:
                vg.name += "_MirrorR"
                break

    # Step 5: flip_map に従い左右識別子を反転し、一時接尾辞を除去
    for vg in mirrored_obj.vertex_groups:
        if vg.name.endswith("_MirrorL"):
            base = vg.name[:-len("_MirrorL")]
            vg.name = apply_name_flip(base, flip_map)
        elif vg.name.endswith("_MirrorR"):
            base = vg.name[:-len("_MirrorR")]
            vg.name = apply_name_flip(base, flip_map)

    # Step 6: 完了ログ出力
    if DEBUG_MODE:
        print(f"[ReflectMeshWeights] 完了: {mirrored_obj.name}")
    return mirrored_obj