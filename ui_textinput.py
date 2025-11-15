import pygame
import time
from ui_textarea import TextArea

class TextInput:
    """
    A simple Pygame text input field with focus handling.
    It stores text internally and provides get_text() and clear().
    """
    text_color: tuple[int, int, int] = (0, 0, 0)
    bg_color: tuple[int, int, int] = (230, 230, 230)
    border_color: tuple[int, int, int] = (150, 150, 150)
    focus_color: tuple[int, int, int] = (100, 0, 150)
    border_width: int = 2

    def __init__(self, window_pos: tuple[int, int], size: tuple[int, int]):
        self.window_pos = window_pos
        self.size = size
        self.focused = False
        self._last_caret_switch = time.time()
        self._caret_visible = True
        self.text_area = TextArea(window_pos, size, "")

    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """
        Draw the input box, its border, the text, and caret when focused.
        """
        rect = pygame.Rect(*self.window_pos, *self.size)

        # Draw background
        pygame.draw.rect(screen, self.bg_color, rect)

        # Highlight border if focused or hovered
        if self.focused or rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.focus_color, rect, self.border_width)
        else:
            pygame.draw.rect(screen, self.border_color, rect, self.border_width)

        # Render underlying text area
        self.text_area.draw(screen)

        # Draw blinking caret
        if self.focused:
            now = time.time()
            if now - self._last_caret_switch > 0.5:
                self._caret_visible = not self._caret_visible
                self._last_caret_switch = now

            caret_pos = self.text_area.get_caret_position()
            if self._caret_visible:
                pygame.draw.line(screen, self.text_color, 
                                 (caret_pos[0], caret_pos[1]), 
                                 (caret_pos[0], caret_pos[1] + caret_pos[2]), 
                                 2)

    def handle_event(self, event: pygame.event.Event):
        """
        Handles mouse clicks for focusing and keyboard input when focused.
        """
        rect = pygame.Rect(*self.window_pos, *self.size)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Gain or lose focus
            self.focused = rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.focused:
            # Backspace
            if event.key == pygame.K_BACKSPACE:
                self.text_area.text = self.text_area.text[:-1]

            # Regular character input
            elif event.key == pygame.K_RETURN:
                pass  # You can ignore or handle Enter differently if desired
            else:
                self.text_area.text += event.unicode

    def get_text(self) -> str:
        """
        Returns the current text inside the field.
        """
        return self.text_area.text

    def clear(self):
        """
        Clears the text content.
        """
        self.text_area.text = ""
