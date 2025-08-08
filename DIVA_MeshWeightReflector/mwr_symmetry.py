# mwr_symmetry.py

import bpy
from typing import Optional
from .mwr_json import (
    get_json_path,
    load_json_data,
    save_json_data,
    DEFAULT_BONE_PATTERN,
    get_bone_pattern_items,
    get_rule_items,
    get_selected_rules,
)
from .mwr_sub import (
    apply_specific_modifiers,
)

from .mwr_debug import DEBUG_MODE   # デバッグ用

def duplicate_and_apply_mirror_symmetry(obj, merge_center_vertices=False, merge_threshold=0.001):
    """
    指定オブジェクトを複製し、Mirror モディファイアを追加して適用。
    merge_threshold は Blender のワールド空間ベースで処理される。
    """
    # オリジナルを複製
    bpy.ops.object.select_all(action='DESELECT')  
    obj.select_set(True)
    bpy.ops.object.duplicate()
    mirrored_obj = bpy.context.selected_objects[0]

    # **複製オブジェクトの名前をカスタムリネーム**
    mirrored_obj.name = f"{obj.name}_Mirror"

    # 複製した方に各種モディファイア適用
    apply_specific_modifiers(mirrored_obj) 

    # ミラーを追加＆適用
    bpy.context.view_layer.objects.active = mirrored_obj
    bpy.ops.object.modifier_add(type='MIRROR')
    mirror_mod = mirrored_obj.modifiers[-1]

    # ✅ 頂点マージ設定
    mirror_mod.use_axis[0] = True
    mirror_mod.use_mirror_merge = merge_center_vertices
    if merge_center_vertices:
        mirror_mod.merge_threshold = merge_threshold
        if DEBUG_MODE:
            print(f"[SymmetrizeMeshWeights] Mirror Merge 有効化 → merge_threshold = {merge_threshold:.6f}")
    else:
        mirror_mod.merge_threshold = 0.0
        if DEBUG_MODE:
            print("[SymmetrizeMeshWeights] Mirror Merge 無効化")

    bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
    return mirrored_obj

def compute_scaled_merge_threshold(obj, base_threshold):
    """merge_threshold を Blender の仕様に合わせて補正（スケールを乗算）"""
    scale_x = obj.matrix_world.to_scale().x
    if scale_x == 0:
        if DEBUG_MODE:
            print(f"[SymmetrizeMeshWeights] ⚠ 無効なスケールX値: {scale_x} → 閾値補正をスキップ")
        return base_threshold
    return base_threshold * scale_x

def are_vertices_mergeable(obj, v1, v2, merge_threshold):
    """
    Mirror Modifier の仕様に基づいて、X軸方向の差のみでマージ可能かを判定する。
    - obj: 対象オブジェクト（スケールやワールド座標の取得に必要）
    - v1, v2: 対象頂点（bpy.types.MeshVertex）
    - merge_threshold: Mirror モディファイアのマージ距離閾値（通常 0.001 など）
    """
    # ワールド座標に変換して X 座標を取得
    x1 = (obj.matrix_world @ v1.co).x
    x2 = (obj.matrix_world @ v2.co).x

    # X軸方向の差を比較（他軸は無視）
    diff = abs(x1 - x2)

    # 閾値以下なら Mirror に準じたマージ対象とみなす
    return diff <= merge_threshold



# 指定したX方向に頂点があるか調べる
def has_vertices_on_positive_x(obj, threshold=0.001):
    """+X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x > threshold for v in obj.data.vertices)

def has_vertices_on_negative_x(obj, threshold=0.001):
    """-X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x < -threshold for v in obj.data.vertices)

def detect_original_side(obj, threshold=0.001):
    """X軸位置に基づいてオリジナル側を判定（診断ログ付き）"""
    left_count = 0
    right_count = 0

    for v in obj.data.vertices:
        x = (obj.matrix_world @ v.co).x
        if x > threshold:         # もとの RIGHT 側の定義
            left_count += 1       # ← 実際には左として扱う
        elif x < -threshold:
            right_count += 1

    if DEBUG_MODE:
        print(f"[SymmetrizeMeshWeights] 左側頂点数: {left_count}, 右側頂点数: {right_count}")

    if left_count > right_count:
        return 'LEFT'
    elif right_count > left_count:
        return 'RIGHT'
    else:
        return None  # 両側均等または中心に集中

def is_vertex_on_side(obj, vertex, side, threshold=0.001):
    """頂点が指定方向にあるかを判定（判定方向を detect_original_side() に合わせて反転）"""
    x = (obj.matrix_world @ vertex.co).x
    return (x > threshold and side == 'LEFT') or (x < -threshold and side == 'RIGHT')


def rename_symmetric_weight_groups(obj, rules, original_side, threshold=0.001):
    """オリジナル側の頂点グループから反対側を除外し、対側の頂点のみを含むグループを複製生成"""

    for rule in rules:
        left_id = rule["left"]
        right_id = rule["right"]

        if original_side == 'LEFT':
            source_id, target_id = left_id, right_id
            source_side, target_side = 'LEFT', 'RIGHT'
        elif original_side == 'RIGHT':
            source_id, target_id = right_id, left_id
            source_side, target_side = 'RIGHT', 'LEFT'
        else:
            continue

        for vg in list(obj.vertex_groups):
            name = vg.name
            if source_id not in name:
                continue

            new_name = name.replace(source_id, target_id)
            if DEBUG_MODE:
                print(f"[SymmetrizeMeshWeights] 複製対象検出: {name} → {new_name}")

            # 複製先が既にあるなら削除
            if obj.vertex_groups.get(new_name):
                obj.vertex_groups.remove(obj.vertex_groups.get(new_name))
                if DEBUG_MODE:
                    print(f"[SymmetrizeMeshWeights] 既存グループ削除: {new_name}")

            # 新しいグループ生成
            new_vg = obj.vertex_groups.new(name=new_name)
            for v in obj.data.vertices:
                if is_vertex_on_side(obj, v, target_side, threshold):
                    try:
                        weight = vg.weight(v.index)
                        new_vg.add([v.index], weight, 'REPLACE')
                    except RuntimeError:
                        continue

            if DEBUG_MODE:
                print(f"[SymmetrizeMeshWeights] ミラーグループ生成完了: {new_name}")

            # オリジナルグループから反対側頂点を除去
            for v in obj.data.vertices:
                if not is_vertex_on_side(obj, v, source_side, threshold):
                    vg.remove([v.index])

            if DEBUG_MODE:
                print(f"[SymmetrizeMeshWeights] オリジナルグループフィルタ適用完了: {name}")



def detect_group_side(name, rules):
    """頂点グループ名から左右の識別子ルールに従って所属側を判定"""
    for rule in rules:
        if rule.get("use_regex"):
            continue  # 正規表現は今は除外

        right_id = rule["right"]
        left_id = rule["left"]

        if right_id and right_id in name:
            return "RIGHT"
        elif left_id and left_id in name:
            return "LEFT"

    return None  # どちらにも属していない場合


def process_symmetrize(obj, pattern_label, duplicate_and_mirror, flip_map, merge_center_vertices=False, merge_threshold=0.001, threshold=0.001):
    """メッシュの対称化処理全体（識別子ラベルからルール取得を含む）"""

    # Step 0: ラベルから識別子ルールを取得
    rules = get_selected_rules(pattern_label)
    if not rules or not isinstance(rules, list):
        if DEBUG_MODE:
            print(f"[SymmetrizeMeshWeights] ⚠ 有効な識別子ルールが未定義: '{pattern_label}' → 処理停止")
        return None

    # ✅ Step 1: オリジナル側判定（ミラー前で空間分布確認）
    original_side = detect_original_side(obj, threshold)
    if DEBUG_MODE:
        print(f"[SymmetrizeMeshWeights] 判定されたオリジナル側: {original_side}")

    # Step 2: Mirror処理（複製あり／なし）
    if duplicate_and_mirror:
        mirrored_obj = duplicate_and_apply_mirror_symmetry(
            obj,
            merge_center_vertices=merge_center_vertices,
            merge_threshold=merge_threshold
        )

    else:
        apply_specific_modifiers(obj)        # オリジナルに対してモディファイア適用
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='MIRROR')
        mirror_mod = obj.modifiers[-1]
        mirror_mod.use_axis[0] = True
        mirror_mod.use_mirror_merge = merge_center_vertices

        if merge_center_vertices:
            mirror_mod.merge_threshold = merge_threshold
            if DEBUG_MODE:
                print(f"[SymmetrizeMeshWeights] Mirror Merge 有効化 → merge_threshold = {merge_threshold:.6f}")
        else:
            mirror_mod.merge_threshold = 0.0
            if DEBUG_MODE:
                print("[SymmetrizeMeshWeights] Mirror Merge 無効化")

        bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
        mirrored_obj = obj

    # Step 3: 頂点グループ対称化（Mirror挙動に依存しない処理）
    if original_side in ('LEFT', 'RIGHT'):
        rename_symmetric_weight_groups(
            mirrored_obj,
            rules=rules,
            original_side=original_side,
            threshold=threshold
        )
    else:
        if DEBUG_MODE:
            print("[SymmetrizeMeshWeights] オリジナル側が不明（両側に頂点がある）ため、リネーム処理をスキップ")

    # Step 4: 完了ログ出力
    if DEBUG_MODE:
        print(f"[SymmetrizeMeshWeights] 完了: {mirrored_obj.name}")
    return mirrored_obj