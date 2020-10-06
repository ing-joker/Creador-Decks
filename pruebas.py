from PIL import Image, ImageSequence
import os
import cv2
import sqlite3
import re,base64
#size=(421,641)

def  consulta(query, parameters=()):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

size = (55,80)  
db='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/database2 - copia.db'
directorio= 'C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas2'
lista = os.listdir(directorio)
#img=Image.open('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/ss/Chica Maga Oscura.png')
#img.thumbnail(size)
#img.save('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/'+ 'x4.png', "JPEG")

for i in lista:
    try:
    
        img=Image.open(directorio +'/'+ i)
        img.thumbnail(img.size)
        img.save('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas3/'+ i, "JPEG")
    except:
        x=cv.imread(directorio + '/' +i)
        cv.imwrite('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/' + i,x)
        print(i)
        pass


         #carga de imágenes a base de datos
'''         
for i in lista:
    f=open('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas3/'+ i,"rb")
    img=base64.encodestring(f.read())
    #print(img)
    query = 'INSERT INTO lista VALUES(NULL, ?,?)'
    parameters=(img,i)
    consulta(query,parameters)'''

 
         #uso de imágen desde base de datos en tkinter
'''
query = 'SELECT * FROM lista WHERE contenido = ?'
parameters='Agujero_de_Cadena.png'
db_columnas=consulta(query,(parameters,))
xd=db_columnas.fetchone()
pimg=cv2.imshow(data=xd[1])    #tk.PhotoImage(data=xd[1])
#imagenn= tk.PhotoImage(data=xd[1] )'''


'''
i='flecha.png'
image2 = Image.open(directorio + '/' + i)
image2.thumbnail([30,30], Image.ANTIALIAS)
image2.save('cartas2/' + i)'''
'''
import tkinter as tk
from tkinter import ttk
from random import choice




colors = ["red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown"]
def recolor():
    print(tree.get_children())
    for child in tree.get_children():
        picked = choice(colors)
        tree.item(child, tags=(picked), values=(picked))
    for color in colors:
        tree.tag_configure(color, background=color)
    tree.tag_configure("red", background="red")


root = tk.Tk()

tree=ttk.Treeview(root)


tree["columns"]=("one","two","three")
tree.column("#0", width=60, minwidth=30, stretch=tk.NO)
tree.column("one", width=120, minwidth=30, stretch=tk.NO)

tree.heading("#0",text="0",anchor=tk.W)
tree.heading("one", text="1",anchor=tk.W)
style = ttk.Style()
# this is set background and foreground of the treeview
style.configure("Treeview",
                background="#E1E1E1",
                foreground="#000000",
                rowheight=25,
                fieldbackground="#E1E1E1")

# set backgound and foreground color when selected
style.map('Treeview', background=[('selected', '#BFBFBF')], foreground=[('selected', 'black')])
for i in range(10):
    tree.insert("", i, text="Elem"+str(i), values=("none"),tags=("red"))
    tree.tag_configure("red", background="red",foreground="white")

tree.pack(side=tk.TOP,fill=tk.X)


b = tk.Button(root, text="Change", command=recolor)
b.pack()


root.mainloop()'''

'''
import threading
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
def download_file_worker():
    url = "https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe"
    filename = "python-3.7.2.exe"
    # Abrir la dirección de URL.
    with urlopen(url) as r:
        with open(filename, "wb") as f:
            # Leer el archivo remoto y escribir el fichero local.
            f.write(r.read())
        
def schedule_check(t):
    """
    Programar la ejecución de la función `check_if_done()` dentro de 
    un segundo.
    """
    root.after(1000, check_if_done, t)
def check_if_done(t):
    # Si el hilo ha finalizado, restaruar el botón y mostrar un mensaje.
    if not t.is_alive():
        info_label["text"] = "¡El archivo se ha descargado!"
        # Restablecer el botón.
        download_button["state"] = "normal"
    else:
        # Si no, volver a chequear en unos momentos.
        schedule_check(t)
def download_file():
    info_label["text"] = "Descargando archivo..."
    # Deshabilitar el botón mientras se descarga el archivo.
    download_button["state"] = "disabled"
    # Iniciar la descarga en un nuevo hilo.
    t = threading.Thread(target=download_file_worker)
    t.start()
    # Comenzar a chequear periódicamente si el hilo ha finalizado.
    schedule_check(t)
def cambio():
    if bt2["text"]=="prueba":
        bt2["text"]="test"
    else:
        bt2["text"]="prueba"
root = tk.Tk()
root.title("Descargar archivo con Tcl/Tk")
info_label = ttk.Label(text="Presione el botón para descargar el archivo.")
info_label.pack()
download_button = ttk.Button(text="Descargar archivo", command=download_file)
download_button.pack()
bt2=ttk.Button(text="prueba",command=cambio)
bt2.pack()
root.mainloop()'''