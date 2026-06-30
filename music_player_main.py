import time
import os
import getpass 
import pygame
from pygame.mixer import music as pymusic
import keyboard_receiver as controller
from file_handler import turn_path_into_list, return_or_show_musiclist, get_song_full_path
from state_handler import set_state_inmenu, set_state_playing, set_state_paused, check_state
from player_actions import pause_song, play_song, stop_song, unpause_song
from difflib import get_close_matches as fuzzymatch
import short_math as mycalc
import fuzzy_matcher

program_is_running = True
FPS = 60
FRAME_TIME = 1/FPS

user = getpass.getuser()
sourcefolder = rf"C:\Users\{user}\Mahou no Ongaku"
#define a pasta a ser usada e descobre o nome do usuário ativo

pygame.mixer.init()

player_state = {

    "mode" : "menu" #pode ser ""playing", "paused", "menu"
    
}


# IMPORT + VARIÁVEIS INICIAIS + PYGAME INIT


def get_wanted_song_index(string_input):
        try:
            integer_input = (int(string_input) - 1)
            return integer_input
        except ValueError:
            return None
        
def get_chosen_song(chosenlist):
    string_input = input("Choose song number:\n>")
    index = get_wanted_song_index(string_input)
    if index is not None:
        return index
    
    string_input




    
#Retorna um index de música



def quit():
    program_is_running = False
    return

def menu():
    global program_is_running
    while True:
        wannacontinue = input("What do you wanna do now?\nP = PLAY ANOTHER SONG\nL = LEAVE\n>")
        if wannacontinue.lower() == "l":
            quit()
        elif wannacontinue.lower() == "p":
            return_or_show_musiclist(sourcefolder)
            return
        else:
            continue  

def in_song_mode():
    ...

def counter(seconds):
    currenttime = time.monotonic()
    targettime = time.monotonic() + seconds
    


def deal_with_song_status():
    is_it_busy = pymusic.get_busy()
    check_key = check_key_and_return(player_state)
    state = check_state(player_state)

    if(state == "playing" and check_key == "pause"): #Spacebar
       pause_song(player_state)
    
    elif(state == "paused" and check_key == "unpause"): #Spacebar
       unpause_song(player_state) 
    
    elif(state in ("playing", "paused") and check_key == "stop"): #Música parando por comando do usuário
        print("Music Stopped.")
        stop_song(player_state)
        menu()
    
    elif(state == "playing" and not is_it_busy): #Música parou sozinha
        print("Song ended!")
        stop_song(player_state)
        menu()
    
    elif(state == "playing" and is_it_busy):
        in_song_mode()


        

#Checa o status da música e avisa se tiver acabado, também chama o cumpridor de comandos


def check_key_and_return(player_state):
    command = controller.command_detector()
    state = check_state(player_state)
   # print(command)
   # SPACEBAR
    if command == " ":
        if state == "playing":
            return "pause"
        elif state == "paused":
            return("unpause")
    elif command == "s":
            return("stop")


#def control_player():
  #  givencommand = check_key_and_return()

#TODO Ainda preciso fazer um tick mais preciso que esse

def realtick(initial_time):
    final_time = initial_time + FRAME_TIME
    current_time = time.monotonic()
    remaining = final_time - current_time

    if remaining > 0:
        time.sleep(remaining)
        

def tick():
    time.sleep(1 / FPS)
    #anda 1 frame


def update():
    deal_with_song_status()
    #atualiza tudo, chama o verificador


""" 

def show_list_and_play(chosenlist, folder):
    return_or_show_musiclist(chosenlist) #mostra a lista de musica

    chosen_song_index = get_chosen_song(chosenlist)
    chosen_song_path = get_song_full_path(chosen_song_index, chosenlist, folder)

    if chosen_song_path is not None:
        play_song(chosen_song_path, player_state)
        return
    else:
        print("Não foi possível encontrar a música")
        return "error"
#Faz as quatro funções mais importantes do file_handler em sequência: Mostra a lista de músicas, obtém o caminho da
#música e manda o Pygame tocar, também verifica se o número que o usuário digitou é válido
 """
#CORPO DO ARQUIVO:


loaded_music_list = turn_path_into_list(sourcefolder) #pega a pasta e lista as músicas
return_or_show_musiclist(loaded_music_list) #mostra a lista de músicas

chosen_song_index = get_chosen_song(loaded_music_list) #descobre a musica que o user quer ouvir
chosen_song_path = get_song_full_path(chosen_song_index, loaded_music_list, sourcefolder)#acha o caminho da música desejada

play_song(chosen_song_path, player_state) if chosen_song_path is not None else print("Não foi possível encontrar a música")
#Se o caminho for válido, toca a música. Senão, manda uma mensagem de erro
       

while program_is_running:
    thistime = time.monotonic()
    update()
    realtick(thistime)




    


