from graphviz import render
class grafos():
    def grafoTokens(self, tokens):
        nombreImagenSalida='grafos/tokens.dot'
        
        escribir = open(nombreImagenSalida, 'w')
        escribir.write('digraph tokens { \n')
        #escribir.write('rankdir=')
#------NODO principal---------------------------
        escribir.write('NodoTokens [shape=none, margin=0, label=<\n')
        escribir.write('<table border=\"0\" cellborder= \"1\">\n')
        escribir.write('<tr>\n')
        escribir.write('<td>No. </td> <td>TOKEN</td> <td>LEXEMA</td>\n')
        escribir.write('</tr>\n')
        indice=0
        for token in tokens:
            indice+=1
            escribir.write('<tr>\n')
            escribir.write('<td>'+str(indice)+'</td> <td>'+str(token[0])+'</td> <td>'+str(token[1])+'</td>\n')
            escribir.write('</tr>\n')
        escribir.write('</table>>];\n')
#-----------------------------------------------
        escribir.write('}\n')
        escribir.close()
        
        render('dot', 'png', nombreImagenSalida)
#-----------------------------------------------
#-----------------------------------------------        
#-----------------------------------------------    
    def grafoErrores(self, errores):
        nombreImagenSalida='grafos/errores.dot'
        
        escribir = open(nombreImagenSalida, 'w')
        escribir.write('digraph errores { \n')
        #escribir.write('rankdir=')
#------NODO principal---------------------------
        escribir.write('NodoErrores [shape=none, margin=0, label=<\n')
        escribir.write('<table border=\"0\" cellborder= \"1\">\n')
        escribir.write('<tr>\n')#[seDetecto,seLee,seEsperaba,Y,X,RazonError]
        escribir.write('<td>No. </td> <td>Tipo Error</td> <td>Se leyo</td> <td>Se esperaba...</td> <td>Linea(Y)</td> <td>Columna(X)</td> <td>DESCRIPCION</td>\n')
        escribir.write('</tr>\n')
        indice=0
        for error in errores:
            indice+=1
            escribir.write('<tr>\n')
            #lista=['(SINTACTICO)',caracter, '-, /, LETRA', fila, columna, 'Desface de caracter']
            escribir.write('<td>'+str(indice)+'</td> <td>'+str(error[0])+'</td> <td>'+str(error[1])+'</td> <td>'+str(error[2])+'</td> <td>'+str(error[3])+'</td> <td>'+str(error[4])+'</td> <td>'+str(error[5])+'</td>\n')
            escribir.write('</tr>\n')
        escribir.write('</table>>];\n')
#-----------------------------------------------
        escribir.write('}\n')
        escribir.close()
        
        render('dot', 'png', nombreImagenSalida)