import bpy
from .btt_main import run_transfer_logic

# UI & メニュー
class BTT_PT_BoneTransferPanel(bpy.types.Panel):
    """ DIVAタブのNパネルUI（スポイト選択 + オプション付き） """
    bl_label = "Bone Transfer Tools"
    bl_idname = "VIEW3D_PT_bone_transfer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DIVA'

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='CONSTRAINT_BONE') # ボーン移植風

    def draw(self, context):
        layout = self.layout
        scene = bpy.data.scenes[0]

        box = layout.box()  # 枠付きセクションを作成
             
        # 統合先アーマーチュア（ラベル20% + プロパティ80%）
        split1 = box.split(factor=0.20, align=True)
        split1.label(text="統合先:", icon='OUTLINER_OB_ARMATURE')
        split1.prop(scene, "btt_merge_target_armature", text="")

        # 移植元アーマーチュア（ラベル20% + プロパティ80%）
        split2 = box.split(factor=0.20, align=True)
        split2.label(text="移植元:", icon='OUTLINER_OB_ARMATURE')
        split2.prop(scene, "btt_armature_b", text="")


        # 移植元メッシュのリスト管理（選択状態と同期を削除）
        box.label(text="移植元オブジェクトリスト:", icon='OUTLINER_OB_MESH')
        row = box.row()
        row.operator("btt.add_to_transfer_list", text="Add")
        row.operator("btt.remove_from_transfer_list", text="Remove")
        row.operator("btt.clear_transfer_list", text="Clear")
        row.operator("btt.toggle_all_use_child_bones", text="", icon='AUTOMERGE_ON')

        # 👇 可変枠・スクロール・選択同期つきリスト表示
        box.template_list(
            "BTT_UL_TransferObjectList", "", 
            scene, "btt_source_objects", 
            scene, "btt_source_objects_index", 
            rows=6  # 初期行数（上下ドラッグで調整可）
        )

        row = box.row()
        row.prop(scene, "btt_duplicate_object", text="")  # チェックボックス
        row.label(text="複製して移植")

        row = box.row()
        row.prop(scene, "btt_bones_only_transfer", text="")  # チェックボックス
        row.label(text="ボーンのみ移植")

        # 実行ボタン
        box.operator("btt.bone_transfer", icon="ARMATURE_DATA")


class BTT_OT_BoneTransfer(bpy.types.Operator):
    """ Nパネル用：移植実行オペレータ """
    bl_idname = "btt.bone_transfer"
    bl_label = "ボーンとオブジェクトを移植"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        a = scene.btt_merge_target_armature
        b = scene.btt_armature_b
        b1_list = scene.btt_source_objects
        dupe = scene.btt_duplicate_object
        bones_only = scene.btt_bones_only_transfer

        # `a` と `b` が `ARMATURE` 型のオブジェクトであることを保証
        if not a or not isinstance(a, bpy.types.Object) or a.type != 'ARMATURE':
            self.report({'ERROR'}, "統合先アーマーチュア (A) は 'ARMATURE' 型のオブジェクトである必要があります。")
            return {'CANCELLED'}

        if not b or not isinstance(b, bpy.types.Object) or b.type != 'ARMATURE':
            self.report({'ERROR'}, "移植元アーマーチュア (B) は 'ARMATURE' 型のオブジェクトである必要があります。")
            return {'CANCELLED'}

        if not b1_list or len(b1_list) == 0:
            self.report({'ERROR'}, "移植元オブジェクト（B1）を選択してください")
            return {'CANCELLED'}

        new_names = []
        total_bones = 0

        for b1 in b1_list:
            new_name, count = run_transfer_logic(a, b, b1, dupe, bones_only)
            new_names.append(new_name)
            total_bones += count

        self.report({'INFO'}, f"{', '.join(new_names)} に合計 {total_bones} 本のボーンを移植しました")
        return {'FINISHED'}


class BTT_OT_AddToTransferList(bpy.types.Operator):
    """ 選択中のメッシュオブジェクトを処理リストに追加 """
    bl_idname = "btt.add_to_transfer_list"
    bl_label = "Add"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        transfer_list = scene.btt_source_objects

        # 現在選択されているメッシュオブジェクトのみを取得
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        # 選択オブジェクトがない場合はエラーを返す
        if not selected_objects:
            self.report({'ERROR'}, "メッシュオブジェクトが選択されていません")
            return {'CANCELLED'}

        # リストの上限を設定（大量登録によるクラッシュを防ぐ）
        if len(transfer_list) + len(selected_objects) > 100:
            self.report({'ERROR'}, "移植リストが上限に達しました（最大100個）")
            return {'CANCELLED'}

        # 重複登録を防ぐ
        existing_names = {item.name for item in transfer_list}
        added_count = 0

        for obj in selected_objects:
            if obj.name not in existing_names:
                item = transfer_list.add()
                item.name = obj.name
                item.object = obj
                added_count += 1

        if added_count > 0:
            self.report({'INFO'}, f"{added_count} 個のメッシュを追加しました")
        else:
            self.report({'WARNING'}, "すべてのオブジェクトがすでに登録されています")

        return {'FINISHED'}


class BTT_OT_RemoveFromTransferList(bpy.types.Operator):
    """ 移植リストから削除 """
    bl_idname = "btt.remove_from_transfer_list"
    bl_label = "Remove"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        transfer_list = scene.btt_source_objects

        # オブジェクト選択処理を削除
        if transfer_list:
            transfer_list.remove(scene.btt_source_objects_index)

        self.report({'INFO'}, "リストから削除しました")
        return {'FINISHED'}


class BTT_OT_ClearTransferList(bpy.types.Operator):
    """ 移植リストをクリア """
    bl_idname = "btt.clear_transfer_list"
    bl_label = "Clear"

    def execute(self, context):
        bpy.data.scenes[0].btt_source_objects.clear()
        self.report({'INFO'}, "移植リストをリセットしました")
        return {'FINISHED'}

''' # btt_main.pyに移設（循環インポートエラー対策）
class BTT_PG_TransferObject(bpy.types.PropertyGroup):
    """ ボーン移植リスト用のプロパティグループ """
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)
'''
    

# 移植メッシュリストの表示（選択状態トグル＋削除ボタン付き）
class BTT_UL_TransferObjectList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.object
        obj_name = obj.name if obj else "未設定"

        row = layout.row(align=True)
        row.operator_context = 'INVOKE_DEFAULT' # Shift/Alt切り替えのポイント

        # 見た目を2列に分割して仕切り風に
        split = row.split(factor=0.05, align=True)  # ← ここで「仕切り風」になる！
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        # 左列：選択トグル
        icon_id = 'RESTRICT_SELECT_OFF' if obj and obj.select_get() else 'RESTRICT_SELECT_ON'
        op = col1.operator("btt.toggle_object_select", text="", icon=icon_id, emboss=False)
        op.object_name = obj_name

        # 中央列：子ボーントグル
        inner_row = col2.row(align=True)
        icon_child = 'AUTOMERGE_ON' if item.use_child_bones else 'AUTOMERGE_OFF'
        inner_row.prop(item, "use_child_bones", text="", icon=icon_child, emboss=False)

        # 右列：名前表示（インデックス番号を行揃え）
        # index_str = str(index + 1).rjust(3)  # ← 左にスペースを詰めて右寄せ： '  9', ' 10', '100'（最大三桁想定）
        index_str = str(index + 1).zfill(3) # 001, 010, 100のようなゼロ埋め揃え（同じく最大三桁）

        label_text = f"{index_str} : {obj_name}"
        inner_row.label(text=label_text) # , icon='OBJECT_DATA')

        # 右列右端：削除ボタン
        rm = inner_row.operator("btt.remove_object_by_name", text="", icon='X', emboss=False)
        rm.object_name = obj_name


# メッシュオブジェクトの選択状態をトグル
class BTT_OT_ToggleObjectSelect(bpy.types.Operator):
    bl_idname = "btt.toggle_object_select"
    bl_label = "Toggle Object Selection"
    # bl_options = {'INVOKE_DEFAULT'}  # 4.xのみ
    bl_description = (
        "オブジェクトを選択\n"
        "Shift：追加選択\n"
        "Alt：選択解除"
    )    
    object_name: bpy.props.StringProperty()

    def invoke(self, context, event):
        obj = bpy.data.objects.get(self.object_name)
        if not obj or obj.type != 'MESH':
            return {'CANCELLED'}

        is_selected = obj.select_get()

        if event.shift:
            obj.select_set(not is_selected)  # Shift でトグル追加・解除
        elif event.alt:
            obj.select_set(False)            # Alt で解除
        else:
            # 通常クリックで単独選択
            for o in context.view_layer.objects:
                o.select_set(False)
            obj.select_set(True)

        return {'FINISHED'}

# オブジェクト名を指定してリストから削除 """
class BTT_OT_RemoveObjectByName(bpy.types.Operator):
    bl_idname = "btt.remove_object_by_name"
    bl_label = "Remove Object from Transfer List"
    bl_description = ("リストからオブジェクトを削除")    

    object_name: bpy.props.StringProperty()

    def execute(self, context):
        transfer_list = context.scene.btt_source_objects
        for i, item in enumerate(transfer_list):
            if item.name == self.object_name:
                transfer_list.remove(i)
                break
            self.report({'INFO'}, "リストから削除しました")
        return {'FINISHED'}

class BTT_OT_ToggleAllUseChildBones(bpy.types.Operator):
    bl_idname = "btt.toggle_all_use_child_bones"
    bl_label = "子ボーン設定をトグル"
    bl_description = "すべてのメッシュのウエイトのない子ボーン移植設定をON/OFF切り替えます"

    def execute(self, context):
        items = context.scene.btt_source_objects
        if not items:
            return {'CANCELLED'}

        # 一括反転方式（1番目の状態を基準にして反転）
        current = items[0].use_child_bones
        for item in items:
            item.use_child_bones = not current

        self.report({'INFO'}, f"全てのメッシュに対して子ボーン設定を {'無効化' if current else '有効化'}しました")
        return {'FINISHED'}

class BTT_PG_TransferObject(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    use_child_bones: bpy.props.BoolProperty(
        name="子ボーンも含める",
        default=True,
        description="ウェイトのある親ボーンを移植する際に、ウエイトのない子ボーンも一緒に移植するかを切り替えます"
    )

# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        BTT_PT_BoneTransferPanel,
        BTT_OT_BoneTransfer,
        BTT_UL_TransferObjectList,
        BTT_OT_AddToTransferList,
        BTT_OT_RemoveFromTransferList,
        BTT_OT_ClearTransferList,
        BTT_PG_TransferObject,
        BTT_OT_ToggleObjectSelect,
        BTT_OT_RemoveObjectByName, 
        BTT_OT_ToggleAllUseChildBones,
    ]

# Scene プロパティ登録処理
def register_properties():
    bpy.types.Scene.btt_merge_target_armature = bpy.props.PointerProperty(
        name="統合先アーマーチュア", type=bpy.types.Object, poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.Scene.btt_armature_b = bpy.props.PointerProperty(
        name="移植元アーマーチュア", type=bpy.types.Object, poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.Scene.btt_source_objects = bpy.props.CollectionProperty(
        name="移植オブジェクトリスト", type=BTT_PG_TransferObject
    )
    bpy.types.Scene.btt_source_objects_index = bpy.props.IntProperty(
        name="移植対象オブジェクト名", default=0
    )
    bpy.types.Scene.btt_duplicate_object = bpy.props.BoolProperty(
        name="複製して移植", default=True
    )
    bpy.types.Scene.btt_bones_only_transfer = bpy.props.BoolProperty(
        name="ボーンのみ移植", default=False
    )

# プロパティ削除処理
def unregister_properties():
    del bpy.types.Scene.btt_merge_target_armature
    del bpy.types.Scene.btt_armature_b
    del bpy.types.Scene.btt_source_objects
    del bpy.types.Scene.btt_source_objects_index
    del bpy.types.Scene.btt_duplicate_object
    del bpy.types.Scene.btt_bones_only_transfer
