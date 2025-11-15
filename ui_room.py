import pygame

class Room:
    """
    Render a room on the GUI (containing the characters in there)
    """
    size: tuple[int, int] = (200, 200)
    color = (200, 200, 200)
    highlight_offset = 10
    highlight_color = (150, 0, 150)

    def __init__(self, room_id: int, window_pos: tuple[int, int]):
        self.room_id = room_id
        self.window_pos = window_pos

    def draw(self, screen: pygame.Surface, highlight: bool):
        room_box = pygame.Rect(self.window_pos[0], self.window_pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, room_box)
        if highlight:
            pygame.draw.rect(screen, self.highlight_color, room_box, self.highlight_offset)

    def is_inside_bounds(self, position: tuple[int, int]):
        return ((self.window_pos[0] < position[0] < self.window_pos[0] + self.size[0])
            and (self.window_pos[1] < position[1] < self.window_pos[1] + self.size[1]))