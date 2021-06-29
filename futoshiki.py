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

def guardaPartidasArchivo():
    partidasFacil = list()
    partidasFacil = [((">", 0, 1), (">", 0, 5), (">", 0, 7),("4", 1, 0), ("2", 1, 8), ("4", 2, 4), ("<", 3, 7), ("4", 3, 8), ("<", 4, 1), ("<", 4, 3))]


    partidasIntermedio = list()
    partidasIntermedio = []

    partidasDificil = list()
    partidasDificil = [((">", 0, 1), (">", 0, 5), (">", 0, 7),("4", 1, 0), ("2", 1, 8), ("4", 2, 4), ("<", 3, 7), ("4", 3, 8), ("<", 4, 1), ("<", 4, 3))]
    
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
def obtener_partida_aleatoria(nivel):
    partidas = leer_partidas()
    if nivel == 0:
        cantidadPartidas = len(partidas[0])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[0][aleatorio],aleatorio
    elif nivel == 1:
        cantidadPartidas = len(partidas[1])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[1][aleatorio],aleatorio
    else:
        cantidadPartidas = len(partidas[2])
        if cantidadPartidas == 0:
            return None
        else:
            aleatorio = random.randint(0,cantidadPartidas - 1)
            return partidas[2][aleatorio],aleatorio

def obtener_partida_x_nivel_id(nivel,idpartida):
    partidas = leer_partidas()
    if nivel == 0:
        return partidas[0][idpartida]
    elif nivel == 1:
        return partidas[1][idpartida]
    else:
        return partidas[2][idpartida]
        
    

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

def validar_numero_tablero(num,i_fila,i_col,tablero_usuario):
    print("tablero",tablero_usuario)
    print("num",num,"i_fila",i_fila,"i_col",i_col)
    total_filas = len(tablero_usuario)
    total_columnas = len(tablero_usuario[0])
    
    if num in tablero_usuario[i_fila]:
        return False,"JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA FILA"

    for indice_f,fila in enumerate(tablero_usuario):
        if fila[i_col] == num:
            return False,"JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA COLUMNA"
    if i_col - 1 > 0:
        anterior = i_col - 1
        trasanterior = i_col - 2
        if tablero_usuario[i_fila][trasanterior] != 0:
            if tablero_usuario[i_fila][anterior] == ">":
                if tablero_usuario[i_fila][trasanterior] < num:
                    return False,"JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON LA RESTRICCIÓN DE MAYOR"
                    
            elif tablero_usuario[i_fila][anterior] == "<":
                if tablero_usuario[i_fila][trasanterior] > num:
                    return False,"JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON LA RESTRICCIÓN DE MENOR"
    if i_col + 1 < total_columnas:
        siguiente = i_col + 1
        subsiguiente = i_col + 2
        if tablero_usuario[i_fila][subsiguiente] != 0:
            if tablero_usuario[i_fila][siguiente] == ">":
                if tablero_usuario[i_fila][subsiguiente] < num:
                    return False,"JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON LA RESTRICCIÓN DE MAYOR"
                    
            elif tablero_usuario[i_fila][siguiente] == "<":
                if tablero_usuario[i_fila][subsiguiente] > num:
                    return False,"JUGADA NO ES VÁLIDA PORQUE NO CUMPLE CON LA RESTRICCIÓN DE MENOR"
        
    return True,True
    

def seleccion_tablero(event,ventanaJuego,num_seleccionado,es_plantilla,i_fila,i_col,tablero_usuario,pila_jugadas):
    boton = event.widget
    if num_seleccionado[0] == 0:
        messagebox.showerror(parent=ventanaJuego,title="Error", message="FALTA QUE SELECCIONE UN DÍGITO")
        return
    else:
        valor = boton.cget("text")
        if es_plantilla:
            messagebox.showerror(parent=ventanaJuego,title="Error", message="JUGADA NO ES VÁLIDA PORQUE ESTE ES UN DÍGITO FIJO")
            return
        else:
            info_posicion = boton.grid_info()
            resultado_validacion = validar_numero_tablero(num_seleccionado[0],info_posicion["row"]-3,info_posicion["column"],tablero_usuario)
            if resultado_validacion[0] == False:
                #boton.configure(bg = "red")
                messagebox.showerror(parent=ventanaJuego,title="Error", message=resultado_validacion[1])
                return
            else:
                boton.configure(text = num_seleccionado[0])

                # se agrega el numero a la pila de jugadas
                jugada = (info_posicion["row"],info_posicion["column"])
                pila_jugadas.append(jugada) # se hace el push a la pila
                
def borrar_jugada(event,ventanaJuego,pila_jugadas):
    if len(pila_jugadas) == 0:
        messagebox.showinfo(parent=ventanaJuego,title="Error", message="NO HAY MÁS JUGADAS PARA BORRAR")
        return
    else:
        posiciones = pila_jugadas.pop()
        boton = ventanaJuego.grid_slaves(row=posiciones[0], column=posiciones[1])[0]
        boton.configure(text = "")
        
        
    
            

def cargar_tablero(ventanaJuego,partida,num_seleccionado,pila_jugadas):
    listaBotones = []
    tablero_usuario = []
    contFila = 0
    pila_jugadas.clear() # Se limpia la pila de jugadas

    posicion_signos = []
    for elemento in partida:
        if not(elemento[0].isnumeric()):
            if elemento[0] == ">" or elemento[0] == "<" and elemento[2] not in posicion_signos:
                posicion_signos.append(elemento[2])
    posicion_signos.sort()

    '''
    signosColumna = []
    for elemento in partida:
        if not(elemento[0].isnumeric()):
            if elemento[0] == "^" or elemento[0] == "˅" and elemento[1] not in signosColumna:
                signosColumna.append(elemento[1])
    signosColumna.sort()
    '''
        
    fila = 3
    col = 0
    while contFila < 5:
        col = 0
        contColumnas = 0
        temp_fila_usuario = []
        while contColumnas < 5:
            bandera_encontrado = False
            for indice,elemento in enumerate(partida):
                if elemento[2] == col and elemento[1] + 3 == fila:                    
                    if elemento[0].isnumeric():
                        contColumnas += 1
                        btn = tk.Button(ventanaJuego,text=elemento[0],compound="c",height=2,width=5)
                        btn.grid(row=fila,column=col,padx=3)
                        btn.bind("<1>",lambda event,es_plantilla=True:seleccion_tablero(event,ventanaJuego,num_seleccionado,es_plantilla,fila,col,tablero_usuario,pila_jugadas))
                        listaBotones += [ btn ]
                        temp_fila_usuario.append(int(elemento[0]))
                    else:
                        btn2 = tk.Button(ventanaJuego,text=elemento[0],compound="c",height=2,width=1,bd=0,state="disabled")
                        listaBotones += [ btn2 ]
                        listaBotones[-1].grid(row=fila,column=col,padx=1)
                        temp_fila_usuario.append(elemento[0])
                    bandera_encontrado = True
                    break     
            if bandera_encontrado == False:
                if col in posicion_signos:
                    temp_fila_usuario.append(0)
                    col += 1
                    continue
                    
                else:
                    contColumnas += 1
                    if contColumnas < 6:
                        btn = tk.Button(ventanaJuego,text="",compound="c",height=2,width=5)
                        btn.grid(row=fila,column=col)
                        btn.bind("<1>",lambda event,es_plantilla=False:seleccion_tablero(event,ventanaJuego,num_seleccionado,es_plantilla,fila,col,tablero_usuario,pila_jugadas))
                        listaBotones += [ btn ]
                        temp_fila_usuario.append(0)
            col += 1
        tablero_usuario.append(temp_fila_usuario)
        contFila += 1
        fila += 1
    

    
def iniciar_juego(event,ventanaJuego,txtNombre,partida,num_seleccionado,obj,btnTerminarJuego,btnBorrarJuego,btnBorrarJugada,pila_jugadas):
    while obj['state'] == "normal":
        if len(txtNombre.get()) < 1 or len(txtNombre.get()) > 20:
            messagebox.showerror(parent=ventanaJuego,title="Error", message="DEBE INGRESAR UN NOMBRE QUE CONTENGA DE 1 A 20 CARACTERES")
            return
        if not txtNombre.get().isalpha():
            messagebox.showerror(parent=ventanaJuego,title="Error", message="DEBE INGRESAR UN NOMBRE VÁLIDO")
            return
        
        if partida == None:
            messagebox.showerror(parent=ventanaJuego,title="Error", message="NO HAY PARTIDAS PARA ESTE NIVEL")
            ventanaJuego.destroy()
            return

        # se carga la partida
        cargar_tablero(ventanaJuego,partida,num_seleccionado,pila_jugadas)
            

        # se deshabilita el boton
        obj.configure(state= "disabled")
        # se habilita el boton de terminar juego
        btnTerminarJuego.configure(state= "normal")
        # se habilita el boton de borrar juego
        btnBorrarJuego.configure(state= "normal")
        # se habilita el boton de borrar jugada
        btnBorrarJugada.configure(state= "normal")
    
def terminar_juego(event,ventana,obj,dic_config,num_selec,n1,n2,n3,n4,n5,pila_jugadas):
    respuesta = messagebox.askyesno(parent=ventana,title="Confirmación", message="¿ESTÁ SEGURO DE TERMINAR EL JUEGO (SI o NO)?")
    if respuesta:
        # Se limpian la seleccion de los botones:
        n1.configure(background = "SystemButtonFace")
        n2.configure(background = "SystemButtonFace")
        n3.configure(background = "SystemButtonFace")
        n4.configure(background = "SystemButtonFace")
        n5.configure(background = "SystemButtonFace")
        
        partida = obtener_partida_aleatoria(dic_configuracion["nivel"])
        num_selec[0] = 0
        cargar_tablero(ventana,partida[0],num_selec,pila_jugadas)
        messagebox.showinfo(parent=ventana,title="Mensaje", message="JUEGO TERMINADO. SE HA CARGADO UN JUEGO NUEVO")
             
def borrar_juego(event,ventana,obj,dic_config,num_partida,num_seleccionado,n1,n2,n3,n4,n5,pila_jugadas):
    respuesta = messagebox.askyesno(parent=ventana,title="Confirmación", message="¿ESTÁ SEGURO DE BORRAR EL JUEGO (SI o NO)")
    if respuesta:
        # Se limpian la seleccion de los botones:
        n1.configure(background = "SystemButtonFace")
        n2.configure(background = "SystemButtonFace")
        n3.configure(background = "SystemButtonFace")
        n4.configure(background = "SystemButtonFace")
        n5.configure(background = "SystemButtonFace")
        
        partida = obtener_partida_x_nivel_id(dic_config["nivel"],num_partida)
        num_seleccionado[0] = 0
        cargar_tablero(ventana,partida,num_seleccionado,pila_jugadas)
        messagebox.showinfo(parent=ventana,title="Mensaje", message="JUEGO BORRADO. SE HA REINICIADO EL JUEGO")

    


#VENTANA JUEGO:
#Funcion que carga la ventana de configuracion asi como todos los componentes
#Entradas: ninguna
#Salidas: ninguna
def juego():
    dic_configuracion = actualizar_dic_configuracion()
    resultado = obtener_partida_aleatoria(dic_configuracion["nivel"]) # se obtiene la partida segun el nivel configurado por el usuario
    partida = resultado[0]
    num_partida = resultado[1]
    num_seleccionado = [0]

    # TDA = PILA para el control del borrado de jugadas
    pila_jugadas = []
    
    lista_nivel = ["FÁCIL", "INTERMEDIO", "DIFÍCIL"]
    ventanaJuego = tk.Toplevel()
    ventanaJuego.title("FUTOSHIKI")
    ventanaJuego.geometry("1400x600")
    lblTitulo = tk.Label(ventanaJuego, text="FUTOSHIKI")
    lblTitulo.grid(row=0,column=10)
    lblNivel = tk.Label(ventanaJuego, text="NIVEL" + " " + lista_nivel[dic_configuracion["nivel"]])
    lblNivel.grid(row=1,column=10)

    lblNombre = tk.Label(ventanaJuego, text="Nombre del jugador:")
    lblNombre.grid(row=2,column=11)
    txtNombre = tk.StringVar()
    entryNombre = tk.Entry(ventanaJuego,textvariable=txtNombre)
    entryNombre.grid(row=2,column=12)

    
    # CUADRICULA INICIAL
    '''
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
    '''
        
    n1 = tk.Button(ventanaJuego,text="1",compound="c",height=2,width=5)
    n1.grid(row=3,column=10,padx=50)
    n2 = tk.Button(ventanaJuego,text="2",compound="c",height=2,width=5)
    n2.grid(row=4,column=10,padx=50)
    n3 = tk.Button(ventanaJuego,text="3",compound="c",height=2,width=5)
    n3.grid(row=5,column=10,padx=50)
    n4 = tk.Button(ventanaJuego,text="4",compound="c",height=2,width=5)
    n4.grid(row=6,column=10,padx=50)
    n5 = tk.Button(ventanaJuego,text="5",compound="c",height=2,width=5)
    n5.grid(row=7,column=10,padx=50)

    n1.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,1,num_seleccionado,n1,n2,n3,n4,n5))
    n2.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,2,num_seleccionado,n1,n2,n3,n4,n5))
    n3.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,3,num_seleccionado,n1,n2,n3,n4,n5))
    n4.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,4,num_seleccionado,n1,n2,n3,n4,n5))
    n5.bind("<1>",lambda event:agregar_digito(event,ventanaJuego,5,num_seleccionado,n1,n2,n3,n4,n5))
    
    # Botones
    btnIniciar = tk.Button(ventanaJuego, text="INICIAR JUEGO", bg="red")
    btnIniciar.grid(row=8,column=11)

    btnBorrarJugada = tk.Button(ventanaJuego, text="BORRAR JUGADA", bg="cyan", state="disabled")
    btnBorrarJugada.grid(row=8,column=12)

    btnTerminarJuego = tk.Button(ventanaJuego, text="TERMINAR JUEGO", bg="green", state="disabled")
    btnTerminarJuego.grid(row=8,column=13)

    btnBorrarJuego = tk.Button(ventanaJuego, text="BORRAR JUEGO", bg="violet",state="disabled")
    btnBorrarJuego.grid(row=8,column=14)

    btnTop10 = tk.Button(ventanaJuego, text="TOP 10", bg="yellow")
    btnTop10.grid(row=8,column=15)

    # Eventos
    btnIniciar.bind("<1>",lambda event,obj=btnIniciar:iniciar_juego(event,ventanaJuego,txtNombre,partida,num_seleccionado,obj,btnTerminarJuego,btnBorrarJuego,btnBorrarJugada, \
                                                                    pila_jugadas))
    btnTerminarJuego.bind("<1>",lambda event,ventana=ventanaJuego,obj=btnTerminarJuego,dic_config=dic_configuracion,num_selec=num_seleccionado: \
                                                        terminar_juego(event,ventana,obj,dic_config,num_selec,n1,n2,n3,n4,n5,pila_jugadas))
    btnBorrarJuego.bind("<1>",lambda event,ventana=ventanaJuego,obj=btnBorrarJuego,dic_config=dic_configuracion,idpartida=num_partida,num_selec=num_seleccionado: \
                                                        borrar_juego(event,ventana,obj,dic_config,idpartida,num_selec,n1,n2,n3,n4,n5,pila_jugadas))
    btnBorrarJugada.bind("<1>",lambda event:borrar_jugada(event,ventanaJuego,pila_jugadas))

    
    # Guardar / Cargar
    btnGuardar = tk.Button(ventanaJuego, text="GUARDAR JUEGO")
    btnGuardar.grid(row=9,column=16)

    btnCargar = tk.Button(ventanaJuego, text="CARGAR JUEGO")
    btnCargar.grid(row=9,column=17)

    
    
    




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

















