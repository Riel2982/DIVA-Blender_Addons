# mwr_sub.py

import bpy

from .mwr_debug import DEBUG_MODE   # デバッグ用


# 特定のモディファイアを適用する（対象は順番維持）
def apply_specific_modifiers(obj, target_types=None):
    """
    指定された種類のモディファイアを順に適用する。
    Blender内部で順序が重要なため、リストをコピーしてループ。
    オフになっている（非表示の）モディファイアは無視される。
    """
    # 適用対象のモディファイア
    if target_types is None:
        target_types = {
            'LATTICE',
            'DATA_TRANSFER',
            'SHRINKWRAP',
            'MESH_DEFORM',
            'VERTEX_WEIGHT_EDIT',
            'VERTEX_WEIGHT_MIX',
            'VERTEX_WEIGHT_PROXIMITY',
        }

    bpy.context.view_layer.objects.active = obj  # アクティブ化必須

    for mod in list(obj.modifiers):  # 安全なループのためにコピー
        if mod.type in target_types:

            # ❌ 無効（オフ）なモディファイアはスキップ
            if not mod.show_viewport:
                if DEBUG_MODE:
                    print(f"[ModifierApply] Skipped {mod.name} ({mod.type}) - disabled in viewport")
                continue

            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
                if DEBUG_MODE:
                    print(f"[ModifierApply] {obj.name}: {mod.name} ({mod.type}) applied")
            except Exception as e:
                print(f"[ModifierApply] Failed to apply {mod.name}: {e}")

if False:
    # Blender モディファイアタイプ一覧（type 値メモ）
    # ※ apply_specific_modifiers() で使用可能な値

    modifier_types = {
        'SUBSURF',                 # Subdivision Surface（サブディビジョンサーフェス）
        'MIRROR',                  # Mirror（ミラー）
        'LATTICE',                 # Lattice（ラティス）
        'SHRINKWRAP',              # Shrinkwrap（シュリンクラップ）
        'DATA_TRANSFER',           # Data Transfer（データ転送）
        'MESH_DEFORM',             # Mesh Deform（メッシュ変形）
        'VERTEX_WEIGHT_EDIT',      # Vertex Weight Edit（頂点ウェイト編集）
        'VERTEX_WEIGHT_MIX',       # Vertex Weight Mix（頂点ウェイト合成）
        'VERTEX_WEIGHT_PROXIMITY', # Vertex Weight Proximity（頂点ウェイト近接）
        'ARMATURE',                # Armature（アーマチュア）
        'SOLIDIFY',                # Solidify（ソリディファイ／厚み付け）
        'DECIMATE',                # Decimate（ディサメート／ポリゴン簡略化）
        'BOOLEAN',                 # Boolean（ブーリアン）
    }


# Blender モディファイアタイプ一覧（type 値メモ）
# ※ apply_specific_modifiers() で使用可能な値

# 'SUBSURF'                 : Subdivision Surface（サブディビジョンサーフェス）
# 'MIRROR'                  : Mirror（ミラー）
# 'LATTICE'                 : Lattice（ラティス）
# 'SHRINKWRAP'              : Shrinkwrap（シュリンクラップ）
# 'DATA_TRANSFER'           : Data Transfer（データ転送）
# 'MESH_DEFORM'             : Mesh Deform（メッシュ変形）
# 'VERTEX_WEIGHT_EDIT'      : Vertex Weight Edit（頂点ウェイト編集）
# 'VERTEX_WEIGHT_MIX'       : Vertex Weight Mix（頂点ウェイト合成）
# 'VERTEX_WEIGHT_PROXIMITY' : Vertex Weight Proximity（頂点ウェイト近接）
# 'ARMATURE'                : Armature（アーマチュア）
# 'SOLIDIFY'                : Solidify（ソリディファイ／厚み付け）
# 'DECIMATE'                : Decimate（ディサメート／ポリゴン簡略化）
# 'BOOLEAN'                 : Boolean（ブーリアン）

