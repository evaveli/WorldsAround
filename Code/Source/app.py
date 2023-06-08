

from dataclasses import dataclass

import pygame

from Source.scene import Scene
from Source.director import Director


class _NullScene(Scene):
    def enter(self, assets, ui):
        pass

    def update(self, dt: int):
        pass

    def draw(self):
        pass


@dataclass
class App:
    """
    The main application class.
    """
    title: str = "Pygame App"
    window_size: tuple[int, int] = (800, 600)
    start_scene: Scene = _NullScene()

    def run(self):
        """
        Run the application.
        """
        pygame.mixer.pre_init(44100, -16, 2, 2048) # pre-init mixer to avoid sound lag

        pygame.init()
        pygame.mixer.init()

        screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.title)

        director = Director()
        director.push(self.start_scene)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                director.input(event)

            screen.fill((255, 255, 255))

            director.update(pygame.time.get_ticks())
            director.draw()

            pygame.display.update()
