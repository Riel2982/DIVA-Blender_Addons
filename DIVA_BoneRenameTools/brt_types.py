import bpy
from bpy.app.translations import pgettext as _
from .brt_preferences import get_bone_pattern_items, get_rule_items
from .brt_panel import BRT_InvertSelectedBonesProps

def register_properties():
    bpy.types.Scene.brt_rename_prefix = bpy.props.StringProperty(
        name="共通部分",
        description="ボーン名の共通部分を入力",
        default=""
    )
    bpy.types.Scene.brt_rename_start_number = bpy.props.IntProperty(
        name="開始番号",
        description="連番の開始値の設定",
        default=0,
        min=0,
        max=20
    )
    bpy.types.Scene.brt_rename_suffix = bpy.props.EnumProperty(
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
    bpy.types.Scene.brt_rename_rule = bpy.props.EnumProperty(
        name="連番法則",
        description="ボーンの連番ルールを選択",
        items=[
            ("000", "000 (3桁)", "3桁の番号を付加"),
            ("00", "00 (2桁)", "2桁の番号を付加")
        ],
        default="000"
    )

    # bpy.types.Scene.brt_show_symmetric_tools = bpy.props.BoolProperty(name="Other Reneme Tools", description="その他のボーンリネーム操作", default=True)    

    bpy.types.Scene.brt_rename_source_name = bpy.props.StringProperty(
        name="変更前ボーン名",
        description="元のボーン名を入力",
        default=""
    )

    bpy.types.Scene.brt_rename_target_name = bpy.props.StringProperty(
        name="変更後ボーン名",
        description="新しいボーン名を入力",
        default=""
    )

    bpy.types.Scene.brt_remove_number_suffix = bpy.props.BoolProperty(
        name="番号サフィックスを削除",
        description=".001 などの複製識別子を削除します",
        default=False
    )

    bpy.types.Scene.brt_show_renumber_tools = bpy.props.BoolProperty(
        name="show_renumber_tools",
        description="ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示",
        default=True
    )

    bpy.types.Scene.brt_show_replace_tools = bpy.props.BoolProperty(
        name="show_replace_tools",
        description="ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示",
        default=True
    )

    bpy.types.Scene.brt_show_invert_tools = bpy.props.BoolProperty(
        name="show_invert_tools",
        description="L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示",
        default=True
    )

    bpy.types.Scene.brt_show_group_tools = bpy.props.BoolProperty(
        name="show_group_tools",
        description="左右対応名の一括リネーム（グループ名含む）や、元に戻す操作を表示",
        default=True
    )

    bpy.types.Scene.brt_bone_x_mirror = bpy.props.BoolProperty(
        name="bone_x_mirror",
        description="選択したボーンをグローバルX軸でミラー反転させる",
        default=True
    )

    bpy.types.Scene.brt_duplicate_and_rename = bpy.props.BoolProperty(
        name="duplicate_and_rename",
        description="選択したボーンを複製してリネームする",
        default=False
    )

    bpy.types.Scene.brt_assign_identifier = bpy.props.BoolProperty(
        name="assign_identifier",
        description="左右識別子を付与する",
        default=False
    )

    bpy.types.Scene.brt_invert_selected_bones = bpy.props.PointerProperty(
        type=BRT_InvertSelectedBonesProps
    )


def unregister_properties():
    del bpy.types.Scene.brt_rename_prefix
    del bpy.types.Scene.brt_rename_start_number
    del bpy.types.Scene.brt_rename_suffix
    del bpy.types.Scene.brt_rename_rule
    # del bpy.types.Scene.brt_show_symmetric_tools
    del bpy.types.Scene.brt_rename_source_name
    del bpy.types.Scene.brt_rename_target_name
    del bpy.types.Scene.brt_remove_number_suffix
    del bpy.types.Scene.brt_show_renumber_tools
    del bpy.types.Scene.brt_show_replace_tools
    del bpy.types.Scene.brt_show_invert_tools
    del bpy.types.Scene.brt_show_group_tools
    del bpy.types.Scene.brt_bone_x_mirror
    del bpy.types.Scene.brt_duplicate_and_rename
    del bpy.types.Scene.brt_assign_identifier
    del bpy.types.Scene.brt_invert_selected_bones
