# mwr_types.py

import bpy
from bpy.app.translations import pgettext as _
from .mwr_json import get_bone_pattern_items, get_rule_items

# プロパティグループ
class DIVA_MeshWeightReflectorProps(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="Identifier set",      # 識別子セット
        items=get_bone_pattern_items, # JSONから読み込み
    )
    duplicate_and_mirror: bpy.props.BoolProperty(
        name="duplicate and mirror",        # 複製してミラーする
        description=_("Duplicate and mirror selected mesh"),
        default=True,
    )

    symmetrize_mode: bpy.props.BoolProperty(   # 対称化モード
        name="symmetrize mode",
        description=_("Enable alternative symmetrize mode"),
        default=False,
    )

    merge_center_vertices: bpy.props.BoolProperty(
        name="merge center",
        description=_("Merge vertices near X=0 when mirroring"),
        default=False,
    )

    merge_threshold: bpy.props.FloatProperty(
        name="merge threshold",
        description=_("X-axis threshold used for merge detection"),
        default=0.001,
        min=0.0,
        max=0.1,
        precision=4,     # 0.0001まで表示される,
        step=0.095,  # ドラッグ時のスライダー変化幅調整
    )

    apply_modifiers: bpy.props.BoolProperty(    # モディファイア適用オプション
        name="Apply Modifiers",
        description=_("Apply specific modifiers before processing"),
        default=True,
    )



# 識別子ルールのデータ（左右ペア）
class MWR_BoneRuleItem(bpy.types.PropertyGroup):
    right: bpy.props.StringProperty(name="Right")
    left: bpy.props.StringProperty(name="Left")
    use_regex: bpy.props.BoolProperty(        # チェックボックス型
        name="Regular expression ON/OFF",
        description=_("Whether to use regular expressions"),
        default=False,      # ← 正規表現で置き換えるか（False＝使わない）
        # options={'HIDDEN'}  # UI非表示のまま
    )

# 識別子セット（ラベルとルールリスト）
class MWR_BonePatternItem(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name="Set Name")
    rules: bpy.props.CollectionProperty(type=MWR_BoneRuleItem)

def get_classes():
    return [
        MWR_BoneRuleItem,
        MWR_BonePatternItem,
        DIVA_MeshWeightReflectorProps, 
    ]


def register_properties():
    # プリファレンスの識別子セット編集折りたたみ機構
    bpy.types.WindowManager.mwr_show_identifier_sets = bpy.props.BoolProperty(      # SceneからWindowManagerに変更して履歴に載せない・変更扱いにしない
        name="Show Identifier Sets",
        description=_("Display UI to edit identifier sets"),# 編集履歴に乗る名目
        default=False  # デフォルトは閉じておく
    )
    
    bpy.types.Scene.diva_mesh_weight_reflect = bpy.props.PointerProperty(type=DIVA_MeshWeightReflectorProps)

    bpy.types.WindowManager.mwr_last_symmetrized_obj_name = bpy.props.StringProperty(
        name="Last Symmetrized Object Name",
        description=_("Name of the last symmetrized mesh object"),
        default=""
    )

def unregister_properties():
    if hasattr(bpy.types.WindowManager, "mwr_show_identifier_sets"):
        del bpy.types.WindowManager.mwr_show_identifier_sets

    if hasattr(bpy.types.Scene, "diva_mesh_weight_reflect"):
        del bpy.types.Scene.diva_mesh_weight_reflect

    if hasattr(bpy.types.WindowManager, "mwr_last_symmetrized_obj_name"):
        del bpy.types.WindowManager.mwr_last_symmetrized_obj_name
