import bpy
from .btt_main import (
    run_transfer_logic,
    collect_transfer_bone_names,
    transfer_bones,
    reparent_and_cleanup,
)
from .btt_types import BTT_PG_TransferObject

# ボタンを分離して切り替える場合
class BTT_OT_SetAllUseChildBones(bpy.types.Operator):
    bl_idname = "btt.set_all_use_child_bones"
    bl_label = "Set Use Child Bones State"
    bl_description = "すべてのオブジェクトにウエイト設定のない子ボーンのON/OFF状態を一括適用します"

    state: bpy.props.BoolProperty()  # True=ON, False=OFF

    def execute(self, context):
        items = context.scene.btt_source_objects
        if not items:
            return {'CANCELLED'}

        for item in items:
            item.use_child_bones = self.state

        self.report({'INFO'}, f"All items set to {'use' if self.state else 'not use'} child bones")
        return {'FINISHED'}

    @classmethod
    def description(cls, context, properties):
        return (
            "Include unweighted child bones in transfer"
            if properties.state
            else "Exclude unweighted child bones from transfer"
        )

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

        # 左側：Add / Remove / Clear を程よい間隔で並べる
        split = row.split(factor=0.9, align=False)
        left = split.row()
        left.operator("btt.add_to_transfer_list", text="Add")
        left.operator("btt.remove_from_transfer_list", text="Remove")
        left.operator("btt.clear_transfer_list", text="Clear")

        # リストのオブジェクトを一括で選択状態に
        left.operator("btt.select_all_transfer_objects", text="", icon='RESTRICT_SELECT_OFF')

        # 右側：2ボタンをぴったり並べる
        right = split.row(align=True)
        op_on = right.operator("btt.set_all_use_child_bones", text="", icon='AUTOMERGE_ON')
        op_on.state = True
        op_off = right.operator("btt.set_all_use_child_bones", text="", icon='AUTOMERGE_OFF')
        op_off.state = False

        '''
        box.label(text="移植元オブジェクトリスト:", icon='OUTLINER_OB_MESH')
        row = box.row()
        row.operator("btt.add_to_transfer_list", text="Add")
        row.operator("btt.remove_from_transfer_list", text="Remove")
        row.operator("btt.clear_transfer_list", text="Clear")
        row.operator("btt.toggle_all_use_child_bones", text="", icon='AUTOMERGE_ON')  # ボタン一つで切り替える場合
        '''

        # 可変枠・スクロール・選択同期つきリスト表示
        box.template_list(
            "BTT_UL_TransferObjectList", "", 
            scene, "btt_source_objects", 
            scene, "btt_source_objects_index", 
            rows=6  # 初期行数（上下ドラッグで調整可）
        )
        
        # 1行目：左＝複製チェック、右＝アーマチュア全体を移植チェック
        row = box.row()
        split = row.split(factor=0.5, align=False)

        # 左側：複製して移植
        col_left = split.row()
        col_left.prop(scene, "btt_duplicate_object", text="")
        col_left.label(text="複製して移植")

        # 右側：アーマチュア全体を移植
        col_right = split.row()
        col_right.prop(scene, "btt_transfer_entire_armature", text="")
        col_right.label(text="アーマチュア全体を移植")

        # 2行目：左＝通常実行、右＝ボーンのみ移植
        row = box.row()
        split = row.split(factor=0.5, align=False)

        # 左側：通常のボーン＋オブジェクト移植
        split.operator("btt.bone_transfer", text="ボーンとオブジェクトを移植", icon="MATCLOTH")

        # 右側：ボーンのみ移植
        split.operator("btt.bone_transfer_bones_only", text="ボーンのみ移植", icon="ARMATURE_DATA")  

        
        '''
        # 実行ボタン分割前
        row = box.row()
        row.prop(scene, "btt_duplicate_object", text="")  # チェックボックス
        row.label(text="複製して移植")

        row = box.row()
        row.prop(scene, "btt_bones_only_transfer", text="")  # チェックボックス
        row.label(text="ボーンのみ移植")

        # 実行ボタン
        box.operator("btt.bone_transfer", icon="ARMATURE_DATA")
        '''


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
        bones_only = scene.btt_bones_only_transfer  # btt.bone_transfer_bones_onlyで個別に実行に変更

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
        success_count = 0  # 移植したオブジェクトの数
        total_bones = 0  # 移植したボーンの数

        to_remove = []  # 成功オブジェクト名を記録

        for b1 in b1_list:
            if not b1.object:
                print(f"スキップ：{b1.name} は .object が未設定です")
                continue

            obj = b1.object
            use_child_bones = b1.use_child_bones

            try:
                new_name, count = run_transfer_logic(a, b, obj, dupe, bones_only, use_child_bones)
                new_names.append(new_name)
                success_count += 1
                total_bones += count

                # ✅ 削除予約だけする
                to_remove.append(b1.name)

            except Exception as e:
                print(f"\n移植失敗：[{b1.name}]")
                print(f"  理由: {e}")

        # ループ後にまとめて削除
        for name in to_remove:
            idx = scene.btt_source_objects.find(name)
            if idx != -1:
                scene.btt_source_objects.remove(idx)

        self.report({'INFO'}, f"{a.name}に{success_count} 個のオブジェクトと {total_bones} 本のボーンを移植しました")
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
    """ 移植リストから選択オブジェクトを除外 """
    bl_idname = "btt.remove_from_transfer_list"
    bl_label = "Remove"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        transfer_list = scene.btt_source_objects
        selected = {obj.name for obj in bpy.context.selected_objects}

        if not selected:
            self.report({'WARNING'}, "選択中のオブジェクトがありません")
            return {'CANCELLED'}

        removed = 0
        # リストを逆順に走査して remove() しても安全
        for i in reversed(range(len(transfer_list))):
            item = transfer_list[i]
            if item.object and item.object.name in selected:
                transfer_list.remove(i)
                removed += 1

        if removed == 0:
            self.report({'WARNING'}, "選択オブジェクトはリストに登録されていません")
        else:
            self.report({'INFO'}, f"{removed} 個のオブジェクトを移植リストから削除しました")
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

        # エラー状態か判定
        arm_b = context.scene.btt_armature_b
        is_linked = obj and obj.parent == arm_b

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

        # 状態アイコン（未リンク）を右寄せ・分離表示
        if not is_linked:
            inner_row.label(icon='ERROR', text="")  # ラベルの後ろ・削除ボタンの前に表示

        # 右列右端：削除ボタン
        rm = inner_row.operator("btt.remove_object_by_name", text="", icon='X', emboss=False)
        rm.object_name = obj_name


#　移植対象オブジェクトを一括選択
class BTT_OT_SelectAllTransferObjects(bpy.types.Operator):
    bl_idname = "btt.select_all_transfer_objects"
    bl_label = "Select All Objects in Transfer List"
    bl_description = "移植リストに登録されているすべてのオブジェクトをビューポート上で選択状態にします"

    def execute(self, context):
        transfer_list = context.scene.btt_source_objects
        if not transfer_list:
            self.report({'WARNING'}, "移植リストが空です")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')

        selected_count = 0
        for item in transfer_list:
            obj = item.object
            if obj and obj.type == 'MESH':
                obj.select_set(True)
                selected_count += 1

        self.report({'INFO'}, f"{selected_count} 個のオブジェクトを選択しました")
        return {'FINISHED'}


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

'''
# 子ボーン移植設定をリスト外のボタン一つで切り替える場合
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
'''

class BTT_OT_BoneTransferBonesOnly(bpy.types.Operator):
    bl_idname = "btt.bone_transfer_bones_only"
    bl_label = "ボーンのみ移植"

    def execute(self, context):
        scene = context.scene
        a = scene.btt_merge_target_armature
        b = scene.btt_armature_b
        transfer_all = scene.btt_transfer_entire_armature

        if not a or not isinstance(a, bpy.types.Object) or a.type != 'ARMATURE':
            self.report({'ERROR'}, "統合先アーマチュア (A) が無効です")
            return {'CANCELLED'}

        if not b or not isinstance(b, bpy.types.Object) or b.type != 'ARMATURE':
            self.report({'ERROR'}, "移植元アーマチュア (B) が無効です")
            return {'CANCELLED'}

        if transfer_all:
            # アーマチュアBの全ボーン名を取得
            bone_names = {bone.name for bone in b.data.bones}
        else:
            # 通常通り、登録されたメッシュからボーン名を抽出
            b1_list = scene.btt_source_objects
            if not b1_list:
                self.report({'ERROR'}, "移植元オブジェクトが未登録です")
                return {'CANCELLED'}
            mesh_objs = [item.object for item in b1_list if item.object]
            bone_names = collect_transfer_bone_names(b, mesh_objs)

        bones = transfer_bones(b, a, bone_names)
        reparent_and_cleanup(a, bones, "Koshi")

        self.report({'INFO'}, f"{len(bones)} 本のボーンを移植しました")
        return {'FINISHED'}

'''
# プロパティ
class BTT_PG_TransferObject(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    use_child_bones: bpy.props.BoolProperty(
        name="子ボーンも含める",
        default=True,
        description="ウェイトのある親ボーンを移植する際に、ウエイトのない子ボーンも一緒に移植するかを切り替えます"
    )
'''


# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        BTT_PT_BoneTransferPanel,
        BTT_OT_BoneTransfer,
        BTT_UL_TransferObjectList,
        BTT_OT_AddToTransferList,
        BTT_OT_RemoveFromTransferList,
        BTT_OT_ClearTransferList,
        # BTT_PG_TransferObject,
        BTT_OT_ToggleObjectSelect,
        BTT_OT_RemoveObjectByName, 
        #　BTT_OT_ToggleAllUseChildBones,　　# ボタン一つで切り替える場合
        BTT_OT_SetAllUseChildBones,  # 個別のボタンで切り替える場合
        BTT_OT_SelectAllTransferObjects,
        BTT_OT_BoneTransferBonesOnly,
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
    bpy.types.Scene.btt_transfer_entire_armature = bpy.props.BoolProperty(
        name="アーマチュア全体を移植", default=False
    )

# プロパティ削除処理
def unregister_properties():
    del bpy.types.Scene.btt_merge_target_armature
    del bpy.types.Scene.btt_armature_b
    del bpy.types.Scene.btt_source_objects
    del bpy.types.Scene.btt_source_objects_index
    del bpy.types.Scene.btt_duplicate_object
    del bpy.types.Scene.btt_bones_only_transfer  # btt.bone_transfer_bones_onlyで個別に実行に変更
