# brt_sub.py（旧rename_detect）

import bpy
import re
from os.path import commonprefix

def clean_name(name):
    base = name.split(".")[0]  # 「.」より右を除外

    # サフィックス除去
    for suffix in ["_wj", "wj", "_wj_ex", "wj_ex"]:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break

    # "_" で区切って末尾が2〜3桁の数字なら除外（1回だけ）
    parts = base.split("_")
    if parts and parts[-1].isdigit() and len(parts[-1]) in (2, 3):
        parts.pop()
    base = "_".join(parts)

    return base

# 共通名の抽出
def detect_common_prefix(bones, suffix_enum, rule_enum):
    if not bones:
        return None

    suffix_patterns = ["_wj", "wj", "_wj_ex", "wj_ex"]
    rule_patterns = {
        "000": r"_\d{3}$",  # 例: _000, _001, ...
        "00": r"_\d{2}$",   # 例: _00, _01, ...
    }

    cleaned_names = [clean_name(b.name) for b in bones]
    if not cleaned_names:
        return None

    prefix = commonprefix(cleaned_names)
    return prefix if prefix else None

# 数字部分を除いた共通グループ名を抽出
def extract_common_group(name):
    parts = name.split("_")
    filtered = [p for p in parts if not re.fullmatch(r"\d{2,3}", p)]
    return "_".join(filtered)

# 自動選択
def select_linear_chain_inclusive(
    bone_name,
    prefix_filter=None,
    allow_branches=False,
    extend_by_common_group=False,
    child_only=False,
    filter_inconsistent=False,
):

    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        return

    mode = bpy.context.mode
    if mode == 'POSE':
        bones = obj.pose.bones
        get_name = lambda b: b.name
        get_parent = lambda b: b.parent
        get_children = lambda b: b.children
        set_active = lambda name: setattr(obj.data, "bones.active", obj.data.bones.get(name))
        is_valid = lambda b: b.bone
        select = lambda b: (
            setattr(b.bone, "select", True),
            setattr(b.bone, "select_head", True),
            setattr(b.bone, "select_tail", True)
        )
    elif mode == 'EDIT_ARMATURE':
        bones = obj.data.edit_bones
        get_name = lambda b: b.name
        get_parent = lambda b: b.parent
        get_children = lambda b: b.children
        set_active = lambda name: setattr(obj.data.edit_bones[name], "select", True)
        is_valid = lambda b: True
        select = lambda b: (
            setattr(b, "select", True),
            setattr(b, "select_head", True),
            setattr(b, "select_tail", True)
        )
    else:
        return  # 非対応モード

    bone = bones.get(bone_name)
    if not bone or not is_valid(bone):
        return

    '''
    # 親方向に一本道をさかのぼる
    current = bone
    while True:
        parent = get_parent(current)
        if not parent or len(parent.children) != 1:
            break
        # 親が prefix に一致しなければ止める
        if prefix_filter and not clean_name(get_name(parent)).startswith(prefix_filter):
            break
        current = parent
    root = current
    '''
    # 親方向に一本道をさかのぼる（child_only=False のときのみ）
    root = bone
    if not child_only:
        current = bone
        while True:
            parent = get_parent(current)
            if not parent or len(parent.children) != 1:
                break
            if prefix_filter and not clean_name(get_name(parent)).startswith(prefix_filter):
                break
            current = parent
        root = current
    

    # 子方向に探索（分岐があっても許容するかどうか）
    chain = []
    visited = set()

    target_group = extract_common_group(clean_name(get_name(bone)))

    def traverse(b):
        if b.name in visited:
            return
        visited.add(b.name)
        cname = clean_name(get_name(b))
        group = extract_common_group(cname)
        if prefix_filter and group != extract_common_group(prefix_filter):
            return  # フィルタと一致しない → 以降は除外
        chain.append(b)
        for child in get_children(b):
            if allow_branches:
                traverse(child)
            elif len(get_children(b)) == 1:
                traverse(child)

    # 分岐許容なら再帰探索、そうでなければ一本道探索
    if allow_branches:
        traverse(root)
    else:
        current = root
        while current:
            cname = clean_name(get_name(current))
            if prefix_filter and not cname.startswith(prefix_filter):
                break
            chain.append(current)
            children = get_children(current)
            if len(children) == 1:
                current = children[0]
            else:
                break
    '''
    # 子方向に一本道をたどる（分岐があってもそのボーンまでは含める）
    chain = []
    current = root
    while current:
        # ここでフィルタを適用
        cname = clean_name(get_name(current))
        if prefix_filter and not cname.startswith(prefix_filter):
            break  # フィルタと一致しない → 以降は除外
        chain.append(current)
        children = get_children(current)
        if len(children) == 1:
            current = children[0]
        else:
            break
    '''
    '''            
    # 共通グループによる選択範囲拡張
    if extend_by_common_group:
        for b in bones:
            if b not in chain and extract_common_group(clean_name(get_name(b))) == target_group:
                chain.append(b)
    '''
    # 共通グループによる選択範囲拡張
    if extend_by_common_group:
        base_clean = clean_name(get_name(bone))
        base_group = extract_common_group(base_clean)

        for b in bones:
            b_clean = clean_name(get_name(b))
            b_group = extract_common_group(b_clean)

            # 🔸 FalseもTrueも group一致だけで抽出（番号違い skirt系全部拾う）
            if b_group != base_group:
                continue

            print("[StrictChain]" if filter_inconsistent else "[OpenChain]",
                "基準ボーン名:", get_name(b),
                "clean_name:", b_clean,
                "extract_group:", b_group)

            if filter_inconsistent:
                extend_chain_strict(
                    bones=bones,
                    base_bone=b,
                    chain=chain,
                    get_name=get_name,
                    get_children=get_children,
                    clean_name=clean_name,
                    extract_common_group=extract_common_group
                )

            else:
                extend_chain_open(
                    bones=bones,
                    base_bone=b,
                    chain=chain,
                    get_name=get_name,
                    get_children=get_children,
                    clean_name=clean_name,
                    extract_common_group=extract_common_group,
                    allow_branches=allow_branches,
                    filter_inconsistent=False
                )

    # 全選択解除
    if mode == 'POSE':
        bpy.ops.pose.select_all(action='DESELECT')
    elif mode == 'EDIT_ARMATURE':
        for eb in bones:
            eb.select = False

    # チェーンの選択とアクティブ設定
    for b in chain:
        select(b)

    set_active(get_name(bone))


# inconsistent:True用            
def extend_chain_strict(
    bones,                   # アーマチュア全ボーン
    base_bone,               # 起点ボーン（選択済みの主ボーン）
    chain,                   # 選択対象リスト（上書き追加される）
    get_name,                # ボーン名取得関数
    get_children,            # 子ボーン取得関数
    clean_name,              # サフィックスや数字除去関数
    extract_common_group,     # 数字のみ除いたグループ名抽出関数

):
    base_name  = get_name(base_bone)
    base_clean = clean_name(base_name)
    base_group = extract_common_group(base_clean)

    print("[StrictChain] 基準ボーン名       :", base_name)
    print("[StrictChain] clean_name         :", base_clean)
    print("[StrictChain] extract_group      :", base_group)
    print("inconsistant & extend → ON")

    visited = set()

    def traverse_chain(bone):
        current = bone
        while current:
            if current.name in visited:
                break
            visited.add(current.name)

            b_clean = clean_name(get_name(current))
            b_group = extract_common_group(b_clean)

            if b_group != base_group or b_clean != base_clean:
                break

            chain.append(current)
            children = get_children(current)
            current = children[0] if len(children) == 1 else None

    for b in bones:
        if b in chain:
            continue
        b_clean = clean_name(get_name(b))
        b_group = extract_common_group(b_clean)

        if extract_common_group(b_clean) != extract_common_group(base_clean):
            continue

        traverse_chain(b)

# inconsistent-allow:False用    
def extend_chain_open(
    bones,                   # アーマチュア全ボーン
    base_bone,               # 起点ボーン（選択済みの主ボーン）
    chain,                   # 選択対象リスト（上書き追加される）
    get_name,                # ボーン名取得関数
    get_children,            # 子ボーン取得関数
    clean_name,              # サフィックスや数字除去関数
    extract_common_group,     # 数字のみ除いたグループ名抽出関数
    allow_branches=False,     # TrueでもFalseでも呼び出し元で固定される
    filter_inconsistent=False
):
    # 起点 clean_name とグループ名を抽出
    base_name  = get_name(base_bone)
    base_clean = clean_name(base_name)
    base_group = extract_common_group(base_clean)

    print("[OpenChain] 基準ボーン名       :", base_name)
    print("[OpenChain] clean_name         :", base_clean)
    print("[OpenChain] extract_group      :", base_group)

    visited = set()

    def traverse_chain_open(bone):
        current = bone
        while current:
            if current.name in visited:
                break
            visited.add(current.name)
            chain.append(current)

            children = get_children(current)
            if len(children) == 1:
                current = children[0]
            else:
                break

    for b in bones:
        b_clean = clean_name(get_name(b))
        b_group = extract_common_group(b_clean)

        if b in chain or b.name in visited:
            continue
        if b_group != base_group:
            continue

        traverse_chain_open(b)



#　親方向はたどらず子方向のみを選ぶ処理(Reneme用)
def select_child_chain_only(bone_name, prefix_filter=None):
    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        return

    mode = bpy.context.mode
    if mode == 'POSE':
        bones = obj.pose.bones
        get_name = lambda b: b.name
        get_children = lambda b: b.children
        set_active = lambda name: setattr(obj.data, "bones.active", obj.data.bones.get(name))
        is_valid = lambda b: b.bone
        select = lambda b: (
            setattr(b.bone, "select", True),
            setattr(b.bone, "select_head", True),
            setattr(b.bone, "select_tail", True)
        )
        clear = lambda: bpy.ops.pose.select_all(action='DESELECT')
    elif mode == 'EDIT_ARMATURE':
        bones = obj.data.edit_bones
        get_name = lambda b: b.name
        get_children = lambda b: b.children
        set_active = lambda name: setattr(obj.data.edit_bones[name], "select", True)
        is_valid = lambda b: True
        select = lambda b: (
            setattr(b, "select", True),
            setattr(b, "select_head", True),
            setattr(b, "select_tail", True)
        )
        clear = lambda: [setattr(b, "select", False) for b in bones]
    else:
        return

    bone = bones.get(bone_name)
    if not bone or not is_valid(bone):
        return

    # 全選択解除
    clear()

    # 子方向に一本道をたどる（親はたどらない）
    chain = []
    current = bone
    while current:
        cname = clean_name(get_name(current))
        if prefix_filter and not cname.startswith(prefix_filter):
            break
        chain.append(current)

        children = get_children(current)
        if len(children) == 1:
            current = children[0]
        else:
            break

    for b in chain:
        select(b)
    set_active(get_name(bone))
