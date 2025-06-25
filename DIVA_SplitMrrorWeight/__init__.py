bl_info = {
    "name": "DIVA - Split Mirror Weight",
    "author": "Riel",
    "version": (0, 1, 4),
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

from .smw_panel import (
    SplitMirrorWeightPanel,
    SMW_OT_OpenPreferences,
    OBJECT_OT_SplitMirrorWeight,
    SplitMirrorWeightProperties,
)

from .smw_preferences import (
    SMW_AddonPreferences,
    SMW_OT_AddBonePattern,
    SMW_OT_AddBoneRule,
    SMW_OT_DeleteBonePattern,
    SMW_OT_DeleteBoneRule,
    SMW_OT_MoveBonePatternUp,
    SMW_OT_MoveBonePatternDown,
    SMW_OT_ResetBonePatterns,
    SMW_OT_SaveBonePatterns,
    SMW_OT_AppendDefaultSet,
    load_bone_patterns_to_preferences,
	SMW_BoneRuleItem,
	SMW_BonePatternItem,
)

def register():
    for cls in (
        SMW_BoneRuleItem,
        SMW_BonePatternItem,
        SMW_AddonPreferences,
        SMW_OT_AddBonePattern,
        SMW_OT_AddBoneRule,
        SMW_OT_DeleteBonePattern,
        SMW_OT_DeleteBoneRule,
        SMW_OT_MoveBonePatternUp,
        SMW_OT_MoveBonePatternDown,
        SMW_OT_ResetBonePatterns,
        SMW_OT_SaveBonePatterns,
        SMW_OT_AppendDefaultSet,
        SplitMirrorWeightPanel,
        SMW_OT_OpenPreferences,
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
        SMW_BoneRuleItem,
        SMW_BonePatternItem,
        SMW_AddonPreferences,
        SMW_OT_AddBonePattern,
        SMW_OT_AddBoneRule,
        SMW_OT_DeleteBonePattern,
        SMW_OT_DeleteBoneRule,
        SMW_OT_MoveBonePatternUp,
        SMW_OT_MoveBonePatternDown,
        SMW_OT_ResetBonePatterns,
        SMW_OT_SaveBonePatterns,
        SMW_OT_AppendDefaultSet,
        SplitMirrorWeightPanel,
        SMW_OT_OpenPreferences,
        OBJECT_OT_SplitMirrorWeight,
        SplitMirrorWeightProperties,
    )):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()