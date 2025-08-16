import bpy
from bpy.types import Operator
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty

from core import bpyImage, config, bpyImage

def _recur_make_image_from_psd_obj_prop(sublayer, combined_image, psd_id, depth=0, layer_index=[0,0,0,0,0]):
    tmp_combined_image = combined_image.copy()
    for layer in sublayer:
        layer_index[depth] += 1
        if layer.visible:
            if len(layer.sublayer) == 0:
                layer_image_name = config.make_name_for_psdtool(kindID=0, objectID=psd_id, layer_index=layer_index)
                layer_image = bpyImage.get_packed_image_by_name(layer_image_name)
                tmp_combined_image = bpyImage.merge_image(tmp_combined_image, layer_image, layer.x, layer.y)
            else:
                tmp_combined_image = _recur_make_image_from_psd_obj_prop(layer.sublayer, tmp_combined_image, psd_id, depth+1, layer_index)
    layer_index[depth] = 0
    return tmp_combined_image

def make_image_from_psd_obj_prop():
    psd_obj_prop = bpy.context.active_object.PSDTOOL_psd_object_properties
    size = [psd_obj_prop.size_x, psd_obj_prop.size_y]
    psd_id = psd_obj_prop.psd_id
    final_image = bpyImage.make_image(size)
    final_image = _recur_make_image_from_psd_obj_prop(psd_obj_prop.sublayer, final_image, psd_id)
    return final_image

def update_tex(target_object):
    new_image = make_image_from_psd_obj_prop()
    new_tex_name = bpyImage.paccking_merged_image_to_blender(new_image)
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

    layer_index: IntProperty(name="layer_index", default=0)  # 何層目のアイテムがターゲットか？ 0~4
    item_index: IntProperty(name="item_index", default=0)  # ターゲットのインデックス。アクティブインデックスが更新されないまま呼ばれる可能性があるため

    # @classmethod
    # def poll(cls, context):#このオペレータが実行可能かどうかを返す
    #     obj = context.object
    #     if obj.mode == "OBJECT":
    #         return True
    #     return False

    def execute(self, context):
        target_obj = context.active_object
        target_parent = target_obj.PSDTOOL_psd_object_properties
        target = target_parent
        for i in range(5):
            if i == self.layer_index:
                target = target.sublayer[self.item_index]
                break
            target = target.sublayer[target.active_layer_index]
            target_parent = target
        target_parent.active_layer_index = self.item_index
        target.visible = not target.visible

        update_tex(target_obj)
        return {'FINISHED'}