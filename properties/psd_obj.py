import bpy
from bpy.props import FloatProperty, CollectionProperty, IntProperty, StringProperty, BoolProperty
from bpy.types import PropertyGroup, Operator

import utils

#名前解決が大事なので同じものを指すときは必ず同じ名前にする
#プロパティグループを継承することで、カスタムプロパティを定義できる
#BlenderのCollectionPropertyを使用すると、複数のデータを1つのプロパティとしてグループ化でき、リストや配列のようなデータ構造を持たせることができます

# ===========================================
# Property classes and set operators
# ===========================================

# シーンプロパティ
class PSDTOOL_scene_properties(PropertyGroup):
    psd_id: IntProperty(name="psd_id", default=0)
    
# psdオブジェクトプロパティ
# 再帰的定義ができないので多層化はこれを増やしていかないといけない（5階層までサポート）
class PSDTOOL_psd_object_properties_sub5_layer(PropertyGroup):
    name: StringProperty(name="増やす場合はこれを変えていく", default="")

class PSDTOOL_psd_object_properties_sub4_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_sub5_layer)#将来的に増やせるように
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    name: StringProperty(name="name", default="")

class PSDTOOL_psd_object_properties_sub3_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_sub4_layer)
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    name: StringProperty(name="name", default="")
    active_layer_index: IntProperty(name="active_layer_index", default=0)

class PSDTOOL_psd_object_properties_sub2_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_sub3_layer)
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    name: StringProperty(name="name", default="")
    active_layer_index: IntProperty(name="active_layer_index", default=0)

class PSDTOOL_psd_object_properties_sub1_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_sub2_layer)
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    name: StringProperty(name="name", default="")
    active_layer_index: IntProperty(name="active_layer_index", default=0)

class PSDTOOL_psd_object_properties_top_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_sub1_layer)
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    name: StringProperty(name="name", default="")
    active_layer_index: IntProperty(name="active_layer_index", default=0)

class PSDTOOL_psd_object_properties(PropertyGroup):
    psd_id: IntProperty(name="psd_id", default=0)
    size_x: IntProperty(name="size_x", default=0)
    size_y: IntProperty(name="size_y", default=0)
    sublayer: CollectionProperty(type=PSDTOOL_psd_object_properties_top_layer)
    active_layer_index: IntProperty(name="active_layer_index", default=0)

class PSDTOOL_OT_make_object_properties(Operator):#指定されたオブジェクトのPSDTOOL_psd_object_propertiesを作成
    bl_idname = "psdtool.make_psd_object_properties"
    bl_label = "psdtool.make_psd_object_properties"

    object_name: StringProperty(name="object_name", default="object_name")
    psd_size_x: IntProperty(name="psd_size_x", default=0)
    psd_size_y: IntProperty(name="psd_size_y", default=0)
    psd_id: IntProperty(name="psd_id", default=0)#PSDTool上におけるpsdのID
    layer_struct: StringProperty(name="psd_struct", default="")#json文字列でpsdの構造情報が入力される

    def execute(self, context):
        target_object = context.scene.objects.get(self.object_name)
        if target_object is not None:
            target_object.PSDTOOL_psd_object_properties.psd_id = self.psd_id
            target_object.PSDTOOL_psd_object_properties.size_x = self.psd_size_x
            target_object.PSDTOOL_psd_object_properties.size_y = self.psd_size_y
            layer_struct = utils.jsonstring2dict(self.layer_struct)
            for top_layer_struct in layer_struct:
                self._recur_make_props(target_object.PSDTOOL_psd_object_properties.sublayer, top_layer_struct)
        else:
            self.report({ 'ERROR' }, "The psd plane can't be found")
            return { 'CANCELLED' }
        return {'FINISHED'}
    
    def _recur_make_props(self, target_prop, layer_struct):
        if layer_struct["sublayer"] is None:
            new_target_prop = target_prop.add()
            _set_psd_object_properties(new_target_prop, layer_struct)
        else:
            new_target_prop = target_prop.add()
            _set_psd_object_properties(new_target_prop, layer_struct)
            for child_layer_struct in layer_struct["sublayer"]:
                self._recur_make_props(new_target_prop.sublayer, child_layer_struct)
        return

# class PSDTOOL_OT_set_object_properties(Operator):#OLD:指定されたオブジェクトのPSDTOOL_psd_object_propertiesに要素を上書き更新。
#     bl_idname = "psdtool.set_psd_object_properties"
#     bl_label = "psdtool.set_psd_object_properties"

#     object_data_name: StringProperty(name="object_data_name", default="object_data_name")
#     sub_layer: BoolProperty(name="sublayer", default=False)#これがsublayerかどうか
#     group_layer_index: IntProperty(name="group_layer_index", default=0)#親レイヤーのインデックス
#     sublayer_index: IntProperty(name="sublayer_index", default=0)#子レイヤーのインデックス

#     x: IntProperty(name="x", default=0)
#     y: IntProperty(name="y", default=0)
#     visible: BoolProperty(name="visible", default=True)
#     layer_name: StringProperty(name="name", default="")

#     def execute(self, context):
#         target_object = context.scene.objects.get(self.object_data_name)
#         if target_object is not None:
#             if self.sublayer:
#                 item = target_object.PSDTOOL_psd_object_properties.psdtool_layer_info[self.group_layer_index].sublayer[self.sublayer_index]
#                 item.x = self.x
#                 item.y = self.y
#                 item.visible = self.visible
#                 item.layer_name = self.layer_name
#             else:
#                 item = target_object.PSDTOOL_object_properties.psdtool_layer_info[self.group_layer_index]
#                 item.x = self.x
#                 item.y = self.y
#                 item.visible = self.visible
#                 item.layer_name = self.layer_name
#         else:
#             self.report({ 'ERROR' }, "The psd plane can't be found")
#             return { 'CANCELLED' }
#         return {'FINISHED'}
    
def _set_psd_object_properties(target_prop, data):
    target_prop.x = data["x"]
    target_prop.y = data["y"]
    target_prop.visible = data["visible"]
    target_prop.name = data["name"]
    return