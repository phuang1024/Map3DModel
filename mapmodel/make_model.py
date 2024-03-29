import bpy
import numpy as np

from .parse_osm import *


def plot_node(context, osm: OSM, node: Node):
    mesh = bpy.data.meshes.new(f"node_{node.id}")
    obj = bpy.data.objects.new(f"node_{node.id}", mesh)
    context.scene.collection.objects.link(obj)

    verts = []
    x, y = osm.world_to_blender(node.lat, node.lon)
    verts.append((x, y, 0))

    mesh.from_pydata(verts, [], [])


def make_all_buildings(context, osm: OSM):
    mesh = bpy.data.meshes.new("buildings")
    obj = bpy.data.objects.new("buildings", mesh)
    context.scene.collection.objects.link(obj)

    i = 0
    verts = []
    faces = []
    for way in osm.ways:
        if "building" in way.tags:
            i_start = i
            for node in way.nodes:
                x, y = osm.world_to_blender(node.lat, node.lon)
                verts.append((x, y, 0))
                i += 1
            faces.append(range(i_start, i))

    mesh.from_pydata(verts, [], faces)


def get_road_width(context, key: str) -> float | None:
    """
    None if not a valid road for our purposes.
    """
    p = context.scene.mapmodel
    if key.startswith("motorway") and p.motorway_enabled:
        return p.motorway_width
    elif key.startswith("trunk") and p.trunk_enabled:
        return p.trunk_width
    elif key.startswith("primary") and p.primary_enabled:
        return p.primary_width
    elif key.startswith("secondary") and p.secondary_enabled:
        return p.secondary_width
    elif key.startswith("tertiary") and p.tertiary_enabled:
        return p.tertiary_width
    elif key.startswith("residential") and p.residential_enabled:
        return p.residential_width
    elif key in ("unclassified", "track", "footway", "cycleway", "path") and p.footway_enabled:
        return p.footway_width

def make_road(context, osm: OSM, way: Way, verts, edges, faces):
    width = get_road_width(context, way.tags["highway"])
    assert width is not None
    width *= context.scene.mapmodel.road_scaling * 0.01

    for i, node in enumerate(way.nodes):
        # Get unit vector following curve at this node.
        # If an edge node, use the tangent of the edge.
        # If a middle node, use the connecting line between the two neighbors.
        loc_this = np.array(osm.world_to_blender(node.lat, node.lon))
        if i > 0:
            node_prev = way.nodes[i - 1]
            loc_prev = np.array(osm.world_to_blender(node_prev.lat, node_prev.lon))
        if i < len(way.nodes) - 1:
            node_next = way.nodes[i + 1]
            loc_next = np.array(osm.world_to_blender(node_next.lat, node_next.lon))
        if i == 0:
            tangent = loc_next - loc_this
        elif i == len(way.nodes) - 1:
            tangent = loc_this - loc_prev
        else:
            tangent = loc_next - loc_prev
        tangent /= np.linalg.norm(tangent)

        left = np.array([-tangent[1], tangent[0]]) * width
        right = -left
        left = loc_this + left
        right = loc_this + right
        left = (left[0], left[1], 0)
        right = (right[0], right[1], 0)

        verts.append(left)
        verts.append(right)
        if i != 0:
            faces.append([len(verts) - 4, len(verts) - 2, len(verts) - 1, len(verts) - 3])

def make_all_roads(context, osm: OSM):
    mesh = bpy.data.meshes.new("roads")
    obj = bpy.data.objects.new("roads", mesh)
    context.scene.collection.objects.link(obj)

    verts = []
    edges = []
    faces = []

    for way in osm.ways:
        if "highway" in way.tags:
            if get_road_width(context, way.tags["highway"]) is not None:
                make_road(context, osm, way, verts, edges, faces)

    mesh.from_pydata(verts, edges, faces)


def make_model_main(context):
    path = bpy.path.abspath(context.scene.mapmodel.osm_path)
    osm = parse_osm_file(path)
    osm.blender_size = context.scene.mapmodel.world_size

    if context.scene.mapmodel.make_buildings:
        make_all_buildings(context, osm)
    if context.scene.mapmodel.make_roads:
        make_all_roads(context, osm)
