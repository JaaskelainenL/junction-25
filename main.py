import pygame
import sys
from game import Game
from ui_room import Room as RoomGUI
from ui_button import Button
from ui_textinput import TextInput
from ui_textarea import TextArea
from ui_clock import Clock as ClockGUI

game = Game()

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input Example")

BG_COLOR = (255, 255, 255)

active_clicked_room = -1
rooms = [
    RoomGUI(0, (600, 100)),
    RoomGUI(1, (900, 100)),
    RoomGUI(2, (750, 400))
]

def advance_turn(selected_room: int):
    print(f"Moving to room {selected_room}!")
    # TODO
    phase_clock.set_time(game.get_time())

# This function is called every time "submit prompt" button is pressed
def on_prompt_submit(input_field: TextInput):
    print(f"Input: {input_field.get_text()}")
    # TODO
    input_field.clear()

advance_button = Button(window_pos=(50, 50), size=(150, 50), text="Advance turn", on_click_function=advance_turn)
prompt_input = TextInput(window_pos=(50, 150), size=(300,250))
submit_prompt = Button(window_pos=(50, 500), size=(100,50), text="Submit", on_click_function=on_prompt_submit)
phase_clock = ClockGUI(window_pos=(900, 50), size=(200, 50), start_time=game.get_time())

# Main game loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change active room selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            for room in rooms:
                if room.is_inside_bounds(event.pos):
                    active_clicked_room = room.room_id

        # Pass event handler to components
        advance_button.handle_event(event, active_clicked_room)
        prompt_input.handle_event(event)
        submit_prompt.handle_event(event, prompt_input)

    for room in rooms:
        room.draw(screen, active_clicked_room == room.room_id)

    mouse_pos = pygame.mouse.get_pos()
    # Draw rest of UI components
    advance_button.draw(screen, mouse_pos)
    prompt_input.draw(screen, mouse_pos)
    submit_prompt.draw(screen, mouse_pos)
    phase_clock.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
