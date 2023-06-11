
from typing import Iterable, Type, TypeVar, cast


class Component:
    """Base class for all components."""
    pass


_Comp = TypeVar("_Comp", bound=Component)


class Entity:
    """
    An entity is a collection of components.
    """

    def __init__(self, comps: Iterable[Component] = ()):
        """
        Create a new entity with the given components.
        """
        self.components = {type(c).__name__: c for c in comps}

    def get(self, kind: Type[_Comp]) -> _Comp | None:
        """
        Get a component of the given type. Returns None if the entity does not have the component.
        """
        return cast(_Comp | None, self.components.get(kind.__name__))

    def unsafe_get(self, kind: Type[_Comp]) -> _Comp:
        """
        Get a component of the given type. Raises KeyError if the entity does not have the component.
        """
        return cast(_Comp, self.components[kind.__name__])

    def add(self, value: Component):
        """
        Add a component to the entity. If the entity already has a component of the same type, it will be replaced.
        """
        self.components.update({type(value).__name__: value})

    def has(self, kind: tuple | Type[_Comp]) -> bool:
        """
        Check if the entity has a component of the given type.
        """
        if isinstance(kind, tuple):
            return all(k.__name__ in self.components for k in kind)
        else:
            return kind.__name__ in self.components

    def remove(self, kind: Type[_Comp]):
        self.components.pop(kind.__name__, None)
