
from typing import cast

import pygame

from Source import ui
from Source.scene import Scene

from Source.assets import Assets, FailedToLoadAssets
from Source.font_cache import FontCache, FontId
from Source.image_cache import ImageCache, TextureId


from Source.scenes.settings import SettingsScene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        self.quit = False
        self.to_settings = False

    def enter(self,  assets: Assets, ui: ui.Context):
        self.assets = assets
        self.ctx = ui

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

        black = pygame.Color(0, 0, 0)
        self.ctx.text_layout(ui.center(head), "Worlds Around",
                             self.assets.SYSTEM_72, black)

        ui.cut_left(body, 10)
        ui.cut_right(body, 10)
        ui.cut_top(body, 70)

        btn1, btn2, btn3 = ui.vsplit_n(body, 3)

        play = self.ctx.button_layout(
            ui.center(btn1), "Play", self.assets.SYSTEM_48, black)
        settings = self.ctx.button_layout(
            ui.center(btn2), "Settings", self.assets.SYSTEM_48, black)
        quitBtn = self.ctx.button_layout(
            ui.center(btn3), "Quit", self.assets.SYSTEM_48, black)

        if settings:
            self.to_settings = True
            return

        if quitBtn:
            self.quit = True
            return

        # ui.cut_left(head, 10)
        # ui.cut_top(head, 50)

    def draw(self, screen: pygame.Surface):
        # render UI
        screen.fill((255, 255, 255))
        self.ctx.draw(screen)
