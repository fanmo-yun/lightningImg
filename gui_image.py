from gui import Top_win
from api import get_time
import customtkinter as ctk, os
from customtkinter import filedialog
import tkinter.messagebox as ctkmb
from PIL import Image, ImageFilter

class output_multiple_win(Top_win):
    def __init__(self, title: str, width: int, height: int):
        super().__init__(title, width, height)
        self.combobox_var = ctk.StringVar(value="JPEG")
        self.filelist = []
    
    def main_surface(self):
        self.btn1 = ctk.CTkButton(self, text="加载", width=90, command=self.load_file)
        self.btn2 = ctk.CTkButton(self, text="清空列表", width=90, command=self.clear_all)
        self.conbtn = ctk.CTkButton(self, text="Convert", width=90, command=self.convert)
        self.combobox = ctk.CTkComboBox(self, values=["JPEG", "PNG"], width=80, variable=self.combobox_var, state="readonly")
        self.textbox = ctk.CTkTextbox(self, height=240)
        self.textbox.configure(state="disabled")

        self.btn1.place(anchor='nw', x=10, y=10)
        self.btn2.place(anchor='nw', x=120, y=10)
        self.conbtn.place(anchor='nw', x=245, y=(self.h/2)+40)
        self.combobox.place(anchor='nw', x=250, y=(self.h/2)-40)
        self.textbox.place(anchor='nw', x=10, y=50)
    
    def load_file(self):
        self.textbox.configure(state="normal")
        file_names = filedialog.askopenfilenames(initialdir=self.home_path, title="Open", filetypes=(["jpeg files", "*.jpg"], ["png files", "*.png"]))
        if len(list(file_names)) != 0:
            for file in list(file_names):
                if file not in self.filelist:
                    self.filelist.append(file)
                    self.textbox.insert("0.0", file + "\n")
        self.textbox.configure(state="disabled")
    
    def clear_all(self):
        if len(self.filelist) != 0:
            self.filelist.clear()
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", ctk.END)
            self.textbox.configure(state="disabled")

    def convert(self):
        name = self.combobox.get()
        out_path = filedialog.askdirectory(initialdir=self.home_path, title="Save")
        if len(out_path) != 0:
            try:
                for convert_file in self.filelist:
                        img = Image.open(convert_file)
                        (_, file_name) = os.path.split(convert_file)
                        file_name = file_name.split(".")[0]
                        if img.format != name:
                            img = img.convert("RGB")
                            img.save(f"{out_path}/{file_name}.{name}", format=name, quality=95)
            except:
                ctkmb.showerror(title="格式转换", message="图片转换出错,请重试")
            finally:
                ctkmb. showinfo(title="格式转换", message="转换完毕")
                
    def release_win(self, release):
        self.destroy()
        release(False, None)
        del self

    def run(self, release):
        self.protocol("WM_DELETE_WINDOW", lambda: self.release_win(release))
        self.main_surface()
        self.mainloop()

class compression_img_win(Top_win):
    def __init__(self, title: str, width: int, height: int, file: str):
        super().__init__(title, width, height)
        self.defaultvar = ctk.IntVar(value=95)
        self.var = ctk.StringVar(value="95")
        self.file = file
    
    def main_surface(self, release):
        self.slider = ctk.CTkSlider(self, from_=1, to=100, variable=self.defaultvar, command=self.show_num)
        self.label = ctk.CTkLabel(self, textvariable=self.var)
        self.but1 = ctk.CTkButton(self, text="Done", width=60, command=lambda: self.save_file(release))
        
        self.slider.pack(side=ctk.TOP, pady=3)
        self.label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        self.but1.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
    
    def show_num(self, num):
        self.var.set(str(int(num)))
    
    def save_file(self, release):
        path = os.path.join("temp", f"{get_time()}.jpg")
        try:
            if len(path) != 0:
                img = Image.open(self.file)
                img = img.convert("RGB")
                img.save(path, quality=int(self.var.get()))
                self.destroy()
                release(True, path)
                del self
        except:
            ctkmb.showerror(title="质量压缩", message="图片压缩出错,请重试")
        finally:
            ctkmb.showinfo(title="质量压缩",message="完毕")
    
    def release_win(self, release):
        self.destroy()
        release(False, None)
        del self

    def run(self, release):
        self.protocol("WM_DELETE_WINDOW", lambda: self.release_win(release))
        self.main_surface(release)
        self.mainloop()

class Zoom_img_win(Top_win):
    def __init__(self, title: str, width: int, height: int, file: str):
        super().__init__(title, width, height)
        self.combobox_var = ctk.StringVar(value="2x")
        self.file = file
    
    def main_surface(self, release):
        self.combobox = ctk.CTkComboBox(self, values=["-3x", "-2x", "2x", "3x"], width=80, variable=self.combobox_var, state="readonly")
        self.but1 = ctk.CTkButton(self, text="Done", width=60, command=lambda: self.save_file(release))
        self.combobox.place(relx=0.5, rely=0.20, anchor=ctk.CENTER)
        self.but1.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
    
    def save_file(self, release):
        path = os.path.join("temp", f"{get_time()}.jpg")
        try:
            if len(path) != 0 and self.combobox_var.get() == "2x":
                self.resize_img(path, 2, True)
            elif len(path) != 0 and self.combobox_var.get() == "3x":
                self.resize_img(path, 3, True)
            elif len(path) != 0 and self.combobox_var.get() == "-2x":
                self.resize_img(path, 2, False)
            elif len(path) != 0 and self.combobox_var.get() == "-3x":
                self.resize_img(path, 3, False)
        except:
            ctkmb.showerror(title="图片缩放", message="图片缩放出错,请重试")
        finally:
            self.destroy()
            release(True, path)
            del self
    
    def resize_img(self, path, size, zoom):
        img = Image.open(self.file)
        if zoom:
            img_resize = (int(img.size[0] * size), int(img.size[1] * size))
        else:
            img_resize = (int(img.size[0] / size), int(img.size[1] / size))
        img = img.convert("RGB")
        image=img.resize(img_resize)
        image.save(path, quality=95)
        ctkmb. showinfo(title="图片缩放", message="完毕")
    
    def release_win(self, release):
        self.destroy()
        release(False, None)
        del self

    def run(self, release):
        self.protocol("WM_DELETE_WINDOW", lambda: self.release_win(release))
        self.main_surface(release)
        self.mainloop()

class Blur_img_win(compression_img_win):
    def __init__(self, title: str, width: int, height: int, file: str):
        super().__init__(title, width, height, file)
        self.defaultvar = ctk.IntVar(value=15)
        self.var = ctk.StringVar(value="15")
    
    def save_file(self, release):
        path = os.path.join("temp", f"{get_time()}.jpg")
        try:
            if len(path) != 0:
                img = Image.open(self.file)
                img = img.convert("RGB")
                gaussimg = img.filter(ImageFilter.GaussianBlur(int(self.var.get())))
                gaussimg.save(path, quality=95)
                ctkmb. showinfo(title="模糊处理", message="完毕")
                self.destroy()
                release(True, path)
                del self
        except:
            ctkmb.showerror(title="模糊处理", message="图片模糊出错,请重试")

class Rotate_img_win(Zoom_img_win):
    def __init__(self, title: str, width: int, height: int, file: str):
        super().__init__(title, width, height, file)
        self.combobox_var = ctk.StringVar(value="HORIZONTAL")
    
    def main_surface(self, release):
        self.combobox = ctk.CTkComboBox(self, values=["HORIZONTAL", "VERTICAL"], width=80, variable=self.combobox_var, state="readonly")
        self.but1 = ctk.CTkButton(self, text="Done", width=60, command=lambda: self.save_file(release))
        self.combobox.place(relx=0.5, rely=0.20, anchor=ctk.CENTER)
        self.but1.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
    
    def save_file(self, release):
        path = os.path.join("temp", f"{get_time()}.jpg")
        try:
            if len(path) != 0 and self.combobox_var.get() == "HORIZONTAL":
                self.rotate_img(path, True)
            elif len(path) != 0 and self.combobox_var.get() == "VERTICAL":
                self.rotate_img(path, False)
        except:
            ctkmb.showerror(title="图片翻转", message="图片翻转出错,请重试")
        finally:
            self.destroy()
            release(True, path)
            del self
    
    def rotate_img(self, path, direction):
        img = Image.open(self.file)
        img = img.convert("RGB")
        if direction == True:
            img.transpose(Image.FLIP_LEFT_RIGHT).save(path, quality=95)
        else:
            img.transpose(Image.FLIP_TOP_BOTTOM).save(path, quality=95)
        ctkmb.showinfo(title="图片翻转", message="完毕")