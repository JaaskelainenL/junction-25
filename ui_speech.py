import pygame
import time
from ui_textarea import TextArea

LETTER_REVEAL_DELAY = 0.02
REMAIN_AFTER_FINISH = 3

class SpeechBubble:
    bg_color: tuple[int, int, int] = (140, 140, 160)

    def __init__(self, character_name: str, text: str):
        self.character_name = character_name
        self.text_to_write = list(text)
        self.window_pos = (300, 150)
        self.size = (600,400)
        self.text_pos = (self.window_pos[0], self.window_pos[1] + 50)
        self.text_size = (self.size[0], self.size[1] - 50)
        self.name_text = TextArea(self.window_pos, self.size, text=f"{self.character_name}:")
        self.text_area = TextArea(self.text_pos, self.text_size, text="")
        self.last_revealed = time.time()
        self.done = False
        self.all_written = False

    def draw(self, screen: pygame.Surface):
        rect = pygame.Rect(*self.window_pos, *self.size)
        pygame.draw.rect(screen, self.bg_color, rect)
        self.name_text.draw(screen)
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
            if not self.all_written and now - self.last_revealed > LETTER_REVEAL_DELAY:
                self.reveal_letter(now)
            if self.all_written and now - self.last_revealed > REMAIN_AFTER_FINISH:
                self.done = True
        return self.done
    
    def is_done(self) -> bool:
        return self.done