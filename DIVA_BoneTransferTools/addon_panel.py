import bpy

# UI & メニュー
class BoneTransferPanel(bpy.types.Panel):
    """ DIVAタブのNパネルUI（スポイト選択 + オプション付き） """
    bl_label = "Bone Transfer Tools"
    bl_idname = "VIEW3D_PT_bone_transfer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DIVA'

    def draw(self, context):
        layout = self.layout
        scene = bpy.data.scenes[0]

        # 統合先アーマーチュア（A）
        layout.label(text="統合先アーマーチュア（A）:")
        layout.prop(scene, "merge_target_armature")

        # 移植元アーマーチュア（B）
        layout.label(text="移植元アーマーチュア（B）:")
        layout.prop(scene, "armature_b")

        # 移植元メッシュのリスト管理（選択状態と同期を削除）
        layout.label(text="移植元オブジェクト（b1）:")
        row = layout.row()
        row.operator("object.add_to_transfer_list", text="Add")
        row.operator("object.remove_from_transfer_list", text="Remove")
        row.operator("object.clear_transfer_list", text="Clear")

        layout.template_list(
            "TransferObjectUIList", "",
            scene, "source_objects",
            scene, "source_objects_index"
        )

        row = layout.row()
        row.prop(scene, "duplicate_object", text="")  # チェックボックス
        row.label(text="複製して移植")

        row = layout.row()
        row.prop(scene, "bones_only_transfer", text="")  # チェックボックス
        row.label(text="ボーンのみ移植")

        # 実行ボタン
        layout.operator("object.bone_transfer", icon="ARMATURE_DATA")


class BoneTransferOperator(bpy.types.Operator):
    """ Nパネル用：移植実行オペレータ """
    bl_idname = "object.bone_transfer"
    bl_label = "ボーンとオブジェクトを移植"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        a = scene.merge_target_armature
        b = scene.armature_b
        b1_list = scene.source_objects
        dupe = scene.duplicate_object
        bones_only = scene.bones_only_transfer

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


class AddToTransferListOperator(bpy.types.Operator):
    """ 選択中のメッシュオブジェクトを処理リストに追加 """
    bl_idname = "object.add_to_transfer_list"
    bl_label = "Add"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        transfer_list = scene.source_objects

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


class RemoveFromTransferListOperator(bpy.types.Operator):
    """ 移植リストから削除 """
    bl_idname = "object.remove_from_transfer_list"
    bl_label = "Remove"

    def execute(self, context):
        scene = bpy.data.scenes[0]
        transfer_list = scene.source_objects

        # オブジェクト選択処理を削除
        if transfer_list:
            transfer_list.remove(scene.source_objects_index)

        self.report({'INFO'}, "リストから削除しました")
        return {'FINISHED'}


class ClearTransferListOperator(bpy.types.Operator):
    """ 移植リストをクリア """
    bl_idname = "object.clear_transfer_list"
    bl_label = "Clear"

    def execute(self, context):
        bpy.data.scenes[0].source_objects.clear()
        self.report({'INFO'}, "移植リストをリセットしました")
        return {'FINISHED'}


class TransferObjectPropertyGroup(bpy.types.PropertyGroup):
    """ ボーン移植リスト用のプロパティグループ """
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)


class TransferObjectUIList(bpy.types.UIList):
    """ 移植メッシュリストの表示 """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        obj_name = item.object.name if item.object else "未設定"
        row.label(text=f"{index + 1}: {obj_name}", icon='OBJECT_DATA')

# Blenderアドオンで使うクラスの登録
classes = [
    BoneTransferPanel,
    BoneTransferOperator,
    TransferObjectUIList,
    AddToTransferListOperator,
    RemoveFromTransferListOperator,
    ClearTransferListOperator,
]

def register():
    bpy.utils.register_class(BoneTransferPanel)
    bpy.utils.register_class(BoneTransferOperator)
    bpy.utils.register_class(AddToTransferListOperator)
    bpy.utils.register_class(RemoveFromTransferListOperator)
    bpy.utils.register_class(ClearTransferListOperator)
    bpy.utils.register_class(TransferObjectPropertyGroup)
    bpy.utils.register_class(TransferObjectUIList)

    bpy.types.Scene.merge_target_armature = bpy.props.PointerProperty(
        name="統合先アーマーチュア", type=bpy.types.Object, poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.Scene.armature_b = bpy.props.PointerProperty(
        name="移植元アーマーチュア", type=bpy.types.Object, poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.Scene.source_objects = bpy.props.CollectionProperty(
        name="移植オブジェクトリスト", type=TransferObjectPropertyGroup
    )
    bpy.types.Scene.source_objects_index = bpy.props.IntProperty(
        name="選択インデックス", default=0
    )
    bpy.types.Scene.duplicate_object = bpy.props.BoolProperty(
        name="複製して移植", default=True
    )
    bpy.types.Scene.bones_only_transfer = bpy.props.BoolProperty(
        name="ボーンのみ移植", default=False
    )

def unregister():
    del bpy.types.Scene.merge_target_armature
    del bpy.types.Scene.armature_b
    del bpy.types.Scene.source_objects
    del bpy.types.Scene.source_objects_index
    del bpy.types.Scene.duplicate_object
    del bpy.types.Scene.bones_only_transfer

    bpy.utils.unregister_class(BoneTransferPanel)
    bpy.utils.unregister_class(BoneTransferOperator)
    bpy.utils.unregister_class(AddToTransferListOperator)
    bpy.utils.unregister_class(RemoveFromTransferListOperator)
    bpy.utils.unregister_class(ClearTransferListOperator)
    bpy.utils.unregister_class(TransferObjectPropertyGroup)
    bpy.utils.unregister_class(TransferObjectUIList)

# スクリプト直接実行時の登録処理
if __name__ == "__main__":
    register()