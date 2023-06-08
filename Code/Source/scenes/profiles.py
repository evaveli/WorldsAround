
import pygame

from Source import ui

from Source.profile import Profile
from Source.scene import Scene, SceneContext

from Source.scenes.confirm_delete import ConfirmDelete
from Source.scenes.mainmenu import MainMenu


class ProfileScene(Scene):
    def __init__(self):
        super().__init__()
        self.profile = -1
        self.remove = -1

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
        elif self.profile != -1:
            profile = Profile.load(f"Profile{self.profile}.json")
            self.profile = -1
            return Scene.Push(MainMenu(profile))
        elif self.remove != -1:
            rem = self.remove
            self.remove = -1
            return Scene.Push(ConfirmDelete(rem))

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

        ui.cut_top(body, 150)

        # body
        profiles = ui.hsplit_n(body, 3)

        for i in range(1, 4):
            exists = Profile.exists(f"Profile{i}.json")
            name = f"Profile  {i}" if exists else "NEW GAME"

            top, bottom = ui.vsplit_n(profiles[i - 1], 2)

            if self.ctx.button_layout(ui.center(top), name, self.assets.ARCADE_24):
                self.profile = i

            if exists and self.ctx.button_layout(ui.center(bottom), "DELETE", self.assets.ARCADE_24, pygame.Color(255, 0, 0)):
                self.remove = i

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
