# fop_import.py

import bpy
import os
import re

from .fop_debug import DEBUG_MODE   # デバッグ用


# ベース名抽出関数
def extract_base_name(filepath):
    filename = os.path.basename(filepath)
    name_without_ext = os.path.splitext(filename)[0]    # 拡張子を除外
    # base_name = name_without_ext.split("_")[0]    # _の手前撫でを抽出

    # mikitm001_obj → mikitm001 抽出
    match = re.search(r"(.*?itm\d+)", name_without_ext)
    if match:
        return match.group(1)
    else:       # 拡張子を除外しただけで処理
        return name_without_ext


# Impot名処理関数
def apply_import_naming(obj_list, base_name, create_collection=True):
    if create_collection:   # コレクションを使用する場合
        # アクティブコレクションを基準に新しいコレクションを作る
        parent_collection = bpy.context.view_layer.active_layer_collection.collection
        new_collection = bpy.data.collections.new(base_name)
        parent_collection.children.link(new_collection)

        for obj in obj_list:
            # まず全所属コレクションから外す
            for coll in obj.users_collection:
                coll.objects.unlink(obj)
            # 新コレクションに入れる
            new_collection.objects.link(obj)

    # オブジェクトアーマチュア名
    for obj in obj_list:
        if obj.type == 'ARMATURE':
            obj.name = base_name
            obj.data.name = base_name


if False: # 新コレクションはScene Collectionに作成されるが、アーマチュアは新コレクション・オブジェクトはアクティブコレクションに配置されてしまう
    def apply_import_naming(obj_list, base_name, create_collection=True):
        if create_collection:   # コレクションを使用する場合
            new_collection = bpy.data.collections.new(base_name)
            bpy.context.scene.collection.children.link(new_collection)

            for obj in obj_list:
                new_collection.objects.link(obj)
                bpy.context.scene.collection.objects.unlink(obj)

        # オブジェクトアーマチュア名
        for obj in obj_list:
            if obj.type == 'ARMATURE':
                obj.name = base_name

        # データアーマチュア名
        for obj in obj_list:
            if obj.type == 'ARMATURE':
                obj.name = base_name
                obj.data.name = base_name



# インポート用プリセット
DIVA_FBX_IMPORT_PRESET = {
    "use_manual_orientation": False,
    "global_scale": 1.0,
    "bake_space_transform": False,
    "use_custom_normals": True,     # カスタム法線
    "use_image_search": True,
    "use_alpha_decals": False,
    "decal_offset": 0.0,
    "use_anim": False,   # アニメーション
    "anim_offset": 1.0,     # アニメのオフセット
    "use_subsurf": False,
    "use_custom_props": True,   # カスタムプロパティ
    "use_custom_props_enum_as_string": True,
    "ignore_leaf_bones": False,     # リーフボーンを無視
    "force_connect_children": False,    # 子を強制的に接続
    "automatic_bone_orientation": False,    # ボーン方向の自動整列
    "primary_bone_axis": "X",   # プライマリーボーン軸
    "secondary_bone_axis": "Y",     # セカンダリーボーン軸
    "use_prepost_rot": True,
    "axis_forward": "-Z",       # -Zが前方
    "axis_up": "Y",     # Yが上
}


# リーフボーン検出
def find_leaf_end_bones(armature_obj):
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')
    armature = armature_obj.data
    edit_bones = armature.edit_bones

    leaf_bones = []

    for bone in edit_bones:
        if bone.name.endswith("_end") and len(bone.children) == 0:
            current = bone
            while current and current.name.endswith("_end"):
                leaf_bones.append(current)
                current = current.parent

    return list(set(leaf_bones))  # 重複除去

# ビューポートの名前表示をON
def set_bone_name_display(armature_obj, visible=True):
    armature_obj.data.show_names = visible

# 検出ボーンを選択
def delete_leaf_bones(bone_names):
    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        return

    edit_bones = obj.data.edit_bones

    # 選択状態に依存せず、明示的に名前指定で削除する
    for name in bone_names:
        if name in edit_bones:
            edit_bones.remove(edit_bones[name])

# 検出ボーンを削除
def select_leaf_bones(bones):
    # すべてのボーンの選択を解除(前提状態を明示的にリセットすることで、誤選択や副作用を防ぐ)
    for bone in bones[0].id_data.edit_bones:
        bone.select = False

    # 対象ボーンのみ選択
    # UI上で削除対象を明示するためのフィードバック
    for bone in bones:
        bone.select = True

# 遅延実行
def delayed_leaf_popup():
    if DEBUG_MODE:
        print("delayed_leaf_popup 呼び出し")

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                context_override = {
                    'window': window,
                    'screen': window.screen,
                    'area': area,
                    'region': area.regions[-1],  # 最後の region は通常 UI 領域
                    'scene': bpy.context.scene,
                    'view_layer': bpy.context.view_layer,
                    'active_object': bpy.context.view_layer.objects.active,
                }

                # ✅ オペレーター呼び出しは context_override を渡す
                bpy.ops.fop.confirm_leaf_bone_delete(
                    context_override,
                    'INVOKE_DEFAULT',
                    armature_name=delayed_leaf_popup.armature_name,
                    bone_names_csv=delayed_leaf_popup.bone_names_csv
                )
                return None
    return None  # 一度だけ実行


# インポート後にリーフボーンを検出
def post_import_leaf_bone_check(context, imported_objs):
    for obj in imported_objs:
        if DEBUG_MODE:
            print("検査対象:", obj.name, obj.type)
        if obj.type != 'ARMATURE':
            if DEBUG_MODE:
                print("アーマチュア確認:", obj.name in bpy.data.objects)
            continue

        leaf_bones = find_leaf_end_bones(obj)
        if leaf_bones:
            # select_leaf_bones(leaf_bones)
            # set_bone_name_display(obj, True)    # ビューポートのアーマチュア名表示ON

            # ポップアップ表示
            bone_names_csv = ",".join([bone.name for bone in leaf_bones])
            if DEBUG_MODE:
                print("検出されたリーフボーン数:", len(leaf_bones))
                print("bone_names_csv:", bone_names_csv)
                print("オペレーター呼び出し開始")

            # ✅ アクティブ化してコンテキストに載せる
            context.view_layer.objects.active = obj
            obj.select_set(True)

            # 遅延実行場情報
            delayed_leaf_popup.armature_name = obj.name
            delayed_leaf_popup.bone_names_csv = bone_names_csv

            # ✅ UIスレッドでポップアップを表示
            bpy.app.timers.register(delayed_leaf_popup, first_interval=0.1)


            # ✅ 処理後にリストを空にする
            leaf_bones.clear()