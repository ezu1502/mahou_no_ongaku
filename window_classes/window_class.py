import tkinter as tk
import os
from .button_class import MahouButton


class MahouWindow:

    def __init__(self, player, dimensions = "600x600"):
        self.player = player

        self.root = tk.Tk()
        self.root.title("Mahou no Ongaku - True Music Player")
        self.root.geometry(dimensions)
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.Xpressed)

        self.title_label = tk.Label(self.root, text = "Mahou no Ongaku")
        self.title_label.pack(pady = 20)

        self.status_label = tk.Label(self.root, text = "Status: Ready")
        self.status_label.pack(pady = 10)
        
        self.play_button = MahouButton(self.root, "▶ Play", self.test_button_pressed)

        # self.test_button = tk.Button(self.root, text = "Text Button", command = self.test_button_pressed)
        # self.test_button.pack(pady = 30) 

    def test_button_pressed(self):
        self.status_label.config(text = "Status: Button Pressed")
    def run(self):
        self.root.mainloop()

    def Xpressed(self):
        self.player.shut_program_down()
        self.root.destroy()
        os._exit(0)


            












