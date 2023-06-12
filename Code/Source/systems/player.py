

from typing import Any

import pygame

from Source.components import *
from Source.entity import Entity
from Source.entity_list import EntityList
from Source.controls import Controls


class Player(Component):
    """
    A component that marks an entity as a player.
    """
    pass


class Goal(Component):
    """
    A component that marks an entity as a goal.
    """
    pass


class Powerup(Component):
    """
    A component that marks an entity as a powerup.
    """
    pass


class PowerupData:
    """
    A type that represents a powerup's properties.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)


@dataclass
class Powerup1(Component):
    """
    A component that shows the player has a powerup at slot 1.
    """

    name: str


@dataclass
class Powerup2(Component):
    """
    A component that shows the player has a powerup at slot 2.
    """

    name: str


# active powerups

class Shield(Component):
    """
    A component that says that the player has an active shield.
    """
    pass


ACCEL = (0.5, 60)


def update_player(entities: EntityList, dt: int, *,
                  key: int, controls: Controls):
    """
    A system that handles player logic.
    """

    # input handling
    for p in entities.query(Player, Velocity, Animator, Sprite).ids():
        vel = p.unsafe_get(Velocity)
        anim = p.unsafe_get(Animator)
        sprite = p.unsafe_get(Sprite)

        if key == controls.left:
            vel.x -= ACCEL[0]
            anim.transition("walk_left")
            sprite.flip = True
        if key == controls.right:
            vel.x += ACCEL[0]
            anim.transition("walk_right")
            sprite.flip = False
        if key == controls.jump and vel.y == 0:
            vel.y -= ACCEL[1]

        if key == controls.powerup_1 and p.has(Powerup1):
            pu = p.unsafe_get(Powerup1)
            _apply_powerup(p, pu.name)
            p.remove(Powerup1)
        elif key == controls.powerup_2 and p.has(Powerup2):
            pu = p.unsafe_get(Powerup2)
            _apply_powerup(p, pu.name)
            p.remove(Powerup2)

        vel.x = max(-10, min(10, vel.x))


def handle_player_collisions(entities: EntityList, tile_size: tuple[int, int]):
    for p in entities.query(Player).ids():
        pos = p.unsafe_get(Position)
        size = p.unsafe_get(Size)

        prect = pygame.Rect(pos.x, pos.y, size.w //
                            tile_size[0], size.h // tile_size[1])

        for pu in entities.query(Powerup, Name, Position, Size, Active).ids():
            pos = pu.unsafe_get(Position)
            size = pu.unsafe_get(Size)
            pu_name = pu.unsafe_get(Name).name

            rect = pygame.Rect(pos.x, pos.y, size.w //
                               tile_size[0], size.h // tile_size[1])

            if prect.colliderect(rect):
                pu.remove(Active)

                if not p.has(Powerup1):
                    p.add(Powerup1(pu_name))
                elif not p.has(Powerup2):
                    p.add(Powerup2(pu_name))


def _apply_powerup(p: Entity, name: str):
    if name == "shield":
        p.add(Shield())
