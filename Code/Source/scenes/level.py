
import json
from pathlib import Path
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
from Source.scenes.congrats import CongratsScene

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
        elif value == "goal":
            return Goal()
        elif value == "powerup":
            return Powerup()
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
        return Name(value)
    elif key == "patrol":
        return PatrolRange(length=2 * int(value["range"]), duration=int(value["duration"]))
    elif key == "collider":
        return Collider(area=pygame.Rect(int(value[0]), int(value[1]), int(value[2]), int(value[3])))

    return _UnknownComponent(key)


DUMMY_EVENT = pygame.event.Event(pygame.USEREVENT, kind="dummy")


class Level(Scene):
    def __init__(self, file: str, profile: Profile):
        super().__init__()
        self.file = file
        self.profile = profile

        self.pu_list = {
            "shield": PowerupData(start=(16, 0), duration=2000,),
            # "speed": PowerupData(),
            # "jump": PowerupData(),
        }

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

        self.done = False
        self.undead_timer = 0

        if ctx.restart:
            ctx.restart = False

            self.timer = 0

            self.map = TileMap.load(
                "./Resources/Maps/" + self.file, self.images, parse)

            for obj in self.map.objects.all():
                obj.add(Velocity(0, 0))
                obj.add(Active())

            for _, size in self.map.objects.query(Powerup, Size).types():
                size.w *= 0.5
                size.h *= 0.5

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

        if self.done:
            self.done = False

            Path("./Data/scores.json").touch(exist_ok=True)

            with open("./Data/scores.json", "r+") as f:
                scores = json.load(f)

                if self.file not in scores:
                    scores[self.file] = {}
                    scores[self.file]["profile"] = self.profile.name[:-5]
                    scores[self.file]["score"] = self.timer // 1000

                elif self.timer // 1000 < scores[self.file]["score"]:
                    scores[self.file]["profile"] = self.profile.name[:-5]
                    scores[self.file]["score"] = self.timer // 1000

                f.seek(0)
                json.dump(scores, f)
                f.truncate()

            return Scene.Push(CongratsScene())

        if self.game_over:
            self.game_over = False
            self.lives = 4
            return Scene.Push(GameOver())

        return Scene.Continue()

    def update(self, dt: int):
        self.timer += dt
        self.undead_timer -= dt

        if self.timer // 1000 >= 999:
            self.died = True
            pygame.event.post(DUMMY_EVENT)
            return

        # Game Logic

        update_animations(self.map.objects, dt)

        # mark_visible_enemies(
        #     self.map.objects, self.camera.area,
        #     self.map.tileset.tile_size, (self.map.width, self.map.height),
        # )

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

        handle_player_collisions(
            self.map.objects, self.map.tileset.tile_size,
        )

        for p in self.map.objects.query(Player, Position, Size, Collider).ids():
            pos = p.unsafe_get(Position)
            size = p.unsafe_get(Size)
            coll = p.unsafe_get(Collider)

            cam = self.camera.area

            tile_size = self.map.tileset.tile_size
            scale = cam.h // tile_size[1] // self.map.height

            # check if goal reached
            for _, gpos in self.map.objects.query(Goal, Position).types():
                if gpos.x - 1 <= pos.x <= gpos.x + 1:
                    self.done = True

            parea = pygame.Rect(
                pos.x * scale + coll.area.x,
                pos.y * scale + coll.area.y,
                coll.area.w,
                coll.area.h,
            )


            # check if collided with enemy
            for _, _, epos, esize in self.map.objects.query(Enemy, Active, Position, Size).types():
                earea = pygame.Rect(
                    epos.x * scale,
                    epos.y * scale,
                    esize.w,
                    esize.h,
                )

                if parea.colliderect(earea):
                    if p.has(Shield):
                        p.remove(Shield)
                        self.undead_timer = self.pu_list["shield"].duration
                        return

                    elif self.undead_timer < 0:
                        self.died = True
                        pygame.event.post(DUMMY_EVENT)
                        return

            if self.undead_timer < 0:
                self.undead_timer = 0

            # check if fell off the map
            diff = size.h // self.map.tileset.tile_size[1]

            if pos.y + diff >= self.map.height:
                self.died = True
                pygame.event.post(DUMMY_EVENT)
                return

            # center camera on player
            self.camera.area.centerx = int(pos.x * scale * tile_size[0])
            self.camera.area.centery = int(pos.y * scale * tile_size[1])

            self.camera.area.x = max(
                0, min(self.camera.area.x, self.map.width * tile_size[0] * scale - self.camera.area.w))
            self.camera.area.y = max(
                0, min(self.camera.area.y, self.map.height * tile_size[1] * scale - self.camera.area.h))

        self._ui()

    def _ui(self):
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

        ui.cut_left(rect, 16)

        self.ctx.text(rect, f"x {self.lives}", self.assets.ARCADE_24,
                      color=pygame.Color(255, 255, 255))

        def powerup_widget(area: pygame.Rect, slot: type, index: str):
            if p.has(slot):
                name = p.unsafe_get(slot).name

                ui.cut_left(area, 50)

                self.ctx.text(area, index, self.assets.ARCADE_24,
                              color=pygame.Color(255, 255, 255))

                ui.cut_left(area, 16)

                self.ctx.image(area, self.assets.ITEMS,
                               (*self.pu_list[name].start, 16, 16),
                               border_color=pygame.Color(255, 255, 255),
                               border_width=2)

        for p in self.map.objects.query(Player).ids():
            powerup_widget(rect, Powerup1, "1")
            powerup_widget(rect, Powerup2, "2")

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
        for obj in self.map.objects.query(Active, Sprite, Position, Size).ids():
            sprite = obj.unsafe_get(Sprite)
            pos = obj.unsafe_get(Position)
            size = obj.unsafe_get(Size)

            tex = self.images.unsafe_get(
                sprite.uid).subsurface(sprite.rect)
            tex = pygame.transform.scale(tex, (scale * size.w, scale * size.h))

            if sprite.flip:
                tex = pygame.transform.flip(tex, True, False)

            if obj.has(Player):
                if self.undead_timer % 2 == 0:
                    self.camera.render(
                        tex, (int(tile_size[0] * pos.x * scale), int(tile_size[1] * pos.y * scale)))
            else:
                self.camera.render(
                    tex, (int(tile_size[0] * pos.x * scale), int(tile_size[1] * pos.y * scale)))

        # render UI
        self.ctx.draw(self.camera.screen)
