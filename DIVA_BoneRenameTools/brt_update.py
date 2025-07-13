# brt_update.py

import bpy
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

    # 成功時だけ表示する INFOラベル
    if getattr(scene, "brt_update_completed", False):
        box.label(text="更新が完了しました。Blenderを再起動してください", icon="INFO")



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
    

class BRT_OT_ExecuteUpdate(bpy.types.Operator):
    """更新ファイルをインストール"""
    bl_idname = "brt.execute_update"
    bl_label = _("Install Update File")
    bl_description = _("Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update")
    bl_options = {'UNDO'}

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

    def invoke(self, context, event):
        # ZIPファイル選択ダイアログを開く
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

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
        import zipfile, shutil, os, re

        # ZIPファイル名の確認（パターンに一致しなければ処理中止）
        filename = os.path.basename(self.filepath)
        pattern = re.compile(r"^DIVA_BoneRenameTools.*\.zip$")
        if not pattern.match(filename):
            self.report({'WARNING'}, _("DIVA_BoneRenameTools で始まるZIPファイル以外は処理できません"))
            context.scene.brt_update_completed = False
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
                context.scene.brt_update_completed = False
                return {'CANCELLED'}

            source_name = self.read_bl_info_name(source_init)
            if not source_name:
                self.report({'WARNING'}, _("ZIP内の bl_info.name を取得できません"))
                shutil.rmtree(extract_path)
                context.scene.brt_update_completed = False
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
                    context.scene.brt_update_completed = False
                    return {'CANCELLED'}

                # 選ばれたフォルダに __init__.py があるか確認
                manual_init = os.path.join(self.dirpath, "__init__.py")
                if not os.path.isfile(manual_init):
                    self.report({'WARNING'}, _("選択されたフォルダに __init__.py が見つかりません"))
                    shutil.rmtree(extract_path)
                    context.scene.brt_update_completed = False
                    return {'CANCELLED'}

                manual_name = self.read_bl_info_name(manual_init)
                if manual_name != source_name:
                    self.report({'WARNING'}, _("bl_info.name が一致しないため、更新できません"))
                    shutil.rmtree(extract_path)
                    context.scene.brt_update_completed = False
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
            context.scene.brt_update_completed = True
            return context.window_manager.invoke_popup(self, width=400)

        except Exception as e:  # 例外発生時のエラー通知とクリーンアップ
            self.report({'ERROR'}, _("更新に失敗しました: {error}").format(error=str(e)))
            shutil.rmtree(extract_path, ignore_errors=True)
            context.scene.brt_update_completed = False
            return {'CANCELLED'}

    # 更新完了時のポップアップ表示内容
    def draw(self, context):
        layout = self.layout
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


def get_classes():
    return [
        BRT_OT_OpenURL,
        BRT_OT_ExecuteUpdate,
        BRT_OT_OpenAddonFolder,
    ]

def register_properties():
    bpy.types.Scene.brt_update_completed = bpy.props.BoolProperty(default=False)

def unregister_properties():
    del bpy.types.Scene.brt_update_completed
