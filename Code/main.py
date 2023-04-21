
import math

import pygame

from Source.app import App
from Source.scene import Scene


class SampleScene(Scene):
    def __init__(self):
        self.zoom = 1

    def update(self, dt: int):
        PERIOD = 2000  # perform one zoom cycle every 2 seconds
        t = dt / PERIOD * 2 * math.pi

        # zoom in and out from 0.5 to 1.5
        self.zoom = (math.sin(t) + 1.0) * 0.5 + 0.5

    def draw(self, screen: pygame.Surface):
        edge = 100 * self.zoom # at zoom = 1, edge is 100 pixels

        rect = pygame.Rect(
            (screen.get_width() - edge) / 2,  # left
            (screen.get_height() - edge) / 2,  # top
            edge, edge  # width, height
        )

        # where to draw, color, rectangle
        pygame.draw.rect(screen, (255, 0, 0), rect)


App(
    title="Worlds Around",
    window_size=(800, 600),
    start_scene=SampleScene(),
).run()
