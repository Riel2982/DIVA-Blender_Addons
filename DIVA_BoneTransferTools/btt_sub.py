import bpy
class BTT_OT_MergeSelectedMeshes(bpy.types.Operator):
    """ 選択したメッシュを複製し統合するオペレーター """
    bl_idname = "btt.merge_selected_meshes"
    bl_label = "選択メッシュを複製＆統合"

    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objects:
            self.report({'ERROR'}, "選択されたメッシュがありません")
            return {'CANCELLED'}

        bpy.ops.object.duplicate()
        copied_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']

        bpy.ops.object.select_all(action='DESELECT')
        for obj in copied_objects:
            obj.select_set(True)

        bpy.ops.object.join()  # 統合処理
        merged = context.selected_objects[0]
        merged.name = "Merged_Mesh"
        
        self.report({'INFO'}, "選択メッシュを統合しました")
        return {'FINISHED'}
    

# ✅ **Blenderアドオンで使うクラスの登録**
def get_classes():
    return [BTT_OT_MergeSelectedMeshes]
