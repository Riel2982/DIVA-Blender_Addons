bl_info = {
    "name": "DIVA - Split Mirror Weight",
    "author": "Riel",
    "version": (1, 2),
    "blender": (3, 6, 22),
    "location": "Nパネル > DIVA",
    "description": "DIVA-CustomRigMirror",
    "category": "Object",
}

import bpy
import os
import json

# JSONデータをグローバル変数として定義
bone_pattern_choices = []

def load_bone_patterns():
    """JSONファイルを読み込み、ボーン識別文字の選択肢を作成"""
    addon_folder = os.path.dirname(__file__)
    file_path = os.path.join(addon_folder, "bone_patterns.json")

    default_values = [("_r_, _l_", "_r_ , _l_")]

    if not os.path.exists(file_path):
        return default_values

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return default_values + [(f"{entry['right']}, {entry['left']}", f"{entry['right']} , {entry['left']}") for entry in data]
        else:
            print("⚠ JSONファイルの構造が正しくありません")
            return default_values

    except json.JSONDecodeError:
        print("⚠ JSONファイルのフォーマットにエラーがあります")
        return default_values

bone_pattern_choices = load_bone_patterns()

# プロパティグループ
class SplitMirrorWeightProperties(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="ボーン識別文字",
        description="ドロップダウンから選択",
        items=[(entry[0], entry[1], "") for entry in bone_pattern_choices],
        default=bone_pattern_choices[0][0] if bone_pattern_choices else "_r_, _l_"
    )

    delete_side: bpy.props.EnumProperty(
        name="オリジナル側",
        description="コピー元を選択（右 or 左）",
        items=[
            ('RIGHT', "左→右に複製", "Blenderの+X側を削除"),
            ('LEFT', "右→左に複製", "Blenderの-X側を削除"),
        ],
        default='RIGHT'
    )

    mirror_auto_detect: bpy.props.BoolProperty(
        name="ミラー自動判別",
        description="ミラーの方向を自動判別するかどうか",
        default=False
    )

# 指定したX方向に頂点があるか調べる
def has_vertices_on_positive_x(obj, threshold=0.001):
    """+X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x > threshold for v in obj.data.vertices)

def has_vertices_on_negative_x(obj, threshold=0.001):
    """-X側に頂点が存在するか"""
    return any((obj.matrix_world @ v.co).x < -threshold for v in obj.data.vertices)

def detect_original_side(obj, threshold=0.001):
    """オブジェクトのオリジナル側を自動判定"""
    if not obj or obj.type != 'MESH':
        return None

    has_left = has_vertices_on_negative_x(obj, threshold)
    has_right = has_vertices_on_positive_x(obj, threshold)

    if has_left and not has_right:
        return 'LEFT'
    elif has_right and not has_left:
        return 'RIGHT'
    else:
        return None  # 両側にメッシュがあるため曖昧（手動選択必須）

# 頂点グループリネーム処理
def rename_symmetric_weight_groups(obj, pattern_left, pattern_right, delete_side):
    """削除する側を考慮し、頂点グループを適切にリネーム"""
    if not obj or obj.type != 'MESH':
        return

    vgroup_map = {vg.name for vg in obj.vertex_groups}

    if delete_side == 'RIGHT':
        for vg_name in list(vgroup_map):
            if pattern_right in vg_name:
                obj.vertex_groups.remove(obj.vertex_groups.get(vg_name))

        for vg_name in list(vgroup_map):
            if pattern_left in vg_name:
                new_name = vg_name.replace(pattern_left, pattern_right)
                vg = obj.vertex_groups.get(vg_name)
                if vg:
                    vg.name = new_name

    else:
        for vg_name in list(vgroup_map):
            if pattern_left in vg_name:
                obj.vertex_groups.remove(obj.vertex_groups.get(vg_name))

        for vg_name in list(vgroup_map):
            if pattern_right in vg_name:
                new_name = vg_name.replace(pattern_right, pattern_left)
                vg = obj.vertex_groups.get(vg_name)
                if vg:
                    vg.name = new_name

# オブジェクトを複製し、編集モードで縮小反転・法線反転を適用
def duplicate_and_mirror(obj):
    if not obj or obj.type != 'MESH':
        print("エラー: 有効なメッシュオブジェクトではありません")
        return None

    # ミラーモディファイアを無効化（オリジナル）
    for mod in obj.modifiers:
        if mod.type == 'MIRROR':
            mod.show_viewport = False
            mod.show_render = False

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.duplicate()
    mirrored_obj = bpy.context.selected_objects[0]

    # ミラーモディファイア削除（複製後のオブジェクト）
    for mod in mirrored_obj.modifiers:
        if mod.type == 'MIRROR':
            bpy.ops.object.modifier_remove(modifier=mod.name)

    # カスタムリネーム（"_R" → "_L" / "_L" → "_R"）
    if obj.name.endswith("_R"):
        mirrored_obj.name = obj.name.replace("_R", "_L")
    elif obj.name.endswith("_L"):
        mirrored_obj.name = obj.name.replace("_L", "_R")
    else:
        mirrored_obj.name = obj.name + "_L"

    # グローバルX軸での反転
    mirrored_obj.scale.x *= -1
    mirrored_obj.data.update()

    # 法線反転
    bpy.context.view_layer.objects.active = mirrored_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    return mirrored_obj

# ミラーリング実行
def run(obj, delete_side, pattern_left, pattern_right):
    """オブジェクトをミラーリングし、ウェイト適用を修正"""
    if not obj or obj.type != 'MESH':
        print("エラー: 無効なオブジェクト")
        return {'CANCELLED'}

    if delete_side == 'RIGHT':
        if not has_vertices_on_positive_x(obj):
            print("⚠ 左側（+X）にメッシュが存在しません。処理を中断します。")
            return {'CANCELLED'}
    elif delete_side == 'LEFT':
        if not has_vertices_on_negative_x(obj):
            print("⚠ 右側（-X）にメッシュが存在しません。処理を中断します。")
            return {'CANCELLED'}

    mirrored_obj = duplicate_and_mirror(obj)
    if not mirrored_obj:
        print("ミラー失敗")
        return {'CANCELLED'}

    rename_symmetric_weight_groups(mirrored_obj, pattern_left, pattern_right, delete_side)
    print(f"ミラー適用＆ウェイトグループ整理完了: {mirrored_obj.name}")
    return {'FINISHED'}

# SplitMirror実行
class OBJECT_OT_SplitMirrorWeight(bpy.types.Operator):
    bl_idname = "object.split_mirror_weight"
    bl_label = "ミラー実行"

    def execute(self, context):
        obj = context.object
        props = context.scene.split_mirror_weight_props

        # 3Dビューで選択されているか確認する
        if not obj or obj not in context.selected_objects:
            self.report({'ERROR'}, "オブジェクトが選択されていません（シーンコレクション選択のみでは不可）")
            return {'CANCELLED'}

        # ミラー自動判別がONの場合、自動判定を実行
        if props.mirror_auto_detect:
            detected_side = detect_original_side(obj)
            if detected_side:
                props.delete_side = detected_side  # 判定した側をオリジナルとして設定
            else:
                self.report({'ERROR'}, "ミラー方向を自動判別できません。手動でオリジナル側を選択してください。")
                return {'CANCELLED'}

        # ミラー処理を実行
        pattern_right, pattern_left = props.bone_pattern.split(", ")
        result = run(obj, props.delete_side, pattern_left.strip(), pattern_right.strip())

        if result == {'FINISHED'}:
            self.report({'INFO'}, "SplitMirrorWeight 実行完了")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "指定された方向にメッシュが存在しません。処理を中止しました。")
            return {'CANCELLED'}

# Nパネル設定
class SplitMirrorWeightPanel(bpy.types.Panel):
    bl_label = "Split Mirror Weight"
    bl_idname = "DIVA_PT_split_mirror_weight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIVA"

    def draw(self, context):
        layout = self.layout
        props = context.scene.split_mirror_weight_props

        # ボーン識別文字（ドロップダウン）
        layout.prop(props, "bone_pattern")

        # オリジナル側
        layout.prop(props, "delete_side")

        # ミラー自動判別（チェックボタン）
        row = layout.row()
        row.prop(props, "mirror_auto_detect", text="")  # チェックボックス
        row.label(text="ミラー自動判別")  # ラベル

        # ミラー実行ボタン
        layout.separator()
        layout.operator("object.split_mirror_weight", icon="MOD_MIRROR")

# 各モジュールに register() / unregister() を定義
def register():
    bpy.utils.register_class(SplitMirrorWeightProperties)
    bpy.utils.register_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.register_class(SplitMirrorWeightPanel)
    bpy.types.Scene.split_mirror_weight_props = bpy.props.PointerProperty(type=SplitMirrorWeightProperties)

def unregister():
    bpy.utils.unregister_class(SplitMirrorWeightProperties)
    bpy.utils.unregister_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.unregister_class(SplitMirrorWeightPanel)
    del bpy.types.Scene.split_mirror_weight_props
