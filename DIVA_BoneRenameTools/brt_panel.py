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

        # --- セクション 1: ボーン連番リネーム -------------------------------------
        box1 = layout.box()
        row = box1.row(align=True)
        row.prop(scene, "brt_show_renumber_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_renumber_tools else 'RIGHTARROW', emboss=False)
        row.label(text="Rename Selected Bones", icon="PRESET") # セクションタイトル

        if scene.brt_show_renumber_tools:
            row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row.prop(scene, "brt_rename_prefix", text="共通部分") # テキストボックス
            row.operator("brt.detect_common_prefix", text="", icon='BONE_DATA') # スポイトツール

            row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row.prop(scene, "brt_rename_start_number", text="連番開始番号")
            row.prop(scene, "brt_rename_rule", text="法則") # ドロップダウン
            row.prop(scene, "brt_rename_suffix", text="末尾") # ドロップダウン

            box1.operator("brt.rename_selected_bones", text="連番リネーム実行", icon="PRESET") # 実行ボタン


        # --- セクション 2: 指定名で置換 ------------------------------------------
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
            '''
            # 説明表示あり版
            # ▼ 親 row：3分割
            row = box2.row(align=True)

            # --- 左ブロック：説明 + 入力欄（置換元） ---
            col1 = row.column(align=True)
            col1.label(text=" Part to change:") #, icon='BLANK1')
            col1.prop(scene, "brt_rename_source_name", text="")

            # --- 中央ブロック：スポイト + FORWARD ---
            col_mid = row.column(align=True)
            # col_mid.operator("brt.extract_source_name", text="", icon="BONE_DATA")
            col_mid.label(icon='BLANK1') # スポイトツールをセクション名に移動させる場合
            col_mid.label(icon='FORWARD')

            # --- 右ブロック：説明 + 入力欄（置換先） ---
            col2 = row.column(align=True)
            col2.label(text=" Change to:") #, icon='BLANK1')
            col2.prop(scene, "brt_rename_target_name", text="")
            '''
            # テキストボックスのみ版
            row = box2.row(align=True)
            row.prop(scene, "brt_rename_source_name", text="") # テキストボックス
            row.label(icon='FORWARD')
            row.prop(scene, "brt_rename_target_name", text="") # テキストボックス

            row = box2.row()
            row.prop(scene, "brt_remove_number_suffix", text="")  # チェックボックス
            row.label(text="重複識別子を削除") # 非連動

            box2.operator("brt.replace_bone_name", text="指定名でボーン名変更", icon="GREASEPENCIL") # 実行ボタン


        # --- セクション 3: 反転リネーム ------------------------------------------
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
            right.operator("brt.brt_select_linear_chain", text="", icon="BONE_DATA")

        """
        # スポイトツールを使わないときのセクションタイトル部
        box3 = layout.box()
        row = box3.row(align=True) # ボタン同士を離したい場合は()
        row.prop(scene, "brt_show_invert_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_invert_tools else 'RIGHTARROW', emboss=False)
        row.label(text="Invert Selected Bones", icon='GROUP_BONE') # セクションタイトル
        """
   
        if scene.brt_show_invert_tools:
            if not hasattr(context.scene, "brt_invert_selected_bones"):
                return  # ← プロパティ未登録なら描画をスキップ

            props = context.scene.brt_invert_selected_bones

            # ボーン識別文字（ドロップダウン）
            row = box3.row()
            split = row.split(factor=0.20, align=True)  # ← ラベル側20%、残りにドロップダウンとボタン
            split.label(text="ボーン識別子:")
            right = split.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            right.prop(props, "bone_pattern", text="")  # ドロップダウン（ラベル非表示）
            right.operator("brt.open_preferences", text="", icon="PREFERENCES")  # 設定ボタン（プリファレンスを開く）

            """
            # 識別子セットの横に識別子ルールのドロップダウンを表示させる場合
            row = box3.row(align=True)
            split = row.split(factor=0.20, align=True)
            split.label(text="ボーン識別子:")

            right = split.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            right.prop(props, "bone_pattern", text="")  # セット選択
            right.prop(props, "bone_rule", text="")     # 選択肢として _r_ / _l_ などが並ぶ
            right.operator("brt.open_preferences", text="", icon="PREFERENCES") # 一番右端に設定ボタン（プリファレンスを開く）
            """

            row = box3.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row.prop(scene, "brt_assign_identifier", text="")  # チェックボックス
            row.label(text="左右識別子を付与する") # 非連動
            row.prop(props, "bone_rule", text="") # 判別ペアのドロップダウン（選択中のセットに応じた項目）

            row = box3.row()
            row.prop(scene, "brt_bone_x_mirror", text="")  # チェックボックス
            row.label(text="選択ボーンをグローバルXミラーする") # 非連動

            row = box3.row()
            row.prop(scene, "brt_duplicate_and_rename", text="")  # チェックボックス
            row.label(text="複製してリネームする") # 非連動

            box3.operator("brt.invert_selected_bones", text="選択ボーン反転リネーム", icon="GROUP_BONE") # 実行ボタン


        # --- セクション 4: その他リネームツール操作 ----------------------------------
        box4 = layout.box()
        row = box4.row(align=True)
        row.prop(scene, "brt_show_group_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_group_tools else 'RIGHTARROW', emboss=False)
        row.label(text="Other Rename Tools", icon="ARROW_LEFTRIGHT") # セクションタイトル

        if scene.brt_show_group_tools:
            row = box4.row()
            row.operator("brt.rename_groups", text="全対称化付与", icon="PLUS") # 実行ボタン
            row.operator("brt.revert_names", text="全対称化削除", icon="CANCEL") # 実行ボタン

    ''' ツールボックス１つのみ版
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box1 = layout.box() # 枠付きセクションを作成

        # 連番リネームタイトル
        row0 = box1.row()
        row0.label(text="Rename Selected Bones", icon="PRESET")

        # box1.label(text="ボーン連番リネーム")
        row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.prop(scene, "brt_rename_prefix", text="共通部分") # 共通部分入力
        row.operator("brt.detect_common_prefix", text="", icon='BONE_DATA') # スポイトツール

        row1 = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row1.prop(scene, "brt_rename_start_number", text="連番開始番号") # 連番開始番号
        row1.prop(scene, "brt_rename_rule", text="法則") # 連番法則選択
        row1.prop(scene, "brt_rename_suffix", text="末尾") # 末尾選択
        # box1.prop(scene, "brt_rename_start_number") # 連番開始番号
        # box1.prop(scene, "brt_rename_suffix") # 末尾選択
        # box1.prop(scene, "brt_rename_rule") # 連番法則選択

        box1.operator("brt.rename_selected_bones", text="連番リネーム実行", icon="PRESET")
        
        # 折りたたみ式ツールボックス
        row = box1.row(align=True)
        row.prop(scene, "brt_show_symmetric_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_symmetric_tools else 'RIGHTARROW', emboss=False)
        row.label(text="その他リネームツール")

        if scene.brt_show_symmetric_tools:

            # 指定名で置き換えタイトル
            row1 = box1.row()
            row1.label(text="Replace Bone Name", icon="GREASEPENCIL")

            row0 = box1.row()
            row0.label(text="　Before Name: ")
            row0.operator("brt.extract_source_name", text="", icon="BONE_DATA") # スポイトツール
            row0.label(text="　After Name: ")
 
            # 変更前後のボーン名入力フィールド（横並び）
            row = box1.row(align=True)

            col1 = row.column()
            col1.prop(scene, "brt_rename_source_name", text="")  # 左のテキストボックス

            col2 = row.column()
            col2.label(icon='FORWARD')  # または 'RIGHTARROW', 'PLAY'

            col3 = row.column()
            col3.prop(scene, "brt_rename_target_name", text="")  # 右のテキストボックス

            # オプション
            row = box1.row()
            row.prop(context.scene, "brt_remove_number_suffix", text="")  # ラベルと非連動
            row.label(text="重複識別子を削除", icon='NONE')
            # row.operator("brt.extract_source_name", text="", icon="BONE_DATA") # スポイトツール

            # 実行ボタンを下に配置
            box1.operator("brt.replace_bone_name", text="指定名でボーン名変更", icon="GREASEPENCIL")
            
            box1.separator()
            row2 = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row2.operator("brt.invert_selected_bones", text="選択ボーン反転リネーム")# 上から順に左側から設置
            row2.operator("brt.rename_groups", text="全対称化付与")
            row2.operator("brt.revert_names", text="全対称化削除")
    '''

class BRT_OT_RenameSelectedBones(bpy.types.Operator):
    """ボーン連番リネーム"""
    bl_idname = "brt.rename_selected_bones"
    bl_label = "Rename Selected Bones"

    def execute(self, context):
        from .rename_bones import rename_selected_bones
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
    bl_label = "共通部分を検出"
    bl_options = {'REGISTER', 'UNDO'}

    use_auto_select: bpy.props.BoolProperty(
        name="線形チェーンを選択",
        description="ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        default=True
    )

    filter_inconsistent: bpy.props.BoolProperty(
        name="一致しないボーンを除外",
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
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        )

        if prefix:
            context.scene.brt_rename_prefix = prefix
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

class BRT_OT_ExtractSourceName(bpy.types.Operator):
    """選択ボーンから置換元名を抽出"""
    bl_idname = "brt.extract_source_name"
    bl_label = "抽出:置換元"
    bl_options = {'REGISTER', 'UNDO'}

    use_auto_select: bpy.props.BoolProperty(
        name="線形チェーンを選択",
        description="ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        default=True
    )

    def execute(self, context):
        from .rename_detect import detect_common_prefix, select_linear_chain_inclusive

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "アーマチュアが選択されていません")
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
        else:
            self.report({'WARNING'}, "対応しているのは Pose または Edit モードです")
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, "ボーンが選択されていません")
            return {'CANCELLED'}

        # ネーミング規則に基づいて共通部分を抽出
        prefix = detect_common_prefix(
            bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        )

        if prefix:
            context.scene.brt_rename_source_name = prefix
            self.report({'INFO'}, f"抽出結果: {prefix}")
        else:
            self.report({'WARNING'}, "共通部分が検出できませんでした")

        # 自動選択が ON の場合はチェーンを選択
        if self.use_auto_select:
            select_linear_chain_inclusive(
                bones[0].name,
                prefix_filter=prefix
            )

        return {'FINISHED'} if prefix else {'CANCELLED'}

class BRT_OT_SelectLinearChain(bpy.types.Operator):
    """選択中ボーンから線形チェーン（分岐のない親子構造）を選択"""
    bl_idname = "brt.brt_select_linear_chain"
    bl_label = "線形チェーン選択"
    bl_options = {'REGISTER', 'UNDO'}

    filter_inconsistent: bpy.props.BoolProperty(
        name="一致しないボーンを除外",
        description="ネーミング規則が共通しないボーンを除外します",
        default=True
    )

    def execute(self, context):
        from . import rename_detect

        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "アーマチュアが選択されていません")
            return {'CANCELLED'}

        mode = context.mode
        if mode == 'POSE':
            bones = [b for b in obj.pose.bones if b.bone.select]
        elif mode == 'EDIT_ARMATURE':
            bones = [b for b in obj.data.edit_bones if b.select]
        else:
            self.report({'WARNING'}, "対応モードは Pose または Edit です")
            return {'CANCELLED'}

        if not bones:
            self.report({'WARNING'}, "起点となるボーンが選択されていません")
            return {'CANCELLED'}

        # 最初に選択されているボーンを起点に線形チェーンを選択
        prefix = rename_detect.detect_common_prefix(
            bones=bones,
            suffix_enum=context.scene.brt_rename_suffix,
            rule_enum=context.scene.brt_rename_rule
        ) if self.filter_inconsistent else None

        rename_detect.select_linear_chain_inclusive(
            bones[0].name,
            prefix_filter=prefix
        )

        self.report({'INFO'}, "線形チェーンを選択しました")
        return {'FINISHED'}

class BRT_OT_RenameGroups(bpy.types.Operator):
    """特定単語リネーム"""
    bl_idname = "brt.rename_groups"
    bl_label = "Rename Bones & Vertex Groups"

    def execute(self, context):
        from .rename_groups import rename_bones_and_vertex_groups
        rename_bones_and_vertex_groups()
        return {'FINISHED'}

class BRT_OT_RevertNames(bpy.types.Operator):
    """名前を元に戻す"""
    bl_idname = "brt.revert_names"
    bl_label = "Revert Renamed Names"

    def execute(self, context):
        from .rename_groups import revert_renamed_names
        revert_renamed_names()
        return {'FINISHED'}

class BRT_OT_InvertSelectedBones(bpy.types.Operator):
    """選択ボーンの左右反転リネーム"""
    bl_idname = "brt.invert_selected_bones"
    bl_label = "Invert Selected Bones"

    def execute(self, context):
        from .rename_symmetry import apply_mirrored_rename
        props = context.scene.brt_invert_selected_bones

        renamed = apply_mirrored_rename(
            context,
            pattern_name=props.bone_pattern,
            duplicate=context.scene.brt_duplicate_and_rename,
            mirror=context.scene.brt_bone_x_mirror,
            assign_identifier=context.scene.brt_assign_identifier,
            suffix_enum="wj",  # 任意の設定値
            rule_enum="000",   # 任意の設定値
            rule_index=int(props.bone_rule)
        )

        self.report({'INFO'}, f"{renamed}本のボーン名を変更しました")
        return {'FINISHED'}

class BRT_OT_ReplaceBoneName(bpy.types.Operator):
    """ボーン名の一部を一括置換"""
    bl_idname = "brt.replace_bone_name"
    bl_label = "Replace Bone Name"

    def execute(self, context):
        from .rename_rules import replace_bone_names_by_rule

        src = context.scene.brt_rename_source_name
        tgt = context.scene.brt_rename_target_name

        success, partial, message = replace_bone_names_by_rule(context, src, tgt)

        if not success:
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
        elif partial:
            self.report({'WARNING'}, message)
        else:
            self.report({'INFO'}, "ボーン名の置換を完了しました")
        return {'FINISHED'}
    

# ボーン識別子セットの取得
def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    items = []

    for i, pattern in enumerate(prefs.bone_patterns):
        label = pattern.label.strip()

        # 識別子としてそのまま使える名前に（ascii前提）
        identifier = label
        name = label  # 表示用にもそのまま使う（日本語でない前提）

        items.append((identifier, name, ""))

    return items

# 選択したボーン識別子セットの識別子ルールを取得
def get_rule_items(self, context):
    prefs = context.preferences.addons.get("DIVA_BoneRenameTools")
    if not prefs:
        return []

    label = self.bone_pattern  # 現在のセットラベル
    patterns = prefs.preferences.bone_patterns

    for pattern in patterns:
        if pattern.label == label:
            return [
                (str(i), f"{r.right} / {r.left}", "")
                for i, r in enumerate(pattern.rules)
                if r.right and r.left
            ]

    return []

# プロパティグループ
class BRT_InvertSelectedBonesProps(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="識別子セット",
        items=get_bone_pattern_items # JSONから読み込み
    )

    bone_rule: bpy.props.EnumProperty(
        name="識別子ペア",
        description="現在のセット内のルールを選択",
        items=lambda self, context: get_rule_items(self, context)
    )

#  DIVAアドオン設定画面（プリファレンス）を開く
class BRT_OT_OpenPreferences(bpy.types.Operator):
    bl_idname = "brt.open_preferences"
    bl_label = "DIVA 設定を開く"

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")  # Preferences ウィンドウを開く
        context.preferences.active_section = 'ADDONS'
        context.window_manager.addon_search = "diva"
        # アドオン指定でプリファレンスを開きたい場合はアドオンフォルダ名を設定
        # context.window_manager.addon_search = "DIVA_BoneRenameTools"
        return {'FINISHED'}
