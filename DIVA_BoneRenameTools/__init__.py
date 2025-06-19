bl_info = {
    "name": "DIVA - Bone Rename Tools",
    "author": "Riel",
    "version": (0, 0, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DIVA",
    "description": "Nパネルからボーンと頂点グループをリネームするアドオン",
    # "warning": "強制リロード必須問題あり",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Rename-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons", 
    "category": "Object",
}

import bpy
import importlib

from . import addon_panel
from . import rename_bones
from . import rename_groups

modules = [addon_panel, rename_bones, rename_groups]

classes = [
    addon_panel.BoneRenamePanel,
    addon_panel.RenameSelectedBonesOperator,
    addon_panel.RenameGroupsOperator,
    addon_panel.RevertNamesOperator
]

# プロパティの登録

def register_properties():
    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(
        name="共通部分",
        description="ボーン名の共通部分を入力",
        default=""
    )

    bpy.types.Scene.rename_start_number = bpy.props.IntProperty(
        name="開始番号",
        description="連番の開始値の設定",
        default=0,
        min=0,
        max=20
    )

    bpy.types.Scene.rename_suffix = bpy.props.EnumProperty(
        name="末尾",
        description="ボーン名の末尾を選択",
        items=[
            ("_wj", "_wj", "ボーン名の末尾に `_wj` を追加"),
            ("wj", "wj", "ボーン名の末尾に `wj` を追加"),
            ("_wj_ex", "_wj_ex", "ボーン名の末尾に `_wj_ex` を追加"),
            ("wj_ex", "wj_ex", "ボーン名の末尾に `wj_ex` を追加")
        ],
        default="_wj"
    )

    bpy.types.Scene.rename_rule = bpy.props.EnumProperty(
        name="連番法則",
        description="ボーンの連番ルールを選択",
        items=[
            ("000", "000 (3桁)", "3桁の番号を付加"),
            ("00", "00 (2桁)", "2桁の番号を付加")
        ],
        default="000"
    )

# Blender起動時にモジュールを強制リロードして UI を更新する。
# 登録済みクラスを再度読み込んで二回目以降の UI 欠落を防ぐ。
def on_startup(dummy):
    importlib.reload(addon_panel)
    addon_panel.register()

    # 起動時にしか使わない初期化ハンドラーを削除
    if set_default_scene_values in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(set_default_scene_values)

# 初回登録時は bpy.context.scene が使えないため、load_post ハンドラーで Blender 起動完了後に scene プロパティの初期値を安全に設定する。
def set_default_scene_values(dummy=None):
    scene = bpy.context.scene
    if scene:
        if not hasattr(scene, "rename_prefix") or scene.rename_prefix == "":
            scene.rename_prefix = ""
        if not hasattr(scene, "rename_start_number") or scene.rename_start_number == 0:
            scene.rename_start_number = 0
        if not hasattr(scene, "rename_suffix") or scene.rename_suffix == "":
            scene.rename_suffix = "_wj"
        if not hasattr(scene, "rename_rule") or scene.rename_rule == "":
            scene.rename_rule = "000"

def register():


    register_properties() # クラス登録をここだけに集約
    addon_panel.register() # クラス登録（addon_panel 側で登録しておく）


    # 初回登録時は context.scene が存在しないので、直接初期値は代入しない。
    # 初期化関数を load_post に渡して、起動完了後に一度だけ呼び出すようにする。
    if set_default_scene_values not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(set_default_scene_values)

    # 起動時は UI 表示が崩れる場合があるので強制リロードで再登録する
    if on_startup not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_startup)

def unregister():
    if on_startup in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_startup)
    if set_default_scene_values in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(set_default_scene_values)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_start_number
    del bpy.types.Scene.rename_suffix
    del bpy.types.Scene.rename_rule