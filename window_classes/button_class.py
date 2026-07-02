import tkinter as tk



class MahouButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            text = text,
            command = command,
            font = ("Segoe UI", 14),
            width = 20,
            height = 2,
            bg = "#222222",
            fg = "#ffffff",
            activebackground = "#333333",
            activeforeground = "#ffffff"
        )
            
        self.pack()



