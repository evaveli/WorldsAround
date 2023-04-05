
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from scene import Scene


class Level(Scene):
    def __init__(self, file: str):
        self.map = load_pygame(file)
        pass

    def draw(self, screen: pygame.Surface):
        tw = self.map.tilewidth
        th = self.map.tileheight

        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    image.texture.draw(
                        image.srcrect,
                        (x * tw, y * th, tw, th),
                        image.angle,
                        None,
                        image.flipx,
                        image.flipy,
                    )
