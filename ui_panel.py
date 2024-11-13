import bpy
from bpy.types import Panel

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
        layout = self.layout
        scene = context.scene
        psd_props = ["a","b"]#scene.PSDTOOLKIT_scene_properties

        # 画像の表示
        row = layout.row()
        row.label(text="Image Display:")
        row.template_preview(context.active_object, show_buttons=False)  # アクティブオブジェクトのプレビュー

        # PSD項目リスト
        layout.label(text="PSD Items:")
        for i, item in enumerate(psd_props.psd_list):
            row = layout.row(align=True)
            row.prop(item, "name", text="")  # 項目の名前表示
            op = row.operator("psdtoolkit.toggle_visibility", text="", icon="HIDE_ON" if item.visible else "HIDE_OFF")
            op.index = i  # トグルボタンのインデックスを設定