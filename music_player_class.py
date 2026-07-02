from pygame.mixer import music as pymusic
import os

class MusicPlayer:

    def __init__(self):
        self.mode = "welcomescreen" #pode ser "playing", "paused", "menu", "stopped", "welcomescreen"
        self.welcome_was_shown = False
        self.paused_was_shown = False

    def set_state_playing(self):
        self.mode = "playing"

    def set_state_paused(self):
        self.mode = "paused"

    def set_state_stopped(self):
        self.mode = "stopped"

    def set_state_menu(self):
        pymusic.stop()
        self.mode = "menu"

    def set_state_killed(self):
        pymusic.stop()
        self.mode = "shut_down"
        
    def set_state_welcomescreen(self):
        self.mode = "welcomescreen"

    def check_state(self):
        return self.mode



    def play_song(self, path):
        if self.mode != "playing":
            if path is None:
                print("Número inválido:")
                self.set_state_stopped()
                return
            
            pymusic.load(path)
            pymusic.play()

            justthename = os.path.basename(path)
            stylizedname = f"< {justthename} >"
            print("Now Playing: ", stylizedname)
            self.set_state_playing()
        

    def pause_song(self):
        if self.mode == "playing":
            pymusic.pause()
            self.set_state_paused()

    def unpause_song(self):
        if self.mode == "paused":
            pymusic.unpause()
            print("Playing!")
            self.set_state_playing()

    def stop_song(self):
        if self.mode == "playing" or self.mode == "paused":
            pymusic.stop()
            self.set_state_stopped()

    def shut_program_down(self):
        if self.mode != "shut_down":
            pymusic.stop()
            self.set_state_killed()

    def check_welcome_was_shown(self):
        return self.welcome_was_shown
    def check_pause_was_shown(self):
        return self.pause_was_shown









