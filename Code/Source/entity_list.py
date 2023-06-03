
from typing import Iterable, Type
from Source.entity import Entity, _Comp


class EntityList:
    def __init__(self, entities: Iterable[Entity] = ()):
        self.entities = list(entities)

    def add(self, entity: Entity):
        self.entities.append(entity)

    def remove(self, entity: Entity):
        self.entities.remove(entity)

    def query(self, cls: tuple | Type[_Comp]):
        for entity in self.entities:
            if entity.has(cls):
                yield entity
