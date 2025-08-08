# mwr_debug.py

# デバッグモード管理（initで切り替え）
DEBUG_MODE = False  # ここで一括制御




import bpy
import mathutils

def audit_vertex_overlap(obj, threshold=0.0001):
    """
    Mirror後に統合されてしまった頂点がないか、位置ベースで確認する関数。
    - threshold: 同一とみなす距離誤差
    """
    mesh = obj.data
    checked = set()
    close_pairs = []

    for i, v1 in enumerate(mesh.vertices):
        for j in range(i + 1, len(mesh.vertices)):
            if j in checked:
                continue
            v2 = mesh.vertices[j]
            dist = (v1.co - v2.co).length
            if dist < threshold:
                close_pairs.append((i, j, dist))
        checked.add(i)

    print(f"[VertexOverlapAudit] 距離 {threshold} 未満の近接頂点ペア数: {len(close_pairs)}")
    for i, j, dist in close_pairs[:20]:  # 最初の20件だけ表示
        print(f"  ⚠️ Index {i} <-> {j} | Distance: {dist:.6f}")
    
    return close_pairs

# オリジナル側の頂点情報を記録
def get_original_coords(obj):
    return {v.index: v.co.copy() for v in obj.data.vertices}

# ミラー後の頂点情報との比較ログ
def compare_vertex_indices_and_positions(original_data, mirrored_obj, threshold=0.00001):
    print(f"[VertexCompare] Mirror後頂点数: {len(mirrored_obj.data.vertices)}")
    mismatch_count = 0
    for orig_index, orig_co in original_data:
        if orig_index >= len(mirrored_obj.data.vertices):
            print(f"  ❌ Index {orig_index} missing in mirrored object")
            mismatch_count += 1
            continue
        new_co = mirrored_obj.data.vertices[orig_index].co
        dist = (new_co - orig_co).length
        if dist > threshold:
            print(f"  ⚠️ Index {orig_index} position changed: Δ={dist:.6f}")
            mismatch_count += 1
    print(f"[VertexCompare] 差異ありインデックス数: {mismatch_count}")

# 頂点削除前の頂点ログ
def log_vertex_data(obj):
    return [(v.index, v.co.copy()) for v in obj.data.vertices]

# 頂点削除後の差分ログ
def log_deleted_vertices(original_data, obj_after_delete, threshold=0.00001):
    remaining_positions = [v.co for v in obj_after_delete.data.vertices]
    deleted = []
    for orig_index, orig_co in original_data:
        if not any((orig_co - p).length < threshold for p in remaining_positions):
            deleted.append((orig_index, orig_co))
    print(f"[VertexDelete] 削除された頂点数: {len(deleted)}")
    for idx, co in deleted:
        print(f"  🗑️ Index {idx} deleted | Position: {co}")
    return deleted

# 削除ログ+削除理由の分類ログ
def classify_deleted_vertices(deleted_data, mirrored_obj, mirror_index_map=None, merged_indices=None, threshold=0.0005):

    if merged_indices is None:
        merged_indices = audit_vertex_overlap(mirrored_obj)

    summary = {
        "LEFT": [],
        "RIGHT": [],
        "CENTER": [],
        "UNKNOWN": [],
        "SKIPPED": []
    }

    for idx, pos in deleted_data:
        # Mirror照合除外
        if mirror_index_map and idx in mirror_index_map:
            mirror_idx = mirror_index_map[idx]
            mirror_pos = mirrored_obj.data.vertices[mirror_idx].co
            if (pos - mirror_pos).length > 0.0003:
                print(f"🚫 Skipped Index {idx}: Mirror mismatch Δ={ (pos - mirror_pos).length:.6f}")
                summary["SKIPPED"].append((idx, pos))
                continue

        # Auto-merge除外
        if idx in merged_indices:
            print(f"🛑 Index {idx} skipped: Auto-merge suspected")
            summary["SKIPPED"].append((idx, pos))
            continue

        # 分類処理
        if pos.x < -threshold:
            summary["LEFT"].append((idx, pos))
        elif pos.x > threshold:
            summary["RIGHT"].append((idx, pos))
        elif abs(pos.x) <= threshold:
            summary["CENTER"].append((idx, pos))
        else:
            summary["UNKNOWN"].append((idx, pos))
