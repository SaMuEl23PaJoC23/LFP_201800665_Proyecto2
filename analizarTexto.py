class analizar():
    def EsLetra(self,caracter):
        if (ord(caracter)>=65 and ord(caracter)<=90) or (ord(caracter)>=97 and ord(caracter)<=122) or ord(caracter)==164 or ord(caracter)==165:
            return True
        else:
            return False
    
    def EsNumero(self,caracter):
        if (ord(caracter) >= 48 and ord(caracter) <=57):
            return True
        else:
            return False
    
    def analizarEntrada(self, texto):
        fila=1
        columna=0
        estado=0
        texto=texto[:-1]
        texto+='#'
        lexActual=''
        funcionesP=['crearbd','eliminarbd','crearcoleccion','eliminarcoleccion','insertarunico','actualizarunico','eliminarunico','buscartodo','buscarunico']
        simbolosP=['/','*','-','=','(',')',':',',',';','\"','{','}','$']
        OtrosSimbolos=[" ","\n","\t","#",'\s']
        simbolosP2=['/','*','-','=','(',')','.',':',',',';','{','}','$'," ","\n","\t","#",'\s']
        listaTokens=[]  #Almacena todos los tokens reconocidos
        listaErrores=[] #Almacena todos los errores detectados
        lista=[]        #Lista auxiliar
        resultado=[]    #Lista que retornara todo lo analizado
        funciones=[]
        AuxFuncion=''
        auxVariable=''
        auxNombreColeccion=''
        datosJson=[]
#--------------------------------inicia Automata----------------------------------------
        for caracter in texto:
            columna+=1
            #print('Estado: '+str(estado)+' -> ('+caracter+'), fila:'+str(fila)+' columna:'+str(columna)+' ,Error:'+str(len(listaErrores)))
#------------------------------------------------------------            
            if self.EsLetra(caracter) == False:
                if self.EsNumero(caracter) == False:
                    if caracter != '.':
                        if caracter not in simbolosP:
                            if caracter not in OtrosSimbolos:
                                lista=['(LEXICO)',caracter, 'LETRA, NUMERO, simbolosP, OtrosSimbolos', fila, columna, 'Caracter No valido']
                                listaErrores.append(lista)
#-------------------Estado S0-------------------------------
            if estado==0:
                if caracter == '-':
                    estado=6
                
                elif caracter == '/':
                    estado=1
                
                elif self.EsLetra(caracter):
                    lexActual=caracter
                    estado=10
                
                elif caracter ==" ":
                    continue
                    
                elif caracter =="\n":
                    fila+=1
                    columna=0

                elif caracter == "\t":
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '-, /, LETRA', fila, columna, 'Desface de caracter']
                    #[seDetecto,seLee,seEsperaba,Y,X,RazonError]
                    listaErrores.append(lista)
#-------------------Estado S1-------------------------------
            elif estado==1:
                if caracter == '*':
                    estado=2
                    lista=['Apertura_ComentMulti', '/*']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, '*', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S2-------------------------------
            elif estado==2:
                if caracter == "\t":
                    columna+=3
                elif caracter =="\n":
                    fila+=1
                    columna=0
                lexActual=caracter
                estado=3
#-------------------Estado S3-------------------------------
            elif estado==3:
                if caracter == '*':
                    estado=4
                    lista=['ComentMulti', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    continue
                    
                elif caracter =="\n":
                    fila+=1
                    columna=0

                elif caracter == "\t":
                    columna+=3
                    
                lexActual+=caracter
#-------------------Estado S4-------------------------------
            elif estado==4:
                if caracter == '/':
                    #>>> se aceptan los comandos <<<
                    estado=5
                    lista=['Cierre_ComentMulti', '*/']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, '/', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S5-------------------------------
            elif estado==5:
                if caracter == '\n':
                    estado=0
                    fila+=1
                    columna=0
                    
                elif caracter == '#':
                    continue
                
                else:
                    lista=['(SINTACTICO)',caracter, '\\n', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S6-------------------------------
            elif estado==6:
                if caracter == '-':
                    estado=7
                    
                else:
                    lista=['(SINTACTICO)',caracter, '-', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S7-------------------------------
            elif estado==7:
                if caracter == '-':
                    estado=8
                    lista=['ComentUnaLinea', '---']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                  
                else:
                    lista=['(SINTACTICO)',caracter, '-', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S8-------------------------------
            elif estado==8:
                if caracter != '\n':
                    if caracter == "\t":
                        columna+=3
                        
                    lexActual=caracter    
                    estado=9
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S9-------------------------------
            elif estado==9:
                if caracter != '\n':
                    lexActual+=caracter
                    
                elif caracter == "\n":
                    #>>> se aceptan los comandos <<<
                    estado=0
                    fila+=1
                    columna=0
                    lista=['ContenidoComentUnaLinea', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
#-------------------Estado S10-------------------------------
            elif estado==10:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                    
                elif caracter == " " or caracter == '\s':
                    if lexActual.lower() in funcionesP:
                        AuxFuncion=lexActual
                        estado=11
                        lista=['FuncionValida', lexActual]#[TokenTipo, Lexema]
                        listaTokens.append(lista)
    
                    else:
                        lista=['(SINTACTICO)',lexActual, 'FUNCION VALIDA', fila, columna, 'Funcion no permitida']
                        listaErrores.append(lista)
                    
                else:
                    lista=['(SINTACTICO)', lexActual+caracter, 'LETRA, (\\s)', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S11-------------------------------
            elif estado==11:
                if self.EsLetra(caracter):
                    estado=12
                    lexActual=caracter
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S12-------------------------------
            elif estado==12:
                if self.EsLetra(caracter) or self.EsNumero(caracter):
                    lexActual+=caracter
                    
                elif caracter ==" ":
                    estado=13
                    auxVariable=lexActual
                    lista=['Nom_VariableComando', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \\s', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S13-------------------------------
            elif estado==13:
                if caracter == '=':
                    estado=14
                    lista=['Signo_Igual', '=']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, '=', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S14-------------------------------
            elif estado==14:    
                if caracter ==" ":
                    estado=15
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\\s', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S15-------------------------------
            elif estado==15:
                if self.EsLetra(caracter):
                    lexActual=caracter
                    estado=16
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S16-------------------------------
            elif estado==16:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                    
                elif caracter ==" ":
                    if lexActual.lower() == 'nueva':
                        estado=17
                        lista=['Afirmacion_FuncionNueva', 'nueva']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                        
                    else:
                        lista=['(SINTACTICO)',lexActual, 'nueva', fila, columna, 'palabra -Reservada- no valida']
                        listaErrores.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \\s', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S17-------------------------------
            elif estado==17:
                if self.EsLetra(caracter):
                    estado=18
                    lexActual=caracter
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S18-------------------------------
            elif estado==18:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                    
                elif caracter =='(':
                    estado=19
                    if lexActual.lower() != AuxFuncion.lower():
                        lista=['(SINTACTICO)', lexActual, AuxFuncion, fila, columna, 'funcionesIncompatibles']
                        listaErrores.append(lista)
                    else:
                        lista=['2daV_FuncionValida', lexActual.lower()]#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                        lista=['Parentesis_Apertura', '(']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, (', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S19-------------------------------
            elif estado==19:
                if caracter == ')':
                    estado=20
                    if AuxFuncion.lower() != 'crearbd' and AuxFuncion.lower() != 'eliminarbd':
                        lista=['(SINTACTICO)',AuxFuncion, 'FaltaParametros', fila, columna, 'Funcion Incompleta']
                        listaErrores.append(lista)
                    else:
                        lista=['Parentesis_Cierre', ')']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                
                
                elif caracter == '\"':
                    estado=21
                    if AuxFuncion.lower() == 'crearbd' or AuxFuncion.lower() == 'eliminarbd':
                        lista=['(SINTACTICO)',caracter, 'Funcion_No_Necesita_Parametros', fila, columna, 'Funcion Incorrecta']
                        listaErrores.append(lista)
                    else:
                        lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                        listaTokens.append(lista) 
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\", )', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S20-------------------------------
            elif estado==20:
                if caracter == ';':
                    estado=5
                    lista=['FinInstruccion', ';']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                    # >>>se aceptan los comandos <<<
                    funciones.append(AuxFuncion)    
                    if AuxFuncion.lower() == 'crearbd' or AuxFuncion.lower() == 'eliminarbd':
                        lista=[auxVariable]
                        funciones.append(lista)
                        #Se guarda: Funcion,[VARfuncion]
                    else:
                        lista=[auxVariable,auxNombreColeccion]
                        funciones.append(lista)
                        # Funcion,[VARfuncion,Coleccion]
                    
                else:
                    lista=['(SINTACTICO)',caracter, ';', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S21-------------------------------
            elif estado==21:
                if self.EsLetra(caracter):
                    estado=22
                    lexActual=caracter
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S22-------------------------------
            elif estado==22:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                    
                elif caracter =='\"':            
                    estado=23
                    auxNombreColeccion=lexActual
                    lista=['NombreColeccion', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S23-------------------------------
            elif estado==23:
                if caracter == ',':
                    if AuxFuncion.lower() == 'eliminarunico' or AuxFuncion.lower() == 'actualizarunico' or AuxFuncion.lower() == 'insertarunico':
                        estado=25
                        lista=['MasParametros', '\',\'']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    else:
                        lista=['(SINTACTICO)',caracter, 'Funcion Incorrecta', fila, columna, 'Funcion Incompleta']
                        listaErrores.append(lista)
                    
                elif caracter ==')':
                    if AuxFuncion.lower() == 'crearcoleccion' or AuxFuncion.lower() == 'eliminarcoleccion' or AuxFuncion.lower() == 'buscartodo' or AuxFuncion.lower() == 'buscarunico':
                        estado=20
                        lista=['Parentesis_Cierre', ')']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    else:
                        lista=['(SINTACTICO)',caracter, 'Funcion Incorrecta', fila, columna, 'Funcion Incompleta']
                        listaErrores.append(lista)
                        
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                
                else:
                    lista=['(SINTACTICO)',caracter, '\',\', )', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S25-------------------------------
            elif estado==25:
                if caracter == '\"':
                    estado=26
                    lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S26-------------------------------
            elif estado==26:
                if caracter == '{':
                    estado=27
                    lista=['llave_Apertura', '{']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '{', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S27-------------------------------
            elif estado==27:
                if caracter == '\"':
                    estado=28
                    lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S28-------------------------------
            elif estado==28:
                if self.EsLetra(caracter):
                    estado=29
                    lexActual=caracter
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S29-------------------------------
            elif estado==29:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                    
                elif caracter =='\"':
                    estado=30
                    auxLLave=lexActual
                    lista=['Campo_LLave', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S30-------------------------------
            elif estado==30:
                if caracter == ':':
                    estado=31
                    lista=['Dospuntos', ':']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3    
                       
                else:
                    lista=['(SINTACTICO)',caracter, ':', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S31-------------------------------
            elif estado==31:
                if caracter == '\"':
                    estado=32
                    lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S32-------------------------------
            elif estado==32:
                if self.EsLetra(caracter) or caracter in simbolosP2:
                    estado=33
                    lexActual=caracter
                    
                    if caracter == '\t':
                        columna+=3
                        
                    elif caracter == '\n':
                        fila+=1
                        columna=0
                        
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S33-------------------------------
            elif estado==33:
                if self.EsLetra(caracter) or caracter in simbolosP2:
                    lexActual+=caracter
                
                    if caracter == '\t':
                        columna+=3
                        
                    elif caracter == '\n':
                        fila+=1
                        columna=0
                
                elif caracter == '\"':
                    estado=34
                    auxValor=lexActual
                    lista=['Campo_Valor', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S34-------------------------------
            elif estado==34:
                if caracter == ',':
                    estado=27
                    datosJson.append(auxLLave)
                    datosJson.append(auxValor)
                    lista=['MasParametros', '\',\'']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '}':
                    estado=39
                    datosJson.append(auxLLave)
                    datosJson.append(auxValor)
                    lista=['llave_Cierre', '}']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                
                elif caracter == '\n':
                    columna=0
                    fila+=1
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\',\', }', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S35-------------------------------
            elif estado==35:
                if caracter == '}':
                    estado=36
                    lista=['llave_Cierre', '}']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '}', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)                          
#-------------------Estado S36-------------------------------
            elif estado==36:
                if caracter == '\"':
                    estado=37
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S37-------------------------------
            elif estado==37:
                if caracter == ')':
                    estado=38
                    lista=['Parentesis_Cierre', ')']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, ')', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S38-------------------------------
            elif estado==38:
                if caracter == ';':
                    estado=5
                    lista=['FinInstruccion', ';']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    #>>> se aceptan los comandos <<<
                    funciones.append(AuxFuncion)#Se almacena: FUNCION,[NomVariable,Coleccion,[DatosJSON]]
                    lista=[auxVariable,auxNombreColeccion,datosJson]
                    funciones.append(lista)
                    datosJson=[]

                else:
                    lista=['(SINTACTICO)',caracter, ';', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S39-------------------------------
            elif estado==39:
                if caracter == ',':
                    if AuxFuncion.lower() == 'actualizarunico':
                        estado=40
                        lista=['MasParametros', '\',\'']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    else:
                        lista=['(SINTACTICO)',caracter, 'Funcion Incorrecta', fila, columna, 'Funcion Incompleta']
                        listaErrores.append(lista) 
                    
                elif caracter == '\"':
                    if AuxFuncion.lower() == 'eliminarunico' or AuxFuncion.lower() == 'insertarunico':
                        estado=37
                        lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    else:
                        lista=['(SINTACTICO)',caracter, 'Funcion Incorrecta', fila, columna, 'Funcion Incompleta']
                        listaErrores.append(lista)    
                    
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\',\'', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S40-------------------------------
            elif estado==40:
                if caracter == '{':
                    estado=41
                    lista=['llave_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '{', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S41-------------------------------
            elif estado==41:
                if caracter == '$':
                    estado=42
                    lista=['ActualizarInfo', '$']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                
                elif caracter == '\n':
                    fila+=1
                    columna=0
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3    
                    
                else:
                    lista=['(SINTACTICO)',caracter, '$', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S42-------------------------------
            elif estado==42:
                if self.EsLetra(caracter):
                    lexActual=caracter
                    estado=43
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S43-------------------------------
            elif estado==43:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                
                elif caracter == ':':
                    if lexActual.lower() == 'set':
                        estado=44
                        lista=['Campo_Establecer', 'set']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                        lista=['Dospuntos', ':']#[TokenTipo, Lexema]
                        listaTokens.append(lista)
                    else:
                        lista=['(SINTACTICO)',lexActual, 'set', fila, columna, 'Palabra no valida']
                        listaErrores.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, :', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S44-------------------------------
            elif estado==44:
                if caracter == '{':
                    estado=45
                    lista=['llave_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '{', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S45-------------------------------
            elif estado==45:
                if caracter == '\"':
                    estado=46
                    lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S46-------------------------------
            elif estado==46:
                if self.EsLetra(caracter):
                    lexActual=caracter
                    estado=47
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S47-------------------------------
            elif estado==47:
                if self.EsLetra(caracter):
                    lexActual+=caracter
                
                elif caracter == '\"':
                    estado=48
                    auxLLave=lexActual
                    lista=['Campo_LLave', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S48-------------------------------
            elif estado==48:
                if caracter == ':':
                    estado=49
                    lista=['Dospuntos', ':']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, ':', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)              
#-------------------Estado S49-------------------------------
            elif estado==49:#AQUI VOY, SEGUIR AQUI EN ADELANTE, terminar tokens, ver almacenamiento de datos impo.
                if caracter == '\"':
                    estado=50
                    lista=['ComillasDob_Apertura', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                elif caracter == ' ' or caracter == '\s':
                    continue
                
                elif caracter == '\t':
                    columna+=3
                    
                else:
                    lista=['(SINTACTICO)',caracter, '\"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S50-------------------------------
            elif estado==50:
                if self.EsLetra(caracter) or caracter in simbolosP2:
                    estado=51
                    lexActual=caracter

                    if caracter == '\t':
                        columna+=3
                        
                    elif caracter == '\n':
                        fila+=1
                        columna=0
                
                    
                else:
                    lista=['(SINTACTICO)',caracter, 'LETRA', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)                           
#-------------------Estado S51-------------------------------
            elif estado==51:
                if self.EsLetra(caracter) or caracter in simbolosP2:
                    lexActual+=caracter
                
                    if caracter == '\t':
                        columna+=3
                        
                    elif caracter == '\n':
                        fila+=1
                        columna=0
                
                elif caracter == '\"':
                    estado=52
                    auxValor=lexActual
                    lista=['Campo_Valor', lexActual]#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    lista=['ComillasDob_Cierre', '\"']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',lexActual+caracter, 'LETRA, \"', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#-------------------Estado S52-------------------------------
            elif estado==52:
                if caracter == '}':
                    estado=35
                    datosJson.append('$')
                    datosJson.append(auxLLave)
                    datosJson.append(auxValor)
                    lista=['llave_Cierre', '}']#[TokenTipo, Lexema]
                    listaTokens.append(lista)
                    
                else:
                    lista=['(SINTACTICO)',caracter, '}', fila, columna, 'Desface de caracter']
                    listaErrores.append(lista)
#------------------------------------------------------------                                      
        resultado.append(funciones) # Funciones: auxFuncion,[auxVariable,auxNombrecoleccion,[datosJSON]],...
        resultado.append(listaTokens) #Tokens: [TokenTipo, Lexema],...
        resultado.append(listaErrores)# Errores: [seDetecto,seLee,seEsperaba,Y,X,RazonError],...
        return resultado