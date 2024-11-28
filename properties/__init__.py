# -*- coding: utf-8 -*-
import bpy
from bpy.props import PointerProperty

from . import psd_obj

classes = (
    psd_obj.PSDTOOL_scene_properties,
    psd_obj.PSDTOOL_psd_object_properties_sub5_layer,
    psd_obj.PSDTOOL_psd_object_properties_sub4_layer,
    psd_obj.PSDTOOL_psd_object_properties_sub3_layer,
    psd_obj.PSDTOOL_psd_object_properties_sub2_layer,
    psd_obj.PSDTOOL_psd_object_properties_sub1_layer,
    psd_obj.PSDTOOL_psd_object_properties_top_layer,
    psd_obj.PSDTOOL_psd_object_properties,
    psd_obj.PSDTOOL_OT_make_object_properties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.PSDTOOL_scene_properties = PointerProperty(type=psd_obj.PSDTOOL_scene_properties)
    bpy.types.Object.PSDTOOL_psd_object_properties = PointerProperty(type=psd_obj.PSDTOOL_psd_object_properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.PSDTOOL_scene_properties
    del bpy.types.Object.PSDTOOL_psd_object_properties