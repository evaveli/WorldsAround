
import json
from pathlib import Path

from Source.controls import Controls
from Source import ui

# TODO: Profile.create(file: str) -> Profile


class Profile:
    name: str
    controls: Controls
    bg: float = 0.5
    sfx: float = 0.5

    @staticmethod
    def temporary() -> "Profile":
        profile = Profile()
        profile.name = "Temporary"
        profile.controls = Controls.default()
        return profile

    @staticmethod
    def load(file: str) -> "Profile":

        if not Path("./Data/Profiles/" + file).exists():
            Path("./Data/Profiles").mkdir(parents=True, exist_ok=True)
            Path("./Data/Profiles/" + file).touch(exist_ok=True)

            p = Profile.temporary()
            p.name = file
            p.save()
            return p

        with open("./Data/Profiles/" + file, "r") as f:
            data = json.load(f)  # type: dict

            profile = Profile()
            profile.name = file
            profile.controls = Controls(**data['controls'])
            profile.bg = float(data['bg'])
            profile.sfx = float(data['sfx'])

            return profile

    @staticmethod
    def exists(file: str) -> bool:
        return Path("./Data/Profiles/" + file).exists()

    @staticmethod
    def delete(file: str) -> None:
        Path("./Data/Profiles/" + file).unlink(missing_ok=True)

    def save(self):
        # Path("./Data/Profiles").mkdir(parents=True, exist_ok=True)
        # Path("./Data/Profiles/" + self.name).touch(exist_ok=True)

        with open("./Data/Profiles/" + self.name, "w") as f:
            json.dump({
                'controls': self.controls.__dict__,
                'bg': self.bg,
                'sfx': self.sfx
            }, f)
