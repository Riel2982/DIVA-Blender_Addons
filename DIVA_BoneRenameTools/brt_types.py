# brt_types.py

import bpy
from bpy.app.translations import pgettext as _
from .brt_json import get_bone_pattern_items, get_rule_items

'''
def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    items = []

    for i, pattern in enumerate(prefs.bone_patterns):
        label = pattern.label.strip()

        # 識別子としてそのまま使える名前に（ascii前提）
        identifier = label
        name = label  # 表示用にもそのまま使う（日本語でない前提）

        items.append((identifier, name, ""))

    return items

# 選択したボーン識別子セットの識別子ルールを取得
def get_rule_items(self, context):
    prefs = context.preferences.addons.get("DIVA_BoneRenameTools")
    if not prefs:
        return []

    label = self.bone_pattern  # 現在のセットラベル
    patterns = prefs.preferences.bone_patterns

    for pattern in patterns:
        if pattern.label == label:
            return [
                (str(i), f"{r.right} / {r.left}", "")
                for i, r in enumerate(pattern.rules)
                if r.right and r.left
            ]

    return []
'''

# プロパティグループ
class BRT_InvertSelectedBonesProps(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="Identifier set",      # 識別子セット
        items=get_bone_pattern_items # JSONから読み込み
    )

    bone_rule: bpy.props.EnumProperty(
        name="Identifier pair",       # 識別子ペア
        description=_("Select a rule in the current set"),
        items=lambda self, context: get_rule_items(self, context)
    )


# 識別子ルールのデータ（左右ペア）
class BRT_BoneRuleItem(bpy.types.PropertyGroup):
    right: bpy.props.StringProperty(name="Right")
    left: bpy.props.StringProperty(name="Left")
    use_regex: bpy.props.BoolProperty(        # チェックボックス型
        name="Regular expression ON/OFF",
        description=_("Whether to use regular expressions"),
        default=False,      # ← 正規表現で置き換えるか（False＝使わない）
        # options={'HIDDEN'}  # UI非表示のまま
    )

# 識別子セット（ラベルとルールリスト）
class BRT_BonePatternItem(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name="Set Name")
    rules: bpy.props.CollectionProperty(type=BRT_BoneRuleItem)


def get_classes():
    return [
        BRT_InvertSelectedBonesProps,
        BRT_BoneRuleItem,
        BRT_BonePatternItem,
    ]

def register_properties():
    # プリファレンスの識別子セット編集折りたたみ機構
    bpy.types.WindowManager.brt_show_identifier_sets = bpy.props.BoolProperty(      # SceneからWindowManagerに変更して履歴に載せない・変更扱いにしない
        name="Show Identifier Sets",
        description=_("Display UI to edit identifier sets"),# 編集履歴に乗る名目
        default=False  # デフォルトは閉じておく
    )

    bpy.types.Scene.brt_rename_prefix = bpy.props.StringProperty(
        name="Base Name",
        description=_("Enter the common part of the bone name"),
        default=""
    )
    bpy.types.Scene.brt_rename_start_number = bpy.props.IntProperty(
        name="Starting Number",
        description=_("Setting the start value for serial numbers"),
        default=0,
        min=0,
        max=20
    )
    bpy.types.Scene.brt_rename_suffix = bpy.props.EnumProperty(
        name="Suffix",
        description=_("Choose the suffix for bone names"),
        items=[
            ("_wj", "_wj", _("Append `_wj` to the bone name")),
            ("wj", "wj", _("Append `wj` to the bone name")),
            ("_wj_ex", "_wj_ex", _("Append `_wj_ex` to the bone name")),
            ("wj_ex", "wj_ex", _("Append `wj_ex` to the bone name"))
        ],
        default="_wj"
    )
    bpy.types.Scene.brt_rename_rule = bpy.props.EnumProperty(
        name="Numbering Rule",      # 連番法則
        description=_("Select numbering pattern for bones"),
        items=[
            ("000", _("000 (3 digits)"), _("Add a 3-digit number")),
            ("00", _("00 (2 digits)"), _("Add a 2-digit number"))
        ],
        default="000"
    )

    bpy.types.Scene.brt_end_bone_plus = bpy.props.BoolProperty(
        name="End Bones plus",
        description=_("Add bones to the end of selected bone branches"),
        default=False
    )

    bpy.types.Scene.brt_add_bones = bpy.props.IntProperty(
        name="Number of Bones to Add",      # 追加ボーン数
        description=_("Choose how many bones to add at the end"),
        default=1,
        min=1,
        max=20
    )

    bpy.types.Scene.brt_mirror_mode = bpy.props.EnumProperty(
        name="X-Mirror Mode",
        description=_("Choose roll correction method for X-mirroring"),
        items=[
            ('DIVA', _("DIVA Mode"), _("Symmetrizes bones in DIVA character models")), # Invert roll, then add 180° and normalize to Blender format(roll を反転後 +180 → Blender仕様に正規化)
            ('SYMMETRY', _("Blender Mode"), _("Like Blender’s symmetry, but also supports custom left/right identifiers")), # Symmetry mode: roll *= -1 only(対称化モード：roll *= -1 のみ)
            # ('NONE', _("補正なし"), _("ロール補正をしない")),
            # ('TEXT', _("+180"), _("+180 → Blender仕様に正規化")),
        ],
        default='DIVA'
    )

    bpy.types.Scene.brt_rename_source_name = bpy.props.StringProperty(
        name="Original Bone Name",
        description=_("Enter the original bone name"),
        default=""
    )

    bpy.types.Scene.brt_rename_target_name = bpy.props.StringProperty(
        name="New Bone Name",
        description=_("Enter the new bone name"),
        default=""
    )

    bpy.types.Scene.brt_remove_number_suffix = bpy.props.BoolProperty(
        name="Remove Number Suffix",
        description=_("Remove duplicate identifiers"),
        default=False
    )

    bpy.types.Scene.brt_show_renumber_tools = bpy.props.BoolProperty(
        name=_("show_renumber_tools"),
        description=_("Renames the selected bone rows based on the specified settings"),    # _("Show renaming tools based on bone prefixes and numbering rules")
        default=True
    )

    bpy.types.Scene.brt_show_replace_tools = bpy.props.BoolProperty(
        name=_("show_replace_tools"),
        description=_("Replace the selected bone name substring in bulk"),   # _("Show tools for substring replacement and removing duplicate identifiers")
        default=True
    )

    bpy.types.Scene.brt_show_invert_tools = bpy.props.BoolProperty(
        name=_("show_invert_tools"),
        description=_("Invert left/right in selected bone names"),    # _("Show tools to invert Left/Right identifiers for selected bones")
        default=True
    )

    bpy.types.Scene.brt_show_group_tools = bpy.props.BoolProperty(
        name=_("show_group_tools"),
        description=_("Batch renaming for symmetric bone names and revert option"),    # _("Show batch renaming for symmetric bone names and revert option")
        default=False
    )

    bpy.types.Scene.brt_bone_x_mirror = bpy.props.BoolProperty(
        name="bone_x_mirror",
        description=_("Mirror selected bones along global X axis"),
        default=True
    )

    bpy.types.Scene.brt_duplicate_and_rename = bpy.props.BoolProperty(
        name="duplicate_and_rename",        # 複製してリネームする
        description=_("Duplicate and rename selected bones"),
        default=False
    )

    bpy.types.Scene.brt_assign_identifier = bpy.props.BoolProperty(
        name="assign_identifier",
        description=_("Assign left/right identifiers"),
        default=False
    )

    bpy.types.Scene.brt_invert_selected_bones = bpy.props.PointerProperty(
        type=BRT_InvertSelectedBonesProps
    )


def unregister_properties():
    del bpy.types.WindowManager.brt_show_identifier_sets
    del bpy.types.Scene.brt_rename_prefix
    del bpy.types.Scene.brt_rename_start_number
    del bpy.types.Scene.brt_rename_suffix
    del bpy.types.Scene.brt_rename_rule
    del bpy.types.Scene.brt_end_bone_plus
    del bpy.types.Scene.brt_add_bones
    del bpy.types.Scene.brt_mirror_mode
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

