import pygame

class Room:
    room_id: int = -1
    window_pos: tuple[int, int] = (0, 0)
    size: tuple[int, int] = (200, 200)
    color = (200, 200, 200)
    highlight_offset = 10
    highlight_color = (150, 0, 150)

    def __init__(self, room_id: int, window_pos: tuple[int, int]):
        self.room_id = room_id
        self.window_pos = window_pos

    def render(self, screen: pygame.Surface, highlight: bool):
        room_box = pygame.Rect(self.window_pos[0], self.window_pos[1], self.size[0], self.size[1])
        if highlight:
            highlight_box = pygame.Rect(
                self.window_pos[0] - self.highlight_offset,
                self.window_pos[1] - self.highlight_offset, 
                self.size[0] + 2 * self.highlight_offset, 
                self.size[1] + 2 * self.highlight_offset
            )
            pygame.draw.rect(screen, self.highlight_color, highlight_box)

        pygame.draw.rect(screen, self.color, room_box)

    def is_inside_bounds(self, position: tuple[int, int]):
        return ((self.window_pos[0] < position[0] < self.window_pos[0] + self.size[0])
            and (self.window_pos[1] < position[1] < self.window_pos[1] + self.size[1]))