# fop_ui_import.py

import bpy
from bpy.props import StringProperty 
from bpy_extras.io_utils import ImportHelper
from bpy.app.translations import pgettext as _

from .fop_import import DIVA_FBX_IMPORT_PRESET, extract_base_name, apply_import_naming
from .fop_import import post_import_leaf_bone_check, set_bone_name_display, select_leaf_bones, delete_leaf_bones, delayed_leaf_popup

from .fop_debug import DEBUG_MODE   # デバッグ用


# --- セクション 1: FBXデータ読み込み ------------------------------------------
def draw_import_ui(layout, context, scene):
    settings = scene.fop_settings
    box = layout.box()  # 枠付きセクションを作る
    row = box.row(align=True)
    row.prop(scene, "fop_show_import_tools", text="", icon='DOWNARROW_HLT' if scene.fop_show_import_tools else 'RIGHTARROW', emboss=False)
    row.label(text="FBX Data Importer", icon="COPYDOWN") # セクションタイトル

    if scene.fop_show_import_tools:
        # カスタム法線の切り替え
        row = box.row()
        row.prop(settings, "use_custom_normals", text="")
        row.label(text=_("Import Custom Normals"))   # カスタム法線を使用

        # コレクションを作成
        row = box.row()
        row.prop(settings, "create_collection", text="")
        row.label(text=_("Import into New Collection"))    

        box.operator("fop.import_fbx_data", text=_("Import FBX Data"), icon='COPYDOWN')




# フォルダ選択オペレーター
class FOP_OT_ImportFBXData(bpy.types.Operator, ImportHelper):  # ImportHelperを継承
    bl_idname = "fop.import_fbx_data"
    bl_label = "Import FBX Data"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = _("FBX Imported")

    filename_ext = ".fbx"  # ImportHelper用
    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        settings = context.scene.fop_settings
        preset = DIVA_FBX_IMPORT_PRESET.copy()

        # ファイルパスを設定
        preset["filepath"] = self.filepath

        # オプション反映
        preset["use_custom_normals"] = settings.use_custom_normals

        # インポート実行
        bpy.ops.import_scene.fbx(**preset)

        # 命名処理
        base_name = extract_base_name(self.filepath)
        imported_objs = context.selected_objects
        apply_import_naming(imported_objs, base_name, create_collection=settings.create_collection) # コレクション分岐もここで

        self.report({'INFO'}, _("FBX data imported to: {name}").format(name=base_name))        

        # リーフボーンの確認
        # post_import_leaf_bone_check(context, imported_objs)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text=_("Please select the FBX file you wish to import"), icon='INFO') 


# リーフボーン検出通知ポップアップ
class FOP_OT_ConfirmLeafBoneDelete(bpy.types.Operator):
    bl_idname = "fop.confirm_leaf_bone_delete"
    bl_label = "リーフボーン削除確認"
    bl_options = {'REGISTER', 'UNDO'}

    armature_name: bpy.props.StringProperty()
    bone_names_csv: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'

    def invoke(self, context, event):
        if DEBUG_MODE:
            print("invoke 呼び出し")
            print("context.area:", context.area)
            print("context.region:", context.region)


        # アーマチュアオブジェクトを取得
        armature_obj = context.object
        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, f"アーマチュアが見つかりません: {self.armature_name}")
            return {'CANCELLED'}
        self.armature_name = armature_obj.name

        bpy.ops.object.mode_set(mode='OBJECT')  # 安定表示のため

        # ポップアップ表示（この時点ではまだEDITモードに入らない）
        # return context.window_manager.invoke_props_dialog(self, width=300)
        result = context.window_manager.invoke_popup(self, width=300)
        if DEBUG_MODE:
            print("invoke_popup result:", result)
        return result



    def draw(self, context):
        if DEBUG_MODE:
            try:
                print("draw 呼び出し")
                layout = self.layout
                layout.label(text="描画テスト")
            except Exception as e:
                print("draw() 例外:", e)

        layout = self.layout
        layout.prop(self, "armature_name")
        # layout.prop(self, "bone_names_csv")

            
        # EDITモードへ切り替え（ポップアップ表示後）
        # bpy.ops.object.mode_set(mode='EDIT')

        # 対象ボーンを取得
        armature_obj = context.object
        if not armature_obj or armature_obj.type != 'ARMATURE':
            layout.label(text="アーマチュアが見つかりません")
            return
        edit_bones = armature_obj.data.edit_bones
        target_names = self.bone_names_csv.split(",")
        bones = [edit_bones[name] for name in target_names if name in edit_bones]

        # 明示的に選択状態を設定
        select_leaf_bones(bones)

        # ボーン名表示ON
        set_bone_name_display(armature_obj, True)

        # UI描画
        layout.label(text=f"対象ボーン数: {len(bones)}")
        layout.label(text="リーフボーンが検出されました。削除しますか？")

        row = layout.row()
        op_ok = row.operator("fop.confirm_leaf_bone_delete_ok", text="削除する", icon='CHECKMARK')
        op_ok.armature_name = self.armature_name
        op_ok.bone_names_csv = self.bone_names_csv

        op_cancel = row.operator("fop.confirm_leaf_bone_delete_cancel", text="削除しない", icon='CANCEL')
        op_cancel.armature_name = self.armature_name

# リーフボーンを削除する
class FOP_OT_ConfirmLeafBoneDelete_OK(bpy.types.Operator):
    bl_idname = "fop.confirm_leaf_bone_delete_ok"
    bl_label = "リーフボーンを削除"

    armature_name: bpy.props.StringProperty()
    bone_names_csv: bpy.props.StringProperty()

    def execute(self, context):
        # ボーン名リストを取得
        bone_names = [name for name in self.bone_names_csv.split(",") if name]

        # アーマチュアオブジェクトを取得
        armature_obj = bpy.data.objects.get(self.armature_name)
        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, "アーマチュアが見つかりません")
            return {'CANCELLED'}

        # リーフボーンを削除
        delete_leaf_bones(bone_names)

        # オブジェクトモードに戻す
        bpy.ops.object.mode_set(mode='OBJECT')

        # ビューポートのボーン名表示をOFFにする
        set_bone_name_display(armature_obj, False)

        # 削除完了通知ポップアップ（フォーカス外すと閉じる）
        def draw_popup(self, context):
            layout = self.layout
            layout.label(text="削除したボーン:")
            for name in bone_names:
                layout.label(text=f"• {name}")

        context.window_manager.popup_menu(draw_popup, title="削除完了", icon='INFO')
        return {'FINISHED'}
    
# リーフボーンを削除しない
class FOP_OT_ConfirmLeafBoneDelete_Cancel(bpy.types.Operator):
    bl_idname = "fop.confirm_leaf_bone_delete_cancel"
    bl_label = "削除しない"

    armature_name: bpy.props.StringProperty()

    def execute(self, context):
        # アーマチュアオブジェクトを取得
        armature_obj = bpy.data.objects.get(self.armature_name)
        if armature_obj and armature_obj.type == 'ARMATURE':
            # ビューポートのボーン名表示をOFFにする（選択状態は維持）
            set_bone_name_display(armature_obj, False)

        # ユーザーにキャンセル通知
        self.report({'INFO'}, "リーフボーンの削除をキャンセルしました")
        return {'CANCELLED'}
    

# Blenderアドオンで使うクラスの登録
def get_classes():
    return [
        FOP_OT_ImportFBXData,
        FOP_OT_ConfirmLeafBoneDelete,
        FOP_OT_ConfirmLeafBoneDelete_OK,
        FOP_OT_ConfirmLeafBoneDelete_Cancel,
    ]

