import time
import os
import getpass 
import pygame
from pygame.mixer import music as pymusic
import keyboard_receiver as controller
import file_handler as fH
from difflib import get_close_matches as fuzzymatch
import toolkit.calc as mycalc
import toolkit.fuzzy_matcher as fuzzy_matcher
from music_player_class import MusicPlayer
from window_classes import MahouWindow, MahouButton

program_is_running = True
FPS = 60
FRAME_TIME = 1/FPS

WINDOW_DIMENSIONS = "900x600"
user = getpass.getuser()
sourcefolder = rf"C:\Users\{user}\Mahou no Ongaku"
#define a pasta a ser usada e descobre o nome do usuário ativo

pygame.mixer.init()

player = MusicPlayer()
window = MahouWindow(player, WINDOW_DIMENSIONS)

# window.run()
# IMPORT + VARIÁVEIS INICIAIS + PYGAME INIT

def welcome_screen():
    default_message = f"WELCOME to Mahou no Ongaku, the True Music Player!\nPress [ANY KEY] to continue!"
    if not player.check_welcome_was_shown():
        print(default_message)
        player.welcome_was_shown = True

    anykey = controller.anykey_detector()
    if anykey:
        player.set_state_menu()
        player.welcome_was_shown = False
        avoidbug = controller.anykey_detector()


def quit_program():
    global program_is_running
    program_is_running = False
    return

def stopped():
    wannacontinue = input("What do you wanna do now?\nP = PLAY ANOTHER SONG\nL = LEAVE\n>")
    if wannacontinue.lower() == "l":
        quit_program()
    elif wannacontinue.lower() == "p":
        player.set_state_menu()
        return
        

def check_key_and_return():
    command = controller.command_detector()
    state = player.check_state()
   # print(command)
   # SPACEBAR
    if command == " ":
        if state == "playing":
            return "pause"
        elif state == "paused":
            return("unpause")
    elif command == "s":
            return("stop")

def get_command_from_key():
    command = controller.command_detector()
    if command == " ":
       return "toggle" #playpause
    elif command == "s" or command == "esc":
       return "stop"
    elif command == "m":
        return "menu"

def in_song_mode(): #Vai rodar se o state for playing, e estiver tudo bonitinho, sem ninguém pausando nem nada
    check_key = get_command_from_key()
    if check_key == "toggle":
        player.pause_song()
        player.paused_was_shown = False
    elif check_key == "stop":
        player.stop_song()
        player.paused_was_shown = False
    elif check_key == "menu":
        player.set_state_menu()
        player.paused_was_shown = False
    

    


def paused_mode():
    if not player.paused_was_shown:
        print(" < PAUSED > ", end = "\n\n")
        print("[SPACEBAR] - RESUME Song\n[M] - Go to MENU")
        player.paused_was_shown = True

    check_key = get_command_from_key()

    if check_key == "toggle":
        player.unpause_song()
        player.paused_was_shown = False
    elif check_key == "menu":
        player.set_state_menu()
        player.paused_was_shown = False  
    elif check_key == "stop":
        player.set_state_stopped()
        player.paused_was_shown = False





    




def deal_with_song_status():
    is_it_busy = pymusic.get_busy()
    state = player.check_state()

    if(state == "playing" and not is_it_busy): #Música parou sozinha
        print("Song ended!")
        player.stop_song()   
    elif(state == "playing" and is_it_busy):
        in_song_mode()
    elif(state == "paused"):
        paused_mode()
    elif(state == "stopped"):
        stopped()
    elif(state == "shut_down"):
        quit_program()


# LIDAM COM CAMINHO DE MÚSICA 


def get_wanted_song_index(string_input):
        try:
            integer_input = (int(string_input) - 1)
            return integer_input
        except ValueError:
            return None
        

def get_closest_matches_list(string_input, chosenlist):
    string_input = string_input.lower()
    matcheslist = fuzzy_matcher.get_matches(string_input, chosenlist, number_of_matches=3)
    return matcheslist
        

def get_song_path():
    loaded_music_list = fH.turn_path_into_list(sourcefolder) #pega a pasta e lista as músicas
    fH.return_or_show_musiclist(loaded_music_list) #mostra a lista inicial
    songpath = None

    inputted = input("Type song number or name:\n>") #Motor da def: Acha o input do user

    try:
        wantedindex = int(inputted)
        wantedsong = loaded_music_list[wantedindex - 1]
        # print (wantedsong)
        songpath = os.path.join(sourcefolder, wantedsong)       #Se o input for número, já retorna um caminho pronto
        # print(songpath)
        return songpath
        
    except ValueError:

        list_that_matches_input = get_closest_matches_list(inputted, loaded_music_list)
        print("Based in your input, we found the following matches:")
        fH.return_or_show_musiclist(list_that_matches_input)            #se nao for int, acha as closematches da string
        secondinputted = input("Type song number or name:\n>")    #e faz uma nova lista, perguntando dnv qual o user quer
        
        try:
            wantedindex = int(secondinputted)
            wantedsong = list_that_matches_input[wantedindex - 1]
            print (wantedsong)
            songpath = os.path.join(sourcefolder, wantedsong)
            print(songpath)
            return songpath
        except Exception as error:
            print("Couldn't find the chosen song.", error)
            #TODO fazer uma última verificação de qual música quer
            player.set_state_stopped()
            return None
        
def get_path_and_play():
    songpath = get_song_path()

    if songpath is None:
        return
    try:
        player.play_song(songpath)
    except:
       player.set_state_stopped()
       print("Task failed.")
       return
    
#Se o caminho for válido, toca a música. Senão, manda uma mensagem de erro








def realtick(initial_time):
    final_time = initial_time + FRAME_TIME
    current_time = time.monotonic()
    remaining = final_time - current_time

    if remaining > 0:
        time.sleep(remaining)
        

def update():
    state = player.check_state()

    if state == "playing" or state == "paused":
        deal_with_song_status()
    elif state == "menu":
        get_path_and_play()
    elif state == "stopped":
        stopped()
    elif state == "welcomescreen":
        welcome_screen()
#atualiza tudo, decide oq cada estado faz



while program_is_running:
    thistime = time.monotonic()
    window.root.update()
    update()
    realtick(thistime)



