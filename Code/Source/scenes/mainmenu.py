
from typing import cast

import pygame

from Source import ui
from Source.scene import Scene
from Source.scene_context import SceneContext

from Source.scenes.settings import SettingsScene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        self.quit = False
        self.to_settings = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.quit:
            self.quit = False
            return Scene.Pop()
        elif self.to_settings:
            self.to_settings = False
            return Scene.Push(SettingsScene())

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        # header
        head, body = ui.cut_top(rect, 100)

        ui.cut_left(head, 10)
        ui.cut_right(head, 10)
        ui.cut_top(head, 150)

        self.ctx.text_layout(
            ui.center(head), "Worlds  Around", self.assets.ARCADE_72)

        _, body = ui.cut_top(body, 150)
        _, body = ui.cut_bottom(body, 150)

        btn1, btn2, btn3 = ui.vsplit_n(body, 3)

        play = self.ctx.button_layout(
            ui.center(btn1), "Play", self.assets.ARCADE_48)
        self.to_settings = self.ctx.button_layout(
            ui.center(btn2), "Settings", self.assets.ARCADE_48)
        self.quit = self.ctx.button_layout(
            ui.center(btn3), "Quit", self.assets.ARCADE_48)

        # ui.cut_left(head, 10)
        # ui.cut_top(head, 50)

    def draw(self, screen: pygame.Surface):
        # render UI
        self.ctx.draw(screen)
