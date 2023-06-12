
from typing import Iterable, Type
from Source.entity import Entity, _Comp


class _TypeIter:
    def __init__(self, entities: Iterable[Entity], *fs: Type[_Comp]):
        self.entities = entities
        self.filters = fs

    def ids(self):
        for entity in self.entities:
            if entity.has(self.filters):
                yield entity

    def types(self):
        if len(self.filters) == 1:
            for entity in self.entities:
                if entity.has(self.filters):
                    yield entity.unsafe_get(self.filters[0])
        else:
            for entity in self.entities:
                if entity.has(self.filters):
                    yield tuple(entity.unsafe_get(c) for c in self.filters)


class EntityList:
    def __init__(self, entities: Iterable[Entity] = ()):
        self.entities = list(entities)

    def add(self, entity: Entity):
        self.entities.append(entity)

    def remove(self, entity: Entity):
        self.entities.remove(entity)

    def all(self):
        for entity in self.entities:
            yield entity

    def query(self, *cls: Type[_Comp]):
        return _TypeIter(self.entities, *cls)  # type: ignore
