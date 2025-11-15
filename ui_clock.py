import pygame
from ui_textarea import TextArea

class Clock:
    """
    Draw clock element into GUI (shows game phase)
    """

    def __init__(self, window_pos: tuple[int, int], size: tuple[int, int], start_time: str):
        self.window_pos = window_pos
        self.size = size
        self.text_area = TextArea(window_pos, size, "")
        self.set_time(start_time)

    def set_time(self, time: str):
        self.time = time
        self.text_area.set_text(f"Time is: {time}")

    def draw(self, screen: pygame.Surface):
        # TODO render some clock sprite
        self.text_area.draw(screen)