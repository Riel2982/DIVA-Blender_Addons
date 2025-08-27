bl_info = {
    "name": "DIVA - FBX Operation Pack",
    "author": "Riel",
    "version": (0, 0, 5),
    "blender": (3, 0, 0),
    "location": "3D View > Sidebar > DIVA > FBX Oparation Pack",
    "description": "DIVAモデル用のFBXのインポート・エクスポートをサポートするツール",
    "warning": "構築中",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-FBX-Operation-Pack",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Import-Export",
}

import bpy

# デバッグモード切り替え
from . import fop_debug
fop_debug.DEBUG_MODE = False

import bpy.app.timers

from . import (
    fop_translation,
    fop_panel,
    fop_types,
    fop_update,
)

# Panel-UI機能モジュール
from . import (
    fop_ui_save,
    fop_ui_import,
    fop_ui_export,
    fop_uix_update,
)


# すべてのクラスをまとめる
modules = [
    fop_types, 
    fop_panel, 
    fop_ui_save,
    fop_ui_import, 
    fop_ui_export,
    fop_uix_update,
    ]


# register() 内で動的にクラスを取得
def register():
    from .fop_update import fop_on_blend_load
    from .fop_save import fop_on_blend_load_or_save

    fop_translation.register()
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

    # アドオン有効化時に実行
    def delayed_init():
        if getattr(bpy.context, "scene", None):
            fop_update.initialize_candidate_list()
            return None  # 一度だけでOK
        return 0.2  # scene がまだない場合は再試行
    bpy.app.timers.register(delayed_init)


    # ハンドラー登録（BLENDファイル読み込み時）
    if fop_on_blend_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(fop_on_blend_load) 
        
    # Blendファイル保存パス自動取得
    for name in ["load_post", "save_post"]:
        handler_list = getattr(bpy.app.handlers, name)
        if fop_on_blend_load_or_save not in handler_list:
            handler_list.append(fop_on_blend_load_or_save)



def unregister():
    from .fop_update import fop_on_blend_load
    from .fop_save import fop_on_blend_load_or_save

    # Blensファイル自動反映用
    for name in ["load_post", "save_post"]:
        handler_list = getattr(bpy.app.handlers, name)
        if fop_on_blend_load_or_save not in handler_list:
            handler_list.remove(fop_on_blend_load_or_save)
    # ハンドラー解除（BLENDファイル読み込み時用）
    if fop_on_blend_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(fop_on_blend_load)


    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

        if hasattr(mod, "unregister_properties"):
            mod.unregister_properties()

    fop_translation.unregister()
