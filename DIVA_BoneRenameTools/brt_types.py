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
        name=_("識別子セット"),
        items=get_bone_pattern_items # JSONから読み込み
    )

    bone_rule: bpy.props.EnumProperty(
        name=_("識別子ペア"),
        description=_("現在のセット内のルールを選択"),
        items=lambda self, context: get_rule_items(self, context)
    )

# 識別子ルールのデータ（左右ペア）
class BRT_BoneRuleItem(bpy.types.PropertyGroup):
    right: bpy.props.StringProperty(name="右")
    left: bpy.props.StringProperty(name="左")
    use_regex: bpy.props.BoolProperty(default=False, options={'HIDDEN'})  # ← 正規表現で置き換えるか（False＝使わない）/ 現時点ではUI側にこの設定は非表示

# 識別子セット（ラベルとルールリスト）
class BRT_BonePatternItem(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name="セット名")
    rules: bpy.props.CollectionProperty(type=BRT_BoneRuleItem)


def get_classes():
    return [
        BRT_InvertSelectedBonesProps,
        BRT_BoneRuleItem,
        BRT_BonePatternItem,
    ]

def register_properties():
    # プリファレンスの識別子セット編集折りたたみ機構
    bpy.types.Scene.brt_show_identifier_sets = bpy.props.BoolProperty(
        name="識別セットの表示",
        description="識別子セット全体の編集UIを表示するかどうか",
        default=False  # デフォルトは閉じておく
    )

    bpy.types.Scene.brt_rename_prefix = bpy.props.StringProperty(
        name=_("共通部分"),
        description=_("ボーン名の共通部分を入力"),
        default=""
    )
    bpy.types.Scene.brt_rename_start_number = bpy.props.IntProperty(
        name=_("開始番号"),
        description=_("連番の開始値の設定"),
        default=0,
        min=0,
        max=20
    )
    bpy.types.Scene.brt_rename_suffix = bpy.props.EnumProperty(
        name="末尾",
        description=_("ボーン名の末尾を選択"),
        items=[
            ("_wj", "_wj", _("ボーン名の末尾に `_wj` を追加")),
            ("wj", "wj", _("ボーン名の末尾に `wj` を追加")),
            ("_wj_ex", "_wj_ex", _("ボーン名の末尾に `_wj_ex` を追加")),
            ("wj_ex", "wj_ex", _("ボーン名の末尾に `wj_ex` を追加"))
        ],
        default="_wj"
    )
    bpy.types.Scene.brt_rename_rule = bpy.props.EnumProperty(
        name=_("連番法則"),
        description=_("ボーンの連番ルールを選択"),
        items=[
            ("000", _("000 (3桁)"), _("3桁の番号を付加")),
            ("00", _("00 (2桁)"), _("2桁の番号を付加"))
        ],
        default="000"
    )

    # bpy.types.Scene.brt_show_symmetric_tools = bpy.props.BoolProperty(name="Other Reneme Tools", description="その他のボーンリネーム操作", default=True)    

    bpy.types.Scene.brt_rename_source_name = bpy.props.StringProperty(
        name=_("変更前ボーン名"),
        description=_("元のボーン名を入力"),
        default=""
    )

    bpy.types.Scene.brt_rename_target_name = bpy.props.StringProperty(
        name=_("変更後ボーン名"),
        description=_("新しいボーン名を入力"),
        default=""
    )

    bpy.types.Scene.brt_remove_number_suffix = bpy.props.BoolProperty(
        name=_("番号サフィックスを削除"),
        description=_(".001 などの複製識別子を削除します"),
        default=False
    )

    bpy.types.Scene.brt_show_renumber_tools = bpy.props.BoolProperty(
        name="show_renumber_tools",
        description=_("ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示"),
        default=True
    )

    bpy.types.Scene.brt_show_replace_tools = bpy.props.BoolProperty(
        name="show_replace_tools",
        description=_("ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示"),
        default=True
    )

    bpy.types.Scene.brt_show_invert_tools = bpy.props.BoolProperty(
        name="show_invert_tools",
        description=_("L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示"),
        default=True
    )

    bpy.types.Scene.brt_show_group_tools = bpy.props.BoolProperty(
        name="show_group_tools",
        description="左右対応名の一括リネーム（グループ名含む）や、元に戻す操作を表示",
        default=True
    )

    bpy.types.Scene.brt_bone_x_mirror = bpy.props.BoolProperty(
        name="bone_x_mirror",
        description=_("選択したボーンをグローバルX軸でミラー反転させる"),
        default=True
    )

    bpy.types.Scene.brt_duplicate_and_rename = bpy.props.BoolProperty(
        name="duplicate_and_rename",
        description=_("選択したボーンを複製してリネームする"),
        default=False
    )

    bpy.types.Scene.brt_assign_identifier = bpy.props.BoolProperty(
        name="assign_identifier",
        description=_("左右識別子を付与する"),
        default=False
    )

    bpy.types.Scene.brt_invert_selected_bones = bpy.props.PointerProperty(
        type=BRT_InvertSelectedBonesProps
    )


def unregister_properties():
    del bpy.types.Scene.brt_show_identifier_sets
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

