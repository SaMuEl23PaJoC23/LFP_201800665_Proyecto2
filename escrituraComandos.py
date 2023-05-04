class escritura():
    def escrituraComandosMongoDB(self, funciones):
        i=0
        texto=''
        while i < len(funciones):
            funcionActual=funciones[i].lower()
            if funcionActual !="crearbd" and funcionActual !='eliminarbd':
                nombreColeccion=funciones[i+1][1]
            
            if  funcionActual == 'crearbd':
                texto+='use(\''+str(funciones[i+1][0])+'\');\n'    
            
            
            elif funcionActual == 'eliminarbd':
                texto+='db.dropDatabase();\n'
            
                
            elif funcionActual == 'crearcoleccion':
                texto+='db.createCollection(\''+nombreColeccion+'\');\n'
            
                
            elif funcionActual == 'eliminarcoleccion':
                texto+='db.'+nombreColeccion+'.drop();\n'
            
                
            elif funcionActual == 'insertarunico':
                Json='\n{\n'
                datosJSON=funciones[i+1][2]
                j=0
                while j < len(datosJSON):
                    Json+='\t\"'+datosJSON[j]+'\": \"'+datosJSON[j+1]+'\"'
                    j+=2
                    if j < len(datosJSON):
                        Json+=',\n'
                Json+='\n}'

                texto+='db.'+nombreColeccion+'.insertOne('+Json+');\n'
             
                
            elif funciones[i].lower() == 'actualizarunico':
                Json='\n{\n'
                datosJSON=funciones[i+1][2]
                j=0
                while j < len(datosJSON):
                    Json+='\t\"'+datosJSON[j]+'\": \"'+datosJSON[j+1]+'\"'
                    j+=2
                    if j < len(datosJSON):
                        Json+=',\n'
                        if datosJSON[j] == '$':
                            j+=1
                Json+='\n}'

                texto+='db.'+nombreColeccion+'.updateOne('+Json+');\n'
                
            
            elif funciones[i].lower() == 'eliminarunico':
                Json='\n{\n'
                datosJSON=funciones[i+1][2]
                j=0
                while j < len(datosJSON):
                    Json+='\t\"'+datosJSON[j]+'\": \"'+datosJSON[j+1]+'\"'
                    j+=2
                    if j < len(datosJSON):
                        Json+=',\n'
                Json+='\n}'

                texto+='db.'+nombreColeccion+'.deleteOne('+Json+');\n'
            
            
            elif funciones[i].lower() == 'buscartodo':
                texto+='db.'+nombreColeccion+'.find();\n'
            
            
            elif funciones[i].lower() == 'buscarunico':
                texto+='db.'+nombreColeccion+'.findOne();\n'
                
            i+=2
            
        return texto