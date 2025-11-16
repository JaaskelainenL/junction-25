import pygame
import random
from math import sqrt
from game import Character, PLAYER_NAME
from ui_textarea import TextArea

SHOW_ALL_CHARACTERS = True

class CharacterGUI:
    def __init__(self, character: Character, room_window_pos: tuple[int, int], room_size: tuple[int, int]):
        # new random instance with name as seed, so color and pos are always same
        self.character = character
        self.character_name = character.get_name()
        rng = random.Random(self.character_name.lower() + "abc")
        self.color = rng.choices(range(256), k=3)

        offset_from_edges = 20
        self.local_pos = (rng.random(), rng.random())
        self.screen_pos = ((self.local_pos[0] * (room_size[0] - 2 * offset_from_edges)) + room_window_pos[0] + offset_from_edges,
                           (self.local_pos[1] * (room_size[1] - 2 * offset_from_edges)) + room_window_pos[1] + offset_from_edges)
        self.radius = 20

    def draw(self, screen: pygame.Surface):
        if self.character_name == PLAYER_NAME:
            player_rect = pygame.Rect(self.screen_pos[0] - self.radius, 
                                      self.screen_pos[1] - self.radius, 
                                      2 * self.radius, 2 * self.radius)
            pygame.draw.rect(screen, self.color, player_rect)
        else:
            if self.character.is_alive():
                pygame.draw.circle(screen, self.color, self.screen_pos, self.radius)
            else:
                pygame.draw.ellipse(screen, self.color, pygame.Rect(self.screen_pos[0] - self.radius, 
                                      self.screen_pos[1] - 0.25* self.radius, 
                                      2 * self.radius, 0.5 * self.radius))

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

    def __init__(self, room_name: str, window_pos: tuple[int, int]):
        self.room_name = room_name
        self.window_pos = window_pos
        self.people_inside = []
        self.label = TextArea(window_pos, self.size, room_name)

    def draw(self, screen: pygame.Surface, highlight: bool):
        room_box = pygame.Rect(self.window_pos[0], self.window_pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, room_box)
        if highlight:
            pygame.draw.rect(screen, self.highlight_color, room_box, self.highlight_offset)

        self.label.draw(screen)

        # Draw people inside this room
        for person in self.people_inside:
            person.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> tuple[str, str]:
        """
        Handles mouse clicks for either selecting the room or selecting a person inside the room
        Returns the name of clicked room and name of clicked character (TODO return types)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_inside_bounds(event.pos):
                # character clicking
                for person in self.people_inside:
                    was_clicked = person.handle_event(event)
                    if was_clicked:
                        return "", person.get_name()
                return self.room_name, ""
        return "", ""
    
    def update(self, people_inside: list[Character]):
        """
        Update people in this room. CharacterGUI wrappers are made from them. People inside is set to empty list
        if SHOW_ALL_CHARACTERS=False and player is not in the room
        """
        is_player_inside = len([c for c in people_inside if c.get_name() == PLAYER_NAME]) > 0
        if SHOW_ALL_CHARACTERS or is_player_inside:
            self.people_inside = [CharacterGUI(c, self.window_pos, self.size) for c in people_inside]

    def is_inside_bounds(self, position: tuple[int, int]) -> bool:
        return ((self.window_pos[0] < position[0] < self.window_pos[0] + self.size[0])
            and (self.window_pos[1] < position[1] < self.window_pos[1] + self.size[1]))