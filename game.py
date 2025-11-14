import random

PLACES = [
    "house",
    "field",
    "forest"
]

STATES = 3

PLAYERS = [
    "alice", "bob", "carol", "dave"
]



def get_start_plan():
    return [random.choice(PLACES) for i in range(STATES)]

def generate_player():
    return {
        "history": [],
        "plan": get_start_plan(),
        "seen": [],
        "heard": []
    }


class Game():    



    game_phase = 0
    game_status = { player: generate_player() for player in PLAYERS}
    


    player = {
        "place": random.choice(PLACES),
        "target": None
    }




    def update_history():
        for person in game_status.keys:
            game_status[person]["history"].append(game_status[person]["plan"][game_phase])


    def update_seen():
        for place in PLACES:
            people_there = [p for p in game_status.keys if game_status[p]["history"][game_phase] == place]

            for p in people_there:
                for p2 in people_there:
                    game_status[p]["seen"].append(f"{p2} seen at {place} during {game_phase}")




    def advance_state():
        update_history()


        game_phase += 1