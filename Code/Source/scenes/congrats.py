

import pygame

from Source import ui

from Source.scene import Scene, SceneContext


class CongratsScene(Scene):
    def __init__(self):
        super().__init__()

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        ui.cut_top(rect, 100)

        congrats, what, then = ui.vsplit_n(rect, 3)

        self.ctx.text_layout(
            ui.center(congrats), "Congratulations!", self.assets.ARCADE_48)

        self.ctx.text_layout(
            ui.center(what), "You  have  completed  the  game!", self.assets.ARCADE_48)

        self.ctx.text_layout(
            ui.center(then), "Go  tell  everyone!", self.assets.ARCADE_48)

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
