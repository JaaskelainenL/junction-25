import pygame
import sys
from game import Game
from ui_room import Room
from ui_button import Button
from ui_textinput import TextInput

game = Game()

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

active_clicked_room = -1
rooms = [
    Room(0, (600, 100)),
    Room(1, (900, 100)),
    Room(2, (750, 400))
]

def greet(name: str):
    print(f"Hello {name}!")

# This function is called every time "submit prompt" button is pressed
def on_prompt_submit(input_field: TextInput):
    print(f"Input: {input_field.get_text()}")
    input_field.clear()


# Create button
button = Button(window_pos=(50, 50), size=(150, 50), on_click_function=greet)

prompt_input = TextInput(window_pos=(50, 150), size=(300,250))
submit_prompt = Button(window_pos=(50, 500), size=(100,50), on_click_function=on_prompt_submit)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change active room selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            for room in rooms:
                if room.is_inside_bounds(event.pos):
                    active_clicked_room = room.room_id

        button.handle_event(event, "World!")
        prompt_input.handle_event(event)
        submit_prompt.handle_event(event, prompt_input)

    for room in rooms:
        room.render(screen, active_clicked_room == room.room_id)

    mouse_pos = pygame.mouse.get_pos()
    button.draw(screen, mouse_pos)
    prompt_input.draw(screen, mouse_pos)
    submit_prompt.draw(screen, mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
