
from dataclasses import dataclass

import pygame


# TODO:
# store controls configuration in a "action": int-key mapping
# no two actions can have the same key

Key = int
"""
A key on the keyboard.
"""


@dataclass
class Controls:
    enter_door: Key
    left: Key
    right: Key
    down: Key
    jump: Key
    powerup_1: Key
    powerup_2: Key

    @staticmethod
    def default() -> "Controls":
        return Controls(
            enter_door=pygame.K_w,
            left=pygame.K_a,
            right=pygame.K_d,
            down=pygame.K_s,
            jump=pygame.K_SPACE,
            powerup_1=pygame.K_1,
            powerup_2=pygame.K_2,
        )

    def used(self, key: Key) -> bool:
        return key in self.__dict__.values()

    def list(self) -> list[Key]:
        return [self.enter_door, self.left, self.down, self.right,  self.jump, self.powerup_1, self.powerup_2]
