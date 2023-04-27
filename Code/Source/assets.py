
from dataclasses import dataclass

from Source.image_cache import ImageCache, TextureId


@dataclass
class FailedToLoadAssets(Exception):
    asset: str


class Assets:
    def __init__(self, images: ImageCache):
        def _load_image(name: str) -> TextureId | None:
            uid = images.load(name)
            if uid is None:
                raise FailedToLoadAssets(name)
            return uid

        # TODO: load assets here
        self.MUSIC_ICON = images.load("music.png")
        self.SOUNDS_ICON = images.load("sounds.png")

    @staticmethod
    def load(images: ImageCache) -> "Assets | FailedToLoadAssets":
        try:
            return Assets(images)
        except FailedToLoadAssets as f:
            return f
