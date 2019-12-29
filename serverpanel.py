import bpy

class ServerUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=1)
        split.label(text=item.ip_address+":"+str(item.port))
    
    def invoke(self,context,event):
        pass

class ServerPanel(bpy.types.Panel):
	#Just like with operators you need to have a bl_idname blablabla 	
    bl_idname = "panel.server_config_panel"
    bl_label = "Server Panel"
    #Ok a bit different, the space_type specifies the 'window' like Properties, 3D Viewport, Timeline etc etc
    bl_space_type = "PROPERTIES"
    #The region type is a bit complicated, e.g. for 3DViewport you can set Tools and it would be in the tools side panel (collapsed by default)
    bl_region_type = "WINDOW"
    #Also complicated, with properties it specifies the 'tab', if you hover over the icons in Blender you will see their respective context.
    bl_context = "render"

    def draw(self,context):
        props = bpy.context.scene.NewServerProp
        locprop = bpy.context.scene.LocalServerProp
        layout = self.layout
        scn = bpy.context.scene

        row = layout.row()
        inputlocal = row.box()
        inputlocal.label(text='Local render')
        inputlocal.prop(locprop,"percentage")
        inputlocal.prop(locprop,"isauto")
        inputlocal.prop(locprop,"doesrender")

        row1 = layout.row()
        row1.template_list("ServerUIList","",scn,"MyServerProps",scn,"ActiveServerIndex",rows=2)

        row2 = layout.row()
        row2.operator("object.serverlist_action",text="Remove Server").action ='REMOVE'

        row3 = layout.row()
        row3.operator("object.render_file",text='Render File')

        row4 = layout.row()
        inputserv = row4.box()
        inputserv.label(text="Add new server")
        inputserv.prop(props,"ip_address")
        inputserv.prop(props,"port")
        inputserv.prop(props,"percentage")
        inputserv.prop(props,"isauto")
        inputserv.operator("object.serverlist_action",text="Add server").action = "ADD"

