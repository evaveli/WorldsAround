
from dataclasses import dataclass
import abc

import pygame
from pygame import event


class Scene(metaclass=abc.ABCMeta):
    """
        A scene is a collection of game objects that are updated and drawn together.
    """

    @dataclass
    class Push:
        """
            Command to push a new scene to the scenes stack.
            Return this from ```input``` to push a new scene.
        """
        scene: "Scene"

    class Pop:
        """
            Command to pop the current scene from the scenes stack.
            Return this from ```input``` to pop the current scene.
        """
        pass

    class Continue:
        """
            Command to continue updating and drawing the current scene.
            Return this from ```input``` to continue updating and drawing the current scene.
        """
        pass

    Command = Push | Pop | Continue
    """
        Commands that can be returned from ```input``` to handle the current scene.
        If Push or Pop is returned, the current scene will be exited or entered respectively.
        If Continue is returned, the current scene will continue to be updated and drawn.
    """


    def enter(self):
        """
            Optional method called when entering the scene.
        """
        pass

    def exit(self):
        """
            Optional method called when exiting the scene.
        """
        pass

    def input(self, event: event.Event) -> Command:
        """
            Optional method called when an event is received.
            Return a command to handle the current scene.
            If Push or Pop is returned, the current scene will be exited or entered respectively.
            If Continue is returned, the current scene will continue to be updated and drawn.
        """
        return Scene.Continue()

    @abc.abstractclassmethod
    def update(self, dt: int):
        """
            Called every frame to update the state of the objects.
            Must be implemented by the subclass.
        """
        pass

    @abc.abstractclassmethod
    def draw(self, screen: pygame.Surface):
        """
            Called every frame to render objects of the scene.
            Must be implemented by the subclass.
        """
        pass
