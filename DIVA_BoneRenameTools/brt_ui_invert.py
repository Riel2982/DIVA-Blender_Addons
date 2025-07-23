# brt_ui_invert.py

import bpy
from bpy.app.translations import pgettext as _
from .brt_sub import extract_common_group, clean_name

# --- セクション 3: 反転リネーム ------------------------------------------
def panel_invert_ui(layout, context, scene):
    box3 = layout.box()
    row = box3.row(align=True)
    split = row.split(factor=0.85)

    # 左エリア：トグルボタン＋ラベル（常に表示）
    left = split.row(align=True)
    left.prop(scene, "brt_show_invert_tools", text="", 
            icon='DOWNARROW_HLT' if scene.brt_show_invert_tools else 'RIGHTARROW', emboss=False)
    left.label(text="Invert Selected Bones", icon="GROUP_BONE")

    # 右エリア：スポイトツール（開いているときだけ表示）
    right = split.row(align=True)
    right.alignment = 'RIGHT'
    if scene.brt_show_invert_tools:
        right.operator("brt.select_linear_chain", text="", icon="BONE_DATA")

    if scene.brt_show_invert_tools:
        if not hasattr(context.scene, "brt_invert_selected_bones"):
            return  # ← プロパティ未登録なら描画をスキップ

        props = context.scene.brt_invert_selected_bones

        # ボーン識別文字（ドロップダウン）
        row = box3.row()
        split = row.split(factor=0.20, align=True)  # ← ラベル側20%、残りにドロップダウンとボタン
        split.label(text=_("ボーン識別子:"))
        right = split.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        right.prop(props, "bone_pattern", text="")  # ドロップダウン（ラベル非表示）
        right.operator("brt.open_preferences", text="", icon="PREFERENCES")  # 設定ボタン（プリファレンスを開く）

        row = box3.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.prop(scene, "brt_assign_identifier", text="")  # チェックボックス
        row.label(text=_("左右識別子を付与")) # 非連動
        # row.prop(props, "bone_rule", text="") # 判別ペアのドロップダウン（選択中のセットに応じた項目）※ 常時表示版

        if scene.brt_assign_identifier:     # ONならドロップダウン表示
            row.prop(props, "bone_rule", text="")       # 判別ペアのドロップダウン（選択中のセットに応じた項目）
        # else: # 今回はないほうが表示崩れなさそう
            # row.label(text="", icon="BLANK1")        # レイアウト維持用のダミー

        row = box3.row()
        row.prop(scene, "brt_duplicate_and_rename", text="")  # チェックボックス
        row.label(text=_("複製してリネーム")) # 非連動

        if scene.brt_duplicate_and_rename:     # ONなら表示
            row.prop(scene, "brt_bone_x_mirror", text="")       # 複製時のみ選択ボーンをミラーする
            row.label(text=_("選択ボーンをXミラー")) 
                
            if scene.brt_bone_x_mirror:     # ONならドロップダウン表示
                row.prop(scene, "brt_mirror_mode", text="")       # 判別ペアのドロップダウン（選択中のセットに応じた項目）
            if not scene.brt_bone_x_mirror:
                row.label(text=" ", icon="BLANK1")  

        '''
        row = box3.row()
        row.prop(scene, "brt_duplicate_and_rename", text="")  # チェックボックス
        row.label(text=_("複製してリネーム")) # 非連動
        
        row = box3.row()
        row.prop(scene, "brt_bone_x_mirror", text="")  # チェックボックス
        row.label(text=_("選択ボーンをXミラー")) # 非連動

        if scene.brt_bone_x_mirror:     # ONならドロップダウン表示
            row.prop(scene, "brt_mirror_mode", text="")       # 判別ペアのドロップダウン（選択中のセットに応じた項目）
        '''
            
        box3.operator("brt.invert_selected_bones", text=_("選択ボーン反転リネーム"), icon="GROUP_BONE") # 実行ボタン

class BRT_OT_InvertSelectedBones(bpy.types.Operator):
    """選択ボーンの左右反転リネーム"""
    bl_idname = "brt.invert_selected_bones"
    bl_label = "Invert Selected Bones"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("選択ボーンの左右反転リネーム")

    def execute(self, context):
        from .brt_invert import apply_mirrored_rename
        props = context.scene.brt_invert_selected_bones

        renamed = apply_mirrored_rename(
            context,
            pattern_name=props.bone_pattern,
            duplicate=context.scene.brt_duplicate_and_rename,
            # mirror=context.scene.brt_bone_x_mirror,
            mirror=context.scene.brt_duplicate_and_rename and context.scene.brt_bone_x_mirror,  # 複製しない時はミラーしない
            assign_identifier=context.scene.brt_assign_identifier,
            suffix_enum="wj",  # 任意の設定値
            rule_enum="000",   # 任意の設定値
            rule_index=int(props.bone_rule)
        )

        self.report({'INFO'}, f"{renamed}本のボーン名を変更しました")
        return {'FINISHED'}


class BRT_OT_SelectLinearChain(bpy.types.Operator):
    """選択中ボーンから線形チェーン（分岐のない親子構造）を選択"""
    bl_idname = "brt.select_linear_chain"
    bl_label = "線形チェーン選択"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("選択中ボーンから線形チェーンを選択")

    # filter_inconsistentがONの時はallow_branchesがOFF
    def update_filter_inconsistent(self, context):
        if self.filter_inconsistent:
            self["allow_branches"] = False

    # allow_branchesがONの時はfilter_inconsistentがOFF
    def update_allow_branches(self, context):
        if self.allow_branches:
            self["filter_inconsistent"] = False

    filter_inconsistent: bpy.props.BoolProperty(
        name=_("一致しないボーンを除外"),
        description=_("ネーミング規則が共通しないボーンを除外します"),
        default=True,
        update=update_filter_inconsistent       # filter_inconsistentをOFFにする
    )

    allow_branches: bpy.props.BoolProperty(
        name=_("分岐も含める"),
        description=_("分岐先も選択対象に含めます"),
        default=False,
        update=update_allow_branches        #　allow_branchesをOFFにする
    )

    extend_by_common_group: bpy.props.BoolProperty(
        name=_("拡張選択"),
        description=_("数字部分を除いた共通グループ名に一致するボーンを追加選択します"),
        default=False
    )

    def execute(self, context):
        from . import brt_sub

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, _("アーマチュアが選択されていません"))
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
        else:
            self.report({'WARNING'}, _("対応モードは Pose または Edit です"))
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, _("起点となるボーンが選択されていません"))
            return {'CANCELLED'}

        # 共通プレフィックスの抽出（オプションで制御）
        prefix = brt_sub.detect_common_prefix(
            bones=bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        ) if self.filter_inconsistent else None

        brt_sub.select_linear_chain_inclusive(
            bone_name=bones[0].name,
            prefix_filter=prefix,
            allow_branches=self.allow_branches,
            extend_by_common_group=self.extend_by_common_group,
            child_only=False,
            filter_inconsistent=self.filter_inconsistent
        )

        '''
        # 最初に選択されているボーンを起点に線形チェーンを選択
        prefix = brt_sub.detect_common_prefix(
            bones=bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        ) if self.filter_inconsistent else None

        brt_sub.select_linear_chain_inclusive(
            bones[0].name,
            prefix_filter=prefix
        )
        '''

        # ▶ コンソールに選択ボーン名を表示
        print(f"\n▶ [LinearChain] 実行オプション:")
        print(f" - filter_inconsistent: {self.filter_inconsistent}")
        print(f" - allow_branches: {self.allow_branches}")
        print(f" - extend_by_common_group: {self.extend_by_common_group}")

        print(f"▶ 起点ボーン: {bones[0].name}")
        print(f"▶ mode: {context.mode}")
        print(f"▶ prefix_filter: {prefix}")
        print(f"▶ target_group: {extract_common_group(clean_name(bones[0].name))}")

        selected_bones = []
        if mode == 'POSE':
            selected_bones = [b.name for b in obj.pose.bones if b.bone.select]
        elif mode == 'EDIT_ARMATURE':
            selected_bones = [b.name for b in obj.data.edit_bones if b.select]

        print(f"\n▶ [LinearChain] 選択ボーン一覧（{len(selected_bones)}本）:")
        for name in selected_bones:
            print(f" - {name}")        

        self.report({'INFO'}, _("線形チェーンを選択しました"))
        return {'FINISHED'}




#  DIVAアドオン設定画面（プリファレンス）を開く
class BRT_OT_OpenPreferences(bpy.types.Operator):
    bl_idname = "brt.open_preferences"
    bl_label = "DIVA 設定を開く"
    bl_description = _("プリファレンスのアドオン設定画面を開きます")

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")  # Preferences ウィンドウを開く
        context.preferences.active_section = 'ADDONS'
        context.window_manager.addon_search = "diva"
        # アドオン指定でプリファレンスを開きたい場合はアドオンフォルダ名を設定
        # context.window_manager.addon_search = "DIVA_BoneRenameTools"
        return {'FINISHED'}


def get_classes():
    return [
        BRT_OT_InvertSelectedBones,
        BRT_OT_SelectLinearChain,
        BRT_OT_OpenPreferences,
    ]