import bpy

class ServerItem(bpy.types.PropertyGroup):
    ip_address: bpy.props.StringProperty(name="Server IPv4")
    port : bpy.props.IntProperty(name="Server Port", default=65432)
    percentage:bpy.props.FloatProperty(name="Percentage",default=0,max=100,min=0,precision=2)
    isauto : bpy.props.BoolProperty(name="Auto calculate Percentage",default=False)
    startx: bpy.props.FloatProperty(name="Start X border",max=1,min=0,precision=4)
    endx: bpy.props.FloatProperty(name="End X border",max=1,min=0,precision=4)
    threadid: bpy.props.IntProperty(name="Thread id")
    isdone : bpy.props.BoolProperty(default=False)

class LocalItem(bpy.types.PropertyGroup):
    percentage:bpy.props.FloatProperty(name="Percentage",default=0,max=100,min=0,precision=2)
    isauto : bpy.props.BoolProperty(name="Auto calculate Percentage",default=False)
    startx: bpy.props.FloatProperty(name="Start X border",max=1,min=0,precision=4)
    endx: bpy.props.FloatProperty(name="End X border",max=1,min=0,precision=4)
    doesrender: bpy.props.BoolProperty(name="Render locally",default=False)