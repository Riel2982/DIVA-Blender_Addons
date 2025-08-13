# bprs_uix_update.py

import bpy
import os
import json
import zipfile
import shutil
import re
import datetime
from bpy.app.handlers import persistent
from bpy.app.translations import pgettext as _

from .bprs_update import save_settings, load_download_folder, get_latest_release_data, get_release_label

from .bprs_debug import DEBUG_MODE   # デバッグ用

# アドオンプリファレンス本体（表示と編集UI）
class BPRS_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "DIVA_BonePositionRotationScale"  # アドオンのフォルダ名（ハイフンや半角スペース、記号は使用不可）

    initialized: bpy.props.BoolProperty(
        name="initialized",
        default=False,
        options={'HIDDEN'}
    )

    def draw(self, context):
        layout = self.layout
        prefs = self
        scene = context.scene

        # 更新用UI
        draw_update_ui(layout, scene)


# --- アドオン更新UI -------------------------------------
def draw_update_ui(layout, scene):
    box = layout.box()
    # box.label(text=_("Update"), icon='FILE_REFRESH')

    row = box.row()  # ← 横一列に並べる
    op1 = row.operator("bprs.open_url", text=_("Check for Updates"), icon="CHECKMARK")      # 更新を確認
    op1.url = "https://github.com/Riel2982/DIVA-Blender_Addons/releases"

    row.operator("bprs.execute_update", text=_("Install"), icon="IMPORT")  # インストール
    row.operator("bprs.open_addon_folder", text=_("Open Addon Folder"), icon="FILE_FOLDER")        # アドオンフォルダを開く

    # アドオンの最新リリースのお知らせ
    wm = bpy.context.window_manager
    if wm.bprs_new_release_available:
        display_version = get_release_label()
        if display_version:
            row = box.row()
            row.label(text=_("GitHub has a recent release: ") + display_version, icon="INFO")

    if False:
        wm = bpy.context.window_manager
        if getattr(wm, "bprs_new_release_available", False): # 最新リリースがあるとき
            release_info = get_latest_release_data()
            version = release_info.get("version", "")
            if version:
                row = box.row()
                # row.label(text=_("GitHub has a recent release. ") + version + ".", icon="INFO")   # バージョンの後にピリオドがついてしまう。
                row.label(text=_("GitHub has a recent release. ") + version, icon="INFO")

    # ダウンロード先パスのラベル＋操作群をまとめて一行に並べる
    row = box.row()
    row.prop(scene, "bprs_download_folder", text=_("Path to ZIP download folder "))  # テキスト入力欄（ラベルなし）/ ZIP保存先フォルダ パス

    # 成功時だけ表示する INFOラベル
    wm = bpy.context.window_manager
    if getattr(wm, "bprs_update_completed", False):
        box.label(text=_("Update completed. Please restart Blender"), icon="INFO")   # 更新が完了しました。Blenderを再起動してください

    # 非実行時・失敗時に表示する 更新ファイルリスト
    else:
        row = box.row()
        row.label(text=_("Update file list: "), icon='PRESET')
        row.operator("bprs.sort_candidates_name", text="", icon="SORTALPHA")     # 名前順
        row.operator("bprs.sort_candidates_date", text="", icon="SORTTIME")      # 日付順
        row.operator("bprs.confirm_download_folder", text="", icon="FILE_REFRESH")  # リスト更新

        box.template_list(
            "BPRS_UL_UpdateCandidateList", "",
            scene, "bprs_update_candidates",
            scene, "bprs_selected_candidate_index",
            rows=2      # 初期行数
        )


# --- プロパティグループ＆UIリスト -------------------------------------
class BPRS_UpdateCandidateItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    date: bpy.props.StringProperty()

class BPRS_UL_UpdateCandidateList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # 行を分割して領域比率を調整
        split = layout.split(factor=0.7, align=True)
        split.label(text=item.name)   # 左側（70%）：ファイル名
        split.label(text=item.date)   # 右側（30%）：日時



# 各種オペレーター
class BPRS_OT_OpenURL(bpy.types.Operator):
    """更新を確認"""
    bl_idname = "bprs.open_url"
    bl_label = "Check for Updates"
    bl_description = _("Opens the GitHub release page to check for update files")

    url: bpy.props.StringProperty()

    def execute(self, context):
        import webbrowser
        webbrowser.open(self.url)   # GitHubのURLを開く
    
        # 更新確認日時を保存
        # now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # save_settings({"update_check": now})
        save_settings({"update_check": datetime.datetime.now(datetime.timezone.utc).isoformat()})


        # 通知を消す
        context.window_manager.bprs_new_release_available = False    

        return {'FINISHED'}


class BPRS_OT_ExecuteUpdate(bpy.types.Operator):
    """更新ファイルをインストール"""
    bl_idname = "bprs.execute_update"
    bl_label = "Install Update File"
    bl_description = _("Select a ZIP archive beginning with DIVA_BonePositionRotationScale to install the update")
    # bl_options = {'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Select ZIP File",
        description=_("Choose a ZIP file starting with DIVA_BonePositionRotationScale"),    # DIVA_BonePositionRotationScaleで始まるZIPファイルを選択してください
        #　filter_glob='*.zip'      # 4.2以降ファイルパスが取得できない原因
    )

    # ユーザーにフォルダ選択してもらうためのプロパティ（手動選択時のみ使用想定だがZIPファイル選択ダイアログとして機能）
    dirpath: bpy.props.StringProperty(
        name="Select Addon Folder",
        description=_("Choose the folder where the addon is installed"),    # アドオンがインストールされているフォルダを選択してください
        subtype='DIR_PATH'
    )

    # 共通処理(更新対象の照合関数)
    def read_bl_info_name(self, init_path):
        """指定された __init__.py から bl_info['name'] を抽出する"""
        import ast
        try:
            with open(init_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), init_path)
                for node in tree.body:
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == "bl_info":
                                for key, value in zip(node.value.keys, node.value.values):
                                    if getattr(key, "s", "") == "name":
                                        return getattr(value, "s", None)
        except Exception:
            return None

    def execute(self, context):
        # 🔹 UIリストが選ばれていて、filepath が空の場合のみ 自動補完
        if not self.filepath:
            index = context.scene.bprs_selected_candidate_index
            candidates = context.scene.bprs_update_candidates
            if 0 <= index < len(candidates):
                self.filepath = candidates[index].path

            # それでも filepath が空なら → ダイアログで選択させるべき
            if not self.filepath:
                self.report({'INFO'}, _("No ZIP file selected. Please specify a file"))     # ZIPファイルが選択されていません。ファイルを指定してください
                context.window_manager.fileselect_add(self)
                return {'RUNNING_MODAL'}

        # ZIPファイル名の確認（パターンに一致しなければ処理中止）
        filename = os.path.basename(self.filepath)
        pattern = re.compile(r"^DIVA_BonePositionRotationScale.*\.zip$", re.IGNORECASE)
        if not pattern.match(filename):
            self.report({'WARNING'}, _("Only ZIP files starting with DIVA_BonePositionRotationScale can be processed"))       # DIVA_BonePositionRotationScale で始まるZIPファイル以外は処理できません
            context.window_manager.bprs_update_completed = False
            return {'CANCELLED'}

        # 一時解凍フォルダの作成
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        extract_path = os.path.join(downloads_path, "_bprs_temp_extract")
        os.makedirs(extract_path, exist_ok=True)

        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # ZIP内のbl_info['name']を取得
            source_folder = os.path.join(extract_path, "DIVA_BonePositionRotationScale")
            source_init = os.path.join(source_folder, "__init__.py")
            if not os.path.isdir(source_folder) or not os.path.isfile(source_init):
                self.report({'WARNING'}, _("Missing DIVA_BonePositionRotationScale folder or __init__.py inside the ZIP file"))       # ZIP内に DIVA_BonePositionRotationScale フォルダまたは __init__.py が見つかりません
                shutil.rmtree(extract_path)
                context.window_manager.bprs_update_completed = False
                return {'CANCELLED'}

            source_name = self.read_bl_info_name(source_init)
            if not source_name:
                self.report({'WARNING'}, _("Could not retrieve bl_info.name from the ZIP file"))        # ZIP内の bl_info.name を取得できません
                shutil.rmtree(extract_path)
                context.window_manager.bprs_update_completed = False
                return {'CANCELLED'}

            # 自分自身のアドオンフォルダを取得
            try:
                self_folder = os.path.dirname(os.path.abspath(__file__))
                self_init = os.path.join(self_folder, "__init__.py")
                self_name = self.read_bl_info_name(self_init)
            except Exception:
                self_folder = None
                self_name = None

            # bl_info.name が一致するか判定（異なれば処理中止）
            if self_folder and self_name == source_name:
                target_folder = self_folder

            # 自動判定失敗 → ユーザーにフォルダを選ばせる
            else:
                if not self.dirpath:
                    # ユーザーに状況を説明してからDIR選択させる
                    self.report({'INFO'}, _("Addon installation folder not found. Please select the destination folder manually"))    # インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください
                    context.window_manager.fileselect_add(self)  # DIR選択を促す
                    return {'RUNNING_MODAL'}

                # DIR選択後：キャンセルされた場合は中止＋後始末
                if not self.dirpath:
                    self.report({'INFO'}, _("Installation was cancelled"))
                    shutil.rmtree(extract_path, ignore_errors=True)     # 一時フォルダの削除
                    context.window_manager.bprs_update_completed = False
                    return {'CANCELLED'}

                # 選ばれたフォルダに __init__.py があるか確認
                manual_init = os.path.join(self.dirpath, "__init__.py")
                if not os.path.isfile(manual_init):
                    self.report({'WARNING'}, _("__init__.py not found in the selected folder"))
                    shutil.rmtree(extract_path)
                    context.window_manager.bprs_update_completed = False
                    return {'CANCELLED'}

                manual_name = self.read_bl_info_name(manual_init)
                if manual_name != source_name:
                    self.report({'WARNING'}, _("Update failed because bl_info.name does not match"))        # bl_info.name が一致しないため、更新できません
                    shutil.rmtree(extract_path)
                    context.window_manager.bprs_update_completed = False
                    return {'CANCELLED'}

                # 一致したので選択されたフォルダに更新実行
                target_folder = self.dirpath

            # 更新を実行（アドオンフォルダに中身を上書きコピー）
            for root, dirs, files in os.walk(source_folder):
                rel_path = os.path.relpath(root, source_folder)
                dest_dir = os.path.join(target_folder, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
                for file in files:
                    shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))

            # 一時フォルダの削除
            shutil.rmtree(extract_path)

            # 更新日時を保存
            # now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # save_settings({"last_update": now})
            save_settings({"last_update": datetime.datetime.now(datetime.timezone.utc).isoformat()})

            # 通知を消す
            context.window_manager.bprs_new_release_available = False

            # 更新完了ポップアップ表示
            self.report({'INFO'}, _("Update completed. Please restart Blender"))        # 更新が完了しました。Blenderを再起動してください
            context.window_manager.bprs_update_completed = True
            return context.window_manager.invoke_popup(self, width=400)

        except Exception as e:  # 例外発生時のエラー通知とクリーンアップ
            self.report({'WARNING'}, _("Update failed: {error}").format(error=str(e)))
            shutil.rmtree(extract_path, ignore_errors=True)
            context.window_manager.bprs_update_completed = False
            return {'CANCELLED'}

    # 更新完了時のポップアップ表示内容
    def draw(self, context):
        layout = self.layout
        # layout.label(text=_("Please select a ZIP file"), icon='INFO')     # ZIPファイルを選択してください
        layout.label(text=_("Please restart Blender after the update"), icon='INFO')    # 更新後はBlenderを再起動してください

        
class BPRS_OT_OpenAddonFolder(bpy.types.Operator):
    """現在のアドオンフォルダを開く"""
    bl_idname = "bprs.open_addon_folder"
    bl_label = "Open Addon Folder"
    bl_description = _("Opens the folder where this addon is installed")

    def execute(self, context):
        import os
        import subprocess

        # 実行中のアドオンフォルダを取得
        self_folder = os.path.dirname(os.path.abspath(__file__))

        # Windowsのエクスプローラーでフォルダを開く
        subprocess.Popen(f'explorer "{self_folder}"')

        return {'FINISHED'}

class BPRS_OT_ConfirmDownloadFolder(bpy.types.Operator):
    """更新ファイルリスト更新"""
    bl_idname = "bprs.confirm_download_folder"
    bl_label = "Confirm Download Folder"
    bl_description = _("Scan the folder and list update candidate files")

    def execute(self, context):
        import os
        scene = context.scene
        folder = scene.bprs_download_folder

        if not os.path.isdir(folder):
            self.report({'WARNING'}, "The specified folder is not valid")   # 有効なフォルダではありません 
            return {'CANCELLED'}

        # 設定ファイルに保存
        save_settings({"download_folder": folder})
        # save_download_folder(folder)
        self.report({'INFO'}, _("Download folder setting has been saved"))      # DLフォルダ設定が保存されました

        # 候補リスト初期化
        scene.bprs_update_candidates.clear()
        files = os.listdir(folder)
        for fname in sorted(files, reverse=True):
            # if fname.startswith("DIVA_BonePositionRotationScale") and fname.endswith(".zip"):
            if re.match(r"^DIVA_BonePositionRotationScale.*\.zip$", fname, re.IGNORECASE):
                full_path = os.path.join(folder, fname)
                timestamp = os.path.getmtime(full_path)
                import datetime
                date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
                item = scene.bprs_update_candidates.add()
                item.name = fname
                item.path = full_path
                item.date = date

        return {'FINISHED'}

class BPRS_OT_SortCandidatesByName(bpy.types.Operator):
    """ZIPファイル名ソート(A–Z / Z–A)"""
    bl_idname = "bprs.sort_candidates_name"
    bl_label = "Sort by File Name"
    bl_description = _("Sort update files by file name. Click again to toggle order")

    def execute(self, context):
        scene = context.scene
        items = [(i.name, i.path, i.date) for i in scene.bprs_update_candidates]
        scene.bprs_update_candidates.clear()

        reverse = scene.bprs_sort_name_desc
        for name, path, date in sorted(items, key=lambda x: x[0].lower(), reverse=reverse):
            item = scene.bprs_update_candidates.add()
            item.name, item.path, item.date = name, path, date

        scene.bprs_sort_name_desc = not scene.bprs_sort_name_desc  # トグル切替
        return {'FINISHED'}

class BPRS_OT_SortCandidatesByDate(bpy.types.Operator):
    """日時順ソート(newest ↔ oldest)"""
    bl_idname = "bprs.sort_candidates_date"
    bl_label = "Sort by Update Date"
    bl_description = _("Sort update files by update/download date. Click again to toggle order")

    def execute(self, context):
        scene = context.scene
        items = [(i.name, i.path, i.date) for i in scene.bprs_update_candidates]
        scene.bprs_update_candidates.clear()

        reverse = scene.bprs_sort_date_desc
        for name, path, date in sorted(items, key=lambda x: x[2], reverse=reverse):
            item = scene.bprs_update_candidates.add()
            item.name, item.path, item.date = name, path, date

        scene.bprs_sort_date_desc = not scene.bprs_sort_date_desc  # トグル切替
        return {'FINISHED'}


def get_classes():
    return [
        BPRS_AddonPreferences,
        BPRS_OT_OpenURL,
        BPRS_OT_ExecuteUpdate,
        BPRS_OT_OpenAddonFolder,
        BPRS_OT_ConfirmDownloadFolder,
        BPRS_UpdateCandidateItem,
        BPRS_UL_UpdateCandidateList,
        BPRS_OT_SortCandidatesByName,
        BPRS_OT_SortCandidatesByDate,
    ]

def register_properties():
    # ダウンロードフォルダの初期値を設定ファイルから読み込む
    bpy.types.Scene.bprs_download_folder = bpy.props.StringProperty(
        name="Download Folder",
        description=_("Specify the folder where the update ZIP is stored"),
        subtype='DIR_PATH',
        default=load_download_folder()
    )

    # 更新候補リスト（CollectionProperty + IntProperty）
    bpy.types.Scene.bprs_update_candidates = bpy.props.CollectionProperty(
        type=BPRS_UpdateCandidateItem
    )
    bpy.types.Scene.bprs_selected_candidate_index = bpy.props.IntProperty(
        name="Selected index in candidate list",        # 候補リスト選択インデックス
        default=-1
    )

    # 更新完了フラグ（INFOラベル表示の制御に使用）
    bpy.types.WindowManager.bprs_update_completed = bpy.props.BoolProperty(
        name="Update completed flag",      # 更新完了フラグ
        default=False
    )
    
    # 名前順ソートトグル式
    bpy.types.Scene.bprs_sort_name_desc = bpy.props.BoolProperty(default=False)
    # 日時順ソートトグル式
    bpy.types.Scene.bprs_sort_date_desc = bpy.props.BoolProperty(default=True)

    # 不要ファイル削除要フラグ
    bpy.types.WindowManager.bprs_obsolete_cleanup_done = bpy.props.BoolProperty(
        name="Obsolete cleanup done",
        default=False
    )

    # GitHubリリース確認
    bpy.types.WindowManager.bprs_new_release_available = bpy.props.BoolProperty(
        name="New Release Available",
        description="True if a newer GitHub release is available",
        default=False
    )

    bpy.types.WindowManager.bprs_initialized = bpy.props.BoolProperty(
        name="Whether initialized or not",
        default=False   # 初期化未実行（True=初期化済み、以降はスキップ）
    )


def unregister_properties():
    del bpy.types.Scene.bprs_download_folder
    del bpy.types.Scene.bprs_update_candidates
    del bpy.types.Scene.bprs_selected_candidate_index
    del bpy.types.WindowManager.bprs_update_completed
    del bpy.types.Scene.bprs_sort_name_desc
    del bpy.types.Scene.bprs_sort_date_desc
    del bpy.types.WindowManager.bprs_obsolete_cleanup_done
    del bpy.types.WindowManager.bprs_new_release_available
    del bpy.types.WindowManager.bprs_initialized