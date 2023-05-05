
from dataclasses import dataclass

from Source.font_cache import FontCache, FontId
from Source.image_cache import ImageCache, TextureId


@dataclass
class FailedToLoadAssets(Exception):
    asset: str


class Assets:
    def __init__(self, images: ImageCache, fonts: FontCache):
        def _load_image(name: str) -> TextureId:
            uid = images.load(name)
            if uid is None:
                raise FailedToLoadAssets(name)
            return uid

        self.MUSIC_ICON = images.load("music.png")
        self.SOUNDS_ICON = images.load("sounds.png")

        def _load_font(name: str, size: int) -> FontId:
            uid = fonts.load(name, size)
            if uid is None:
                raise FailedToLoadAssets(name)
            return uid

        self.ARCADE_24 = _load_font("ARCADECLASSIC.TTF", 24)
        self.ARCADE_48 = _load_font("ARCADECLASSIC.TTF", 48)
        self.ARCADE_72 = _load_font("ARCADECLASSIC.TTF", 72)

    @staticmethod
    def load(images: ImageCache, fonts: FontCache) -> "Assets | FailedToLoadAssets":
        try:
            return Assets(images, fonts)
        except FailedToLoadAssets as f:
            return f
