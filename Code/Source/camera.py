
import pygame


class Camera:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.area = screen.get_rect()

    def visible(self, area: pygame.Rect) -> bool:
        return self.area.colliderect(area)

    # def move_by(self, dx: int, dy: int):
    #     self.area.move_ip(dx, dy)

    # def center_on(self, x: int, y: int):
    #     self.area.center = (x, y)

    def render(self, image: pygame.Surface, dst: tuple[int, int] = (0, 0), area: pygame.Rect | None = None):
        # TODO: recheck this
        if self.visible(image.get_rect(topleft=dst)):
            self.screen.blit(
                image,
                (dst[0] - self.area.x, dst[1] - self.area.y),
                area,
            )

    def render_at(self, image: pygame.Surface, dst: pygame.Rect, area: pygame.Rect | None = None):
        if self.visible(dst):
            self.screen.blit(
                image,
                dst.move(-self.area.x, -self.area.y),
                area,
            )
