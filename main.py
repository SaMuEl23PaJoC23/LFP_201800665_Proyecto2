import tkinter
import tkinter.font as tkFont
from tkinter import DISABLED, END, NORMAL, messagebox
from analizarTexto import analizar
from escrituraComandos import escritura
from crearGrafos import grafos
import webbrowser as wb
import easygui

Mensaje="Esperando Archivo..."
analizarT=analizar()
traducir=escritura()
grafo=grafos()
#------------Ventana Principal--------
VentanaRaiz = tkinter.Tk()
VentanaRaiz.config(bg="chartreuse")
VentanaRaiz.geometry("328x50")
VentanaRaiz.resizable(0,0)
VentanaRaiz.title("Proyecto No.2-Menu Principal")
fontStyle = tkFont.Font(family="Times", size=12)

#-----------------------------------------------------------------------------
def ManualUsuario():
    wb.open_new(r'manuales\Manual de Usuario.pdf')
#-----------------------------------------------------------------------------
def ManualTecnico():
    wb.open_new(r'manuales\Manual Tecnico.pdf')

#-----------------------------------------------------------------------------
def mostrarTokens():
    wb.open_new(r'grafos\tokens.dot.png')
#-----------------------------------------------------------------------------
def mostrarErrores():
    wb.open_new(r'grafos\errores.dot.png')
#-----------------------------------------------------------------------------
def guardar():
    archivoGuardar=open(ruta, 'w')
    archivoGuardar.write(areaTexto.get("1.0",END))
    archivoGuardar.close()
    messagebox.showinfo("--ALERT--",">> Archivo -Guardado- <<")

#-----------------------------------------------------------------------------
def guardarC():
    if inputNombreArchivoGC.get() != "":
        NomArchivo=inputNombreArchivoGC.get()+".txt"
        
        archivoGuardar=open(NomArchivo, 'w')
        archivoGuardar.write(areaTexto.get("1.0",END))
        archivoGuardar.close()
        messagebox.showinfo("--ALERT--",">> Archivo -Guardado- <<")
        inputNombreArchivoGC.delete(0, END)
    else:
        messagebox.showerror("--ALERT--","!! Debe ingresar un nombre !!")

#-----------------------------------------------------------------------------
def guardarComo():
    VentanaGuardarC = tkinter.Tk()
    VentanaGuardarC.config(bg="chartreuse")
    VentanaGuardarC.geometry("305x80")
    VentanaGuardarC.resizable(0,0)
    VentanaGuardarC.title("Guardar como:")
    
    fontStyle = tkFont.Font(family="Times", size=14)
    subTitulo = tkinter.Label(VentanaGuardarC, text="Nombre del nuevo archivo:", bg="orange", font='Times 13')
    subTitulo.place(x=25, y=10)
    
    global inputNombreArchivoGC
    inputNombreArchivoGC = tkinter.Entry(VentanaGuardarC, font=fontStyle)
    inputNombreArchivoGC.place(x=25, y=45)
    
    botonG = tkinter.Button(VentanaGuardarC, text="Guardar", bg="cyan", font='Times 13', command=guardarC)
    botonG.place(x=230,y=40)
    
#-----------------------------------------------------------------------------
def Bloquear():
    botonNuevo.config(state=DISABLED)
    botonGuardar.config(state=DISABLED)
    botonGuardarC.config(state=DISABLED)
    botonAnalizar.config(state=DISABLED)
    botonErrores.config(state=DISABLED)
    botonTokens.config(state=DISABLED)
#-----------------------------------------------------------------------------
def DesBloquear():
    botonNuevo.config(state=NORMAL)
    botonGuardar.config(state=NORMAL)
    botonGuardarC.config(state=NORMAL)
    botonAnalizar.config(state=NORMAL)
#-----------------------------------------------------------------------------
def analizarTextoPantalla():
    global resultado
    texto=areaTexto.get("1.0",END)
    resultado=analizarT.analizarEntrada(texto)
    #resultado: [[Funciones],[Tokens],[Errores]]
    botonTokens.config(state=NORMAL)
    grafo.grafoTokens(resultado[1])
    
    if resultado[2] == []:
        botonErrores.config(state=DISABLED)
        resultado2=traducir.escrituraComandosMongoDB(resultado[0])
        areaTextoSalida.delete("1.0",END)
        areaTextoSalida.insert("1.0",resultado2)
        messagebox.showinfo("--ALERT--",">> Archivo Analizado Exitosamente<<")
        
        archivoGuardar2=open('traduccion\\comandos_MongoDB.txt', 'w')
        archivoGuardar2.write(resultado2)
        archivoGuardar2.close()
        
    
    else:
        messagebox.showerror("--ALERT--","!! El archivo cuenta con error(es)!!\n\n  !!Verificar en opcion-->> Ver Errores!!")
        botonErrores.config(state=NORMAL)
        grafo.grafoErrores(resultado[2])
        areaTextoSalida.delete("1.0",END)

#-----------------------------------------------------------------------------
def guardarN():
    if inputNombreArchivo.get() != "" and inputRutaArchivo.get() != "":
        
        archivoN=inputRutaArchivo.get()+"\\"+inputNombreArchivo.get()+".txt"
        archivoGuardar=open(archivoN, 'w')
        archivoGuardar.write(auxTexto)
        archivoGuardar.close()
        messagebox.showinfo("--ALERT--",">> Archivo -Guardado- <<")
        inputRutaArchivo.delete(0, END)
        inputNombreArchivo.delete(0, END)

    else:
        messagebox.showerror("--ALERT--","!! Debe completar todos los campos !!")

#-----------------------------------------------------------------------------
def guardarNuevo():
    
    global auxTexto
    auxTexto=areaTexto.get("1.0",END)
    areaTexto.delete("1.0",END)
    areaTexto.insert("1.0","Esperando Archivo...")
    areaTextoSalida.delete("1.0",END)
    Bloquear()
    
    VentanaGuardarN = tkinter.Tk()
    VentanaGuardarN.config(bg="chartreuse")
    VentanaGuardarN.geometry("445x135")
    VentanaGuardarN.resizable(0,0)
    VentanaGuardarN.title(">> Guardar Cambios <<")
    
    fontStyle = tkFont.Font(family="Times", size=14)
    subTitulo = tkinter.Label(VentanaGuardarN, text="Para guardar cambios ingrese:", bg="orange", font='Times 13')
    subTitulo.place(x=135, y=10)
    
    labelPath = tkinter.Label(VentanaGuardarN, text="path para el archivo:", bg="chartreuse", font='Times 13')
    labelPath.place(x=10, y=45)
    
    labelNombreA = tkinter.Label(VentanaGuardarN, text="Nombre del archivo:", bg="chartreuse", font='Times 13')
    labelNombreA.place(x=10, y=95)
    
    
    global inputNombreArchivo, inputRutaArchivo
    
    inputRutaArchivo = tkinter.Entry(VentanaGuardarN, font=fontStyle)
    inputRutaArchivo.place(x=155, y=50)
    
    inputNombreArchivo = tkinter.Entry(VentanaGuardarN, font=fontStyle)
    inputNombreArchivo.place(x=155, y=100)
    
    botonGNuevo = tkinter.Button(VentanaGuardarN, text="Guardar", bg="cyan", font='Times 13', command=guardarN)
    botonGNuevo.place(x=355,y=68)

#----------- Funcion abrir archivo --------
def Abrir():
    global ruta
    ruta=easygui.fileopenbox()
    
    if ruta != None:
        messagebox.showinfo("--ALERT--",">> Archivo cargado exitosamente <<")
        archivoSeleccionado=open(ruta)
        textoArchivo=archivoSeleccionado.read()
        archivoSeleccionado.close()
        
        areaTexto.delete("1.0",END)
        areaTexto.insert("1.0",textoArchivo)
        DesBloquear()
    else:
        messagebox.showerror("--ALERT--","!! Archivo no seleccionado !!")

#------------Ventana Menu Archivo--------
def ventanaMenuArchivo():
    ventanaArchivo = tkinter.Tk()
    ventanaArchivo.config(bg="mediumturquoise")
    ventanaArchivo.geometry("1130x560")
    ventanaArchivo.resizable(0,0)
    ventanaArchivo.title(">> Menu Archivo <<")
    #--------- Componentes (Ventana Menu Archivo) ---------
    global areaTexto, areaTextoSalida, botonGuardar, botonGuardarC, botonNuevo, botonAnalizar, botonErrores, botonTokens
    
    areaTexto=tkinter.Text(ventanaArchivo, width=60, height=24, font=fontStyle, bg="lightgray")
    areaTexto.insert("1.0",Mensaje)
    areaTexto.place(x=10,y=90)
    
    areaTextoSalida=tkinter.Text(ventanaArchivo, width=60, height=24, font=fontStyle, bg="lightgray")
    areaTextoSalida.place(x=570,y=90)
    
    botonAbrir = tkinter.Button(ventanaArchivo, text="Abrir", bg="chartreuse", font='Times 13 bold', command=Abrir)
    botonAbrir.place(x=10,y=10)
    
    botonNuevo = tkinter.Button(ventanaArchivo, text="Nuevo", bg="cyan", font='Times 13', state=DISABLED, command=guardarNuevo)
    botonNuevo.place(x=120,y=10)
    
    botonGuardar = tkinter.Button(ventanaArchivo, text="Guardar", bg="gold", font='Times 13', state=DISABLED, command=guardar)
    botonGuardar.place(x=190,y=10)
    
    botonGuardarC = tkinter.Button(ventanaArchivo, text="Guardar Como...", bg="yellow", font='Times 13', state=DISABLED, command=guardarComo)
    botonGuardarC.place(x=270,y=10)
    
    botonAnalizar = tkinter.Button(ventanaArchivo, text="Analizar", bg="red", font='Times 13 bold', state=DISABLED, command=analizarTextoPantalla)
    botonAnalizar.place(x=530,y=45)
    
    botonTokens = tkinter.Button(ventanaArchivo, text="Ver Tokens", bg="teal", font='Times 13', state=DISABLED, command=mostrarTokens)
    botonTokens.place(x=910,y=10)
    
    botonErrores = tkinter.Button(ventanaArchivo, text="Ver Errores", bg="purple", font='Times 13', state=DISABLED, command=mostrarErrores)
    botonErrores.place(x=1020,y=10)
    
    EtiquetaX = tkinter.Label(ventanaArchivo, text="X: ", font='Times 10', bg='mediumturquoise')
    EtiquetaX.place(x=10, y=530)
    
    EtiquetaY = tkinter.Label(ventanaArchivo, text="Y: ", font='Times 10', bg='mediumturquoise')
    EtiquetaY.place(x=85, y=530)
    
    EtiquetaEntrada = tkinter.Label(ventanaArchivo, text="Instrucciones de >> Entrada <<", fg='yellow', font='Times 13 bold', bg='black')
    EtiquetaEntrada.place(x=145, y=58)
    
    EtiquetaSalida = tkinter.Label(ventanaArchivo, text="Instrucciones de >> Salida <<", fg='yellow', font='Times 13 bold', bg='black')
    EtiquetaSalida.place(x=760, y=58)
    
#------------Ventana Documentacion--------
def ventanaDocu():
    global fontStyle
    ventanaDocu = tkinter.Tk()
    ventanaDocu.config(bg="lightseagreen")
    ventanaDocu.geometry("295x95")
    ventanaDocu.resizable(0,0)
    ventanaDocu.title(">> Documentacion <<")
    #--------- Componentes (Ventana Documentacion) ---------
    botonManUsuario = tkinter.Button(ventanaDocu, text="Manual Usuario", bg="chartreuse", font=fontStyle, command=ManualUsuario)
    botonManUsuario.place(x=90,y=10)
    
    botonManTecnico = tkinter.Button(ventanaDocu, text="Manual Tecnico", bg="purple", font=fontStyle, command=ManualTecnico)
    botonManTecnico.place(x=90,y=50)

#--------- Componentes (Ventana Principal) ---------
botonArchivo = tkinter.Button(VentanaRaiz, text="Menu Archivo", bg="orange", font=fontStyle, command=ventanaMenuArchivo)
botonArchivo.place(x=20,y=10)
botonDocu = tkinter.Button(VentanaRaiz, text="Documentacion", bg="yellow", font=fontStyle, command=ventanaDocu)
botonDocu.place(x=200,y=10)

#--------------------------------
VentanaRaiz.mainloop()