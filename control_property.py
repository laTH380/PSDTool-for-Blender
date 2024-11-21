import bpy
from bpy.props import FloatProperty, CollectionProperty, IntProperty, StringProperty, BoolProperty
from bpy.types import PropertyGroup, Operator

#名前解決が大事なので同じものを指すときは必ず同じ名前にする
#プロパティグループを継承することで、カスタムプロパティを定義できる

# ===========================================
# Property classes and set operators
# ===========================================

# シーンプロパティ
class PSDTOOLKIT_scene_properties_psdlist_item(PropertyGroup):
    objectname: StringProperty(name="objectname", default="objectname")

class PSDTOOLKIT_scene_properties(PropertyGroup):
    psd_list: CollectionProperty(type=PSDTOOLKIT_scene_properties_psdlist_item)#BlenderのCollectionPropertyを使用すると、複数のデータを1つのプロパティとしてグループ化でき、リストや配列のようなデータ構造を持たせることができます

class PSDTOOLKIT_OT_add_scene_properties_psd_list(Operator):#カスタムプロパティはこのようにアクセッサを作っておいてアクセスする
    bl_idname = "psdtoolkit.add_scene_properties_psd_list"
    bl_label = "Add psd object"

    objectname: StringProperty(name="objectname", default="objectname")#プロパティのセットはこのようにオペレータのプロパティを介す

    def execute(self, context):
        scene = context.scene
        item = scene.PSDTOOLKIT_scene_properties.psd_list.add()
        item.objectname = self.objectname
        return {'FINISHED'}
    
# psdオブジェクトプロパティ
# 再帰的定義ができないので多層化はこれを増やしていかないといけない
class PSDTOOLKIT_psd_object_properties_sub_layer(PropertyGroup):
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    layer_name: StringProperty(name="name", default="")

class PSDTOOLKIT_psd_object_properties_group_layer(PropertyGroup):
    sublayer: CollectionProperty(type=PSDTOOLKIT_psd_object_properties_sub_layer)
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    layer_name: StringProperty(name="name", default="")

class PSDTOOLKIT_psd_object_properties(PropertyGroup):
    psdtoolkit_layer_info: CollectionProperty(type=PSDTOOLKIT_psd_object_properties_group_layer)

class PSDTOOLKIT_OT_make_object_properties(Operator):#指定されたオブジェクトのPSDTOOLKIT_psd_object_propertiesの枠組みを作成
    bl_idname = "psdtoolkit.make_psd_object_properties"
    bl_label = "psdtoolkit.make_psd_object_properties"

    object_data_name: StringProperty(name="object_data_name", default="object_data_name")
    layer_nums: StringProperty(name="layer_nums", default="")#1,2,12,...のように親レイヤーごとのレイヤー数をカンマ区切りで指定

    def execute(self, context):
        target_object = context.scene.objects.get(self.object_data_name)
        if target_object is not None:
            layer_nums_list = [int(layer_num) for layer_num in self.layer_nums.split(",")]
            for layer_num in layer_nums_list:
                if layer_num == 0:
                    group_layer = target_object.PSDTOOLKIT_psd_object_properties.psdtoolkit_layer_info.add()
                else:
                    group_layer = target_object.PSDTOOLKIT_psd_object_properties.psdtoolkit_layer_info.add()
                    for i in range(layer_num):
                        group_layer.sublayer.add()
        return {'FINISHED'}

class PSDTOOLKIT_OT_set_object_properties(Operator):#指定されたオブジェクトのPSDTOOLKIT_psd_object_propertiesに要素を上書き更新。
    bl_idname = "psdtoolkit.set_psd_object_properties"
    bl_label = "psdtoolkit.set_psd_object_properties"

    object_data_name: StringProperty(name="object_data_name", default="object_data_name")
    sub_layer: BoolProperty(name="sublayer", default=False)#これがsublayerかどうか
    group_layer_index: IntProperty(name="group_layer_index", default=0)#親レイヤーのインデックス
    sublayer_index: IntProperty(name="sublayer_index", default=0)#子レイヤーのインデックス

    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)
    layer_name: StringProperty(name="name", default="")

    def execute(self, context):
        target_object = context.scene.objects.get(self.object_data_name)
        if target_object is not None:
            if self.sublayer:
                item = target_object.PSDTOOLKIT_psd_object_properties.psdtoolkit_layer_info[self.group_layer_index].sublayer[self.sublayer_index]
                item.x = self.x
                item.y = self.y
                item.visible = self.visible
                item.layer_name = self.layer_name
            else:
                item = target_object.PSDTOOLKIT_object_properties.psdtoolkit_layer_info[self.group_layer_index]
                item.x = self.x
                item.y = self.y
                item.visible = self.visible
                item.layer_name = self.layer_name
        return {'FINISHED'}