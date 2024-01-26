import bpy

from .make_model import make_model_main

ROAD_TYPES = (
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "footway",
)

DEFAULT_WIDTHS = (
    2.7,
    2.4,
    2.1,
    1.7,
    1.4,
    1,
    1,
)


class MAPMODEL_Props(bpy.types.PropertyGroup):
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

    for _name, _default_width in zip(ROAD_TYPES, DEFAULT_WIDTHS):
        exec(f"{_name}_enabled: bpy.props.BoolProperty(name='{_name}', default=True)")
        exec(f"{_name}_width: bpy.props.FloatProperty(name='{_name} Width', default={_default_width}, min=0, soft_max=10)")


class MAPMODEL_OT_MakeModel(bpy.types.Operator):
    bl_idname = "mapmodel.make_model"
    bl_label = "Make Model"
    bl_description = "Make object(s) from OSM file"

    def execute(self, context):
        make_model_main(context)
        return {"FINISHED"}


class MAPMODEL_BasePanel:
    """
    Common properties.
    """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MapModel"
    bl_options = {"DEFAULT_CLOSED"}


class MAPMODEL_PT_Main(MAPMODEL_BasePanel, bpy.types.Panel):
    bl_idname = "MAPMODEL_PT_Main"
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


class MAPMODEL_PT_Roads(MAPMODEL_BasePanel, bpy.types.Panel):
    bl_idname = "MAPMODEL_PT_Roads"
    bl_parent_id = "MAPMODEL_PT_Main"
    bl_label = "Roads"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Road visibility and widths.")

        for name in ROAD_TYPES:
            row = layout.row()
            row.prop(context.scene.mapmodel, f"{name}_enabled", text=name.capitalize())
            col = row.column()
            col.enabled = getattr(context.scene.mapmodel, f"{name}_enabled")
            col.prop(context.scene.mapmodel, f"{name}_width", text="")
