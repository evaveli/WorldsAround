
from Source.components import *
from Source.entity_list import EntityList



def update_animations(entities: EntityList, dt: int):
    for anim in entities.query(Animator).types():
        anim.elapsed += dt
        if anim.anims[anim.active].duration >= anim.elapsed and anim.anims[anim.active].loop:
            anim.elapsed = 0

    for size, anim, sprite in entities.query(Size, Animator, Sprite).types():
        active = anim.anims[anim.active]

        sprite.rect.x = (active.start[0] +
                         active.frames * (anim.elapsed / active.duration)) * size.w
        sprite.rect.y = active.start[1] * size.h
