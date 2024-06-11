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
    "name" : "001_apply_modifier",##
    "author" : "lath",
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
    imp.reload(test_operator)
    imp.reload(test_panel)
else:
    from . import test_operator
    from . import test_panel
    import bpy

import bpy

classes = (
    test_panel.TEST_PT_Panel,
    test_operator.TEST_OT_Apply_All_Op,
    test_operator.TEST_OT_Delete_All_Op
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.register_class(c)

if __name__ == "__main__":
    register()

