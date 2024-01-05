bl_info = {
    "name": "Map Model",
    "description": "Convert OSM data to 3D models.",
    "author": "Patrick Huang",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar > Map Model",
    "doc_url": "https://github.com/phuang1024/Map3DModel",
    "tracker_url": "https://github.com/phuang1024/Map3DModel/issues",
    "category": "3D View",
}

import bpy

from .interface import *


classes = (
    MapModel_Props,
    MapModel_OT_MakeModel,
    MapModel_PT_Main,
    MapModel_PT_Roads,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mapmodel = bpy.props.PointerProperty(type=MapModel_Props)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mapmodel
