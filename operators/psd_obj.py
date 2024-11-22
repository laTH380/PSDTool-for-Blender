import bpy
from bpy.types import Operator
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty


class PSDTOOL_OT_toggle_visibility(Operator):
    bl_idname = "psdtool.toggle_visibility"
    bl_label = "Toggle Visibility"

    layer_index: IntProperty()  # 第何層目を操作されたか0~4

    def execute(self, context):
        obj = context.active_object
        target_parent = obj.PSDTOOLKIT_psd_object_properties
        target = target_parent.sublayer
        for i in range(self.layer_index):
            target_parent = target_parent.sublayer
            target = target.sublayer
        target[target_parent.active_layer_index].visible = not target[target_parent.active_layer_index].visible
        return {'FINISHED'}