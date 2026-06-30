import os
from state_handler import set_state_inmenu, set_state_playing, set_state_paused, check_state
import pygame
from pygame.mixer import music as pymusic



def play_song(path, player_state):
    if path is None:
        print("Número inválido:")
        return
    
    pymusic.load(path)
    pymusic.play()
    justthename = os.path.basename(path)
    stylizedname = f"< {justthename} >"
    print("Now Playing: ", stylizedname)
    set_state_playing(player_state)

def pause_song(player_state):
    pymusic.pause()
    print(" --PAUSED-- ")
    set_state_paused(player_state)
def unpause_song(player_state):
    pymusic.unpause()
    print("Playing!")
    set_state_playing(player_state)
def stop_song(player_state):
    pymusic.stop()
    set_state_inmenu(player_state)