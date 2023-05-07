
from Source.controls import Controls

class Profile:
    controls: Controls
    
    @staticmethod
    def default() -> "Profile":
        profile = Profile()
        profile.controls = Controls.default()
        return profile