import pygame
from pygame.mixer import music as Pymusic


class MahouPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play_song(self, song_path):
        Pymusic.load(song_path)
        Pymusic.play()