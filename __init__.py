bl_info = {
    "name":"Chris Blender Network Render addon",
    "description":"",
    "blender":(2,80,0),
    "category":"All"
}

import bpy
import socket

from .dataitems import ServerItem, LocalItem
from .renderfile import RenderFile
from .serverpanel import ServerPanel, ServerUIList
from .addremoveoperator import AddRemoveOperator
from .renderserver import RenderServer,RenderThread


#Register all the classes in Blender and set up the Message Property collection
def register() :
    bpy.utils.register_class(LocalItem)
    bpy.utils.register_class(ServerItem)
    bpy.utils.register_class(ServerPanel)
    bpy.utils.register_class(ServerUIList)
    bpy.utils.register_class(AddRemoveOperator)
    bpy.utils.register_class(RenderFile)
    bpy.utils.register_class(RenderServer)
    bpy.types.Scene.MyServerProps = bpy.props.CollectionProperty(type=ServerItem)
    bpy.types.Scene.ActiveServerIndex = bpy.props.IntProperty()
    bpy.types.Scene.NewServerProp = bpy.props.PointerProperty(type=ServerItem)
    bpy.types.Scene.LocalServerProp = bpy.props.PointerProperty(type=LocalItem)
    
    

#Reverse of the above
def unregister() :
    bpy.utils.unregister_class(ServerItem)
    bpy.utils.unregister_class(ServerPanel)
    bpy.utils.unregister_class(ServerUIList)
    bpy.utils.unregister_class(AddRemoveOperator)
    bpy.utils.unregister_class(RenderFile)
    bpy.utils.unregister_class(RenderServer)
    bpy.utils.unregister_class(LocalItem)
    del(bpy.types.Scene.MyServerProps)
    del(bpy.types.Scene.ActiveServerIndex)
    del(bpy.types.Scene.NewServerProp)
    del(bpy.types.Scene.LocalServerProp)

