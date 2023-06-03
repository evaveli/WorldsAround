
from dataclasses import dataclass
import json
from typing import Callable, NewType

from Source.entity import Component, Entity
from Source.entity_list import EntityList
from Source.image_cache import ImageCache, TextureId

# TODO:
# objects and layers would be nice

"""
    map format specification

    map file format:
        - name: str                 # name of the map
        # path to the background image, relative to "Resources/Images"
        - background: Optional[str]
        - width: int                # width of the map in pixels
        - tileset: Tileset          # tileset used by the map
        - tiles: list[TileId]       # list of tiles in the map

    tileset file format:
        - name: str                 # name of the tileset
        - image: str                # path to the tileset image, relative to "Resources/Images"
        - tile_size: (int, int)     # size of a tile in pixels
        - tiles: dict[TileId, Tile] # mapping from tile id to tile

    tile format:
        - offset: (int, int)         # offset of the tile in the tileset image
        # mapping from property name to property value
        - properties: dict[str, str]
"""

TileId = NewType("TileId", int)
"""
    A tile ID is an integer that uniquely identifies a tile.
"""

NULL_TILE = 0
"""
    The null tile is a tile that is always empty.
"""


PropertyParser = Callable[[str], Component]
"""
    A property parser is a mapping from property name to a parsed component for an object.
"""


@dataclass
class Tag(Component):
    name: str


@dataclass
class Tile:
    """
        A tile is a rectangular area in a tileset.
    """
    offset: tuple[int, int]
    properties: dict[str, str]


@dataclass
class Tileset:
    """
        A tileset is a collection of tiles.
    """
    name: str
    image: TextureId
    tile_size: tuple[int, int]
    tiles: dict[TileId, Tile]


@dataclass
class TileMap:
    """
        A tile map is a collection of tiles.
    """
    name: str
    background: TextureId | None
    width: int
    tileset: Tileset
    tiles: list[TileId]
    objects: EntityList

    @staticmethod
    def __default_property_parser(name: str) -> Component:
        """
            The default property parser.
        """
        return Tag(name)

    @staticmethod
    def load(file: str, images: ImageCache, parser: PropertyParser = __default_property_parser) -> "TileMap":
        """
            Load a tile map from a file.
        """
        with open(file, "r") as handle:
            data = json.load(handle)

            bg = data.get("background", None)
            ts = json.load(open("./Resources/Maps/" + data["tileset"], "r"))

            return TileMap(
                name=data["name"],
                background=bg,
                width=int(data["width"]),
                tileset=Tileset(
                    name=ts["name"],
                    image=images.load(ts["image"]),
                    tile_size=ts["tile_size"],
                    tiles={
                        TileId(int(tile["tid"])): Tile(
                            offset=tile["offset"],
                            properties=tile.get("properties", {})
                        )
                        for tile in ts["tiles"]
                    }
                ),
                tiles=[
                    TileId(int(tile)) for tile in data["tiles"]
                ],
                objects=EntityList(
                    Entity(
                        parser(name) for name in obj["properties"].keys()
                    )
                    for obj in data["objects"]
                ) if "objects" in data else EntityList()
            )
