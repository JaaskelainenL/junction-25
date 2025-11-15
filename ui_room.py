import pygame
import random
from math import sqrt
from game import Character

class CharacterGUI:
    def __init__(self, character: Character, room_window_pos: tuple[int, int], room_size: tuple[int, int]):
        # new random instance with name as seed, so color and pos are always same
        self.character_name = character.get_name()
        rng = random.Random(self.character_name)
        self.color = rng.choices(range(256), k=3)

        offset_from_edges = 20
        self.local_pos = (rng.random(), rng.random())
        self.screen_pos = ((self.local_pos[0] * (room_size[0] - 2 * offset_from_edges)) + room_window_pos[0] + offset_from_edges,
                           (self.local_pos[1] * (room_size[1] - 2 * offset_from_edges)) + room_window_pos[1] + offset_from_edges)
        self.radius = 20

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.screen_pos, self.radius)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Returns true if this elements is clicked
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.is_inside_bounds(event.pos)
        return False

    def is_inside_bounds(self, position: tuple[int, int]) -> bool:
        # Euclidean dist of circle
        dist = sqrt((position[0] - self.screen_pos[0]) * (position[0] - self.screen_pos[0]) 
                    + (position[1] - self.screen_pos[1]) * (position[1] - self.screen_pos[1]))
        return dist < self.radius
    
    def get_name(self) -> str:
        return self.character_name


class RoomGUI:
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
            person.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> tuple[int, str]:
        """
        Handles mouse clicks for either selecting the room or selecting a person inside the room
        Returns the id of clicked room and name of clicked character (TODO return types)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_inside_bounds(event.pos):
                # character clicking
                for person in self.people_inside:
                    was_clicked = person.handle_event(event)
                    if was_clicked:
                        return -1, person.get_name()
                return self.room_id, ""
        return -1, ""
    
    def update(self, people_inside: list[Character]):
        """
        Update people in this room. CharacterGUI wrappers are made from them
        """
        self.people_inside = [CharacterGUI(c, self.window_pos, self.size) for c in people_inside]

    def is_inside_bounds(self, position: tuple[int, int]) -> bool:
        return ((self.window_pos[0] < position[0] < self.window_pos[0] + self.size[0])
            and (self.window_pos[1] < position[1] < self.window_pos[1] + self.size[1]))