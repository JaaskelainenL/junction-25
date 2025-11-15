import random

PLACES = [
    "House",
    "Field",
    "Forest"
]


PHASE_LOOKUP = ["6AM", "9AM", "12PM", "3PM", "6PM", "9PM"]
STATES = len(PHASE_LOOKUP)

PLAYER_NAME = "Jarmo"

PLAYER_NAMES = [
    "Alice", "Bob", "Carol", "Dave"
]

class Character:
    def __init__(self, name):
        self.name = name
        self.alive = True
        self.plan = [random.choice(PLACES) for i in range(STATES)]
        self.history = [self.plan.pop(0)]
        self.seen = []
        self.heard = []

    def kill(self):
        self.alive = False

    def is_alive(self):
        return self.alive

    def get_name(self):
        return self.name

    def get_current_place(self):
        return self.history[-1]

    def get_place(self, phase):
        return self.history[phase]

    def get_plans(self):
        return self.plan

    def get_seen(self):
        return self.seen

    def get_heard(self):
        return self.heard
    
    def add_heard(self, heard):
        self.heard.append(heard)
        self.heard = list(set(self.heard))
    
    def add_seen(self, seen_msg):
        self.seen.append(seen_msg)
        self.seen = list(set(self.seen))

    def get_history(self):
        return self.history
    
    def advance(self, next_phase, seen, place = None):
        if place is None:
            if self.plan:
                place = self.plan.pop(0)
            else:
                place = self.get_current_place()
                

        self.add_seen(f"{seen} in {self.get_current_place()} at {PHASE_LOOKUP[next_phase-1]}")
        self.history.append(place)



class Game():

    def __init__(self):
        self.characters = {name: Character(name) for name in PLAYER_NAMES}
        self.player = Character(PLAYER_NAME)
        self.characters[PLAYER_NAME] = self.player
        self.target = None

        self.game_phase = 0

    def people_in_room(self, room):
        return [c for c in self.characters.values() if c.get_current_place() == room]

    def get_characters(self):
        return self.characters
    
    def get_player(self):
        return self.player

    def get_time(self):
        return PHASE_LOOKUP[min(STATES-1,self.game_phase)]
    
    def get_place(self, index):
        return PLACES[index]

    def advance(self, player_move):
        if self.game_phase >= STATES:
            return
        t = self.game_phase
        for c in self.characters.values():
            if c.is_alive():
                seen = [character.get_name() for character in self.characters.values() if character.get_current_place() == c.get_current_place()]
                print(f"{c.get_name()} saw: {seen} in {c.get_current_place()}")
                
        for c in self.characters.values():
            print(f"{c.get_name()} has heard: {c.heard}")

        for c in self.characters.values():
            if c.is_alive():
                if c == self.player:
                    c.advance(t + 1, seen, player_move)
                else:
                    # randomly pick seen/heard to tell others
                    c.advance(t+1, seen)
        self.game_phase += 1




