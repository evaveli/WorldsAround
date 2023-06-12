
import pygame
from dataclasses import dataclass

from Source.entity_list import EntityList
from Source.components import *


class Enemy(Component):
    """
    A component that marks an entity as an enemy.
    """
    pass

@dataclass
class PatrolRange(Component):
    """
    A component that marks an entity as having a patrol range.
    """
    length: int
    duration: int
    elapsed: int = 0
    left: bool = False


# def mark_visible_enemies(
#     entities: EntityList, area: pygame.Rect,
#         tile_size: tuple[int, int], map_size: tuple[int, int]):
#     """
#     A system that marks enemies as active if they are visible.
#     """
#     # pass
#     for obj in entities.query(Enemy, Active).ids():
#         obj.remove(Active)

#     scale = (map_size[0] * tile_size[0], map_size[1] * tile_size[1])

#     camera = pygame.Rect(area.x / scale[0], area.y / scale[1],
#                             area.w / scale[0], area.h / scale[1])

#     for obj in entities.query(Enemy, Position, Size).ids():
#         pos = obj.unsafe_get(Position)
#         size = obj.unsafe_get(Size)

#         rect = pygame.Rect(pos.x, pos.y, size.w / tile_size[0], size.h / tile_size[1])

#         print(f"rect: {rect}, camera: {camera}")

#         if camera.colliderect(rect):
#             obj.add(Active())


def update_enemies(entities: EntityList, dt: int):
    """
    A system that handles enemies.
    """
    for _, pos, patrol in entities.query(Enemy, Position, PatrolRange).types():
        patrol.elapsed += dt
        speed = patrol.length / patrol.duration
        pos.x += dt * speed * (-1 if patrol.left else 1)

    for _, patrol, anim in entities.query(Enemy, PatrolRange, Animator).types():
        if patrol.elapsed >= patrol.duration:
            patrol.elapsed = 0
            patrol.left = not patrol.left
            # sprite.flip = not sprite.flip

            if patrol.left:
                anim.transition("idle_left")
            else:
                anim.transition("idle_right")
