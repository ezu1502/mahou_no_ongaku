import time
import os
import getpass 
import pygame
import player_controls as controller
#import Player Controller


program_is_running = True
FPS = 60

user = getpass.getuser()
sourcefolder = rf"C:\Users\{user}\Mahou no Ongaku"
#define a pasta a ser usada e descobre o nome do usuário ativo

pygame.mixer.init()
now_playing = False

# IMPORT + VARIÁVEIS INICIAIS + PYGAME INIT


def load_music_list(folder):
    music_files_list = []

    files = os.listdir(folder)

    for eachfile in files:
        if eachfile.lower().endswith(".mp3"):
            music_files_list.append(eachfile)   
    music_files_list.sort(key=lambda name: name.lstrip("\ufeff").strip().lower())
    return music_files_list


#load_music_list() transforma a pasta escolhida em uma lista, eliminando os arquivos que não são .mp3
# e retorna essa lista. printmusiclist() printa no terminal cada nome de arquivo junto com um número no formato:
# Número, Nome.mp3



#Executando load e print na nossa pasta escolhida sourcefolder, atribuindo a lista a uma variável global loaded_...

# PREPARANDO OS ARQUIVOS
def showmusiclist(chosenlist):
    for indx, musicname in enumerate(chosenlist):
        print(indx + 1, " ", (musicname))

def askget_music_number():
    while True:
        try:
            chosenmusicnumber = int(input("Choose song number:\n>")) - 1
            return chosenmusicnumber
        except ValueError:
            print("Dumbass, type a number")
            continue
#Pega o input do usuário e retorna ele -1 pra usarmos na arraylist

def get_song_full_path(musicnumber, loadedmusiclist, folder):
    listlength = len(loadedmusiclist)
    if musicnumber < 0 or musicnumber >= listlength:
        print("Please choose a number between 1 and ", listlength)
        return None
    song_name = loadedmusiclist[musicnumber]
    #print(song_name)
    fullsongpath = os.path.join(folder, song_name)
    #print(fullsongpath)
    return fullsongpath
            
        
#Retorna o caminho da música baseado no numero que receber

def play_song(path):
    global now_playing

    if path is None:
        print("Número inválido:")
        return
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    justthename = os.path.basename(path)
    stylizedname = f"< {justthename} >"
    print("Now Playing: ", stylizedname)
    now_playing = True
   
       
#Manda o Pygame tocar a música e avisa o update()

#loadedlist = loaded_music_list


def show_list_and_play(loadedlist, folder):
    while True:
        showmusiclist(loadedlist)
        numberweget = askget_music_number()
        wannaplay = get_song_full_path(numberweget, loadedlist, folder)
        if wannaplay is not None:
            play_song(wannaplay)
            return
#Faz as quatro funções acima em sequência: Mostra a lista de músicas, obtém o caminho da música e manda o Pygame tocar
#Também verifica se o número que o usuário digitou é válido
loaded_music_list = load_music_list(sourcefolder)
show_list_and_play(loaded_music_list, sourcefolder)

def ask_leave_or_play_new_song():
    global program_is_running
    while True:
        wannacontinue = input("What do you wanna do now?\nP = PLAY ANOTHER SONG\nL = LEAVE\n>")
        if wannacontinue.lower() == "l":
            program_is_running = False
            return
        elif wannacontinue.lower() == "p":
            show_list_and_play(loaded_music_list, sourcefolder)
            return
        else:
            continue  


def tick():
    time.sleep(1 / FPS)
    #anda 1 frame

def update():
    global now_playing
    
    reallyplaying = pygame.mixer.music.get_busy()


    if(now_playing and reallyplaying):
       status = controller.command_detector()
       if status is not None:
            print(status)

    elif(now_playing and not reallyplaying):
        print("Cabou a música kkkkkkkk")
        now_playing = False
        ask_leave_or_play_new_song()

    #atualiza tudo, verifica se a música tá rodando


while program_is_running:
    update()
    tick()



   