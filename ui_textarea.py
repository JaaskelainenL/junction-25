import pygame

class TextArea:
    """
    Any text display, with word wrapping
    """
    text_color: tuple[int, int, int] = (0, 0, 0)

    def __init__(self, window_pos: tuple[int, int], size: tuple[int, int], text: str):
        self.window_pos = window_pos
        self.size = size
        self.text = text
        # Must be set in ctor because must be called after pygame init
        self.font: pygame.font.Font = pygame.font.Font(None, 32)

    def set_text(self, new_text: str):
        self.text = new_text

    def draw(self, screen: pygame.Surface):
        """
        Draw the rectangle and the wrapped text inside it.
        """
        # Wrap text to fit width
        words = self.text.split(None)
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            width, _ = self.font.size(test_line)

            if width < self.size[0] - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        x = self.window_pos[0] + 5
        y = self.window_pos[1] + 5

        line_height = self.font.get_height()

        for i, line in enumerate(lines):
            # Uncomment to allow cutting off text that doesnt fit into designated area
            #if y + line_height > self.window_pos[1] + self.size[1] - 5:
            #    break
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (x, y))

            # If this is the last visible line, update caret
            if i == len(lines) - 1:
                text_width = text_surface.get_width()
                self._caret_x = x + text_width
                self._caret_y = y

            y += line_height

    def get_caret_position(self) -> tuple[int, int, int]:
        """
        Returns (caret_x, caret_y, font_height (= caret height)).
        Used by TextInput to draw the blinking caret.
        """
        return self._caret_x, self._caret_y, self.font.get_height()