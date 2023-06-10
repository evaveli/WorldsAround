
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


class EnemiesSystem:
    """
    A system that handles enemies.
    """

    @staticmethod
    def run(entities: EntityList, dt: int):
        for _, pos, patrol in entities.query(Enemy, Position, PatrolRange).types():
            patrol.elapsed += dt
            speed = patrol.length / patrol.duration
            pos.x += dt * speed * (-1 if patrol.left else 1)

        for _, patrol, sprite, anim in entities.query(Enemy, PatrolRange, Sprite, Animator).types():
            if patrol.elapsed >= patrol.duration:
                patrol.elapsed = 0
                patrol.left = not patrol.left
                # sprite.flip = not sprite.flip

                if patrol.left:
                    anim.transition("idle_left")
                else:
                    anim.transition("idle_right")
