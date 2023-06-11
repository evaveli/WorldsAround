
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
from Source.scenes.livesscene import LivesScene

from Source.systems.animations import *
from Source.systems.enemies import *
from Source.systems.player import *
from Source.systems.physics import *
from Source.systems.gravity import *

from Source import ui

# TODO:
# lives
# powerup: shield


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


DUMMY_EVENT = pygame.event.Event(pygame.USEREVENT, kind="dummy")


class Level(Scene):
    def __init__(self, file: str, profile: Profile):
        super().__init__()
        self.file = file
        self.profile = profile

        self.lives = 3  # number of tries left

        # UI state
        self.pause = False
        self.game_over = False
        self.died = False

        self.dirty: set[TextureId] = set()

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.images = ctx.images
        self.ctx = ctx.ui
        self.camera = ctx.camera

        self.dir = (0, 0)  # used for movement
        self.key = -1  # last key pressed

        if ctx.restart:
            ctx.restart = False

            self.timer = 0

            self.map = TileMap.load(
                "./Resources/Maps/" + self.file, self.images, parse)

            for obj in self.map.objects.all():
                obj.add(Velocity(0, 0))

            for obj in self.map.objects.query(Enemy).ids():
                obj.add(Active())

            if self.map.background is not None and self.map.background not in self.dirty:
                bg = self.images.unsafe_get(self.map.background)
                bg.fill((80, 80, 80), special_flags=pygame.BLEND_SUB)
                self.dirty.add(self.map.background)

            if self.map.tileset.colorkey is not None:
                self.images.unsafe_get(self.map.tileset.image).set_colorkey(
                    self.map.tileset.colorkey)

            pygame.mixer.music.rewind()

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
        elif self.died:
            self.died = False
            self.lives -= 1

            if self.lives <= 0:
                self.game_over = True
            else:
                return Scene.Push(LivesScene(self.lives))

        if self.game_over:
            self.game_over = False
            self.lives = 4
            return Scene.Push(GameOver())

        return Scene.Continue()

    def update(self, dt: int):
        self.timer += dt
        if self.timer // 1000 >= 999:
            self.died = True
            pygame.event.post(DUMMY_EVENT)
            return

        # Game Logic

        update_animations(self.map.objects, dt)

        mark_visible_enemies(
            self.map.objects, self.camera.area,
            self.map.tileset.tile_size, (self.map.width, self.map.height),
        )

        update_enemies(self.map.objects, dt)
        update_player(
            self.map.objects, dt,
            key=self.key, controls=self.profile.controls,
        )

        gravity(self.map.objects)

        update_physics(
            self.map.objects, dt,
            tile_size=self.map.tileset.tile_size,
            tiles=self.map.tiles,
            map_w=self.map.width, map_h=self.map.height,
        )

        for _, pos, size in self.map.objects.query(Player, Position, Size).types():
            scale = size.h / self.map.tileset.tile_size[1]

            if pos.y + scale >= self.map.height:
                self.died = True
                pygame.event.post(DUMMY_EVENT)
                return

            cam = self.camera.area

            dstx = cam.center[0] - pos.x
            dsty = cam.center[1] - pos.y

            if abs(dstx) > cam.w * 0.75 or abs(dsty) > cam.h * 0.75:
                self.camera.area.x = int(pos.x) - cam.w // 2
                self.camera.area.y = int(pos.y) - cam.h // 2
            # self.camera.center_on(int(pos.x), int(pos.y))

        # UI
        pygame.display.get_surface().fill((0, 0, 0))

        rect = pygame.display.get_surface().get_rect()

        ui.cut_left(rect, 20)
        ui.cut_top(rect, 20)
        ui.cut_right(rect, 20)

        self.pause = self.ctx.button(
            rect, "Pause", self.assets.ARCADE_24, text_color=pygame.Color(255, 255, 255))

        rect, _ = ui.cut_top(rect, 20)

        ui.cut_left(rect, 50)

        self.ctx.image(
            rect, self.assets.ITEMS, pygame.Rect(0, 0, 16, 16))

        l, x = ui.cut_left(rect, 16)

        self.ctx.text(x, f"x {self.lives}", self.assets.ARCADE_24,
                      color=pygame.Color(255, 255, 255))

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

        map_w = self.map.width
        map_h = self.map.height

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
        for sprite, pos in self.map.objects.query(Sprite, Position).types():
            tex = self.images.unsafe_get(
                sprite.uid).subsurface(sprite.rect)
            tex = pygame.transform.scale_by(tex, scale)

            if sprite.flip:
                tex = pygame.transform.flip(tex, True, False)

            self.camera.render(
                tex, (int(tile_size[0] * pos.x * scale), int(tile_size[1] * pos.y * scale)))

        for _, _, pos, size in self.map.objects.query(Enemy, Active, Position, Size).types():
            pygame.draw.rect(
                pygame.display.get_surface(),
                (255, 0, 0),
                (tile_size[0] * pos.x * scale, tile_size[1] *
                 pos.y * scale, size.w * scale, size.h * scale),
                1,
            )

        # render UI
        self.ctx.draw(self.camera.screen)
