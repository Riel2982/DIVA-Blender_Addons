# bprs_ui_export.py

import bpy
import os
import sys
import time
import json
import subprocess
from bpy.app.translations import pgettext as _

from . import DivaBonePositionRotationScale
from . bprs_export import get_timestamp, rename_existing_file, convert_bone_data_to_json

from .bprs_debug import DEBUG_MODE   # デバッグ用

# --- セクション 1: ボーンデータ出力 ------------------------------------------
def draw_export_ui(layout, context, scene):
    box = layout.box()  # 枠付きセクションを作る
    row = box.row(align=True)
    row.prop(scene, "bprs_show_export_tools", text="", icon='DOWNARROW_HLT' if scene.bprs_show_export_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Bone Data Exporter", icon="EXPORT") # セクションタイトル

    if scene.bprs_show_export_tools:
        # ファイル名（ラベル20%）
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text="File Name")
        split.prop(scene, "bprs_export_filename", text="")

        # 出力パス（ラベル20%）
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text="Export Path")
        row_sub = split.row(align=True)
        row_sub.prop(scene, "bprs_export_filepath", text="")
        row_sub.operator("bprs.export_select_folder", text="", icon='FILE_FOLDER')

        
        # チェックボックスを左側に配置
        row = box.row()
        row.prop(scene, "bprs_export_auto_open", text="")  # チェックボックス
        row.label(text="Auto Open File")  # ラベル

        row = box.row()
        row.prop(scene, "bprs_export_overwrite", text="")  # チェックボックス
        row.label(text="Overwrite Existing File")  # ラベル

        row = box.row()
        row.prop(scene, "bprs_export_format_json", text="")  # チェックボックス
        row.label(text="Export as JSON")  # ラベル

        box.operator("bprs.export_bone_data", text="Export Bone Data", icon='EXPORT')


if False:
    # タイムスタンプを付与する関数
    def get_timestamp():
        return time.strftime("%Y%m%d_%H%M%S")

    # ファイル名をチェックしてリネームする関数（上書きするかどうかをチェック）
    def rename_existing_file(filepath, overwrite):
        if os.path.exists(filepath):
            if overwrite:
                return None  # 上書きモードの場合、リネームせずそのまま使用
            else:
                file_dir, file_name = os.path.split(filepath)
                file_base, file_ext = os.path.splitext(file_name)
                new_name = f"{file_base}_{get_timestamp()}{file_ext}"
                new_filepath = os.path.join(file_dir, new_name)
                os.rename(filepath, new_filepath)
                return new_filepath
        return None



# フォルダ選択オペレーター
class BPRS_OT_SelectFolder(bpy.types.Operator):
    """フォルダ選択ダイアログを開く"""
    bl_idname = "bprs.export_select_folder"
    bl_label = "Select Folder"
    bl_description = _("Open folder selection dialog")
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        # 保存先が未設定なら、現在の .blend ファイルのフォルダをセット

        if not self.filepath:
            self.filepath = bpy.path.abspath("//")  # .blend のフォルダのみを設定
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        selected_path = bpy.path.abspath(self.filepath)

        # `.blend` ファイル名を含まないフォルダパスに変換
        if os.path.isdir(selected_path):  # フォルダ選択ならそのまま使用
            scene.bprs_export_filepath = selected_path
        else:  # ファイル名付きならディレクトリ部分のみを抽出
            scene.bprs_export_filepath = os.path.dirname(selected_path)

        self.report({'INFO'}, _("Selected folder: {path}").format(path=scene.bprs_export_filepath))
        return {'FINISHED'}


# エクスポートオペレーター
class BPRS_OT_ExportBoneData(bpy.types.Operator):
    """アーマチュアを選択した状態でボーンデータを取得しファイルに出力"""
    bl_idname = "bprs.export_bone_data"
    bl_label = "Export Bone Data"
    bl_description = _("Retrieve bone data from the selected armature and export to file")

    def execute(self, context):
        scene = context.scene

        # `.blend` ファイルのフォルダ取得（作業ファイルの保存場所）
        blend_folder = bpy.path.abspath("//").strip()
        blend_file_exists = bpy.data.filepath != ""  # `.blend` ファイルが保存されているかチェック

        # 保存先の取得（ユーザー入力値を取得し、空白を除去）
        folder_path = bpy.path.abspath(scene.bprs_export_filepath).strip()

        # **フォルダパスのバリデーション（適正チェック）**
        def is_valid_path(path):
            return path and os.path.exists(path) and os.path.isdir(path) and os.access(path, os.W_OK)  # 書き込み可能かチェック

        # **保存先が空欄 & `.blend` ファイルが存在する場合** → `.blend` のフォルダを使用（意図した動作）
        if not folder_path and blend_file_exists:
            folder_path = blend_folder

        # **保存先が無効な場合はエラーを表示し、処理を中止**
        if not is_valid_path(folder_path):
            self.report({'WARNING'}, _("Invalid destination folder. Please select a proper directory"))
            return {'CANCELLED'}

        # **Blenderの実行フォルダへの誤保存を防止**
        blender_executable_path = os.path.dirname(sys.executable)
        if folder_path.lower().startswith(blender_executable_path.lower()):
            self.report({'WARNING'}, _("Cannot save to Blender’s installation folder. Please choose another location"))
            return {'CANCELLED'}

        # **ファイル名の取得 & 補正**
        file_base_name = scene.bprs_export_filename.strip() or "bone_data"
        file_ext = ".json" if scene.bprs_export_format_json else ".txt"
        filepath = os.path.join(folder_path, f"{file_base_name}{file_ext}")

        # **フォルダが存在しない場合は処理を中止**
        if not os.path.exists(folder_path):
            self.report({'WARNING'}, ("The selected folder does not exist. Please choose a valid directory"))
            return {'CANCELLED'}

        # **上書き確認＆リネーム処理**
        renamed_file = rename_existing_file(filepath, scene.bprs_export_overwrite)
        if renamed_file:
            if DEBUG_MODE:
                print(_("Existing file renamed to: {name}").format(name=renamed_file))

        try:
            bone_data = DivaBonePositionRotationScale.get_bone_data()
            if not bone_data:
                self.report({'WARNING'}, _("No armature selected"))
                return {'CANCELLED'}

            '''
            # **JSON変換処理**
            if scene.bprs_export_format_json:
                bone_data_json = [
                    {
                        "Signature": "OSG",
                        "Name": parts[0].strip(),
                        "ParentName": parts[1].split(":")[-1].strip(),
                        "Position": parts[2].split(":")[-1].strip(),
                        "Rotation": parts[3].split(":")[-1].strip(),
                        "Scale": parts[4].split(":")[-1].strip()
                    }
                    for line in bone_data.split("\n\n")
                    for parts in [line.split("\n")]
                    if len(parts) >= 5
                ]

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(bone_data_json, f, indent=4)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(bone_data)
            '''
            # **JSON変換処理**
            if scene.bprs_export_format_json:
                bone_data_json = convert_bone_data_to_json(bone_data)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(bone_data_json, f, indent=4)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(bone_data)

            self.report({'INFO'}, _("Bone data exported to: {path}").format(path=filepath))

            # **自動でファイルを開く処理**
            if scene.bprs_export_auto_open:
                if sys.platform.startswith("win"):
                    os.startfile(filepath)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", filepath])
                else:
                    subprocess.Popen(["xdg-open", filepath])

        except Exception as e:
            self.report({'WARNING'}, _("Failed to export: {error}").format(error=str(e)))
            return {'CANCELLED'}

        return {'FINISHED'}
    

# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        BPRS_OT_SelectFolder,
        BPRS_OT_ExportBoneData,
    ]


