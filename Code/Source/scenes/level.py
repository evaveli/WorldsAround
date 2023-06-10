
from typing import Any

import pygame
from pygame import event

from Source.components import *
from Source.profile import Profile
from Source.scene import Scene
from Source.scene_context import SceneContext
from Source.tilemap import TileMap

from Source.scenes.game_over import GameOver
from Source.scenes.pause_menu import PauseMenu

from Source.systems.enemies import *
from Source.systems.player import *

from Source import ui


@dataclass
class _UnknownComponent(Component):
    name: str


@dataclass
class _UnknownType(Component):
    name: str


class _PropertyParser:
    @staticmethod
    def parse_type(value: Any) -> Component:
        if value == "player":
            return Player()
        elif value == "enemy":
            return Enemy()
        else:
            return _UnknownType(value)

    @staticmethod
    def parse_anim(value: Any):
        anims = {
            name: Animation(
                start=(int(j["start"]["x"]), int(j["start"]["y"])),
                frames=int(j["frames"]),
                duration=int(j["duration"]),
                loop=bool(j["loop"]),
            ) for name, j in value.items()
        }

        return Animator(
            anims=anims,
            active=list(value.keys())[0],
        )


def parse(key: str, value: Any) -> Component:
    if key == "type":
        return _PropertyParser.parse_type(value)
    elif key == "animations":
        return _PropertyParser.parse_anim(value)
    elif key == "name":
        return Name(key)
    elif key == "patrol":
        return PatrolRange(length=2 * int(value["range"]), duration=int(value["duration"]))

    return _UnknownComponent(key)


class Level(Scene):
    def __init__(self, file: str, profile: Profile):
        super().__init__()
        self.file = file

        self.profile = profile
        # UI state
        self.pause = False
        self.game_over = False

        self.dirty: set[TextureId] = set()

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.images = ctx.images
        self.ctx = ctx.ui
        self.camera = ctx.camera

        self.dir = (0, 0)  # used for movement
        self.timer = 0
        self.key = -1  # last key pressed

        self.map = TileMap.load(
            "./Resources/Maps/" + self.file, self.images, parse)

        if self.map.background is not None and self.map.background not in self.dirty:
            bg = self.images.unsafe_get(self.map.background)
            bg.fill((80, 80, 80), special_flags=pygame.BLEND_SUB)
            self.dirty.add(self.map.background)

        if self.map.tileset.colorkey is not None:
            self.images.unsafe_get(self.map.tileset.image).set_colorkey(
                self.map.tileset.colorkey)

        pygame.mixer.music.play(-1)

    def input(self, event: event.Event) -> Scene.Command:
        self.ctx.feed(event)

        if event.type == pygame.KEYDOWN:
            dx, dy = self.dir
            self.key = event.key
            self.pause = event.key == pygame.K_ESCAPE

        elif event.type == pygame.KEYUP:
            self.dir = (0, 0)
            self.key = -1

        if self.pause:
            self.pause = False
            return Scene.Push(PauseMenu(self.profile))
        elif self.game_over:
            self.game_over = False
            return Scene.Push(GameOver())

        return Scene.Continue()

    def update(self, dt: int):
        self.timer += dt
        if self.timer // 1000 >= 999:
            self.game_over = True
            return

        # Game Logic
        PlayerSystem.run(self.map.objects, dt,
                         key=self.key, profile=self.profile)
        EnemiesSystem.run(self.map.objects, dt)

        for anim in self.map.objects.query(Animator).types():
            anim.elapsed += dt
            if anim.anims[anim.active].duration >= anim.elapsed and anim.anims[anim.active].loop:
                anim.elapsed = 0

        # UI
        pygame.display.get_surface().fill((0, 0, 0))

        rect = pygame.display.get_surface().get_rect()

        ui.cut_left(rect, 20)
        ui.cut_top(rect, 20)
        ui.cut_right(rect, 20)

        self.pause = self.ctx.button(
            rect, "Pause", self.assets.ARCADE_24, text_color=pygame.Color(255, 255, 255))

        self.ctx.text_layout(
            ui.right(rect), f"{(self.timer//1000):>03}",
            self.assets.ARCADE_24,
            color=pygame.Color(255, 255, 255))

    def draw(self):
        if self.map.background is not None:
            _, _, w, h = self.camera.screen.get_rect()

            bg = self.images.unsafe_get(self.map.background)
            bg = pygame.transform.scale(bg, (w, h))

            self.camera.render(bg)

        tile_size = self.map.tileset.tile_size
        tile_count = len(self.map.tiles)

        map_w = self.map.width
        map_h = tile_count // map_w

        offset = (0, 0)
        scale = (pygame.display.get_surface(
        ).get_height() // map_h) / tile_size[1]

        ts = self.images.unsafe_get(self.map.tileset.image)
        ts = pygame.transform.scale_by(ts, scale)

        # render tiles
        for j in range(map_h):
            for i in range(map_w):
                tile = self.map.tiles[i + j * map_w]
                if tile == 0:
                    continue

                tile_offset = self.map.tileset.tiles[tile].offset

                area = pygame.Rect(
                    tile_offset[0] * scale,
                    tile_offset[1] * scale,
                    tile_size[0] * scale,
                    tile_size[1] * scale,
                )

                dst = (
                    int(tile_size[0] * i * scale + offset[0]),
                    int(tile_size[1] * j * scale + offset[1]),
                )

                # TODO:
                # replace this with `blits`
                # which processes a list of surfaces
                self.camera.render(ts, dst, area)

        # render objects
        for sprite, pos, size in self.map.objects.query(Sprite, Position, Size).types():
            tex = self.images.unsafe_get(
                sprite.uid).subsurface(sprite.rect)
            tex = pygame.transform.scale_by(tex, scale)

            if sprite.flip:
                tex = pygame.transform.flip(tex, True, False)

            self.camera.render(
                tex, (int(tile_size[0] * pos.x * scale), int(tile_size[1] * pos.y * scale)))

        # render UI
        self.ctx.draw(self.camera.screen)
