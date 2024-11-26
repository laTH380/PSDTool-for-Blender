import bpy
from bpy.types import Panel, UIList


#カスタムリストUIの定義
class PSDTOOL_UL_display_toplayer_frames(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #item:与えられたリストの要素
        if self.layout_type in {'DEFAULT'}:#表示形式をコントロールするblender標準の変数
            row = layout.split(factor=0.8, align=True)
            row.label(text=item.name, translate=False)
            if item.visible:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_OFF')
                op.layer_index = 0
                op.item_index = index
            else:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_ON')
                op.layer_index = 0
                op.item_index = index
        elif self.layout_type in {'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass

class PSDTOOL_UL_display_sub1layer_frames(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #item:与えられたリストの要素
        if self.layout_type in {'DEFAULT'}:#表示形式をコントロールするblender標準の変数
            row = layout.split(factor=0.8, align=True)
            row.label(text=item.name, translate=False)
            if item.visible:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_OFF')
                op.layer_index = 1
                op.item_index = index
            else:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_ON')
                op.layer_index = 1
                op.item_index = index
        elif self.layout_type in {'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass


class PSDTOOL_PT_Panel(Panel):#領域定義
    bl_space_type = "VIEW_3D" #ツールチップの説明文
    bl_region_type = "UI"
    bl_label = "Modifier Operations"
    bl_category = "TEST"

    def draw(self, context):#内容定義
        layout = self.layout

        row = layout.row()#横並びの要素枠
        col = row.column()#縦並びの要素枠
        col.operator("psdtoolkit.import_psd", text = "Apply All")
        col.operator("psdtoolkit.import_psd", text = "Apply All_3")

        col = row.column()
        col.operator("psdtoolkit.import_psd", text = "Delete All")

class PSDTOOL_PT_main_panel(Panel):
    bl_label = "PSD Toolkit"
    bl_idname = "PT_PSDTOOLKIT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PSD Toolkit'

    def draw(self, context):#描画内容
        #情報取得
        active_object = context.active_object
        is_active_object_psd = False
        if len(active_object.PSDTOOLKIT_psd_object_properties.sublayer)>=1:
            is_active_object_psd = True
        else:
            print("no psd object properties")
            is_active_object_psd = False

        #描画
        layout = self.layout.column()#縦に詰める箱を追加（一列だけ）

        # コントロールパネル
        row = layout.row()#横に並べられる箱を追加（一行だけ）
        row.label(text="ここにコントロールパネルを表示")

        # 画像の表示
        row = layout.row()
        row.label(text="ここに画像を表示")
        if is_active_object_psd:
            row.template_preview(context.active_object, show_buttons=False)

        # レイヤー一覧
        col = layout.column()
        row = col.row()
        row.label(text="ここにレイヤー一覧を表示")
        if is_active_object_psd:
            group_layer_table = col.column()
            group_layer_table_item = group_layer_table.row()
            group_layer_table_item.label(text="ここにグループレイヤー一覧を表示")
            psd_info = active_object.PSDTOOLKIT_psd_object_properties
            group_layer_table_item = group_layer_table.row()
            group_layer_table_item.template_list(#その中にリストUIを作成
                "PSDTOOL_UL_display_toplayer_frames",  # リストタイプの名前を文字列として渡す
                "",
                psd_info, "sublayer",#リストのデータソースで、
                psd_info, "active_layer_index",#アクティブなアイテムのインデクス。
            )
            sub1_layer = psd_info.sublayer[psd_info.active_layer_index]
            if len(sub1_layer.sublayer)>=1:
                group_layer_table_item = group_layer_table.row()
                group_layer_table_item.template_list(#その中にリストUIを作成
                    "PSDTOOL_UL_display_sub1layer_frames",  # リストタイプの名前を文字列として渡す
                    "",
                    sub1_layer, "sublayer",#リストのデータソースで、
                    sub1_layer, "active_layer_index",#アクティブなアイテムのインデクス。
                )

            # layout.label(text="PSD Items:")
            # for i, item in enumerate(psd_props.psd_list):
            #     row = layout.row(align=True)
            #     row.prop(item, "name", text="")  # 項目の名前表示
            #     op = row.operator("psdtoolkit.toggle_visibility", text="", icon="HIDE_ON" if item.visible else "HIDE_OFF")
            #     op.index = i  # トグルボタンのインデックスを設定

# class MMDDisplayItemsPanel(Panel):
#     bl_label = "PSD Toolkit"
#     bl_idname = "PT_PSDTOOLKIT_main_panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'PSD Toolkit'

#     def draw(self, context):
#         active_obj = context.active_object
#         # root = mmd_model.Model.findRoot(active_obj)
#         # if root is None:
#         #     self.layout.label(text='Select a MMD Model')
#         #     return

#         mmd_root = {'display_item_frames': [], 'active_display_item_frame': 0}
#         col = self.layout.column()#新しい列を作成（一列だけ）
#         ##表示パネルの第一要素
#         row = col.row()#その中に行を作成（一行だけ）
#         row.template_list(#その中にリストUIを作成
#             "MMD_ROOT_UL_display_item_frames",
#             "",
#             mmd_root, "display_item_frames",#mmd_root.display_item_frames がリストのデータソースで、
#             mmd_root, "active_display_item_frame",#mmd_root.active_display_item_frame がアクティブなアイテムフレームを示します。
#             )
#         tb = row.column()
#         tb1 = tb.column(align=True)#追加UI
#         tb1.operator('mmd_tools.display_item_frame_add', text='', icon=ICON_ADD)
#         tb1.operator('mmd_tools.display_item_frame_remove', text='', icon=ICON_REMOVE)
#         tb1.menu('OBJECT_MT_mmd_tools_display_item_frame_menu', text='', icon='DOWNARROW_HLT')
#         tb.separator()
#         tb1 = tb.column(align=True)#上下移動UI
#         tb1.operator('mmd_tools.display_item_frame_move', text='', icon='TRIA_UP').type = 'UP'
#         tb1.operator('mmd_tools.display_item_frame_move', text='', icon='TRIA_DOWN').type = 'DOWN'

#         frame = ItemOp.get_by_index(mmd_root.display_item_frames, mmd_root.active_display_item_frame)
#         if frame is None:
#             return

#         ##表示パネルの第二要素
#         c = col.column(align=True)
#         row = c.row()
#         row.template_list(
#             "MMD_ROOT_UL_display_items",
#             "",
#             frame, "data",
#             frame, "active_item",
#             )
#         tb = row.column()
#         tb1 = tb.column(align=True)
#         tb1.operator('mmd_tools.display_item_add', text='', icon=ICON_ADD)
#         tb1.operator('mmd_tools.display_item_remove', text='', icon=ICON_REMOVE)
#         tb1.menu('OBJECT_MT_mmd_tools_display_item_menu', text='', icon='DOWNARROW_HLT')
#         tb.separator()
#         tb1 = tb.column(align=True)
#         tb1.operator('mmd_tools.display_item_move', text='', icon='TRIA_UP').type = 'UP'
#         tb1.operator('mmd_tools.display_item_move', text='', icon='TRIA_DOWN').type = 'DOWN'

#         row = col.row()
#         r = row.row(align=True)
#         r.operator('mmd_tools.display_item_find', text='Bone', icon='VIEWZOOM').type = 'BONE'
#         r.operator('mmd_tools.display_item_find', text='Morph', icon='VIEWZOOM').type = 'MORPH'
#         row.operator('mmd_tools.display_item_select_current', text='Select')