bl_info = {
    "name": "DIVA - Split Mirror Weight",
    "author": "Riel",
    "version": (1, 3),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "DIVA-CustomRigMirror",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Split-Mirror-Weight",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Object",
}

import bpy
import importlib
from .addon_panel import (
    SplitMirrorWeightProperties,
    OBJECT_OT_SplitMirrorWeight,
    SplitMirrorWeightPanel
)

# 登録・解除
def register():
    bpy.utils.register_class(SplitMirrorWeightProperties)
    bpy.utils.register_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.register_class(SplitMirrorWeightPanel)
    bpy.types.Scene.split_mirror_weight = bpy.props.PointerProperty(type=SplitMirrorWeightProperties)

def unregister():
    bpy.utils.unregister_class(SplitMirrorWeightProperties)
    bpy.utils.unregister_class(OBJECT_OT_SplitMirrorWeight)
    bpy.utils.unregister_class(SplitMirrorWeightPanel)
    del bpy.types.Scene.split_mirror_weight

if __name__ == "__main__":
    register()