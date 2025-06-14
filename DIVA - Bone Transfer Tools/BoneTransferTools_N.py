import bpy

# ---------------------------------------
# 処理系
# ---------------------------------------

def get_relevant_bone_names(obj):
    """ 指定されたオブジェクト（b1）の頂点グループ名を取得
        → 必要なボーンのみを抽出するためのリストを作成
    """
    return [vg.name for vg in obj.vertex_groups]

def transfer_bones(b_armature, a_armature, target_obj):
    """ Bアーマーチュアのボーンを Aアーマーチュアへ移植
        - 必要なボーンのみ取得（b1の頂点グループに含まれるもの）
        - 既にAに存在するボーンはスキップ
        - 親ボーンの情報をできる限り保持
    """
    relevant_bones = get_relevant_bone_names(target_obj)
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
            new.roll = bone.matrix.to_euler().z  # ✅ 修正: 回転情報の取得

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
                eb[bone].parent = eb[parent_name]  # ✅ 親ボーンを正しく設定
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

def run_transfer_logic(a, b, b1, duplicate=True):
    """ ボーン移植処理の実行関数（Nパネル・右クリック共通処理）
        - b1を複製するかどうかのオプション
        - 必要なボーンをB → Aに移植
        - 親関係を整理し、オブジェクトをAアーマーチュアへ移動
    """

    if not b1:
        raise RuntimeError("移植元オブジェクト (`b1`) が None です。適切なオブジェクトを選択してください。")

    # ✅ 統合先アーマーチュアのコレクションを取得
    target_collection = a.users_collection[0] if a.users_collection else bpy.context.collection

    if duplicate:
        bpy.ops.object.mode_set(mode='OBJECT')  # ✅ **オブジェクトモードに変更**
        bpy.ops.object.select_all(action='DESELECT')  # ✅ **選択解除**
        b1.select_set(True)  # ✅ **コピー対象を選択**
        bpy.ops.object.duplicate()  # ✅ **Blenderのアンドゥシステムに統合された複製処理**
        b1_copy = bpy.context.selected_objects[0]  # ✅ **複製されたオブジェクトを取得**
        target_collection.objects.link(b1_copy)  # ✅ **統合先アーマーチュアのコレクションへ移動**

        b1_copy.name = b1.name + "_copy"
        
        # ✅ **修正: 元のコレクションから `b1_copy` を削除**
        for coll in b1.users_collection:
            if b1_copy.name in coll.objects:  # 🔹 **オブジェクトではなく名前（string）で比較**
                coll.objects.unlink(b1_copy)  # 🔹 **旧コレクションから `b1_copy` を削除**

        b1 = b1_copy  # ✅ **複製したオブジェクトに切り替え**

    else:
        # ✅ 複製しない場合でも統合先のコレクションへ移動
        for coll in b1.users_collection:
            coll.objects.unlink(b1)  # 🔹 旧コレクションからオブジェクトを削除
        
        target_collection.objects.link(b1)  # ✅ 統合先アーマーチュアのコレクションへ移動

    bones = transfer_bones(b, a, b1)
    reparent_and_cleanup(a, bones, "Koshi")
    move_object_to_armature(b1, a)
    return b1.name, len(bones)

# ---------------------------------------
# UI & メニュー
# ---------------------------------------

class BoneTransferPanel(bpy.types.Panel):
    """ DIVAタブのNパネルUI（スポイト選択 + オプション付き） """
    bl_label = "Bone Transfer Tools"
    bl_idname = "VIEW3D_PT_bone_transfer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DIVA'

    def draw(self, context):
        layout = self.layout

        # 🔹 統合先アーマーチュア（A）をチェック
        if hasattr(context.scene, "merge_target_armature"):
            layout.label(text="統合先アーマーチュア（A）:")
            layout.prop(context.scene, "merge_target_armature")
        else:
            layout.label(text="⚠️ 統合先アーマーチュアが未登録です")

        # 🔹 移植元アーマーチュア（B）
        if hasattr(context.scene, "armature_b"):
            layout.label(text="移植元アーマーチュア（B）:")
            layout.prop(context.scene, "armature_b")
        else:
            layout.label(text="⚠ 移植元アーマーチュアが未登録です")

        # 🔹 移植元オブジェクト（b1）をチェック
        if hasattr(context.scene, "source_object"):
            layout.label(text="移植元オブジェクト（b1）:")
            layout.prop(context.scene, "source_object")
        else:
            layout.label(text="⚠️ 移植元オブジェクトが未登録です")

        # 🔹 複製オプションをチェック
        if hasattr(context.scene, "duplicate_object"):
            layout.prop(context.scene, "duplicate_object")
        else:
            layout.label(text="⚠️ 複製オプションが未登録です")

        # 🔹 実行ボタン
        layout.operator("object.bone_transfer", icon="ARMATURE_DATA")

class BoneTransferOperator(bpy.types.Operator):
    """ Nパネル用：移植実行オペレータ """
    bl_idname = "object.bone_transfer"
    bl_label = "ボーンとオブジェクトを移植"
    bl_description = "ボーンの移植と対象オブジェクトのペアレントを行います"

    def execute(self, context):
        a = context.scene.merge_target_armature
        b = context.scene.armature_b  # ✅ 修正：移植元のアーマーチュア（b_armature）を取得
        b1 = context.scene.source_object
        dupe = context.scene.duplicate_object

        # ✅ 修正：必要なオブジェクトが適切に選択されているか確認
        if not a or a.type != 'ARMATURE':
            self.report({'ERROR'}, "統合先アーマーチュアはArmatureオブジェクトである必要があります")
            return {'CANCELLED'}
        if not b or b.type != 'ARMATURE':
            self.report({'ERROR'}, "移植元アーマーチュア（b）を選択してください")
            return {'CANCELLED'}
        if not b1:
            self.report({'ERROR'}, "移植元オブジェクト（b1）を選択してください")
            return {'CANCELLED'}

        new_name, count = run_transfer_logic(a, b, b1, dupe)
        self.report({'INFO'}, f"{new_name} に {count} 本のボーンを移植")
        return {'FINISHED'}

# ✅ **Blenderアドオンで使うクラスの登録**
classes = [
    BoneTransferPanel,
    BoneTransferOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.append(
        lambda self, ctx: self.layout.operator("object.bone_transfer_context")
    )

    if not hasattr(bpy.types.Scene, "merge_target_armature"):
        bpy.types.Scene.merge_target_armature = bpy.props.PointerProperty(
            name="統合先アーマーチュア", type=bpy.types.Object, poll=lambda self, obj: obj.type == 'ARMATURE'
        )

    if not hasattr(bpy.types.Scene, "source_object"):
        bpy.types.Scene.source_object = bpy.props.PointerProperty(
            name="移植オブジェクト",
            type=bpy.types.Object,
            poll=lambda self, obj: obj.type == 'MESH' 
        )

    if not hasattr(bpy.types.Scene, "duplicate_object"):
        bpy.types.Scene.duplicate_object = bpy.props.BoolProperty(
            name="複製して移植", default=True
        )

    if not hasattr(bpy.types.Scene, "armature_b"):
        bpy.types.Scene.armature_b = bpy.props.PointerProperty(
            name="移植元アーマーチュア",
            type=bpy.types.Object,
            poll=lambda self, obj: obj.type == 'ARMATURE'
        )

def unregister():
    for cls in reversed(classes):  # ✅ **逆順で登録解除**
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.remove(
        lambda self, ctx: self.layout.operator("object.bone_transfer_context")
    )

    if hasattr(bpy.types.Scene, "merge_target_armature"):
        del bpy.types.Scene.merge_target_armature
    if hasattr(bpy.types.Scene, "source_object"):
        del bpy.types.Scene.source_object
    if hasattr(bpy.types.Scene, "duplicate_object"):
        del bpy.types.Scene.duplicate_object
    if hasattr(bpy.types.Scene, "armature_b"):
        del bpy.types.Scene.armature_b

'''
# __init__.py以外には不要
if __name__ == "__main__":
    register()
'''