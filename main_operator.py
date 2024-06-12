import bpy
from bpy.types import Operator

class PSDTOOL_OT_psd_import(Operator):
    bl_idname = "psdtool.psd_import"
    bl_label = "psd import"
    bl_description = "import psd and make psd object"

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj.mode == "OBJECT":
            return True
        return False

    def execute(self, context):#これがメインの処理。このオペレータが呼び出されるとこれが実行される
        active_obj = bpy.context.active_object
        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        return {'FINISHED'}
    
class TEST_OT_Delete_All_Op(Operator):
    bl_idname = "test.delete_modifier"
    bl_label = "Delete Modifier"
    bl_description = "Remove modifiers."

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is not None:
            if obj.mode == "OBJECT":
                return True
            return False
        
    def execute(self, context):
        active_obj = bpy.context.active_object
        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=mod.name)
        return {'FINISHED'}