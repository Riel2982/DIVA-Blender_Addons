# fop_panel.py

import bpy
import addon_utils

from bpy.app.translations import pgettext as _

from .fop_ui_save import draw_save_ui
from .fop_ui_import import draw_import_ui
from .fop_ui_export import draw_export_ui

from .fop_debug import DEBUG_MODE   # デバッグ用

class DIVA_PT_FBXOperationPackPanel(bpy.types.Panel):
    bl_label = "FBX Operation Pack"
    bl_idname = "VIEW3D_PT_diva_fbx_operation_pack"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"
    bl_options = {'DEFAULT_CLOSED'} 

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MESH_MONKEY')    # 'ARMATURE_DATA'

    # UIをセクションごとに分離
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if is_fbx_addon_enabled():  # FBX Formatアドオン有効化時
            # 各セクション描画        
            draw_save_ui(layout, self, context, scene)
            draw_import_ui(layout, context, scene)
            draw_export_ui(layout, context, scene)

        else:   # FBX Formatアドオン無効化時
            box = layout.box()
            box.label(text=_("Please enable Blenders built-in FBX format addon"), icon='ERROR')
            box.operator("preferences.addon_show_fbx", text="FBX Formatアドオンを有効化する", icon='PREFERENCES')



# FBX Format アドオンの確認
def is_fbx_addon_enabled():
    return addon_utils.check("io_scene_fbx")[1]

# FBXアドオン設定を開くオペレーター
class FOP_OT_ShowFBXAddonPreferences(bpy.types.Operator):
    bl_idname = "preferences.addon_show_fbx"
    bl_label = "Show FBX Addon Preferences"
    bl_description = _("Open the FBX Format addon settings in Preferences")

    def execute(self, context):
        bpy.ops.preferences.addon_show(module="io_scene_fbx")
        return {'FINISHED'}


def get_classes():
    return [
        DIVA_PT_FBXOperationPackPanel,
        FOP_OT_ShowFBXAddonPreferences,
    ]
