bl_info = {
    "name": "DIVA - Bone Position Rotation Scale",
    "author": "Saltlapse, Riel",
    "version": (0, 1, 1),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "This addon converts bone data from Blender armatures into the DIVA format.",
    # "warning": "特になし",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Position-Rotation-Scale",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Rigging",
}


import bpy.app.timers

from . import (
    bprs_translation,
    bprs_panel,
    # bprs_preferences,
    bprs_types,
    bprs_update,
)

# Panel-UI機能モジュール
from . import (
    bprs_ui_export,
    # bprs_ui_import,
    bprs_ui_check,
)


# すべてのクラスをまとめる
modules = [
    bprs_types, 
    bprs_panel, 
    # bprs_preferences, 
    bprs_ui_export,
    # bprs_ui_import, 
    bprs_ui_check, 
    bprs_translation, 
    bprs_update,
    ]

# register() 内で動的にクラスを取得
def register():
    bprs_translation.register()
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
        


def unregister():
    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()

    bprs_translation.unregister()
