import bpy

from .make_model import make_model_main


class MapModel_Props(bpy.types.PropertyGroup):
    osm_path: bpy.props.StringProperty(
        name="OSM File",
        description="Path to the OSM file.",
        subtype="FILE_PATH",
    )

    world_size: bpy.props.FloatProperty(
        name="World Size",
        description="Size of the model.",
        default=10,
        min=0,
        soft_max=100,
    )

    road_scaling: bpy.props.FloatProperty(
        name="Road Scaling",
        description="Scaling factor for road width.",
        default=1,
        min=0,
        soft_max=5,
    )

    make_buildings: bpy.props.BoolProperty(
        name="Make Buildings",
        description="Make buildings.",
        default=True,
    )

    make_roads: bpy.props.BoolProperty(
        name="Make Roads",
        description="Make roads.",
        default=True,
    )


class MapModel_OT_MakeModel(bpy.types.Operator):
    bl_idname = "mapmodel.make_model"
    bl_label = "Make Model"
    bl_description = "Make object(s) from OSM file"

    def execute(self, context):
        make_model_main(context)
        return {"FINISHED"}


class MapModel_BasePanel:
    """
    Common properties.
    """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MapModel"
    bl_options = {"DEFAULT_CLOSED"}


class MapModel_PT_Main(MapModel_BasePanel, bpy.types.Panel):
    bl_idname = "MapModel_PT_Main"
    bl_label = "MapModel"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.mapmodel, "osm_path")
        layout.separator()
        layout.prop(context.scene.mapmodel, "road_scaling")
        layout.prop(context.scene.mapmodel, "world_size")
        layout.separator()
        layout.prop(context.scene.mapmodel, "make_buildings")
        layout.prop(context.scene.mapmodel, "make_roads")
        layout.separator()
        layout.operator("mapmodel.make_model")
