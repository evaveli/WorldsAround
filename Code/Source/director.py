
import sys

from pygame import event
import pygame

from Source.scene import Scene


class Director:
    def __init__(self):
        self.scenes: list[Scene] = []

    def push(self, scene: Scene):
        if len(self.scenes) > 0:
            self.scenes[-1].exit()

        self.scenes.append(scene)
        self.scenes[-1].enter()

    def pop(self):
        self.scenes[-1].exit()
        self.scenes.pop()

        if len(self.scenes) == 0:
            pygame.quit()
            sys.exit(0)

        self.scenes[-1].enter()

    def input(self, event: event.Event):
        cmd = self.scenes[-1].input(event)
        if isinstance(cmd, Scene.Push):
            self.push(cmd.scene)
        elif isinstance(cmd, Scene.Pop):
            self.pop()

    def update(self, dt: int):
        self.scenes[-1].update(dt)

    def draw(self, screen: pygame.Surface):
        self.scenes[-1].draw(screen)
