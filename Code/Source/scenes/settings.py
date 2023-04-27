
from typing import cast
import pygame

from Source import ui

from Source.assets import Assets, FailedToLoadAssets
from Source.image_cache import ImageCache, TextureId
from Source.scene import Scene


class SettingsScene(Scene):
    def __init__(self):
        super().__init__()

        self.images = ImageCache()
        self.assets = Assets.load(self.images)

        if isinstance(self.assets, FailedToLoadAssets):
            raise Exception(f"Failed to load assets: {self.assets.asset}")

        self.ctx = ui.Context(self.images)
        # UI state
        self.go_back = False
        self.music_volume = ui.Param(0.5)
        self.sfx_volume = ui.Param(0.5)

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.go_back:
            self.go_back = False
            return Scene.Pop()

        return Scene.Continue()

    def update(self, dt: int):
        # just to satisfy the type checker
        self.assets = cast(Assets, self.assets)

        rect = pygame.display.get_surface().get_rect()

        # header
        head, body = ui.cut_top(rect, 75)

        ui.cut_left(head, 10)
        ui.cut_right(head, 10)
        ui.cut_top(head, 10)

        self.ctx.text_layout(ui.center(head), "Settings")

        ui.cut_left(head, 10)
        ui.cut_top(head, 10)

        if self.ctx.button(head, "Back"):
            self.go_back = True
            return

        # body
        controls, sound = ui.cut_top(body, 375)
        buttons, reset = ui.cut_top(controls, 300)

        ui.cut_top(buttons, 10)
        ui.cut_left(buttons, 20)
        ui.cut_right(buttons, 20)

        left, right = ui.hsplit(buttons)

        enter_door, move_left, move_down, move_right = ui.vsplit_n(left, 4)

        def mapping(rect: pygame.Rect, text: str, key: str) -> bool:
            action, btn = ui.hsplit_pct(rect, 0.75)

            ui.cut_top(action, 10)
            ui.cut_left(action, 10)
            ui.cut_right(action, 10)

            self.ctx.text_layout(ui.center(action), text)

            ui.cut_top(btn, 10)
            ui.cut_left(btn, 10)
            ui.cut_right(btn, 10)

            return self.ctx.button_layout(ui.center(btn), key)

        if mapping(enter_door, "Enter door", "E"):
            # remap
            pass

        if mapping(move_left, "Move left", "A"):
            # remap
            pass

        if mapping(move_down, "Move down", "S"):
            # remap
            pass

        if mapping(move_right, "Move right", "D"):
            # remap
            pass

        jump, powerup_1, powerup_2, _ = ui.vsplit_n(right, 4)

        if mapping(jump, "Jump", "Space"):
            # remap
            pass

        if mapping(powerup_1, "Powerup 1", "1"):
            # remap
            pass

        if mapping(powerup_2, "Powerup 2", "2"):
            # remap
            pass

        if self.ctx.button_layout(ui.center(reset), "Reset"):
            # reset controls
            pass

        bg, sfx = ui.vsplit(sound)

        def volume_slider(rect: pygame.Rect, param: ui.Param[float], img: TextureId) -> bool:
            ui.cut_top(rect, 20)
            ui.cut_left(rect, 20)
            ui.cut_right(rect, 20)
            ui.cut_bottom(rect, 20)

            _, rect = ui.hsplit_pct(rect, 0.27)

            self.ctx.image(rect, img)

            ui.cut_left(rect, 30)

            return self.ctx.slider(rect, param, 0, 1)

        if volume_slider(bg, self.music_volume, self.assets.MUSIC_ICON):
            # change bg volume
            pass

        if volume_slider(sfx, self.sfx_volume, self.assets.SOUNDS_ICON):
            # change sfx volume
            pass

    def draw(self, screen: pygame.Surface):
        # render UI
        self.ctx.draw(screen)
