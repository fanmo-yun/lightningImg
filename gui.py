import customtkinter as ctk
import pathlib

class Window(ctk.CTk):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry(f'{width}x{height}+{int((self.winfo_screenwidth() - width) / 2)}+{int((self.winfo_screenheight() - height) / 2)}')
        self.resizable(False, False)
        self.title(title)
        
        self.w = width
        self.h = height
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.home_path = pathlib.Path.home()
    
    def surface_size(self):
        return (self.width, self.height)

    def run(self):
        self.mainloop()

class Top_win(ctk.CTkToplevel):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()
        self.home_path = pathlib.Path.home()
        self.geometry(f'{width}x{height}+{int((self.winfo_screenwidth() - width) / 2)}+{int((self.winfo_screenheight() - height) / 2)}')
        self.resizable(False, False)
        self.title(title)

        self.w = width
        self.h = height
    
    def run(self):
        self.mainloop()