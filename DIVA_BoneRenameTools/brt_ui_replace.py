# brt_ui_replace.py

import bpy
from bpy.app.translations import pgettext as _



# --- セクション 2: 指定名で置換 ------------------------------------------
def panel_replace_ui(layout, scene):
    box2 = layout.box()
    row = box2.row(align=True)
    split = row.split(factor=0.85)

    # 左エリア：トグルボタン＋ラベル（常に表示）
    left = split.row(align=True)
    left.prop(scene, "brt_show_replace_tools", text="", 
            icon='DOWNARROW_HLT' if scene.brt_show_replace_tools else 'RIGHTARROW', emboss=False)
    left.label(text="Replace Bone Name", icon="GREASEPENCIL")

    # 右エリア：スポイトツール（開いているときだけ表示）
    right = split.row(align=True)
    right.alignment = 'RIGHT'
    if scene.brt_show_replace_tools:
        right.operator("brt.extract_source_name", text="", icon="BONE_DATA")

    if scene.brt_show_replace_tools:
        # テキストボックスのみ版
        row = box2.row(align=True)
        row.prop(scene, "brt_rename_source_name", text="") # テキストボックス
        row.label(icon='FORWARD')
        row.prop(scene, "brt_rename_target_name", text="") # テキストボックス

        row = box2.row()
        row.prop(scene, "brt_remove_number_suffix", text="")  # チェックボックス
        row.label(text=_("Remove duplicate suffix")) # 非連動

        box2.operator("brt.replace_bone_name", text=_("Rename Bones by Specified Name"), icon="GREASEPENCIL") # 実行ボタン



class BRT_OT_ReplaceBoneName(bpy.types.Operator):
    """ボーン名の一部を一括置換"""
    bl_idname = "brt.replace_bone_name"
    bl_label = "Replace Bone Name"
    bl_description = _("Replace the selected bone name substring in bulk")

    def execute(self, context):
        from .brt_replace import replace_bone_names_by_rule

        src = context.scene.brt_rename_source_name
        tgt = context.scene.brt_rename_target_name

        success, partial, message = replace_bone_names_by_rule(context, src, tgt)

        if not success:
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
        elif partial:
            self.report({'WARNING'}, message)
        else:
            self.report({'INFO'}, _("Bone name replacement completed"))
        return {'FINISHED'}



class BRT_OT_ExtractSourceName(bpy.types.Operator):
    """選択ボーンから置換元名を抽出"""
    bl_idname = "brt.extract_source_name"
    bl_label = "Extract: Source Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("Extract source name from selected bones")
    use_auto_select: bpy.props.BoolProperty(
        name=_("Select Linear Chain"),      # 線形チェーン選択
        description=_("If enabled, automatically selects a linear parent-child chain from selected bone"),
        default=True
    )

    def execute(self, context):
        from .brt_sub import detect_common_prefix, select_linear_chain_inclusive

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, _("No armature is selected"))
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
        else:
            self.report({'WARNING'}, _("Only Pose or Edit mode is supported"))
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, _("No bones are selected"))
            return {'CANCELLED'}

        # ネーミング規則に基づいて共通部分を抽出
        prefix = detect_common_prefix(
            bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        )

        if prefix:
            context.scene.brt_rename_source_name = prefix
            self.report({'INFO'}, _("Detected prefix: {prefix}").format(prefix=prefix))
        else:
            self.report({'WARNING'}, _("Could not detect common prefix"))

        # 自動選択が ON の場合はチェーンを選択
        if self.use_auto_select:
            select_linear_chain_inclusive(
                bones[0].name,
                prefix_filter=prefix
            )

        return {'FINISHED'} if prefix else {'CANCELLED'}



def get_classes():
    return [
        BRT_OT_ReplaceBoneName,
        BRT_OT_ExtractSourceName,
    ]