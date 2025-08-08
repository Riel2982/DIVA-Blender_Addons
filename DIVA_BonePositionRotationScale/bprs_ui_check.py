# bprs_ui_check.py

import bpy
from bpy.app.translations import pgettext as _

from . import DivaBonePositionRotationScale
from . bprs_check import parse_bone_data_string, get_bone_data_map, collect_correction_data, set_checked_armature_as_active

from .bprs_debug import DEBUG_MODE   # デバッグ用

# --- セクション 3: ボーンデータ確認 ------------------------------------------
def draw_check_ui(layout, context, scene):
    box = layout.box()  # 枠付きセクションを作る
    row = box.row(align=True)
    row.prop(scene, "bprs_show_check_tools", text="", icon='DOWNARROW_HLT' if scene.bprs_show_check_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Bone Data Checker", icon="WORKSPACE") # セクションタイトル

    # パネル描画
    if scene.bprs_show_check_tools:
        row = box.row()
        box.operator("bprs.check_bone_data", text="Check Bone Data", icon='WORKSPACE')  # 実行ボタン
        row = box.row()
        if not scene.bprs_bones_data:
            row.label(text=_("Please execute the checker after selecting an armature"), icon='INFO')
        else:
            checked_name = getattr(scene, "bprs_last_checked_armature", None)
            row.label(text="{name}".format(name=checked_name), icon='OUTLINER_OB_ARMATURE')     # ボーンデータのアーマチュア名

        # 左側：表示モード切替
        row = box.row()
        split = row.split(factor=0.7)
        left = split.row()
        left.prop(scene.bprs_filter_settings, "bprs_display_mode", text=_("List Mode")) 

        # 🔸 中央列：選択中ボーンを表示切り替え
        mid = split.row(align=True)
        op_add = mid.operator("bprs.toggle_show_selected", text="", icon='ADD')
        op_add.value = True
        op_remove = mid.operator("bprs.toggle_show_selected", text="", icon='REMOVE')
        op_remove.value = False

        # 左列：選択トグル
        inner = split.row(align=True)
        op_on = inner.operator("bprs.toggle_all_bone_select", text="", icon='RESTRICT_SELECT_OFF')
        op_on.toggle_on = True
        op_off = inner.operator("bprs.toggle_all_bone_select", text="", icon='RESTRICT_SELECT_ON')
        op_off.toggle_on = False

        # 右側：一括選択切り替え
        right = split.row(align=True)
        op_on = right.operator("bprs.toggle_all_show_info", text="", icon='CHECKBOX_HLT')
        op_on.value = True
        op_off = right.operator("bprs.toggle_all_show_info", text="", icon='CHECKBOX_DEHLT')
        op_off.value = False

        # アーマーチュアのボーンリスト
        box.template_list("BPRS_UL_BoneDataList", "", scene, "bprs_bones_data", scene, "bprs_bones_data_index", rows=6)

        # 🧩 補正情報の動的UI表示
        draw_bone_correction_info(layout.box(), context, scene)  # 分離された補正情報UI呼び出し



class BPRS_OT_CheckBoneData(bpy.types.Operator):
    """アーマチュアのボーンデータを取得して表示リストに登録する"""
    bl_idname = "bprs.check_bone_data"
    bl_label = "Check Bone Data"
    # bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("Retrieve armature bone data and register to the display list")

    def execute(self, context):
        obj = context.object
        scene = context.scene

        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, _("The selected object is not an armature: {name}").format(name=obj.name if obj else "None"))
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')  # 編集モードに切替

        scene.bprs_bones_data.clear()   # ボーンデータの初期化
        scene.bprs_last_checked_armature = obj.name     # シュトクアーマチュア名の記録

        try:
            bone_data = DivaBonePositionRotationScale.get_bone_data()

            bone_data_map = get_bone_data_map()

            if not bone_data_map:
                self.report({'WARNING'}, _("Failed to retrieve bone data"))
                return {'CANCELLED'}

            for bone_name in bone_data_map.keys():
                item = scene.bprs_bones_data.add()
                item.name = bone_name

            count = len(bone_data_map)
            self.report({'INFO'},_("Retrieved {count} bones from armature: {name}").format(count=count, name=obj.name)
)
            return {'FINISHED'}

        except Exception as e:
            self.report({'WARNING'}, _("Retrieval error: {error}").format(error=str(e)))
            return {'CANCELLED'}


# アーマチュアのボーンリストの表示
class BPRS_UL_BoneDataList(bpy.types.UIList):
    def filter_items(self, context, data, propname):
        arm = context.object
        if not arm or arm.type != 'ARMATURE':
            return [], []

        ebones = arm.data.edit_bones
        items = getattr(data, propname)
        mode = context.scene.bprs_filter_settings.bprs_display_mode

        flags = []

        for item in items:
            bone_name = item.name
            ebone = ebones.get(bone_name)
            is_selected = ebone and ebone.select
            is_hidden = ebone and ebone.hide

            # 表示条件に応じてフィルター適用
            if mode == 'ALL': # すべて表示
                flags.append(self.bitflag_filter_item)
            elif mode == 'VISIBLE':     # 表示中のみ
                if ebone and not ebone.hide:
                    flags.append(self.bitflag_filter_item)
                else:
                    flags.append(0)
            elif mode == 'SELECTED':    # 選択中のみ表示
                flags.append(self.bitflag_filter_item if is_selected else 0)
            elif mode == 'UNSELECTED':  # 非選択中のみ表示
                flags.append(self.bitflag_filter_item if not is_selected else 0)
            else:
                flags.append(0)

        return flags, []

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            arm = context.object
            ebones = arm.data.edit_bones if arm and arm.type == 'ARMATURE' else {}

            bone_name = item.name
            ebone = ebones.get(bone_name)
            is_selected = ebone and ebone.select
            icon_id = 'RESTRICT_SELECT_OFF' if is_selected else 'RESTRICT_SELECT_ON'

            label_text = "{num:03} : {name}".format(num=index + 1, name=bone_name)

            row = layout.row(align=True)
            row.operator_context = 'INVOKE_DEFAULT'  # Shift / Alt 連動

            # 🔹 すべてを同一行に並べる
            row.prop(item, "show_info", text="", emboss=True)

            select_op = row.operator("bprs.toggle_bone_select", text="", icon=icon_id, emboss=False)
            select_op.bone_name = bone_name
            row.separator()

            row.label(text=label_text)

def draw_bone_correction_info(layout, context, scene):
    arm = context.object
    bone_data_text = DivaBonePositionRotationScale.get_bone_data()
    if not bone_data_text:
        return

    # 非UI処理を関数化して取得
    correction_blocks = collect_correction_data(scene, arm, bone_data_text)

    for bone_name, info_entries in correction_blocks:
        outer_box = layout.box()
        row = outer_box.row(align=True)
        split = row.split(factor=0.3, align=False)
        split.label(text=" Bone Name")
        split.label(text=bone_name)
        copy = row.operator("bprs.copy_to_clipboard", text="", icon='COPYDOWN')
        copy.text = bone_name
        row.separator()

        inner_box = outer_box.box()

        def add_row(label, value):
            row = inner_box.row(align=True)
            split = row.split(factor=0.3, align=False)
            split.label(text=label)
            split.label(text=value)
            copy = row.operator("bprs.copy_to_clipboard", text="", icon='COPYDOWN')
            copy.text = value

        for label, value in info_entries:
            add_row(label, value)


if False:
    for item in scene.bprs_bones_data:
        if not item.show_info:  # ✅ チェックされていないボーンはスキップ
            continue

        bone_name = item.name
        info_lines = bone_data_map.get(bone_name)
        if not info_lines:
            continue

        bone = arm.data.bones.get(bone_name)
        bone_length = bone.length if bone else 0.0

        box = layout.box()
        # box.label(text=f"{bone_name} 補正情報", icon='BONE_DATA')

        def add_row(label, value):
            row = box.row(align=True)
            split = row.split(factor=0.3, align=False)   # 表示幅の調整（ラベル30$）
            split.label(text=label)
            split.label(text=value)
            copy = row.operator("bprs.copy_to_clipboard", text="", icon='COPYDOWN')
            copy.text = value

        add_row("Bone Name", bone_name)

        for line in info_lines[1:]:
            parts = line.lstrip().split(": ", 1)
            if len(parts) == 2:
                label, value = parts
                add_row(label.strip(), value.strip())
            else:
                add_row("?", "[未取得]")

        add_row("Length", "{:.6f}".format(bone_length))

if False:
    def draw_bone_correction_info(layout, context, scene):
        arm = context.object
        index = scene.bprs_bones_data_index
        if index >= len(scene.bprs_bones_data):
            return

        bone_name = scene.bprs_bones_data[index].name
        bone_data_text = DivaBonePositionRotationScale.get_bone_data()

        # ボーン単位で分割（\n\n区切り → 各ブロックを対象に）
        bone_blocks = bone_data_text.strip().split("\n\n")
        info_lines = None
        for block in bone_blocks:
            lines = block.strip().split("\n")
            if lines and lines[0].strip() == bone_name:
                info_lines = lines
                break
        if not info_lines:
            return
        
        if DEBUG_MODE:
            # デバッグ用
            print("=== DEBUG: info_lines ===")
            for i, line in enumerate(info_lines):
                print(f"[{i}] {repr(line)}")

        bone = arm.data.bones.get(bone_name)
        bone_length = bone.length if bone else 0.0

        box = layout.box()
        # box.label(text="補正後ボーン情報", icon='BONE_DATA')

        def add_row(label, value):
            row = box.row(align=True)
            split = row.split(factor=0.4, align=True)  # ラベルと値を左右に分割

            split.label(text=label)                    # 左：ラベル
            split.label(text=value)                    # 右：値を表示
            copy = row.operator("bprs.copy_to_clipboard", text="", icon='COPYDOWN')     # コピペ用ボタン
            copy.text = value

        # ✅ 確実に全行表示（順序固定）
        add_row("Bone Name", bone_name)
        for line in info_lines[1:]:  # ParentName～Scaleをラベルごと抽出
            parts = line.lstrip().split(": ", 1)

            if DEBUG_MODE:
                print(f"DEBUG SPLIT: {repr(parts)} from line: {repr(line)}")        # デバッグ用
            
            if len(parts) == 2:
                label, value = parts
                add_row(label.strip(), value.strip())
            else:
                label, value = line.strip(), "[未取得]"
                add_row(label.strip(), value.strip())

        add_row("Length", "{:.6f}".format(bone_length))





class BPRS_OT_CopyToClipboard(bpy.types.Operator):
    """指定された文字列をクリップボードにコピーする"""
    bl_idname = "bprs.copy_to_clipboard"
    bl_label = "Copy to Clipboard"
    bl_description = _("Copy the specified string to the clipboard")

    text: bpy.props.StringProperty()

    def execute(self, context):
        context.window_manager.clipboard = self.text
        self.report({'INFO'}, _("Copied to clipboard"))
        return {'FINISHED'}


class BPRS_OT_ToggleAllShowInfo(bpy.types.Operator):
    """ボーン表示のチェックを一括 ON/OFF"""
    bl_idname = "bprs.toggle_all_show_info"
    bl_label = "Toggle checkbox"
    bl_description = _("Toggle bone display checkboxes ON/OFF in bulk")

    value: bpy.props.BoolProperty()

    def execute(self, context):
        scene = context.scene
        for item in scene.bprs_bones_data:
            item.show_info = self.value
        return {'FINISHED'}


# アーマチュアボーンの選択状態をトグル
class BPRS_OT_ToggleBoneSelect(bpy.types.Operator):
    """ ボーンを選択\n Shift：追加選択\n Alt：選択解除 """    # \nで改行    
    bl_idname = "bprs.toggle_bone_select"
    bl_label = "Toggle Bone Select"
    # bl_options = {'INVOKE_DEFAULT'}  # 4.xのみ
    bl_description = _("Select Bone \n Shift: Add Selection \n Alt: Deselect")     # bl_descriptionは英語に翻訳できない

    bone_name: bpy.props.StringProperty()

    def invoke(self, context, event):
        arm = set_checked_armature_as_active(context, self)   # ボーンデータのアーマチュアの編集モードに切り替える
        if not arm:
            self.report({'WARNING'}, _("No valid armature found"))
            return {'CANCELLED'}
        '''
        if not arm or arm.type != 'ARMATURE':
            self.report({'WARNING'}, _("No armature is selected"))
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='EDIT')  # 安全に編集モードへ
        '''

        ebone = arm.data.edit_bones.get(self.bone_name)
        if not ebone:
            self.report({'WARNING'}, _("Target bone not found: {name}").format(name=self.bone_name))
            return {'CANCELLED'}

        is_selected = ebone.select

        if event.shift:             # Shift でトグル追加・解除
            ebone.select = not is_selected
        elif event.alt:            # Alt で解除
            ebone.select = False
        else:
            # 単独選択：他の選択を解除
            for b in arm.data.edit_bones:
                b.select = False
            ebone.select = True

        return {'FINISHED'}


class BPRS_OT_ToggleAllBoneSelect(bpy.types.Operator):
    """リストに表示中のボーンを一括で選択／選択解除"""
    bl_idname = "bprs.toggle_all_bone_select"
    bl_label = "Toggle All Bone Select"
    bl_description = _("Select or deselect all bones currently visible in the list")

    toggle_on: bpy.props.BoolProperty()


    def execute(self, context):
        arm = context.object
        if not arm or arm.type != 'ARMATURE':
            self.report({'WARNING'}, _("No armature is selected"))
            return {'CANCELLED'}

        if context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = arm.data.edit_bones
        bones_data = context.scene.bprs_bones_data
        display_mode = context.scene.bprs_filter_settings.bprs_display_mode

        updated_count = 0
        for item in bones_data:
            bone_name = item.name
            ebone = edit_bones.get(bone_name)

            # ⬇ 表示対象のフィルタに基づいて処理
            if not ebone or ebone.hide:
                continue

            is_selected = ebone.select

            visible = (
                display_mode == 'ALL' or
                (display_mode == 'VISIBLE' and not ebone.hide) or
                (display_mode == 'SELECTED' and is_selected) or
                (display_mode == 'UNSELECTED' and not is_selected)
            )

            if visible:
                ebone.select = self.toggle_on
                updated_count += 1

        mode_str = _("selected") if self.toggle_on else _("deselected")
        self.report({'INFO'}, _("{count} visible bones {mode}").format(count=updated_count, mode=mode_str))
        return {'FINISHED'}

class BPRS_OT_ShowSelected(bpy.types.Operator):
    """編集モードで選択中のボーンに対して表示フラグを ON/OFF"""
    bl_idname = "bprs.toggle_show_selected"
    bl_label = "Show Selected Bones"
    bl_description = _("Toggle display flag for selected bones in edit mode")

    value: bpy.props.BoolProperty()

    def execute(self, context):
        arm = context.object
        if not arm or arm.type != 'ARMATURE':
            self.report({'WARNING'}, _("No armature is selected"))
            return {'CANCELLED'}

        edit_bones = arm.data.edit_bones
        bones_data = context.scene.bprs_bones_data

        affected_count = 0
        for item in bones_data:
            ebone = edit_bones.get(item.name)
            if ebone and ebone.select:
                item.show_info = self.value
                affected_count += 1

        mode_str = _("added") if self.value else _("removed")
        self.report({'INFO'}, _("{count} bones were {mode} from display").format(count=affected_count, mode=mode_str))
        return {'FINISHED'}


# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        BPRS_OT_CheckBoneData,
        BPRS_UL_BoneDataList,
        BPRS_OT_ToggleAllShowInfo,
        BPRS_OT_CopyToClipboard,
        BPRS_OT_ToggleBoneSelect,
        BPRS_OT_ToggleAllBoneSelect,
        BPRS_OT_ShowSelected,

    ]

