#Importacion de modulos:

import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime
import PyPDF2
from datetime import datetime, timedelta
import math
import random #uso del modulo random



#Variables de la aplicacion:

dic_configuracion = {"nivel": 0, "reloj":0, "posicion": 0, "hora": "", "minutos": "", "segundos": ""}

    
#Funcion para validar los datos ingresados en la ventana de configuracion
#Entradas: campos de entrada de la ventana configuracion
#Salidas: None, en caso correcto o de lo contrario se presenta el mensaje de error
def validaEntradasVentanaConfiguracion(ventanaConfig,CheckNivel, CheckHoras, CheckPosicion,txtHora,txtMinutos,txtSegundos):
    if CheckHoras.get() == 2:
        try:
            hora = int(txtHora.get())
            if hora < 0 or hora > 2:
                messagebox.showerror(parent=ventanaConfig,title="Error", message="Las horas deben estar entre 0 y 2")
                return

            minutos = int(txtMinutos.get())
            if minutos < 0 or minutos > 59:
                messagebox.showerror(parent=ventanaConfig,title="Error", message="Los minutos deben estar entre 0 y 59")
                return

            segundos = int(txtSegundos.get())
            if segundos < 0 or segundos > 59:
                messagebox.showerror(parent=ventanaConfig,title="Error", message="Los segundos deben estar entre 0 y 59")
                return
        except:
            messagebox.showerror(parent=ventanaConfig,title="Error", message="Debe ingresar valores válidos para el timer")
            return

    #se guardan los datos
    guardaDatosConfiguracion(CheckNivel, CheckHoras, CheckPosicion,txtHora,txtMinutos,txtSegundos)
    messagebox.showinfo(parent=ventanaConfig,title="Mensaje", message="Datos de configuración guardados")
    ventanaConfig.destroy()

    
#Funcion para guardar los datos de las variables de configuracion en el archivo correspondiente
#Entradas: variables de la pantalla de configuracion
#Salidas: ninguna   
def guardaDatosConfiguracion(CheckNivel, CheckHoras, CheckPosicion,txtHora,txtMinutos,txtSegundos):
    configuracion = {}
    configuracion["nivel"] = CheckNivel.get()
    configuracion["reloj"] = CheckHoras.get()
    configuracion["posicion"] = CheckPosicion.get()
    configuracion["hora"] = txtHora.get()
    configuracion["minutos"] = txtMinutos.get()
    configuracion["segundos"] = txtSegundos.get()
    
    #se guardan los datos de la configuracion en el archivo 
    f=open("futoshiki2021configuración.dat","wb")
    pickle.dump(configuracion,f)
    f.close()

    #se refresca el diccionario de la configuracion
    dic_configuracion = actualizar_dic_configuracion()
    print("despues",dic_configuracion)

def guardaPartidasArchivo():
    partidasFacil = list()
    partidasFacil = [((">", 0, 0), (">", 0, 2), (">", 0, 3), ("4", 1, 0), ("2", 1, 4), ("4", 2, 2), ("<", 3, 3), ("4", 3, 4), ("<", 4, 0), ("<", 4, 1))]

    partidasIntermedio = list()
    partidasIntermedio = []

    partidasDificil = list()
    partidasDificil = [((">", 0, 0), (">", 0, 2), (">", 0, 3), ("4", 1, 0), ("2", 1, 4), ("4", 2, 2), ("<", 3, 3), ("4", 3, 4), ("<", 4, 0), ("<", 4, 1))]
    
    #se guardan los datos de las partidas en el archivo
    f=open("futoshiki2021partidas.dat","wb")
    pickle.dump(partidasFacil,f)
    pickle.dump(partidasIntermedio,f)
    pickle.dump(partidasDificil,f)
    f.close()
    
                                                                                                                                                                           
#Funcion para realizar la lectura de los distintos archivos y cargar la informacion en las listas y diccionarios
#Entradas: listas y diccionarios a cargar
#Salidas: se retornan dichas listas y diccionarios con la informacion cargada 
def cargarDatosConfiguracion():
    dic_temp = {}
    f=open("futoshiki2021configuración.dat","rb")
    while True:
        try:
            dic_temp=pickle.load(f)
        except EOFError:
            break
    f.close()
    if len(dic_temp) != 0:
        return dic_temp
    return None

def actualizar_dic_configuracion():
    #print("metodo actualiza",dic_configuracion)
    temp = dic_configuracion
    resultado = cargarDatosConfiguracion()
    if resultado != None:
        return resultado
    return temp

def valida_controles_timer():
    return None
    
    

#VENTANA CONFIGURACION:
#Funcion que carga la ventana de configuracion asi como todos los componentes
#Entradas: ninguna
#Salidas: ninguna
def configuracion():
    dic_configuracion = actualizar_dic_configuracion()
    ventanaConfig = tk.Toplevel()
    ventanaConfig.title("FUTOSHIKI - CONFIGURACIÓN")
    ventanaConfig.geometry("800x600")
    lblTitulo = tk.Label(ventanaConfig, text="FUTOSHIKI - CONFIGURACIÓN")
    lblTitulo.grid(row=0,column=1,pady=10,padx=1)

    lblNivel = tk.Label(ventanaConfig,text="1. Nivel:",pady=10)
    lblNivel.grid(row=1,column=0)

    CheckNivel=tk.IntVar()
    
    rbFacil = tk.Radiobutton(ventanaConfig,text="Fácil",variable=CheckNivel,value=0,tristatevalue=0)
    rbIntermedio = tk.Radiobutton(ventanaConfig,text="Intermedio",variable=CheckNivel,value=1,tristatevalue=1)
    rbAvanzado = tk.Radiobutton(ventanaConfig,text="Avanzado",variable=CheckNivel,value=2,tristatevalue=2)

    CheckNivel.set(dic_configuracion["nivel"])    

    rbFacil.grid(row=1,column=1)
    rbIntermedio.grid(row=1,column=2)
    rbAvanzado.grid(row=1,column=3)


    lblHoras = tk.Label(ventanaConfig,text="2. Horas:",pady=10)
    lblHoras.grid(row=2,column=0)

    CheckHoras = tk.IntVar()
    
    rbHoraSi = tk.Radiobutton(ventanaConfig, text="Sí", variable = CheckHoras, value=0)
    rbHoraSi.grid(row=2,column=1)

    rbHorasNo = tk.Radiobutton(ventanaConfig, text = "No", variable = CheckHoras, value=1)
    rbHorasNo.grid(row=2,column=2)

    rbHorasTimer = tk.Radiobutton(ventanaConfig, text = "Timer", variable = CheckHoras, value=2)
    rbHorasTimer.grid(row=2,column=3)

    CheckHoras.set(dic_configuracion["reloj"])

    habilitado = 'disabled'
    if dic_configuracion["reloj"] != "":
        if dic_configuracion["reloj"] == 2:
            habilitado = 'normal'            

    lblHora = tk.Label(ventanaConfig,text="Horas:",pady=10)
    lblHora.grid(row=3,column=3)
    txtHora = tk.StringVar(value=dic_configuracion["hora"])
    entryHora  = tk.Entry(ventanaConfig,textvariable=txtHora,state=habilitado)
    entryHora.grid(row=3,column=4)

    lblMinutos = tk.Label(ventanaConfig,text="Minutos:",pady=10)
    lblMinutos.grid(row=3,column=5)
    txtMinutos = tk.StringVar(value=dic_configuracion["minutos"])
    entryMinutos  = tk.Entry(ventanaConfig,textvariable=txtMinutos,state=habilitado)
    entryMinutos.grid(row=3,column=6)

    lblSegundos = tk.Label(ventanaConfig,text="Segundos:",pady=10)
    lblSegundos.grid(row=3,column=7)
    txtSegundos = tk.StringVar(value=dic_configuracion["segundos"])
    entrySegundos  = tk.Entry(ventanaConfig,textvariable=txtSegundos,state=habilitado)
    entrySegundos.grid(row=3,column=8)

    lblPosicion = tk.Label(ventanaConfig,text="3. Posición en la ventana del panel de dígitos:",pady=10)
    lblPosicion.grid(row=4,column=0)

    CheckPosicion = tk.IntVar()
    
    rbPosicionDerecha = tk.Radiobutton(ventanaConfig, text="Derecha", variable = CheckPosicion, value=0)
    rbPosicionDerecha.grid(row=4,column=1)

    rbPosicionIzquierda = tk.Radiobutton(ventanaConfig, text="Izquierda", variable = CheckPosicion, value=1)
    rbPosicionIzquierda.grid(row=4,column=2)

    CheckPosicion.set(dic_configuracion["posicion"])


    btnOk = tk.Button(ventanaConfig, text="   Ok   ", command=lambda:validaEntradasVentanaConfiguracion(ventanaConfig,CheckNivel,CheckHoras,CheckPosicion, \
                                                                                                        txtHora,txtMinutos,txtSegundos))
    btnOk.grid(row=8,column=0)

    btnCancelar = tk.Button(ventanaConfig, text="   Cancelar   ", command=ventanaConfig.destroy)
    btnCancelar.grid(row=8,column=1)

    ventanaConfig.mainloop()

def leer_partidas():
    partidasFacil = list()
    partidasIntermedio = list()
    partidasDificil = list()
    
    f=open("futoshiki2021partidas.dat","rb")
    while True:
        try:
            partidasFacil=pickle.load(f)
            partidasIntermedio=pickle.load(f)
            partidasDificil=pickle.load(f)
        except EOFError:
            break
    f.close()
    return partidasFacil,partidasIntermedio,partidasDificil

    

# lee el archivo de partidas
def obtener_partida(nivel):
    partidas = leer_partidas()
    if nivel == 0:
        cantidadPartidas = len(partidas[0])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[0][aleatorio]
    elif nivel == 1:
        cantidadPartidas = len(partidas[1])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[1][aleatorio]
    else:
        cantidadPartidas = len(partidas[2])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[2][aleatorio]
        
    

def agregar_digito(event,ventanaConfig,nueva_seleccion,num_seleccionado,n1,n2,n3,n4,n5):
    n1.configure(background = "SystemButtonFace")
    n2.configure(background = "SystemButtonFace")
    n3.configure(background = "SystemButtonFace")
    n4.configure(background = "SystemButtonFace")
    n5.configure(background = "SystemButtonFace")

    caller = event.widget

    if nueva_seleccion != num_seleccionado[0]:
        num_seleccionado[0] = nueva_seleccion
        
        caller.configure(background = "green")
    else:
        caller = event.widget
        caller.configure(background = "SystemButtonFace")
        num_seleccionado[0] = 0

def seleccion_tablero(event,num_seleccionado):
    caller = event.widget
    caller.configure(text = num_seleccionado[0])

def cargar_tablero(ventanaJuego,partida,num_seleccionado):
    listaBotones = []
    cont = 0
    fila = 3
    col = 0
    for i in range(5):
        col = 0
        for j in range(5):
            cont += 1
            btn = tk.Button(ventanaJuego,text="",compound="c",height=2,width=5)
            btn.grid(row=fila,column=col)
            btn.bind("<1>",lambda event:seleccion_tablero(event,num_seleccionado))          
            listaBotones += [ btn ] 
            #if j == 2:
            #    listaBotones += [ tk.Label(text=">")]
            #listaBotones[-1].grid(row=fila,column=col)
            col += 1
        fila += 1
    
    

def iniciar_juego(event,ventanaJuego,txtNombre,partida,num_seleccionado):
    if not txtNombre.get().isalpha():
        messagebox.showerror(parent=ventanaJuego,title="Error", message="DEBE INGRESAR UN NOMBRE VÁLIDO")
        return
    if partida == None:
        messagebox.showerror(parent=ventanaJuego,title="Error", message="NO HAY PARTIDAS PARA ESTE NIVEL")
        ventanaJuego.destroy()
        return

    # se carga la partida
    cargar_tablero(ventanaJuego,partida,num_seleccionado)
        

    # se deshabilita el boton
    caller = event.widget
    caller.configure(state = "disabled")
    
        


#VENTANA JUEGO:
#Funcion que carga la ventana de configuracion asi como todos los componentes
#Entradas: ninguna
#Salidas: ninguna
def juego():
    dic_configuracion = actualizar_dic_configuracion()
    partida = obtener_partida(dic_configuracion["nivel"]) # se obtiene la partida segun el nivel configurado por el usuario
    num_seleccionado = [0]
    
    lista_nivel = ["FÁCIL", "INTERMEDIO", "DIFÍCIL"]
    ventanaJuego = tk.Toplevel()
    ventanaJuego.title("FUTOSHIKI")
    ventanaJuego.geometry("800x600")
    lblTitulo = tk.Label(ventanaJuego, text="FUTOSHIKI")
    lblTitulo.grid(row=0,column=5)
    lblNivel = tk.Label(ventanaJuego, text="NIVEL" + " " + lista_nivel[dic_configuracion["nivel"]])
    lblNivel.grid(row=1,column=5)

    lblNombre = tk.Label(ventanaJuego, text="Nombre del jugador:")
    lblNombre.grid(row=2,column=50)
    txtNombre = tk.StringVar()
    entryNombre = tk.Entry(ventanaJuego,textvariable=txtNombre)
    entryNombre.grid(row=2,column=51)

    
    # CUADRICULA INICIAL
    listaBotones = []
    cont = 0
    fila = 3
    col = 0
    for i in range(5):
        col = 0
        for j in range(5):
            cont += 1
            btn = tk.Button(ventanaJuego,text="",compound="c",height=2,width=5,state="disabled")
            btn.grid(row=fila,column=col)
            #btn.bind("<1>",lambda event:seleccion_tablero(event,num_seleccionado))          
            listaBotones += [ btn ] 
            #if j == 2:
            #    listaBotones += [ tk.Label(text=">")]
            #listaBotones[-1].grid(row=fila,column=col)
            col += 1
        fila += 1
        
    n1 = tk.Button(ventanaJuego,text="1",compound="c",height=2,width=5)
    n1.grid(row=3,column=7)
    n2 = tk.Button(ventanaJuego,text="2",compound="c",height=2,width=5)
    n2.grid(row=4,column=7)
    n3 = tk.Button(ventanaJuego,text="3",compound="c",height=2,width=5)
    n3.grid(row=5,column=7)
    n4 = tk.Button(ventanaJuego,text="4",compound="c",height=2,width=5)
    n4.grid(row=6,column=7)
    n5 = tk.Button(ventanaJuego,text="5",compound="c",height=2,width=5)
    n5.grid(row=7,column=7)

    n1.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,1,num_seleccionado,n1,n2,n3,n4,n5))
    n2.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,2,num_seleccionado,n1,n2,n3,n4,n5))
    n3.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,3,num_seleccionado,n1,n2,n3,n4,n5))
    n4.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,4,num_seleccionado,n1,n2,n3,n4,n5))
    n5.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,5,num_seleccionado,n1,n2,n3,n4,n5))
    
    # Botones
    btnIniciar = tk.Button(ventanaJuego, text="INICIAR JUEGO", bg="red")
    btnIniciar.bind("<1>",lambda event:iniciar_juego(event,ventanaJuego,txtNombre,partida,num_seleccionado))
    btnIniciar.grid(row=8,column=0)

    btnBorrarJugada = tk.Button(ventanaJuego, text="BORRAR JUGADA", bg="cyan")
    btnBorrarJugada.grid(row=8,column=1)

    btnTerminarJuego = tk.Button(ventanaJuego, text="TERMINAR JUEGO", bg="green")
    btnTerminarJuego.grid(row=8,column=2)

    btnBorrarJuego = tk.Button(ventanaJuego, text="BORRAR JUEGO", bg="violet")
    btnBorrarJuego.grid(row=8,column=3)

    btnTop10 = tk.Button(ventanaJuego, text="TOP 10", bg="yellow")
    btnTop10.grid(row=8,column=4)

    # Guardar / Cargar
    btnGuardar = tk.Button(ventanaJuego, text="GUARDAR JUEGO")
    btnGuardar.grid(row=9,column=1)

    btnCargar = tk.Button(ventanaJuego, text="CARGAR JUEGO")
    btnCargar.grid(row=9,column=2)

    
    
    




#Funcion que carga la ventana de acerca de del programa
#Entradas: ninguna
#Salidas: ninguna
def acerca_de():
    ventanaAcercaDe = tk.Toplevel()
    ventanaAcercaDe.title("Futoshiki – ACERCA DE")
    ventanaAcercaDe.geometry("800x600")
    lblTitulo = tk.Label(ventanaAcercaDe, text="Juego de Futoshiki")
    lblTitulo.pack(pady=13,padx=8)
    lblVersion = tk.Label(ventanaAcercaDe, text="Versión: 1.0")
    lblVersion.pack(pady=13,padx=8)
    lblFecha = tk.Label(ventanaAcercaDe, text="Fecha de Creación: 09/06/2021")
    lblFecha.pack(pady=13,padx=8)
    lblAutor = tk.Label(ventanaAcercaDe, text="Autor: Cristofer Ulate Bolaños")
    lblAutor.pack(pady=13,padx=8)

#Funcion que carga la ventana de ayuda de del programa donde se imprime el manual de usuario
#Entradas: ninguna
#Salidas: ninguna
def ayuda():
    ventanaAyuda = tk.Toplevel()
    ventanaAyuda.title("FUTOSHIKI – AYUDA")
    ventanaAyuda.geometry("800x600")
    lblTitulo = tk.Label(ventanaAyuda, text="FUTOSHIKI - AYUDA")
    lblTitulo.grid(row=0,column=0,pady=13)

    entryAyuda = tk.Text(ventanaAyuda,height=40,width=80)
    entryAyuda.grid(row=1,column=0,padx=30)

    # Lectura delPDF:
    # se obtiene el archivo a leer
    pdf_archivo = open('manual_de_usuario_ parqueo.pdf', 'rb')
      
    # se crea una variable lectora
    lector_pdf = PyPDF2.PdfFileReader(pdf_archivo)

    texto = ""     
    for pagina in lector_pdf.pages:
        contenido = pagina.extractText()
        texto += contenido
      
    # se cierra la variable con la referencia al archivo
    pdf_archivo.close()

    entryAyuda.insert(1.0,texto)

        

    
#VENTANA PRINCIPAL:

#lectura de archivos
dic_configuracion = actualizar_dic_configuracion()

ventana = tk.Tk()
ventana.title("FUTOSHIKI")
ventana.geometry("800x600")
menubar = tk.Menu(ventana)
filemenu = tk.Menu(menubar,tearoff=0)
menubar.add_command(label="Configuración",command=configuracion)
menubar.add_command(label="Jugar",command=juego)

menubar.add_command(label="Ayuda",command=ayuda)
menubar.add_command(label="Acerca de",command=acerca_de)
ventana.config(menu=menubar)

lblBienvenido = tk.Label(ventana, text="Bienvenido al Juego de Futoshiki")
lblBienvenido.pack(pady=(40, 10))
lblBienvenido.config(font=("Arial", 20))

foto = tk.PhotoImage(file='parqueo.gif')
lblFoto = tk.Label(ventana, image=foto)
lblFoto.pack()

ventana.mainloop()

















