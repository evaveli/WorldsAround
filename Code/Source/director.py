
import sys
from typing import cast

from pygame import event
import pygame

from Source.assets import Assets, FailedToLoadAssets
from Source.font_cache import FontCache
from Source.image_cache import ImageCache
from Source import ui
from Source.scene import Scene


class Director:
    def __init__(self):
        self.scenes: list[Scene] = []

        self.images = ImageCache()
        self.fonts = FontCache()
        self._assets = Assets.load(self.images, self.fonts)

        if isinstance(self._assets, FailedToLoadAssets):
            raise Exception(f"Failed to load assets: {self._assets.asset}")

        self.assets: Assets = cast(Assets, self._assets)

        self.ui = ui.Context(self.images, self.fonts)

    def push(self, scene: Scene):
        if len(self.scenes) > 0:
            self.scenes[-1].exit()

        self.scenes.append(scene)
        self.scenes[-1].enter(self.assets, self.ui)

    def pop(self):
        self.scenes[-1].exit()
        self.scenes.pop()

        if len(self.scenes) == 0:
            pygame.quit()
            sys.exit(0)

        self.scenes[-1].enter(self.assets, self.ui)

    def input(self, event: event.Event):
        cmd = self.scenes[-1].input(event)
        if isinstance(cmd, Scene.Push):
            self.push(cmd.scene)
        elif isinstance(cmd, Scene.Pop):
            self.pop()

    def update(self, dt: int):
        self.scenes[-1].update(dt)

    def draw(self, screen: pygame.Surface):
        self.scenes[-1].draw(screen)
