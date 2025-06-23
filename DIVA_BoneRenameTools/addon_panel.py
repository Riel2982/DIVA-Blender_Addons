import bpy

class BoneRenamePanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Rename Tools"
    bl_idname = "DIVA_PT_BoneRenamePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='GROUP_BONE') # ボーンミラー風

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box1 = layout.box() # 枠付きセクションを作成

        # box1.label(text="ボーン連番リネーム")
        row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.prop(scene, "rename_prefix", text="共通部分") # 共通部分入力
        row.operator("object.detect_common_prefix", text="", icon='EYEDROPPER') # スポイトアイコンボタン

        row1 = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row1.prop(scene, "rename_start_number", text="連番開始番号") # 連番開始番号
        row1.prop(scene, "rename_rule", text="法則") # 連番法則選択
        row1.prop(scene, "rename_suffix", text="末尾") # 末尾選択
        # box1.prop(scene, "rename_start_number") # 連番開始番号
        # box1.prop(scene, "rename_suffix") # 末尾選択
        # box1.prop(scene, "rename_rule") # 連番法則選択

        box1.operator("object.rename_selected_bones", text="連番リネーム実行")
        
        # 折りたたみ式ツールボックス
        row = box1.row(align=True)
        row.prop(scene, "show_symmetric_tools", text="", icon='TRIA_DOWN' if scene.show_symmetric_tools else 'TRIA_RIGHT', emboss=False)
        row.label(text="その他リネームツール")

        if scene.show_symmetric_tools:
            # 変更前後のボーン名入力フィールド（横並び）
            row = box1.row(align=True)

            col1 = row.column()
            col1.prop(scene, "rename_source_name", text="")  # 左のテキストボックス

            col2 = row.column()
            col2.label(icon='FORWARD')  # または 'TRIA_RIGHT', 'PLAY'

            col3 = row.column()
            col3.prop(scene, "rename_target_name", text="")  # 右のテキストボックス

            # 実行ボタンを下に配置
            box1.operator("object.rename_bone_pair", text="指定名でボーン名変更")
            
            box1.separator()
            row2 = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row2.operator("object.invert_selected_bones", text="選択ボーン反転リネーム")# 上から順に左側から設置
            row2.operator("object.rename_groups", text="全対称化付与")
            row2.operator("object.revert_names", text="全対称化削除")


class RenameSelectedBonesOperator(bpy.types.Operator):
    """ボーン連番リネーム"""
    bl_idname = "object.rename_selected_bones"
    bl_label = "Rename Selected Bones"

    def execute(self, context):
        from .rename_bones import rename_selected_bones
        rename_selected_bones(
            context.scene.rename_prefix,
            context.scene.rename_start_number,
            context.scene.rename_suffix,
            context.scene.rename_rule
        )
        return {'FINISHED'}

class DetectCommonPrefixOperator(bpy.types.Operator):
    """選択ボーン名の共通部分を抽出 または 線形チェーン選択"""
    bl_idname = "object.detect_common_prefix"
    bl_label = "共通部分を検出"
    bl_options = {'REGISTER', 'UNDO'}

    use_auto_select: bpy.props.BoolProperty(
        name="線形チェーンを選択",
        description="ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        default=True
    )

    filter_inconsistent: bpy.props.BoolProperty(
        name="共通部分に一致しないボーンを除外",
        description="明らかにネーミングルールが異なるボーンを共通抽出対象から除外します",
        default=True
    )

    def execute(self, context):
        from . import rename_detect  # 外部ロジックに分離

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "アーマチュアが選択されていません")
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
            clear_selection = lambda: bpy.ops.pose.select_all(action='DESELECT')
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
            clear_selection = lambda: [setattr(b, "select", False) for b in bones]
        else:
            self.report({'WARNING'}, "対応しているのは Pose モードまたは Edit モードです")
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, "ボーンが選択されていません")
            return {'CANCELLED'}

        # 共通プレフィックス名を抽出
        prefix = rename_detect.detect_common_prefix(
            bones=bones,
            suffix_enum=context.scene.rename_suffix,
            rule_enum=context.scene.rename_rule
        )

        if prefix:
            context.scene.rename_prefix = prefix
            self.report({'INFO'}, f"共通部分を設定: {prefix}")
        else:
            self.report({'WARNING'}, "共通部分が検出できませんでした")

        # use_auto_select が ON の場合は選択処理も行う
        if self.use_auto_select:
            rename_detect.select_linear_chain_inclusive(
                bones[0].name,
                prefix_filter=prefix if self.filter_inconsistent else None
            )

        return {'FINISHED'} if prefix else {'CANCELLED'}

class RenameGroupsOperator(bpy.types.Operator):
    """特定単語リネーム"""
    bl_idname = "object.rename_groups"
    bl_label = "Rename Bones & Vertex Groups"

    def execute(self, context):
        from .rename_groups import rename_bones_and_vertex_groups
        rename_bones_and_vertex_groups()
        return {'FINISHED'}

class RevertNamesOperator(bpy.types.Operator):
    """名前を元に戻す"""
    bl_idname = "object.revert_names"
    bl_label = "Revert Renamed Names"

    def execute(self, context):
        from .rename_groups import revert_renamed_names
        revert_renamed_names()
        return {'FINISHED'}

class InvertSelectedBonesOperator(bpy.types.Operator):
    """選択ボーンの左右反転リネーム"""
    bl_idname = "object.invert_selected_bones"
    bl_label = "Invert Selected Bones"

    def execute(self, context):
        # （後でロジックを実装する場合はここに）
        self.report({'INFO'}, "選択ボーンの反転リネームを実行しました（仮動作）")
        return {'FINISHED'}

class RenameBonePairOperator(bpy.types.Operator):
    """ボーン名の一部を一括変更"""
    bl_idname = "object.rename_bone_pair"
    bl_label = "Rename Bone by Name"

    def execute(self, context):
        src = context.scene.rename_source_name
        tgt = context.scene.rename_target_name

        for obj in context.selected_objects:
            if obj.type == 'ARMATURE':
                for bone in obj.data.bones:
                    if bone.name == src:
                        bone.name = tgt

        return {'FINISHED'}