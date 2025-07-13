# brt_ui_other.py

import bpy
from bpy.app.translations import pgettext as _

# --- セクション 4: その他リネームツール操作 ----------------------------------
def panel_other_ui(layout, scene): 
    box4 = layout.box()
    row = box4.row(align=True)
    row.prop(scene, "brt_show_group_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_group_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Other Rename Tools", icon="ARROW_LEFTRIGHT") # セクションタイトル

    if scene.brt_show_group_tools:
        row = box4.row()
        row.operator("brt.rename_groups", text=_("全対称化付与"), icon="PLUS") # 実行ボタン
        row.operator("brt.revert_names", text=_("全対称化削除"), icon="CANCEL") # 実行ボタン



class BRT_OT_RenameGroups(bpy.types.Operator):
    """特定単語リネーム"""
    bl_idname = "brt.rename_groups"
    bl_label = "Rename Bones & Vertex Groups"

    def execute(self, context):
        from .brt_other import rename_bones_and_vertex_groups
        rename_bones_and_vertex_groups()
        return {'FINISHED'}

class BRT_OT_RevertNames(bpy.types.Operator):
    """名前を元に戻す"""
    bl_idname = "brt.revert_names"
    bl_label = "Revert Renamed Names"

    def execute(self, context):
        from .brt_other import revert_renamed_names
        revert_renamed_names()
        return {'FINISHED'}





def get_classes():
    return [
        BRT_OT_RenameGroups,
        BRT_OT_RevertNames,
    ]