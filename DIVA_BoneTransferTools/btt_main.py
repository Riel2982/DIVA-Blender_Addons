import bpy
# from .btt_panel import BTT_PG_TransferObject  # 循環インポート対策のためこのファイル内に移設
from .btt_types import BTT_PG_TransferObject

# 処理系

def get_relevant_bone_names(objects):
    """ 指定されたオブジェクト（b1）の頂点グループ名を取得
        → 必要なボーンのみを抽出するためのリストを作成
    """
    relevant_groups = set()
    for obj in objects:
        relevant_groups.update(vg.name for vg in obj.vertex_groups)
    return list(relevant_groups)  # 重複を除去したリスト


def transfer_bones(b_armature, a_armature, bone_names):
    """指定されたボーン名に一致するボーンを移植"""
    existing = {b.name for b in a_armature.data.bones}

    # 安全なモード切り替えのための表示/選択状態の確保
    was_hidden = a_armature.hide_get()
    was_hidden_select = a_armature.hide_select

    a_armature.hide_set(False)
    a_armature.hide_select = False

    # 🔧 アクティブ設定前に選択状態にする
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    a_armature.select_set(True)
    bpy.context.view_layer.objects.active = a_armature

    # ✨ poll() を満たした状態で編集モード
    bpy.ops.object.mode_set(mode='EDIT')
    a_edit = a_armature.data.edit_bones
    added = []

    for bone in b_armature.data.bones:
        if bone.name in bone_names and bone.name not in existing:
            new = a_edit.new(bone.name)
            new.head = bone.head_local
            new.tail = bone.tail_local
            new.roll = bone.matrix.to_euler().z

            if bone.parent and bone.parent.name in a_edit:
                new.parent = a_edit[bone.parent.name]
            elif bone.parent and (bone.parent.name + ".001") in a_edit:
                new.parent = a_edit[bone.parent.name + ".001"]

            added.append(new.name)

    bpy.ops.object.mode_set(mode='OBJECT') # ボーンコピー終了

    # 🔙 元の状態に戻す
    if was_hidden:
        a_armature.hide_set(True)
    a_armature.hide_select = was_hidden_select

    return added

def reparent_and_cleanup(a_armature, added_bones, parent_name="Koshi"):
    """ 移植されたボーンの親関係を整理し、不要なKoshi.001を削除 """

    # 表示・選択状態の保存と解除
    was_hidden = a_armature.hide_get()
    was_hidden_select = a_armature.hide_select

    a_armature.hide_set(False)
    a_armature.hide_select = False

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    a_armature.select_set(True)
    bpy.context.view_layer.objects.active = a_armature

    bpy.ops.object.mode_set(mode='EDIT')
    eb = a_armature.data.edit_bones

    p_old = parent_name + ".001"
    if p_old in eb and parent_name in eb:
        for bone in added_bones:
            if bone in eb:
                eb[bone].parent = eb[parent_name] # 親ボーンを正しく設定
        if p_old in eb:
            eb.remove(eb[p_old]) # Koshi.001を削除

    bpy.ops.object.mode_set(mode='OBJECT')

    # 元の状態に戻す
    if was_hidden:
        a_armature.hide_set(True)
    a_armature.hide_select = was_hidden_select

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

def run_transfer_logic(a, b, obj, duplicate=True, bones_only=False, use_child_bones=True):
    """ ボーン移植処理の実行関数
        - objを複製するかどうかのオプション
        - 必要なボーンをB → Aに移植
        - 親関係を整理し、オブジェクトをAアーマーチュアへ移動
    """
    if not obj:
        raise RuntimeError("移植元オブジェクト (`obj`) が None です。適切なオブジェクトを選択してください。")

    # obj が Object でなければエラー
    if not isinstance(obj, bpy.types.Object):
        raise RuntimeError(f"obj is not a valid object for selection. Type: {type(obj)}")

    # 統合先アーマーチュアのコレクションを取得
    target_collection = a.users_collection[0] if a.users_collection else bpy.context.collection

    # ボーンのみを移植する場合の分岐条件
    if bones_only:
        bone_names = collect_transfer_bone_names(b, [obj], include_children=use_child_bones)
        bones = transfer_bones(b, a, bone_names)
        reparent_and_cleanup(a, bones, "Koshi")
        return "（ボーンのみ移植）", len(bones)

    if duplicate:
        # 元オブジェクトの非表示状態を記録し、一時的に表示・選択可能にする
        was_hidden = obj.hide_get()
        was_hidden_select = obj.hide_select

        obj.hide_set(False)
        obj.hide_select = False

        bpy.ops.object.select_all(action='DESELECT')  # 選択解除
        obj.select_set(True)  # objを選択
        bpy.context.view_layer.objects.active = obj  # objをアクティブに設定
        bpy.ops.object.mode_set(mode='OBJECT')  # オブジェクトモードに変更        
        bpy.ops.object.duplicate()  # Blenderのアンドゥシステムに統合された複製処理

        obj_copy = bpy.context.selected_objects[0]  # 複製されたオブジェクトを取得
        target_collection.objects.link(obj_copy)  # 統合先アーマーチュアのコレクションへ移動

        obj_copy.name = obj.name + "_copy"
        
        # 元の非表示状態に戻す（移植後の obj は非表示でOK）
        if was_hidden:
            obj.hide_set(True)
        obj.hide_select = was_hidden_select

        # 元のコレクションから `obj_copy` を削除
        for coll in obj.users_collection:
            if obj_copy.name in coll.objects:
                coll.objects.unlink(obj_copy)  # 旧コレクションから削除

        obj = obj_copy  # 複製したオブジェクトに切り替え

    else:
        # 非表示だった場合でも、表示状態にして処理（元に戻さない）
        obj.hide_set(False)
        obj.hide_select = False

        # 複製しない場合でも統合先のコレクションへ移動
        for coll in obj.users_collection:
            coll.objects.unlink(obj)  # 旧コレクションからオブジェクトを削除
        
        target_collection.objects.link(obj)  # 統合先アーマーチュアのコレクションへ移動

    # 使用ボーン名のみ抽出 → 移植
    bone_names = collect_transfer_bone_names(b, [obj], include_children=use_child_bones)
    bones = transfer_bones(b, a, bone_names)  # obj をリストにして渡す

    reparent_and_cleanup(a, bones, "Koshi")
    move_object_to_armature(obj, a)

    if bones:
        print(f"\n▶ {obj.name} : {len(bones)} bones")
        for bname in sorted(bones):
            print(f"    - {bname}")
    else:
        print(f"\n▶ {obj.name} : 0 bones (no new bones transferred)")

    return obj.name, len(bones)


#　ウエイトありグループ取得関数
def get_weighted_bone_names(obj):
    """オブジェクトの頂点で実際にウエイトが設定されている頂点グループ名を抽出"""
    used_groups = set()
    for v in obj.data.vertices:
        for g in v.groups:
            if g.weight > 0:
                group = obj.vertex_groups[g.group]
                used_groups.add(group.name)
    return used_groups


#　上位ボーン補完
def expand_with_parents(b_armature, bone_names):
    """指定されたボーンの親チェーンを再帰的にたどり、必要な上位ボーンを追加"""
    bones = b_armature.data.bones
    result = set(bone_names)

    supplemented = set()  # ← 補完されたボーン名を記録

    def add_parents(bn):
        bone = bones.get(bn)
        while bone and bone.parent:
            pname = bone.parent.name
            if pname not in result:
                result.add(pname)
                supplemented.add(pname)  # ← ログ対象に追加
                bone = bone.parent
            else:
                break

    for name in list(bone_names):
        add_parents(name)

    # ログ出力（補完された親ボーンがあれば）
    if supplemented:
        print("補完された親ボーン：", ", ".join(sorted(supplemented)))

    return result


# 子ボーン付随拡張（トグル対応）

def expand_with_children(b_armature, bone_names):
    """親ボーンを基準に、すべての子孫を追加する"""
    bones = b_armature.data.bones
    result = set(bone_names)

    def add_children(bone):
        for child in bone.children:
            if child.name not in result:
                result.add(child.name)
                add_children(child)

    for bn in list(result):
        bone = bones.get(bn)
        if bone:
            add_children(bone)

    return result


# 移植対象ボーン名を構成する関数
def collect_transfer_bone_names(b_armature, mesh_objs, include_children=True):
    """すべての条件を統合して移植すべきボーン名セットを構築する"""
    weighted_bones = set()
    for obj in mesh_objs:
        weighted_bones |= get_weighted_bone_names(obj)

    relevant = expand_with_parents(b_armature, weighted_bones)

    if include_children:
        relevant = expand_with_children(b_armature, relevant)

    return relevant


'''
class BTT_PG_TransferObject(bpy.types.PropertyGroup):
    """ ボーン移植リスト用のプロパティグループ """
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    use_child_bones: bpy.props.BoolProperty(
        name="子ボーンも含める",
        default=True,
        description="ウェイトのある親ボーンを移植する際に、ウエイトのない子ボーンも一緒に移植するかを切り替えます"
    )
'''    