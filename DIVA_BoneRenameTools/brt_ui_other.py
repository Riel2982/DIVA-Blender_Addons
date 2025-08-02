# brt_ui_other.py

import bpy
from bpy.app.translations import pgettext as _

from .brt_other import rename_bones_and_vertex_groups, revert_renamed_names, rename_selected_bones, revert_selected_bone_names


# --- セクション 4: その他リネームツール操作 ----------------------------------
def panel_other_ui(layout, scene): 
    box4 = layout.box()
    row = box4.row(align=True)
    row.prop(scene, "brt_show_group_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_group_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Other Rename Tools", icon="ARROW_LEFTRIGHT") # セクションタイトル

    if scene.brt_show_group_tools:
        row = box4.row()
        row.operator("brt.rename_groups", text=_("Apply Symmetric Renaming"), icon="PLUS") # 実行ボタン
        row.operator("brt.revert_names", text=_("Remove Symmetric Renaming"), icon="CANCEL") # 実行ボタン



class BRT_OT_RenameGroups(bpy.types.Operator):
    """DIVA式左右識別子にBlenderが認識できる左右識別接尾辞を付与する"""
    bl_idname = "brt.rename_groups"
    bl_label = "Rename Bones & Vertex Groups"
    bl_description = _("Add Blender-recognizable left/right identification suffixes to DIVA-style lateral identifiers")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        mode = context.mode

        if mode == 'OBJECT':
            if not obj or obj.type != 'ARMATURE':
                self.report({'WARNING'}, _("No armature is selected"))
                return {'CANCELLED'}

            rename_bones_and_vertex_groups()

            self.report({'INFO'}, _("Symmetric renaming applied successfully"))

            return {'FINISHED'}

        elif mode in {'EDIT_ARMATURE', 'POSE'}:
            selected = []
            if mode == 'EDIT_ARMATURE':
                selected = [b for b in obj.data.edit_bones if b.select]
            else:
                selected = [pb for pb in obj.pose.bones if pb.bone.select]

            if not selected:
                self.report({'WARNING'}, _("No bones selected"))
                return {'CANCELLED'}

            renamed = rename_selected_bones()

            if renamed == 0:
                self.report({'WARNING'}, _("No bone name with left/right identifier was found"))
                return {'CANCELLED'}

            self.report({'INFO'}, _("Symmetric renaming applied successfully"))

            return {'FINISHED'}

        self.report({'WARNING'}, _("No armature is selected"))
        return {'CANCELLED'}


class BRT_OT_RevertNames(bpy.types.Operator):
    """名前を元に戻す"""
    bl_idname = "brt.revert_names"
    bl_label = "Revert Renamed Names"
    bl_description = _("Revert left/right identification suffixes")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        mode = context.mode

        if mode == 'OBJECT':
            if not obj or obj.type != 'ARMATURE':
                self.report({'WARNING'}, _("No armature is selected"))
                return {'CANCELLED'}
          
            revert_renamed_names()

            self.report({'INFO'}, _("Symmetric renaming reverted"))
            return {'FINISHED'}

        elif mode in {'EDIT_ARMATURE', 'POSE'}:
            selected = []
            if mode == 'EDIT_ARMATURE':
                selected = [b for b in obj.data.edit_bones if b.select]
            else:
                selected = [pb for pb in obj.pose.bones if pb.bone.select]

            if not selected:
                self.report({'WARNING'}, _("No bones selected"))
                return {'CANCELLED'}

            reverted = revert_selected_bone_names()

            if reverted == 0:
                self.report({'WARNING'}, _("Undo target identifier not found"))
                return {'CANCELLED'}

            self.report({'INFO'}, _("Symmetric renaming reverted"))
            return {'FINISHED'}

        self.report({'WARNING'}, _("No armature is selected"))
        return {'CANCELLED'}







def get_classes():
    return [
        BRT_OT_RenameGroups,
        BRT_OT_RevertNames,
    ]