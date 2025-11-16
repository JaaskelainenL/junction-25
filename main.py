import pygame
import random
import sys
import threading
from typing import Self
from queue import Queue
from game import Game, PLAYER_NAME, STATES, Character
from ui_room import RoomGUI
from ui_button import Button
from ui_textinput import TextInput
from ui_textarea import TextArea
from ui_clock import Clock as ClockGUI
from ui_speech import SpeechBubble
from ai import Conversation, DetectiveConversation

WIDTH, HEIGHT = 1280, 720
BG_COLOR = (255, 255, 255)

class IWindow:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.block_interaction = False
        self.is_waiting = False
        self.speech_queue: Queue[SpeechBubble] = Queue()
        self.active_speech: SpeechBubble | None = None

    def add_speech_to_queue(self, character_name: str, text: str):
        speech = SpeechBubble(character_name, text)
        self.speech_queue.put(speech)
    
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

    def draw_all(self):
        pass # override

    def handle_standard_events(self, event):
        pass # override

    def get_next_window(self) -> Self | None:
        return None

    def get_llm_response_async(self, conversation: Conversation, message: str, callback):
        def worker():
            self.is_waiting = True # lock mutex
            response = conversation.send_message(message)
            callback(response)
            self.is_waiting = False
        thread = threading.Thread(target=worker)
        thread.start()

    def main_loop(self):
        running = True
        while running:
            next_window = self.get_next_window()
            if next_window:
                return next_window
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # interaction is blocked when speech bubble is shown
                if not self.block_interaction and not self.is_waiting:
                    self.handle_standard_events(event)

            self.handle_speech()
            self.draw_all()

        # end of game loop
        pygame.quit()

class GameWindow(IWindow):
    def __init__(self, screen: pygame.Surface):
        IWindow.__init__(self, screen)
        self.game = Game()
        self.conversations = {}
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

    # This function is called every time "submit prompt" button is pressed
    def on_prompt_submit(self, input_field: TextInput):
        message = input_field.get_text()
        talking_to = self.active_clicked_character
        if not talking_to or not message or talking_to == PLAYER_NAME:
            return        
        
        # Check if we are in the same room
        if self.game.characters[talking_to].get_current_place() != self.game.player.get_current_place():
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
                self.game.kill_character(character)
                print(f"{character.get_name()} alive: {character.is_alive()}")

        self.set_clicked_character("")

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

    def get_next_window(self):
        if self.game.game_phase >= STATES:
            return DetectiveWindow(self.screen, self.game)
        else:
            return None

class DetectiveWindow(IWindow):

    def __init__(self, screen: pygame.Surface, game: Game):
        IWindow.__init__(self, screen)
        self.game = game
        self.screen = screen
        self.prompt_input = TextInput(window_pos=(200, 100), size=(500,350), on_enter_function=self.on_prompt_submit)
        self.submit_prompt = Button(window_pos=(400, 500), size=(100,50), text="Submit", on_click_function=self.on_prompt_submit)
        self.add_speech_to_queue(f"It's {self.game.get_time()}", "Times up!")

        self.get_detective_async(
            callback=lambda response, person: self.add_speech_to_queue(person, response)
        )

    def get_detective_async(self, callback):
        def worker():
            self.is_waiting = True # lock mutex
            detective = DetectiveConversation(None, " and ".join(self.game.killed_people()))
            detective_char = Character("Detective")
            suspects = self.game.alive_people()
            random.shuffle(suspects)
            for suspect in suspects:
                sus_conversation = Conversation(detective_char, suspect, STATES)
                sus_conversation.send_message(f"""{detective.victim} has been killed by someone in this village. 
                                              A detective has come to find out who did it and will interrogate each town member. 
                                              Now it's your turn to answer the questions he asks you.""")
                question = detective.change_character(suspect)
                while detective.question_limit >= 0 and "i am done here" not in question.text.lower():
                    callback(question.text, f"{detective_char.get_name()} question #{detective.question_limit}")
                    response = sus_conversation.send_message(question.text)
                    callback(response.text, f"{suspect.get_name()}")
                    question = detective.send_message(response.text)
            final_response = detective.end_conversation()
            final_message = f"{final_response.suspect} did it. Reasoning: {final_response.explanation}"
            callback(final_message, f"{detective_char.get_name()} solution")
            self.is_waiting = False
        thread = threading.Thread(target=worker)
        thread.start()

    def on_prompt_submit(self, input_field: TextInput):
        message = input_field.get_text()
        
        self.add_speech_to_queue(PLAYER_NAME, message)
        #self.get_llm_response_async(
        #    self.conversations[talking_to],
        #    message,
        #    callback=lambda response: self.add_speech_to_queue(talking_to, response.text)
        #)
        input_field.clear()

    def draw_all(self):
        mouse_pos = pygame.mouse.get_pos()
        self.prompt_input.draw(self.screen, mouse_pos)
        self.submit_prompt.draw(self.screen, mouse_pos)

        if (self.active_speech != None):
            self.active_speech.draw(self.screen)

        pygame.display.flip()

    def handle_standard_events(self, event):
        self.prompt_input.handle_event(event, self.prompt_input)
        self.submit_prompt.handle_event(event, self.prompt_input)

# ================ MAIN FUNC ==================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic murder mystery game")

window = GameWindow(screen)
while window:
    window = window.main_loop()
sys.exit()
# =============================================