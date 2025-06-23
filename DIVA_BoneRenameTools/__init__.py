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

from . import addon_panel
from . import rename_bones
from . import rename_groups

classes = [
    addon_panel.BoneRenamePanel,
    addon_panel.RenameSelectedBonesOperator,
    addon_panel.DetectCommonPrefixOperator,
    addon_panel.RenameGroupsOperator,
    addon_panel.RevertNamesOperator,
    addon_panel.InvertSelectedBonesOperator,
    addon_panel.RenameBonePairOperator,
]

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

    bpy.types.Scene.show_symmetric_tools = bpy.props.BoolProperty(
        name="Other Reneme Tools",
        description="その他のボーンリネーム操作",
        default=True
    )    

    bpy.types.Scene.rename_source_name = bpy.props.StringProperty(
        name="変更前ボーン名",
        description="元のボーン名を入力",
        default=""
    )

    bpy.types.Scene.rename_target_name = bpy.props.StringProperty(
        name="変更後ボーン名",
        description="新しいボーン名を入力",
        default=""
    )

def unregister_properties():
    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_start_number
    del bpy.types.Scene.rename_suffix
    del bpy.types.Scene.rename_rule
    del bpy.types.Scene.show_symmetric_tools
    del bpy.types.Scene.rename_source_name
    del bpy.types.Scene.rename_target_name

def register():
    register_properties()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_properties()