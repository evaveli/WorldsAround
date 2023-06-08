
from enum import Enum

import pygame
from pygame import key

from Source import ui

from Source.controls import Controls
from Source.image_cache import TextureId
from Source.profile import Profile
from Source.scene import Scene
from Source.scene_context import SceneContext


class _Colors(Enum):
    IDLE = pygame.Color(0, 0, 0, 0)
    ERROR = pygame.Color(255, 0, 0, 255)
    SELECTED = pygame.Color(0, 0, 0, 255)


class _Controls(Enum):
    NONE = -1

    ENTER_DOOR = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    JUMP = 4
    POWERUP_1 = 5
    POWERUP_2 = 6


class SettingsScene(Scene):
    def __init__(self, profile: Profile):
        super().__init__()
        self.profile = profile
        self.music_volume = ui.Param(profile.bg)
        self.sfx_volume = ui.Param(profile.sfx)

        # UI state
        self.go_back = False
        self.listening = _Controls.NONE.value

        self.color_table = [
            _Colors.IDLE,  # enter door
            _Colors.IDLE,  # move left
            _Colors.IDLE,  # move right
            _Colors.IDLE,  # move down
            _Colors.IDLE,  # jump
            _Colors.IDLE,  # powerup 1
            _Colors.IDLE,  # powerup 2
        ]

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.ctx = ctx.ui
        self.camera = ctx.camera

    def exit(self):
        self.profile.save()

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.listening != -1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.color_table[self.listening] = _Colors.IDLE
                elif self.profile.controls.used(event.key) and event.key != self.profile.controls.list()[self.listening]:
                    self.color_table[self.listening] = _Colors.ERROR
                else:
                    if self.listening == _Controls.ENTER_DOOR.value:
                        self.profile.controls.enter_door = event.key
                    elif self.listening == _Controls.LEFT.value:
                        self.profile.controls.left = event.key
                    elif self.listening == _Controls.DOWN.value:
                        self.profile.controls.down = event.key
                    elif self.listening == _Controls.RIGHT.value:
                        self.profile.controls.right = event.key
                    elif self.listening == _Controls.JUMP.value:
                        self.profile.controls.jump = event.key
                    elif self.listening == _Controls.POWERUP_1.value:
                        self.profile.controls.powerup_1 = event.key
                    elif self.listening == _Controls.POWERUP_2.value:
                        self.profile.controls.powerup_2 = event.key

                self.listening = -1
                return Scene.Continue()

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     self.listening = -1

        if self.go_back:
            self.go_back = False
            self.profile.save()
            return Scene.Pop()

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        # header
        head, body = ui.cut_top(rect, 75)

        ui.cut_left(head, 10)
        ui.cut_right(head, 10)
        ui.cut_top(head, 10)

        self.ctx.text_layout(ui.center(head), "Settings",
                             self.assets.ARCADE_48)

        ui.cut_left(head, 10)
        ui.cut_top(head, 10)

        if self.listening == -1 and self.ctx.button(head, "Back", self.assets.ARCADE_24):
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

        index = ui.Param(0)

        def mapping(rect: pygame.Rect, text: str, key: str, index=index) -> bool:
            action, btn = ui.hsplit_pct(rect, 0.75)

            ui.cut_top(action, 10)
            ui.cut_left(action, 10)
            ui.cut_right(action, 10)

            self.ctx.text_layout(ui.center(action), text,
                                 self.assets.ARCADE_24)

            ui.cut_top(btn, 10)
            ui.cut_left(btn, 10)
            ui.cut_right(btn, 10)

            text = key

            if self.listening == index.value:
                self.color_table[index.value] = _Colors.SELECTED
                text = "   "
            elif self.color_table[index.value] == _Colors.SELECTED:
                self.color_table[index.value] = _Colors.IDLE

            index.value += 1

            return self.ctx.button_layout(ui.center(btn), text, self.assets.ARCADE_24, border_color=self.color_table[index.value - 1].value) \
                and (self.listening == -1 or self.listening == index.value - 1)

        if mapping(enter_door, "Enter  door", key.name(self.profile.controls.enter_door)):
            self.listening = _Controls.ENTER_DOOR.value

        if mapping(move_left, "Move  left", key.name(self.profile.controls.left)):
            self.listening = _Controls.LEFT.value

        if mapping(move_down, "Move  down", key.name(self.profile.controls.down)):
            self.listening = _Controls.DOWN.value

        if mapping(move_right, "Move  right", key.name(self.profile.controls.right)):
            self.listening = _Controls.RIGHT.value

        jump, powerup_1, powerup_2, _ = ui.vsplit_n(right, 4)

        if mapping(jump, "Jump", key.name(self.profile.controls.jump)):
            self.listening = _Controls.JUMP.value

        if mapping(powerup_1, "Powerup  1", key.name(self.profile.controls.powerup_1)):
            self.listening = _Controls.POWERUP_1.value

        if mapping(powerup_2, "Powerup  2", key.name(self.profile.controls.powerup_2)):
            self.listening = _Controls.POWERUP_2.value

        if self.ctx.button_layout(ui.center(reset), "Reset", self.assets.ARCADE_24):
            defc = Controls.default()
            self.profile.controls.enter_door = defc.enter_door
            self.profile.controls.left = defc.left
            self.profile.controls.down = defc.down
            self.profile.controls.right = defc.right
            self.profile.controls.jump = defc.jump
            self.profile.controls.powerup_1 = defc.powerup_1
            self.profile.controls.powerup_2 = defc.powerup_2

            # sound
            self.profile.bg = 0.5
            self.profile.sfx = 0.5

        bg, sfx = ui.vsplit(sound)

        def volume_slider(rect: pygame.Rect, param: ui.Param[float], img: TextureId) -> bool:
            ui.cut_top(rect, 20)
            ui.cut_left(rect, 20)
            ui.cut_right(rect, 20)
            ui.cut_bottom(rect, 20)

            _, rect = ui.hsplit_pct(rect, 0.27)

            self.ctx.image(rect, img)

            ui.cut_left(rect, 30)

            changed = self.ctx.slider(rect, param, 0, 1)

            ui.cut_left(rect, 10)

            self.ctx.text(rect, f"{param.value * 100:.0f}",
                                 self.assets.ARCADE_24)

            return changed
        
        self.music_volume = ui.Param(self.profile.bg)

        if volume_slider(bg, self.music_volume, self.assets.MUSIC_ICON):
            # change bg volume
            self.profile.bg = self.music_volume.value
            pass

        self.sfx_volume = ui.Param(self.profile.sfx)

        if volume_slider(sfx, self.sfx_volume, self.assets.SOUNDS_ICON):
            # change sfx volume
            self.profile.sfx = self.sfx_volume.value
            pass

    def draw(self):
        # render UI
        self.ctx.draw(self.camera.screen)
