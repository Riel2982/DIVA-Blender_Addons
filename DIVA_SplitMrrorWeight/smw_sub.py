import bpy
import bmesh
from .smw_main import rename_symmetric_weight_groups

def process_origin_overlap(obj, delete_side, rules):
    """原点越えを含む片側メッシュの左右反転処理"""
    # ① 複製（opsベースで完全コピー）
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    duplicate = bpy.context.selected_objects[0]

    # ② 名前：残す側（オリジナル側と逆）を付与
    mirror_side = 'R' if delete_side == 'RIGHT' else 'L'
    duplicate.name = f"{obj.name}_{mirror_side}"

    # ③ Mirror_L / R を先に作成し、オリジナル側にウェイト割り当て
    group_L = duplicate.vertex_groups.new(name="Mirror_L")
    group_R = duplicate.vertex_groups.new(name="Mirror_R")
    group_target = group_R if delete_side == 'RIGHT' else group_L

    for v in duplicate.data.vertices:
        group_target.add([v.index], 1.0, 'REPLACE')

    # ④ ミラーモディファイア追加（ウェイトミラーON）
    bpy.context.view_layer.objects.active = duplicate
    bpy.ops.object.modifier_add(type='MIRROR')
    mirror = duplicate.modifiers[-1]
    mirror.use_axis[0] = True
    mirror.use_mirror_vertex_groups = True
    mirror.use_bisect_axis[0] = False
    mirror.use_clip = False

    # ⑤ モディファイアを適用（Mirror_L / R も反映される）
    bpy.ops.object.modifier_apply(modifier=mirror.name)

    # ⑥ 選択状態をクリア → 削除対象グループだけ選択
    bpy.ops.object.mode_set(mode='OBJECT')

    for v in duplicate.data.vertices:
        v.select = False  # 初期化

    for v in duplicate.data.vertices:
        group_indices = [g.group for g in v.groups]
        if group_target.index in group_indices:
            v.select = True
            print(f"[DIVA] 選択: v{v.index} in group {group_target.name}, X={v.co.x:.4f}")
            world_x = (duplicate.matrix_world @ v.co).x
            print(f"[DIVA] 選択: v{v.index}, group={group_target.name}, X_world={world_x:.4f}")

    """ # v.select版
    # ⑦ 選択された頂点を削除（オリジナル側）
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    """

    # ⑦ 対象グループに属する頂点を bmesh 経由で削除
    # delete_vertices_in_group(duplicate, group_target.index)

    # ⑦ Mirror_L / Mirror_R をグループ名から再取得して削除
    mirror_group_name = "Mirror_R" if delete_side == 'RIGHT' else "Mirror_L"
    group = duplicate.vertex_groups.get(mirror_group_name)

    if group:
        delete_vertices_in_group(duplicate, group.index)
    else:
        print(f"[DIVA] 削除対象グループが見つかりません: {mirror_group_name}")

    """
    # ⑧ Mirror_L / Mirror_R は後始末で削除
    for name in ("Mirror_L", "Mirror_R"):
        vg = duplicate.vertex_groups.get(name)
        if vg:
            duplicate.vertex_groups.remove(vg)
    """
            
    # ⑨ ミラー側ウェイトの削除＋リネーム（既存関数で）
    rename_symmetric_weight_groups(duplicate, rules, delete_side)

    print(f"[DIVA] 原点越えミラー処理完了: {duplicate.name}")


# 補助関数

def assign_all_vertices_to_group(obj, group):
    indices = [v.index for v in obj.data.vertices]
    group.add(indices, 1.0, 'REPLACE')


def select_vertices_in_group(obj, group_name):
    vg = obj.vertex_groups.get(group_name)
    if not vg:
        return

    bpy.ops.object.mode_set(mode='OBJECT')
    for v in obj.data.vertices:
        v.select = any(g.group == vg.index for g in v.groups)

""" # v.select版
def deselect_vertices_in_group(obj, group_name):
    vg = obj.vertex_groups.get(group_name)
    if not vg:
        return

    bpy.ops.object.mode_set(mode='OBJECT')
    for v in obj.data.vertices:
        if any(g.group == vg.index for g in v.groups):
            v.select = False
"""

#　Mirror_R / Mirror_L に基づくメッシュ削除処理
def delete_vertices_in_group(obj, group_index):
    """指定した頂点グループに属する頂点のみ削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    deform_layer = bm.verts.layers.deform.verify()

    print(f"[DIVA] 指定削除グループ index = {group_index}")
    for vg in obj.vertex_groups:
        print(f"[DIVA] グループ一覧: {vg.name}, index = {vg.index}")

    to_delete = []

    for v in bm.verts:
        dvert = v[deform_layer]
        if group_index in dvert:
            to_delete.append(v)

    for v in to_delete:
        bm.verts.remove(v)

    bm.to_mesh(mesh)
    bm.free()

'''
# bmesh版
def delete_vertices_in_group(obj, group_index):
    """指定した頂点グループに属する頂点のみ削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    deform_layer = bm.verts.layers.deform.verify()

    # デバック用
    print(f"[DIVA] 指定削除グループ index = {group_index}")
    for vg in obj.vertex_groups:
        print(f"[DIVA] グループ一覧: {vg.name}, index = {vg.index}")
    for v in bm.verts:
        weights = v[deform_layer]
        if weights:
            print(f"[DIVA] v{v.index} のウェイト情報: {weights}")

    to_delete = []
    for v in to_delete:
        bm.verts.remove(v)

    bm.to_mesh(mesh)
    bm.free()

# bmesh版
def delete_original_side_verts(obj, delete_side):
    """オリジナル側のメッシュだけを削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    for v in list(bm.verts):
        co_world = obj.matrix_world @ v.co
        if (delete_side == 'RIGHT' and co_world.x > 0) or \
           (delete_side == 'LEFT' and co_world.x < 0):
            bm.verts.remove(v)

    bm.to_mesh(mesh)
    bm.free()
'''
    
#　Mirror_R / Mirror_L に基づくメッシュ削除処理
def delete_group_side_mesh(obj, group_name):
    """指定された頂点グループに所属する頂点を削除"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Deformレイヤー取得（ウェイト情報）
    deform_layer = bm.verts.layers.deform.verify()

    # 対象グループのインデックスを取得
    group = obj.vertex_groups.get(group_name)
    if not group:
        print(f"[DIVA] 指定削除グループが見つかりません: {group_name}")
        bm.free()
        return

    group_index = group.index
    print(f"[DIVA] 削除対象グループ: {group_name}, index = {group_index}")

    delete_verts = []

    for v in bm.verts:
        dvert = v[deform_layer]
        if group_index in dvert:
            delete_verts.append(v)

    for v in delete_verts:
        bm.verts.remove(v)

    bm.to_mesh(mesh)
    bm.free()