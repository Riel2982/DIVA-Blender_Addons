# brt_invert.py（旧# rename_symmetry.py）

import bpy
import re
from typing import Optional
import mathutils
import math

# ミラー処理の関数化
def apply_mirror_transform(target, mirror_mode):
    if mirror_mode == 'SYMMETRY':    # ロール反転のみ
        target.head[0] *= -1
        target.tail[0] *= -1

        target.roll *= -1

    elif mirror_mode == 'DIVA':  # ロール反転後+180、のち正規化
        # X軸方向を反転してミラー
        target.head[0] *= -1
        target.tail[0] *= -1

        # ロールを度数に変換 → 反転 → +180 → Blender仕様に正規化
        roll_deg = math.degrees(target.roll)  # ラジアン → 度
        roll_deg *= -1      # ロールも反転（Z軸を基準に反転するようなイメージ）
        roll_deg += 180     # +180で逆転させる

        # Blender [-180, 180) の範囲に正規化
        if roll_deg > 180:
            roll_deg -= 360
        elif roll_deg < -180:
            roll_deg += 360

        # 最終値をラジアンに戻して適用
        target.roll = math.radians(roll_deg)

    elif mirror_mode == 'NONE': # ロール補正をしない
        target.head[0] *= -1
        target.tail[0] *= -1

    elif mirror_mode == 'TEST':  # 反転しないで+180
        # target.head[0] *= -1
        # target.tail[0] *= -1

        roll_deg = math.degrees(target.roll)
        roll_deg += 180
        if roll_deg > 180:
            roll_deg -= 360
        elif roll_deg < -180:
            roll_deg += 360
        target.roll = math.radians(roll_deg)

# グローバル軸でミラー
def mirror_bone_global(target, mirror_mode):
    arm = bpy.context.object

    # グローバル座標取得
    head_global = arm.matrix_world @ target.head
    tail_global = arm.matrix_world @ target.tail

    # X軸反転（グローバル）
    head_global.x *= -1
    tail_global.x *= -1

    # ローカル座標に戻す
    target.head = arm.matrix_world.inverted() @ head_global
    target.tail = arm.matrix_world.inverted() @ tail_global

    # ロール処理
    if mirror_mode == 'SYMMETRY':
        target.roll *= -1

    elif mirror_mode == 'DIVA':
        roll_deg = math.degrees(target.roll)
        roll_deg *= -1
        roll_deg += 180

        if roll_deg > 180:
            roll_deg -= 360
        elif roll_deg < -180:
            roll_deg += 360

        target.roll = math.radians(roll_deg)

# 選択中のボーンに対して、識別パターンに基づいて名前を反転リネーム
def apply_mirrored_rename(context, pattern_name: str, *, duplicate=False, mirror=False, assign_identifier=False, suffix_enum="wj", rule_enum="000", rule_index=0):
    from .brt_sub import detect_common_prefix

    obj = context.object
    if not obj or obj.type != 'ARMATURE':
        return 0

    initial_mode = context.mode
    if initial_mode not in {'POSE', 'EDIT_ARMATURE'}:
        return 0

    # 対象ボーン収集（Pose or Edit）
    if initial_mode == 'POSE':
        bones = [b for b in obj.pose.bones if b.bone.select]
    elif initial_mode == 'EDIT_ARMATURE':
        bones = [b for b in obj.data.edit_bones if b.select]

    # デバック用
    print(f"▶ apply_mirrored_rename: mode = {initial_mode}")
    print(f"▶ 選択ボーン数: {len(bones)}")

    if not bones:
        return 0

    # 選ばれた識別子セットとルールに基づく辞書を取得
    rule_index = rule_index if assign_identifier else None
    mirror_map = get_pattern_map_from_prefs(context, pattern_name, rule_index)
    if not mirror_map:
        return 0

    # プレフィックスを抽出（必要なら）
    prefix = detect_common_prefix(bones, suffix_enum, rule_enum) if assign_identifier else None

    # デバック用
    print(f"▶ mirror_map: {mirror_map}")
    print(f"▶ prefix: {prefix}")

    renamed = 0
    bpy.ops.object.mode_set(mode='EDIT')  # ミラーや複製はEDITで実行

    bone_map = {}  # オリジナル名 → 複製ボーン を記録する辞書

    # 識別子リストを抽出（flip対象として登録されているすべて）
    ident_list = list(mirror_map["flip"].keys())

    for bone in obj.data.edit_bones:
        if not bone.select:
            continue

        target = bone

        if duplicate:
            # _copyサフィックスを明示的に付与した新しいボーンを作成
            src_name = bone.name + "_copy"
            target = obj.data.edit_bones.new(src_name)
            target.head = bone.head.copy()
            target.tail = bone.tail.copy()
            target.roll = bone.roll
            target.use_connect = False
            target.parent = None
            renamed += 1
            bone_map[bone.name] = target

        mirror_mode = context.scene.brt_mirror_mode

        if mirror:
            mirror_mode = context.scene.brt_mirror_mode

            if duplicate:   # 複製しない時はミラーしない
                # apply_mirror_transform(target, mirror_mode)   # ローカル軸
                mirror_bone_global(target, mirror_mode)   # グローバル軸
            
            # 名前反転と識別子付与の順序処理
            name = strip_copy_suffix(target.name)  # "_copy"除去済みのベース名

            # flip処理（識別子が既に含まれている場合のみ）
            has_identifier = has_structured_identifier(name, ident_list)
            if has_identifier:
                name = apply_name_flip(name, mirror_map["flip"])
                print(f"▶ 名前反転: {target.name} → {name}")
                renamed += 1

            # 識別子の付与（反転後の target に対して）
            if assign_identifier:
                actual_side = determine_side(target)  # ←ここを bone ではなく target にする！
                identifier = (
                    mirror_map.get("left") if actual_side == "L"
                    else mirror_map.get("right") if actual_side == "R"
                    else ""
                )
                prefix_fallback = prefix or derive_local_prefix(name)
                name = insert_identifier_by_structure(name, identifier, prefix_fallback)
                print(f"▶ 識別子付与: {target.name} → {name}")
                renamed += 1

            target.name = name

            
        '''
        if mirror:
            # X軸方向を反転してミラー
            target.head[0] *= -1
            target.tail[0] *= -1
            
            # ロールも反転（Z軸を基準に反転するようなイメージ）
            target.roll *= -1
        '''

        # STEP1: _copy を除去して base name を取得
        name = strip_copy_suffix(target.name)

        # STEP2: すでに識別子を持っていれば flip 処理のみ
        if has_structured_identifier(name, ident_list):
            new_name = apply_name_flip(name, mirror_map["flip"])
            print(f"▶ 名前反転: {name} → {new_name}")
            renamed += 1
            target.name = new_name

        # STEP3: 識別子がない場合 → 空間位置から判断して付与
        elif assign_identifier:
            actual_side = determine_side(target)  # ← target は反転済みの状態
            identifier = (
                mirror_map.get("left") if actual_side == "L"
                else mirror_map.get("right") if actual_side == "R"
                else ""
            )
            prefix_fallback = prefix or derive_local_prefix(name)
            new_name = insert_identifier_by_structure(name, identifier, prefix_fallback)
            print(f"▶ 識別子付与: {name} → {new_name}")
            renamed += 1
            target.name = new_name

    
    if duplicate:
        for orig_name, target in bone_map.items():
            orig_bone = obj.data.edit_bones.get(orig_name)
            if orig_bone and orig_bone.parent:
                parent_name = orig_bone.parent.name
                parent_target = bone_map.get(parent_name)
                if parent_target:
                    target.parent = parent_target
                    if orig_bone.use_connect:
                        target.use_connect = True
                        target.head = parent_target.tail.copy()  # 接続点を一致させる
                    else:
                        target.use_connect = False
                        # 接続しない場合は、head/tailを元のローカル位置のまま維持する
                        

    # 編集完了後に元のモードに戻す（Blenderの仕様に準拠）
    if initial_mode == 'EDIT_ARMATURE':
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        bpy.ops.object.mode_set(mode=initial_mode)

    # デバック用
    print(f"▶ 処理完了: renamed = {renamed}")
    return renamed

# 指定されたパターン名に基づいて置換辞書を返す
def get_pattern_map_from_prefs(context, pattern_label: str, rule_index: Optional[int]) -> dict:
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    for p in prefs.bone_patterns:
        if p.label == pattern_label:

            # 🔧 assign_identifier=False → 全ルールからflipマップ構成
            if rule_index is None:
                flip_dict = {}
                for r in p.rules:
                    if r.left and r.right:
                        flip_dict[r.left] = r.right
                        flip_dict[r.right] = r.left
                return {
                    "left": "",   # 未使用でもキーとして必要
                    "right": "",
                    "flip": flip_dict
                }


            elif rule_index < len(p.rules):
                r = p.rules[rule_index]

                # ★ flip辞書は全ルールから構成する（付与は指定の left/right のみ）
                full_flip = {}
                for rr in p.rules:
                    if rr.left and rr.right:
                        full_flip[rr.left] = rr.right
                        full_flip[rr.right] = rr.left

                return {
                    "left": r.left,       # 付与にはこのleftを使う
                    "right": r.right,     # 付与にはこのrightを使う
                    "flip": full_flip     # 反転には全識別子を使う
                }

            '''
            # 🔧 assign_identifier=True → 単一ルールだけ使う
            elif rule_index < len(p.rules):
                r = p.rules[rule_index]
                return {
                    "left": r.left,
                    "right": r.right,
                    "flip": {r.left: r.right, r.right: r.left}
                }
            '''

    return {}
def apply_name_flip(name, flip_map):
    for left, right in flip_map.items():
        if right in name:
            return name.replace(right, left)
        elif left in name:
            return name.replace(left, right)
    return name  # flip対象なし

'''
# ボーン名に対して左右識別子に基づく置換を適用
def apply_name_flip(name: str, mapping: dict) -> str:
    for a, b in mapping.items():
        if a in name:
            return name.replace(a, b)
    return name
'''
    
'''
# サフィックス除去関数（_copy式に変えたので使わない）
def strip_duplicate_suffix(name: str) -> str:
    """
    Blenderが自動で付ける `.001`, `.002` などを除去。
    例: 'Head_L.001' → 'Head_L'
    """
    return re.sub(r"\.\d{3}$", "", name)
'''
    
# _copy' で終わっていれば除去
def strip_copy_suffix(name: str) -> str:
    return name[:-5] if name.endswith("_copy") else name

# ボーンの左右側を判定（EDITモード・POSEモード兼用）
def determine_side(bone) -> str:
    """ bone.head.x が + なら 'R'、- なら 'L'、0に近い場合は 'C'（中央扱い）"""
    x = bone.head.x if hasattr(bone, "head") else 0
    if x > 0.0001:
        return "R"
    elif x < -0.0001:
        return "L"
    else:
        return "C"



def insert_identifier_after_prefix(name: str, identifier: str, prefix: str) -> str:
    if name.startswith(prefix):
        rest = name[len(prefix):]

        # アンダースコア重複を抑制
        if prefix.endswith("_") and identifier.startswith("_"):
            identifier = identifier.lstrip("_")
        if identifier.endswith("_") and rest.startswith("_"):
            identifier = identifier.rstrip("_")

        return prefix + identifier + rest
    return name


#　識別子の有無を構造的に判定
def has_structured_identifier(name: str, identifiers: list) -> bool:
    """
    ボーン名に識別子（_l_, _r_, r01, l01 など）が含まれているか構造的に判定。
    """
    name_lower = name.lower()

    for ident in identifiers:
        ident_lower = ident.lower()
        # 完全一致 or 接頭辞/接尾辞的な一致を許容
        if (ident_lower in name_lower
            or name_lower.startswith(ident_lower)
            or name_lower.endswith(ident_lower)):
            return True

    return False

# 識別子の挿入位置を末尾の連番・サフィックスの前にする
def insert_identifier_before_suffix(name: str, identifier: str) -> str:
    """
    末尾の _000, _wj, _wj_ex などの前に識別子を挿入。
    例: j_hand_a_000_wj → j_hand_a_l_000_wj
    """
    match = re.search(r"(_\d{2,3}(_wj(_ex)?)?|_wj(_ex)?)$", name)
    if match:
        idx = match.start()
        return name[:idx] + "_" + identifier.strip("_") + name[idx:]
    else:
        return name + "_" + identifier.strip("_")
    
# 識別子の種類別挿入ルール
def insert_identifier_by_style(name: str, identifier: str, prefix: Optional[str]) -> str:
    ident = identifier.strip()
    prefix = prefix or ""

    starts_special = ident.startswith(("_", "."))
    ends_special = ident.endswith(("_", "."))

    if starts_special and ends_special:
        # 両端に記号 → prefixの後に挿入
        return insert_identifier_after_prefix(name, ident, prefix)

    elif starts_special:
        # 先頭に記号のみ → 末尾に追加（_r → name_r）
        return name.rstrip("_") + ident

    elif ends_special:
        # 末尾に記号のみ → 先頭に追加（r_ → r_name）
        return ident + name.lstrip("_")

    else:
        # 両端に記号なし → _付きで末尾追加（ex → name_ex）
        return name + "_" + ident

# 識別子がない場合、個別ボーン名からprefixを推定（例: j_hand → j_hand_）
def derive_local_prefix(name: str) -> str:
    parts = name.split("_")
    return "_".join(parts[:2]) + "_" if len(parts) >= 2 else ""

# 指定の識別子（例: _l_）を、ボーン名構造に従って最適な位置に挿入する。
def insert_identifier_by_structure(name: str, identifier: str, prefix: Optional[str]) -> str:
    identifier = identifier.strip("_")
    
    # ① _00_000_形式を検出 → _00 の前に挿入
    match = re.search(r"(_\d{2})_\d{3}(_)?(wj|wj_ex)?$", name)
    if match:
        idx = match.start(1)
        return name[:idx] + "_" + identifier + name[idx:]

    # ② _000_wj / _wj の形式 → サフィックスの前に挿入
    match = re.search(r"(_\d{2,3}(_wj(_ex)?)?|_wj(_ex)?)$", name)
    if match:
        idx = match.start()
        return name[:idx] + "_" + identifier + name[idx:]

    # ③ 数字もサフィックスもない → derive_local_prefixで挿入
    prefix = derive_local_prefix(name)
    if prefix and prefix in name:
        return insert_identifier_after_prefix(name, "_" + identifier + "_", prefix)

    # ④ 最後の保険として末尾に追加
    return name + "_" + identifier