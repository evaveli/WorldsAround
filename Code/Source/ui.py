
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

import pygame

from Source.font_cache import FontCache, FontId
from Source.image_cache import ImageCache, TextureId

# IDEA:
# you can avoid passing the rect to every widget by storing the rect inside the context
# then you would "split" the context if you wanted to separate the widgets into different rects
# this would allow for removing the "_layout" functions with the "default" ones, by simply passing a layout as a parameter


# Rectcut-related stuff


def cut_left(rect: pygame.Rect, amount: int) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Cuts the left side of a rect by the given amount.
    Returns a tuple of the new rect and the remaining rect.
    """

    minx = rect.left
    rect.left = min(rect.right, rect.left + amount)
    rect.w = max(0, rect.w - amount)

    new = pygame.Rect(minx, rect.top, rect.left - minx, rect.height)

    return (new, rect)


def cut_right(rect: pygame.Rect, amount: int) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Cuts the right side of a rect by the given amount.
    Returns a tuple of the new rect and the remaining rect.
    """
    maxx = rect.right
    rect.w = max(0, rect.w - amount)

    new = pygame.Rect(rect.right, rect.top, maxx - rect.right, rect.height)

    return (new, rect)


def cut_top(rect: pygame.Rect, amount: int) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Cuts the top side of a rect by the given amount.
    Returns a tuple of the new rect and the remaining rect.
    """
    miny = rect.top
    rect.top = min(rect.bottom, rect.top + amount)
    rect.h = max(0, rect.h - amount)

    new = pygame.Rect(rect.left, miny, rect.width, rect.top - miny)

    return (new, rect)


def cut_bottom(rect: pygame.Rect, amount: int) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Cuts the bottom side of a rect by the given amount.
    Returns a tuple of the new rect and the remaining rect.
    """
    maxy = rect.bottom
    rect.h = max(0, rect.h - amount)

    new = pygame.Rect(rect.left, rect.bottom, rect.width, maxy - rect.bottom)

    return (new, rect)


class Direction(Enum):
    """
    The direction in which to align a rect.
    """
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    CENTER = 5


@dataclass
class Layout:
    """
    A layout is a rect and a direction.
    """
    rect: pygame.Rect
    direction: Direction


def left(rect: pygame.Rect) -> Layout:
    """
    Returns a layout that aligns the given rect to the left.
    """
    return Layout(rect, Direction.LEFT)


def right(rect: pygame.Rect) -> Layout:
    """
    Returns a layout that aligns the given rect to the right.
    """
    return Layout(rect, Direction.RIGHT)


def top(rect: pygame.Rect) -> Layout:
    """
    Returns a layout that aligns the given rect to the top.
    """
    return Layout(rect, Direction.UP)


def bottom(rect: pygame.Rect) -> Layout:
    """
    Returns a layout that aligns the given rect to the bottom.
    """
    return Layout(rect, Direction.DOWN)


def center(rect: pygame.Rect) -> Layout:
    """
    Returns a layout that centers the given rect.
    """
    return Layout(rect, Direction.CENTER)


def rectcut(rect: pygame.Rect, amount: int, direction: Direction) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Cuts a rect in the given direction by the given amount.
    Returns a tuple of the new rect and the remaining rect.
    """
    if direction == Direction.LEFT:
        return cut_left(rect, amount)
    elif direction == Direction.RIGHT:
        return cut_right(rect, amount)
    elif direction == Direction.UP:
        return cut_top(rect, amount)
    elif direction == Direction.DOWN:
        return cut_bottom(rect, amount)
    elif direction == Direction.CENTER:
        # For center alignment, the amount is the width of the new rect.
        # It is the only alignment for which the amount is not a distance
        # and that we don't cut the original rect.
        diff = rect.width - amount
        return pygame.Rect(rect.left + diff // 2, rect.top, amount, rect.height), rect


def get_left(rect: pygame.Rect, amount: int) -> pygame.Rect:
    """
    Returns a new rect that is the leftmost part of the given rect.
    """
    return pygame.Rect(rect.left, rect.top, amount, rect.height)


def get_right(rect: pygame.Rect, amount: int) -> pygame.Rect:
    """
    Returns a new rect that is the rightmost part of the given rect.
    """
    return pygame.Rect(rect.right - amount, rect.top, amount, rect.height)


def get_top(rect: pygame.Rect, amount: int) -> pygame.Rect:
    """
    Returns a new rect that is the topmost part of the given rect.
    """
    return pygame.Rect(rect.left, rect.top, rect.width, amount)


def get_bottom(rect: pygame.Rect, amount: int) -> pygame.Rect:
    """
    Returns a new rect that is the bottommost part of the given rect.
    """
    return pygame.Rect(rect.left, rect.bottom - amount, rect.width, amount)


def rectget(rect: pygame.Rect, amount: int, direction: Direction) -> pygame.Rect:
    """
    Returns a new rect that is the given amount in the given direction from the given rect.
    """
    if direction == Direction.LEFT:
        return get_left(rect, amount)
    elif direction == Direction.RIGHT:
        return get_right(rect, amount)
    elif direction == Direction.UP:
        return get_top(rect, amount)
    elif direction == Direction.DOWN:
        return get_bottom(rect, amount)
    elif direction == Direction.CENTER:
        # For center alignment, the amount is the width of the new rect.
        diff = rect.width - amount
        return pygame.Rect(rect.left + diff // 2, rect.top, amount, rect.height)


# UI-related stuff

def hsplit_pct(rect: pygame.Rect, pct: float) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Splits a rect horizontally by the given percentage.
    """
    return cut_left(rect, int(rect.width * pct))


def vsplit_pct(rect: pygame.Rect, pct: float) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Splits a rect vertically by the given percentage.
    """
    return cut_top(rect, int(rect.height * pct))


def hsplit_n(rect: pygame.Rect, count: int) -> list[pygame.Rect]:
    """
    Splits a rect horizontally into the given number of rects.
    """
    rects = []
    w = rect.w // count

    for _ in range(count-1):
        new, rect = cut_left(rect, w)
        rects.append(new)

    rects.append(rect)
    return rects


def vsplit_n(rect: pygame.Rect, count: int) -> list[pygame.Rect]:
    """
    Splits a rect vertically into the given number of rects.
    """
    rects = []
    h = rect.h // count

    for _ in range(count-1):
        new, rect = cut_top(rect, h)
        rects.append(new)

    rects.append(rect)
    return rects


def hsplit(rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Splits a rect horizontally in half.
    """
    return cut_left(rect, rect.width // 2)


def vsplit(rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
    """
    Splits a rect vertically in half.
    """
    return cut_top(rect, rect.height // 2)


@dataclass
class _DrawRect:
    rect: pygame.Rect
    color: pygame.Color
    border: int = 0


@dataclass
class _DrawText:
    text: pygame.Surface  # FIXME: this should ideally be a unique ID
    rect: pygame.Rect


@dataclass
class _DrawImage:
    rect: pygame.Rect
    uid: TextureId
    crop: pygame.Rect | None = None


_Command = _DrawRect | _DrawText | _DrawImage


class _Mouse:
    def __init__(self):
        self.pos = pygame.math.Vector2(0, 0)
        self.pressed = False


T = TypeVar('T')


@dataclass
class Param(Generic[T]):
    """
    Helper type used to pass values to widgets which need to mutate them.
    """
    value: T


class Context:
    """
    A context is responsible for drawing widgets and managing events related to them.
    """

    def __init__(self, images: ImageCache, fonts: FontCache):
        """
        Creates a new context.
        """
        self._images = images
        self._fonts = fonts

        self._commands: list[_Command] = []
        self._mouse = _Mouse()

    def feed(self, event: pygame.event.Event):
        """
        Feeds an event to the context.
        """
        if event.type == pygame.MOUSEMOTION:
            self._mouse.pos = pygame.math.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse.pressed = event.button == 1
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse.pressed = False

    # widgets

    def image(self, rect: pygame.Rect, uid: TextureId, crop: pygame.Rect | None = None, *,
              border_color: pygame.Color | None = None, border_width: int = 0):
        """
        Draws an image at the given rect.
        """
        img = self._images.get(uid)
        if img is None:
            return

        img_rect = img.get_rect()
        area, rect = cut_left(rect, int(rect.h * (img_rect.w / img_rect.h)))

        self._commands.append(_DrawImage(area, uid, crop))

        if border_color is not None:
            area = area.inflate(border_width * 2 + 6, border_width * 2 + 6)
            self._commands.append(_DrawRect(area, border_color, border_width))

    def image_layout(self, layout: Layout, uid: TextureId, crop: pygame.Rect | None = None, *,
                     border_color: pygame.Color | None = None, border_width: int = 0):
        """
        Draws an image with the given layout.
        """
        img = self._images.get(uid)
        if img is None:
            return

        area = rectget(layout.rect, img.get_rect().w, layout.direction)
        self._commands.append(_DrawImage(area, uid, crop))

        if border_color is not None:
            area.left -= border_width + 2
            area.top -= border_width + 2
            area.width += border_width * 2 + 4
            area.height += border_width * 2 + 4
            self._commands.append(_DrawRect(area, border_color, border_width))

    def text(
            self,
            rect: pygame.Rect, text: str,
            uid: FontId | None = None,
            color: pygame.Color = pygame.Color(0, 0, 0)) -> pygame.Rect:
        """
        Draws text at the given rect. If no font is specified, a default one is used.
        """
        font = self._fonts.get(uid) if uid is not None else None
        if font is None:
            font = pygame.font.Font(None, 24)

        surf = font.render(text, False, color)
        # area, _ = cut_left(rect, surf.get_rect().w)

        # pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), textpos, 1)
        area = surf.get_rect().move(rect.left, rect.top)
        self._commands.append(_DrawText(surf, area))
        cut_left(rect, area.w)

        return area

    def text_layout(
            self,
            layout: Layout, text: str,
            uid: FontId | None = None,
            color: pygame.Color = pygame.Color(0, 0, 0)) -> pygame.Rect:
        """
        Draws text with the given layout. If no font is specified, a default one is used.
        """
        font = self._fonts.get(uid) if uid is not None else None
        if font is None:
            font = pygame.font.Font(None, 24)

        surf = font.render(text, False, color)

        area, _ = rectcut(layout.rect, surf.get_rect().w, layout.direction)

        # pygame.display.get_surface().blit(surf, textpos)
        self._commands.append(_DrawText(surf, area))

        return area

    def button(
            self,
            rect: pygame.Rect, text: str,
            font: FontId | None = None,
            text_color: pygame.Color = pygame.Color(0, 0, 0),
            border_color: pygame.Color = pygame.Color(0, 0, 0, 0)) -> bool:
        """
        Draws a button at the given rect. If no font is specified, a default one is used.
        """
        area = self.text(rect, text, font, text_color)
        border = pygame.Rect(area.left - 10, area.top - 10,
                             area.width + 20, area.height + 10)

        if border_color.a > 0:
            self._commands.append(_DrawRect(border, border_color, 3))

        return self._mouse.pressed and border.collidepoint(self._mouse.pos)

    def button_layout(
            self,
            layout: Layout, text: str,
            font: FontId | None = None,
            text_color: pygame.Color = pygame.Color(0, 0, 0),
            border_color: pygame.Color = pygame.Color(0, 0, 0, 0)) -> bool:
        """
        Draws a button with the given layout. If no font is specified, a default one is used.
        """
        area = self.text_layout(layout, text, font, text_color)
        border = pygame.Rect(area.left - 10, area.top - 10,
                             area.width + 20, area.height - 10)

        if border_color.a > 0:
            self._commands.append(_DrawRect(border, border_color, 3))

        return self._mouse.pressed and border.collidepoint(self._mouse.pos)

    def slider(
            self,
            rect: pygame.Rect, param: Param[float],
            min: float, max: float,
            color: pygame.Color = pygame.Color(0, 0, 0)) -> bool:
        w = 256  # the width of the slider

        area = pygame.Rect(rect.left, rect.top + 4, w, 8)

        pct = (param.value - min) / (max - min)
        slider_rect = pygame.Rect(rect.left, rect.top + 4, pct * w, 8)

        self._commands.append(_DrawRect(area, pygame.Color(180, 180, 180)))
        self._commands.append(_DrawRect(slider_rect, color))

        safe_area = area.inflate(20, 20).move(-10, -10)

        if self._mouse.pressed and safe_area.collidepoint(self._mouse.pos):
            pct = (self._mouse.pos.x - rect.left) / w
            pct = 0 if pct < 0 else 1 if pct > 1 else pct
            param.value = min + pct * (max - min)

            rect.x += w + 10

            return True

        rect.x += w + 10

        return False

    # drawing
    def draw(self, screen: pygame.Surface):
        """
        Draws the widgets built this frame to the screen.
        """
        for cmd in self._commands:
            if isinstance(cmd, _DrawRect):
                pygame.draw.rect(screen, cmd.color, cmd.rect, cmd.border)
            elif isinstance(cmd, _DrawText):
                screen.blit(cmd.text, cmd.rect)
            elif isinstance(cmd, _DrawImage):
                img = self._images.unsafe_get(cmd.uid)
                if cmd.crop is not None:
                    img = img.subsurface(cmd.crop)

                aspect = img.get_rect().w / img.get_rect().h

                scale = (int(cmd.rect.h * aspect), cmd.rect.h)

                scaled = pygame.transform.scale(img, scale)
                screen.blit(scaled, cmd.rect)

        self._commands.clear()
