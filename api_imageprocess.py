from api import check_path, remove_file, suit_img
from api_screenshot import ScreenShot_Win
from customtkinter import filedialog
import tkinter.messagebox as ctkmb
import customtkinter as ctk, sys
import tkinter as tk
from gui import Window
from gui_image import *
from PIL import ImageTk

class ImageProcess_Win(Window):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        check_path()
        self.config()
        self.filename = ""
        self.canvas_w = self.w-22
        self.canvas_h = self.h-150
    
    def release(self, howclose: bool, path):
        self.state("normal")
        self.attributes("-disabled", False)
        if howclose:
            self.ImageCanvas.delete(ctk.ALL)
            self.filename = path
        self.update_img()
    
    def main_surface(self):
        self.proframe = ctk.CTkFrame(master=self, width=self.w, height=self.h)
        self.loadbutton = ctk.CTkButton(master=self.proframe, text="加载", width=80, command=self.load_file, font=self.fontname)
        self.outputbutton = ctk.CTkButton(master=self.proframe, text="批量格式转换", width=80, command=self.output_multiple, font=self.fontname)
        self.savebutton = ctk.CTkButton(master=self.proframe, text="另存为", width=80, command=self.save_file, font=self.fontname)
        self.ImageCanvas = ctk.CTkCanvas(master=self.proframe, width=self.canvas_w, height=self.canvas_h, background='grey', highlightthickness=1, highlightbackground="grey")

        self.comprbutton = ctk.CTkButton(master=self.proframe, text="质量压缩", width=100, height=55, command=self.compression_img, font=self.fontname)
        self.wmarkbutton = ctk.CTkButton(master=self.proframe, text="翻转", width=100, height=55, command=self.rotate_img, font=self.fontname)
        self.zoombutton = ctk.CTkButton(master=self.proframe, text="缩放", width=100, height=55, command=self.zoom_img, font=self.fontname)
        self.blurbutton = ctk.CTkButton(master=self.proframe, text="模糊", width=100, height=55, command=self.blur_img, font=self.fontname)
        self.screenshotbutton = ctk.CTkButton(master=self.proframe, text="屏幕截取", width=340, height=55, command=self.screenshot_win, font=self.fontname)

        self.loadbutton.place(anchor='nw', x=10, y=10)
        self.outputbutton.place(anchor='nw', x=100, y=10)
        self.savebutton.place(anchor='nw', x=self.w-90, y=10)

        self.comprbutton.place(anchor='nw', x=10, y=self.h-80)
        self.wmarkbutton.place(anchor='nw', x=120, y=self.h-80)
        self.zoombutton.place(anchor='nw', x=230, y=self.h-80)
        self.blurbutton.place(anchor='nw', x=340, y=self.h-80)
        self.screenshotbutton.place(anchor='nw', x=450, y=self.h-80)

        self.ImageCanvas.place(anchor='nw', x=10, y=50)
        self.proframe.pack(fill="both", expand=True)
    
    def update_img(self):
        if len(self.filename) != 0:
            self.tk_img = ImageTk.PhotoImage(suit_img(self.filename, self.canvas_w, self.canvas_h)[0])
            self.ImageCanvas.create_image(self.canvas_w/2,self.canvas_h/2,anchor=ctk.CENTER, image=self.tk_img)
        else:
            self.ImageCanvas.delete(ctk.ALL)
        self.ImageCanvas.update()
    
    def screenshot_win(self):
        self.iconify()
        self.attributes("-disabled", True)
        self.screenshotwin = ScreenShot_Win("屏幕截取", 250, 100)
        self.screenshotwin.run(self.release)
    
    def load_file(self):
        filename = filedialog.askopenfilename(initialdir=self.home_path, title="打开文件", filetypes = (["jpeg files","*.jpg"], ["png files","*.png"]))
        if len(filename) != 0:
            self.filename = filename
        self.update_img()
    
    def save_file(self):
        if len(self.filename) != 0:
            savefile_path = filedialog.asksaveasfilename(initialdir=self.home_path, title="保存文件", defaultextension=".jpg",filetypes = (["jpeg files","*.jpg"], ["png files","*.png"]))
            if len(savefile_path) != 0: 
                Image.open(self.filename).save(savefile_path, quality=85)

    def output_multiple(self):
        self.attributes("-disabled", True)
        self.top1 = output_multiple_win("批量格式转换", 400, 300)
        self.top1.run(self.release)

    def compression_img(self):
        if len(self.filename) != 0:
            self.attributes("-disabled", True)
            self.top2 = compression_img_win("图片质量压缩", 300, 90, self.filename)
            self.top2.run(self.release)
        else:
            ctkmb.showerror(message="未加载图片")

    def rotate_img(self):
        if len(self.filename) != 0:
            self.attributes("-disabled", True)
            self.top3 = Rotate_img_win("图片旋转", 300, 90, self.filename)
            self.top3.run(self.release)
        else:
            ctkmb.showerror(message="未加载图片")

    def zoom_img(self):
        if len(self.filename) != 0:
            self.attributes("-disabled", True)
            self.top4 = Zoom_img_win("图片缩放处理", 300 ,90, self.filename)
            self.top4.run(self.release)
        else:
            ctkmb.showerror(message="未加载图片")

    def blur_img(self):
        if len(self.filename) != 0:
            self.attributes("-disabled", True)
            self.top5 = Blur_img_win("图片模糊处理", 300 ,90, self.filename)
            self.top5.run(self.release)
        else:
            ctkmb.showerror(message="未加载图片")
    
    def exit_win(self):
        remove_file(os.path.join("./temp"))
        sys.exit()

    def run(self):
        self.main_surface()
        self.protocol("WM_DELETE_WINDOW", self.exit_win)
        self.mainloop()