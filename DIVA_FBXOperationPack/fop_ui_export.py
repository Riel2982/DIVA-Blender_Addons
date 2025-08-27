# fop_ui_export.py

import bpy
import os
import sys
import time
import json
import subprocess
from bpy.app.translations import pgettext as _
from bpy.app.translations import pgettext as tr

from .fop_export import DIVA_FBX_EXPORT_PRESET, get_safe_export_path
from .fop_export import store_restore_point, restore_to_point, try_run_marker_tool


from .fop_debug import DEBUG_MODE   # デバッグ用

# --- セクション 2: FBXデータ出力 ------------------------------------------
def draw_export_ui(layout, context, scene):
    settings = scene.fop_settings
    box = layout.box()  # 枠付きセクションを作る
    row = box.row(align=True)
    row.prop(scene, "fop_show_export_tools", text="", icon='DOWNARROW_HLT' if scene.fop_show_export_tools else 'RIGHTARROW', emboss=False)
    row.label(text="FBX Data Exporter", icon="PASTEDOWN") # セクションタイトル

    if scene.fop_show_export_tools:
        # 出力ファイル名
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text="File Name :")
        split.prop(settings, "export_filename", text="")

        # 出力設定
        row = box.row()
        row.prop(settings, "export_overwrite_guard", text="")
        row.label(text=_("Auto Numbering"))

        row = box.row()
        row.prop(scene, "fop_export_use_blend_folder", text="")
        row.label(text=_("Save in the same location as the blend file"))

        # 出力オプション
        row = box.row()
        split = row.split(factor=0.22)
        split.label(text=_("Export Options :"))
        split.prop(settings, "use_selection", text="", toggle=True, icon='RESTRICT_SELECT_OFF')    # 選択オブジェクトのみ
        split.prop(settings, "use_visible", text="", toggle=True, icon='HIDE_OFF')     # 可視オブジェクトのみ
        split.prop(settings, "use_active_collection", text="", toggle=True, icon='GROUP')      # アクティブコレクションのみ
        row.separator()

        # 実行ボタン
        box.operator("fop.export_fbx_data", text=_("Export FBX Data"), icon='PASTEDOWN')


# エクスポートオペレーター
class FOP_OT_ExportFBXData(bpy.types.Operator):
    bl_idname = "fop.export_fbx_data"
    bl_label = "Export FBX Data"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("FBX Exported")

    filepath: bpy.props.StringProperty(
        name="File Path",
        description=_("Path to export FBX file"),
        subtype="FILE_PATH", 
        default="//untitled.fbx",
        options={'HIDDEN'}  # オペレーターパネルに表示しない
    )


    def invoke(self, context, event):
        scene = context.scene

        if scene.fop_export_use_blend_folder:
            # Blendファイルパス自動取得
            if not scene.fop_blend_saved_path and bpy.data.filepath:
                scene.fop_blend_saved_path = os.path.dirname(bpy.path.abspath(bpy.data.filepath))

            if not scene.fop_blend_saved_path:
                context.window_manager.fileselect_add(self)
                return {'RUNNING_MODAL'}

            return self.execute(context)

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        settings = context.scene.fop_settings
        preset = DIVA_FBX_EXPORT_PRESET.copy()

        # 復元ポイント保存
        restore_data = store_restore_point(context)

        # マーカー処理（アドオン有効時のみ）
        try_run_marker_tool(context)


        # UIオプションを反映
        preset["use_selection"] = settings.use_selection
        preset["use_visible"] = settings.use_visible
        preset["use_active_collection"] = settings.use_active_collection

        # 保存先パスの決定
        if scene.fop_export_use_blend_folder and scene.fop_blend_saved_path:
            # filename = settings.export_filename.strip() or "untitled.fbx"     # ファイル名未設定時は "untitled.fbx" で保存
            filename = settings.export_filename.strip()
            if not filename:
                self.report({'WARNING'}, tr("Export filename is empty"))     # コメントで抽出対象を確保 _("Export filename is empty"))
                return {'CANCELLED'}

            self.filepath = get_safe_export_path(
                scene.fop_blend_saved_path,
                filename,
                overwrite_guard=settings.export_overwrite_guard
            )
        else:
            abs_path = bpy.path.abspath(self.filepath)
            folder, _ = os.path.split(abs_path)
            # filename = settings.export_filename.strip() or os.path.basename(abs_path)     # ファイル名未設定時はBlendファイルと同名で保存
            filename = settings.export_filename.strip()
            if not filename:
                self.report({'WARNING'}, tr("Export filename is empty"))    # コメントで抽出対象を確保 _("Export filename is empty"))
                return {'CANCELLED'}
            
            self.filepath = get_safe_export_path(
                folder,
                filename,
                overwrite_guard=settings.export_overwrite_guard
            )

        preset["filepath"] = self.filepath

        # 出力対象オブジェクトの収集（選択・可視・コレクション設定に応じる）
        allowed_colls = None
        if preset["use_active_collection"]:
            active_coll = context.view_layer.active_layer_collection.collection

            def collect_children(coll, out_set):
                out_set.add(coll)
                for ch in coll.children:
                    collect_children(ch, out_set)

            allowed_colls = set()
            collect_children(active_coll, allowed_colls)

        if False:
            def is_export_object(obj, scene, preset):
                # 選択オブジェクト限定
                if preset["use_selection"] and not obj.select_get():
                    return False
                # 可視オブジェクト限定
                if preset["use_visible"] and not obj.visible_get():
                    return False
                # アクティブコレクション限定（子孫含む）
                if preset["use_active_collection"]:
                    if not obj.users_collection:
                        return False
                    if not any(c in allowed_colls for c in obj.users_collection):
                        return False
                return True

            # アーマチュアの存在確認
            meshes = [obj for obj in scene.objects if obj.type == 'MESH' and is_export_object(obj, scene, preset)]
            armatures = [obj for obj in scene.objects if obj.type == 'ARMATURE' and is_export_object(obj, scene, preset)]

            warning_issued = False  # ← 警告を出したかどうか記録するフラグ

            if not armatures:
                # アーマチュアが存在しない警告
                self.report({'WARNING'}, "No Armature found in export data")     # コメントで抽出対象を確保 _("No Armature found in export data"))
                warning_issued = True
            else:
                # アーマチュアはあるが、非ペアレントMeshを検査
                unlinked_meshes = [m for m in meshes if not m.find_armature()]  # find_armatureはモディファイア経由も含めて検索する
                if unlinked_meshes:
                    if DEBUG_MODE:
                        print("[FOP][DEBUG] Unlinked Mesh Objects:")
                        for m in unlinked_meshes:
                            print(" -", m.name)
                    else:
                        self.report({'WARNING'}, "There are {count} mesh objects not linked to any Armature".format(count=len(unlinked_meshes))) # コメントで抽出対象を確保 _("There are {count} mesh objects not linked to any Armature")
                    warning_issued = True

        # scene と preset は execute 内のローカル変数
        def is_export_object(obj):
            # 対象タイプ（エクスポータの object_types と一致）
            if obj.type not in preset["object_types"]:
                return False
            # 選択限定
            if preset["use_selection"] and not obj.select_get():
                return False
            # 可視限定
            if preset["use_visible"] and not obj.visible_get():
                return False
            # アクティブコレクション限定（子孫含む）
            if preset.get("use_active_collection"):
                if not obj.users_collection:
                    return False
                if not any(c in allowed_colls for c in obj.users_collection):
                    return False
            return True


        # エクスポート対象 Mesh / Armature を抽出
        export_meshes = [o for o in scene.objects if o.type == 'MESH' and is_export_object(o)]
        export_armatures = [o for o in scene.objects if o.type == 'ARMATURE' and is_export_object(o)]

        warning_issued = False  # ← 警告を出したかどうか記録するフラグ

        if 'ARMATURE' in preset["object_types"] and len(export_armatures) == 0:
            self.report({'WARNING'}, tr("No Armature found in export data"))     # コメントで抽出対象を確保 _("No Armature found in export data"))
            warning_issued = True

        elif 'MESH' in preset["object_types"] and len(export_meshes) > 0:
            unlinked_meshes = [m for m in export_meshes if not m.find_armature()]
            if unlinked_meshes:
                # 件数だけ report（format を使用）
                self.report({'WARNING'}, tr("There are {count} mesh objects not linked to any Armature").format(count=len(unlinked_meshes))) # コメントで抽出対象を確保 _("There are {count} mesh objects not linked to any Armature"))
                warning_issued = True

                if DEBUG_MODE:
                    print("[FOP][DEBUG] Unlinked Mesh Objects:")
                    for m in unlinked_meshes:
                        print(" -", m.name)



        # エクスポート実行
        bpy.ops.export_scene.fbx(**preset)

        # 復元処理
        restore_to_point(context, restore_data)

        # self.report({'INFO'}, _("FBX data exported to: {path}").format(path=self.filepath)) #  オペレーターパネルにファイルパスの場所が表示される意味不明
        # self.report({'INFO'}, "FBX data exported")    # ここだけ_()を使うとエラーになるのでコメントで代わりに抽出対象を確保する / tr()なら大丈夫 _("FBX data exported") 
        # 警告が出ていなければ成功メッセージを表示
        if not warning_issued:
            self.report({'INFO'}, tr("FBX data exported"))

        return {'FINISHED'}

if False:   # オペレーターパネルに描画されてしまうのでなし
    def draw(self, context):
        layout = self.layout
        layout.label(text=_("Please select where you would like to export the FBX file"), icon='INFO') 

    

# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        FOP_OT_ExportFBXData,
    ]
