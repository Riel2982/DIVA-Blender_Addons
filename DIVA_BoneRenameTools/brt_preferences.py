import bpy
from bpy.app.translations import pgettext as _
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, UILayout
from .brt_types import BRT_BonePatternItem, BRT_BoneRuleItem
from .brt_types import get_bone_pattern_items, get_rule_items
from .brt_update import draw_update_ui
import os
import json


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
        for p in DEFAULT_BONE_PATTERN:
            pattern = prefs.bone_patterns.add()
            pattern.label = p["label"]
            for r in p["rules"]:
                rule = pattern.rules.add()
                rule.right = r["right"]
                rule.left = r["left"]
                rule.use_regex = r.get("use_regex", False)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN, f, ensure_ascii=False, indent=2)
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
            json.dump(DEFAULT_BONE_PATTERN, f, ensure_ascii=False, indent=2)
        apply_default()

'''
def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    return [(p.label, p.label, "") for p in prefs.bone_patterns]

def get_rule_items(self, context):
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    for p in prefs.bone_patterns:
        if p.label == self.bone_pattern:
            return [(r.left + "↔" + r.right, r.left + "↔" + r.right, "") for r in p.rules]
    return []
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

        # 更新用UI
        draw_update_ui(layout, scene)

        # 左右識別子設定UI
        main_box = layout.box() 
        main_box.label(text=_("識別セットの編集"), icon='ASSET_MANAGER')  # 必要に応じて icon を調整

        for i, pattern in enumerate(prefs.bone_patterns):
            row_outer = main_box.row(align=True)

            # 左側：上下ボタン（枠の外）
            col_left = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.operator("brt.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.operator("brt.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i

            # 中央：セット全体の枠（box）
            box = row_outer.box()

            # セット名
            row = box.row(align=True)
            row.prop(pattern, "label", text=_("セット名"))
            row.separator(factor=4.5) # ペア欄と右端を揃える

            # 識別ペアの表示
            for j, rule in enumerate(pattern.rules):
                row = box.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
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

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        new_pattern = prefs.bone_patterns.add()
        new_pattern.label = "New Set"
        rule = new_pattern.rules.add()
        rule.right = "R"
        rule.left = "L"
        rule.use_regex = False  # 正規表現置き換え不使用
        return {'FINISHED'}

class BRT_OT_AddBoneRule(bpy.types.Operator):
    """識別子ルールを追加"""
    bl_idname = "brt.add_bone_rule"
    bl_label = _("Add Identifier Rule")
    bl_description = _("Add a left-right identifier rule to the selected set")

    index: bpy.props.IntProperty()  # 追加対象の bone_patterns インデックス

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        if self.index < len(prefs.bone_patterns):
            pattern = prefs.bone_patterns[self.index]
            rule = pattern.rules.add()
            rule.right = ""
            rule.left = ""
            rule.use_regex = False
        return {'FINISHED'}

# 識別子セットの移動ボタン
class BRT_OT_MoveBonePatternUp(bpy.types.Operator):
    """↑ 上に移動"""
    bl_idname = "brt.move_bone_pattern_up"
    bl_label = _("Move Indentifier Set Up")
    bl_description = _("Move the identifier set up one position")

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        i = self.index  # 修正点: self.index を使う
        if i > 0:
            prefs.bone_patterns.move(i, i - 1)
            prefs.bone_patterns_index = i - 1
        return {'FINISHED'}

class BRT_OT_MoveBonePatternDown(bpy.types.Operator):
    """↓ 下に移動"""
    bl_idname = "brt.move_bone_pattern_down"
    bl_label = _("Move Indentifier Set Down")
    bl_description = _("Move the identifier set down one position")

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        i = self.index  # self.index を使う
        if i < len(prefs.bone_patterns) - 1:
            prefs.bone_patterns.move(i, i + 1)
            prefs.bone_patterns_index = i + 1
        return {'FINISHED'}

class BRT_OT_SaveBonePatterns(bpy.types.Operator):
    """識別子セットを保存"""
    bl_idname = "brt.save_bone_patterns"
    bl_label = _("Save Identifier Sets")
    bl_description = _("Save all identifier sets to a JSON file")

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences

        # バリデーションチェック（ラベル未設定・不完全ペアを検出）
        for p in prefs.bone_patterns:
            label = p.label.strip()

            # 日本語や全角文字の検出
            if any(ord(c) > 127 for c in label):
                self.report({'WARNING'}, _("{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください").format(label=pattern.label))
                return {'CANCELLED'}

            if not label:
                self.report({'WARNING'}, _("識別子セットの名前を入力してください"))
                return {'CANCELLED'}

            complete_pairs = [r for r in p.rules if r.right.strip() and r.left.strip()]
            incomplete_pairs = [r for r in p.rules if (r.right.strip() and not r.left.strip()) or (not r.right.strip() and r.left.strip())]

            if not complete_pairs:
                self.report({'WARNING'}, _("{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）").format(label=pattern.label))
                return {'CANCELLED'}

            if incomplete_pairs:
                self.report({'WARNING'}, _("{label}に片側だけ空白の識別子ペアがあります（両方入力してください）").format(label=pattern.label))
                return {'CANCELLED'}
            
        # 保存後に再読込（Nパネルに反映させるため）
        data = []
        for pattern in prefs.bone_patterns:
            rules = [{
                "right": r.right,
                "left": r.left,
                "use_regex": r.use_regex  # ← 正規表現フラグも保存
            } for r in pattern.rules]
            data.append({"label": pattern.label, "rules": rules})
        with open(get_json_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.report({'INFO'}, _("保存しました！"))

        load_bone_patterns_to_preferences(prefs)

        return {'FINISHED'}
    
class BRT_OT_ResetBonePatterns(bpy.types.Operator):
    """JSONファイルを読み直して識別子セットを元に戻します"""
    bl_idname = "brt.reset_bone_patterns"
    bl_label = _("Reload Identifier Sets")
    bl_description = _("Reload the identifier sets from the saved JSON file")

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        load_bone_patterns_to_preferences(prefs)
        self.report({'INFO'}, _("識別子セットを元に戻しました"))
        return {'FINISHED'}

class BRT_OT_AppendDefaultSet(bpy.types.Operator):
    """コード定義のデフォルトセットを先頭に追加します"""
    bl_idname = "brt.append_default_bone_set"
    bl_label = _("Append Default Set")
    bl_description = _("Insert the default set of identifiers at the top")

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        pattern = prefs.bone_patterns.add()     # セットを追加

        pattern_data = DEFAULT_BONE_PATTERN[0]  #デフォルトセットの先頭の辞書を取得
        pattern.label = pattern_data["label"]
        pattern.rules.clear()
        for r in pattern_data["rules"]: 
            rule = pattern.rules.add()
            rule.right = r["right"]
            rule.left = r["left"]
            rule.use_regex = r.get("use_regex", False) # 正規表現置き換えは不使用

        index = len(prefs.bone_patterns) - 1
        prefs.bone_patterns.move(index, 0)   # セットを先頭へ移動

        self.report({'INFO'}, _("デフォルトセットを追加しました"))
        return {'FINISHED'}
    

class BRT_OT_DeleteBonePattern(bpy.types.Operator):
    """識別子セットの削除"""
    bl_idname = "brt.delete_bone_pattern"
    bl_label = _("Delete Identifier Set")
    bl_description = _("Delete the selected identifier set")

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

    pattern_index: bpy.props.IntProperty()
    rule_index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
        rules = prefs.bone_patterns[self.pattern_index].rules
        if len(rules) <= 1:
            self.report({'WARNING'}, _("最低でも1つの識別子ペアを設定してください"))
            return {'CANCELLED'}
        rules.remove(self.rule_index)
        return {'FINISHED'}



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
