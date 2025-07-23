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

        row = box1.row()
        row.prop(scene, "brt_end_bone_plus", text=(""))       # 末端にボーンを追加するチェックボックス
        row.label(text=_("末端にボーンを追加する"))
        if scene.brt_end_bone_plus:     # ONなら表示
            row.prop(scene, "brt_add_bones", text=_("追加ボーン数"))     # 追加ボーン数選択
        
        box1.operator("brt.rename_selected_bones", text=_("連番リネーム実行"), icon="PRESET") # 実行ボタン


class BRT_OT_RenameSelectedBones(bpy.types.Operator):
    """ボーン連番リネーム"""
    bl_idname = "brt.rename_selected_bones"
    bl_label = "Rename Selected Bones"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("Renames the selected bone rows based on the specified settings")

    def execute(self, context):
        from .brt_rename import rename_selected_bones, find_terminal_bones, extend_and_subdivide_bone
        print("分割付きリネーム開始")

        if bpy.context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')

        obj = context.object
        bones = obj.data.edit_bones

        selected_before_split = [b for b in bones if b.select]

        if context.scene.brt_end_bone_plus and context.scene.brt_add_bones > 0:
            existing_names = set(b.name for b in bones)
            terminals = find_terminal_bones(selected_before_split)
            for bone in terminals:
                extend_and_subdivide_bone(bone, context.scene.brt_add_bones)
            added_bones = [b for b in bones if b.name not in existing_names]
        else:
            added_bones = []

        # 選択状態を復元（分割前 + 分割後）
        bpy.ops.armature.select_all(action='DESELECT')
        for b in selected_before_split + added_bones:
            b.select = True

        rename_selected_bones(
            context.scene.brt_rename_prefix,
            context.scene.brt_rename_start_number,
            context.scene.brt_rename_suffix,
            context.scene.brt_rename_rule
        )

        print("完了")
        return {'FINISHED'}

class BRT_OT_DetectCommonPrefix(bpy.types.Operator):
    """選択ボーン名の共通部分を抽出 または 線形チェーン選択"""
    bl_idname = "brt.detect_common_prefix"
    bl_label = _("共通部分を検出")
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("選択ボーン名の共通部分を抽出し、設定を自動反映します")

    # 従属オプションがONの時主オプションをONにする
    def enable_auto_select(self, context):
        if not self.use_auto_select:
            self["use_auto_select"] = True

    # オプション定義（update付き）
    def update_settings(self, context):
        # use_auto_select切替時に代表ボーンと設定を再抽出するためUI更新を行う為
        from .brt_rename import update_rename_settings_from_selection
        update_rename_settings_from_selection(context.scene)
        
        # 主オプション（use_auto_select）がOFFなら従属オプションもOFFにする
        if not self.use_auto_select:
            self["select_children_only"] = False
            self["filter_inconsistent"] = False


    use_auto_select: bpy.props.BoolProperty(
        name=_("線形チェーンを選択"),
        description=_("ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"),
        default=True,
        update=update_settings
    )

    select_children_only: bpy.props.BoolProperty(
        name=_("末端方向のみ選択"),
        description=_("ONの場合、最初に選択されたボーンから末端までを対象とします"),
        default=False,
        # update=update_settings,
        update=enable_auto_select       # 主オプションをON
    )

    filter_inconsistent: bpy.props.BoolProperty(
        name=_("一致しないボーンを除外"),
        description=_("明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"),
        default=True,
        # update=update_settings,
        update=enable_auto_select       # 主オプションをON
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
                bone_name=bones[0].name,
                prefix_filter=prefix if self.filter_inconsistent else None,
                allow_branches=False,
                extend_by_common_group=False,
                child_only=self.select_children_only  # ← ここで切り替え
            )
        '''
        if self.use_auto_select:
            if self.select_children_only:
                brt_sub.select_child_chain_only(        # 末端方向のみ
                    bones[0].name,
                    prefix_filter=prefix if self.filter_inconsistent else None
                )
            else:
                brt_sub.select_linear_chain_inclusive(
                    bones[0].name,
                    prefix_filter=prefix if self.filter_inconsistent else None
                )
        '''
                
        from .brt_rename import extract_rename_settings

        # 代表ボーン決定（先頭 or 選択ボーン）
        ref_bone = bones[0]
        if self.use_auto_select and not self.select_children_only:
            from .brt_rename import get_linear_chain  # ✅ 正しいモジュールから import
            chain = get_linear_chain(ref_bone.name, prefix_filter=prefix)
            if chain:
                ref_bone = chain[0]

        # 設定抽出関数を呼び出し
        scene = context.scene
        start_num, rule, suffix = extract_rename_settings(ref_bone.name, prefix_filter=prefix)
        scene.brt_rename_start_number = start_num
        scene.brt_rename_rule = rule
        scene.brt_rename_suffix = suffix

        return {'FINISHED'} if prefix else {'CANCELLED'}

    





def get_classes():
    return [
        BRT_OT_DetectCommonPrefix,
        BRT_OT_RenameSelectedBones,
    ]