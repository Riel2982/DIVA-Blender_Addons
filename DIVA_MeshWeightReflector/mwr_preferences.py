import bpy
import os
import json
from bpy.app.translations import pgettext as _
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, UILayout
from .mwr_types import MWR_BonePatternItem, MWR_BoneRuleItem
from .mwr_types import get_bone_pattern_items, get_rule_items
from .mwr_json import load_bone_patterns_to_preferences, get_json_path, DEFAULT_BONE_PATTERN
from .mwr_json import load_json_data, save_json_data, sync_bone_patterns
from .mwr_uix_update import draw_update_ui


# アドオンプリファレンス本体（表示と編集UI）
class MWR_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "DIVA_MeshWeightReflector"  # アドオンのフォルダ名（ハイフンや半角スペース、記号は使用不可）

    initialized: bpy.props.BoolProperty(name="initialized", default=False, options={'HIDDEN'})      # DLフォルダ更新用 

    bone_patterns: bpy.props.CollectionProperty(type=MWR_BonePatternItem)
    bone_patterns_index: bpy.props.IntProperty(name="Index", default=0)

    def draw(self, context):
        layout = self.layout
        prefs = self  # アドオンプリファレンス本体（表示と編集UI）
        scene = context.scene
        wm = context.window_manager

        # 更新用UI
        draw_update_ui(layout, scene)

        # 識別子セット編集用UI
        draw_identifier_ui(layout, wm, prefs)

# 識別子セット編集用UI
def draw_identifier_ui(layout, wm, prefs):
    # 明示的な変数名で状態を保持（折りたたみが複数増えても対応しやすくなる）
    show_identifier_sets = wm.mwr_show_identifier_sets

    # トグル付きヘッダー行
    main_box = layout.box()
    row = main_box.row(align=True)

    row.prop(wm, "mwr_show_identifier_sets", text="", icon='DOWNARROW_HLT' if show_identifier_sets else 'RIGHTARROW', emboss=False)
    row.label(text=_("Editing Identifier Sets"), icon='ASSET_MANAGER')

    # 🔻折りたたみ状態なら描画（識別子セット編集のUIの中身）
    if show_identifier_sets:
        for i, pattern in enumerate(prefs.bone_patterns):
            row_outer = main_box.row(align=True)

            # 左側：上下ボタン（枠の外）
            col_left = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            # col_left.operator("mwr.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
            if i > 0:
                col_left.operator("mwr.move_bone_pattern_up", text="", icon="TRIA_UP").index = i
            else:
                col_left.label(text="", icon="BLANK1")
            col_left.separator()  # セパレータで上にスペースを追加
            col_left.separator()  # セパレータで上にスペースを追加
            # col_left.operator("mwr.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i
            if i < len(prefs.bone_patterns) - 1:
                col_left.operator("mwr.move_bone_pattern_down", text="", icon="TRIA_DOWN").index = i
            else:
                col_left.label(text="", icon="BLANK1")


            # 中央：セット全体の枠（box）
            box = row_outer.box()

            # セット名
            row = box.row(align=True)
            row.prop(pattern, "label", text=_("Set name"))
            row.separator(factor=4.5) # ペア欄と右端を揃える

            # 識別ペアの表示
            for j, rule in enumerate(pattern.rules):
                row = box.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
                # row.prop(rule, "use_regex", text="")    # 正規表現の切り替え
                row.prop(rule, "right", text=_("Right"))
                row.prop(rule, "left", text=_("Left"))

                del_op = row.operator("mwr.delete_bone_rule", text="", icon="X")  # ペア削除ボタン
                del_op.pattern_index = i
                del_op.rule_index = j

            # 識別子ペア追加ボタンをセット内に設置
            box.operator("mwr.add_bone_rule", text=_("Add a pair"), icon="ADD").index = i

            # 右側：セット削除ボタン（枠の外）
            col_right = row_outer.column() # ぴったりボタン同士をくっつけたい場合は(align=True)
            col_right.separator()  # セパレータで上にスペースを追加
            col_right.operator("mwr.delete_bone_pattern", text="", icon="X").index = i  # セット削除ボタン

        main_box.separator()

        row = main_box.row()
        row.operator("mwr.add_bone_pattern", text=_("Add Identifier Set"), icon="COLLECTION_NEW") # 識別端子セットの追加
        row.operator("mwr.append_default_bone_set", text=_("Restore Default Set"), icon="COPY_ID") # デフォルトセットの復元

        row = main_box.row()    # ぴったりボタン同士をくっつけたい場合は(align=True)
        row.operator("mwr.sync_bone_patterns", text=_("Synchronize"), icon="FILE_REFRESH")
        row.operator("mwr.reset_bone_patterns", text=_("Reset"), icon="DECORATE_OVERRIDE")
        row.operator("mwr.save_bone_patterns", text=_("Save"), icon="FILE_TICK")

# プリファレンスの編集UI
class MWR_OT_AddBonePattern(bpy.types.Operator):
    """識別子セットを追加"""
    bl_idname = "mwr.add_bone_pattern"
    bl_label = "Add Identifier Set"
    bl_description = _("Add a new identifier set to the preferences")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences

        pattern = prefs.bone_patterns.add()
        pattern.label = "New Set"
        rule = pattern.rules.add()
        rule.right = "R"
        rule.left = "L"
        rule.use_regex = False

        self.report({'INFO'}, _("A new set of identifiers has been added"))
        return {'FINISHED'}


class MWR_OT_AddBoneRule(bpy.types.Operator):
    """識別子ルールを追加"""
    bl_idname = "mwr.add_bone_rule"
    bl_label = "Add Identifier Rule"
    bl_description = _("Add a left-right identifier rule to the selected set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()  # 追加対象の bone_patterns インデックス

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences

        rule = prefs.bone_patterns[self.index].rules.add()
        rule.right = ""
        rule.left = ""
        rule.use_regex = False

        self.report({'INFO'}, _("Identifier pair has been added"))
        return {'FINISHED'}


# 識別子セットの移動ボタン
class MWR_OT_MoveBonePatternUp(bpy.types.Operator):
    """↑ 上に移動"""
    bl_idname = "mwr.move_bone_pattern_up"
    bl_label = "Move Indentifier Set Up"
    bl_description = _("Move the identifier set up one position")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
        i = self.index

        if i <= 0:
            self.report({'WARNING'}, _("Already at the top"))
            return {'CANCELLED'}

        prefs.bone_patterns.move(i, i - 1)
        self.report({'INFO'}, _("Moved up"))
        return {'FINISHED'}


class MWR_OT_MoveBonePatternDown(bpy.types.Operator):
    """↓ 下に移動"""
    bl_idname = "mwr.move_bone_pattern_down"
    bl_label = "Move Indentifier Set Down"
    bl_description = _("Move the identifier set down one position")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
        i = self.index

        if i < len(prefs.bone_patterns) - 1:
            prefs.bone_patterns.move(i, i + 1)
            self.report({'INFO'}, _("Moved down"))
        else:
            self.report({'WARNING'}, _("Already at the bottom"))
        return {'FINISHED'}



class MWR_OT_SaveBonePatterns(bpy.types.Operator):
    """識別子セットを保存"""
    bl_idname = "mwr.save_bone_patterns"
    bl_label = "Save Identifier Sets"
    bl_description = _("Save all identifier sets to a JSON file")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
        data = []

        for p in prefs.bone_patterns:
            label = p.label.strip()
            if not label:
                self.report({'WARNING'}, _("Please enter a name for the identifier set"))   # 識別子セットの名前を入力してください
                return {'CANCELLED'}
            if any(ord(c) > 127 for c in label):
                self.report({'WARNING'}, _("{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name").format(label=label))
                return {'CANCELLED'}        # {label}には使用できない文字が含まれています。セット名には半角英数字のみを使用してください

            complete = [r for r in p.rules if r.right.strip() and r.left.strip()]
            incomplete = [r for r in p.rules if (r.right.strip() and not r.left.strip()) or (not r.right.strip() and r.left.strip())]

            if not complete:
                self.report({'WARNING'}, _("{label} requires identifier pairs with both sides filled in").format(label=label))
                return {'CANCELLED'}    # {label}には両側が入力された識別子ペアが必要です
            if incomplete:
                self.report({'WARNING'}, _("There is an identifier pair with only one side").format(label=label))
                return {'CANCELLED'}        # {label}に片側だけの識別子ペアがあります

            rules = [{
                "right": r.right,
                "left": r.left,
                "use_regex": r.use_regex
            } for r in p.rules]
            data.append({"label": label, "rules": rules})

        save_json_data(data)
        self.report({'INFO'}, _("Saved!"))
        load_bone_patterns_to_preferences(prefs)
        return {'FINISHED'}
    
class MWR_OT_ResetBonePatterns(bpy.types.Operator):
    """JSONファイルを読み直して識別子セットを元に戻します"""
    bl_idname = "mwr.reset_bone_patterns"
    bl_label = "Reload Identifier Sets"
    bl_description = _("Reload the identifier sets from the saved JSON file")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        load_bone_patterns_to_preferences(context.preferences.addons["DIVA_MeshWeightReflector"].preferences)
        self.report({'INFO'}, _("Reloaded identifier sets"))
        return {'FINISHED'}

class MWR_OT_SyncBonePatterns(bpy.types.Operator):
    """識別子セットを同期"""
    bl_idname = "mwr.sync_bone_patterns"
    bl_label = "Sync Identifier Sets"
    bl_description = _("Synchronize identifier sets")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        try:
            synced = sync_bone_patterns()
            if synced:
                joined = ", ".join(synced)
                self.report({'INFO'}, _("Synchronized: {names}").format(names=joined))
            else:
                self.report({'WARNING'}, _("No addons were synchronized"))
        except Exception as e:
            self.report({'ERROR'}, _("Sync failed: {msg}").format(msg=str(e)))
        return {'FINISHED'}


class MWR_OT_AppendDefaultSet(bpy.types.Operator):
    """コード定義のデフォルトセットを先頭に追加します"""
    bl_idname = "mwr.append_default_bone_set"
    bl_label = "Append Default Set"
    bl_description = _("Insert the default set of identifiers at the top")
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
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

        self.report({'INFO'}, _("Default set added"))
        return {'FINISHED'}
    

class MWR_OT_DeleteBonePattern(bpy.types.Operator):
    """識別子セットの削除"""
    bl_idname = "mwr.delete_bone_pattern"
    bl_label = "Delete Identifier Set"
    bl_description = _("Delete the selected identifier set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
        if len(prefs.bone_patterns) <= 1:
            self.report({'WARNING'}, _("At least one identifier set must be defined"))
            return {'CANCELLED'}        # 最低でも1つの識別子セットを設定してください
        prefs.bone_patterns.remove(self.index)
        return {'FINISHED'}


class MWR_OT_DeleteBoneRule(bpy.types.Operator):
    """識別子ペアの削除"""
    bl_idname = "mwr.delete_bone_rule"
    bl_label = "Delete Identifier Pair"
    bl_description = _("Remove the selected identifier pair from the set")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    pattern_index: bpy.props.IntProperty()
    rule_index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences

        try:
            pattern = prefs.bone_patterns[self.pattern_index]
            if len(pattern.rules) <= 1:
                self.report({'WARNING'}, _("At least one pair is required"))
                return {'CANCELLED'}

            pattern.rules.remove(self.rule_index)
            self.report({'INFO'}, _("Identifier pair removed"))
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, _("Failed to delete: {msg}").format(msg=str(e)))
            return {'CANCELLED'}




def get_classes():
    return [
        MWR_OT_AddBonePattern,
        MWR_OT_AddBoneRule,
        MWR_OT_DeleteBonePattern,
        MWR_OT_DeleteBoneRule,
        MWR_OT_MoveBonePatternUp,
        MWR_OT_MoveBonePatternDown,
        MWR_OT_ResetBonePatterns,
        MWR_OT_SaveBonePatterns,
        MWR_OT_SyncBonePatterns,
        MWR_OT_AppendDefaultSet,
        MWR_AddonPreferences,
    ]



