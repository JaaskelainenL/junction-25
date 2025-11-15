import pygame
import random

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
        self.people_inside = []

    def draw(self, screen: pygame.Surface, highlight: bool):
        room_box = pygame.Rect(self.window_pos[0], self.window_pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, room_box)
        if highlight:
            pygame.draw.rect(screen, self.highlight_color, room_box, self.highlight_offset)

        # Draw people inside this room
        for person in self.people_inside:
            rng = random.Random(person) # new random instance with name as seed
            person_color = rng.choices(range(256), k=3)
            offset_from_edges = 20
            pos = (rng.uniform(0, self.size[0] - 2 * offset_from_edges) + self.window_pos[0] + offset_from_edges, 
                   rng.uniform(0, self.size[1] - 2 * offset_from_edges) + self.window_pos[1] + offset_from_edges)

            radius = 20
            pygame.draw.circle(screen, person_color, pos, radius)

    def handle_event(self, event: pygame.event.Event) -> tuple[int, int]:
        """
        Handles mouse clicks for either selecting the room or selecting a person inside the room
        Returns the id of clicked room and id of clicked character (TODO return types)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_inside_bounds(event.pos):
                # TODO character clicking
                return self.room_id, -1
        return -1, -1
    
    def update(self, people_inside: list[str]):
        self.people_inside = people_inside

    def is_inside_bounds(self, position: tuple[int, int]):
        return ((self.window_pos[0] < position[0] < self.window_pos[0] + self.size[0])
            and (self.window_pos[1] < position[1] < self.window_pos[1] + self.size[1]))