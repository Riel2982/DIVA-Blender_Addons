# fop_save.py

import bpy
import os
import re
from bpy.app.handlers import persistent

from .fop_debug import DEBUG_MODE   # デバッグ用


# 拡張子補完・自動ナンバリング保存関数
def get_safe_blend_save_path(folder, filename, overwrite_guard=True):
    if not filename.lower().endswith(".blend"):
        filename += ".blend"

    base_path = os.path.join(folder, filename)

    # overwrite_guard=False の時はそのまま保存、overwrite_guard=True の時はナンバリング保存
    if not overwrite_guard:
        return base_path

    base, ext = os.path.splitext(base_path)

    # 常に _01 から始める
    for i in range(1, 100):
        new_path = f"{base}_{i:02d}{ext}"
        if not os.path.exists(new_path):
            if DEBUG_MODE:
                print(f"[FOP] Blend保存 上書き防止: {new_path}")
            return new_path

    raise RuntimeError("Blend保存先がすべて埋まっています（上書き防止）")


if False:   # 拡張子補完・上書き防止関数
    def get_safe_blend_save_path(folder, filename, overwrite_guard=True):
        if not filename.lower().endswith(".blend"):
            filename += ".blend"
        base_path = os.path.join(folder, filename)

        # overwrite_guard=False の時はそのまま保存、overwrite_guard=True でも base_path が未使用ならそのまま保存（_01 など付けない）
        if not overwrite_guard or not os.path.exists(base_path):
            return base_path

        base, ext = os.path.splitext(base_path)
        for i in range(1, 100):
            new_path = f"{base}_{i:02d}{ext}"
            if not os.path.exists(new_path):
                if DEBUG_MODE:
                    print(f"[FOP] Blend保存 上書き防止: {new_path}")
                return new_path

        raise RuntimeError("Blend保存先がすべて埋まっています（上書き防止）")


# blendfile_overwrite_guard の更新時に scene.fop_blend_save_filename を再計算する
def update_overwrite_guard(self, context):
    scene = context.scene
    filename = os.path.basename(bpy.data.filepath) if bpy.data.filepath else "untitled.blend"
    base_name = os.path.splitext(filename)[0]

    if self.blendfile_overwrite_guard:
        base_name = re.sub(r'_\d{2}$', '', base_name)

    scene.fop_blend_save_filename = base_name

    if DEBUG_MODE:
        print(f"[FOP] overwrite_guard toggled → UI filename updated to {base_name}")






# --- 外部データ格納に関して ---------------------------------------------------------------------------------------------------------

""" # 除外対象の書き方
    "name_equals": "MyTexture.png",                     # ファイル名が完全一致
    "name_startswith": "BoneSplitGradientPreview",      # ファイル名が指定文字列で始まる
    "name_contains": "BoneSplit",                       # ファイル名が部分一致
    "path": "preview",                                  # ファイルパスに指定文字列が含まれる
    "path": "MyApp\Blender_Launcher",                   # ファイルパスに指定文字列が含まれる
"""
# 単一条件による除外ルール
EXCLUDE_SINGLE = {
    # "name_equals": "MyTexture.png",  
}

""" # 除外条件の書き方
    { "and": {
        "name_startswith": "Temp",                  # ファイル名が "Temp" で始まり
        "path": "temp"                              # パスが "temp" を含む
    }},
    { "or": {
        "name_equals": "Legacy.png",                # ファイル名が "Legacy.png" に一致
        "name_startswith": "Old",                   # またはファイル名が "Old" で始まる
    }},
    { "not": {
        "name_equals": "AlwaysInclude.png"          # このファイル名は除外対象から除外（強制含め）
    }},
    # Blenderでは "//" で始まるパスはプロジェクトルートからの相対パス
    # Windowsのバックスラッシュ（￥,\）は Blenderではスラッシュ（/）に変換する
"""
# 複合条件による除外ルール（AND / OR / NOT を明示）
EXCLUDE_COMPOSITE = [
    { "and": {
        "name_startswith": "BoneSplitGradientPreview",                  # ファイル名が "BoneSplitGradientPreview" で始まり
        "path": "Bone&WeightSplitter/resources/preview_image"           # パスがBone&WeightSplitter/resources/preview_imageを含む
    }},
]


# 判定対象のパスに、任意の除外ルールの "path" が部分一致すれば True
def is_excluded(path, rules):
    # ルール形式は {"path": "部分文字列"} に固定
    normalized = path.replace("\\", "/")    # バックスラッシュをスラッシュに統一（Windows対策）
    for rule in rules:
        target = rule.get("path", "").replace("\\", "/")
        if target and target in normalized:
            return True
    return False

# 画像名に対して、指定された単一除外ルールが一致すれば True を返す
def is_excluded_name(name, rule):
    for key, value in rule.items():
        if key == "name_equals" and name == value:  # name_equals: 完全一致
            return True
        elif key == "name_startswith" and name.startswith(value):   # name_startswith: 指定文字列で始まる
            return True
        elif key == "name_contains" and value in name:      # name_contains: 指定文字列を含む（部分一致）
            return True
    return False

# 複合条件ルールに従って、name/path に対する除外判定を行う
def is_excluded_composite(name, path, rule):
    def match(subrule):
        return (
            is_excluded_name(name, subrule) or
            is_excluded(path, [subrule])  # path判定はリスト形式で渡す
        )

    for key, subrules in rule.items():
        if key == "and":    # "and": 全ての条件が一致すれば除外
            return all(match({k: v}) for k, v in subrules.items())
        elif key == "or":   # "or": いずれかの条件が一致すれば除外
            return any(match({k: v}) for k, v in subrules.items())
        elif key == "not":  # "not": 条件が一致しなければ除外（＝一致したら含める）
            return not any(match({k: v}) for k, v in subrules.items())

    return False  # 論理構造が不明な場合は除外しない

# 除外判定の統合関数
def should_exclude(name, path):
    # 単一ルールによる除外（nameベース）
    if is_excluded_name(name, EXCLUDE_SINGLE):
        return True

    # 単一ルールによる除外（pathベース）
    if is_excluded(path, [EXCLUDE_SINGLE]):
        return True

    # 複合ルールによる除外（AND / OR / NOT）
    for rule in EXCLUDE_COMPOSITE:
        if is_excluded_composite(name, path, rule):
            return True

    return False  # いずれの除外条件にも一致しない

# フォントのアンパック処理
def unpack_fonts_safely():
    for font in bpy.data.fonts:
        name = font.name
        path = font.filepath

        # 内蔵フォントは除外（filepathが空かつpacked_fileがNone）
        if not path and not font.packed_file:
            if DEBUG_MODE:
                print(f"[SKIP] 内蔵フォント: {name}")
            continue

        # 除外対象かどうかを判定（name/path に対して）
        if should_exclude(name, path):
            if DEBUG_MODE:
                print(f"[SKIP] 除外対象フォント: {name}")
            continue

        # ファイルパスが空 or 実在しない場合はスキップ（行方不明）
        if not path or not os.path.exists(bpy.path.abspath(path)):
            if DEBUG_MODE:
                print(f"[SKIP] 行方不明フォント: {name} → {path}")
            continue

        # パックされていない場合はスキップ
        if not font.packed_file:
            if DEBUG_MODE:
                print(f"[SKIP] 未パックフォント: {name}")
            continue

        # アンパック解除（元の保存先を維持）
        font.unpack(method='USE_ORIGINAL')
        if DEBUG_MODE:
            print(f"[UNPACK] フォントアンパック解除: {name} → {path}")


# PACK状態のときに使用するアンパック解除処理
def unpack_external_data_safely():
    # 対象となる外部データ型を統合
    external_blocks = (
        list(bpy.data.images) +
        list(bpy.data.fonts) +
        list(bpy.data.movieclips) +
        list(bpy.data.sounds) +
        list(bpy.data.texts)
    )

    for block in external_blocks:
        name = getattr(block, "name", "")
        path = getattr(block, "filepath", "")

        # filepathが空かつ未パック → 実体なし（除外）
        if not path and not getattr(block, "packed_file", None):
            if DEBUG_MODE:
                print(f"[SKIP] 実体なし: {name}")
            continue

        # 除外対象かどうかを判定（name/path に対して）
        if should_exclude(name, path):
            if DEBUG_MODE:
                print(f"[SKIP] 除外対象: {name}")
            continue

        # ファイルパスが空 or 実在しない場合はスキップ（行方不明）
        if not path or not os.path.exists(bpy.path.abspath(path)):
            if DEBUG_MODE:
                print(f"[SKIP] 行方不明: {name} → {path}")
            continue

        # パックされていない場合はスキップ
        if not getattr(block, "packed_file", None):
            if DEBUG_MODE:
                print(f"[SKIP] 未パック: {name}")
            continue

        # unpack() メソッドが存在する型だけ処理
        if hasattr(block, "unpack"):
            block.unpack(method='USE_ORIGINAL')
            if DEBUG_MODE:
                print(f"[UNPACK] アンパック解除: {name} → {path}")
        else:
            if DEBUG_MODE:
                print(f"[SKIP] unpack不可: {name}（型: {type(block).__name__})")

if False:
    #  パス変更関数
    def make_paths_relative_safely():   # 相対パス化
        for block in (
            list(bpy.data.images) +
            list(bpy.data.fonts) +
            list(bpy.data.movieclips) +
            list(bpy.data.sounds) +
            list(bpy.data.texts)
        ):
            name = getattr(block, "name", "")
            path = getattr(block, "filepath", "")
            if should_exclude(name, path):
                if DEBUG_MODE:
                    print(f"[SKIP] 除外対象（相対化対象外）: {name}")
                continue
            if hasattr(block, "filepath") and path.startswith("//") is False:
                block.filepath = bpy.path.relpath(path)
                if DEBUG_MODE:
                    print(f"[RELATIVE] {name} → {block.filepath}")

    def make_paths_absolute_safely():   # 絶対パス化
        for block in (
            bpy.data.images +
            bpy.data.fonts +
            bpy.data.movieclips +
            bpy.data.sounds +
            bpy.data.texts
        ):
            name = getattr(block, "name", "")
            path = getattr(block, "filepath", "")

            if should_exclude(name, path):
                if DEBUG_MODE:
                    print(f"[SKIP] 除外対象（絶対化対象外）: {name}")
                continue

            if path and not os.path.isabs(bpy.path.abspath(path)):
                try:
                    block.filepath = bpy.path.abspath(path)
                    if DEBUG_MODE:
                        print(f"[ABSOLUTE] {name} → {block.filepath}")
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"[ERROR] 絶対パス変換失敗: {name} → {e}")



# 外部データ格納方式の判別
def detect_external_data_mode():
    # 対象となる外部データ型を統合（画像・フォント・動画・音声・テキスト）
    external_blocks = (
        list(bpy.data.images) +
        list(bpy.data.fonts) +
        list(bpy.data.movieclips) +
        list(bpy.data.sounds) +
        list(bpy.data.texts)
    )

    # 各モードのカウント初期化
    packed_count = 0       # PACKされたデータ数
    relative_count = 0     # 相対パス（//）のデータ数
    absolute_count = 0     # 絶対パスのデータ数
    total = 0              # 判定対象の総数

    for block in external_blocks:
        # filepath を持たない型は除外（例：内蔵フォントや空テキスト）
        if not hasattr(block, "filepath"):
            continue

        name = getattr(block, "name", "")
        path = block.filepath

        # filepathが空かつ未パック → 実体なし（除外）
        if not path and not getattr(block, "packed_file", None):
            continue

        # 除外対象かどうかを判定（name/path に対して）
        if should_exclude(name, path):
            if DEBUG_MODE:
                print(f"[SKIP] 除外対象（モード判定対象外）: {name}")
            continue


        total += 1  # 判定対象としてカウント

        # PACKされたデータ
        if getattr(block, "packed_file", None):
            packed_count += 1

        # 相対パス（//）のデータ
        elif path.startswith("//"):
            relative_count += 1

        # 絶対パスのデータ
        elif os.path.isabs(bpy.path.abspath(path)):
            absolute_count += 1

    # 判定対象がゼロ → 判定不能
    if total == 0:
        return None

    # dominant mode を判定（割合が閾値以上ならそのモード）
    threshold = 0.8
    if packed_count / total >= threshold:
        return 'PACK'
    elif relative_count / total >= threshold:
        return 'RELATIVE'
    elif absolute_count / total >= threshold:
        return 'ABSOLUTE'

    # どのモードも支配的でない場合 → 混在とみなす
    return 'MIXED'








# --- 保存・読み込み時に自動更新 ---------------------------------------------------------------------------------------

# --- 保存先パスの自動反映
def update_blend_save_path(scene):
    if bpy.data.filepath:   # Blendファイルが保存されている場合 → 保存先パスを更新
        scene.fop_blend_save_path = os.path.dirname(bpy.path.abspath(bpy.data.filepath))
        if DEBUG_MODE:
            print("[FOP] fop_blend_save_path updated:", scene.fop_blend_save_path)
    else:       # 保存されていない場合 → 保存先パスを空にする
        scene.fop_blend_save_path = ""
        if DEBUG_MODE:
            print("[FOP] No blend file saved yet")

# --- ファイル名の自動反映（overwrite_guard に応じて切り替え）
def update_blend_save_filename(scene):
    if bpy.data.filepath:
        filename = os.path.basename(bpy.data.filepath)
        base_name = os.path.splitext(filename)[0]

        if scene.fop_settings.blendfile_overwrite_guard:    # Trueの時
            # ナンバリング除去（例：Blendfile_01 → Blendfile）
            base_name = re.sub(r'_\d{2}$', '', base_name)

        scene.fop_blend_save_filename = base_name   # Falseの時（そのまま反映）

        if DEBUG_MODE:
            print("[FOP] fop_blend_save_filename updated:", scene.fop_blend_save_filename)
    else:
        scene.fop_blend_save_filename = "untitled"

# --- 外部データ格納方式反映（PACK / RELATIVE / ABSOLUTE / None）
def update_external_data_mode(scene):
    detected_mode = detect_external_data_mode()

    # PACKモード → pack_resources を True に設定
    if detected_mode == 'PACK':
        scene.fop_settings.pack_resources = True
        if DEBUG_MODE:
            print("[FOP] PACK mode detected → pack_resources = True")

    # RELATIVE / ABSOLUTE → external_data に反映
    elif detected_mode in {'RELATIVE', 'ABSOLUTE'}:
        scene.fop_settings.external_data = detected_mode
        if DEBUG_MODE:
            print(f"[FOP] external_data mode detected and set to: {detected_mode}")

    # 判別不能（混在 or 不明）→ 何も設定せずログのみ
    else:
        if DEBUG_MODE:
            print("[FOP] external_data mode could not be determined (mixed or unknown)")


# --- 保存・読み込み時に自動更新
@persistent
def fop_on_blend_load_or_save(dummy):
    scene = bpy.context.scene or bpy.data.scenes[0]     # シーン取得（bpy.context.scene が None の場合は fallback）

    update_blend_save_path(scene)   # ファイルパス自動反映
    update_blend_save_filename(scene)   # ファイル名自動反映（上書き防止対応済）
    update_external_data_mode(scene)    # 外部データ格納方式自動反映


if False:
    @persistent
    def fop_on_blend_load_or_save(dummy):
        # 自動パス更新
        scene = bpy.context.scene or bpy.data.scenes[0]     # シーン取得（bpy.context.scene が None の場合は fallback）
        
        if bpy.data.filepath:   # Blendファイルが保存されている場合 → 保存先パスを更新
            scene.fop_blend_save_path = os.path.dirname(bpy.path.abspath(bpy.data.filepath))
            if DEBUG_MODE:
                print("[FOP] fop_blend_save_path updated:", scene.fop_blend_save_path)

        else:       # 保存されていない場合 → 保存先パスを空にする
            scene.fop_blend_saved_path = ""
            if DEBUG_MODE:
                print("[FOP] No blend file saved yet")

        if False:
            # ファイル名の反映（保存済みの場合のみ）
            if bpy.data.filepath:
                # scene.fop_blend_save_filename = os.path.basename(bpy.data.filepath)   # 拡張子まで反映される
                scene.fop_blend_save_filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]    # 拡張子除く
                if DEBUG_MODE:
                    print("[FOP] fop_blend_save_filename updated:", scene.fop_blend_save_filename)
            else:   # 未保存時は"untitled"を仮代入
                scene.fop_blend_save_filename = "untitled"

        # ファイル名の反映（overwrite_guard に応じて切り替え）
        if bpy.data.filepath:
            filename = os.path.basename(bpy.data.filepath)
            base_name = os.path.splitext(filename)[0]

            if scene.fop_settings.blendfile_overwrite_guard:    # Trueの時
                # ナンバリング除去（例：Blendfile_01 → Blendfile）
                base_name = re.sub(r'_\d{2}$', '', base_name)

            scene.fop_blend_save_filename = base_name   # Falseの時（そのまま反映）

            if DEBUG_MODE:
                print("[FOP] fop_blend_save_filename updated:", scene.fop_blend_save_filename)
        else:
            scene.fop_blend_save_filename = "untitled"



        # 外部データ格納方式反映（PACK / RELATIVE / ABSOLUTE / None）
        detected_mode = detect_external_data_mode()

        # PACKモード → pack_resources を True に設定
        if detected_mode == 'PACK':
            scene.fop_settings.pack_resources = True
            if DEBUG_MODE:
                print("[FOP] PACK mode detected → pack_resources = True")

        # RELATIVE / ABSOLUTE → external_data に反映
        elif detected_mode in {'RELATIVE', 'ABSOLUTE'}:
            scene.fop_settings.external_data = detected_mode
            if DEBUG_MODE:
                print(f"[FOP] external_data mode detected and set to: {detected_mode}")

        # 判別不能（混在 or 不明）→ 何も設定せずログのみ
        else:
            if DEBUG_MODE:
                print("[FOP] external_data mode could not be determined (mixed or unknown)")
