from dataclasses import dataclass
import xml.etree.ElementTree as ET

import numpy as np


@dataclass
class Node:
    id: int
    lat: float
    lon: float


@dataclass
class Way:
    id: int
    nodes: list[Node]
    tags: dict[str, str]


@dataclass
class Relation:
    # TODO
    pass


@dataclass
class OSM:
    nodes: dict[int, Node]
    # TODO maybe make ways and relations dicts.
    ways: list[Way]
    relations: list[Relation]

    # lat and lon bounds
    top: float
    left: float
    bottom: float
    right: float

    # Size (blender units) of X side (longitude difference).
    # Y is calculated from aspect.
    blender_size: float = 10
    # Additional scaling applied to Y direction; compensate for distortion.
    scaling_factor: float = 1

    def world_to_blender(self, lat, lon):
        bl_x_size = self.blender_size
        bl_y_size = self.scaling_factor * bl_x_size * (self.top - self.bottom) / (self.right - self.left)
        x = np.interp(lon, [self.left, self.right], [-bl_x_size / 2, bl_x_size / 2])
        y = np.interp(lat, [self.top, self.bottom], [bl_y_size / 2, -bl_y_size / 2])
        return x, y


def parse_osm(root):
    """
    root: tree.getroot()
    x_metric: Diff in longitude for a fixed distance.
    y_metric: Diff in latitude for that same fixed distance.
    """
    nodes = {}
    ways = []
    relations = []

    top = float("inf")
    left = float("inf")
    bottom = float("-inf")
    right = float("-inf")

    for child in root:
        if child.tag == "node":
            id = int(child.attrib["id"])
            lat = float(child.attrib["lat"])
            lon = float(child.attrib["lon"])
            nodes[id] = Node(
                id=id,
                lat=lat,
                lon=lon,
            )

            top = min(top, lat)
            left = min(left, lon)
            bottom = max(bottom, lat)
            right = max(right, lon)

        elif child.tag == "way":
            way = Way(
                id=int(child.attrib["id"]),
                nodes=[],
                tags={},
            )
            for subchild in child:
                if subchild.tag == "nd":
                    way.nodes.append(nodes[int(subchild.attrib["ref"])])
                elif subchild.tag == "tag":
                    way.tags[subchild.attrib["k"]] = subchild.attrib["v"]
            ways.append(way)

        elif child.tag == "relation":
            # TODO
            pass

    # TODO explain this
    scaling = 1 / np.cos(np.radians(top))

    return OSM(
        nodes=nodes,
        ways=ways,
        relations=relations,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        scaling_factor=scaling,
    )


def parse_osm_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return parse_osm(root)


if __name__ == "__main__":
    path = "test2.osm"
    data = parse_osm_file(path)
    for way in data.ways:
        if "building" not in way.tags:
            print(way)
