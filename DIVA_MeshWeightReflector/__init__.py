bl_info = {
    "name": "DIVA - Mesh Weight Reflector",
    "author": "Riel",
    "version": (0, 0, 3),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "Automatically separates mirrored meshes and applies symmetrical weight copying to vertex groups.",
    # "warning": "デバッグ中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Mesh-Weight-Reflector",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Object",
}

import bpy

# デバッグモード切り替え
from . import mwr_debug
mwr_debug.DEBUG_MODE = False

from . import (
    mwr_translation,
    mwr_panel,
    mwr_preferences,
    mwr_types,
    mwr_update,
)
from .mwr_preferences import load_bone_patterns_to_preferences

# すべてのクラスをまとめる
modules = [
    mwr_types, 
    mwr_panel, 
    mwr_preferences, 
    mwr_translation, 
    mwr_update,
    ]

# register() 内で動的にクラスを取得
def register():
    mwr_translation.register()
    for mod in modules:
        if hasattr(mod, "get_classes"):
            for cls in mod.get_classes():
                bpy.utils.register_class(cls)

        if hasattr(mod, "register_properties"):
            mod.register_properties()

        def delayed_initialize():   # BLENDER起動時用
            if hasattr(mod, "initialize_candidate_list"):
                mod.initialize_candidate_list()
            return None  # 一度だけでOK
        bpy.app.timers.register(delayed_initialize)

    addon = bpy.context.preferences.addons.get(__name__)
    if addon:
        load_bone_patterns_to_preferences(addon.preferences)

    # ハンドラー登録（BLENDファイル読み込み時）
    from .mwr_update import mwr_on_blend_load
    if mwr_on_blend_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(mwr_on_blend_load)


def unregister():
    # ハンドラー解除（BLENDファイル読み込み時用）
    from .mwr_update import mwr_on_blend_load
    if mwr_on_blend_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(mwr_on_blend_load)

    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()

    mwr_translation.unregister()