bl_info = {
    "name": "DIVA - Split Mirror Weight",
    "author": "Riel",
    "version": (0, 1, 5),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "Automatically separates mirrored meshes and applies symmetrical weight copying to vertex groups.",
    "warning": "多言語対応中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Split-Mirror-Weight",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Object",
}

import bpy
from . import smw_translation
from . import smw_types
from . import smw_preferences
from . import smw_panel
from .smw_preferences import load_bone_patterns_to_preferences

# すべてのクラスをまとめる
modules = [smw_types, smw_panel, smw_preferences]

# register() 内で動的にクラスを取得
def register():
    smw_translation.register(__name__)
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
    smw_translation.unregister(__name__)