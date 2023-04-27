
from typing import NewType, cast

import pygame

TextureId = NewType("TextureId", int)
"""
Type safe representation of a texture id.
"""


class ImageCache:
    """
    A class that manages the lifetime of images.
    """

    def __init__(self):
        """
        Creates a new image cache.
        """
        self.ids: dict[str, int] = {}
        self.textures: list[pygame.Surface | None] = []

    def load(self, path: str) -> TextureId:
        """
        Loads an image from the given path and returns a texture id.
        For ease of use, the path must be relative to the Resources/Images folder.
        """
        if path not in self.ids:
            self.ids[path] = len(self.textures)
            self.textures.append(pygame.image.load("Resources/Images/" + path))

        return TextureId(self.ids[path])

    def get(self, uid: TextureId) -> pygame.Surface | None:
        """
        Returns the image associated with the given texture id, or None otherwise.
        """
        return self.textures[uid] if uid >= 0 else None

    def unsafe_get(self, uid: TextureId) -> pygame.Surface:
        """
        Returns the image associated with the given texture id. This method is unsafe
        and will throw an exception if the given texture id is invalid.
        """
        return cast(pygame.Surface, self.textures[uid])

    def has(self, uid: TextureId) -> bool:
        """
        Returns True if the given texture id is valid, False otherwise.
        """
        return (0 <= uid < len(self.textures)) and (self.textures[uid] is not None)
