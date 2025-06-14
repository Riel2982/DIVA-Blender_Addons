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

class BoneTransferContextOperator(bpy.types.Operator):
    """ 右クリックメニュー用オペレータ（b1とAを選択して実行） """
    bl_idname = "object.bone_transfer_context"
    bl_label = "DIVA: 移植実行（複製あり）"

    def execute(self, context):
        a = context.scene.merge_target_armature
        b = context.scene.armature_b  # ✅ `b` を `context.scene.armature_b` に定義
        b1 = context.scene.source_object
        dupe = context.scene.duplicate_object

        # ✅ 修正：統合先アーマーチュアが「Armature」オブジェクトであることを確認
        if not a or a.type != 'ARMATURE':
            self.report({'ERROR'}, "統合先アーマーチュアはArmatureオブジェクトである必要があります")
            return {'CANCELLED'}

        if not b or b.type != 'ARMATURE':  # ✅ `b` が適切に選択されているかチェック
            self.report({'ERROR'}, "移植元アーマーチュア（b）を選択してください")
            return {'CANCELLED'}

        if not b1:
            self.report({'ERROR'}, "移植元オブジェクトを選択してください")
            return {'CANCELLED'}

        new_name, count = run_transfer_logic(a, b, b1, dupe)
        self.report({'INFO'}, f"{new_name} に {count} 本のボーンを移植しました")
        return {'FINISHED'}

# ✅ **Blenderアドオンで使うクラスの登録**
classes = [BoneTransferContextOperator]

def menu_draw(self, context):
    self.layout.operator("object.bone_transfer_context")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # ✅ `menu_draw` を `append()` に登録
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_draw)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # ✅ `menu_draw` が登録されている場合のみ解除
    if menu_draw in bpy.types.VIEW3D_MT_object_context_menu.__dict__.values():
        bpy.types.VIEW3D_MT_object_context_menu.remove(menu_draw)

'''
# 不要
if __name__ == "__main__":
    register()
'''