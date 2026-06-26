import pygame
import msvcrt as keyboard

#Player Controller

def command_detector():
    if not keyboard.kbhit():
        return None
    key = keyboard.getch().decode().lower()
    #print(key)
    return key