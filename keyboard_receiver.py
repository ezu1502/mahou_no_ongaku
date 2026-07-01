import pygame
import msvcrt as keyboard

#Player Controller
""" 
def command_detector():
    if not keyboard.kbhit():
        return None
    key = keyboard.getch().decode().lower()

    #print(key)
    return key """

def command_detector():
    if not keyboard.kbhit():
        return None
    key = keyboard.getch()
    skey = key.decode().lower()
    
    if key == b'\x1b':
        print("esc")
        return "esc"
    return skey

def anykey_detector():
    if keyboard.kbhit():
        return True
    return False