
import pygame
import sys

from Source.director import Director

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My Game")

fps = pygame.time.Clock()

director = Director()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    pygame.display.update()
    fps.tick(60)

