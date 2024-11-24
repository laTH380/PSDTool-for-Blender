# -*- coding: utf-8 -*-
import bpy
from . import io_import_psd_as_planes
from . import psd_obj

classes = (
    io_import_psd_as_planes.PSDTOOLKIT_OT_import_psd,
    # psd_obj.PSDTOOL_OT_toggle_visibility,
)

def import_psds_button(self, context):
    self.layout.operator(
        io_import_psd_as_planes.PSDTOOLKIT_OT_import_psd.bl_idname, 
        text="Import Psd as Planes", 
        icon='TEXTURE'
    )

def register():
    print("register operatoraaaaaaaaaaaaaaaaaaaaaaaa")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(import_psds_button)
    bpy.types.VIEW3D_MT_image_add.append(import_psds_button)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(import_psds_button)
    bpy.types.VIEW3D_MT_image_add.remove(import_psds_button)