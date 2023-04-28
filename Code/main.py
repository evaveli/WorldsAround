
from Source.app import App
from Source.scenes.settings import SettingsScene
from Source.scenes.mainmenu import MainMenu

App(
    title="Worlds Around",
    window_size=(800, 600),
    start_scene=MainMenu(),
).run()
