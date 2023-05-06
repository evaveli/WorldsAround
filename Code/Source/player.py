
from dataclasses import dataclass

import pygame

from Source.entity import Entity, Component


Key = tuple[int, str]
"""
    A tuple of a key ID and a string representation.
"""


@dataclass
class Controls(Component):
    open_door: Key
    left: Key
    right: Key
    down: Key
    jump: Key
    powerup_1: Key
    powerup_2: Key

    @staticmethod
    def default() -> "Controls":
        return Controls(
            open_door=(pygame.K_w, "W"),
            left=(pygame.K_a, "A"),
            right=(pygame.K_d, "D"),
            down=(pygame.K_s, "S"),
            jump=(pygame.K_SPACE, "Space"),
            powerup_1=(pygame.K_1, "1"),
            powerup_2=(pygame.K_2, "2"),
        )


class Player(Entity):
    def __init__(self):
        super().__init__(
            Controls.default(),
        )
