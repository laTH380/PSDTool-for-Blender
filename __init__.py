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

##########################
# PSDTool for Blender
##########################

bl_info = {
    "name" : "PSDTool for Blender",
    "author" : "laTH380",
    "description" : "",
    "version" : (1, 3, 0),
    "blender" : (3, 6, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import os
import sys
import importlib
import importlib.util

import bpy
from bpy.types import AddonPreferences

# PYTHONPATHにex-libraryを追加（Pythonバージョン別フォルダを優先）
basepath = os.path.split(os.path.realpath(__file__))[0]


def _get_exlibrary_path():
    exlibrary_root = os.path.join(basepath, "ex-library")
    py_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
    versioned_path = os.path.join(exlibrary_root, py_tag)

    if os.path.isdir(versioned_path):
        return versioned_path
    if os.path.isdir(exlibrary_root):
        return exlibrary_root
    return None


selected_exlibrary = _get_exlibrary_path()
if selected_exlibrary:
    print(f"[PSDTool] ex-library path: {selected_exlibrary}")
    sys.path.insert(0, selected_exlibrary)
else:
    print("[PSDTool] ex-library path not found")

sys.path.insert(0, basepath)


_REQUIRED_MODULES = ("PIL", "psd_tools")
_missing_dependencies = [name for name in _REQUIRED_MODULES if importlib.util.find_spec(name) is None]
_loaded_feature_modules = []

modules = [
    "panels",
    "properties",
    "operators"
]


class PSDTOOL_preferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        if _missing_dependencies:
            layout.label(text="PSDTool dependencies are missing:", icon='ERROR')
            for module_name in _missing_dependencies:
                layout.label(text=f"- {module_name}")
            layout.separator()
            layout.label(text="Install requirements.txt into Blender Python and re-enable the addon.")
        else:
            layout.label(text="Dependencies are ready.", icon='CHECKMARK')


classes = (
    PSDTOOL_preferences,
)


# 翻訳辞書
translations = {
    "ja_JP": {
        ("*", "Import Psd as Planes"): "PSDファイルを画像として追加",
        ("*", "Object ID"): "オブジェクトID",
        ("*", "Object Name"): "オブジェクト名",
        ("*", "Target Object Name"): "ターゲットオブジェクト名",
    }
}


def _register_translations_safely():
    # VSCode addon loader で再読み込み時に残存キャッシュがある場合に備える
    try:
        bpy.app.translations.unregister(__name__)
    except ValueError:
        pass
    bpy.app.translations.register(__name__, translations)


def _unregister_translations_safely():
    try:
        bpy.app.translations.unregister(__name__)
    except ValueError:
        pass


def _load_feature_modules():
    loaded = []
    if _missing_dependencies:
        return loaded

    if "bpy" in locals():
        for module in modules:
            if module in locals():
                importlib.reload(locals()[module])
                loaded.append(locals()[module])
            else:
                loaded.append(importlib.import_module(__name__ + "." + module))
    else:
        for module in modules:
            loaded.append(importlib.import_module(__name__ + "." + module))
    return loaded


def register():
    global _loaded_feature_modules

    for c in classes:
        bpy.utils.register_class(c)

    _register_translations_safely()

    if _missing_dependencies:
        print(
            "[PSDTool] Missing dependencies: "
            + ", ".join(_missing_dependencies)
            + ". Install requirements.txt into Blender Python."
        )
        return

    _loaded_feature_modules = _load_feature_modules()
    for module in _loaded_feature_modules:
        module.register()


def unregister():
    global _loaded_feature_modules

    if not _missing_dependencies:
        for module in reversed(_loaded_feature_modules):
            module.unregister()
        _loaded_feature_modules = []

    _unregister_translations_safely()

    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()

#わからなくなるのでアドオン名を使う場合はid以外すべて大文字/小文字で
