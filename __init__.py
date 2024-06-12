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
   
# PYTHONPATHにzipファイルを追加
basepath = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, os.path.join(basepath, 'ex-library.zip'))

if "bpy" in locals():
    import imp
    imp.reload(main_operator)
    imp.reload(ui_panel)
    imp.reload(io_import_psd_as_planes)
else:
    from . import main_operator
    from . import ui_panel
    from . import io_import_psd_as_planes
    import bpy

import bpy

classes = (
    ui_panel.PSDTOOL_PT_Panel,
    # main_operator.TEST_OT_Apply_All_Op,
    io_import_psd_as_planes.IMPORT_IMAGE_OT_to_plane
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.register_class(c)

if __name__ == "__main__":
    register()

