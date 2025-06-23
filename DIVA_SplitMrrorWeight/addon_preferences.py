import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, UILayout
import os
import json


# デフォルト識別子の定義
DEFAULT_BONE_PATTERN = {
    "label": "DIVA(Default)",
    "rules": [
        {"right": "_r_", "left": "_l_"},
        {"right": "_r0", "left": "_l0"},
        {"right": "_r1", "left": "_l1"},
    ]
}


# JSONファイルの保存先（アドオンフォルダの中などに）
def get_json_path():
    return os.path.join(os.path.dirname(__file__), "bone_patterns.json")

# JSONファイルの読み込み
def load_bone_patterns_to_preferences(prefs):
    path = get_json_path()
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        prefs.bone_patterns.clear()
        unnamed_count = 1

        for entry in data:
            label = entry.get("label", "").strip()
            if not label:
                label = f"未定義セット{unnamed_count}"
                unnamed_count += 1

            pattern = prefs.bone_patterns.add()
            pattern.label = label

            for rule_data in entry.get("rules", []):
                rule = pattern.rules.add()
                rule.right = rule_data.get("right", "")
                rule.left = rule_data.get("left", "")
    except Exception as e:
        print(f"[DIVA] ⚠ JSON読み込みエラー: {e}")

# オプションひとつずつのデータ
# 識別子ルールのデータ（左右ペア）
class BoneRuleItem(bpy.types.PropertyGroup):
    right: bpy.props.StringProperty(name="右")
    left: bpy.props.StringProperty(name="左")

# 識別子セット（ラベルとルールリスト）
class BonePatternItem(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name="セット名")
    rules: bpy.props.CollectionProperty(type=BoneRuleItem)

# アドオンプリファレンス本体（表示と編集UI）
class DIVAAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "DIVA_SplitMirrorWeight"  # アドオンのフォルダ名（ハイフンや半角スペース、記号は使用不可）

    bone_patterns: bpy.props.CollectionProperty(type=BonePatternItem)
    bone_patterns_index: bpy.props.IntProperty(name="Index", default=0)

    def draw(self, context):
        layout = self.layout
        prefs = self  # アドオンプリファレンス本体（表示と編集UI）

        for i, pattern in enumerate(prefs.bone_patterns):
            row_outer = layout.row(align=True)

            # 左側：上下ボタン（枠の外）
            col_left = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.operator("diva.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.operator("diva.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i

            # 中央：セット全体の枠（box）
            box = row_outer.box()

            # セット名
            row = box.row(align=True)
            row.prop(pattern, "label", text="セット名")
            row.separator(factor=4.5) # ペア欄と右端を揃える

            # 識別ペアの表示
            for j, rule in enumerate(pattern.rules):
                row = box.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
                row.prop(rule, "right", text="右")
                row.prop(rule, "left", text="左")

                del_op = row.operator("diva.delete_bone_rule", text="", icon="X")  # ペア削除ボタン
                del_op.pattern_index = i
                del_op.rule_index = j

            # 識別子ペア追加ボタンをセット内に設置
            box.operator("diva.add_bone_rule", text="ペアを追加", icon="ADD").index = i

            # 右側：セット削除ボタン（枠の外）
            col_right = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
            col_right.separator()  # セパレータで上にスペースを追加
            col_right.operator("diva.delete_bone_pattern", text="", icon="X").index = i  # セット削除ボタン

        layout.separator()

        layout.operator("diva.add_bone_pattern", icon="COLLECTION_NEW") # 識別端子セットの追加

        row1 = layout.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        row1.operator("diva.append_default_bone_set", text="デフォルトセットを復元", icon="COPY_ID")
        row1.operator("diva.reset_bone_patterns", text="リセット", icon="FILE_REFRESH")
        row1.operator("diva.save_bone_patterns", text="保存", icon="DISC")

# プリファレンスの編集UI
class DIVA_OT_AddBonePattern(bpy.types.Operator):
    bl_idname = "diva.add_bone_pattern"
    bl_label = "識別子セットを追加"

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        new_pattern = prefs.bone_patterns.add()
        new_pattern.label = "New Set"
        rule = new_pattern.rules.add()
        rule.right = "R"
        rule.left = "L"
        return {'FINISHED'}

class DIVA_OT_AddBoneRule(bpy.types.Operator):
    bl_idname = "diva.add_bone_rule"
    bl_label = "識別子ルールを追加"

    index: bpy.props.IntProperty()  # 追加対象の bone_patterns インデックス

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        if self.index < len(prefs.bone_patterns):
            pattern = prefs.bone_patterns[self.index]
            rule = pattern.rules.add()
            rule.right = ""
            rule.left = ""
        return {'FINISHED'}

# 識別子セットの移動ボタン
class DIVA_OT_MoveBonePatternUp(bpy.types.Operator):
    bl_idname = "diva.move_bone_pattern_up"
    bl_label = "↑ 上に移動"

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        i = self.index  # 修正点: self.index を使う
        if i > 0:
            prefs.bone_patterns.move(i, i - 1)
            prefs.bone_patterns_index = i - 1
        return {'FINISHED'}

class DIVA_OT_MoveBonePatternDown(bpy.types.Operator):
    bl_idname = "diva.move_bone_pattern_down"
    bl_label = "↓ 下に移動"

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        i = self.index  # 修正点: self.index を使う
        if i < len(prefs.bone_patterns) - 1:
            prefs.bone_patterns.move(i, i + 1)
            prefs.bone_patterns_index = i + 1
        return {'FINISHED'}

class DIVA_OT_SaveBonePatterns(bpy.types.Operator):
    bl_idname = "diva.save_bone_patterns"
    bl_label = "識別子セットを保存"

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences

        # バリデーションチェック（ラベル未設定・不完全ペアを検出）
        for p in prefs.bone_patterns:
            label = p.label.strip()

            # 日本語や全角文字の検出
            if any(ord(c) > 127 for c in label):
                self.report({'WARNING'}, f"「{label}」には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください。")
                return {'CANCELLED'}

            if not label:
                self.report({'WARNING'}, "識別子セットの名前を入力してください")
                return {'CANCELLED'}

            complete_pairs = [r for r in p.rules if r.right.strip() and r.left.strip()]
            incomplete_pairs = [r for r in p.rules if (r.right.strip() and not r.left.strip()) or (not r.right.strip() and r.left.strip())]

            if not complete_pairs:
                self.report({'WARNING'}, f"「{p.label}」には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）")
                return {'CANCELLED'}

            if incomplete_pairs:
                self.report({'WARNING'}, f"「{p.label}」に片側だけ空白の識別子ペアがあります（両方入力してください）")
                return {'CANCELLED'}
            
        # 保存後に再読込（Nパネルに反映させるため）
        data = []
        for pattern in prefs.bone_patterns:
            rules = [{"right": r.right, "left": r.left} for r in pattern.rules]
            data.append({"label": pattern.label, "rules": rules})
        with open(get_json_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.report({'INFO'}, "保存しました！")

        load_bone_patterns_to_preferences(prefs)

        return {'FINISHED'}
    
class DIVA_OT_ResetBonePatterns(bpy.types.Operator):
    bl_idname = "diva.reset_bone_patterns"
    bl_label = "編集をリセット"
    bl_description = "JSONファイルを読み直して識別子セットを元に戻します"

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        load_bone_patterns_to_preferences(prefs)
        self.report({'INFO'}, "識別子セットを元に戻しました")
        return {'FINISHED'}

class DIVA_OT_AppendDefaultSet(bpy.types.Operator):
    bl_idname = "diva.append_default_bone_set"
    bl_label = "デフォルトセットを復元"
    bl_description = "コード定義のデフォルトセットを先頭に追加します"

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        prefs.bone_patterns.add()
        for i in reversed(range(len(prefs.bone_patterns) - 1)):
            prefs.bone_patterns.move(i, i + 1)

        pattern = prefs.bone_patterns[0]
        pattern.label = DEFAULT_BONE_PATTERN["label"]
        pattern.rules.clear()
        for r in DEFAULT_BONE_PATTERN["rules"]:
            rule = pattern.rules.add()
            rule.right = r["right"]
            rule.left = r["left"]

        self.report({'INFO'}, "デフォルトセットを追加しました")
        return {'FINISHED'}
    

class DIVA_OT_DeleteBonePattern(bpy.types.Operator):
    bl_idname = "diva.delete_bone_pattern"
    bl_label = "セットを削除"
    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        if len(prefs.bone_patterns) <= 1:
            self.report({'WARNING'}, "最低でも1つの識別子セットを設定してください")
            return {'CANCELLED'}
        prefs.bone_patterns.remove(self.index)
        return {'FINISHED'}


class DIVA_OT_DeleteBoneRule(bpy.types.Operator):
    bl_idname = "diva.delete_bone_rule"
    bl_label = "ペアを削除"
    pattern_index: bpy.props.IntProperty()
    rule_index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_SplitMirrorWeight"].preferences
        rules = prefs.bone_patterns[self.pattern_index].rules
        if len(rules) <= 1:
            self.report({'WARNING'}, "最低でも1つの識別子ペアを設定してください")
            return {'CANCELLED'}
        rules.remove(self.rule_index)
        return {'FINISHED'}




