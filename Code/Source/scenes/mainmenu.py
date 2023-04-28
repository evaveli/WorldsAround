import pygame

from Source import ui
from Source.scene import Scene

from Source.assets import Assets, FailedToLoadAssets
from Source.image_cache import ImageCache, TextureId

class MainMenu(Scene):
    def __init__(self):
        super().__init__()

        self.images = ImageCache()
        self.assets = Assets.load(self.images)

        if isinstance(self.assets, FailedToLoadAssets):
            raise Exception(f"Failed to load assets: {self.assets.asset}")

        self.ctx = ui.Context(self.images)
        self.quit = False

    def input(self, event: pygame.event.Event) -> Scene.Command:
        # inform the UI context of the event
        self.ctx.feed(event)

        if self.quit:
            self.quit = False
            return Scene.Pop()

        return Scene.Continue()
    
    def update(self, dt: int):
        rect = pygame.display.get_surface().get_rect()

        # header
        head, body = ui.cut_top(rect, 100)

        ui.cut_left(head, 10)
        ui.cut_right(head, 10)
        ui.cut_top(head, 150)

        self.ctx.text_layout(ui.center(head), "Worlds Around", (0,0,0), 72)

        ui.cut_left(body, 10)
        ui.cut_right(body, 10)
        ui.cut_top(body, 70)

        

        btn1, btn2, btn3 = ui.vsplit_n(body, 3)

        play = self.ctx.button_layout(ui.center(btn1), "Play", (0,0,0), 48)
        settings = self.ctx.button_layout(ui.center(btn2), "Settings", (0,0,0), 48)
        quitBtn = self.ctx.button_layout(ui.center(btn3), "Quit", (0,0,0), 48)

        play, settings
        if quitBtn:
            self.quit = True
            return
        
        ui.cut_left(head, 10)
        ui.cut_top(head, 50)
        
    def draw(self, screen: pygame.Surface):
        # render UI
        screen.fill((255,255,255))
        self.ctx.draw(screen)