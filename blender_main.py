import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bpy
import numpy as np

from parse import *

ROAD_SCALING = 0.01


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

    for i, node in enumerate(way.nodes):
        x, y = osm.world_to_blender(node.lat, node.lon)
        verts.append((x, y, 0))
        if i != 0:
            edges.append((len(verts) - 2, len(verts) - 1))

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

    #make_all_buildings(osm)
    make_all_roads(osm)


if __name__ == "__main__":
    main()
