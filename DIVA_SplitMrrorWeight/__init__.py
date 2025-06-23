bl_info = {
    "name": "DIVA - Split Mirror Weight",
    "author": "Riel",
    "version": (0, 1, 3),
    "blender": (3, 0, 0),
    "location": "Nパネル > DIVA",
    "description": "Automatically separates mirrored meshes and applies symmetrical weight copying to vertex groups.",
    "warning": "X軸を超えたメッシュがある時のミラーは非対応",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Riel2982/DIVA-Blender_Addons/wiki/DIVA-%E2%80%90-Split-Mirror-Weight",
    "tracker_url": "https://github.com/Riel2982/DIVA-Blender_Addons",
    "category": "Object",
}

import bpy

from .addon_panel import (
    SplitMirrorWeightPanel,
    DIVA_OT_OpenPreferences,
    OBJECT_OT_SplitMirrorWeight,
    SplitMirrorWeightProperties,
)

from .addon_preferences import (
    DIVAAddonPreferences,
    DIVA_OT_AddBonePattern,
    DIVA_OT_AddBoneRule,
    DIVA_OT_DeleteBonePattern,
    DIVA_OT_DeleteBoneRule,
    DIVA_OT_MoveBonePatternUp,
    DIVA_OT_MoveBonePatternDown,
    DIVA_OT_ResetBonePatterns,
    DIVA_OT_SaveBonePatterns,
    DIVA_OT_AppendDefaultSet,
    load_bone_patterns_to_preferences,
	BoneRuleItem,
	BonePatternItem,
)

def register():
    for cls in (
        BoneRuleItem,
        BonePatternItem,
        DIVAAddonPreferences,
        DIVA_OT_AddBonePattern,
        DIVA_OT_AddBoneRule,
        DIVA_OT_DeleteBonePattern,
        DIVA_OT_DeleteBoneRule,
        DIVA_OT_MoveBonePatternUp,
        DIVA_OT_MoveBonePatternDown,
        DIVA_OT_ResetBonePatterns,
        DIVA_OT_SaveBonePatterns,
        DIVA_OT_AppendDefaultSet,
        SplitMirrorWeightPanel,
        DIVA_OT_OpenPreferences,
        OBJECT_OT_SplitMirrorWeight,
        SplitMirrorWeightProperties,
    ):
        bpy.utils.register_class(cls)

    bpy.types.Scene.split_mirror_weight = bpy.props.PointerProperty(type=SplitMirrorWeightProperties)

    addon = bpy.context.preferences.addons.get(__name__)
    if addon:
        load_bone_patterns_to_preferences(addon.preferences)

def unregister():
    del bpy.types.Scene.split_mirror_weight

    for cls in reversed((
        BoneRuleItem,
        BonePatternItem,
        DIVAAddonPreferences,
        DIVA_OT_AddBonePattern,
        DIVA_OT_AddBoneRule,
        DIVA_OT_DeleteBonePattern,
        DIVA_OT_DeleteBoneRule,
        DIVA_OT_MoveBonePatternUp,
        DIVA_OT_MoveBonePatternDown,
        DIVA_OT_ResetBonePatterns,
        DIVA_OT_SaveBonePatterns,
        DIVA_OT_AppendDefaultSet,
        SplitMirrorWeightPanel,
        DIVA_OT_OpenPreferences,
        OBJECT_OT_SplitMirrorWeight,
        SplitMirrorWeightProperties,
    )):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()