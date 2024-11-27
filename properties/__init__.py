# -*- coding: utf-8 -*-
import bpy
from bpy.props import PointerProperty

from . import psd_obj

classes = (
    psd_obj.PSDTOOLKIT_scene_properties_psdlist_item,
    psd_obj.PSDTOOLKIT_scene_properties,
    psd_obj.PSDTOOLKIT_psd_object_properties_sub5_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties_sub4_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties_sub3_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties_sub2_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties_sub1_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties_top_layer,
    psd_obj.PSDTOOLKIT_psd_object_properties,
    psd_obj.PSDTOOLKIT_OT_add_scene_properties_psd_list,
    psd_obj.PSDTOOLKIT_OT_make_object_properties,
    psd_obj.PSDTOOLKIT_OT_set_object_properties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.PSDTOOLKIT_scene_properties = PointerProperty(type=psd_obj.PSDTOOLKIT_scene_properties)
    bpy.types.Object.PSDTOOLKIT_psd_object_properties = PointerProperty(type=psd_obj.PSDTOOLKIT_psd_object_properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.PSDTOOLKIT_scene_properties
    del bpy.types.Object.PSDTOOLKIT_psd_object_properties