# bprs_types.py

import bpy
from bpy.app.translations import pgettext as _

class BPRS_BoneDisplayFilterSettings(bpy.types.PropertyGroup):
    bprs_display_mode: bpy.props.EnumProperty(
        name="Display Mode",
        items=[
            ('ALL', _("Show All"), _("Display all bones")),
            ('VISIBLE', _("Visible Bones Only"), _("Display only bones not hidden in Edit Mode")),
            ('SELECTED', _("Selected Only"), _("Only bones selected in Edit Mode")),    # _("選択中のみ")
            ('UNSELECTED', _("Unselected Only"), _("Only bones not selected")),
        ],
        default='ALL'
    )

class BPRS_BoneItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    show_info: bpy.props.BoolProperty(name=_("Show"), default=False)  # ✅ チェックボックス表示制御


def get_classes():
    return [
        BPRS_BoneDisplayFilterSettings,
        BPRS_BoneItem,
    ]


def register_properties():
    # Panel_UI
    bpy.types.Scene.bprs_show_export_tools = bpy.props.BoolProperty(
        name="show_export_tools",
        description=_("Show tool to export bone data of selected armature to file"),        # 選択アーマーチュアのボーンデータをファイルに出力するツールを表示
        default=False
    )
    '''
    bpy.types.Scene.bprs_show_import_tools = bpy.props.BoolProperty(
        name="show_import_tools",
        description=_("Show tool to generate hidden bones from bone data"),     # ボーンデータから隠しボーンを生成するツールを表示
        default=True
    )
    '''
    bpy.types.Scene.bprs_show_check_tools = bpy.props.BoolProperty(
        name="show_check_tools",
        description=_("Show tool to inspect bone data of selected armature"),      # 選択アーマチュアのボーンデータを確認するツールを表示
        default=True
    )

    
    # Exporter: カスタムプロパティ（ファイル名＆保存先＆自動オープン＆上書き制御）
    bpy.types.Scene.bprs_export_filename = bpy.props.StringProperty(
        name="File Name",
        description=_("Filename to save - without extension"),
        default="bone_data"
    )
    bpy.types.Scene.bprs_export_filepath = bpy.props.StringProperty(
        name="Export Path",
        description=_("Destination folder"),
        default=""
    )
    bpy.types.Scene.bprs_export_auto_open = bpy.props.BoolProperty(
        name=_("Auto Open File"),
        description=_("Automatically open the file after export"),
        default=False
    )
    bpy.types.Scene.bprs_export_overwrite = bpy.props.BoolProperty(
        name=_("Overwrite Existing File"),
        description=_("Overwrite existing file / rename if unchecked"),
        default=True
    )
    bpy.types.Scene.bprs_export_format_json = bpy.props.BoolProperty(
        name=_("Export as JSON"),
        description=_("Save in JSON format / TXT if unchecked"),
        default=False
    )

    # Checker:

    bpy.types.Scene.bprs_filter_settings = bpy.props.PointerProperty(type=BPRS_BoneDisplayFilterSettings)
    bpy.types.Scene.bprs_bones_data = bpy.props.CollectionProperty(type=BPRS_BoneItem)
    bpy.types.Scene.bprs_bones_data_index = bpy.props.IntProperty(
        name="Armature Bones List",
        description=_("List of armature bones"),
    )
    bpy.types.Scene.bprs_last_checked_armature = bpy.props.StringProperty(name="Last Checked Armature")     # 取得したデータのアーマチュア名記録



def unregister_properties():
    del bpy.types.Scene.bprs_show_export_tools
    # del bpy.types.Scene.bprs_show_import_tools
    del bpy.types.Scene.bprs_show_check_tools
    del bpy.types.Scene.bprs_export_filename
    del bpy.types.Scene.bprs_export_filepath
    del bpy.types.Scene.bprs_export_auto_open
    del bpy.types.Scene.bprs_export_format_json

    del bpy.types.Scene.bprs_filter_settings

    del bpy.types.Scene.bprs_bones_data
    del bpy.types.Scene.bprs_bones_data_index
    del bpy.types.Scene.bprs_last_checked_armature


