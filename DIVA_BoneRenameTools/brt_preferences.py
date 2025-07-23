import bpy
import os
import json
from bpy.app.translations import pgettext as _
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, UILayout
from .brt_types import BRT_BonePatternItem, BRT_BoneRuleItem
from .brt_types import get_bone_pattern_items, get_rule_items
from .brt_json import load_bone_patterns_to_preferences, get_json_path, DEFAULT_BONE_PATTERN
from .brt_json import load_json_data, save_json_data
from .brt_update import draw_update_ui

'''
# デフォルト識別子の定義
DEFAULT_BONE_PATTERN = [
    {
        "label": "DIVA(Default)",
        "rules": [
            {"right": "_r_", "left": "_l_", "use_regex": False},
            {"right": "_r0", "left": "_l0", "use_regex": False},
            {"right": "_r1", "left": "_l1", "use_regex": False},
        ],
    }
]


# JSONファイルの保存先（アドオンフォルダの中などに）
def get_json_path():
    path = os.path.join(os.path.dirname(__file__), "bone_patterns.json")
    print("[DIVA] JSON path:", path)
    return path

# JSONファイルの読み込み
def load_bone_patterns_to_preferences(prefs):
    path = get_json_path()

    def apply_default():
        prefs.bone_patterns.clear()
        for p in DEFAULT_BONE_PATTERN():
            pattern = prefs.bone_patterns.add()
            pattern.label = p["label"]
            for r in p["rules"]:
                rule = pattern.rules.add()
                rule.right = r["right"]
                rule.left = r["left"]
                rule.use_regex = r.get("use_regex", False)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN(), f, ensure_ascii=False, indent=2)
        apply_default()
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSONルートが配列形式ではありません")

        prefs.bone_patterns.clear()
        unnamed_count = 1
        for entry in data:
            label = entry.get("label", "").strip() or f"未定義セット{unnamed_count}"
            if not entry.get("label"):
                unnamed_count += 1
            pattern = prefs.bone_patterns.add()
            pattern.label = label
            for rule_data in entry.get("rules", []):
                rule = pattern.rules.add()
                rule.right = rule_data.get("right", "")
                rule.left = rule_data.get("left", "")
                rule.use_regex = rule_data.get("use_regex", False)
    except Exception as e:
        print(f"[DIVA] ⚠ JSON読み込みエラー: {e}")

        # タイムスタンプ付きでバックアップ
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.replace(".json", f".invalid_{timestamp}.json")
        try:
            shutil.move(path, backup_path)
            print(f"[DIVA] ⚠ 破損JSONをバックアップ: {backup_path}")
        except Exception as move_err:
            print(f"[DIVA] ⚠ バックアップに失敗しました: {move_err}")

        # デフォルトで再生成
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN(), f, ensure_ascii=False, indent=2)
        apply_default()
'''


# アドオンプリファレンス本体（表示と編集UI）
class BRT_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "DIVA_BoneRenameTools"  # アドオンのフォルダ名（ハイフンや半角スペース、記号は使用不可）

    bone_patterns: bpy.props.CollectionProperty(type=BRT_BonePatternItem)
    bone_patterns_index: bpy.props.IntProperty(name="Index", default=0)

    def draw(self, context):
        layout = self.layout
        prefs = self  # アドオンプリファレンス本体（表示と編集UI）
        scene = context.scene
        wm = context.window_manager

        # 更新用UI
        draw_update_ui(layout, scene)

        # 明示的な変数名で状態を保持（折りたたみが複数増えても対応しやすくなる）
        show_identifier_sets = wm.brt_show_identifier_sets

        # トグル付きヘッダー行
        main_box = layout.box()
        row = main_box.row(align=True)

        row.prop(wm, "brt_show_identifier_sets", text="", icon='DOWNARROW_HLT' if show_identifier_sets else 'RIGHTARROW', emboss=False)
        row.label(text=_("識別子セットの編集"), icon='ASSET_MANAGER')

        # 🔻折りたたみ状態なら描画（識別子セット編集のUIの中身）
        if show_identifier_sets:
            for i, pattern in enumerate(prefs.bone_patterns):
                row_outer = main_box.row(align=True)

                # 左側：上下ボタン（枠の外）
                col_left = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
                col_left.separator()  # セパレータで上にスペースを追加
                col_left.separator()  # セパレータで上にスペースを追加
                # col_left.operator("brt.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
                if i > 0:
                    col_left.operator("brt.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
                else:
                    col_left.label(text="", icon="BLANK1")
                col_left.separator()  # セパレータで上にスペースを追加
                col_left.separator()  # セパレータで上にスペースを追加
                # col_left.operator("brt.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i
                if i < len(prefs.bone_patterns) - 1:
                    col_left.operator("brt.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i
                else:
                    col_left.label(text="", icon="BLANK1")


                # 中央：セット全体の枠（box）
                box = row_outer.box()

                # セット名
                row = box.row(align=True)
                row.prop(pattern, "label", text=_("セット名"))
                row.separator(factor=4.5) # ペア欄と右端を揃える

                # 識別ペアの表示
                for j, rule in enumerate(pattern.rules):
                    row = box.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
                    # row.prop(rule, "use_regex", text="")    # 正規表現の切り替え
                    row.prop(rule, "right", text=_("右"))
                    row.prop(rule, "left", text=_("左"))

                    del_op = row.operator("brt.delete_bone_rule", text="", icon="X")  # ペア削除ボタン
                    del_op.pattern_index = i
                    del_op.rule_index = j

                # 識別子ペア追加ボタンをセット内に設置
                box.operator("brt.add_bone_rule", text=_("ペアを追加"), icon="ADD").index = i

                # 右側：セット削除ボタン（枠の外）
                col_right = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
                col_right.separator()  # セパレータで上にスペースを追加
                col_right.operator("brt.delete_bone_pattern", text="", icon="X").index = i  # セット削除ボタン

            main_box.separator()

            main_box.operator("brt.add_bone_pattern", text=_("Add Identifier Set"), icon="COLLECTION_NEW") # 識別端子セットの追加

            row1 = main_box.row()    # ぴったりボタン同士をくっつけたい場合は(align=True)
            row1.operator("brt.append_default_bone_set", text=_("デフォルトセットを復元"), icon="COPY_ID")
            row1.operator("brt.reset_bone_patterns", text=_("リセット"), icon="DECORATE_OVERRIDE")
            row1.operator("brt.save_bone_patterns", text=_("保存"), icon="FILE_TICK")

# プリファレンスの編集UI
class BRT_OT_AddBonePattern(bpy.types.Operator):
    """識別子セットを追加"""
    bl_idname = "brt.add_bone_pattern"
    bl_label = _("Add Identifier Set")
    bl_description = _("Add a new identifier set to the preferences")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences

        pattern = prefs.bone_patterns.add()
        pattern.label = "New Set"
        rule = pattern.rules.add()
        rule.right = "R"
        rule.left = "L"
        rule.use_regex = False

        self.report({'INFO'}, _("新しい識別子セットを追加しました"))
        return {'FINISHED'}


class BRT_OT_AddBoneRule(bpy.types.Operator):
    """識別子ルールを追加"""
    bl_idname = "brt.add_bone_rule"
    bl_label = _("Add Identifier Rule")
    bl_description = _("Add a left-right identifier rule to the selected set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()  # 追加対象の bone_patterns インデックス

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences

        rule = prefs.bone_patterns[self.index].rules.add()
        rule.right = ""
        rule.left = ""
        rule.use_regex = False

        self.report({'INFO'}, _("識別子ペアを追加しました"))
        return {'FINISHED'}


# 識別子セットの移動ボタン
class BRT_OT_MoveBonePatternUp(bpy.types.Operator):
    """↑ 上に移動"""
    bl_idname = "brt.move_bone_pattern_up"
    bl_label = _("Move Indentifier Set Up")
    bl_description = _("Move the identifier set up one position")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        i = self.index

        if i <= 0:
            self.report({'WARNING'}, _("既に先頭にあります"))
            return {'CANCELLED'}

        prefs.bone_patterns.move(i, i - 1)
        self.report({'INFO'}, _("上に移動しました"))
        return {'FINISHED'}


class BRT_OT_MoveBonePatternDown(bpy.types.Operator):
    """↓ 下に移動"""
    bl_idname = "brt.move_bone_pattern_down"
    bl_label = _("Move Indentifier Set Down")
    bl_description = _("Move the identifier set down one position")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        i = self.index

        if i < len(prefs.bone_patterns) - 1:
            prefs.bone_patterns.move(i, i + 1)
            self.report({'INFO'}, _("下に移動しました"))
        else:
            self.report({'WARNING'}, _("既に末尾にあります"))
        return {'FINISHED'}



class BRT_OT_SaveBonePatterns(bpy.types.Operator):
    """識別子セットを保存"""
    bl_idname = "brt.save_bone_patterns"
    bl_label = _("Save Identifier Sets")
    bl_description = _("Save all identifier sets to a JSON file")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        data = []

        for p in prefs.bone_patterns:
            label = p.label.strip()
            if not label:
                self.report({'WARNING'}, _("識別子セットの名前を入力してください"))
                return {'CANCELLED'}
            if any(ord(c) > 127 for c in label):
                self.report({'WARNING'}, _("{label}には使用できない文字が含まれています。セット名には半角英数字のみを使用してください").format(label=label))
                return {'CANCELLED'}

            complete = [r for r in p.rules if r.right.strip() and r.left.strip()]
            incomplete = [r for r in p.rules if (r.right.strip() and not r.left.strip()) or (not r.right.strip() and r.left.strip())]

            if not complete:
                self.report({'WARNING'}, _("{label}には両側が入力された識別子ペアが必要です").format(label=label))
                return {'CANCELLED'}
            if incomplete:
                self.report({'WARNING'}, _("{label}に片側だけの識別子ペアがあります").format(label=label))
                return {'CANCELLED'}

            rules = [{
                "right": r.right,
                "left": r.left,
                "use_regex": r.use_regex
            } for r in p.rules]
            data.append({"label": label, "rules": rules})

        save_json_data(data)
        self.report({'INFO'}, _("保存しました！"))
        load_bone_patterns_to_preferences(prefs)
        return {'FINISHED'}
    
class BRT_OT_ResetBonePatterns(bpy.types.Operator):
    """JSONファイルを読み直して識別子セットを元に戻します"""
    bl_idname = "brt.reset_bone_patterns"
    bl_label = _("Reload Identifier Sets")
    bl_description = _("Reload the identifier sets from the saved JSON file")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        load_bone_patterns_to_preferences(context.preferences.addons["DIVA_BoneRenameTools"].preferences)
        self.report({'INFO'}, _("識別子セットを再読込しました"))
        return {'FINISHED'}


class BRT_OT_AppendDefaultSet(bpy.types.Operator):
    """コード定義のデフォルトセットを先頭に追加します"""
    bl_idname = "brt.append_default_bone_set"
    bl_label = _("Append Default Set")
    bl_description = _("Insert the default set of identifiers at the top")
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        pattern_data = DEFAULT_BONE_PATTERN()[0]

        pattern = prefs.bone_patterns.add()
        pattern.label = pattern_data["label"]
        for r in pattern_data["rules"]:
            rule = pattern.rules.add()
            rule.right = r["right"]
            rule.left = r["left"]
            rule.use_regex = r.get("use_regex", False)

        # 先頭に移動
        index = len(prefs.bone_patterns) - 1
        prefs.bone_patterns.move(index, 0)

        self.report({'INFO'}, _("デフォルトセットを追加しました"))
        return {'FINISHED'}
    

class BRT_OT_DeleteBonePattern(bpy.types.Operator):
    """識別子セットの削除"""
    bl_idname = "brt.delete_bone_pattern"
    bl_label = _("Delete Identifier Set")
    bl_description = _("Delete the selected identifier set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        if len(prefs.bone_patterns) <= 1:
            self.report({'WARNING'}, _("最低でも1つの識別子セットを設定してください"))
            return {'CANCELLED'}
        prefs.bone_patterns.remove(self.index)
        return {'FINISHED'}


class BRT_OT_DeleteBoneRule(bpy.types.Operator):
    """識別子ペアの削除"""
    bl_idname = "brt.delete_bone_rule"
    bl_label = _("Delete Identifier Pair")
    bl_description = _("Remove the selected identifier pair from the set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    pattern_index: bpy.props.IntProperty()
    rule_index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences

        try:
            pattern = prefs.bone_patterns[self.pattern_index]
            if len(pattern.rules) <= 1:
                self.report({'WARNING'}, "最低1ペアは必要です")
                return {'CANCELLED'}

            pattern.rules.remove(self.rule_index)
            self.report({'INFO'}, _("識別子ペアを削除しました"))
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, _("削除に失敗しました: {msg}").format(msg=str(e)))
            return {'CANCELLED'}




def get_classes():
    return [
        BRT_OT_AddBonePattern,
        BRT_OT_AddBoneRule,
        BRT_OT_DeleteBonePattern,
        BRT_OT_DeleteBoneRule,
        BRT_OT_MoveBonePatternUp,
        BRT_OT_MoveBonePatternDown,
        BRT_OT_ResetBonePatterns,
        BRT_OT_SaveBonePatterns,
        BRT_OT_AppendDefaultSet,
        # BRT_BoneRuleItem,
        # BRT_BonePatternItem,
        BRT_AddonPreferences,
    ]
