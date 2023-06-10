
from dataclasses import dataclass
from pygame import Rect

from Source.entity import Component
from Source.image_cache import TextureId


@dataclass
class Position(Component):
    x: float = 0
    y: float = 0


@dataclass
class Velocity(Component):
    x: float = 0
    y: float = 0


@dataclass
class Size(Component):
    w: int = 0
    h: int = 0


@dataclass
class Sprite(Component):
    rect: Rect
    uid: TextureId = TextureId(-1)  # the id of the sprite in the ImageCache
    flip: bool = False


@dataclass
class Name(Component):
    name: str


@dataclass
class Animation:
    start: tuple[int, int] = (0, 0)
    frames: int = 1000
    duration: int = 1
    loop: bool = True


class Animator(Component):
    anims: dict[str, Animation]
    active: str
    elapsed: int = 0

    def __init__(self, anims: dict[str, Animation], active: str):
        self.anims = anims
        self.active = active

    def transition(self, name: str):
        self.elapsed = 0
        self.active = name
