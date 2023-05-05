
from typing import NewType, cast

import pygame

FontId = NewType("FontId", int)


class FontCache:
    """
    A class that manages the lifetime of fonts.
    """

    def __init__(self) -> None:
        """
        Creates a new font cache.
        """
        pygame.font.init()

        self.ids: dict[str, int] = {}
        self.fonts: list[pygame.font.Font | None] = []

    def load_system(self, size: int) -> FontId:
        """
        Loads a system font with the given size and returns a font id.
        """

        name = f"system-{size}"
        if name not in self.ids:
            self.ids[name] = len(self.fonts)
            font = pygame.font.Font(None, size)
            self.fonts.append(font)

        return FontId(self.ids[name])

    def load(self, path: str, size: int) -> FontId:
        """
        Loads a font from the given path and returns a font id.
        For ease of use, the path must be relative to the Resources/Fonts folder.
        """
        name = f"{path}-{size}"
        if path not in self.ids:
            self.ids[name] = len(self.fonts)
            self.fonts.append(pygame.font.Font(
                "./Resources/Fonts/" + path, size))

        return FontId(self.ids[name])

    def get(self, uid: FontId) -> pygame.font.Font | None:
        """
        Returns the font associated with the given font id, or None otherwise.
        """
        return self.fonts[uid] if uid >= 0 else None

    def unsafe_get(self, uid: FontId) -> pygame.font.Font:
        """
        Returns the font associated with the given font id. This method is unsafe
        and will throw an exception if the given font id is invalid.
        """
        return cast(pygame.font.Font, self.fonts[uid])

    def has(self, uid: FontId) -> bool:
        """
        Returns True if the given font id is valid, False otherwise.
        """
        return (0 <= uid < len(self.fonts)) and (self.fonts[uid] is not None)
