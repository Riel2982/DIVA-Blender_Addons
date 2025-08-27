# fop_types.py

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
    IntProperty,
)
from bpy.types import PropertyGroup
from bpy.app.translations import pgettext as _

from .fop_save import update_overwrite_guard



# オプション設定
class FOP_FBXSettings(bpy.types.PropertyGroup):
    # Saver
    blendfile_overwrite_guard: BoolProperty(
        name="Blend file Overwrite Guard",     # エクスポートファイルの上書き防止
        description=_("Save with numbering if a file with the same name exists"),
        default=True,
        update=update_overwrite_guard,  # UIの選択状況に応じてファイル名のナンバリング反映も制御
    )
    pack_resources: BoolProperty(
        name="Pack Resources",  # リソースのパック
        description="Pack all used external files into this .blend",
        default=False
)
    external_data: EnumProperty(    # _("External Data Storage Mode") "外部データの格納方式"
        name="External Data",
        description=_("External Data Pass Mode"),
        items=[
            # ('PACK', _("Pack Resources"), "Pack all used external files into this .blend"),
            ('RELATIVE', _("Make Paths Relative"), "Make all paths to external files relative to current .blend"),
            ('ABSOLUTE', _("Make Paths Absolute"), "Make all paths to external files absolute"), 
            ('MIXED', _("Leave As-Is"), _("Do not change external file paths")),
        ],
        default='MIXED'
    )

    # Import
    use_custom_normals: BoolProperty(
        name="Custom Normals",      # カスタム法線を使用
        description=_("Import custom normals if they are available; if not, Blender will recompute them automatically"),    # Import custom nomals, if available (otherwise Blender will recompute them)
        default=True
    )
    create_collection: BoolProperty(
        name="Create a Collection", 
        description=_("Create a new collection for imported FBX"),
        default=True)

    # Export
    export_filename: StringProperty(
        name="Export Filename",
        description=_("Name of the FBX file to export"),    # 出力するFBXファイル名
        default="untitled"
    )

    export_overwrite_guard: BoolProperty(
        name="FBX data Overwrite Guard",     # エクスポートファイルの上書き防止
        description=_("Save with numbering if a data with the same name exists"),
        default=True
    )
    use_selection: BoolProperty(
        name="Selected Objects",        # 選択中のオブジェクトをエクスポート
        description="Export selected and visible objects only",
        default=False
        )
    use_visible: BoolProperty(
        name="Visible Objects",        # 可視オブジェクトをエクスポート
        description="Export visible objects only",
        default=False
        )
    use_active_collection: BoolProperty(
        name="Active Collection",        # アクティブコレクションをエクスポート
        description="Export only objects from the active collection (and its children)",
        default=False
        )



def get_classes():
    return [
        FOP_FBXSettings,
    ]


def register_properties():
    # Settings
    bpy.types.Scene.fop_settings = bpy.props.PointerProperty(type=FOP_FBXSettings)  # class登録したPropertyGroup
    # Panel_UI
    bpy.types.Scene.fop_show_save_tools = bpy.props.BoolProperty(
        name="Show Save Tools",
        description=_("Show tool to save blend file"), 
        default=True
    )
    bpy.types.Scene.fop_show_import_tools = bpy.props.BoolProperty(
        name="Show Import Tools",
        description=_("Show tool to import fbx data"), 
        default=True
    )
    bpy.types.Scene.fop_show_export_tools = bpy.props.BoolProperty(
        name="Show Export Tools",
        description=_("Show tool to export fbx data"), 
        default=True
    )
    # Export用
    bpy.types.Scene.fop_blend_save_path = bpy.props.StringProperty(
        name="Save Path",
        description=_("Folder to save blend file"),
        default="",
        subtype='NONE'  # DIR_PATHだとsplitと併用できないみたいでフォルダアイコンが2つ並んでしまう
    )
    bpy.types.Scene.fop_blend_saved_path = bpy.props.StringProperty(
        name="Saved Path",
        description = _("Whether the blend file is saved"),     # BLENDファイルが保存されているかどうか
    )
    bpy.types.Scene.fop_blend_save_filename = bpy.props.StringProperty(
        name="Blend Filename",
        description=_("Name of the blend file to save"),    # 保存するBlendファイル名（拡張子不要）
        default="untitled"
    )
    bpy.types.Scene.fop_export_use_blend_folder = bpy.props.BoolProperty(
        name="Use Blend Folder", 
        description=_("Save in the same location as the blend file"),   # Blendファイルと同じ場所に保存する
        default=True)



def unregister_properties():
    del bpy.types.Scene.fop_settings
    del bpy.types.Scene.fop_show_save_tools
    del bpy.types.Scene.fop_show_export_tools
    del bpy.types.Scene.fop_show_import_tools
    del bpy.types.Scene.fop_blend_save_path
    del bpy.types.Scene.fop_blend_saved_path
    del bpy.types.Scene.fop_blend_save_filename
    del bpy.types.Scene.fop_export_use_blend_folder

