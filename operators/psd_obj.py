import bpy
from bpy.types import Operator
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty


class PSDTOOL_OT_toggle_visibility(Operator):
    bl_idname = "psdtool.toggle_visibility"
    bl_label = "Toggle Visibility"

    index: IntProperty()  # インデックスをプロパティとして追加

    def execute(self, context):
        obj = context.active_object
        layer = obj.PSDTOOLKIT_psd_object_properties.sublayer[self.index]
        layer.visible = not layer.visible
        return {'FINISHED'}