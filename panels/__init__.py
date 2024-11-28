# -*- coding: utf-8 -*-
import bpy
from . import tool

classes = (
    tool.PSDTOOL_PT_top_panel,
    tool.PSDTOOL_UL_display_toplayer_frames,
    tool.PSDTOOL_UL_display_sub1layer_frames,
    tool.PSDTOOL_UL_display_sub2layer_frames,
    tool.PSDTOOL_UL_display_sub3layer_frames,
    tool.PSDTOOL_UL_display_sub4layer_frames,
    tool.PSDTOOL_PT_layers_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)