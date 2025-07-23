bl_info = {
    "name": "DIVA - Bone Rename Tools",
    "author": "Riel",
    "version": (0, 0, 10),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DIVA",
    "description": "Tools for renaming bones, assigning identifiers, and managing naming rules for armatures",
    # "warning": "多言語対応途中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Rename-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons", 
    "category": "Object",
}

import bpy
import bpy.app.timers

from . import (
    brt_translation,
    brt_panel,
    brt_preferences,
    brt_types,
    brt_update,
)

# Panel-UI機能モジュール
from . import (
    brt_ui_rename,
    brt_ui_replace,
    brt_ui_invert,
    brt_ui_other,
)
from .brt_preferences import load_bone_patterns_to_preferences


# すべてのクラスをまとめる
modules = [brt_types, brt_panel, brt_preferences, brt_ui_rename, brt_ui_replace, brt_ui_invert, brt_ui_other,brt_translation, brt_update]

# register() 内で動的にクラスを取得
def register():
    brt_translation.register()
    for mod in modules:
        if hasattr(mod, "get_classes"):
            for cls in mod.get_classes():
                bpy.utils.register_class(cls)

        if hasattr(mod, "register_properties"):
            mod.register_properties()

        def delayed_initialize():
            if hasattr(mod, "initialize_candidate_list"):
                mod.initialize_candidate_list()
            return None  # 一度だけでOK
        bpy.app.timers.register(delayed_initialize)

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
    brt_translation.unregister()
