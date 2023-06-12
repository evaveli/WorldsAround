
import pygame

from math import ceil

from Source.components import *
from Source.entity_list import EntityList


from Source.tilemap import TileId
from Source.systems.player import Player


def update_physics(entities: EntityList, dt: int, *,
                   tile_size: tuple[int, int],
                   tiles: list[TileId],
                   map_w: int, map_h: int):
    """
    A system that handles physics.
    """

    # physics
    for obj in entities.query(Position, Velocity, Size).ids():
        pos = obj.unsafe_get(Position)
        vel = obj.unsafe_get(Velocity)
        size = obj.unsafe_get(Size)
        coll = obj.get(Collider) or Collider(
            area=pygame.Rect(0, 0, size.w, size.h))

        diff = (
            int(ceil(coll.area.w // tile_size[0])), int(ceil(coll.area.h / tile_size[1])))

        minx, miny = int(pos.x + coll.area.x /
                         size.w), int(pos.y + coll.area.y / size.h)
        maxx, maxy = int(ceil(pos.x + coll.area.x / size.w +
                         diff[0])), int(ceil(pos.y + coll.area.y / size.h + diff[1]))

        area = pygame.Rect(
            (pos.x + coll.area.x / size.w) * tile_size[0],
            (pos.y + coll.area.y / size.h) * tile_size[1],
            coll.area.w,
            coll.area.h,
        )

        def clamp(a, b, x): return min(b, max(a, x))

        # NOTE: -1/+1 is to check the tiles next to the player
        minx = clamp(0, map_w - 1, minx)
        # TODO: we only need to check the bottom right corner, right?
        miny = clamp(0, map_h - 1, maxy)
        maxx = clamp(0, map_w - 1, maxx)
        maxy = clamp(0, map_h - 1, maxy)

        for i in range(minx, maxx):
            if tiles[maxy * map_w + i] != 0 and pos.y + diff[1] > maxy and area.colliderect(i * tile_size[0], maxy * tile_size[1], tile_size[0], tile_size[1]):
                vel.y = min(0, vel.y)
                # pos.y = ((maxy - 1) * tile_size[1] - coll.area.h) / tile_size[1]
                # break

        pos.x += vel.x * (dt / 1000)
        pos.y += vel.y * (dt / 1000)

        pos.x = clamp(0, map_w - diff[0], pos.x)
        # TODO: this should be clamped to the floor
        pos.y = clamp(0, map_h, pos.y)

        # friction
        vel.x *= 0.9
        vel.y *= 0.9
