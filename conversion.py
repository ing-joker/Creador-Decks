from PIL import Image, ImageSequence
import os

size= (2705*0.3 , 4384*0.3)

def tifthumb(tifname):
    try:
        filename,extension = os.path.splitext(tifname)
        if extension==".tiff" or extension==".tif":
            tmbname=filename + ".tmb.jpg"
            img=Image.open(tifname)
            for i, page in enumerate(ImageSequence.Iterator(img)):
                page.thumbnail(size)
                page.save(tmbname)
                break
    except IOError:
        print(" cannot convert ", filename)

def imgthumb(imgname):
    try:
        filename,extension = os.path.splitext(imgname)
        if extension==".tiff" or extension==".tif":
            tifthumb(imgname)
        else:
            tmbname=filename + ".tmb.jpg"
            img=Image.open(imgname)

            img.thumbnail(size)
            img.save(tmbname, "JPEG")
                
    except IOError:
        print(" cannot create thumbnail for ", imgname)

imgthumb('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/image33.png')
#imgthumb()