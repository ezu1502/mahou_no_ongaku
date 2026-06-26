
#STATE HANDLER!!!!!!!



def set_state_playing(player_state):
    player_state["should_be_playing"] = True
    player_state["is_it_paused"] = False
def set_state_paused(player_state):
    player_state["should_be_playing"] = True
    player_state["is_it_paused"] = True
def set_state_inmenu(player_state):
    player_state["should_be_playing"] = False
    player_state["is_it_paused"] = False

def check_state(player_state):
    if player_state["should_be_playing"] == True and player_state["is_it_paused"] == False:
        return "playing"
    elif player_state["should_be_playing"] == True and player_state["is_it_paused"] == True:
        return "paused"
    elif player_state["should_be_playing"] == False and player_state["is_it_paused"] == False:
        return "in menu"