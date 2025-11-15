import pygame
from ui_textarea import TextArea

class Button:
    """
    A pygame Button with hover highlighting and a flexible click callback.
    """
    color: tuple[int, int, int] = (200, 200, 200)
    highlight_color: tuple[int, int, int] = (150, 0, 150)
    highlight_offset: int = 10

    def __init__(self, window_pos: tuple[int, int], size: tuple[int, int], text: str, on_click_function):
        self.window_pos: tuple[int, int] = window_pos
        self.size: tuple[int, int] = size
        self.on_click_function = on_click_function
        self.text_area = TextArea(window_pos, size, text)

    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """
        Draw the button, using highlight color if hovered.
        """
        rect = pygame.Rect(*self.window_pos, *self.size)
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.highlight_color, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)
        # Button text
        self.text_area.draw(screen)

    def click(self, *args):
        """
        Call the assigned on_click_function with provided arguments.
        """
        return self.on_click_function(*args)

    def handle_event(self, event: pygame.event.Event, *args):
        """
        Check if the button was clicked and call its callback if so.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            rect = pygame.Rect(*self.window_pos, *self.size)
            if rect.collidepoint(mouse_pos):
                return self.click(*args)
