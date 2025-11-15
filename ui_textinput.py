import pygame
import time

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
        self.text = ""
        self.focused = False
        self._last_caret_switch = time.time()
        self._caret_visible = True
        # Must be set in ctor because must be called after pygame init
        self.font: pygame.font.Font = pygame.font.Font(None, 32)

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

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.window_pos[0] + 5, self.window_pos[1] + 5))

        # Draw blinking caret
        if self.focused:
            now = time.time()
            if now - self._last_caret_switch > 0.5:
                self._caret_visible = not self._caret_visible
                self._last_caret_switch = now

            if self._caret_visible:
                caret_x = self.window_pos[0] + 5 + text_surface.get_width()
                caret_y = self.window_pos[1] + 5
                caret_h = text_surface.get_height()
                pygame.draw.line(screen, self.text_color, (caret_x, caret_y), (caret_x, caret_y + caret_h), 2)

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
                self.text = self.text[:-1]

            # Regular character input
            elif event.key == pygame.K_RETURN:
                pass  # You can ignore or handle Enter differently if desired
            else:
                self.text += event.unicode

    def get_text(self) -> str:
        """
        Returns the current text inside the field.
        """
        return self.text

    def clear(self):
        """
        Clears the text content.
        """
        self.text = ""
