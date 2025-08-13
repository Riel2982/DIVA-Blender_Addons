# mwr_sub.py

import bpy
from bpy.app.translations import pgettext as _

from .mwr_debug import DEBUG_MODE   # デバッグ用

# 多言語対応モディファイアラベル辞書
MODIFIER_LABELS = {
    'SUBSURF': _("Subdivision Surface"),        # サブディビジョンサーフェス
    'MIRROR': _("Mirror"),                      # ミラー
    'LATTICE': _("Lattice"),                    # ラティス
    'SHRINKWRAP': _("Shrinkwrap"),              # シュリンクラップ
    'DATA_TRANSFER': _("Data Transfer"),        # データ転送
    'MESH_DEFORM': _("Mesh Deform"),            # メッシュ変形
    'VERTEX_WEIGHT_EDIT': _("Vertex Weight Edit"),      # 頂点ウェイト編集
    'VERTEX_WEIGHT_MIX': _("Vertex Weight Mix"),        # 頂点ウェイト合成
    'VERTEX_WEIGHT_PROXIMITY': _("Vertex Weight Proximity"),  # 頂点ウェイト（近接）
    'ARMATURE': _("Armature"),                  # アーマチュア
    'SOLIDIFY': _("Solidify"),                  # ソリッド化（厚み付け）
    'DECIMATE': _("Decimate"),                  # ディサメート（ポリゴン簡略化）
    'BOOLEAN': _("Boolean"),                    # ブーリアン
}

_last_applied_modifiers = None

# 特定のモディファイアを適用する（対象は順番維持）
def apply_specific_modifiers(obj, target_types=None):
    """
    指定された種類のモディファイアを順に適用する。
    Blender内部で順序が重要なため、リストをコピーしてループ。
    オフになっている（非表示の）モディファイアは無視される。
    適用されたモディファイアの種類をリストで返す。
    """
    global _last_applied_modifiers

    # 適用対象のモディファイア
    if target_types is None:
        target_types = {
            'LATTICE',      # ラティス
            'DATA_TRANSFER',    # データ転送
            'SHRINKWRAP',       # シュリンクラップ
            'MESH_DEFORM',      # メッシュ変形
            'VERTEX_WEIGHT_EDIT',     # 頂点ウエイト編集
            'VERTEX_WEIGHT_MIX',      # 頂点ウエイト合成
            'VERTEX_WEIGHT_PROXIMITY',        # 頂点ウエイト近接
            # 'BOOLEAN',        # ブーリアン
        }

    bpy.context.view_layer.objects.active = obj  # アクティブ化必須
    applied = []  # 適用されたモディファイアの種類を記録

    for mod in list(obj.modifiers):  # 安全なループのためにコピー      
        if DEBUG_MODE:
            print(f"[DEBUG] Modifier {mod.name} show_viewport={mod.show_viewport}")     
        def safe_str(s):
            try:
                if isinstance(s, bytes):
                    return s.decode('utf-8', errors='replace')  # 不正バイトは � に置換
                return str(s)
            except Exception as e:
                try:
                    return repr(s)[1:-1]  # クォート除去した repr 表示
                except Exception:
                    return f"<decode error: {e}>"
                
        if mod.type in target_types:
            # 無効（オフ）なモディファイアはスキップ
            if not mod.show_viewport:
                if DEBUG_MODE:
                    print(f"[ModifierApply] {safe_str(obj.name)}: Skipped modifier of type {mod.type} (disabled in viewport)")
                continue

            # 有効なモディファイアを適用
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
                applied.append(mod.type)  # 適用されたモディファイアの種類を記録
                if DEBUG_MODE:
                    print(f"[ModifierApply] Applied modifier of type {mod.type}")
            except Exception as e:
                if DEBUG_MODE:
                    print(f"[ModifierApply] Failed to apply modifier of type {mod.type}: {e}")

    if DEBUG_MODE:
        print(f"[DEBUG] apply_specific_modifiers: applied list = {applied}")

    _last_applied_modifiers = applied  # 結果を保存

    return applied  # 適用されたモディファイアの種類を呼び出し元に返す


                    
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
        'SOLIDIFY',                # Solidify（ソリッド化／厚み付け）
        'DECIMATE',                # Decimate（デシメート／ポリゴン簡略化）
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
# 'SOLIDIFY'                : Solidify（ソリッド化／厚み付け）
# 'DECIMATE'                : Decimate（デシメート／ポリゴン簡略化）
# 'BOOLEAN'                 : Boolean（ブーリアン）

