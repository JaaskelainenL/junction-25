import pygame
import sys
import random
from game import Game
from ui_room import RoomGUI
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
pygame.display.set_caption("Epic murder mystery game")

BG_COLOR = (255, 255, 255)

active_clicked_character = ""
active_clicked_room = ""
rooms = [
    RoomGUI(game.get_place(0), (600, 100)),
    RoomGUI(game.get_place(1), (900, 100)),
    RoomGUI(game.get_place(2), (750, 400))
]

def update_people_in_all_rooms():
    for room in rooms:
        room.update(game.people_in_room(room.room_name))

def advance_turn(selected_room: str):
    print(f"Moving to room {selected_room}!")
    # TODO
    update_people_in_all_rooms()
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

character_selection_text = TextArea(window_pos=(400, 50), size=(400, 50), text="")

# seen before first advance
update_people_in_all_rooms()

# Main game loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change active room and character selection
        for room in rooms:
            (clicked_room, clicked_character) = room.handle_event(event)

            if clicked_character != "":
                active_clicked_character = clicked_character
                character_selection_text.set_text(f"Selected character: {active_clicked_character}")

            if clicked_room != "":
                active_clicked_room = clicked_room

        # Pass event handler to components
        advance_button.handle_event(event, active_clicked_room)
        prompt_input.handle_event(event)
        submit_prompt.handle_event(event, prompt_input)

    for room in rooms:
        room.draw(screen, active_clicked_room == room.room_name)

    mouse_pos = pygame.mouse.get_pos()
    # Draw rest of UI components
    advance_button.draw(screen, mouse_pos)
    prompt_input.draw(screen, mouse_pos)
    submit_prompt.draw(screen, mouse_pos)
    phase_clock.draw(screen)
    character_selection_text.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
