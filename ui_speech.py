import pygame
import time
from ui_textarea import TextArea
from ui_room import CharacterGUI

class SpeechBubble:

    def __init__(self, character: CharacterGUI, text: str):
        self.character = character
        self.text_to_write = list(text)
        self.text_area = TextArea(window_pos=(300, 150), size=(600,400), text=f"{self.character}:\n")
        self.last_revealed = time.time()
        self.done = False
        self.all_written = False

    def draw(self, screen: pygame.Surface):
        self.text_area.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def reveal_letter(self, now: float):
        if len(self.text_to_write) > 0:
            self.text_area.text += self.text_to_write.pop(0)
            self.last_revealed = now
        else:
            self.all_written = True

    def update(self) -> bool:
        now = time.time()
        if not self.done:
            if not self.all_written and now - self.last_revealed > 0.5:
                self.reveal_letter(now)
            if self.all_written and now - self.last_revealed > 3:
                self.done = True
        return self.done
    
    def is_done(self) -> bool:
        return self.done