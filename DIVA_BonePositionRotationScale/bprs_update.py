# bprs_update.py

import bpy
import os
import json
import zipfile
import shutil
import re
import datetime
import addon_utils

from bpy.app.handlers import persistent
from bpy.app.translations import pgettext as _

from .bprs_debug import DEBUG_MODE   # デバッグ用

# 処理制御関連 -------------------------------------

# 通知モード切り替え（True: バージョン比較 / False: プレリリース含む時刻比較）
USE_VERSION_CHECK = True

# モードに応じてフラグを設定（自動で排他的に切り替わる）
CHECK_CURRENT_VERSION = USE_VERSION_CHECK
CHECK_PRE_RELEASE = not USE_VERSION_CHECK

if False:
    # 現在のバージョンと比較して通知を決定（Falseならバージョン関係なく日時基準で通知）
    CHECK_CURRENT_VERSION = True
    # stable以外の通知を出すかどうか
    CHECK_PRE_RELEASE = False

# 不要ファイル実行制御フラグ（一括管理）
ENABLE_OBSOLETE_FILE_REMOVAL = False


# 設定ファイル関連の関数 -------------------------------------
def get_addon_folder():
    return os.path.dirname(os.path.abspath(__file__))

def get_settings_path():
    return os.path.join(get_addon_folder(), "bprs_settings.json")

# 設定ファイルの生成・保存
def load_settings():
    try:
        with open(get_settings_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(new_data):
    settings = load_settings()
    before = settings.copy()  # 変更前を記録
    settings.update(new_data)  # 既存項目を保持しつつ更新

    try:        # w=存在しない場合は生成
        with open(get_settings_path(), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)

        if DEBUG_MODE:
            changed_keys = [k for k in new_data if before.get(k) != new_data[k]]
            if changed_keys:
                print("[BPRS] 設定ファイルを保存しました:", ", ".join(changed_keys))
            else:
                print("[BPRS] 設定ファイル: 変更なし")

    except Exception as e:
        if DEBUG_MODE:
            print("[BPRS] 保存失敗:", str(e))

# DL先フォルダの読み込み
def load_download_folder():
    settings = load_settings()
    return settings.get("download_folder", "")




# 更新通知関連の関数 -------------------------------------

# ZIPファイル名からstatusを抽出
def parse_release_filename(name):
    name = name.lower().replace(".zip", "")
    # match = re.match(r"^.*[_\-]?v?(\d+\.\d+\.\d+)(?:\s+([a-z0-9αβ]+))?$", name)
    match = re.search(
        r"[_\-]?v?(\d+\.\d+\.\d+)(?:[._\-\s]*([a-zαβ]+)[\s\-]?(\d+)?)?",
        name
    )

    if match:
        version = f"v{match.group(1)}"
        raw_status = match.group(2)
        status_num = match.group(3)

        if not raw_status:
            status = "stable"
        else:
            original = raw_status

            # 正規化処理
            status = raw_status.replace("α", "alpha").replace("β", "beta")

            # 例: alpha3 → alpha3（そのまま）、beta → beta
            # 例: rc1 → rc1（そのまま）

            # 誤字補正（bata → beta）
            status = re.sub(r"^bata", "beta", status)

            # 数字があれば結合（例: beta + 3 → beta3）
            if status_num:
                status += status_num

            if DEBUG_MODE and original != status:
                print(f"[BPRS] ステータス補正: '{original}' → '{status}'")

        if DEBUG_MODE:
            print(f"[BPRS] ファイル名解析: version={version}, status={status}")

        return {"version": version, "status": status}

    if DEBUG_MODE:
        print(f"[BPRS] ファイル名解析失敗: '{name}'")

    return {"version": "", "status": "unknown"}


# GitHub最新リリース情報取得
def get_latest_release_info(force=False):
    settings = load_settings()
    last_api_check_str = settings.get("api_checked_at", "")
    try:
        last_api_check = datetime.datetime.fromisoformat(last_api_check_str)
    except Exception:
        last_api_check = None

    # GitHub APIを叩くかどうかを判定（60分以上経過していたら取得）
    now = datetime.datetime.now(datetime.timezone.utc)
    should_refresh = force or (not last_api_check or (now - last_api_check) > datetime.timedelta(minutes=60))   # 引数がTrueなら時間間隔を無視して取得

    if not should_refresh:
        # キャッシュされた日時を返す（保存済みの latest_release を使う）
        release = settings.get("latest_release", {})
        return release  # ← datetime に変換せず、そのまま返す

    # 取得処理（GitHub API）
    url = "https://api.github.com/repos/Riel2982/DIVA-Blender_Addons/releases/latest"
    try:
        import urllib.request, json
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

            if DEBUG_MODE:
                print("[BPRS] GitHub API レスポンス:")
                print("  - published_at:", data.get("published_at"))
                print("  - tag_name:", data.get("tag_name"))
                print("  - assets:", [a.get("name") for a in data.get("assets", [])])

            published_at = data.get("published_at", "")
            assets = data.get("assets", [])

            version = None

            # ZIPファイル照合
            pattern = re.compile(r"^DIVA_BonePositionRotationScale.*\.zip$", re.IGNORECASE)
            
            for asset in assets:
                name = asset.get("name", "")
                if DEBUG_MODE:
                    print("  [BPRS] ZIPファイル名:", name)

                if pattern.match(name):
                    parsed = parse_release_filename(name)
                    version = parsed["version"]
                    status = parsed["status"]
                    if DEBUG_MODE:
                        print(f"  [BPRS] バージョン抽出: {version} / ステータス: {status}")
                    break
                else:
                    if DEBUG_MODE:
                        print("  [BPRS] バージョン抽出失敗:", name)

            if not version and DEBUG_MODE:
                print("[BPRS] ZIPファイルからバージョンが抽出できません")

            release_info = {
                "published_at": published_at,
                "version": version or "",
                "status": status or "unknown"
            }

            # 保存
            save_settings({
                "api_checked_at": now.isoformat(),         # ← API取得制御用
                "latest_release": release_info             # ← リリース情報
            })

            return release_info  # dict: {published_at, version}

    except Exception as e:
        if DEBUG_MODE:
            print("[BPRS] GitHub取得失敗:", str(e))
        return {}  # API取得失敗時


# GitHubリリース情報の取得（API取得ではなく保存したローカルから取得）
def get_latest_release_data():
    settings = load_settings()
    return settings.get("latest_release", {})

# アドオンのバージョン取得
def get_current_version():
    try:
        from . import bl_info
        version = bl_info.get("version", ())
        if DEBUG_MODE:
            print(f"[BPRS] 現在のアドオンバージョン: {version}")
        return version
    except Exception:
        if DEBUG_MODE:
            print("[BPRS] bl_info の取得に失敗")
        return ()

# 更新通知判定
def is_new_release_available():
    latest = get_latest_release_info()
    if not latest:
        if DEBUG_MODE:
            print("[BPRS] 最新リリース情報が取得できません")
        return False

    # GitHubのバージョンを取得
    version_str = latest.get("version", "").lstrip("v")
    try:
        latest_version = tuple(map(int, version_str.split(".")))
        if DEBUG_MODE:
            print("[BPRS] GitHub最新バージョン:", latest_version)
    except Exception:
        if DEBUG_MODE:
            print("[BPRS] バージョン文字列の解析失敗:", version_str)
        return False

    # latest["published_at"] を datetime に変換
    published_at = latest.get("published_at", "")
    try:
        latest_dt = datetime.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        if DEBUG_MODE:
            print("[BPRS] GitHubリリース日時:", latest_dt)
    except Exception:
        if DEBUG_MODE:
            print("[BPRS] リリース日時の解析失敗:", published_at)
        return False

    settings = load_settings()
    
    # update_check を取得
    update_check_str = settings.get("update_check", "")
    try:
        update_check = datetime.datetime.fromisoformat(update_check_str)
    except Exception:
        update_check = None

    # last_update を取得
    last_update_str = settings.get("last_update", "")
    try:
        last_update = datetime.datetime.fromisoformat(last_update_str)
    except Exception:
        last_update = None

    # どちらか新しい方を基準にする
    reference = max(filter(None, [update_check, last_update]), default=None)
    if DEBUG_MODE:
        print("[BPRS] 通知判定の基準日時:", reference)

    # 現在のアドオンバージョンを取得
    if CHECK_CURRENT_VERSION:
        current_version = get_current_version()

        if current_version and latest_version <= current_version:
            if DEBUG_MODE:
                print("[BPRS] 現在のバージョンが最新以上のため通知不要")
            return False  # 最新と同じかそれ以上なら通知不要

        # バージョンが新しい → 時刻も新しいか確認
        if not reference or latest_dt > reference:
            if DEBUG_MODE:
                print("[BPRS] 新しいバージョンが検出されました")
            return True
        else:
            if DEBUG_MODE:
                print("[BPRS] バージョンは新しいが通知基準日時に達していません")
            return False

	# 時間基準で通知判定
    else:
        # バージョン無視 → 時刻のみで判定
        if not reference or latest_dt > reference:
            if DEBUG_MODE:
                print("[BPRS] リリース日時が通知基準を超えました")
            return True
        else:
            if DEBUG_MODE:
                print("[BPRS] 通知不要：リリース日時が基準以下")
            return False

# UI通知ラベル表示
def get_release_label():
    wm = bpy.context.window_manager
    if not getattr(wm, "bprs_new_release_available", False):
        if DEBUG_MODE:
            print("[BPRS] 通知なし: bprs_new_release_available=False")
        return None

    release_info = get_latest_release_data()
    version = release_info.get("version", "")
    status = release_info.get("status", "unknown")

    if not version:
        if DEBUG_MODE:
            print("[BPRS] 通知なし: versionが空")
        return None

    if status != "stable" and not CHECK_PRE_RELEASE:
        if DEBUG_MODE:
            print(f"[BPRS] 通知抑制: status={status}")
        return None

    # 表示用バージョン名
    display_version = version
    if status != "stable":
        display_version += f" ({status})"

    # 日本語用表示整形（statusの括弧を除去して括弧で囲む）
    locale = bpy.app.translations.locale
    if locale == "ja_JP":
        clean = re.sub(r"\((.*?)\)", r" \1", display_version).strip()
        display_version = f"({clean})"

    if DEBUG_MODE:
        print(f"[BPRS] 通知表示: {display_version}")

    return display_version







# アドオン起動時・Blendファイル展開時・アドオン有効化時関連の関数 -------------------------------------

# フラグに応じて不要ファイル削除を実行
def remove_obsolete_files_on_startup():
    # 更新後に削除する不要ファイル一覧（相対パス）
    OBSOLETE_FILES = [
        # "bprs_main.py",
        # "bprs_sub.py",     # コメントアウトで一時的に除外も可能
        # "bprs_import.py",
        # "bprs_ui_import.py",
        # "example/unused_script.py",  # フォルダに入っている場合はフォルダ名/ファイル名
    ]

    if not ENABLE_OBSOLETE_FILE_REMOVAL:
        return  # ファイルを削除しない

    wm = bpy.context.window_manager
    if getattr(wm, "bprs_obsolete_cleanup_done", False):
        return  # すでに削除済みならスキップ

    addon_folder = os.path.dirname(os.path.abspath(__file__))
    deleted_files = []  # 削除成功ファイル一覧

    for rel_path in OBSOLETE_FILES:
        abs_path = os.path.join(addon_folder, rel_path)
        if os.path.isfile(abs_path):
            try:
                os.remove(abs_path)
                deleted_files.append(rel_path)
                if DEBUG_MODE:
                    print(f"[BPRS] 起動時に削除: {abs_path}")
            except Exception as e:
                if DEBUG_MODE:
                    print(f"[BPRS] 起動時削除失敗: {abs_path} → {str(e)}")
        else:
            if DEBUG_MODE:
                print(f"[BPRS] 起動時削除対象なし: {abs_path}")

    if DEBUG_MODE and deleted_files:
        print("[BPRS] 起動時に削除されたファイル一覧:")
        for f in deleted_files:
            print(f"  - {f}")

    wm.bprs_obsolete_cleanup_done = True  # フラグを立てて再実行防止



# 有効なDLフォルダが設定されている場合のみ更新リストを自動生成
def confirm_download_folder():
    scene = bpy.context.scene   # Scene からDLフォルダパスを取得（プロパティが未登録なら中止）
    if not hasattr(scene, "bprs_download_folder"):
        return  # プロパティ未登録 → スキップ
    
    folder = scene.bprs_download_folder  # 有効なパスかチェック
    if folder and os.path.isdir(folder):
        bpy.ops.bprs.confirm_download_folder('INVOKE_DEFAULT')   # フォルダが有効なら、リスト更新オペレーターを呼び出す

        if DEBUG_MODE:
            print("[BPRS] DLフォルダ確認を実行しました")



# BLENDファイル読み込み後に不要ファイル削除とDLフォルダ確認を実行
@persistent
def bprs_on_blend_load(dummy):
    wm = bpy.context.window_manager

    # 不要なファイルの削除
    remove_obsolete_files_on_startup()

    # 有効なDLフォルダが設定されている場合のみ更新リストを自動生成
    confirm_download_folder()

    # GitHub更新チェック
    result = is_new_release_available()
    wm.bprs_new_release_available = result

    if DEBUG_MODE:
        print("[BPRS] ファイル読み込み時更新チェック:", result)
        print("[BPRS] 通知フラグ:", wm.bprs_new_release_available)


# アドオン起動直後に呼ばれる初期処理
def initialize_candidate_list():
    wm = bpy.context.window_manager

    # 初期化済みならスキップ
    if getattr(wm, "bprs_initialized", False):
        if DEBUG_MODE:
            print("[BPRS] 初期化スキップ: bprs_initialized=True")
        return
    wm.bprs_initialized = True   # 以降の処理はスキップし、初期化フラグを立てる

    # 更新完了フラグをリセット（前回の更新完了表示が残っていたら消す）
    wm.bprs_update_completed = False

    # 起動時に不要ファイル削除
    remove_obsolete_files_on_startup()
    
    # 有効なDLフォルダが設定されている場合のみ更新リストを自動生成
    confirm_download_folder()

    # GitHub更新チェック
    result = is_new_release_available()
    wm.bprs_new_release_available = result

    if DEBUG_MODE:
        print("[BPRS] 起動時更新チェック:", result)
        print("[BPRS] 通知フラグ:", wm.bprs_new_release_available)