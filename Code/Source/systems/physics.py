
from math import ceil

from Source.components import *
from Source.entity_list import EntityList


from Source.tilemap import TileId


def update_physics(entities: EntityList, dt: int, *,
                   tile_size: tuple[int, int],
                   tiles: list[TileId],
                   map_w: int, map_h: int):
    """
    A system that handles physics.
    """

    # physics
    for pos, vel, size in entities.query(Position, Velocity, Size).types():
        x, y = int(pos.x), int(pos.y)
        diff = (size.w // tile_size[0], size.h // tile_size[1])

        minx, miny = int(pos.x), int(pos.y)
        maxx, maxy = int(ceil(pos.x + diff[0])), int(ceil(pos.y + diff[1]))

        def clamp(a, b, x): return min(b, max(a, x))

        # NOTE: -1/+1 is to check the tiles next to the player
        minx = clamp(0, map_w - 1, minx)
        # TODO: we only need to check the bottom right corner, right?
        miny = clamp(0, map_h - 1, maxy)
        maxx = clamp(0, map_w - 1, maxx)
        maxy = clamp(0, map_h - 1, maxy)

        for i in range(minx, maxx):
            if tiles[maxy * map_w + i] != 0 and pos.y + diff[1] > maxy:
                vel.y = min(0, vel.y)

        pos.x += vel.x * (dt / 1000)
        pos.y += vel.y * (dt / 1000)

        pos.x = clamp(0, map_w - diff[0], pos.x)
        # TODO: this should be clamped to the floor
        pos.y = clamp(0, map_h, pos.y)

        # friction
        vel.x *= 0.9
        vel.y *= 0.9
