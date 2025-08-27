# fop_export.py

import bpy
import os
import sys

from .fop_debug import DEBUG_MODE


# エクスポート用プリセット
DIVA_FBX_EXPORT_PRESET = {
    "use_selection": False,
    "use_visible": False,
    "use_active_collection": False,
    "global_scale": 1.0,
    "apply_unit_scale": True,
    "apply_scale_options": "FBX_SCALE_UNITS",   # FBXスケールを適用
    "use_space_transform": True,
    "bake_space_transform": False,
    # "object_types": {"CAMERA", "ARMATURE", "MESH", "OTHER", "LIGHT", "EMPTY"},    # 全部
    "object_types": {"ARMATURE", "MESH", "EMPTY"},
    "use_mesh_modifiers": True,     # モディファイアーを適用
    "use_mesh_modifiers_render": True,
    "mesh_smooth_type": "OFF",
    "use_subsurf": False,
    "use_mesh_edges": False,
    "use_tspace": False,
    "use_triangles": False,     # 三角面化
    "use_custom_props": False,      # カスタムプロパティ
    "add_leaf_bones": False,        # リーフボーン追加
    "primary_bone_axis": "X",       # プライマリーボーン軸
    "secondary_bone_axis": "Y",     # セカンダリーボーン軸
    "use_armature_deform_only": False,
    "armature_nodetype": "NULL",
    # アニメーションをベイク
    "bake_anim": False,
    "bake_anim_use_all_bones": False,
    "bake_anim_use_nla_strips": False,
    "bake_anim_use_all_actions": False,
    "bake_anim_force_startend_keying": False,
    "bake_anim_step": 1.0,      # サンプリング数
    "bake_anim_simplify_factor": 1.0,       # 簡略化
    "path_mode": "AUTO",        # パスモード（参照パスに使用される方式）
    "embed_textures": False,
    "batch_mode": "OFF",        # バッチモード（アクティブなシーンをファイルへ）
    "use_batch_own_dir": True,      # エクスポートしたファイル毎にディレクトリを追加
    "axis_forward": "-Z",       # -Zが前方
    "axis_up": "Y",     # Yが上
}



if False:   # ファイル名補正+上書き防止関数
    def get_safe_export_path(folder, filename, overwrite_guard=True):
        if not filename.lower().endswith(".fbx"):
            filename += ".fbx"
        base_path = os.path.join(folder, filename)

        # overwrite_guard=False の時はそのまま保存、overwrite_guard=True でも base_path が未使用ならそのまま保存（_01 など付けない）
        if not overwrite_guard or not os.path.exists(base_path):
            return base_path

        base, ext = os.path.splitext(base_path)
        for i in range(1, 100):
            new_path = f"{base}_{i:02d}{ext}"
            if not os.path.exists(new_path):
                if DEBUG_MODE:
                    print(f"[FOP] 上書き防止: {new_path}")
                return new_path

        return base_path  # fallback

# ファイル拡張子補正+自動ナンバリング関数
def get_safe_export_path(folder, filename, overwrite_guard=True):
    if not filename.lower().endswith(".fbx"):
        filename += ".fbx"
    base_path = os.path.join(folder, filename)

    # overwrite_guard=False の時はそのまま保存、overwrite_guard=True の時はナンバリング保存
    if not overwrite_guard:
        return base_path

    base, ext = os.path.splitext(base_path)

    # 常に _01 から始める
    for i in range(1, 100):
        new_path = f"{base}_{i:02d}{ext}"
        if not os.path.exists(new_path):
            if DEBUG_MODE:
                print(f"[FOP] 上書き防止: {new_path}")
            return new_path

    return base_path  # fallback









# --- マーカーツール連携 -------------------------------------------------------------------------------------------------------------
MARKER_ADDON_NAME = "DIVA_MarkerManagementTools"


# 復元ポイントの記録
def store_restore_point(context):
    bpy.ops.ed.undo_push(message="復元ポイント: Export準備前")

# 復元ポイントへ戻す
def restore_to_point(context, data):
    bpy.ops.ed.undo()


# run_marker_tool() を呼び出す
def try_run_marker_tool(context):
    addon_name = "DIVA_MarkerManagementTools"
    if addon_name not in bpy.context.preferences.addons:
        if DEBUG_MODE:
            print(f"[FOP] マーカー管理ツールが有効化されていないためスキップ: {addon_name}")
        return

    try:
        # アドオンのモジュールを取得
        marker_module = sys.modules.get("DIVA_MarkerManagementTools.mrk_core")
        if not marker_module:
            if DEBUG_MODE:
                print(f"[FOP] モジュール未ロード: DIVA_MarkerManagementTools.mrk_core")
            return

        # 関数を取得して呼び出し
        run_func = getattr(marker_module, "run_marker_tool", None)
        if callable(run_func):
            run_func(context)
        else:
            if DEBUG_MODE:
                print(f"[FOP] run_marker_tool が見つからないか呼び出し不可")
    except Exception as e:
        print(f"[FOP] run_marker_tool 呼び出し中にエラー: {e}")