
from dataclasses import dataclass
from pygame import Rect

from Source.entity import Component
from Source.image_cache import TextureId


@dataclass
class Position(Component):
    x: float = 0
    y: float = 0


@dataclass
class Size(Component):
    w: int = 0
    h: int = 0


@dataclass
class Sprite(Component):
    rect: Rect
    uid: TextureId = TextureId(-1) # the id of the sprite in the ImageCache
