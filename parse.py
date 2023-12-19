from dataclasses import dataclass
import xml.etree.ElementTree as ET


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


def parse_osm(root):
    """
    root is tree.getroot()
    """
    nodes = []
    ways = []
    relations = []
    for child in root:
        if child.tag == "node":
            nodes.append(Node(
                id=int(child.attrib["id"]),
                lat=float(child.attrib["lat"]),
                lon=float(child.attrib["lon"]),
            ))

        elif child.tag == "way":
            way = Way(
                id=int(child.attrib["id"]),
                nodes=[],
                tags={},
            )
            for subchild in child:
                if subchild.tag == "nd":
                    way.nodes.append(subchild.attrib["ref"])
                elif subchild.tag == "tag":
                    way.tags[subchild.attrib["k"]] = subchild.attrib["v"]
            ways.append(way)

        elif child.tag == "relation":
            # TODO
            pass

    return {
        "nodes": nodes,
        "ways": ways,
        "relations": relations,
    }


if __name__ == "__main__":
    path = "test.osm"

    tree = ET.parse(path)
    root = tree.getroot()
    data = parse_osm(root)

    for node in data["nodes"]:
        print(node)

    for way in data["ways"]:
        print(way)
