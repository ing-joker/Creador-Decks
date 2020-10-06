import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter.font import Font
#from PIL import Image,ImageTk
import sqlite3
import threading
import crea_imagen_completa as ci

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey',width=10,relief='solid',font=None):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self["width"]=width
        self.put_placeholder()
        self["relief"]=relief
        self["font"]=font
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()



class APP(tk.Frame):
    db='database2.db'
    arra_no_imag=[False]*37    
    posiciones=([[0,1,2,3,4,30],[5,6,7,8,9,31],[10,11,12,13,14,32],[15,16,17,18,19,33],[20,21,22,23,24,34],[25,26,27,28,29,35],[-1,-1,-1,-1,-1,36]])
    btns=[None]*37
    color_fondo_main='#060b17' #"#112b0e"
    color_fondo_extra='#2b0226' #"#630250"
    imagenes_main=[None]*37
    cont=0
    cont_copias=0
    con_extra=0
    con_todo=0
    copias_cartas=([[None]*37,[None]*37])
    limitaciones=[0,0,0]
    solo_nombre=["zz"]*37
    variable_tipo_c='Todas'
    variable_elemento='Todos'
    variable_rareza=''
    variable_nivel=''
    variable_tipo_m=''
    variable_limite=''
    orden='DESC'
    clave=''
    mames=True
    para_crear=[None]*37
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.init_ui()
           
    
    def init_ui(self):
        self.configure(bg='#c0c0c0')
        '''
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        '''
        font=Font(family='Arial',size=16)
        font.metrics()
        font2=Font(family='Lucida Fax', size=12)
        font2.metrics()

        self.funt=Font(family='Arial',size=26)
        self.funt.metrics()

        ###########         IMÁGENES    IMÁGENES    IMÁGENES    IMÁGENES    IMÁGENES    IMÁGENES    IMÁGENES    ########
        self.otraimage = tk.PhotoImage(file="fuentes/fondov.png" )
        self.otraimage2 = tk.PhotoImage(file="fuentes/fondom.png" )
        
        #self.image = tk.PhotoImage(file="fuentes/alv.png" )
        self.flechas = tk.PhotoImage(file = "fuentes/flecha.png")
        self.sahcelf = tk.PhotoImage(file = "fuentes/ahcelf.png")
        self.search = tk.PhotoImage(file = "fuentes/search.png")

        ############ ÁRBOL   ÁRBOL   ÁRBOL   ÁRBOL   ÁRBOL   ÁRBOL   ÁRBOL   #############

        style = ttk.Style()
        style.configure(".", font=('Lucida Fax', 8), foreground="black")
        style.configure("Treeview.Heading", foreground='blue',font=('Lucida Fax', 14))
        style.configure('Treeview' , rowheight=80 , font=font)

        self.mostrador = ttk.Treeview(self,height = 7,columns=("size", "lastmod"), style="mystyle.Treeview")
        self.mostrador.grid(row = 5, column = 0, columnspan = 5, rowspan=30,sticky="NSEW")
        
        self.mostrador.heading('#0', text = '', anchor = 'center')
        self.mostrador.column("#0",width=70, anchor = 'center')
        self.mostrador.heading('#1', text = 'Nombre', anchor = 'center')
        self.mostrador.column("#1",width=400, anchor = 'center')
        self.mostrador.heading('lastmod', text = 'Rareza', anchor = 'center')
        self.mostrador.column("lastmod",width=100, anchor = 'center')
        style = ttk.Style()
        # this is set background and foreground of the treeview
        style.configure("Treeview",background="#E1E1E1",foreground="#000000",fieldbackground="#E1E1E1")

        # set backgound and foreground color when selected
        style.map('Treeview', background=[('selected', '#0000f0')], foreground=[('selected', 'white')])
        self.mostrador.bind("<Button-3>", self.popup)
        self.mostrador.bind('<<TreeviewSelect>>' and '<Button-1>', self.fnStockClick)
        vsb = ttk.Scrollbar(self,orient="vertical",   command=self.mostrador.yview)
        self.mostrador.configure(yscrollcommand=vsb.set)#, xscrollcommand=hsb.set)
        vsb.grid(column=5, row=5,rowspan=30, sticky='ns')

        self.aMenu = tk.Menu(self, tearoff=0)
        self.aMenu.add_command(label='Agregar', command=self.fnStockClick)
        self.aMenu.add_command(label='Ver', command=self.ver_carta)

        ###########         LABELFRAMES   LABELFRAMES   LABELFRAMES   LABELFRAMES   LABELFRAMES   LABELFRAMES   #######

        self.label=tk.LabelFrame(self,text="MAIN DECK",foreground="white" ,height=600 ,bg=self.color_fondo_main , width=400 , font=("Courier" ,18))
        self.label.grid( row=5 , column=7 ,rowspan=30, sticky="NSEW",columnspan=4)
        self.label2=tk.LabelFrame(self,text="EXTRA" ,foreground="white", height=600 ,bg=self.color_fondo_extra , width=100 ,font=("Courier" ,18))
        self.label2.grid(row=5 , column=11 ,rowspan=30, sticky="NSEW")

        ###########         LABELS    LABELS    LABELS    LABELS    LABELS    LABELS    LABELS    ##################
        self.letrero_tipo=ttk.Label(self, text='Tipo de Carta',font=font2,background='#093992',foreground='white',anchor = 'center')
        self.letrero_tipo.grid(row=4,column=0,sticky="NSEW")

        self.letrero_limite=ttk.Label(self,text='Limitación:',font=font2,background='#093992',foreground='white',anchor = 'center',width=12)
        self.letrero_limite.grid(row=4,column=2,sticky="NSEW")

        self.letrero_busqueda=ttk.Label(self, text='Búsqueda:              ',font=font2,background='#093992',foreground='white',anchor = 'center',relief='solid')
        self.letrero_busqueda.grid(row=3,column=0,sticky="NSW", pady=(0,2),columnspan=2,ipadx=25)

        self.letrero_habilidad=ttk.Label(self, text='Habilidad:',font=font2,background='#093992',foreground='white',anchor = 'center')
        self.letrero_habilidad.grid(row=3,column=7,rowspan=2,sticky="W",ipady=8)

        self.letrero_rareza=ttk.Label(self, text='Rareza',font=font2,background='#093992',foreground='white',anchor = 'center',width=9)
        self.letrero_rareza.grid(row=3,column=2,sticky="NSEW",pady=(0,2),padx=(25,0))

        self.letrero_tipo_m=ttk.Label(self, text='Tipo',font=font2,background='#093992',foreground='white',anchor = 'center',width=4)
        self.letrero_tipo_m.grid(row=8,column=6,sticky='EW')
                
        self.letrero_nivel=ttk.Label(self, text='Nivel',font=font2,background='#093992',foreground='white',anchor = 'center',width=5)
        self.letrero_nivel.grid(row=10,column=6,sticky='EW')
                
        self.letrero_atributo=ttk.Label(self, text='Atributo',font=font2,background='#093992',foreground='white',anchor = 'center')
        self.letrero_atributo.grid(row=6,column=6,sticky='EW')
        
        ############        MENÚS    MENÚS    MENÚS    MENÚS    MENÚS    MENÚS    MENÚS    MENÚS    ##################
        self.ns=ttk.Combobox(self,values=['Todas','Monstruos','Trampas','Mágicas','Sincros','Fusión','Xyz'] , state="readonly",width=10, font=font2,justify = 'center')
        self.ns.current(0)
        self.ns.grid(column=1,row=4,sticky="NSEW")
        self.ns.bind("<<ComboboxSelected>>",self.filtro_principal)
        
        self.ns2=ttk.Combobox(self,values=['Todos','Agua','Fuego','Viento','Tierra','Luz','Oscuridad','Divinidad'] , state="readonly",width=12, font=font2,justify = 'center')
        self.ns2.current(0)
        self.ns2.grid(column=6,row=7,sticky="EW")
        self.ns2.bind("<<ComboboxSelected>>",self.filtro_elemento)

        self.option_add('*TCombobox*Listbox.font',font2)
        self.habilidad=ttk.Combobox(self,values=['','Acceso Denegado','¡Adelante!','¡Adelante Goyo!','Adivinación del Futuro','Adivinación Iluminada','Adivinación Potenciada','Adivinador','¡ADN de Dinosaurio!','Afinación','Afinación de Nivel','Afinación Oscura 100','Al Borde de la Derrota','Alto Rendimiento','Alzamiento Alanegra','Amar Duelo','Amenaza de Profundidades','Amigos y Enemigos','Animación de las Hadas','Arremetida Psíquica','As en la Manga','Aterrador Como la Oscuridad','ATK= Pulso de 8800','Atraído por la Oscuridad','¡Aún no he Terminado!','Aumento de Contador Mágico','Aumento de Nivel','Aumento de Vida Alpha','Aumento de Vida Betha','Aumento de Vida Gamma','Aumento de Vida Omega','Aumento de Vida Delta','Cambios','Carga de Defensa','Carga de Vida','Ciberestilo','Comienzo Fuerte','Compensación','¡Conoce a mi Familia!','Constructor del Laberinto','Con Valor','Cristales Trascendentes','Duplicar Nivel','Equilibrio','Especialista en Magia','Evolución Alternativa','¡Fíjate en mi Vehículo!','¡Fíjate en mi Fusión!','¡Fusión Milagrosa!','Flash Hero!!','Fundas Profundas','¡Guardia Neos!','¡Hasta Pronto!','¡Hora de una Fusión!','Infierno de Trampas','Infierno Inférnico','Juego de las Sombras','Lanzaconjuros','¡Llega Zorc!','Maestro de Fusión','Maestro de Magos','Maestro del Destino','Nacido en el Cementerio','¡Neo Espacio!','Ningún Mortal se Resiste','¡No Tienes Nada que Hacer!','Obra de Titanes','Paliza','¡Ojamataque!','Poder de la Oscuridad','P. de ATK=Guerreros S.','¡Preparados y a Luchar!','Profundidades Míticas','¡Quedas Detenido!','Reacción en Cadena','Reducción de Nivel','Reiniciar','¡Respeta mi Autoridad!','Robar Sentido= Agua','Robar Sentido= Fuego','Robar Sentido= Luz','Robar Sentido= Nivel Alto','Robar Sentido= Nivel Bajo','Robar Sentido= Oscuridad','Robar Sentido= Tierra','Robar Sentido= Viento','Robo del Destino','Sacar o Destino','Show de Pesadillas','¡Sin Excusas!','Territorio de las Arpías','¡Toma un Poco de Combustible de Duelo!','Tumbas Selladas','¡Un Nuevo Poder!','¡Una Gran Sonrisa','¡Unión Elemental!','¡Vamos Ruleta Temporal','¡Ve Dragón Gema','Vinculaciones','¡Yo También Quiero Luchar!'] , state="readonly",width=23, font=font2,justify = 'center')
        self.habilidad.current(0)
        self.habilidad.grid(column=7,row=3,columnspan=4,rowspan=2,sticky="E",ipady=8)

        self.rarezas=ttk.Combobox(self,values=['','UR','SR','R','N'],state="readonly",width=4, font=font2,justify = 'center')
        self.rarezas.current(0)
        self.rarezas.grid(row=3,column=3,pady=(0,2),sticky="NSW")
        self.rarezas.bind("<<ComboboxSelected>>",self.filtro_rareza)

        self.tipo_m=ttk.Combobox(self,values=['','Aqua','Bestia','Bestia Alada','Ciberso','Demonio','Dinosaurio','Dragón','Guerrero','Guerrero-Bestia','Hada','Insecto','Lanzador de Conjuros','Máquina','Pez','Piro','Planta','Psíquico','Reptil','Roca','Serpiente Marina','Trueno','Zombi'],state="readonly",width=12, font=font2,justify = 'center')
        self.tipo_m.grid(row=9,column=6,sticky="EW")
        self.tipo_m.current(0)
        self.tipo_m.bind("<<ComboboxSelected>>",self.filtro_tipo_m)

        self.nivel=ttk.Combobox(self,values=['','1','2','3','4','5','6','7','8','9','10','11','12'],state="readonly",width=2, font=font2,justify = 'center')
        self.nivel.grid(row=11,column=6,sticky="EW")
        self.nivel.current(0)
        self.nivel.bind("<<ComboboxSelected>>",self.filtro_nivel)

        self.limites=ttk.Combobox(self, values=['','3','2','1','P'],state="readonly",width=4, font=font2,justify = 'center')
        self.limites.current(0)
        self.limites.grid(column=3,row=4,sticky="WNS")
        self.limites.bind("<<ComboboxSelected>>",self.filtro_limitacion)

##########          BOTONES    BOTONES    BOTONES    BOTONES    BOTONES    BOTONES    BOTONES    ###############
        self.b = tk.Button(self, text="Hello, world",  compound="bottom", command=self.impresiones, height=1,  width=8)
        #self.b["bg"] = '#c0c0c0'
        #self.b["border"] = "0"
        self.b.grid(row=4,column=6)

        self.sentido=tk.Button(self , image=self.flechas, command=self.cambiar_sentido, height=25, width=25,cursor='hand2')
        self.sentido.grid(row=3,column=4,columnspan=2,rowspan=2)
        
        self.btn_buscar=tk.Button(self, image=self.search, height=30, width=30,command=self.iniciar_busqueda,cursor='hand2')
        self.btn_buscar.grid(row=3,column=2,sticky='W')

        self.btn_crear_imagen=tk.Button(self,text='Crear Imagen...', height=1,command=self.crear_imagen,font=font2,relief='solid',overrelief='solid',cursor='hand2',bg='#76d24f')
        self.btn_crear_imagen.grid(row=13,column=6,sticky="NSEW",rowspan=2,padx=(5,5))#r3,c7,cs4ss'NSEW'

        self.btn_reiniciar=tk.Button(self, text='Reset',height=1,command=self.reiniciar_cartas ,font=font2,relief='solid',overrelief='solid',cursor='hand2',bg='#ef3236')
        self.btn_reiniciar.grid(row=3,column=11,rowspan=2)
 ########        OTROS    OTROS    OTROS    OTROS    OTROS    OTROS    OTROS    OTROS    ##########
        self.text_buscar=EntryWithPlaceholder(self, "Buscar...",width=15,font=font2)
        self.text_buscar.grid(row=3,column=1,sticky="NSEW",padx=(7,0),pady=(0,2))
        self.text_buscar.bind("<Return>", self.iniciar_busqueda)


        self.colocar_cartas(main=True,extra=True)
        root.bind("<Button-1>", self.click)
        self.obtener_cartas()

# MÉTODOS
    def filtro_limitacion(self,event):
        mos=self.limites.get()
        if mos!=self.variable_limite:
            self.variable_limite=mos
            self.obtener_cartas()

    def filtro_nivel(self, event):
        mos=self.nivel.get()
        if mos!=self.variable_nivel:
            if self.variable_tipo_c=='Xyz' and mos!='':
                self.variable_nivel=int(mos)*(-1)
            else:
                self.variable_nivel=mos
            
            self.obtener_cartas()

    def filtro_tipo_m(self,event):
        mos=self.tipo_m.get()
        if mos!=self.variable_tipo_m:
            self.variable_tipo_m=mos
            self.obtener_cartas()

    def reiniciar_cartas(self):
        if self.cont>0 or self.con_extra>0:
            self.solo_nombre.clear()
            self.solo_nombre=["zz"]*37
            self.arra_no_imag.clear()
            self.arra_no_imag=[False]*37
            self.copias_cartas.clear()
            self.copias_cartas=([[None]*37,[None]*37])
            self.limitaciones=[0,0,0]
            self.imagenes_main.clear()
            self.imagenes_main=[None]*37
            self.cont=0
            self.cont_copias=0
            self.con_extra=0
            self.con_todo=0
            self.colocar_cartas(main=True,extra=True)

    def iniciar_busqueda(self,event=None):
        self.clave=self.text_buscar.get()
        self.obtener_cartas()

    def cambiar_sentido(self):
        if self.orden=='DESC':
            self.sentido["image"]=self.sahcelf
            self.orden='ASC'
        elif self.orden=='ASC':
            self.sentido["image"]=self.flechas
            self.orden='DESC'
        self.mostrador.grid_remove()
        self.mostrador2 = ttk.Treeview(self,height = 7,columns=("size", "lastmod"), style="mystyle.Treeview")
        self.mostrador2.grid(row = 5, column = 0, columnspan = 5, rowspan=30,sticky="NSEW")
        self.mostrador2.heading('#0', text = '', anchor = 'center')
        self.mostrador2.column("#0",width=70, anchor = 'center')
        self.mostrador2.heading('#1', text = 'Nombre', anchor = 'center')
        self.mostrador2.column("#1",width=400, anchor = 'center')
        self.mostrador2.heading('lastmod', text = 'Rareza', anchor = 'center')
        self.mostrador2.column("lastmod",width=100, anchor = 'center')  

        self.rarezas["state"]="disable"
        self.ns["state"]="disable"
        self.ns2["state"]="disable"
        self.limites["state"]="disable"
        self.nivel["state"]="disable"
        self.tipo_m["state"]="disable"

        self.btn_buscar["state"]="disable"
        self.sentido["state"]="disable"
        self.text_buscar["state"]="disable"
        self.btn_crear_imagen["state"]="disable"
        self.btn_reiniciar["state"]="disable"

        t = threading.Thread(target=self.obtener_cartas)
        t.start()
        # Comenzar a chequear periódicamente si el hilo ha finalizado.
        self.schedule_check(t)

    def schedule_check(self,t):
        root.after(100, self.check_if_done, t)

    def check_if_done(self,t):
        # Si el hilo ha finalizado, restaruar el botón y mostrar un mensaje.
        if not t.is_alive():
            self.mostrador2.grid_remove()
            self.mostrador.grid(row = 5, column = 0, columnspan = 5, rowspan=30,sticky="NSEW")
            self.ns["state"]="readonly"
            self.ns2["state"]="readonly"
            self.limites["state"]="readonly"
            self.rarezas["state"]="readonly"
            self.nivel["state"]="readonly"
            self.tipo_m["state"]="readonly"

            self.btn_buscar["state"]="normal"
            self.sentido["state"]="normal"
            self.btn_reiniciar["state"]="normal"
            self.btn_crear_imagen["state"]="normal"
            self.text_buscar["state"]="normal"
            
        else:
            # Si no, volver a chequear en unos momentos.
            self.schedule_check(t)

    def ver_carta(self):
        item = self.mostrador.selection()[0]
        nombre_carta=self.mostrador.item(item,'text')
        query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
        db_columnas = self.consulta(query, (nombre_carta,))
        xd=db_columnas.fetchone()
        self.vista_imagen = tk.Toplevel()
        self.vista_imagen.resizable(0, 0)
        self.vista_imagen.title(xd[2])
        self.vista_imagen.geometry('421x614')
        self.vista_imagen.img=tk.PhotoImage(file='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas/'+ xd[8])
        img_a_mostrar=ttk.Label(self.vista_imagen,image=self.vista_imagen.img)#image=tk.PhotoImage(file='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas/'+ xd[8]))
        img_a_mostrar.pack()

    def popup(self, event):
            self.iid = self.mostrador.identify_row(event.y)
            if self.iid:
                # mouse pointer over item
                self.mostrador.selection_set(self.iid)
                self.aMenu.post(event.x_root, event.y_root)
            else:
                pass

    def filtro_elemento(self, event):
        mos=self.ns2.get()
        if mos !=self.variable_elemento:
            self.variable_elemento=mos
            if self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz' or self.variable_tipo_c=='Todas':
                self.obtener_cartas()

    def filtro_principal(self,event):
        mos=self.ns.get()
        if mos != self.variable_tipo_c:
            aux=(self.variable_nivel)
            if mos =='Xyz':
                self.letrero_nivel["text"]='Rango'
                if aux!='':
                    self.variable_nivel=int(aux)*(-1)
            else:
                self.letrero_nivel["text"]='Nivel'
                if aux!='' and int(self.variable_nivel)<0:
                    self.variable_nivel=int(aux)*(-1)
            if mos =='Mágicas' or mos=='Trampas':
                self.nivel.current(0)
                self.tipo_m.current(0)
                self.ns2.current(0)
                self.nivel['state']='disable'
                self.tipo_m['state']='disable'
                self.ns2['state']='disable'
                self.variable_nivel=''
                self.variable_tipo_m=''
                self.variable_elemento='Todos'
            else:
                self.nivel['state']='readonly'
                self.tipo_m['state']='readonly'
                self.ns2['state']='readonly'

            self.variable_tipo_c=mos
            self.obtener_cartas()

    def filtro_rareza(self,event):
        mos=self.rarezas.get()
        if mos!=self.variable_rareza:
            self.variable_rareza=mos
            self.obtener_cartas()

    def crear_imagen(self):
        h=0
        for i in range(36):
            if self.solo_nombre[i]!='zz':

                query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
                db_columnas = self.consulta(query, (self.solo_nombre[i],))
                xd=db_columnas.fetchone()
                self.para_crear[i]=xd[8]
                h+=1
        if h>0:
            ci.crear(v_cartas=self.para_crear[0:30],v_cartasx=self.para_crear[30:36],HD=False,skill=self.habilidad.get())
            self.para_crear.clear()
            self.para_crear=[None]*36

    def fnStockClick(self,event=None):
        try:
            self.mames=False
            if event!=None:
                self.iid = self.mostrador.identify_row(event.y)
            if self.iid:
                self.mostrador.selection_set(self.iid)
            else:
                pass
            item = self.mostrador.selection()[0]
            nombre_carta=self.mostrador.item(item,'text')
            query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
            db_columnas = self.consulta(query, (nombre_carta,))
            xd=db_columnas.fetchone()
            xd[1]
            if xd[1]=='Mágicas' or xd[1]=='Trampas' or xd[1]=='Monstruos':
                principal=True
            else:
                principal=False
            if xd[1]=='Sincros' or xd[1]=='Fusión' or xd[1]=='Xyz':
                secundario=True
            else:
                secundario=False
            hacer=False
            if principal and self.cont<30:

                self.con_todo=self.cont
                for xx in range(6):
                    for yy in range(5):
                        if self.posiciones[xx][yy]==self.cont:
                            hacer=True
                            ok=self.limitadas(xd)
                            break
            elif secundario and self.con_extra<7:
                self.con_todo=self.con_extra + 30
                hacer=True
                ok=self.limitadas(xd)
            try:
                if hacer and ok:
                    va=True
                    if principal:
                        for i in range (30):
                            if nombre_carta ==self.solo_nombre[i]:
                                aux=self.solo_nombre[30:37]                                
                                extension=self.solo_nombre[i:29]
                                inicio=self.solo_nombre[0:i]
                                inicio.append(nombre_carta)
                                inicio.extend(extension)
                                self.solo_nombre.clear()
                                self.solo_nombre[0:29]=inicio
                                self.solo_nombre[30:37]=aux
                                self.solo_nombre.clear()
                                inicio.extend(aux)
                                self.solo_nombre=inicio
                                va=False
                                
                                break
                    if secundario:
                        for i in range(30,37):
                            if nombre_carta ==self.solo_nombre[i]:
                                extension=self.solo_nombre[i:37]
                                inicio=self.solo_nombre[30:i]
                                inicio.append(nombre_carta)
                                inicio.extend(extension)
                                self.solo_nombre[30:37]=inicio
                                aux=self.solo_nombre[0:37]
                                self.solo_nombre.clear()
                                self.solo_nombre=aux
                                va=False
                                break

                    if va:
                        self.solo_nombre[self.con_todo]=nombre_carta
                        i=0
                    if secundario:
                        if va==False:
                            i-=30
                        self.colocar_cartas(extra=True,ie=(i+1),nt=True)
                        self.arra_no_imag[(self.con_extra +30)]=True
                        self.con_extra+=1
                    
                    if principal:
                        self.colocar_cartas(main=True,im=(i),nt=True)
                        self.arra_no_imag[self.cont]=True
                        self.cont+=1
                    no_esta=0
                    for i in range(37):
                        if nombre_carta == self.copias_cartas[0][i]:
                            self.copias_cartas[1][i]+=1
                        else:
                            no_esta+=1
                    if no_esta==37:
                        self.copias_cartas[0][self.cont_copias]=nombre_carta
                        self.copias_cartas[1][self.cont_copias]=1
                        self.cont_copias+=1
            except:
                pass
        except:
            pass

    def limitadas(self, nose):
        copias=nose[6]
        nombre=nose[2]

        for i in range(36):
            if nombre == self.copias_cartas[0][i]:
                if copias == 4:
                    if self.copias_cartas[1][i]<3:
                        ok=True
                    elif self.copias_cartas[1][i]==3:
                        ok=False
                elif copias !=4:
                    if copias == 1 and self.limitaciones[0] != 0:
                        ok=False
                    elif copias ==1 and self.limitaciones[0] ==0:
                        ok=True
                    elif copias ==2 and self.limitaciones[1] ==2:
                        ok=False
                    elif copias ==2 and self.limitaciones[1] <2:
                        self.limitaciones[1]+=1
                        ok=True
                    elif copias ==3 and self.limitaciones[2] ==3:
                        ok=False
                    elif copias ==3 and self.limitaciones[2] <3:
                        ok=True
                        self.limitaciones[2]+=1
                break
            elif nombre != self.copias_cartas[0][i]:
                if copias == 4:
                    ok=True
                elif copias !=4:
                    if copias == 1 and self.limitaciones[0] != 0:
                        ok=False
                    elif copias ==1 and self.limitaciones[0] ==0:
                        ok=True
                        self.limitaciones[0]+=1
                        break
                    elif copias ==2 and self.limitaciones[1] ==2:
                        ok=False
                    elif copias ==2 and self.limitaciones[1] <2:
                        ok=True
                        self.limitaciones[1]+=1
                        break
                    elif copias ==3 and self.limitaciones[2] ==3:
                        ok=False
                    elif copias ==3 and self.limitaciones[2] <3:
                        ok=True
                        self.limitaciones[2]+=1
                        break
        return(ok)

    def impresiones(self):
        #print("limitaciones: " + str(self.limitaciones))
        print("copias: " + str(self.copias_cartas[1][:]))
        print("Nombre: " + str(self.copias_cartas[0][:]))
        print("Solo nombres: " + str(self.solo_nombre))
        print( "True or False: " + str(self.arra_no_imag))
        print("Image main:" + str(self.imagenes_main))
        print("Limites: " + str(self.limitaciones))
        
    def ssgnar(self,z,z1):
        # con los datos recibidos se modifica la imagen del botón presionado y se del main o extra
        #print(z)
        #print(z1)
        try:
            if z[0]<1 or z[1]<0:
                btn_num=None
            elif z[0]>=1 and z[0]<=5 and z1[0]!=0:
                btn_num=self.posiciones[z[1]][z[0]-1]
            elif z1[0]==0 and z1[1]>=0 and z1[1]<=6 and z[0]==6:
                btn_num=z1[1]+30

            if z[0]>=0 and z[0]<6 and z1[0]==(-1):
                if self.arra_no_imag[btn_num]==False:
                    pass
                elif self.arra_no_imag[btn_num]==True:

                    self.cont-=1
                    for i in range(30):
                        if self.solo_nombre[btn_num]==self.copias_cartas[0][i]:
                            self.copias_cartas[1][i]-=1
                            query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
                            db_columnas = self.consulta(query, (self.solo_nombre[btn_num],))
                            xd=db_columnas.fetchone()
                            if xd[6]==3:
                                self.limitaciones[2]-=1
                            elif xd[6]==2:
                                self.limitaciones[1]-=1
                            elif xd[6]==1:
                                self.limitaciones[0]-=1
                            for k in range(btn_num,30):
                                
                                if k<29:
                                    self.solo_nombre[k]=self.solo_nombre[k+1]
                                    self.solo_nombre[k+1]="zz"
                                elif k==29:
                                    self.solo_nombre[k]="zz"
                                if self.solo_nombre[k]=="zz":
                                    break

                            if self.copias_cartas[1][i]==0:
                                self.cont_copias-=1
                                self.copias_cartas[0][i]=None
                            break
                    for i in range(37):
                        if self.copias_cartas[1][i]==0 or self.copias_cartas[1][i]==None:
                            if i<35:
                                self.copias_cartas[0][i]=self.copias_cartas[0][i+1]
                                self.copias_cartas[1][i]=self.copias_cartas[1][i+1]
                                self.copias_cartas[0][i+1]=None
                                self.copias_cartas[1][i+1]=None
                            elif i==35:
                                self.copias_cartas[0][i]=None
                                self.copias_cartas[1][i]=None

                    for i in range(btn_num,30):
                        if self.solo_nombre[i]=='zz':
                            self.arra_no_imag[i]=False
                    
                    self.colocar_cartas(main=True,im=btn_num,nt=True)

            if z[0]==6 and z1[0]==0:
                if self.arra_no_imag[btn_num]==False:
                    print("esta cosita 2")
                elif self.arra_no_imag[btn_num]==True:
                    self.con_extra-=1

                    for i in range(37):
                        if self.solo_nombre[btn_num]==self.copias_cartas[0][i]:
                            self.copias_cartas[1][i]-=1
                            query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
                            db_columnas = self.consulta(query, (self.copias_cartas[0][i],))
                            xd=db_columnas.fetchone()
                            if xd[6]==3:
                                self.limitaciones[2]-=1
                            elif xd[6]==2:
                                self.limitaciones[1]-=1
                            elif xd[6]==1:
                                self.limitaciones[0]-=1
                            for k in range(btn_num,37):
                                if k<36:
                                    self.solo_nombre[k]=self.solo_nombre[k+1]
                                    self.solo_nombre[k+1]="zz"
                                elif k==36:
                                    self.solo_nombre[k]="zz"
                                
                            if self.copias_cartas[1][i]==0:
                                self.cont_copias-=1
                                self.copias_cartas[0][i]=None
                            break
                    for i in range(37):
                        if self.copias_cartas[1][i]==0 or self.copias_cartas[1][i]==None:
                            
                            if i<36:
                                self.copias_cartas[0][i]=self.copias_cartas[0][i+1]
                                self.copias_cartas[1][i]=self.copias_cartas[1][i+1]
                                self.copias_cartas[0][i+1]=None
                                self.copias_cartas[1][i+1]=None
                            elif i==36:
                                self.copias_cartas[0][i]=None
                                self.copias_cartas[1][i]=None

                    
                    for i in range(btn_num,37):
                        if self.solo_nombre[i]=='zz':
                            self.arra_no_imag[i]=False
                    self.colocar_cartas(extra=True,ie=btn_num-29,nt=True)
        except:
            pass

    def colocar_cartas(self,main=False,extra=False,im=0,ie=1,nt=False):
        #asignación de cartas por orden
        #aux1=sorted(aux1)
        #aux2=self.solo_nombre[30:36]
        #aux2=sorted(aux2)
        #print("im: " + str(im)+" ie: " + str(ie))
        #print("ie: " + str(ie))
        
        if main:
            y=0
            z=0
            for xx in range(6):
                    for yy in range(5):
                        if self.posiciones[xx][yy]==im:
                            y=xx
                            z=yy
                            break

            for i in range(im,30):
                z=z+1
                if self.solo_nombre[i]!="zz":
                    query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
                    db_columnas = self.consulta(query, (self.solo_nombre[i],))
                    xd=db_columnas.fetchone()
                    imagen=tk.PhotoImage(file='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas2/'+ xd[8])
                elif self.solo_nombre[i]=="zz":
    
                    imagen=self.otraimage
                if self.mames:
                    self.btns[i]=tk.Button(self.label , activebackground=self.color_fondo_main,relief="flat",overrelief="flat",bg=self.color_fondo_main, text=(" "))#,image=imagen)
                    self.btns[i].grid(row=y , column=z ,padx=(5,0) , pady=(5,0),sticky="NSEW")
                self.btns[i]["image"]=imagen
                
                self.imagenes_main[i]=imagen
                if nt and self.solo_nombre[i]=="zz":
                    break
                if z==5:
                    y=y+1
                    z=0
        if extra:
            for j in range(ie,8):
                if self.solo_nombre[30+j-1]!="zz":
                    query = 'SELECT * FROM cartas WHERE nombre = ?' #ascedente ASC
                    db_columnas = self.consulta(query, (self.solo_nombre[30+j-1],))
                    xd=db_columnas.fetchone()
                    imagen=tk.PhotoImage(file='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas2/'+ xd[8])
                elif self.solo_nombre[30+j-1]=="zz":
                    imagen=self.otraimage2
                if self.mames:
                    self.btns[29+j]=tk.Button(self.label2 , activebackground=self.color_fondo_extra,relief="flat",overrelief="flat",bg=self.color_fondo_extra, text=(" "),height=70)#height=67
                    self.btns[29+j].grid(row=j-1 , column=0 ,padx=(5,0) , pady=(3,0),sticky="NSEW")
                self.btns[29+j]["image"]=imagen
                self.imagenes_main[j+29]=imagen
                if nt and self.solo_nombre[30+j-1]=="zz":
                    break

    def click(self,event): 
        # recibe la ubicación donde se realizó click izquierdo 
        # con ese dato se sabe que espacio se presionó para modeficarse
        x = event.x_root - self.label.winfo_rootx() 
        y = event.y_root - self.label.winfo_rooty() 
        z = self.label.grid_location(x, y)
        x1 = event.x_root - self.label2.winfo_rootx() 
        y1 = event.y_root - self.label2.winfo_rooty() 
        z1 = self.label2.grid_location(x1, y1)
        self.ssgnar(z,z1)

    def consulta(self,query, parameters=()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
        
    def obtener_cartas(self):
        # cleaning Table 
        records = self.mostrador.get_children()
        for element in records:
            self.mostrador.delete(element)
            # getting data

        #1 todas las cartas
        #2 magias y trampas
        #3 monstruos sin elemento
        #4 monstruos con elemento
        #5 todos los monstruos con elemento

        #con búsqueda específica pero sin rareza
        if self.clave!='' and self.variable_rareza=='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas' and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ?  ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',))
        #sin búsqueda específica pero sin rareza
        elif self.clave=='' and self.variable_rareza=='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query)
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,))
        # con búsqueda específica y con rareza
        elif self.clave!='' and self.variable_rareza!='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ? and rareza=? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_rareza,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ? and rareza=? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ? and rareza = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
        # sin búsqueda específica pero con de rareza
        elif self.clave=='' and self.variable_rareza!='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE rareza=? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_rareza,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and rareza=? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_rareza,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and rareza = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_rareza,))
        #### LIMITACIÓN
        if self.clave!='' and self.variable_rareza=='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas' and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ?  and limitacion = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_limite,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_limite,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_limite,))
        #sin búsqueda específica pero sin rareza
        elif self.clave=='' and self.variable_rareza=='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas  WHERE limitacion = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_limite,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_limite,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_limite,))
        # con búsqueda específica y con rareza
        elif self.clave!='' and self.variable_rareza!='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ? and rareza=?  and limitacion = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_rareza,self.variable_limite,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ? and rareza=?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ? and rareza = ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,))
        # sin búsqueda específica pero con de rareza
        elif self.clave=='' and self.variable_rareza!='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m=='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE rareza=?  and limitacion = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_rareza,self.variable_limite,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and limitacion = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_limite,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and rareza=?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_rareza,self.variable_limite,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and rareza = ?  and limitacion = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_rareza,self.variable_limite,))

        ### con tipo de monstruo

                #con búsqueda específica pero sin rareza
        if self.clave!='' and self.variable_rareza=='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas' and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ? and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_m,))
        #sin búsqueda específica pero sin rareza
        elif self.clave=='' and self.variable_rareza=='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas  WHERE pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_tipo_m,))
        # con búsqueda específica y con rareza
        elif self.clave!='' and self.variable_rareza!='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ? and rareza=?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_rareza,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ? and rareza=?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ? and rareza = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_m,))
        # sin búsqueda específica pero con de rareza
        elif self.clave=='' and self.variable_rareza!='' and self.variable_limite=='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE rareza=?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_rareza,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and rareza=?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_rareza,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and rareza = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_rareza,self.variable_tipo_m,))
        #### LIMITACIÓN
        if self.clave!='' and self.variable_rareza=='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas' and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ?  and limitacion = ?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_limite,self.variable_tipo_m,))
        #sin búsqueda específica pero sin rareza
        elif self.clave=='' and self.variable_rareza=='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas  WHERE limitacion = ?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_limite,self.variable_tipo_m,))
        # con búsqueda específica y con rareza
        elif self.clave!='' and self.variable_rareza!='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE nombre LIKE ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,('%'+self.clave+'%',self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and nombre LIKE ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and nombre LIKE ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and nombre LIKE ? and rareza = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
        # sin búsqueda específica pero con de rareza
        elif self.clave=='' and self.variable_rareza!='' and self.variable_limite!='' and self.variable_nivel=='' and self.variable_tipo_m!='':
            if self.variable_tipo_c=='Todas'and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY nombre '+ self.orden #ascedente ASC
                db_columnas = self.consulta(query,(self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Mágicas' or self.variable_tipo_c=='Trampas':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento=='Todos':
                query = 'SELECT * FROM cartas WHERE clase = ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo '+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif (self.variable_tipo_c=='Monstruos' or self.variable_tipo_c=='Sincros' or self.variable_tipo_c=='Fusión' or self.variable_tipo_c=='Xyz') and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE clase = ? and atributo = ? and rareza=?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_tipo_c,self.variable_elemento,self.variable_rareza,self.variable_limite,self.variable_tipo_m,))
            elif self.variable_tipo_c=='Todas' and self.variable_elemento!='Todos':
                query = "SELECT * FROM cartas WHERE atributo = ? and rareza = ?  and limitacion = ?  and pri_tipo = ? ORDER BY archivo "+ self.orden
                db_columnas = self.consulta(query,(self.variable_elemento,self.variable_rareza,self.variable_limite,self.variable_tipo_m,))

        ### con nivel o rango
        elif self.variable_nivel!='':
            if self.variable_tipo_m!='':
                if self.variable_limite!='':
                    if self.variable_elemento!='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and atributo = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_elemento,))
                    elif self.variable_elemento=='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and limitacion = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_limite,))
                elif self.variable_limite=='':
                    if self.variable_elemento!='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and atributo = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_elemento,))
                    elif self.variable_elemento=='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and pri_tipo = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_m,))
            elif self.variable_tipo_m=='':
                if self.variable_limite!='':
                    if self.variable_elemento!='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and atributo = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_elemento,))
                    elif self.variable_elemento=='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and limitacion = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_limite,))
                elif self.variable_limite=='':
                    if self.variable_elemento!='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and atributo = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_elemento,))
                    elif self.variable_elemento=='Todos':
                        if self.clave!='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and nombre LIKE ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,'%'+self.clave+'%',self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and nombre LIKE ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,'%'+self.clave+'%',self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and nombre LIKE ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,'%'+self.clave+'%',self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and nombre LIKE ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,'%'+self.clave+'%',))
                        elif self.clave=='':
                            if self.variable_rareza!='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and rareza = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_rareza,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and rareza = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_rareza,))
                            elif self.variable_rareza=='':
                                if self.variable_tipo_c!='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ? and clase = ? ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,self.variable_tipo_c,))
                                elif self.variable_tipo_c=='Todas':
                                    query = "SELECT * FROM cartas WHERE nivel = ?  ORDER BY archivo "+ self.orden
                                    db_columnas = self.consulta(query,(self.variable_nivel,))



        records=db_columnas.fetchall()
        i=0
        self.icon2=[None]*len(records)    
        
        for row in records:
            if i%2==0:
                tg='white'
            else:
                tg='#c0c0c0'
            self.icon2[i] = tk.PhotoImage(file='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas2/'+ row[8])
            self.mostrador.insert('', 0 , text = row[2], values =(row[2] , row[7]),image=self.icon2[i],tag=(tg))
            self.mostrador.tag_configure(tg, background=tg,foreground="black")
            i+=1

if __name__ == "__main__":
       root = tk.Tk()
       root.title("Creador de Mazo")
       root.geometry("1155x650")
       #root.option_add("*Background",'#c0c0c0')
       root.resizable(0, 0)# impedir cambio de tamaño
       view = APP(root)
       view.pack(side="top", fill="both", expand=True)
       root.mainloop()