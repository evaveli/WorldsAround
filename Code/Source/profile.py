
import json

from Source.controls import Controls
from Source import ui


class Profile:
    controls: Controls
    bg = ui.Param(0.5)
    sfx = ui.Param(0.5)

    @staticmethod
    def temporary() -> "Profile":
        profile = Profile()
        profile.controls = Controls.default()
        return profile

    @staticmethod
    def load(file: str) -> "Profile":
        with open("./Data/Profiles/" + file, "r") as f:
            data = json.load(f)

            profile = Profile()
            profile.controls = Controls(**data['controls'])
            profile.bg = data['bg']
            profile.sfx = data['sfx']

            return profile

    def save(self, file: str):
        with open("./Data/Profiles/" + file, "w") as f:
            json.dump(self.__dict__, f)
