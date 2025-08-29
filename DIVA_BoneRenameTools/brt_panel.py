import bpy
from bpy.app.translations import pgettext as _
from .brt_ui_rename import panel_rename_ui
from .brt_ui_replace import panel_replace_ui
from .brt_ui_invert import panel_invert_ui
from .brt_ui_other import panel_other_ui

class DIVA_PT_BoneRenamePanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Rename Tools"
    bl_idname = "DIVA_PT_bone_rename"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"
    bl_options = {'DEFAULT_CLOSED'} 

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='GROUP_BONE') # ボーンミラー風

    # UIをセクションごとに分離
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        panel_rename_ui(layout, scene)
        panel_replace_ui(layout, scene)
        panel_invert_ui(layout, context, scene)
        panel_other_ui(layout, scene)




def get_classes():
    return [
        DIVA_PT_BoneRenamePanel,
    ]