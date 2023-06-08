
import pygame
from pygame import event

from Source.components import *
from Source.entity import Entity
from Source.profile import Profile
from Source.scene import Scene
from Source.scene_context import SceneContext
from Source.tilemap import TileMap

from Source.scenes.pause_menu import PauseMenu

from Source import ui


class Level(Scene):
    def __init__(self, file: str, profile: Profile):
        super().__init__()
        self.file = file
        self.objects: list[Entity] = []

        self.profile = profile
        self.dir = (0, 0)  # used for camera movement

        # UI state
        self.pause = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.images = ctx.images
        self.ctx = ctx.ui
        self.camera = ctx.camera

        self.map = TileMap.load("./Resources/Maps/" + self.file, self.images)
        self.objects = self.map.objects.entities
        pygame.mixer.music.play(-1)

    def input(self, event: event.Event) -> Scene.Command:
        self.ctx.feed(event)

        if event.type == pygame.KEYDOWN:
            dx, dy = self.dir

            if event.key == pygame.K_ESCAPE:
                self.pause = True
            elif event.key == self.profile.controls.left:
                self.dir = (-10, dy)
            elif event.key == self.profile.controls.right:
                self.dir = (10, dy)
            elif event.key == self.profile.controls.enter_door:
                self.dir = (dx, -10)
            elif event.key == self.profile.controls.down:
                self.dir = (dx, 10)

        elif event.type == pygame.KEYUP:
            self.dir = (0, 0)

        self.camera.move_by(*self.dir)

        if self.pause:
            self.pause = False
            return Scene.Push(PauseMenu(self.profile))

        return Scene.Continue()

    def update(self, dt: int):
        pygame.display.get_surface().fill((0, 0, 0))

        rect = pygame.display.get_surface().get_rect()

        ui.cut_left(rect, 20)
        ui.cut_top(rect, 20)

        self.pause = self.ctx.button(
            rect, "Pause", self.assets.ARCADE_24, text_color=pygame.Color(255, 255, 255))

    def draw(self):
        if self.map.background is not None:
            self.camera.render(self.images.unsafe_get(self.map.background))

        tile_size = self.map.tileset.tile_size
        tile_count = len(self.map.tiles)

        map_w = self.map.width
        map_h = tile_count // map_w

        offset = (0, 0)
        scale = (pygame.display.get_surface(
        ).get_height() // map_h) / tile_size[1]

        ts = self.images.unsafe_get(self.map.tileset.image)
        ts = pygame.transform.scale_by(ts, scale)

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
        for obj in self.objects:
            sprite = obj.get(Sprite)
            pos = obj.get(Position) or Position(0, 0)
            size = obj.get(Size) or Size(1, 1)

            if sprite is not None:
                tex = self.images.unsafe_get(
                    sprite.uid).subsurface(sprite.rect)
                tex = pygame.transform.scale_by(tex, scale)
                self.camera.render(
                    tex, (int(tile_size[0] * pos.x * scale), int(tile_size[1] * pos.y * scale)))

        # render UI
        self.ctx.draw(self.camera.screen)
