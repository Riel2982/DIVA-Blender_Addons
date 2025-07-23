import bpy
from bpy.app.translations import pgettext as _
from .brt_ui_rename import panel_rename_ui
from .brt_ui_replace import panel_replace_ui
from .brt_ui_invert import panel_invert_ui
from .brt_ui_other import panel_other_ui

class DIVA_PT_BoneRenamePanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Rename Tools"
    bl_idname = "DIVA_PT_bone_rename"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='GROUP_BONE') # ボーンミラー風

    # UIをセクションごとに分離
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        panel_rename_ui(layout, scene)
        panel_replace_ui(layout, scene)
        panel_invert_ui(layout, context, scene)
        panel_other_ui(layout, scene)

if False:
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
            row.prop(scene, "brt_rename_prefix", text=_("共通部分")) # テキストボックス
            row.operator("brt.detect_common_prefix", text="", icon='BONE_DATA') # スポイトツール

            row = box1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
            row.prop(scene, "brt_rename_start_number", text=_("連番開始番号"))
            row.prop(scene, "brt_rename_rule", text=_("法則")) # ドロップダウン
            row.prop(scene, "brt_rename_suffix", text=_("末尾")) # ドロップダウン

            box1.operator("brt.rename_selected_bones", text=_("連番リネーム実行"), icon="PRESET") # 実行ボタン


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
            row.label(text=_("重複識別子を削除")) # 非連動

            box2.operator("brt.replace_bone_name", text=_("指定名でボーン名変更"), icon="GREASEPENCIL") # 実行ボタン


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
            right.operator("brt.select_linear_chain", text="", icon="BONE_DATA")

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
            split.label(text=_("ボーン識別子:"))
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
            row.label(text=_("左右識別子を付与する")) # 非連動
            row.prop(props, "bone_rule", text="") # 判別ペアのドロップダウン（選択中のセットに応じた項目）

            row = box3.row()
            row.prop(scene, "brt_bone_x_mirror", text="")  # チェックボックス
            row.label(text=_("選択ボーンをグローバルXミラーする")) # 非連動

            row = box3.row()
            row.prop(scene, "brt_duplicate_and_rename", text="")  # チェックボックス
            row.label(text=_("複製してリネームする")) # 非連動

            box3.operator("brt.invert_selected_bones", text=_("選択ボーン反転リネーム"), icon="GROUP_BONE") # 実行ボタン


        # --- セクション 4: その他リネームツール操作 ----------------------------------
        box4 = layout.box()
        row = box4.row(align=True)
        row.prop(scene, "brt_show_group_tools", text="", icon='DOWNARROW_HLT' if scene.brt_show_group_tools else 'RIGHTARROW', emboss=False)
        row.label(text="Other Rename Tools", icon="ARROW_LEFTRIGHT") # セクションタイトル

        if scene.brt_show_group_tools:
            row = box4.row()
            row.operator("brt.rename_groups", text=_("全対称化付与"), icon="PLUS") # 実行ボタン
            row.operator("brt.revert_names", text=_("全対称化削除"), icon="CANCEL") # 実行ボタン

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

    
'''
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
'''



def get_classes():
    return [
        DIVA_PT_BoneRenamePanel,
    ]