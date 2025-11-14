import random

PLACES = [
    "house",
    "field",
    "forest"
]

STATES = 3

PLAYER_NAMES = [
    "alice", "bob", "carol", "dave"
]
def get_start_plan():
    return [random.choice(PLACES) for i in range(STATES)]

class Character:
    def __init__(self, name):
        self.name = name
        self.history = []
        self.plan = [random.choice(PLACES) for i in range(STATES)]
        self.seen = []
        self.heard = []

    def get_current_place(self):
        return self.history[-1]

    def get_place(self, phase):
        return self.history[phase]

    def get_plan(self, phase):
        return self.plan[phase]

    def get_seen(self, phase):
        return self.seen[phase]

    def get_heard(self, phase):
        return self.heard[phase]
    
    def add_heard(self, heard):
        self.heard.append(heard)


    def advance(self, next_phase, seen, place = None):
        if place is None:
            place = self.plan[next_phase]

        self.history.append(place)
        self.seen.append(seen)



class Game():

    def __init__(self):
        self.characters = {name: Character(name) for name in PLAYER_NAMES}
        self.player = Character("player")
        self.characters["player"] = self.player
        self.target = None

        self.game_phase = 0

    def people_in_room(self, room):
        return [c.get_current_place() for c in self.characters.values]


    def advance(self, player_move):
        t = self.game_phase
        for c in self.characters.values:
            seen = [character.get_current_place() for character in self.characters.values]

            if c == self.player:
                c.advance(t + 1, seen, player_move)
            else:
                c.advance(t+1, seen)
        self.game_phase += 1




