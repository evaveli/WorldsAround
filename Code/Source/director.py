
from pygame import event
import pygame

from Source.scene import Scene

# NullScene is a scene that does nothing
# Used internally by Director


class NullScene(Scene):
    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen: pygame.Surface):
        pass


class Director:
    def __init__(self):
        self.scenes = list[Scene]()
        self.scenes.append(NullScene())
        self.current = self.scenes[-1]

    def push(self, scene: Scene):
        self.current.exit()
        self.scenes.append(scene)
        self.current = self.scenes[-1]
        self.current.enter()

    def pop(self) -> Scene:
        self.current.exit()
        scene = self.scenes.pop()

        if len(self.scenes) == 0:
            self.scenes.append(NullScene())

        self.current = self.scenes[-1]
        self.current.enter()

        return scene

    def input(self, event: event.Event):
        self.scenes[-1].input(event)

    def update(self, dt):
        self.scenes[-1].update(dt)

    def draw(self, screen: pygame.Surface):
        self.scenes[-1].draw(screen)
