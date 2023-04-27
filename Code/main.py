
from Source.app import App
from Source.scenes.settings import SettingsScene

App(
    title="Worlds Around",
    window_size=(800, 600),
    start_scene=SettingsScene(),
).run()
