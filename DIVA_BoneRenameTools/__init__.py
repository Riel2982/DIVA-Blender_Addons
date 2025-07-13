bl_info = {
    "name": "DIVA - Bone Rename Tools",
    "author": "Riel",
    "version": (0, 0, 8),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DIVA",
    "description": "Nパネルからボーンと頂点グループをリネームするアドオン",
    "warning": "oppaiボーンの左右反転不具合あり / 多言語対応途中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Rename-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons", 
    "category": "Object",
}

import bpy
from . import brt_translation
from . import brt_panel
from . import brt_preferences
from . import brt_types
from . import brt_ui_rename
from . import brt_ui_replace
from . import brt_ui_invert
from . import brt_ui_other
from . import brt_update
from .brt_preferences import load_bone_patterns_to_preferences


# すべてのクラスをまとめる
modules = [brt_types, brt_panel, brt_preferences, brt_ui_rename, brt_ui_replace, brt_ui_invert, brt_ui_other, brt_update]

# register() 内で動的にクラスを取得
def register():
    brt_translation.register(__name__)
    for mod in modules:
        if hasattr(mod, "get_classes"):
            for cls in mod.get_classes():
                bpy.utils.register_class(cls)

        if hasattr(mod, "register_properties"):
            mod.register_properties()

    addon = bpy.context.preferences.addons.get(__name__)
    if addon:
        load_bone_patterns_to_preferences(addon.preferences)


def unregister():
    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()
    brt_translation.unregister(__name__)
