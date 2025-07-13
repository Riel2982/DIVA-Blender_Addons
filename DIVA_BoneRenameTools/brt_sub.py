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

# 自動選択
def select_linear_chain_inclusive(bone_name, prefix_filter=None):
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
        select = lambda b: setattr(b, "select", True)
    else:
        return  # 非対応モード

    bone = bones.get(bone_name)
    if not bone or not is_valid(bone):
        return

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