from PIL import ImageGrab, ImageTk, Image
import customtkinter as ctk
from customtkinter import filedialog
from gui import Window
from api import get_time
import os, time

class ScreenShot_Win(Window):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        self.minimize = False
    
    def main_surface(self):
        self.frame1 = ctk.CTkFrame(master=self)
        self.switch1 = ctk.CTkSwitch(self.frame1, text="最小化", command=self.change_val)
        self.button1 = ctk.CTkButton(self.frame1, width=50, text="全屏截取", command=self.full_screenshot)
        self.button2 = ctk.CTkButton(self.frame1, width=50, text="选区截取", command=self.rect_screenshot)
        
        self.switch1.pack(side=ctk.TOP)
        self.button1.pack(side=ctk.LEFT, padx=40)
        self.button2.pack(side=ctk.LEFT)
        self.frame1.pack(fill="both", expand=True)
    
    def change_val(self):
        if self.minimize == False:
            self.minimize = True
        else:
            self.minimize = False
    
    def full_screenshot(self):
        if self.minimize:
            self.iconify()
        filepath = filedialog.asksaveasfilename(initialdir=self.home_path, defaultextension=".png", title = "Save", filetypes = (["png files","*.png"], ["jpeg files","*.jpg"]))
        if len(filepath) != 0:
            self.screenshot(filepath, (0,0), self.surface_size(), 95)
        self.state('normal')
    
    def rect_screenshot(self):
        if self.minimize:
            self.iconify()
            time.sleep(0.5)
        path = os.path.join("temp")
        now_time = get_time()
        tempath = os.path.join(path, f"{now_time}.png")
        self.screenshot(tempath, (0,0), self.surface_size(), 75)
        self.process_img(tempath)
    
    def screenshot(self, path, startsize, endsize, qua):
        full_size = startsize + endsize
        img_data = ImageGrab.grab(full_size)
        img_data.save(path, quality=qua)

    def scope_screen(self, path_in, path_out, startsize, endsize, qua):
        img = Image.open(path_in)
        if startsize[0] - endsize[0] == 0:
            self.release()
        if startsize > endsize:
            cropsize = endsize + startsize
        else:
            cropsize = startsize + endsize
        cropped = img.crop(cropsize)
        cropped.save(path_out, quality=qua)

    def process_img(self, path):
        self.attributes("-disabled", True)
        img = ImageTk.PhotoImage(Image.open(path))

        self.handlewin = ctk.CTkToplevel()
        self.handlewin.geometry(f"{self.width}x{self.height}")
        self.handlewin.attributes("-fullscreen", True)
        
        self.handlecanvas = ctk.CTkCanvas(self.handlewin, width=self.width, height=self.height, highlightthickness=1, highlightbackground="black",cursor="cross")
        self.handlecanvas.pack(side="top", fill="both", expand=True)
        self.handlecanvas.create_image(0, 0, anchor=ctk.NW, image=img)
        self.handlecanvas.bind(sequence="<ButtonPress-1>", func=self.get_start_pos)
        self.handlecanvas.bind(sequence="<B1-Motion>", func=self.draw_rect)
        self.handlecanvas.bind(sequence="<ButtonRelease-1>", func=lambda event: self.scope_screenshot(event, path))
        self.handlecanvas.bind(sequence="<Button-3>", func=lambda event: self.close_win(event))
        
        self.handlewin.protocol("WM_DELETE_WINDOW", self.release_win)
        self.handlewin.mainloop()
    
    def get_start_pos(self, event):
        self.startx = event.x
        self.starty = event.y
        self.rect = self.handlecanvas.create_rectangle(self.startx, self.starty, self.startx + 1, self.starty + 1, outline='white', width=1)

    def get_end_pos(self, event):
        self.endx = event.x
        self.endy = event.y

    def draw_rect(self, event):
        nowx = event.x
        nowy = event.y
        self.handlecanvas.coords(self.rect, self.startx, self.starty, nowx, nowy)

    def scope_screenshot(self, event, path):
        self.get_end_pos(event)
        self.release()
        filepath = filedialog.asksaveasfilename(initialdir=self.home_path, defaultextension=".png", title = "Save", filetypes = (["png files","*.png"], ["jpeg files","*.jpg"]))
        if len(filepath) != 0:
            self.scope_screen(path, filepath, (self.startx, self.starty), (self.endx, self.endy), 95)
    
    def close_win(self, event):
        self.release()
    
    def release_win(self):
        self.release()
    
    def release(self):
        self.state('normal')
        self.attributes("-disabled", False)
        self.handlewin.destroy()
    
    def release_main_win(self, release_main):
        self.destroy()
        release_main(False, None)
    
    def run(self, release_main):
        self.main_surface()
        self.protocol("WM_DELETE_WINDOW",lambda: self.release_main_win(release_main))
        self.mainloop()