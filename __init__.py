# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "PSDtool-for-blender",
    "author" : "laTH380",
    "description" : "",
    "blender" : (3, 6, 11),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import os
import sys
   
# PYTHONPATHにex-libraryを追加
basepath = os.path.split(os.path.realpath(__file__))[0]
print(os.path.join(basepath, 'ex-library'))
sys.path.insert(0, os.path.join(basepath, 'ex-library'))
sys.path.insert(0, basepath)

# PILモジュールのロード
import PIL
from PIL import Image


if "bpy" in locals():
    import imp
    imp.reload(main_operator)
    imp.reload(ui_panel)
    imp.reload(control_property)
    imp.reload(process_psd)
    imp.reload(io_import_psd_as_planes)
else:
    from . import main_operator
    from . import ui_panel
    from . import control_property
    from . import process_psd
    from . import io_import_psd_as_planes
    import bpy

import bpy
from bpy.props import PointerProperty, StringProperty, IntProperty

classes = (
    #data
    control_property.PSDTOOLKIT_scene_properties_psdlist_item,
    control_property.PSDTOOLKIT_scene_properties,
    control_property.PSDTOOLKIT_object_properties_layer_info_item,
    control_property.PSDTOOLKIT_object_properties_layer_info,
    control_property.PSDTOOLKIT_object_properties,
    #ui
    ui_panel.PSDTOOL_PT_Panel,
    #operator
    control_property.PSDTOOLKIT_OT_add_scene_properties_psd_list,
    control_property.PSDTOOLKIT_OT_add_object_properties_layer_info,
    io_import_psd_as_planes.PSDTOOLKIT_OT_import_psd
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.PSDTOOLKIT_scene_properties = PointerProperty(type=control_property.PSDTOOLKIT_scene_properties)
    bpy.types.Object.PSDTOOLKIT_object_properties = PointerProperty(type=control_property.PSDTOOLKIT_object_properties)

def unregister():
    for c in classes:
        bpy.utils.register_class(c)
    del bpy.types.Scene.PSDTOOLKIT_scene_properties
    del bpy.types.Object.PSDTOOLKIT_object_properties

if __name__ == "__main__":
    register()

#わからなくなるのでアドオン名を使う場合はid以外すべて大文字で
