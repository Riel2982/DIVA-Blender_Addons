import bpy

# -------------------------------------------------------------
# 頂点削除処理（インデックスベース・非破壊構造）
# -------------------------------------------------------------
def delete_vertices_by_index(obj, index_list):
    """
    指定された頂点インデックス群に基づいて、対象オブジェクトの頂点を削除する。
    完全にインデックス情報のみで判定し、座標（X軸など）や識別名には一切依存しない。
    選択操作は Edit モード内で Blender の標準オペレータを利用して安全に実行される。
    """
    mesh = obj.data

    # Step 1: Editモードで選択解除（安全初期化）
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Step 2: 対象インデックスだけ選択状態にする
    for idx in index_list:
        mesh.vertices[idx].select = True

    # Step 3: 選択頂点を削除
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')


# -------------------------------------------------------------
# 原点越えミラー処理：複製・削除・グループ整備の統合フロー
# -------------------------------------------------------------
def process_origin_overlap(obj, delete_side, rules):
    """
    原点をまたぐ左右ミラー処理の統合制御関数。
    ワークフローは構造ベース・インデックス式で構成され、座標依存や名前依存は排除されている。

    フロー概要：
    ① 元オブジェクトの頂点インデックスを取得（非破壊保証）
    ② 複製＋Mirrorモディファイアを適用（ウェイト含む）
    ③ mirrored_obj から original_indices に基づく頂点削除（構造整合）
    ④ 頂点グループを識別子法則（rules）に基づいて削除・リネーム
    ⑤ 処理完了ログ（Operatorから呼び出される前提なので report は不要）

    ※ グループ処理・Mirror処理は smw_main.py に定義された関数に委譲。
    """
    # Step 1: 元頂点インデックスを構造ベースで記録
    original_indices = [v.index for v in obj.data.vertices]

    # Step 2: 複製オブジェクトを生成し、Mirrorモディファイアを適用
    from .smw_main import duplicate_and_apply_mirror, rename_symmetric_weight_groups
    mirrored_obj = duplicate_and_apply_mirror(obj, delete_side)

    # Step 3: mirrored_obj から original_indices に該当する頂点だけ削除
    delete_vertices_by_index(mirrored_obj, original_indices)

    # Step 4: mirrored_obj の頂点グループにルールベースの削除＋リネーム処理を適用
    rename_symmetric_weight_groups(mirrored_obj, rules, delete_side)

    # Step 5: 処理完了ログ（通知目的）
    print(f"process_origin_overlap(): 完了 - {mirrored_obj.name}")
