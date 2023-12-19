import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

import bmesh
import bpy

from parse import *


def plot_node(osm: OSM, node: Node):
    mesh = bpy.data.meshes.new(f"node_{node.id}")
    obj = bpy.data.objects.new(f"node_{node.id}", mesh)
    bpy.context.scene.collection.objects.link(obj)

    verts = []
    x, y = osm.world_to_blender(node.lat, node.lon)
    verts.append((x, y, 0))

    mesh.from_pydata(verts, [], [])


def make_building(osm: OSM, building: Way):
    mesh = bpy.data.meshes.new(f"building_{building.id}")
    obj = bpy.data.objects.new(f"building_{building.id}", mesh)
    bpy.context.scene.collection.objects.link(obj)

    verts = []
    for node in building.nodes:
        x, y = osm.world_to_blender(node.lat, node.lon)
        verts.append((x, y, 0))
    faces = [list(range(len(verts)))]

    mesh.from_pydata(verts, [], faces)


def main():
    path = "complete.osm"
    osm = parse_osm_file(path)
    print(osm.top, osm.left, osm.bottom, osm.right)
    print(osm.scaling_factor)

    """
    for node in osm.nodes.values():
        plot_node(osm, node)
    """

    for way in osm.ways:
        if "building" in way.tags:
            make_building(osm, way)


if __name__ == "__main__":
    main()
