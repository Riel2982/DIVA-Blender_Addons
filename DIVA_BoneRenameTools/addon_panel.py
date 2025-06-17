import bpy

class BoneRenamePanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Rename Tools"
    bl_idname = "DIVA_PT_BoneRenamePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="ボーン連番リネーム")
        layout.prop(scene, "rename_prefix")  # 共通部分入力
        layout.prop(scene, "rename_start_number")  # 連番開始番号
        layout.prop(scene, "rename_suffix")  # 末尾選択
        layout.prop(scene, "rename_rule")  # 連番法則選択

        layout.operator("object.rename_selected_bones", text="連番リネーム実行")
        
        layout.separator()
        
        layout.label(text="特定単語のリネーム")
        layout.operator("object.rename_groups", text="単語リネーム実行")
        layout.operator("object.revert_names", text="リネーム解除")

class RenameSelectedBonesOperator(bpy.types.Operator):
    """ボーン連番リネーム"""
    bl_idname = "object.rename_selected_bones"
    bl_label = "Rename Selected Bones"

    def execute(self, context):
        from .rename_bones import rename_selected_bones
        rename_selected_bones(
            context.scene.rename_prefix,
            context.scene.rename_start_number,
            context.scene.rename_suffix,
            context.scene.rename_rule
        )
        return {'FINISHED'}

class RenameGroupsOperator(bpy.types.Operator):
    """特定単語リネーム"""
    bl_idname = "object.rename_groups"
    bl_label = "Rename Bones & Vertex Groups"

    def execute(self, context):
        from .rename_groups import rename_bones_and_vertex_groups
        rename_bones_and_vertex_groups()
        return {'FINISHED'}

class RevertNamesOperator(bpy.types.Operator):
    """名前を元に戻す"""
    bl_idname = "object.revert_names"
    bl_label = "Revert Renamed Names"

    def execute(self, context):
        from .rename_groups import revert_renamed_names
        revert_renamed_names()
        return {'FINISHED'}


def register():
    # 🔹 まずプロパティを登録する
    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(name="共通部分")
    bpy.types.Scene.rename_start_number = bpy.props.IntProperty(name="開始番号", default=0, min=0, max=12)
    bpy.types.Scene.rename_suffix = bpy.props.EnumProperty(
        name="末尾",
        description="ボーン名の末尾を選択します",
        items=[
            ("_wj", "_wj", "ボーン名の末尾に `_wj` を追加"),
            ("wj", "wj", "ボーン名の末尾に `wj` を追加"),
            ("_wj_ex", "_wj_ex", "ボーン名の末尾に `_wj_ex` を追加"),
            ("wj_ex", "_wj_ex", "ボーン名の末尾に `wj_ex` を追加")
        ]
    )
    bpy.types.Scene.rename_rule = bpy.props.EnumProperty(
        name="連番法則",
        description="ボーンの連番ルールを選択します",
        items=[
            ("000", "000 (3桁)", "3桁の番号を付加"),
            ("00", "00 (2桁)", "2桁の番号を付加")
        ]
    )

    # 🔹 次にUIクラスを登録
    bpy.utils.register_class(BoneRenamePanel)
    bpy.utils.register_class(RenameSelectedBonesOperator)
    bpy.utils.register_class(RenameGroupsOperator)
    bpy.utils.register_class(RevertNamesOperator)

    # 🔹 シーンの初期化（シーンが存在する場合のみ）
    if bpy.context.scene is not None:
        bpy.context.scene.rename_prefix = ""
        bpy.context.scene.rename_start_number = 0
        bpy.context.scene.rename_suffix = "_wj"
        bpy.context.scene.rename_rule = "000"


def unregister():
    bpy.utils.unregister_class(BoneRenamePanel)
    bpy.utils.unregister_class(RenameSelectedBonesOperator)
    bpy.utils.unregister_class(RenameGroupsOperator)
    bpy.utils.unregister_class(RevertNamesOperator)

    # Sceneプロパティの削除
    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_start_number
    del bpy.types.Scene.rename_suffix
    del bpy.types.Scene.rename_rule

if __name__ == "__main__":
    register()
