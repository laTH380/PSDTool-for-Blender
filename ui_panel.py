import bpy
from bpy.types import Panel

class PSDTOOL_PT_Panel(Panel):#領域定義
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Modifier Operations"
    bl_category = "TEST"

    def draw(self, context):#内容定義
        layout = self.layout

        row = layout.row()#横並びの要素枠
        col = row.column()#縦並びの要素枠
        col.operator("import_image.to_plane", text = "Apply All")
        col.operator("import_image.to_plane", text = "Apply All_3")

        col = row.column()
        col.operator("import_image.to_plane", text = "Delete All")