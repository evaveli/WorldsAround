
from Source.components import Velocity
from Source.entity_list import EntityList

GRAVITY = 3

def gravity(entities: EntityList):
    """
    A system that handles gravity.
    """
    for vel in entities.query(Velocity).types():
        vel.y += GRAVITY