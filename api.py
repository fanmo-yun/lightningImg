import os, time
from PIL import Image

def remove_file(path: str):
    try:
        for dir, _, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(dir, file))
    except:
        pass

def check_path():
    path = os.path.join("temp")
    if not os.path.exists(path):
        os.mkdir(path)

def get_time():
    return int(round(time.time() * 1000))

def suit_img(path, canvas_w, canvas_h):
    img = Image.open(path)
    size1 = 1.0*canvas_w/img.size[0]
    size2 = 1.0*canvas_h/img.size[1]
    suitvar = min([size1, size2])
    w = int(img.size[0]*suitvar)
    h = int(img.size[1]*suitvar)
    return img.resize((w, h), Image.LANCZOS), suitvar