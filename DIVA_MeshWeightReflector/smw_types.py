# smw_types.py

import bpy
from bpy.app.translations import pgettext as _

# ボーン識別子セットの取得
def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
    items = []

    for i, pattern in enumerate(prefs.bone_patterns):
        label = pattern.label.strip()

        # 識別子としてそのまま使える名前に（ascii前提）
        identifier = label
        name = label  # 表示用にもそのまま使う（日本語でない前提）

        items.append((identifier, name, ""))

    return items



# プロパティグループ
class DIVA_SplitMirrorWeightProps(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name=_("識別子セット"),
        items=get_bone_pattern_items # JSONから読み込み
    )

    delete_side: bpy.props.EnumProperty(
        name=_("オリジナル側"),
        description=_("コピー元を選択（右 or 左）"),
        items=[
            ('RIGHT', _("左→右に複製"), _("Blenderの+X側を削除")),
            ('LEFT', _("右→左に複製"), _("Blenderの-X側を削除")),
        ],
        default='RIGHT'
    )

    mirror_auto_detect: bpy.props.BoolProperty(
        name=_("ミラー自動判別"),
        description=_("ミラーの方向を自動判別するかどうか"),
        default=False
    )

    allow_origin_overlap: bpy.props.BoolProperty(
        name=_("原点越えに対応"),
        description=_("原点からわずかにはみ出した片側メッシュでも反転する（ミラー自動判別と併用不可）"),
        default=False
    )

# 識別子ルールのデータ（左右ペア）
class SMW_BoneRuleItem(bpy.types.PropertyGroup):
    right: bpy.props.StringProperty(name="右")
    left: bpy.props.StringProperty(name="左")
    use_regex: bpy.props.BoolProperty(default=False, options={'HIDDEN'})  # ← 正規表現で置き換えるか（False＝使わない）/ 現時点ではUI側にこの設定は非表示

# 識別子セット（ラベルとルールリスト）
class SMW_BonePatternItem(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name="セット名")
    rules: bpy.props.CollectionProperty(type=SMW_BoneRuleItem)

def get_classes():
    return [
        SMW_BoneRuleItem,
        SMW_BonePatternItem,
        DIVA_SplitMirrorWeightProps, 
    ]


def register_properties():
    bpy.types.Scene.diva_split_mirror_weight = bpy.props.PointerProperty(type=DIVA_SplitMirrorWeightProps)

def unregister_properties():
    del bpy.types.Scene.diva_split_mirror_weight