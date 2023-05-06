
import pygame

from Source.assets import Assets
from Source.components import Position, Sprite
from Source.entity import Entity
from Source import ui
from Source.scene import Scene, SceneContext


class Level(Scene):
    def __init__(self, file: str, map: dict[int, Sprite]):
        super().__init__()
        self.objects: list[Entity] = []

        with open("Resources/Levels/" + file, "r") as handle:
            col = 0
            row = 0

            for line in handle.readlines():
                for n in line.split(','):
                    n = int(n)
                    if n == 0:
                        pass
                    elif n in map:
                        self.objects.append(Entity(
                            Position(col * 32, row * 32),
                            map[n]
                        ))

                    row += 1

                col += 1

    def enter(self, ctx: SceneContext):
        self.assets = ctx.assets
        self.images = ctx.images

    def render(self, screen: pygame.Surface):
        for obj in self.objects:
            sprite = obj.get(Sprite)
            pos = obj.get(Position) or Position(0, 0)

            if sprite is not None:
                # TODO: is this safe?
                # it should be, given that the mapping
                # is passed from the code, not the map
                tex = self.images.unsafe_get(sprite.uid)
                screen.blit(tex, sprite.rect.move(pos.x, pos.y))
