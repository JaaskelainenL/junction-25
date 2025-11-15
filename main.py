import pygame
import sys
import threading
from queue import Queue
from game import Game, PLAYER_NAME, STATES
from ui_room import RoomGUI
from ui_button import Button
from ui_textinput import TextInput
from ui_textarea import TextArea
from ui_clock import Clock as ClockGUI
from ui_speech import SpeechBubble
from ai import Conversation

WIDTH, HEIGHT = 1280, 720
BG_COLOR = (255, 255, 255)


class GameWindow:
    def __init__(self):
        self.game = Game()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Epic murder mystery game")

        self.conversations = {}


        self.block_interaction = False
        self.active_clicked_character = ""
        self.active_clicked_room = ""
        self.rooms = [
            RoomGUI(self.game.get_place(0), (600, 100)),
            RoomGUI(self.game.get_place(1), (900, 100)),
            RoomGUI(self.game.get_place(2), (750, 400))
        ]
        self.speech_queue: Queue[SpeechBubble] = Queue()
        self.active_speech: SpeechBubble | None = None
        self.init_gui_components()

    def update_people_in_all_rooms(self):
        for room in self.rooms:
            room.update(self.game.people_in_room(room.room_name))

    def advance_turn(self, selected_room: str):
        # End all conversations
        for conv in self.conversations.values():
            conv.end_conversation()

        self.conversations.clear()

        if not selected_room:
            selected_room = self.game.player.get_current_place()

        self.game.advance(selected_room)

        print(f"Moving to room {selected_room}!")
        # TODO
        self.update_people_in_all_rooms()
        self.phase_clock.set_time(self.game.get_time())

    def get_llm_response_async(self, conversation: Conversation, message: str, callback):
        def worker():
            response = conversation.send_message(message)
            callback(response)
        thread = threading.Thread(target=worker)
        thread.start()

    # This function is called every time "submit prompt" button is pressed
    def on_prompt_submit(self, input_field: TextInput):
        message = input_field.get_text()
        talking_to = self.active_clicked_character

        if not talking_to or not message:
            return        

        if talking_to not in self.conversations:
            self.conversations[talking_to] = Conversation(self.game.player, self.game.characters[talking_to], self.game.game_phase)

        self.add_speech_to_queue(PLAYER_NAME, message)

        self.get_llm_response_async(
            self.conversations[talking_to],
            message,
            callback=lambda response: self.add_speech_to_queue(talking_to, response.text)
        )
        input_field.clear()

    def on_kill(self):
        if self.active_clicked_character != "" and self.active_clicked_character != PLAYER_NAME:
            character = self.game.get_characters()[self.active_clicked_character]
            player = self.game.get_characters()[PLAYER_NAME]
            if character.get_current_place() == player.get_current_place():
                character.kill()
                print(f"{character.get_name()} alive: {character.is_alive()}")

        self.set_clicked_character("")

    def add_speech_to_queue(self, character_name: str, text: str):
        speech = SpeechBubble(character_name, text)
        self.speech_queue.put(speech)

    def init_gui_components(self):
        self.advance_button = Button(window_pos=(50, 50), size=(150, 50), text="Advance turn", on_click_function=self.advance_turn)
        self.prompt_input = TextInput(window_pos=(50, 150), size=(300,250), on_enter_function=self.on_prompt_submit)
        self.submit_prompt = Button(window_pos=(50, 500), size=(100,50), text="Submit", on_click_function=self.on_prompt_submit)
        self.phase_clock = ClockGUI(window_pos=(900, 50), size=(200, 50), start_time=self.game.get_time())
        self.character_selection_text = TextArea(window_pos=(400, 50), size=(400, 50), text="")
        self.debug = TextArea(window_pos=(50, 520), size=(400, 50), text="")
        self.kill_button = Button(window_pos=(800, 50), size=(100, 50), text="Kill", on_click_function=self.on_kill)
        # seen before first advance
        self.update_people_in_all_rooms()

    def draw_all(self):
        for room in self.rooms:
            room.draw(self.screen, self.active_clicked_room == room.room_name)

        mouse_pos = pygame.mouse.get_pos()
        # Draw rest of UI components
        self.advance_button.draw(self.screen, mouse_pos)
        self.prompt_input.draw(self.screen, mouse_pos)
        self.submit_prompt.draw(self.screen, mouse_pos)
        self.phase_clock.draw(self.screen)
        self.kill_button.draw(self.screen, mouse_pos)
        self.character_selection_text.draw(self.screen)

        debugtext = ""
        for c,k in self.game.characters.items():
            debugtext += f"{c} plan: {k.plan}".replace(" ", "") + " "

        self.debug.set_text(debugtext)

        self.debug.draw(self.screen)

        if (self.active_speech != None):
            self.active_speech.draw(self.screen)

        pygame.display.flip()

    def set_clicked_character(self, clicked_character):
        self.active_clicked_character = clicked_character
        self.character_selection_text.set_text(f"Selected character: {self.active_clicked_character}")
        self.kill_button.text_area.set_text(f"Kill {self.active_clicked_character}")

    def handle_standard_events(self, event):
        # Change active room and character selection
        for room in self.rooms:
            (clicked_room, clicked_character) = room.handle_event(event)

            if clicked_character != "":
                self.set_clicked_character(clicked_character)

            if clicked_room != "":
                self.active_clicked_room = clicked_room

        # Rest of components
        self.advance_button.handle_event(event, self.active_clicked_room)
        self.prompt_input.handle_event(event, self.prompt_input)
        self.submit_prompt.handle_event(event, self.prompt_input)
        self.kill_button.handle_event(event)

    def handle_speech(self):
        if not self.speech_queue.empty():
            if self.active_speech == None:
                self.active_speech = self.speech_queue.get()

        if self.active_speech != None:
            self.active_speech.update()
            if self.active_speech.is_done():
                self.active_speech = None
                self.block_interaction = False
            else:
                self.block_interaction = True

    def main_loop(self):
        running = True
        while running:
            if self.game.game_phase >= STATES:
                self.block_interaction = True
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # interaction is blocked when speech bubble is shown
                if not self.block_interaction:
                    self.handle_standard_events(event)

            self.handle_speech()
            self.draw_all()

        # end of game loop
        pygame.quit()

# ================ MAIN FUNC ==================
window = GameWindow()
window.main_loop()
sys.exit()
# =============================================