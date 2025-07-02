bl_info = {
    "name": "DIVA - Bone Transfer Tools",
    "author": "Riel",
    "version": (0, 0, 4),
    "blender": (3, 0, 0),
    "location": "3D View > Sidebar > DIVA",
    "description": "Transfer bones and optionally duplicate b1 object to new armature",
    "warning": "一部のボーンの親が正常にペアレントされない。アドオン登録時やUI表示に不具合の可能性あり",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Bone-Transfer-Tools",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Rigging",
}

import bpy

from . import btt_panel
from . import btt_main
from . import btt_sub

# すべてのクラスをまとめる
modules = [btt_panel, btt_main, btt_sub]
# 定義していたグローバル変数は削除
# classes = [] ← 消してOK

# register() 内で動的にクラスを取得
def register():
    for mod in modules:
        if hasattr(mod, "get_classes"):
            for cls in mod.get_classes():
                bpy.utils.register_class(cls)

    if hasattr(btt_panel, "register_properties"):
        btt_panel.register_properties()

def unregister():
    for mod in reversed(modules):
        if hasattr(mod, "get_classes"):
            for cls in reversed(mod.get_classes()):
                bpy.utils.unregister_class(cls)

    if hasattr(btt_panel, "unregister_properties"):
        btt_panel.unregister_properties()