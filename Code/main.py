
from Source.app import App
from Source.scenes.mainmenu import MainMenu


if __name__ == "__main__":
    App(
        title="Worlds Around",
        window_size=(800, 600),
        start_scene=MainMenu(),
    ).run()
