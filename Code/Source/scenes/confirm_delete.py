

import pygame

from Source import ui

from Source.profile import Profile
from Source.scene import Scene, SceneContext


class ConfirmDelete(Scene):
    def __init__(self, profile: int):
        super().__init__()
        self.profile = profile

        # UI state
        self.cancel = False
        self.confirm = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.cancel or self.confirm:
            return Scene.Pop()
        
        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        ui.cut_top(rect, 200)

        head, body = ui.cut_top(rect, 150)

        self.ctx.text_layout(
            ui.center(head), f"Delete    Profile    {self.profile}?", self.assets.ARCADE_48)

        yes, no = ui.hsplit_n(body, 2)

        ui.cut_left(yes, 10)
        ui.cut_right(yes, 10)

        ui.cut_left(no, 10)
        ui.cut_right(no, 10)

        ui.cut_top(yes, 10)
        ui.cut_top(no, 10)

        if self.ctx.button_layout(ui.center(yes), "Yes", self.assets.ARCADE_48):
            Profile.delete(f"Profile{self.profile}.json")
            self.confirm = True

        if self.ctx.button_layout(ui.center(no), "No", self.assets.ARCADE_48):
            self.cancel = True

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
