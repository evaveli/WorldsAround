

from Source.components import *
from Source.entity_list import EntityList
from Source.controls import Controls


class Player(Component):
    """
    A component that marks an entity as a player.
    """
    pass


ACCEL = (0.5, 60)


def update_player(entities: EntityList, dt: int, *,
                  key: int, controls: Controls):
    """
    A system that handles player logic.
    """

    # input handling
    for _, vel, anim, sprite in entities.query(Player, Velocity, Animator, Sprite).types():
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

        vel.x = max(-100, min(100, vel.x))
