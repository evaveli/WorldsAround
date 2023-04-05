
import abc

import pygame
from pygame import event


class Scene(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def enter(self):
        pass

    @abc.abstractclassmethod
    def exit(self):
        pass

    # optional method
    def input(self, event: event.Event):
        pass

    @abc.abstractclassmethod
    def update(self, dt):
        pass

    @abc.abstractclassmethod
    def draw(self, screen: pygame.Surface):
        pass
