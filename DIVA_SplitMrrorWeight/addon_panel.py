import bpy
from .addon_main import (
    get_selected_rules,
    detect_original_side,
    disable_mirror_modifier,
    duplicate_and_apply_mirror,
    has_vertices_on_positive_x,
    has_vertices_on_negative_x,
    delete_x_side_mesh,
    rename_symmetric_weight_groups
)
from .addon_preferences import get_json_path  # ← もし保存に関するユーティリティ関数などがあれば

# Nパネル設定
class SplitMirrorWeightPanel(bpy.types.Panel):
    bl_label = "Split Mirror Weight"
    bl_idname = "DIVA_PT_split_mirror_weight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIVA"

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MOD_MIRROR') # 左右反転風

    def draw(self, context):

        print("Nパネル draw 実行確認") # デバック用

        layout = self.layout
        props = context.scene.split_mirror_weight

        box = layout.box()  # 枠付きセクションを作成

        # ボーン識別文字（ドロップダウン）
        row1 = box.row()
        split1 = row1.split(factor=0.20, align=True)  # ← ラベル側20%、残りにドロップダウンとボタン
        split1.label(text="ボーン識別子:")
        right1 = split1.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        right1.prop(props, "bone_pattern", text="")  # ドロップダウン（ラベル非表示）
        right1.operator("diva.open_preferences", text="", icon="PREFERENCES")  # 設定ボタン（プリファレンスを開く）

        # オリジナル側
        row2 = box.row()
        split2 = row2.split(factor=0.20, align=True)  # ← ラベル側20%、残りにドロップダウン
        split2.label(text="オリジナル側:")
        right2 = split2.row(align=True)
        right2.prop(props, "delete_side", text="")  # ドロップダウン（ラベル非表示）
  
        # ミラー自動判別（チェックボタン）
        row3 = box.row()
        row3.prop(props, "mirror_auto_detect", text="")  # チェックボックス
        row3.label(text="ミラー自動判別")  # ラベル

        # ミラー実行ボタン
        box.separator()
        box.operator("object.split_mirror_weight", icon="MOD_MIRROR")

# アドオン処理
class OBJECT_OT_SplitMirrorWeight(bpy.types.Operator):
    bl_idname = "object.split_mirror_weight"
    bl_label = "ミラー実行"

    def execute(self, context):
        obj = bpy.context.object
        properties = bpy.context.scene.split_mirror_weight

        # 3Dビューで選択されているか確認する
        if not obj or obj not in context.selected_objects:
            self.report({'ERROR'}, "オブジェクトが選択されていません（シーンコレクション選択のみでは不可）")
            return {'CANCELLED'}

        # ミラー自動判別がONの場合、自動判定を実行
        if properties.mirror_auto_detect:
            detected_side = detect_original_side(obj)
            if detected_side:
                properties.delete_side = detected_side  # 判定した側をオリジナルとして設定
            else:
                self.report({'ERROR'}, "ミラー方向を自動判別できません。手動でオリジナル側を選択してください。")
                return {'CANCELLED'}

        delete_positive_x = (properties.delete_side == 'RIGHT')

        if obj and obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE':
            armature = obj.parent

            disable_mirror_modifier(obj)  
            mirrored_obj = duplicate_and_apply_mirror(obj, properties.delete_side)  # **リネーム処理を適用**

            # メッシュの有無をチェック（関数定義が必要）
            if delete_positive_x and not has_vertices_on_positive_x(mirrored_obj):
                self.report({'ERROR'}, "右側（+X）メッシュが存在しません。処理を中止しました。")
                return {'CANCELLED'}
            elif not delete_positive_x and not has_vertices_on_negative_x(mirrored_obj):
                self.report({'ERROR'}, "左側（-X）にメッシュが存在しません。処理を中止しました。")
                return {'CANCELLED'}

            delete_x_side_mesh(mirrored_obj, delete_positive_x)  

            # 識別子セットに対応
            selected_label = properties.bone_pattern
            selected_rules = get_selected_rules(selected_label)
            if not selected_rules:
                self.report({'ERROR'}, "識別ルールが見つかりません。")
                return {'CANCELLED'}

            rename_symmetric_weight_groups(mirrored_obj, selected_rules, properties.delete_side)

            self.report({'INFO'}, f"ミラー適用 & ウェイト転送完了: {mirrored_obj.name}")
        return {'FINISHED'}


# ボーン識別子セットの取得
def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
    items = []

    for i, pattern in enumerate(prefs.bone_patterns):
        label = pattern.label.strip()

        # 識別子としてそのまま使える名前に（ascii前提）
        identifier = label
        name = label  # 表示用にもそのまま使う（日本語でない前提）

        items.append((identifier, name, ""))

    return items

# プロパティグループ
class SplitMirrorWeightProperties(bpy.types.PropertyGroup):
    bone_pattern: bpy.props.EnumProperty(
        name="識別子セット",
        items=get_bone_pattern_items # JSONから読み込み
    )

    delete_side: bpy.props.EnumProperty(
        name="オリジナル側",
        description="コピー元を選択（右 or 左）",
        items=[
            ('RIGHT', "左→右に複製", "Blenderの+X側を削除"),
            ('LEFT', "右→左に複製", "Blenderの-X側を削除"),
        ],
        default='RIGHT'
    )

    mirror_auto_detect: bpy.props.BoolProperty(
        name="ミラー自動判別",
        description="ミラーの方向を自動判別するかどうか",
        default=False
    )

#  DIVAアドオン設定画面（プリファレンス）を開く
class DIVA_OT_OpenPreferences(bpy.types.Operator):
    bl_idname = "diva.open_preferences"
    bl_label = "DIVA 設定を開く"

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")  # Preferences ウィンドウを開く
        context.preferences.active_section = 'ADDONS'
        context.window_manager.addon_search = "diva"
        # アドオン指定でプリファレンスを開きたい場合はアドオンフォルダ名を設定
        # context.window_manager.addon_search = "DIVA_SplitMirrorWeight"
        return {'FINISHED'}

