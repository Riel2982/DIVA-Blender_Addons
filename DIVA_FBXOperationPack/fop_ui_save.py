# fop_ui_save.py


import bpy
import os
import sys
import time
import json
import subprocess
from bpy.types import UIList
from bpy.props import IntProperty
# import self
from bpy.app.translations import pgettext as _

from .fop_save import (
    get_safe_blend_save_path,
    # make_paths_relative_safely,
    # make_paths_absolute_safely,
    unpack_external_data_safely,
)

from .fop_debug import DEBUG_MODE   # デバッグ用

#  --- Blendファイル保存セクション --- ------------------------------------------
def draw_save_ui(layout, self, context, scene):
    settings = scene.fop_settings
    box = layout.box()  # 枠付きセクションを作る
    row = box.row(align=True)
    row.prop(scene, "fop_show_save_tools", text="", icon='DOWNARROW_HLT' if scene.fop_show_save_tools else 'RIGHTARROW', emboss=False)
    row.label(text="Blend File Saver", icon="FILE_BACKUP") # セクションタイトル

    if scene.fop_show_save_tools:
        row = box.row()

        # 保存名入力欄
        # row = box.row()
        split = row.split(factor=0.2)
        split.label(text=_("File Name :"))
        split.prop(scene, "fop_blend_save_filename", text="")

        # 保存先フォルダ選択
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text=_("Save Path :"))
        row = split.row(align=True)        
        row.prop(scene, "fop_blend_save_path", text="")
        row.operator("fop.select_blend_save_folder", text="", icon='FILE_FOLDER')

        # リソースの自動パック
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text=_("External Data :"))
        row = split.row(align=True)        
        row.prop(settings, "external_data", text="")
        # row.prop(settings, "external_data", text=_("External Data :")) 
        row.separator()
        row.separator()
        row.prop(settings, "pack_resources", text="")
        row.label(text=_("Pack Resources"))

        # 上書き防止
        row = box.row()
        row.prop(settings, "blendfile_overwrite_guard", text="")
        row.label(text=_("Auto Numbering"))

        
        # 保存ボタン
        box.operator("fop.save_blend_file", text="Save Blend File", icon='FILE_BACKUP')  # または'BLENDER'






# Blendファイル系 --------------------------------------------------------------------------------------
# BLENDファイル保存場所を選択
class FOP_OT_SelectBlendSaveFolder(bpy.types.Operator):
    bl_idname = "fop.select_blend_save_folder"
    bl_label = "Select Blend Save Folder"
    bl_description = _("Open dialog to select blend file save location")

    # Blendフォルダ選択用
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        # 既定の開始位置を .blend フォルダに
        if bpy.data.filepath:
            self.directory = bpy.path.abspath("//")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        scene.fop_blend_save_path = bpy.path.abspath(self.directory)
        self.report({'INFO'}, _("Save location has been set"))
        return {'FINISHED'}
    


# BLENDファイルを保存
class FOP_OT_SaveBlendFile(bpy.types.Operator):
    bl_idname = "fop.save_blend_file"
    bl_label = "Save Blend File"
    bl_description = _("Save blend file")

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        # invokeから実行される場合は即executeへ
        return self.execute(context)

    def execute(self, context):
        scene = context.scene
        settings = context.scene.fop_settings

        if False:
            # 自動取得（ファイル保存パス）
            if not scene.fop_blend_save_path and bpy.data.filepath:
                scene.fop_blend_save_path = os.path.dirname(bpy.path.abspath(bpy.data.filepath))

        folder = scene.fop_blend_save_path or bpy.path.abspath(self.directory)

        if False:
            # ファイル名の自動反映
            if bpy.data.filepath:
                scene.fop_blend_save_filename = os.path.basename(bpy.data.filepath)
            else:
                scene.fop_blend_save_filename = "untitled"

            if DEBUG_MODE:
                print("[FOP] SaveBlendFile → folder:", folder)
                print("[FOP] SaveBlendFile → filename:", scene.fop_blend_save_filename)
        
        filename = scene.fop_blend_save_filename.strip() or "untitled"

        # フォルダが未設定または存在しない場合はダイアログを開く
        if not folder or not os.path.isdir(folder):
            self.directory = ""
            context.window_manager.fileselect_add(self)  # ここでフォルダ選択UIを開く
            return {'RUNNING_MODAL'}

        if False:
            if not os.path.isdir(folder):
                self.report({'WARNING'}, _("Please select a valid folder to save"))
                return {'CANCELLED'}
            
        return self._save_to_path(context, folder, filename, settings)  # 以下に渡す

    def _save_to_path(self, context, folder, filename, settings):
        # 拡張子補完・上書き防止
        full_path = get_safe_blend_save_path(
            folder,
            filename,
            overwrite_guard=settings.blendfile_overwrite_guard
        )

        # 外部データの格納方式に応じた処理
        if settings.pack_resources:        # リソースの自動パック
            bpy.ops.file.pack_all()
            if DEBUG_MODE:
                print("Packed all external resources.")
        else:
            unpack_external_data_safely()   # 一部除外してアンパック
            if DEBUG_MODE:
                print("Unpacked external resources (excluding protected ones).")

        if False:   # リソースの自動パックのドロップダウン式
            if settings.external_data == 'PACK':
                bpy.ops.file.pack_all()
                if DEBUG_MODE:
                    print("Packed all external resources.")

        if settings.external_data == 'RELATIVE':  # 相対パス
            bpy.ops.file.make_paths_relative()
            if DEBUG_MODE:
                print("Made all external paths relative.")

        elif settings.external_data == 'ABSOLUTE':      # 絶対パス
            bpy.ops.file.make_paths_absolute()
            if DEBUG_MODE:
                print("Made all external paths absolute.")

        elif settings.external_data == 'MIXED':
            # 何も変更しない（初期状態のまま保存）
            if DEBUG_MODE:
                print("[FOP] External data mode is MIXED → no path changes applied")



        if False:
            # リソースの自動パック
            if settings.pack_resources:
                bpy.ops.file.pack_all()
                if DEBUG_MODE:
                    print("Packed all external resources.")

                """ # False時はアンパックしたい時（ファイルが存在しないと失敗するリスクあり）
                else:
                    bpy.ops.file.unpack_all(method='USE_ORIGINAL')  # または 'WRITE_LOCAL'
                    if DEBUG_MODE:
                        print("Unpacked all resources.")
                """

        # パスが有効化の確認
        if not os.path.isdir(os.path.dirname(full_path)):
            self.report({'ERROR'}, _("Invalid folder path"))
            return {'CANCELLED'}

        # 書き込み権限のチェック
        if not os.access(os.path.dirname(full_path), os.W_OK):
            self.report({'ERROR'}, _("Cannot write to the selected folder"))
            return {'CANCELLED'}

        # コピー保存。現在の .blend を置き換えない（作業ファイルは保存前のまま）
        # bpy.ops.wm.save_as_mainfile(filepath=full_path, copy=True)

        # 保存されたファイルを現在の作業ファイルにする
        # bpy.ops.wm.save_as_mainfile(filepath=full_path)
        try:
            bpy.ops.wm.save_as_mainfile(filepath=full_path)
        except Exception as e:
            error_msg = str(e).lower()

            if "permission" in error_msg or "access" in error_msg:
                self.report({'ERROR'}, _("Cannot write to the selected location (permission denied)"))
            elif "locked" in error_msg or "in use" in error_msg:
                self.report({'ERROR'}, _("Blend file could not be saved because it is locked or in use"))
            elif "invalid" in error_msg or "path" in error_msg:
                self.report({'ERROR'}, _("Invalid path. Please check the save location"))
            else:
                self.report({'ERROR'}, _("Failed to save Blend file: {error}").format(error=str(e)))

            if DEBUG_MODE:
                print(f"[FOP] Save failed: {e}")
            return {'CANCELLED'}


        # 保存先を記録
        context.scene.fop_blend_saved_path = os.path.dirname(full_path)
        # scene.fop_blend_saved_path = os.path.dirname(full_path)

        if DEBUG_MODE:
            print("Last saved to:", context.scene.fop_blend_saved_path)

        # 保存完了
        # self.report({'INFO'}, _("Blend file has been saved"))

        blend_filename = os.path.basename(full_path)

        if settings.pack_resources and settings.external_data == 'RELATIVE':    # パック＆相対パス
            self.report({'INFO'}, _("Packed external data using relative paths and saved the Blend file as {name}").format(name=blend_filename))

        elif settings.pack_resources and settings.external_data == 'ABSOLUTE':      # パック＆絶対パス
            self.report({'INFO'}, _("Packed external data using absolute paths and saved the Blend file as {name}").format(name=blend_filename))

        elif not settings.pack_resources and settings.external_data == 'RELATIVE':      # アンパック＆相対パス
            self.report({'INFO'}, _("Unpacked external data using relative paths and saved the Blend file as {name}").format(name=blend_filename))

        elif not settings.pack_resources and settings.external_data == 'ABSOLUTE':      # アンパック＆絶対パス
            self.report({'INFO'}, _("Unpacked external data using absolute paths and saved the Blend file as {name}").format(name=blend_filename))

        elif settings.pack_resources and settings.external_data == 'MIXED':     # パック・パス変更なし
            self.report({'INFO'}, _("Packed external data  and saved the Blend file as {name}").format(name=blend_filename))

        elif not settings.pack_resources and settings.external_data == 'MIXED':     # アンパック・パス変更なし
            self.report({'INFO'}, _("Unpacked external data and saved the Blend file as {name}").format(name=blend_filename))


        else:       # その他
            self.report({'INFO'}, _("Blend file has been saved"))

        return {'FINISHED'}


    # フォルダ選択後に呼ばれる処理
    def execute_from_dialog(self, context):
        return self._save_to_path(
            context,
            bpy.path.abspath(self.directory),
            context.scene.fop_blend_save_filename.strip() or "untitled",
            context.scene.fop_settings
        )

    def draw(self, context):
        layout = self.layout
        layout.label(text=_("Please select where you would like to export the blend file"), icon='INFO') 




# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        FOP_OT_SelectBlendSaveFolder,
        FOP_OT_SaveBlendFile,
    ]

