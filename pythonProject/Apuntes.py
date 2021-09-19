# -*- coding: utf-8 -*-
class Apuntes:
    def main(self):
        respuesta = 0
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input("¿Qué deseas hacer?\n1. Crear fichero serializable de olimpiadas\n2. Añadir edición olímpica\n3. Buscar olimpiadas por sede\n4. Eliminar edición olímpica\n5. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 1 or respuesta > 5:
                    print("El número introducido escapa del rango (1-5)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.ejercicio1()
        elif respuesta == 2:
            self.ejercicio2()
        elif respuesta == 3:
            self.ejercicio3()
        elif respuesta == 4:
            self.ejercicio4()
        else:
            print("Programa Finalizado")

    def ejercicio1(self):
        self.main()

    def ejercicio2(self):
        self.main()

    def ejercicio3(self):
        self.main()

    def ejercicio4(self):
        self.main()

examen = Apuntes()
examen.main()

#0-Manejo de Conectores
"""
query =  "SELECT Evento.nombre, Evento.id_evento "
query += "FROM Evento, Participacion "
query += "WHERE Evento.id_evento = Participacion.id_evento "
query += "AND " + self.comodin + " = id_deportista;"
self.cursor.execute(query, (deportista[1],))

eventos = {}
contEvento = 0
for row in self.cursor:
    eventos[contEvento] = (row[0], row[1])
    print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t-Evento: " + str(row[0]))
    contEvento += 1

eventoValido = False
while (eventoValido == False):
    try:
        numEvento = int(input("\nNúmero del evento deseado: "))
        if (numEvento < 0):
            print("Valores negativos no permitidos")
        elif (numEvento >= contEvento):
            print("El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(contEvento - 1))
        else:
            evento = eventos[numEvento]
            eventoValido = True
    except:
        eventoValido = False
"""

#1-Archivos
""" import os, shutil

Crear carpeta           --> os.makedirs(rutaDir + '/' + nombreDir)     

Diferenciar archivos de
carpetas                --> with os.scandir(rutaDir) as ficheros:
                                for fichero in ficheros:
                                    isFile = os.path.isfile(rutaDir+"/"+fichero.name)
                                    if isFile == True:
                                        print("\t"+fichero.name)
                                    else:
                                        print("DIR "+fichero.name)    
                                        
Copiar archivo          --> if not os.path.exists(rutaOriginal):
                                print("La ruta original no existe.")
                            else:
                                shutil.copyfile(rutaOriginal, rutaDestino)

Mover archivo           --> if not os.path.exists(rutaOriginal):
                                print("La ruta original no existe.")
                            else:
                                shutil.move(rutaOriginal, rutaDestino)

Eliminar              
- os.remove()           --> borra un archivo
- os.rmdir()            --> borra una carpeta VACÍA
- shutil.rmtree()       --> borra una carpeta Y SU CONTENIDO                            
                            if(os.path.exists(ruta)):
                                if(os.path.isfile(ruta) == True):
                                    os.remove(ruta)
                                    print("Archivo eliminado")
                                else:
                                    if not os.listdir(ruta):
                                        os.rmdir(ruta)
                                        print("Carpeta vacía eliminada")
                                    else:
                                        print("La carpeta no se pudo eliminar porque no está vacía")
                            else:
                                print("La ruta especificada no existe")
"""


#2-CSV
""" import csv

Leer CSV y crear CSV 
con fieldnames          --> archivoSalida = open('olimpiadas.csv', 'w')
                            with open('athlete_events.csv', newline='') as archivoEntrada:
                               reader = csv.reader(archivoEntrada)
                               fieldnames = ["Games", "Year", "Season", "City"]
                               writer = csv.DictWriter(archivoSalida, fieldnames=fieldnames)
                               for row in reader:
                                    writer.writerow(
                                    {
                                        "Games"     : row[8],
                                        "Year"      : row[9],
                                        "Season"    : row[10],
                                        "City"      : row[11]
                                    })
                            archivoSalida.close()
                                    
Append CSV              --> with open('athlete_events.csv', 'a') as archivoSalida:
                                writer = csv.writer(archivoSalida)
                                writer.writerow([str(id), str(nomDep), sexDep, edadDep, altDep, pesDep, equipoDep, nocDep, juegosDep, anioDep, tempDep, ciuDep, deporteDep, eventoDep, medallaDep])
"""


#3-XML
""" import csv
    import lxml.etree as ET
    from xml.sax import make_parser
    from xml.sax.handler import ContentHandler
    import cgi
    
Crear fichero XML a 
partir de CSV           --> root = ET.Element('olimpiadas')
                            with open('olimpiadas.csv', newline='') as archivoEntrada:
                                reader = csv.reader(archivoEntrada)
                                headerTerminado = False
                                for row in reader:
                                    if (headerTerminado == False):
                                        headerTerminado = True
                                    else:
                                        olimpiada = ET.SubElement(root, 'olimpiada')
                                        olimpiada.set('year', row[1])
                                        juegos = ET.SubElement(olimpiada, 'juegos')
                                        juegos.text = row[0]
                                        temporada = ET.SubElement(olimpiada, 'temporada')
                                        temporada.text = row[2]
                                        ciudad = ET.SubElement(olimpiada, 'ciudad')
                                        ciudad.text = row[3]
                            archivoSalida = open("olimpiadas.xml", "w")
                            archivoSalida.write(ET.tostring(root, pretty_print=True).decode("utf-8"))
                            archivoSalida.close()
                            
Listar subelementos     --> for deporte in participaciones.findall('deporte'):
                                if (deporte.get('nombre') == row[12]):
                                    participacion = ET.SubElement(deporte, 'participacion')
                                    
SAX Parser              --> def buscarListadoOlimpiadas(self):
                                FormData = cgi.FieldStorage()
                                parser = make_parser()
                                handler = XMLHandler()
                                parser.setContentHandler(handler)
                                parser.parse(open('olimpiadas.xml'))
                                self.main()
                            
                            class XMLHandler(ContentHandler):
                                def __init__(self):
                                    self.n = 0;
                                    self.esGamesElement = False;
                            
                                def startElement(self, name, attrs):
                                    if name == 'olimpiada':
                                        self.olimpiadaYear = attrs.get('year', "")
                                    elif name == 'juegos':
                                        self.olimpiadaGames = "";
                                        self.esGamesElement = True;
                                    return
                            
                                def characters(self, ch):
                                    if self.esGamesElement == True:
                                        self.olimpiadaGames += ch
                            
                                def endElement(self, name):
                                    self.esGamesElement = False;
                                    if name == 'olimpiada':
                                        self.n = self.n + 1;
                                        print("Olimpiada Número " + str(self.n))
                                        print("Juegos: " + self.olimpiadaGames + "\nAño: " + self.olimpiadaYear + "\n")
"""


#4-Binario de objetos
""" from xml.sax import make_parser
    from xml.sax.handler import ContentHandler
    import cgi
    import pickle
    import os

Clase objeto            --> class Olimpiada():
                                def __init__(self,anio,juegos,temporada,ciudad):
                                    self.anio = anio;
                                    self.juegos = juegos;
                                    self.temporada = temporada;
                                    self.ciudad = ciudad;
                                def __str__(self):
                                    return "Año: " + self.anio + " Juegos: " + self.juegos + " Temporada: " + self.temporada + " Ciudad: " + self.ciudad
        
Añadir objeto           --> olimpiada = Olimpiada(olimpiadaYear,olimpiadaGames,olimpiadaTemporada,olimpiadaCiudad);
                            with open('archivoSerializado.olimpiadas', 'ab') as f:
                                pickle.dump(olimpiada, f)
                                
Buscar objeto           --> ciudadABuscar = input("\nIntroduce nombre de la ciudad a buscar: ")
                            with open('archivoSerializado.olimpiadas', 'rb') as f:
                                while True:
                                    try:
                                        olimpiada = pickle.load(f)
                                        if(olimpiada.ciudad == ciudadABuscar):
                                            print(olimpiada.__str__())
                                    except EOFError:
                                        break
"""


#5-Apuntes adicionales
"""
id = int(float(row[0]))

Contiene texto          --> if ("patata".upper().__contains__("pATA".upper())):
                                print("Bien")
                            else:
                                print("Mal")

Castear                 --> edad = int(input("Edad: "))
                            texto = str(edad)

Validación              --> pesDep = -1
                            while (pesDep < 0 or pesDep > 1000):
                                try:
                                    pesDep = int(input("Peso: "))
                                except:
                                    pesDep = -1
"""