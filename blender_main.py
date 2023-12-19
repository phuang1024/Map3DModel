import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bpy
import numpy as np

from parse import *

ROAD_SCALING = 0.013


def plot_node(osm: OSM, node: Node):
    mesh = bpy.data.meshes.new(f"node_{node.id}")
    obj = bpy.data.objects.new(f"node_{node.id}", mesh)
    bpy.context.scene.collection.objects.link(obj)

    verts = []
    x, y = osm.world_to_blender(node.lat, node.lon)
    verts.append((x, y, 0))

    mesh.from_pydata(verts, [], [])


def make_all_buildings(osm: OSM):
    mesh = bpy.data.meshes.new("buildings")
    obj = bpy.data.objects.new("buildings", mesh)
    bpy.context.scene.collection.objects.link(obj)

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


def get_road_width(key: str) -> float | None:
    """
    None if not a valid road for our purposes.
    """
    if key.startswith("motorway"):
        return 5
    if key.startswith("trunk"):
        return 4
    if key.startswith("primary"):
        return 3.2
    if key.startswith("secondary"):
        return 2.4
    if key.startswith("tertiary"):
        return 1.6
    if key in ("residential", "unclassified"):
        return 1

def make_road(osm: OSM, way: Way, verts, edges, faces):
    width = get_road_width(way.tags["highway"])
    assert width is not None
    width *= ROAD_SCALING

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

def make_all_roads(osm: OSM):
    mesh = bpy.data.meshes.new("roads")
    obj = bpy.data.objects.new("roads", mesh)
    bpy.context.scene.collection.objects.link(obj)

    verts = []
    edges = []
    faces = []

    for way in osm.ways:
        if "highway" in way.tags:
            if get_road_width(way.tags["highway"]) is not None:
                make_road(osm, way, verts, edges, faces)

    mesh.from_pydata(verts, edges, faces)


def main():
    path = "./Blaney_Johnson_Bollinger_Rainbow.osm"
    osm = parse_osm_file(path)

    make_all_buildings(osm)
    make_all_roads(osm)


if __name__ == "__main__":
    main()
