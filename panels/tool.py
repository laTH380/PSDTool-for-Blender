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

class PSDTOOL_UL_display_sub2layer_frames(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #item:与えられたリストの要素
        if self.layout_type in {'DEFAULT'}:#表示形式をコントロールするblender標準の変数
            row = layout.split(factor=0.8, align=True)
            row.label(text=item.name, translate=False)
            if item.visible:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_OFF')
                op.layer_index = 2
                op.item_index = index
            else:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_ON')
                op.layer_index = 2
                op.item_index = index
        elif self.layout_type in {'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass

class PSDTOOL_UL_display_sub3layer_frames(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #item:与えられたリストの要素
        if self.layout_type in {'DEFAULT'}:#表示形式をコントロールするblender標準の変数
            row = layout.split(factor=0.8, align=True)
            row.label(text=item.name, translate=False)
            if item.visible:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_OFF')
                op.layer_index = 3
                op.item_index = index
            else:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_ON')
                op.layer_index = 3
                op.item_index = index
        elif self.layout_type in {'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass

class PSDTOOL_UL_display_sub4layer_frames(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #item:与えられたリストの要素
        if self.layout_type in {'DEFAULT'}:#表示形式をコントロールするblender標準の変数
            row = layout.split(factor=0.8, align=True)
            row.label(text=item.name, translate=False)
            if item.visible:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_OFF')
                op.layer_index = 4
                op.item_index = index
            else:
                op = row.operator("psdtool.toggle_visibility", text="", icon='HIDE_ON')
                op.layer_index = 4
                op.item_index = index
        elif self.layout_type in {'COMPACT'}:
            pass
        elif self.layout_type in {'GRID'}:
            pass

class PSDTOOL_PT_top_panel(Panel):#領域定義
    bl_label = "PSDTool" #ツールチップの説明文
    bl_idname = "PSDTOOL_PT_top_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PSDTool'

    def draw(self, context):#内容定義
        layout = self.layout.column()
        # コントロールパネル
        row = layout.row()
        row.operator('psdtoolkit.import_psd', text='import PSD', icon='OUTLINER_OB_MESH')

class PSDTOOL_PT_layers_panel(Panel):
    bl_label = "PSD layers"
    bl_idname = "PSDTOOLKIT_PT_layers_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PSDTool'

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
        # レイヤー一覧
        col = layout.column()
        # row = col.row()
        # row.label(text="ここにレイヤー画像を表示")
        
        group_layer_table = col.column()
        psd_info = active_object.PSDTOOLKIT_psd_object_properties
        group_layer_table_item = group_layer_table.row()
        group_layer_table_item.template_list(#その中にリストUIを作成
            "PSDTOOL_UL_display_toplayer_frames",  # リストタイプの名前を文字列として渡す
            "",
            psd_info, "sublayer",#リストのデータソースで、
            psd_info, "active_layer_index",#アクティブなアイテムのインデクス。
        )
        if is_active_object_psd:
            sub1_layer = psd_info.sublayer[psd_info.active_layer_index]
            if len(sub1_layer.sublayer)>=1:
                group_layer_table_item = group_layer_table.row()
                group_layer_table_item.template_list(#その中にリストUIを作成
                    "PSDTOOL_UL_display_sub1layer_frames",  # リストタイプの名前を文字列として渡す
                    "",
                    sub1_layer, "sublayer",#リストのデータソースで、
                    sub1_layer, "active_layer_index",#アクティブなアイテムのインデクス。
                )
                sub2_layer = sub1_layer.sublayer[sub1_layer.active_layer_index]
                if len(sub2_layer.sublayer)>=1:
                    group_layer_table_item = group_layer_table.row()
                    group_layer_table_item.template_list(#その中にリストUIを作成
                        "PSDTOOL_UL_display_sub2layer_frames",  # リストタイプの名前を文字列として渡す
                        "",
                        sub2_layer, "sublayer",#リストのデータソースで、
                        sub2_layer, "active_layer_index",#アクティブなアイテムのインデクス。
                    )
                    sub3_layer = sub2_layer.sublayer[sub2_layer.active_layer_index]
                    if len(sub3_layer.sublayer)>=1:
                        group_layer_table_item = group_layer_table.row()
                        group_layer_table_item.template_list(#その中にリストUIを作成
                            "PSDTOOL_UL_display_sub3layer_frames",  # リストタイプの名前を文字列として渡す
                            "",
                            sub3_layer, "sublayer",#リストのデータソースで、
                            sub3_layer, "active_layer_index",#アクティブなアイテムのインデクス。
                        )
                        sub4_layer = sub3_layer.sublayer[sub3_layer.active_layer_index]
                        if len(sub4_layer.sublayer)>=1:
                            group_layer_table_item = group_layer_table.row()
                            group_layer_table_item.template_list(#その中にリストUIを作成
                                "PSDTOOL_UL_display_sub4layer_frames",  # リストタイプの名前を文字列として渡す
                                "",
                                sub4_layer, "sublayer",#リストのデータソースで、
                                sub4_layer, "active_layer_index",#アクティブなアイテムのインデクス。
                            )