bl_info = {
    "name": "DIVA - Bone Data Exporter",
    "author": "Saltlapse, Riel",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "Nパネル > DIVA",
    "description": "DIVA-CustomRig",
    "category": "Rigging",
}

import bpy
import os
import sys
import time
import json
import subprocess

from . import DivaBonePositionRotationScale

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

# カスタムプロパティ（ファイル名＆保存先＆自動オープン＆上書き制御）
bpy.types.Scene.bone_export_filename = bpy.props.StringProperty(
    name="File Name",
    description="保存するファイル名（拡張子なし）",
    default="bone_data"
)
bpy.types.Scene.bone_export_filepath = bpy.props.StringProperty(
    name="Export Path",
    description="保存先フォルダ",
    default=""
)
bpy.types.Scene.bone_export_auto_open = bpy.props.BoolProperty(
    name="Auto Open File",
    description="エクスポート後に自動でファイルを開く",
    default=False
)
bpy.types.Scene.bone_export_overwrite = bpy.props.BoolProperty(
    name="Overwrite Existing File",
    description="既存ファイルを上書きする（OFFならリネーム）",
    default=True
)
bpy.types.Scene.bone_export_format_json = bpy.props.BoolProperty(
    name="Export as JSON",
    description="JSON形式で保存する（チェックなしならTXT）",
    default=False
)

# フォルダ選択オペレーター
class SelectFolderOperator(bpy.types.Operator):
    """フォルダ選択ダイアログを開く"""
    bl_idname = "export.select_folder"
    bl_label = "Select Folder"
    
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
            scene.bone_export_filepath = selected_path
        else:  # ファイル名付きならディレクトリ部分のみを抽出
            scene.bone_export_filepath = os.path.dirname(selected_path)

        self.report({'INFO'}, f"Selected folder: {scene.bone_export_filepath}")
        return {'FINISHED'}

# エクスポートオペレーター
class ExportBoneDataOperator(bpy.types.Operator):
    """アーマチュアを選択した状態でボーンデータを取得しファイルに出力"""
    bl_idname = "export.bone_data"
    bl_label = "Export Bone Data"

    def execute(self, context):
        scene = context.scene

        # `.blend` ファイルのフォルダ取得（作業ファイルの保存場所）
        blend_folder = bpy.path.abspath("//").strip()
        blend_file_exists = bpy.data.filepath != ""  # `.blend` ファイルが保存されているかチェック

        # 保存先の取得（ユーザー入力値を取得し、空白を除去）
        folder_path = bpy.path.abspath(scene.bone_export_filepath).strip()

        # **フォルダパスのバリデーション（適正チェック）**
        def is_valid_path(path):
            return path and os.path.exists(path) and os.path.isdir(path) and os.access(path, os.W_OK)  # 書き込み可能かチェック

        # **保存先が空欄 & `.blend` ファイルが存在する場合** → `.blend` のフォルダを使用（意図した動作）
        if not folder_path and blend_file_exists:
            folder_path = blend_folder

        # **保存先が無効な場合はエラーを表示し、処理を中止**
        if not is_valid_path(folder_path):
            self.report({'ERROR'}, "保存先のフォルダが無効です。適切なフォルダを選択してください。")
            return {'CANCELLED'}

        # **Blenderの実行フォルダへの誤保存を防止**
        blender_executable_path = os.path.dirname(sys.executable)
        if folder_path.lower().startswith(blender_executable_path.lower()):
            self.report({'ERROR'}, "Blenderの実行フォルダには保存できません。別の場所を指定してください。")
            return {'CANCELLED'}

        # **ファイル名の取得 & 補正**
        file_base_name = scene.bone_export_filename.strip() or "bone_data"
        file_ext = ".json" if scene.bone_export_format_json else ".txt"
        filepath = os.path.join(folder_path, f"{file_base_name}{file_ext}")

        # **フォルダが存在しない場合は処理を中止**
        if not os.path.exists(folder_path):
            self.report({'ERROR'}, "指定されたフォルダが存在しません。正しいフォルダを選択してください。")
            return {'CANCELLED'}

        # **上書き確認＆リネーム処理**
        renamed_file = rename_existing_file(filepath, scene.bone_export_overwrite)
        if renamed_file:
            print(f"Existing file renamed to: {renamed_file}")

        try:
            bone_data = DivaBonePositionRotationScale.get_bone_data()
            if not bone_data:
                self.report({'WARNING'}, "アーマチュアを選択してください（No armature selected.）")
                return {'CANCELLED'}

            # **JSON変換処理**
            if scene.bone_export_format_json:
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

            self.report({'INFO'}, f"Bone data exported to: {filepath}")

            # **自動でファイルを開く処理**
            if scene.bone_export_auto_open:
                if sys.platform.startswith("win"):
                    os.startfile(filepath)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", filepath])
                else:
                    subprocess.Popen(["xdg-open", filepath])

        except Exception as e:
            self.report({'ERROR'}, f"エクスポートに失敗しました（Failed to export: {str(e)}）")
            return {'CANCELLED'}

        return {'FINISHED'}

# NパネルのUI
class BoneDataExporterPanel(bpy.types.Panel):
    """NパネルのUI"""
    bl_label = "Bone Data Exporter"
    bl_idname = "DIVA_PT_bone_data_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DIVA"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "bone_export_filename")
        row = layout.row()
        row.prop(scene, "bone_export_filepath", text="Export Path")
        row.operator("export.select_folder", text="", icon='FILE_FOLDER')

        # チェックボックスを左側に配置
        row = layout.row()
        row.prop(scene, "bone_export_auto_open", text="")  # チェックボックス
        row.label(text="Auto Open File")  # ラベル

        row = layout.row()
        row.prop(scene, "bone_export_overwrite", text="")  # チェックボックス
        row.label(text="Overwrite Existing File")  # ラベル

        row = layout.row()
        row.prop(scene, "bone_export_format_json", text="")  # チェックボックス
        row.label(text="Export as JSON")  # ラベル

        layout.operator("export.bone_data", text="Export Bone Data")

# 登録・解除
def register():
    bpy.utils.register_class(BoneDataExporterPanel)
    bpy.utils.register_class(ExportBoneDataOperator)
    bpy.utils.register_class(SelectFolderOperator)

def unregister():
    bpy.utils.unregister_class(BoneDataExporterPanel)
    bpy.utils.unregister_class(ExportBoneDataOperator)
    bpy.utils.unregister_class(SelectFolderOperator)

if __name__ == "__main__":
    register()
