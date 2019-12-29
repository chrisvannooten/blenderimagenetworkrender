import bpy
import re

class AddRemoveOperator(bpy.types.Operator):
    bl_idname = "object.serverlist_action"
    bl_label = "Server List Actions"
    bl_description = "Add and remove servers"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))
    
    def invoke(self, context, event):
        scn = context.scene
        idx = scn.ActiveServerIndex

        try:
            item = scn.MyServerProps[idx]
        except IndexError:
            pass
        else:
            if self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.MyServerProps[idx].ip_address)
                scn.ActiveServerIndex -= 1
                scn.MyServerProps.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            ippattern = re.compile(r'^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')
            if bpy.context.scene.NewServerProp.ip_address != "" and ippattern.search(bpy.context.scene.NewServerProp.ip_address):
                item = scn.MyServerProps.add()
                item.ip_address = bpy.context.scene.NewServerProp.ip_address
                item.port = bpy.context.scene.NewServerProp.port
                item.percentage = bpy.context.scene.NewServerProp.percentage
                item.isauto = bpy.context.scene.NewServerProp.isauto
                bpy.context.scene.NewServerProp.ip_address = ""
                bpy.context.scene.NewServerProp.port = 65432

        return {"FINISHED"}
