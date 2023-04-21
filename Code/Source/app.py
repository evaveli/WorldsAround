

from dataclasses import dataclass

import pygame

from Source.scene import Scene
from Source.director import Director, NullScene


@dataclass
class App:
    title: str = "Pygame App"
    window_size: tuple[int, int] = (800, 600)
    start_scene: Scene = NullScene()

    def run(self):
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
