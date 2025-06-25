bl_info = {
    "name": "DIVA - Bone Rename Tools",
    "author": "Riel",
    "version": (0, 0, 6),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DIVA",
    "description": "Nパネルからボーンと頂点グループをリネームするアドオン",
    "warning": "一部機能の未実装",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Rename-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons", 
    "category": "Object",
}

import bpy

from . import brt_panel
from . import rename_bones
from . import rename_groups

from .brt_preferences import (
    BRT_AddonPreferences,
    BRT_OT_AddBonePattern,
    BRT_OT_AddBoneRule,
    BRT_OT_DeleteBonePattern,
    BRT_OT_DeleteBoneRule,
    BRT_OT_MoveBonePatternUp,
    BRT_OT_MoveBonePatternDown,
    BRT_OT_ResetBonePatterns,
    BRT_OT_SaveBonePatterns,
    BRT_OT_AppendDefaultSet,
    load_bone_patterns_to_preferences,
	BRT_BoneRuleItem,
	BRT_BonePatternItem,
)


classes = [
    brt_panel.BoneRenamePanel,
    brt_panel.RenameSelectedBonesOperator,
    brt_panel.DetectCommonPrefixOperator,
    brt_panel.RenameGroupsOperator,
    brt_panel.RevertNamesOperator,
    brt_panel.InvertSelectedBonesOperator,
    brt_panel.ReplaceBoneNameOperator,
    brt_panel.ExtractSourceNameOperator,
    brt_panel.BRT_OT_OpenPreferences,
    brt_panel.InvertSelectedBonesProperties,
    brt_preferences.BRT_OT_AddBonePattern,
    brt_preferences.BRT_OT_AddBoneRule,
    brt_preferences.BRT_OT_DeleteBonePattern,
    brt_preferences.BRT_OT_DeleteBoneRule,
    brt_preferences.BRT_OT_MoveBonePatternUp,
    brt_preferences.BRT_OT_MoveBonePatternDown,
    brt_preferences.BRT_OT_ResetBonePatterns,
    brt_preferences.BRT_OT_SaveBonePatterns,
    brt_preferences.BRT_OT_AppendDefaultSet,
	brt_preferences.BRT_BoneRuleItem,
	brt_preferences.BRT_BonePatternItem,
    brt_preferences.BRT_AddonPreferences,
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

    # bpy.types.Scene.show_symmetric_tools = bpy.props.BoolProperty(name="Other Reneme Tools", description="その他のボーンリネーム操作", default=True)    

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

    bpy.types.Scene.remove_number_suffix = bpy.props.BoolProperty(
        name="番号サフィックスを削除",
        description=".001 などの複製識別子を削除します",
        default=False
    )

    bpy.types.Scene.show_renumber_tools = bpy.props.BoolProperty(
        name="show_renumber_tools",
        description="ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示",
        default=True
    )

    bpy.types.Scene.show_replace_tools = bpy.props.BoolProperty(
        name="show_replace_tools",
        description="ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示",
        default=True
    )

    bpy.types.Scene.show_invert_tools = bpy.props.BoolProperty(
        name="show_invert_tools",
        description="L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示",
        default=True
    )

    bpy.types.Scene.show_group_tools = bpy.props.BoolProperty(
        name="show_group_tools",
        description="左右対応名の一括リネーム（グループ名含む）や、元に戻す操作を表示",
        default=True
    )

    bpy.types.Scene.bone_x_mirror = bpy.props.BoolProperty(
        name="bone_x_mirror",
        description="選択したボーンをグローバルX軸でミラー反転させる",
        default=True
    )

    bpy.types.Scene.duplicate_and_rename = bpy.props.BoolProperty(
        name="duplicate_and_rename",
        description="選択したボーンを複製してリネームする",
        default=False
    )

def unregister_properties():
    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_start_number
    del bpy.types.Scene.rename_suffix
    del bpy.types.Scene.rename_rule
    # del bpy.types.Scene.show_symmetric_tools
    del bpy.types.Scene.rename_source_name
    del bpy.types.Scene.rename_target_name
    del bpy.types.Scene.remove_number_suffix
    del bpy.types.Scene.show_renumber_tools
    del bpy.types.Scene.show_replace_tools
    del bpy.types.Scene.show_invert_tools
    del bpy.types.Scene.show_group_tools
    del bpy.types.Scene.bone_x_mirror
    del bpy.types.Scene.duplicate_and_rename


def register():
    register_properties()

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.invert_selected_bones = bpy.props.PointerProperty(
        type=brt_panel.InvertSelectedBonesProperties
    )

    addon = bpy.context.preferences.addons.get(__name__)
    if addon:
        load_bone_patterns_to_preferences(addon.preferences)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.invert_selected_bones

    unregister_properties()