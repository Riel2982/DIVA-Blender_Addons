# bprs_panel.py

import bpy
from bpy.app.translations import pgettext as _
from .bprs_ui_export import draw_export_ui
# from .bprs_ui_import import draw_import_ui
from .bprs_ui_check import draw_check_ui


class DIVA_PT_BonePositionRotationPanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Position Rotation Scale"
    bl_idname = "DIVA_PT_bone_position_rotation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"
    bl_options = {'DEFAULT_CLOSED'} 

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='SCREEN_BACK') # Export風

    # UIをセクションごとに分離
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        draw_export_ui(layout, context, scene)
        draw_check_ui(layout, context, scene)
        # draw_import_ui(layout, context, scene)


def get_classes():
    return [
        DIVA_PT_BonePositionRotationPanel,
    ]

