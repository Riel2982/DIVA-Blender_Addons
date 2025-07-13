# brt_ui_rename.py

import bpy
from bpy.app.translations import pgettext as _

# --- セクション 1: ボーン連番リネーム -------------------------------------
def panel_rename_ui(layout, scene):
    box1 = layout.box()
    row = box1.row(align=True)
    row.prop(scene, "brt_show_renumber_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_renumber_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Rename Selected Bones", icon="PRESET") # セクションタイトル

    if scene.brt_show_renumber_tools:
        row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.prop(scene, "brt_rename_prefix", text=_("共通部分")) # テキストボックス
        row.operator("brt.detect_common_prefix", text="", icon='BONE_DATA') # スポイトツール

        row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.prop(scene, "brt_rename_start_number", text=_("連番開始番号"))
        row.prop(scene, "brt_rename_rule", text=_("法則")) # ドロップダウン
        row.prop(scene, "brt_rename_suffix", text=_("末尾")) # ドロップダウン

        box1.operator("brt.rename_selected_bones", text=_("連番リネーム実行"), icon="PRESET") # 実行ボタン


class BRT_OT_RenameSelectedBones(bpy.types.Operator):
    """ボーン連番リネーム"""
    bl_idname = "brt.rename_selected_bones"
    bl_label = "Rename Selected Bones"
    bl_description = _("Renames the selected bone rows based on the specified settings")

    def execute(self, context):
        from .brt_rename import rename_selected_bones
        rename_selected_bones(
            context.scene.brt_rename_prefix,
            context.scene.brt_rename_start_number,
            context.scene.brt_rename_suffix,
            context.scene.brt_rename_rule
        )
        return {'FINISHED'}

class BRT_OT_DetectCommonPrefix(bpy.types.Operator):
    """選択ボーン名の共通部分を抽出 または 線形チェーン選択"""
    bl_idname = "brt.detect_common_prefix"
    bl_label = _("共通部分を検出")
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("選択ボーン名の共通部分を抽出 または 線形チェーン選択")

    use_auto_select: bpy.props.BoolProperty(
        name=_("線形チェーンを選択"),
        description=_("ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"),
        default=True
    )

    filter_inconsistent: bpy.props.BoolProperty(
        name=_("一致しないボーンを除外"),
        description=_("明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"),
        default=True
    )

    def execute(self, context):
        from . import brt_sub  # 外部ロジックに分離

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, _("アーマチュアが選択されていません"))
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
            clear_selection = lambda: bpy.ops.pose.select_all(action='DESELECT')
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
            clear_selection = lambda: [setattr(b, "select", False) for b in bones]
        else:
            self.report({'WARNING'}, _("対応しているのは Pose モードまたは Edit モードです"))
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, _("ボーンが選択されていません"))
            return {'CANCELLED'}

        # 共通プレフィックス名を抽出
        prefix = brt_sub.detect_common_prefix(
            bones=bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        )

        if prefix:
            context.scene.brt_rename_prefix = prefix
            self.report({'INFO'}, f"共通部分を設定: {prefix}")
        else:
            self.report({'WARNING'}, _("共通部分が検出できませんでした"))

        # use_auto_select が ON の場合は選択処理も行う
        if self.use_auto_select:
            brt_sub.select_linear_chain_inclusive(
                bones[0].name,
                prefix_filter=prefix if self.filter_inconsistent else None
            )

        return {'FINISHED'} if prefix else {'CANCELLED'}

    





def get_classes():
    return [
        BRT_OT_DetectCommonPrefix,
        BRT_OT_RenameSelectedBones,
    ]