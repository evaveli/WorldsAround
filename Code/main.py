
from pygame import event
from Source.app import App
from Source.scenes.level import Level
from Source.scenes.mainmenu import MainMenu


if __name__ == "__main__":
    App(
        title="Worlds Around",
        window_size=(800, 600),
        start_scene=Level("level1.json"),
    ).run()

# if __name__ == "__main__":
#     App(
#         title="Worlds Around",
#         window_size=(800, 600),
#         start_scene=MainMenu(),
#     ).run()
