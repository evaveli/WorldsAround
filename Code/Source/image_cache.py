
import pygame

class ImageCache:
    def __init__(self):
        self.ids: dict[str, int] = {}
        self.textures: list[pygame.Surface | None] = []

    def load(self, path: str) -> int:
        if path not in self.ids:
            self.ids[path] = len(self.textures)
            self.textures.append(pygame.image.load(path))

        return self.ids[path]

    def get(self, uid: int) -> pygame.Surface | None:
        return self.textures[uid] if uid >= 0 else None

    def has(self, uid: int) -> bool:
        return 0 <= uid < len(self.textures)