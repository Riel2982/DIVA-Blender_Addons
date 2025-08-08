bl_info = {
    "name": "DIVA - Bone Position Rotation Scale",
    "author": "Saltlapse, Riel",
    "version": (0, 2, 0),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "This addon converts bone data from Blender armatures into the DIVA format.",
    # "warning": "デバッグ中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Position-Rotation-Scale",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Rigging",
}

import bpy

# デバッグモード切り替え
from . import bprs_debug
bprs_debug.DEBUG_MODE = False

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

        def delayed_initialize():   # BLENDER起動時用
            if hasattr(mod, "initialize_candidate_list"):
                mod.initialize_candidate_list()
            return None  # 一度だけでOK
        bpy.app.timers.register(delayed_initialize)

    # ハンドラー登録（BLENDファイル読み込み時）
    from .bprs_update import bprs_on_blend_load
    if bprs_on_blend_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(bprs_on_blend_load)        


def unregister():
    # ハンドラー解除（BLENDファイル読み込み時用）
    from .bprs_update import bprs_on_blend_load
    if bprs_on_blend_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(bprs_on_blend_load)

    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()

    bprs_translation.unregister()
