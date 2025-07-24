import bpy

# 頂点インデックスに基づいて削除（X軸超え対応向け）
def delete_vertices_by_index(obj, index_list):
    mesh = obj.data
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for idx in index_list:
        mesh.vertices[idx].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')

# 原点を超えているメッシュを処理（allow_origin_overlap = True 時に呼び出される）
def process_origin_overlap(obj, delete_side, rules):
    # 1. オリジナル頂点インデックスを記録（非破壊保証）
    original_indices = [v.index for v in obj.data.vertices]

    # 2. Mirror処理実行（mirror modifier を適用し、複製オブジェクトを取得）
    from .smw_main import duplicate_and_apply_mirror, rename_symmetric_weight_groups, delete_x_side_mesh
    mirrored_obj = duplicate_and_apply_mirror(obj, delete_side)

    # 3. オリジナル頂点を削除（記録済インデックスを基に）
    delete_vertices_by_index(mirrored_obj, original_indices)

    # 4. 対象メッシュ側にウェイトのリネーム処理を適用
    rename_symmetric_weight_groups(mirrored_obj, rules, delete_side)

    # 5. X軸に残る反対側頂点を除去（安全処理）
    delete_positive_x = (delete_side == 'RIGHT')
    delete_x_side_mesh(mirrored_obj, delete_positive_x)

    # 6. 終了ログ（元の処理が Operator から呼ばれているため、report は不要）
    print(f"process_origin_overlap(): 完了 - {mirrored_obj.name}")
