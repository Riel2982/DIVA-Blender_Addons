import bpy
from .SplitMirrorWeight import (
    bone_pattern_choices,
    detect_original_side,
    disable_mirror_modifier,
    duplicate_and_apply_mirror,
    has_vertices_on_positive_x,
    has_vertices_on_negative_x,
    delete_x_side_mesh,
    rename_symmetric_weight_groups
)

# Nパネル設定
class SplitMirrorWeightPanel(bpy.types.Panel):
    bl_label = "Split Mirror Weight"
    bl_idname = "DIVA_PT_split_mirror_weight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIVA"

    def draw(self, context):
        layout = self.layout
        props = context.scene.split_mirror_weight

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

# アドオン処理
class OBJECT_OT_SplitMirrorWeight(bpy.types.Operator):
    bl_idname = "object.split_mirror_weight"
    bl_label = "ミラー実行"

    def execute(self, context):
        obj = bpy.context.object
        properties = bpy.context.scene.split_mirror_weight

        # 3Dビューで選択されているか確認する
        if not obj or obj not in context.selected_objects:
            self.report({'ERROR'}, "オブジェクトが選択されていません（シーンコレクション選択のみでは不可）")
            return {'CANCELLED'}

        # ミラー自動判別がONの場合、自動判定を実行
        if properties.mirror_auto_detect:
            detected_side = detect_original_side(obj)
            if detected_side:
                properties.delete_side = detected_side  # 判定した側をオリジナルとして設定
            else:
                self.report({'ERROR'}, "ミラー方向を自動判別できません。手動でオリジナル側を選択してください。")
                return {'CANCELLED'}

        delete_positive_x = (properties.delete_side == 'RIGHT')

        if obj and obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE':
            armature = obj.parent

            disable_mirror_modifier(obj)  
            mirrored_obj = duplicate_and_apply_mirror(obj, properties.delete_side)  # **リネーム処理を適用**

            # メッシュの有無をチェック（関数定義が必要）
            if delete_positive_x and not has_vertices_on_positive_x(mirrored_obj):
                self.report({'ERROR'}, "右側（+X）メッシュが存在しません。処理を中止しました。")
                return {'CANCELLED'}
            elif not delete_positive_x and not has_vertices_on_negative_x(mirrored_obj):
                self.report({'ERROR'}, "左側（-X）にメッシュが存在しません。処理を中止しました。")
                return {'CANCELLED'}

            delete_x_side_mesh(mirrored_obj, delete_positive_x)  

            pattern_right, pattern_left = properties.bone_pattern.split(", ")  

            rename_symmetric_weight_groups(mirrored_obj, pattern_left, pattern_right, properties.delete_side)

            self.report({'INFO'}, f"ミラー適用 & ウェイト転送完了: {mirrored_obj.name}")
        return {'FINISHED'}

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



def register():
    bpy.utils.register_class(SplitMirrorWeightProperties)
    bpy.utils.register_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.register_class(SplitMirrorWeightPanel)
    bpy.types.Scene.split_mirror_weight = bpy.props.PointerProperty(type=SplitMirrorWeightProperties)

def unregister():
    bpy.utils.unregister_class(SplitMirrorWeightProperties)
    bpy.utils.unregister_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.unregister_class(SplitMirrorWeightPanel)
    del bpy.types.Scene.split_mirror_weight
if __name__ == "__main__":
    register()
