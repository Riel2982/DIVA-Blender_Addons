bl_info = {
    "name": "DIVA - Split Mrror Weight",
    "author": "Riel",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Nパネル > DIVA",
    "description": "DIVA-CustomRigMirror",
    "category": "Object",
}

import bpy
import bmesh
import os
import json

# JSONデータをグローバル変数として定義
bone_pattern_choices = []

def load_bone_patterns():
    """JSONファイルを読み込み、ボーン識別文字の選択肢を作成"""
    addon_folder = os.path.dirname(__file__)
    file_path = os.path.join(addon_folder, "bone_patterns.json")

    if not os.path.exists(file_path):
        return [("_r_", "_l_")]  # **デフォルト値**

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return [(f"{entry['right']}, {entry['left']}", f"{entry['right']} , {entry['left']}") for entry in data]
    except json.JSONDecodeError:
        print("⚠ JSONファイルのフォーマットにエラーがあります")
        return [("_r_", "_l_")]  # **デフォルト値**

# **Blenderの登録前にロード**
bone_pattern_choices = load_bone_patterns()

# プロパティグループ
class SplitMirrorWeightProperties(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="ボーン識別文字",
        description="ドロップダウンから選択",
        items=[(entry[0], entry[1], "") for entry in bone_pattern_choices],  # ✅ 形式を修正
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

# Nパネル設定
class SplitMirrorWeightPanel(bpy.types.Panel):
    bl_label = "DIVA-CustomRigMirror"
    bl_idname = "OBJECT_PT_symmetric_weight_transfer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIVA"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.symmetric_weight_transfer_props
        layout.prop(properties, "bone_pattern")  # ✅ **ドロップダウン化**
        layout.prop(properties, "delete_side")  # 削除する側を選択
        layout.operator("object.symmetric_weight_transfer")

# ミラーモディファイアをオフにする処理
def disable_mirror_modifier(obj):
    """対象メッシュのミラーモディファイアをオフにする"""
    for mod in obj.modifiers:
        if mod.type == 'MIRROR':
            mod.show_viewport = False
            mod.show_render = False

# オブジェクト複製＆ミラー適用
def duplicate_and_apply_mirror(obj):
    """オリジナルオブジェクトを複製し、複製にミラーモディファイアを適用"""
    bpy.ops.object.select_all(action='DESELECT')  
    obj.select_set(True)
    bpy.ops.object.duplicate()
    mirrored_obj = bpy.context.selected_objects[0]  

    # ミラーを追加＆適用
    bpy.context.view_layer.objects.active = mirrored_obj
    bpy.ops.object.modifier_add(type='MIRROR')
    mirror_mod = mirrored_obj.modifiers[-1]
    mirror_mod.use_axis[0] = True  

    bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
    return mirrored_obj

# X軸側メッシュ削除
def delete_x_side_mesh(obj, delete_positive_x=True):
    """選択された側のメッシュを削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    for vert in bm.verts:
        if (delete_positive_x and vert.co.x > 0) or (not delete_positive_x and vert.co.x < 0):
            bm.verts.remove(vert)

    bm.to_mesh(mesh)
    bm.free()

# 頂点グループリネーム処理
def rename_symmetric_weight_groups(obj, pattern_left, pattern_right, delete_side):
    """削除する側を考慮し、頂点グループを適切にリネーム"""
    vgroup_map = {vg.name for vg in obj.vertex_groups}

    if delete_side == 'RIGHT':
        for vg_name in list(vgroup_map):
            if pattern_right in vg_name:
                obj.vertex_groups.remove(obj.vertex_groups.get(vg_name))

        for vg_name in list(vgroup_map):
            if pattern_left in vg_name:
                new_name = vg_name.replace(pattern_left, pattern_right)
                obj.vertex_groups.get(vg_name).name = new_name

    else:
        for vg_name in list(vgroup_map):
            if pattern_left in vg_name:
                obj.vertex_groups.remove(obj.vertex_groups.get(vg_name))

        for vg_name in list(vgroup_map):
            if pattern_right in vg_name:
                new_name = vg_name.replace(pattern_right, pattern_left)
                obj.vertex_groups.get(vg_name).name = new_name

# アドオン処理
class OBJECT_OT_SplitMirrorWeight(bpy.types.Operator):
    bl_idname = "object.symmetric_weight_transfer"
    bl_label = "DIVA-CustomRigMirror"

    def execute(self, context):
        obj = bpy.context.object
        properties = bpy.context.scene.symmetric_weight_transfer_props

        delete_positive_x = (properties.delete_side == 'RIGHT')

        if obj and obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE':
            armature = obj.parent

            disable_mirror_modifier(obj)  
            mirrored_obj = duplicate_and_apply_mirror(obj)  

            delete_x_side_mesh(mirrored_obj, delete_positive_x)  

            pattern_right, pattern_left = properties.bone_pattern.split(", ")  

            rename_symmetric_weight_groups(mirrored_obj, pattern_left, pattern_right, properties.delete_side)

            self.report({'INFO'}, "ミラー適用 & ウェイト転送完了")
        return {'FINISHED'}

# 登録
def register():
    bpy.utils.register_class(SplitMirrorWeightProperties)
    bpy.utils.register_class(SplitMirrorWeightPanel)
    bpy.utils.register_class(OBJECT_OT_SplitMirrorWeight)
    bpy.types.Scene.symmetric_weight_transfer_props = bpy.props.PointerProperty(type=SplitMirrorWeightProperties)

def unregister():
    bpy.utils.unregister_class(SplitMirrorWeightPanel)
    bpy.utils.unregister_class(SplitMirrorWeightProperties)
    bpy.utils.unregister_class(OBJECT_OT_SplitMirrorWeight)
    del bpy.types.Scene.symmetric_weight_transfer_props

if __name__ == "__main__":
    register()