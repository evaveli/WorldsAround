

import pygame

from Source import ui
from Source.scene import Scene
from Source.scene_context import SceneContext
from Source.profile import Profile


class GameOver(Scene):
    def __init__(self):
        super().__init__()

        # UI state
        self.quit = False
        self.restart = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.quit:
            return Scene.PopAll()
        elif self.restart:
            return Scene.Pop()

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        ui.cut_top(rect, 100)

        head, body = ui.cut_top(rect, 150)

        self.ctx.text_layout(
            ui.center(head), "GAME    OVER", self.assets.ARCADE_72)

        ui.cut_top(body, 50)
        ui.cut_bottom(body, 100)

        restart, quit = ui.vsplit_n(body, 2)

        self.restart = self.ctx.button_layout(
            ui.center(restart), "RESTART", self.assets.ARCADE_48)
        self.quit = self.ctx.button_layout(
            ui.center(quit), "QUIT", self.assets.ARCADE_48)

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
