import bpy
from bpy.types import Operator
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty

from core import config, processing_psd, texture

def _recur_make_image_from_psd_obj_prop(sublayer, combined_image, depth=0, layer_index=[0,0,0,0,0]):
    combined_image = combined_image
    for layer in sublayer:
        layer_index[depth] += 1
        if layer.visible:
            if layer.sublayer is None:
                layer_image_name = config.make_name_for_psdtool(kindID=0, layer_index=layer_index)
                layer_image = texture.get_packed_image_by_name(layer_image_name)
                combined_image = processing_psd.merge_image(combined_image, layer_image, layer.x, layer.y)
            else:
                combined_image = _recur_make_image_from_psd_obj_prop(layer.sublayer, combined_image, depth+1, layer_index)
    layer_index[depth] = 0
    return combined_image

def make_image_from_psd_obj_prop():
    psd_obj_prop = bpy.context.active_object.PSDTOOLKIT_psd_object_properties
    size = [psd_obj_prop.size_x, psd_obj_prop.size_y]
    final_image = processing_psd.make_image(size)
    final_image = _recur_make_image_from_psd_obj_prop(psd_obj_prop.sublayer, final_image)
    return final_image

def update_tex(target_object):
    new_image = make_image_from_psd_obj_prop()
    new_tex_name = texture.paccking_merged_image_to_blender(new_image)
    new_tex = bpy.data.images.get(new_tex_name)
    # オブジェクトのすべてのマテリアルをループ
    for mat in target_object.data.materials:
        if mat and mat.use_nodes:
            # ノードツリー内のすべてのノードをループ
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    node.image = new_tex
        elif mat:
            # ノードを使用していない場合の対応
            for tex_slot in mat.texture_slots:
                if tex_slot and tex_slot.texture.type == 'IMAGE':
                    tex_slot.texture.image = new_tex

class PSDTOOL_OT_toggle_visibility(Operator):
    bl_idname = "psdtool.toggle_visibility"
    bl_label = "Toggle Visibility"

    layer_index: IntProperty(name="layer_index", default=0)  # 第何層目を操作されたか0~4
    item_index: IntProperty(name="item_index", default=0) #何番目のアイテムを操作されたか

    def execute(self, context):
        obj = context.active_object
        target_parent = obj.PSDTOOLKIT_psd_object_properties
        target = target_parent.sublayer
        for i in range(self.layer_index):
            target_parent = target_parent.sublayer
            target = target.sublayer
        target_parent.active_layer_index = self.item_index
        target[self.item_index].visible = not target[self.item_index].visible

        update_tex(obj)
        return {'FINISHED'}