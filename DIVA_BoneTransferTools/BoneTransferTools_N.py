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


