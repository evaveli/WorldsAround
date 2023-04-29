
from dataclasses import dataclass

import pygame

from Source.font_cache import FontCache
from Source.image_cache import ImageCache, TextureId


@dataclass
class FailedToLoadAssets(Exception):
    asset: str


class Assets:
    def __init__(self, images: ImageCache, fonts: FontCache):
        def _load_image(name: str) -> TextureId | None:
            uid = images.load(name)
            if uid is None:
                raise FailedToLoadAssets(name)
            return uid

        # TODO: load assets here
        self.MUSIC_ICON = images.load("music.png")
        self.SOUNDS_ICON = images.load("sounds.png")

        self.SYSTEM_24 = fonts.load_system(24)
        self.SYSTEM_48 = fonts.load_system(48)
        self.SYSTEM_72 = fonts.load_system(72)

    @staticmethod
    def load(images: ImageCache, fonts: FontCache) -> "Assets | FailedToLoadAssets":
        try:
            return Assets(images, fonts)
        except FailedToLoadAssets as f:
            return f
