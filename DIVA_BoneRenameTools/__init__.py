bl_info = {
    "name": "DIVA - Bone Rename Tools",
    "author": "Riel",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DIVA",
    "description": "Tools for renaming bones, assigning identifiers, and managing naming rules for armatures",
    # "warning": "バグチェック中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Rename-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons", 
    "category": "Object",
}

import bpy

# デバッグモード切り替え
from . import brt_debug
brt_debug.DEBUG_MODE = False

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
modules = [
    brt_types, 
    brt_panel, 
    brt_preferences, 
    brt_ui_rename, 
    brt_ui_replace, 
    brt_ui_invert, 
    brt_ui_other,
    brt_translation, 
    brt_update
    ]

# register() 内で動的にクラスを取得
def register():
    brt_translation.register()
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
    from .brt_update import brt_on_blend_load
    if brt_on_blend_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(brt_on_blend_load)


def unregister():
    # ハンドラー解除（BLENDファイル読み込み時用）
    from .brt_update import brt_on_blend_load
    if brt_on_blend_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(brt_on_blend_load)

    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()
    brt_translation.unregister()
