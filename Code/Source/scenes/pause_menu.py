

import pygame

from Source import ui
from Source.profile import Profile
from Source.scene import Scene
from Source.scene_context import SceneContext

from Source.scenes.settings import SettingsScene


class PauseMenu(Scene):
    def __init__(self, profile: Profile):
        super().__init__()
        self.profile = profile
        # UI state
        self.resume = False
        self.restart = False
        self.to_settings = False
        self.quit = False


    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera
        self.game = ctx

        pygame.mixer.music.pause()

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.resume:
            self.resume = False
            return Scene.Pop()
        elif self.restart:
            self.restart = False
            self.game.restart = True
            # TODO: restart the level
            return Scene.Pop()
        elif self.to_settings:
            self.to_settings = False
            return Scene.Push(SettingsScene(self.profile))
        elif self.quit:
            self.quit = False
            return Scene.PopAll()

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        _, body = ui.cut_top(rect, 100)
        _, body = ui.cut_bottom(body, 100)

        resume, restart, settings, quit = ui.vsplit_n(body, 4)

        self.resume = self.ctx.button_layout(
            ui.center(resume), "Resume", self.assets.ARCADE_48)
        self.restart = self.ctx.button_layout(
            ui.center(restart), "Restart", self.assets.ARCADE_48)
        self.to_settings = self.ctx.button_layout(
            ui.center(settings), "Settings", self.assets.ARCADE_48)
        self.quit = self.ctx.button_layout(
            ui.center(quit), "Quit", self.assets.ARCADE_48)

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
