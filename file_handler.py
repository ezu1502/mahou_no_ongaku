
import os

#FILE HANDLER


def turn_path_into_list(folder):
    music_files_list = []

    files = os.listdir(folder)

    for eachfile in files:
        if eachfile.lower().endswith(".mp3"):
            music_files_list.append(eachfile)  
    music_files_list.sort(key=lambda name: name.lstrip("\ufeff").strip().lower())
    return music_files_list
#load_music_list() transforma a pasta escolhida em uma lista, eliminando os arquivos que não são .mp3

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

def return_or_show_musiclist(chosenlist, returnmode=False):
    
    if not returnmode:
    
        for indx, musicname in enumerate(chosenlist):

            index_and_name = (indx + 1, " ", (musicname))

            print(index_and_name)
        return None
    
# RETURNMODE!!
    index_and_name_list = []
    for indx, musicname in enumerate(chosenlist):
        fullname = (indx + 1, musicname)
        index_and_name_list.append(fullname)








# Mostra a lista com index e 

