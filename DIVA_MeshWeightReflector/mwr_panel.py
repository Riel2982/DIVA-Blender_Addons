# mwr_panel.py

import bpy

from bpy.app.translations import pgettext as _

from .mwr_main import (
    disable_mirror_modifier,
    duplicate_and_apply_mirror,
    get_pattern_map_from_prefs, 
    process_origin_overlap,
)
from .mwr_sub import (
    process_symmetrize,
)
from .mwr_json import get_bone_pattern_items, get_selected_rules

# Nパネル設定
class DIVA_PT_MeshWeightReflectorPanel(bpy.types.Panel):
    bl_label = "Mesh Weight Reflector"
    bl_idname = "DIVA_PT_mesh_weight_reflect"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIVA"
    bl_options = {'DEFAULT_CLOSED'} 

    # セクションの左側にアイコンを追加
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MOD_MIRROR') # 左右反転風

    def draw(self, context):
        layout = self.layout
        props = context.scene.diva_mesh_weight_reflect

        box = layout.box()  # 枠付きセクションを作成

        # ボーン識別文字（ドロップダウン）
        row = box.row()
        split = row.split(factor=0.20, align=True)  # ← ラベル側20%、残りにドロップダウンとボタン
        split.label(text=_("Bone Identifier:"))
        right = split.row() # ぴったりボタン同士をくっつけたい場合は(align=True)
        right.prop(props, "bone_pattern", text="")  # ドロップダウン（ラベル非表示）
        right.operator("mwr.open_preferences", text="", icon="PREFERENCES")  # 設定ボタン（プリファレンスを開く）

        # ミラー自動判別（チェックボタン）
        row = box.row()
        row.prop(props, "duplicate_and_mirror", text="")  # チェックボックス
        row.label(text=_("Duplicate and Mirror"))  # ラベル

        # 対称化モード（チェックボックス）
        row = box.row()
        row.prop(props, "symmetrize_mode", text="")
        row.label(text=_("Symmetrize Mode"))  # ラベル（トグルと並列表示）

        # 対称化モード有効時のみ、追加オプション表示
        if props.symmetrize_mode:
            # マージON/OFFトグル
            row.prop(props, "merge_center_vertices", text="")
            row.label(text=_("Merge Center"))

            # マージ閾値（マージする場合のみ）
            if props.merge_center_vertices:
                row.prop(props, "merge_threshold", text=_("Merge Distance"))
            # マージ閾値（マージしない時のレイアウトダミー）
            if not props.merge_center_vertices:
                row.label(text="")

        # ミラー実行ボタン
        # box.operator("diva.mesh_weight_reflect", text=_("Reflect Mesh Weights"), icon="MOD_MIRROR")

        button_label = "Reflect Mesh Weights"  # デフォルト
        if props.symmetrize_mode:
            button_label = "Symmetrize Mesh Weights"

        box.operator("diva.mesh_weight_reflect", text=button_label, icon="MOD_MIRROR")


# アドオン処理
class DIVA_OT_MeshWeightReflector(bpy.types.Operator):
    """ 選択されたメッシュオブジェクトの鏡像反転版を作成します """
    bl_idname = "diva.mesh_weight_reflect"
    bl_label = "Reflect Mesh Weights"
    bl_description = _("Creates a mirrored version of the selected mesh object")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        props = context.scene.diva_mesh_weight_reflect

        # 3Dビューで選択されているか確認する
        if not obj or obj not in context.selected_objects:
            self.report({'ERROR'}, _("No object is selected in the 3D View"))
            return {'CANCELLED'}
        '''        
        obj = context.active_object
        if obj.type != 'MESH':
            self.report({'ERROR'}, _("The active object is not a mesh"))
            return {'CANCELLED'}
        '''
            
        # 安全策①: 編集モードならオブジェクトモードに切り替える（メッシュ限定）
        if obj.mode == 'EDIT':
            if obj.type == 'MESH':
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                self.report({'ERROR'}, _("The editing object {name} is not a mesh. Please switch to Object Mode").format(name=obj.name))
                return {'CANCELLED'}

        # 安全策②: アーマチュアなど他の編集モードでは強制終了
        if obj.mode != 'OBJECT':
            self.report({'ERROR'}, _("The current mode is {mode}. Please run in Object Mode").format(mode=obj.mode))
            return {'CANCELLED'}

        # 安全策③: オブジェクトモードでもメッシュが選ばれていない場合
        if obj.type != 'MESH':
            self.report({'ERROR'}, _("The selected object {name} is not a mesh. Please select a mesh object").format(name=obj.name))
            return {'CANCELLED'}


        # 識別子セットに対応（識別子マップを取得）
        pattern_label = props.bone_pattern
        pattern_map = get_selected_rules(pattern_label)
        if not pattern_map:
            self.report({'ERROR'}, _("Identifier rule {label} not found").format(label=pattern_label))
            return {'CANCELLED'}

        # flipマップ付きの構造を取得
        pattern_struct = get_pattern_map_from_prefs(context, pattern_label, None)
        flip_map = pattern_struct["flip"]

        # ✅ 対称化モードチェック
        if props.symmetrize_mode:
            # 新オペレーターに切り替え実行
            bpy.ops.mwr.symmetrize_mesh_weights('INVOKE_DEFAULT')  # 対称化モードオペレーター
            return {'FINISHED'}

        # ミラー処理実行（対称化モードではないとき）
        mirrored_obj = process_origin_overlap(
            obj,
            pattern_map,
            props.duplicate_and_mirror,
            flip_map,
            merge_center_vertices=False  # ← 絶対に False
        )

        self.report({'INFO'}, _("Mirrored version generated: {name}").format(name=mirrored_obj.name))
        return {'FINISHED'}


class MWR_OT_MeshWeightSymmetry(bpy.types.Operator):
    """ 左右対称版を作成 """
    bl_idname = "mwr.symmetrize_mesh_weights"
    bl_label = "Symmetrize Mesh Weights"
    bl_description = _("Symmetrizes the selected mesh object")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.diva_mesh_weight_reflect
        obj = context.active_object

        # 3Dビューで選択されているか確認する
        if not obj or obj not in context.selected_objects:
            self.report({'ERROR'}, _("No object is selected in the 3D View"))
            return {'CANCELLED'}
        '''        
        obj = context.active_object
        if obj.type != 'MESH':
            self.report({'ERROR'}, _("The active object is not a mesh"))
            return {'CANCELLED'}
        '''
            
        # 安全策①: 編集モードならオブジェクトモードに切り替える（メッシュ限定）
        if obj.mode == 'EDIT':
            if obj.type == 'MESH':
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                self.report({'ERROR'}, _("The editing object {name} is not a mesh. Please switch to Object Mode").format(name=obj.name))
                return {'CANCELLED'}

        # 安全策②: アーマチュアなど他の編集モードでは強制終了
        if obj.mode != 'OBJECT':
            self.report({'ERROR'}, _("The current mode is {mode}. Please run in Object Mode").format(mode=obj.mode))
            return {'CANCELLED'}

        # 安全策③: オブジェクトモードでもメッシュが選ばれていない場合
        if obj.type != 'MESH':
            self.report({'ERROR'}, _("The selected object {name} is not a mesh. Please select a mesh object").format(name=obj.name))
            return {'CANCELLED'}


        # bone_pattern、duplicate_and_mirror は props から取得可能
        pattern_label = props.bone_pattern
        flip_map = get_pattern_map_from_prefs(context, pattern_label, None)["flip"]
        

        # 実際の対称化処理ロジック
        symmetrical_obj = process_symmetrize(
            obj,
            pattern_label,
            props.duplicate_and_mirror,
            flip_map,
            merge_center_vertices=props.merge_center_vertices,
            merge_threshold=props.merge_threshold
        )

        self.report({'INFO'}, _("Symmetrization completed: {name}").format(name=symmetrical_obj.name))
        return {'FINISHED'}


#  DIVAアドオン設定画面（プリファレンス）を開く
class MWR_OT_OpenPreferences(bpy.types.Operator):
    bl_idname = "mwr.open_preferences"
    bl_label = "Open DIVA preferences"
    bl_description = _("Open the addon settings in Preferences")
    bl_options = {'INTERNAL'}  # ← Undo履歴に残さない

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")  # Preferences ウィンドウを開く
        context.preferences.active_section = 'ADDONS'
        context.window_manager.addon_search = "diva"
        # アドオン指定でプリファレンスを開きたい場合はアドオンフォルダ名を設定
        # context.window_manager.addon_search = "DIVA_MeshWeightReflector"
        return {'FINISHED'}


def get_classes():
    return [   
        DIVA_PT_MeshWeightReflectorPanel,
        MWR_OT_OpenPreferences,
        DIVA_OT_MeshWeightReflector,
        MWR_OT_MeshWeightSymmetry
    ]
