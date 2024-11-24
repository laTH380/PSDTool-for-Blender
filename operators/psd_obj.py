import bpy
from bpy.types import Operator
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty

from core import config

def _recur_make_image_from_psd_obj_prop(sublayer, combined_image, depth=0, layer_index=[0,0,0,0,0]):
    combined_image = combined_image
    for layer in sublayer:
        layer_index[depth] += 1
        if layer.visible:
            if layer.sublayer is None:
                layer_image_name = config.make_name_for_psdtool(kindID=0, layer_index=layer_index)
                combined_image.paste(layer_image, (layer.x, layer.y), layer_image)
            else:
                combined_image = _recur_make_image_from_psd_obj_prop(layer.sublayer, combined_image)
    return combined_image

def recur_paccking_imageobject(self, layer_images, layer_index, depth=0):#layer_index=[0,0,0,0,0]
        for layer_image in layer_images:
            layer_index[depth] += 1
            if len(layer_image) == 1:
                layer_image_obj = layer_image[0]
                name = config.make_name_for_psdtool(kindID=0, layer_index=layer_index)
                self.paccking_imageobject(layer_image_obj, name)
            else:
                self.recur_paccking_imageobject(layer_image, layer_index, depth+1)
        layer_index[depth] = 0
        return

def make_image_from_psd_obj_prop():
    active_obj = bpy.context.active_object

    pass

def change_tex_image(image_name):
    pass

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