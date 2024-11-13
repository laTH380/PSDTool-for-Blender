import bpy
from bpy.props import FloatProperty, CollectionProperty, IntProperty, StringProperty, BoolProperty
from bpy.types import PropertyGroup, Operator

#名前解決が大事なので同じものを指すときは必ず同じ名前にする
#プロパティグループを継承することで、カスタムプロパティを定義できる

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
class PSDTOOLKIT_object_properties_layer_info_item(PropertyGroup):
    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)

class PSDTOOLKIT_object_properties_layer_info(PropertyGroup):
    sublayer_info: CollectionProperty(type=PSDTOOLKIT_object_properties_layer_info_item)

class PSDTOOLKIT_object_properties(PropertyGroup):
    psdtoolkit_layer_info: CollectionProperty(type=PSDTOOLKIT_object_properties_layer_info)

class PSDTOOLKIT_OT_add_object_properties_layer_info(Operator):#指定されたオブジェクトのpsdtoolkit_layer_infoプロパティの最下層の一番最後に要素を追加していく。change_parent_layerがTrueのときはペアレントレイヤーに要素を追加してから処理を行う。
    bl_idname = "psdtoolkit.add_object_properties_layer_info"
    bl_label = "Add layer info"

    object_data_name: StringProperty(name="object_data_name", default="object_data_name")
    change_parent_layer: BoolProperty(name="change_parent_layer_flag", default=False)

    x: IntProperty(name="x", default=0)
    y: IntProperty(name="y", default=0)
    visible: BoolProperty(name="visible", default=True)

    def execute(self, context):
        target_object = context.scene.objects.get(self.object_data_name)
        if target_object is not None:
            if self.change_parent_layer:
                item = target_object.PSDTOOLKIT_object_properties.psdtoolkit_layer_info.add().add()
                item.x = self.x
                item.y = self.y
                item.visible = self.visible
            else:
                item = target_object.PSDTOOLKIT_object_properties.psdtoolkit_layer_info[-1].add()
                item.x = self.x
                item.y = self.y
                item.visible = self.visible
        return {'FINISHED'}