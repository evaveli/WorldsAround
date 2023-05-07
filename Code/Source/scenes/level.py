
import pygame
from pygame import event

from Source.components import Position, Sprite
from Source.entity import Entity
from Source.scene import Scene
from Source.scene_context import SceneContext
from Source.tilemap import TileMap

from Source import ui


class Level(Scene):
    def __init__(self, file: str):
        super().__init__()
        self.file = file
        self.objects: list[Entity] = []
        self.pause = False

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.images = ctx.images
        self.ctx = ctx.ui

        self.map = TileMap.load("./Resources/Maps/" + self.file, self.images)

    def input(self, event: event.Event) -> Scene.Command:
        if self.pause:
            self.pause = False
            # TODO: replace with Push(PauseMenu())
            return Scene.Continue()
            # return Scene.Push(PauseMenu())

        return Scene.Continue()

    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        ui.cut_left(rect, 20)
        ui.cut_top(rect, 20)

        if self.ctx.button(rect, "Pause"):
            self.pause = True

    def draw(self, screen: pygame.Surface):
        if self.map.background is not None:
            screen.blit(self.images.unsafe_get(self.map.background), (0, 0))

        tile_size = self.map.tileset.tile_size
        tile_count = len(self.map.tiles)

        map_w = self.map.width
        map_h = tile_count // self.map.width

        offset = (0, -200)
        scale = 5

        ts = self.images.unsafe_get(self.map.tileset.image)
        ts = pygame.transform.smoothscale_by(ts, scale)

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
                    tile_size[0] * i * scale + offset[0],
                    tile_size[1] * j * scale + offset[1],
                )

                # TODO:
                # replace this with `blits`
                # which processes a list of surfaces
                screen.blit(ts, dst, area)

        # render objects
        for obj in self.objects:
            sprite = obj.get(Sprite)
            pos = obj.get(Position) or Position(0, 0)

            if sprite is not None:
                # TODO: is this safe?
                # it should be, given that the mapping
                # is passed from the code, not the map
                tex = self.images.unsafe_get(sprite.uid)
                screen.blit(tex, sprite.rect.move(pos.x, pos.y))

        # render UI
        self.ctx.draw(screen)
