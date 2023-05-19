
import pygame

from Source import ui

from Source.scene import Scene, SceneContext


class ProfileScene(Scene):
    def __init__(self):
        super().__init__()
        # UI state
        self.go_back = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.go_back:
            self.go_back = False
            return Scene.Pop()

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        # header
        head, body = ui.cut_top(rect, 75)

        ui.cut_left(head, 10)
        ui.cut_right(head, 10)
        ui.cut_top(head, 10)

        self.ctx.text_layout(ui.center(head), "Profiles",
                             self.assets.ARCADE_48)

        ui.cut_left(head, 10)
        ui.cut_top(head, 10)

        if self.ctx.button(head, "Back", self.assets.ARCADE_24):
            self.go_back = True
            return

        ui.cut_top(body, 20)
        ui.cut_left(body, 350)

        # body
        profile1, profile2, profile3 = ui.vsplit_n(body, 3)

        if self.ctx.button(profile1, "Profile 1", self.assets.ARCADE_24):
            pass
        if self.ctx.button(profile2, "Profile 2", self.assets.ARCADE_24):
            pass
        if self.ctx.button(profile3, "Profile 3", self.assets.ARCADE_24):
            pass

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
