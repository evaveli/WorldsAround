

import pygame

from Source import ui

from Source.profile import Profile
from Source.scene import Scene, SceneContext

DUMMY_EVENT = pygame.event.Event(pygame.USEREVENT, kind="dummy")


class LivesScene(Scene):
    def __init__(self, lives: int):
        super().__init__()
        self.lives = lives

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

        self.timer = 0
        ctx.restart = True

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        return Scene.Pop() if self.timer > 1500 else Scene.Continue()

    def update(self, dt: int):
        self.timer += dt

        if self.timer > 1500:
            # trigger a dummy event so that `input` is called
            pygame.event.post(DUMMY_EVENT)

        pygame.display.get_surface().fill((0, 0, 0))

        rect = pygame.display.get_surface().get_rect()

        ui.cut_top(rect, 250)
        ui.cut_bottom(rect, 250)
        ui.cut_left(rect, 250)

        self.ctx.image(
            rect, self.assets.ITEMS, pygame.Rect(0, 0, 16, 16))

        # ui.cut_top(rect, 20)
        # ui.cut_left(rect, 20)

        x, l = ui.cut_left(rect, 80)

        ui.cut_top(x, 30)
        ui.cut_left(x, 20)

        self.ctx.text(x, "x",
                      self.assets.ARCADE_48, color=pygame.Color(255, 255, 255))

        ui.cut_top(l, 5)

        self.ctx.text(l, str(self.lives),
                      self.assets.ARCADE_96, color=pygame.Color(255, 255, 255))

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
