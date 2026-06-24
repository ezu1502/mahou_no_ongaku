#Player Controller

import pygame
import msvcrt as keyboard

def command_detector():
    if not keyboard.kbhit():
        return None
    
    key = keyboard.getch().decode().lower()

    if key == "p":
        return "pause"
    if key == "s":
        return "select new song"
    if key == "l":
        return "leave"