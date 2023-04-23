

from dataclasses import dataclass

import pygame

from Source.scene import Scene
from Source.director import Director


class _NullScene(Scene):
    def update(self, dt: int):
        pass

    def draw(self, screen: pygame.Surface):
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
        pygame.init()

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

            director.update(pygame.time.get_ticks())

            screen.fill((0, 0, 0))
            director.draw(screen)
            pygame.display.update()
