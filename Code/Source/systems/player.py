
from Source.components import *
from Source.entity_list import EntityList
from Source.profile import Profile


class Player(Component):
    """
    A component that marks an entity as a player.
    """
    pass


class PlayerSystem:
    @staticmethod
    def run(entities: EntityList, dt: int, *, key: int, profile: Profile):
        for _, anim, pos, sprite in entities.query(Player, Animator, Position, Sprite).types():
            dir = (0, 0)

            if key == profile.controls.left:
                dir = (-10, 0)
                anim.transition("walk_left")  # type: ignore
                sprite.flip = True
            elif key == profile.controls.right:
                dir = (10, 0)
                anim.transition("walk_right")  # type: ignore
                sprite.flip = False

            active = anim.anims[anim.active]

            sprite.rect.x = active.start[0] + \
                active.frames * (anim.elapsed // active.duration)
            sprite.rect.y = active.start[1]

            pos.x += dir[0] * (dt / 1000)
            pos.y += dir[1] * (dt / 1000)
