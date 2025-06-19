import bpy

class BoneRenamePanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Rename Tools"
    bl_idname = "DIVA_PT_BoneRenamePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='GROUP_BONE') # ボーンミラー風

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box1 = layout.box() # 枠付きセクションを作成

        box1.label(text="ボーン連番リネーム")
        box1.prop(scene, "rename_prefix") # 共通部分入力
        box1.prop(scene, "rename_start_number") # 連番開始番号
        box1.prop(scene, "rename_suffix") # 末尾選択
        box1.prop(scene, "rename_rule") # 連番法則選択

        box1.operator("object.rename_selected_bones", text="連番リネーム実行")
        
        layout.separator()
        
        box2 = layout.box() # 枠付きセクションを作成
        box2.label(text="特定単語のリネーム")
        box2.operator("object.rename_groups", text="単語リネーム実行")
        box2.operator("object.revert_names", text="リネーム解除")

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

# UIとオペレータクラスの登録のみ行う
def register():
    # register_properties() や context.scene の初期化処理は __init__.py が担当する（初回登録時に RestrictContext で落ちるのを防ぐ）
    # 以前はここで context.scene.rename_xxx に初期値を代入していたが、アドオンが初回に有効化される時点では Blender が "_RestrictContext" という制限付き環境で register() を実行するため、context.scene 自体が存在しない。 
    # そのため、scene にアクセスする処理は load_post ハンドラー経由で Blender の起動完了後に遅延実行する構成に変更した。
    # これにより初回登録時と、Blender再起動後のどちらでもエラーを防げる。

    bpy.utils.register_class(BoneRenamePanel)
    bpy.utils.register_class(RenameSelectedBonesOperator)
    bpy.utils.register_class(RenameGroupsOperator)
    bpy.utils.register_class(RevertNamesOperator)


def unregister():
    bpy.utils.unregister_class(BoneRenamePanel)
    bpy.utils.unregister_class(RenameSelectedBonesOperator)
    bpy.utils.unregister_class(RenameGroupsOperator)
    bpy.utils.unregister_class(RevertNamesOperator)

if __name__ == "__main__":
    register()
