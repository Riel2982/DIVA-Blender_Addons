import bpy


# 処理系

def get_relevant_bone_names(objects):
    """ 指定されたオブジェクト（b1）の頂点グループ名を取得
        → 必要なボーンのみを抽出するためのリストを作成
    """
    relevant_groups = set()
    for obj in objects:
        relevant_groups.update(vg.name for vg in obj.vertex_groups)
    return list(relevant_groups)  # 重複を除去したリスト

def transfer_bones(b_armature, a_armature, target_objs):
    """ Bアーマーチュアのボーンを Aアーマーチュアへ移植
        - 必要なボーンのみ取得（b1の頂点グループに含まれるもの）
        - 既にAに存在するボーンはスキップ
        - 親ボーンの情報をできる限り保持
    """
    relevant_bones = get_relevant_bone_names(target_objs)
    existing_bones = {b.name for b in a_armature.data.bones}

    bpy.context.view_layer.objects.active = a_armature
    bpy.ops.object.mode_set(mode='EDIT')  # 編集モードへ
    a_edit = a_armature.data.edit_bones

    added = []
    for bone in b_armature.data.bones:
        if bone.name in relevant_bones and bone.name not in existing_bones:
            # 新規ボーンを作成し、Bから形状をコピー
            new = a_edit.new(bone.name)
            new.head = bone.head_local
            new.tail = bone.tail_local
            new.roll = bone.matrix.to_euler().z  # 回転情報の取得

            # 可能ならば親ボーンも設定
            if bone.parent and bone.parent.name in existing_bones:
                new.parent = a_edit[bone.parent.name]
            elif bone.parent and (bone.parent.name + ".001") in a_edit:
                new.parent = a_edit[bone.parent.name + ".001"]

            added.append(new.name)

    bpy.ops.object.mode_set(mode='OBJECT')  # オブジェクトモードへ戻る
    return added

def reparent_and_cleanup(a_armature, added_bones, parent_name="Koshi"):
    """ 移植されたボーンの親関係を整理し、不要なKoshi.001を削除
        - Koshi.001 → Koshi に再接続
        - 不要なKoshi.001があれば削除
    """
    bpy.context.view_layer.objects.active = a_armature
    bpy.ops.object.mode_set(mode='EDIT')
    eb = a_armature.data.edit_bones

    p_old = parent_name + ".001"
    if p_old in eb and parent_name in eb:
        for bone in added_bones:
            if bone in eb:
                eb[bone].parent = eb[parent_name]  # 親ボーンを正しく設定
        if p_old in eb:
            eb.remove(eb[p_old])  # Koshi.001を削除
    bpy.ops.object.mode_set(mode='OBJECT')

def move_object_to_armature(obj, a_armature):
    """ b1オブジェクトのモディファイアをAアーマーチュアに切り替え
        - Armatureモディファイアの修正（なければ追加）
        - オブジェクトペアレントの更新（Keep Transform）
    """
    for mod in obj.modifiers:
        if mod.type == 'ARMATURE':
            mod.object = a_armature
            break
    else:
        mod = obj.modifiers.new(name="Armature", type='ARMATURE')
        mod.object = a_armature

    # 親関係の更新（トランスフォーム維持）
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    a_armature.select_set(True)
    bpy.context.view_layer.objects.active = a_armature
    bpy.ops.object.parent_set(type='ARMATURE_NAME', keep_transform=True)

def run_transfer_logic(a, b, b1, duplicate=True, bones_only=False):
    """ ボーン移植処理の実行関数
        - b1を複製するかどうかのオプション
        - 必要なボーンをB → Aに移植
        - 親関係を整理し、オブジェクトをAアーマーチュアへ移動
    """

    if not b1:
        raise RuntimeError("移植元オブジェクト (`b1`) が None です。適切なオブジェクトを選択してください。")

    # ✅ `b1` が `TransferObjectPropertyGroup` の場合、`object` を取得
    if isinstance(b1, TransferObjectPropertyGroup):
        if hasattr(b1, "object") and isinstance(b1.object, bpy.types.Object):
            b1 = b1.object  # `bpy.types.Object` に変換
        else:
            raise RuntimeError("b1.object が None または適切な 'Object' 型ではありません。")

    # ✅ `b1` が `bpy.types.Object` の場合のみ選択可能
    if isinstance(b1, bpy.types.Object):
        bpy.ops.object.select_all(action='DESELECT')
        b1.select_set(True)
    else:
        raise RuntimeError(f"b1 is not a valid object for selection. Type: {type(b1)}")


    # 統合先アーマーチュアのコレクションを取得
    target_collection = a.users_collection[0] if a.users_collection else bpy.context.collection

    # ボーンのみを移植する場合の分岐条件
    if bones_only:
        bones = transfer_bones(b, a, b1)
        reparent_and_cleanup(a, bones, "Koshi")
        return "（ボーンのみ移植）", len(bones)

    if duplicate:
        bpy.ops.object.mode_set(mode='OBJECT')  # オブジェクトモードに変更
        bpy.ops.object.select_all(action='DESELECT')  # 選択解除
        b1.select_set(True)
        bpy.ops.object.duplicate()  # Blenderのアンドゥシステムに統合された複製処理
        b1_copy = bpy.context.selected_objects[0]  # 複製されたオブジェクトを取得
        target_collection.objects.link(b1_copy)  # 統合先アーマーチュアのコレクションへ移動

        b1_copy.name = b1.name + "_copy"
        
        # 元のコレクションから `b1_copy` を削除
        for coll in b1.users_collection:
            if b1_copy.name in coll.objects:
                coll.objects.unlink(b1_copy)  # 旧コレクションから削除

        b1 = b1_copy  # 複製したオブジェクトに切り替え

    else:
        # 複製しない場合でも統合先のコレクションへ移動
        for coll in b1.users_collection:
            coll.objects.unlink(b1)  # 旧コレクションからオブジェクトを削除
        
        target_collection.objects.link(b1)  # 統合先アーマーチュアのコレクションへ移動

    bones = transfer_bones(b, a, [b1])  # b1 をリストにして渡す
    reparent_and_cleanup(a, bones, "Koshi")
    move_object_to_armature(b1, a)
    return b1.name, len(bones)


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

        # 複製オプション
        layout.prop(scene, "duplicate_object")

        # ボーンのみ複製オプション
        layout.prop(scene, "bones_only_transfer")

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

        # ✅ `a` と `b` が `ARMATURE` 型のオブジェクトであることを保証
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

        # ✅ 現在選択されているメッシュオブジェクトのみを取得
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        # ✅ 選択オブジェクトがない場合はエラーを返す
        if not selected_objects:
            self.report({'ERROR'}, "メッシュオブジェクトが選択されていません")
            return {'CANCELLED'}

        # ✅ リストの上限を設定（大量登録によるクラッシュを防ぐ）
        if len(transfer_list) + len(selected_objects) > 100:
            self.report({'ERROR'}, "移植リストが上限に達しました（最大100個）")
            return {'CANCELLED'}

        # ✅ 重複登録を防ぐ
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
    TransferObjectUIList,  # ✅ `UIList` を追加
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