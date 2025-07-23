# brt_update.py

import bpy
import os
import json
import zipfile
import shutil
import re
import datetime
from bpy.app.handlers import persistent
from bpy.app.translations import pgettext as _

# --- アドオン更新UI -------------------------------------
def draw_update_ui(layout, scene):
    box = layout.box()
    # box.label(text=_("アップデート"), icon='FILE_REFRESH')

    row = box.row()  # ← 横一列に並べる
    op1 = row.operator("brt.open_url", text=_("更新を確認"), icon="CHECKMARK") 
    op1.url = "https://github.com/Riel2982/DIVA-Blender_Addons/releases"

    row.operator("brt.execute_update", text=_("インストール"), icon="IMPORT") 
    row.operator("brt.open_addon_folder", text=_("アドオンフォルダを開く"), icon="FILE_FOLDER") 

    # ダウンロード先パスのラベル＋操作群をまとめて一行に並べる
    row = box.row()
    row.prop(scene, "brt_download_folder", text="ZIP保存先フォルダパス")  # テキスト入力欄（ラベルなし）

    # 成功時だけ表示する INFOラベル
    wm = bpy.context.window_manager
    if getattr(wm, "brt_update_completed", False):
        box.label(text=_("更新が完了しました。Blenderを再起動してください"), icon="INFO")

    # 非実行時・失敗時に表示する 更新ファイルリスト
    else:
        row = box.row()
        row.label(text=_("更新ファイル一覧: "), icon='PRESET')
        row.operator("brt.sort_candidates_name", text="", icon="SORTALPHA")     # 名前順
        row.operator("brt.sort_candidates_date", text="", icon="SORTTIME")      # 日付順
        row.operator("brt.confirm_download_folder", text="", icon="FILE_REFRESH")  # リスト更新

        box.template_list(
            "BRT_UL_UpdateCandidateList", "",
            scene, "brt_update_candidates",
            scene, "brt_selected_candidate_index",
            rows=2      # 初期行数
        )


# --- プロパティグループ＆UIリスト -------------------------------------
class BRT_UpdateCandidateItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    date: bpy.props.StringProperty()

class BRT_UL_UpdateCandidateList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # 行を分割して領域比率を調整
        split = layout.split(factor=0.75, align=True)
        split.label(text=item.name)   # 左側（75%）：ファイル名
        split.label(text=item.date)   # 右側（25%）：日時

# 設定ファイル関連の関数 -------------------------------------
def get_addon_folder():
    return os.path.dirname(os.path.abspath(__file__))

def get_settings_path():
    return os.path.join(get_addon_folder(), "brt_settings.json")

# 設定ファイルの生成・保存
def save_download_folder(path):
    try:        # w=存在しない場合は生成
        with open(get_settings_path(), "w", encoding="utf-8") as f:
            json.dump({"download_folder": path}, f)
        print("✅ 設定ファイルを保存しました:", get_settings_path())
    except Exception as e:
        print("❌ 保存失敗:", str(e))

def load_download_folder():
    try:
        with open(get_settings_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("download_folder", "")
    except Exception:
        return ""


# 各種オペレーター
class BRT_OT_OpenURL(bpy.types.Operator):
    """更新を確認"""
    bl_idname = "brt.open_url"
    bl_label = _("Check for Updates")
    bl_description = _("Opens the GitHub release page to check for update files")

    url: bpy.props.StringProperty()

    def execute(self, context):
        import webbrowser
        webbrowser.open(self.url)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # ZIPファイル選択ダイアログを開く
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class BRT_OT_ExecuteUpdate(bpy.types.Operator):
    """更新ファイルをインストール"""
    bl_idname = "brt.execute_update"
    bl_label = _("Install Update File")
    bl_description = _("Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update")
    # bl_options = {'UNDO'}

    filepath: bpy.props.StringProperty(
        name=_("Select ZIP File"),
        description=_("Choose a ZIP file starting with DIVA_BoneRenameTools"),
        #　filter_glob='*.zip'      # 4.2以降ファイルパスが取得できない原因
    )

    # ユーザーにフォルダ選択してもらうためのプロパティ（手動選択時のみ使用）
    dirpath: bpy.props.StringProperty(
        name=("Select Addon Folder"),
        description=_("Choose the folder where the addon is installed"),
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
            index = context.scene.brt_selected_candidate_index
            candidates = context.scene.brt_update_candidates
            if 0 <= index < len(candidates):
                self.filepath = candidates[index].path

            # それでも filepath が空なら → ダイアログで選択させるべき
            if not self.filepath:
                self.report({'INFO'}, _("ZIPファイルが選択されていません。ファイルを指定してください"))
                context.window_manager.fileselect_add(self)
                return {'RUNNING_MODAL'}

        # ZIPファイル名の確認（パターンに一致しなければ処理中止）
        filename = os.path.basename(self.filepath)
        pattern = re.compile(r"^DIVA_BoneRenameTools.*\.zip$")
        if not pattern.match(filename):
            self.report({'WARNING'}, _("DIVA_BoneRenameTools で始まるZIPファイル以外は処理できません"))
            context.window_manager.brt_update_completed = False
            return {'CANCELLED'}

        # 一時解凍フォルダの作成
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        extract_path = os.path.join(downloads_path, "_brt_temp_extract")
        os.makedirs(extract_path, exist_ok=True)

        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # ZIP内のbl_info['name']を取得
            source_folder = os.path.join(extract_path, "DIVA_BoneRenameTools")
            source_init = os.path.join(source_folder, "__init__.py")
            if not os.path.isdir(source_folder) or not os.path.isfile(source_init):
                self.report({'WARNING'}, _("ZIP内に DIVA_BoneRenameTools フォルダまたは __init__.py が見つかりません"))
                shutil.rmtree(extract_path)
                context.window_manager.brt_update_completed = False
                return {'CANCELLED'}

            source_name = self.read_bl_info_name(source_init)
            if not source_name:
                self.report({'WARNING'}, _("ZIP内の bl_info.name を取得できません"))
                shutil.rmtree(extract_path)
                context.window_manager.brt_update_completed = False
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
                    self.report({'INFO'}, _("インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください"))
                    context.window_manager.fileselect_add(self)  # DIR選択を促す
                    return {'RUNNING_MODAL'}

                # DIR選択後：キャンセルされた場合は中止＋後始末
                if not self.dirpath:
                    self.report({'INFO'}, _("インストールはキャンセルされました"))
                    shutil.rmtree(extract_path, ignore_errors=True)     # 一時フォルダの削除
                    context.window_manager.brt_update_completed = False
                    return {'CANCELLED'}

                # 選ばれたフォルダに __init__.py があるか確認
                manual_init = os.path.join(self.dirpath, "__init__.py")
                if not os.path.isfile(manual_init):
                    self.report({'WARNING'}, _("選択されたフォルダに __init__.py が見つかりません"))
                    shutil.rmtree(extract_path)
                    context.window_manager.brt_update_completed = False
                    return {'CANCELLED'}

                manual_name = self.read_bl_info_name(manual_init)
                if manual_name != source_name:
                    self.report({'WARNING'}, _("bl_info.name が一致しないため、更新できません"))
                    shutil.rmtree(extract_path)
                    context.window_manager.brt_update_completed = False
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
            # 更新完了ポップアップ表示
            self.report({'INFO'}, _("更新が完了しました。Blenderを再起動してください"))
            context.window_manager.brt_update_completed = True
            return context.window_manager.invoke_popup(self, width=400)

        except Exception as e:  # 例外発生時のエラー通知とクリーンアップ
            self.report({'ERROR'}, _("更新に失敗しました: {error}").format(error=str(e)))
            shutil.rmtree(extract_path, ignore_errors=True)
            context.window_manager.brt_update_completed = False
            return {'CANCELLED'}

    # 更新完了時のポップアップ表示内容
    def draw(self, context):
        layout = self.layout
        # layout.label(text=_("ZIPファイルを選択してください"), icon='INFO')
        layout.label(text=_("更新後はBlenderを再起動してください"), icon='INFO')

        
class BRT_OT_OpenAddonFolder(bpy.types.Operator):
    """現在のアドオンフォルダを開く"""
    bl_idname = "brt.open_addon_folder"
    bl_label = _("Open Addon Folder")
    bl_description = _("Opens the folder where this addon is installed")

    def execute(self, context):
        import os
        import subprocess

        # 実行中のアドオンフォルダを取得
        self_folder = os.path.dirname(os.path.abspath(__file__))

        # Windowsのエクスプローラーでフォルダを開く
        subprocess.Popen(f'explorer "{self_folder}"')

        return {'FINISHED'}

class BRT_OT_ConfirmDownloadFolder(bpy.types.Operator):
    """更新ファイルリスト更新"""
    bl_idname = "brt.confirm_download_folder"
    bl_label = _("Confirm Download Folder")
    bl_description = _("Scan the folder and list update candidate files")

    def execute(self, context):
        import os
        scene = context.scene
        folder = scene.brt_download_folder

        if not os.path.isdir(folder):
            self.report({'WARNING'}, "有効なフォルダではありません")
            return {'CANCELLED'}

        # 設定ファイルに保存
        save_download_folder(folder)
        self.report({'INFO'}, _("DLフォルダ設定が保存されました"))

        # 候補リスト初期化
        scene.brt_update_candidates.clear()
        files = os.listdir(folder)
        for fname in sorted(files, reverse=True):
            if fname.startswith("DIVA_BoneRenameTools") and fname.endswith(".zip"):
                full_path = os.path.join(folder, fname)
                timestamp = os.path.getmtime(full_path)
                import datetime
                date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
                item = scene.brt_update_candidates.add()
                item.name = fname
                item.path = full_path
                item.date = date

        return {'FINISHED'}

class BRT_OT_SortCandidatesByName(bpy.types.Operator):
    """ZIPファイル名ソート(A–Z / Z–A)"""
    bl_idname = "brt.sort_candidates_name"
    bl_label = _("Sort by File Name")
    bl_description = _("Sort update files by file name. Click again to toggle order.")

    def execute(self, context):
        scene = context.scene
        items = [(i.name, i.path, i.date) for i in scene.brt_update_candidates]
        scene.brt_update_candidates.clear()

        reverse = scene.brt_sort_name_desc
        for name, path, date in sorted(items, key=lambda x: x[0].lower(), reverse=reverse):
            item = scene.brt_update_candidates.add()
            item.name, item.path, item.date = name, path, date

        scene.brt_sort_name_desc = not scene.brt_sort_name_desc  # トグル切替
        return {'FINISHED'}

class BRT_OT_SortCandidatesByDate(bpy.types.Operator):
    """日時順ソート(newest ↔ oldest)"""
    bl_idname = "brt.sort_candidates_date"
    bl_label = _("Sort by Update Date")
    bl_description = _("Sort update files by update/download date. Click again to toggle order.")

    def execute(self, context):
        scene = context.scene
        items = [(i.name, i.path, i.date) for i in scene.brt_update_candidates]
        scene.brt_update_candidates.clear()

        reverse = scene.brt_sort_date_desc
        for name, path, date in sorted(items, key=lambda x: x[2], reverse=reverse):
            item = scene.brt_update_candidates.add()
            item.name, item.path, item.date = name, path, date

        scene.brt_sort_date_desc = not scene.brt_sort_date_desc  # トグル切替
        return {'FINISHED'}

def get_classes():
    return [
        BRT_OT_OpenURL,
        BRT_OT_ExecuteUpdate,
        BRT_OT_OpenAddonFolder,
        BRT_OT_ConfirmDownloadFolder,
        BRT_UpdateCandidateItem,
        BRT_UL_UpdateCandidateList,
        BRT_OT_SortCandidatesByName,
        BRT_OT_SortCandidatesByDate,
    ]

def register_properties():
    # ダウンロードフォルダの初期値を設定ファイルから読み込む
    bpy.types.Scene.brt_download_folder = bpy.props.StringProperty(
        name=_("ダウンロードフォルダ"),
        description=_("更新用ZIPが保存されているフォルダを指定してください"),
        subtype='DIR_PATH',
        default=load_download_folder()
    )

    # 更新候補リスト（CollectionProperty + IntProperty）
    bpy.types.Scene.brt_update_candidates = bpy.props.CollectionProperty(
        type=BRT_UpdateCandidateItem
    )
    bpy.types.Scene.brt_selected_candidate_index = bpy.props.IntProperty(
        name=_("候補リスト選択インデックス"),
        default=-1
    )

    # 更新完了フラグ（INFOラベル表示の制御に使用）
    bpy.types.WindowManager.brt_update_completed = bpy.props.BoolProperty(
        name=_("更新完了フラグ"),
        default=False
    )
    
    # 名前順ソートトグル式
    bpy.types.Scene.brt_sort_name_desc = bpy.props.BoolProperty(default=False)
    # 日時順ソートトグル式
    bpy.types.Scene.brt_sort_date_desc = bpy.props.BoolProperty(default=True)

def unregister_properties():
    del bpy.types.Scene.brt_download_folder
    del bpy.types.Scene.brt_update_candidates
    del bpy.types.Scene.brt_selected_candidate_index
    del bpy.types.WindowManager.brt_update_completed
    del bpy.types.Scene.brt_sort_name_desc
    del bpy.types.Scene.brt_sort_date_desc

# アドオン起動直後に呼ばれる初期処理
def initialize_candidate_list():
    # 更新完了フラグをリセット（前回の更新完了表示が残っていたら消す）
    wm = bpy.context.window_manager
    wm.brt_update_completed = False

    # 「有効なDLフォルダが設定されている場合のみ更新リストを自動生成する」  
    scene = bpy.context.scene   # Scene からDLフォルダパスを取得（プロパティが未登録なら中止）
    if not hasattr(scene, "brt_download_folder"):
        return  # DLフォルダプロパティがない → 以降の処理はスキップ
    
    folder = scene.brt_download_folder# 有効なパスかチェック
    if folder and os.path.isdir(folder):
        bpy.ops.brt.confirm_download_folder('INVOKE_DEFAULT')   # フォルダが有効なら、リスト更新オペレーターを呼び出す
