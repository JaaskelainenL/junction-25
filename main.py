import pygame
import sys
import random
from game import Game
from ui_room import RoomGUI
from ui_button import Button
from ui_textinput import TextInput
from ui_textarea import TextArea
from ui_clock import Clock as ClockGUI

WIDTH, HEIGHT = 1280, 720
BG_COLOR = (255, 255, 255)

class GameWindow:
    def __init__(self):
        self.game = Game()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Epic murder mystery game")

        self.active_clicked_character = ""
        self.active_clicked_room = ""
        self.rooms = [
            RoomGUI(self.game.get_place(0), (600, 100)),
            RoomGUI(self.game.get_place(1), (900, 100)),
            RoomGUI(self.game.get_place(2), (750, 400))
        ]
        self.init_gui_components()

    def update_people_in_all_rooms(self):
        for room in self.rooms:
            room.update(self.game.people_in_room(room.room_name))

    def advance_turn(self, selected_room: str):
        print(f"Moving to room {selected_room}!")
        # TODO
        self.update_people_in_all_rooms()
        self.phase_clock.set_time(self.game.get_time())

    # This function is called every time "submit prompt" button is pressed
    def on_prompt_submit(self, input_field: TextInput):
        print(f"Input: {input_field.get_text()}")
        # TODO
        input_field.clear()

    def init_gui_components(self):
        self.advance_button = Button(window_pos=(50, 50), size=(150, 50), text="Advance turn", on_click_function=self.advance_turn)
        self.prompt_input = TextInput(window_pos=(50, 150), size=(300,250))
        self.submit_prompt = Button(window_pos=(50, 500), size=(100,50), text="Submit", on_click_function=self.on_prompt_submit)
        self.phase_clock = ClockGUI(window_pos=(900, 50), size=(200, 50), start_time=self.game.get_time())
        self.character_selection_text = TextArea(window_pos=(400, 50), size=(400, 50), text="")
        # seen before first advance
        self.update_people_in_all_rooms()

    def main_loop(self):
        running = True
        while running:
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Change active room and character selection
                for room in self.rooms:
                    (clicked_room, clicked_character) = room.handle_event(event)

                    if clicked_character != "":
                        active_clicked_character = clicked_character
                        self.character_selection_text.set_text(f"Selected character: {active_clicked_character}")

                    if clicked_room != "":
                        self.active_clicked_room = clicked_room

                # Pass event handler to components
                self.advance_button.handle_event(event, self.active_clicked_room)
                self.prompt_input.handle_event(event)
                self.submit_prompt.handle_event(event, self.prompt_input)

            for room in self.rooms:
                room.draw(self.screen, self.active_clicked_room == room.room_name)

            mouse_pos = pygame.mouse.get_pos()
            # Draw rest of UI components
            self.advance_button.draw(self.screen, mouse_pos)
            self.prompt_input.draw(self.screen, mouse_pos)
            self.submit_prompt.draw(self.screen, mouse_pos)
            self.phase_clock.draw(self.screen)
            self.character_selection_text.draw(self.screen)

            pygame.display.flip()

        # end of game loop
        pygame.quit()

# ================ MAIN FUNC ==================
window = GameWindow()
window.main_loop()
sys.exit()
# =============================================