
from typing import Type, TypeVar, cast


class Component:
    """Base class for all components."""
    pass


_Comp = TypeVar("_Comp", bound=Component)


class Entity:
    """
    An entity is a collection of components.
    """

    def __init__(self, *comps: Component):
        """
        Create a new entity with the given components.
        """
        self.components = {type(c).__name__: c for c in comps}

    def get(self, kind: Type[_Comp]) -> Type[_Comp] | None:
        """
        Get a component of the given type. Returns None if the entity does not have the component.
        """
        if kind.__name__ not in self.components:
            return None
        else:
            return cast(Type[_Comp], self.components[kind.__name__])

    def unsafe_get(self, kind: Type[_Comp]) -> Type[_Comp]:
        """
        Get a component of the given type. Raises KeyError if the entity does not have the component.
        """
        return cast(Type[_Comp], self.components[kind.__name__])

    def add(self, value: Component):
        """
        Add a component to the entity. If the entity already has a component of the same type, it will be replaced.
        """
        self.components.update({type(value).__name__: value})

    def has(self, kind: type) -> bool:
        """
        Check if the entity has a component of the given type.
        """
        return kind.__name__ in self.components