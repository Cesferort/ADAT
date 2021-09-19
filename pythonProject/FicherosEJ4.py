# -*- coding: utf-8 -*-
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import cgi
import pickle
import os

class Olimpiada():
    def __init__(self,anio,juegos,temporada,ciudad):
        self.anio = anio;
        self.juegos = juegos;
        self.temporada = temporada;
        self.ciudad = ciudad;
    def __str__(self):
        return "Año: " + self.anio + " Juegos: " + self.juegos + " Temporada: " + self.temporada + " Ciudad: " + self.ciudad

class XMLHandler(ContentHandler):
    def __init__(self):
        self.esGamesElement = False;
        self.esTemporadaElement = False;
        self.esCiudadElement = False;

    def startElement(self, name, attrs):
        if name == 'olimpiada':
            self.olimpiadaYear = attrs.get('year', "")
        elif name == 'juegos':
            self.olimpiadaGames = "";
            self.esGamesElement = True;
        elif name == 'temporada':
            self.olimpiadaTemporada = "";
            self.esTemporadaElement = True;
        elif name == 'ciudad':
            self.olimpiadaCiudad = "";
            self.esCiudadElement = True;
        return

    def characters(self, ch):
        if self.esGamesElement == True:
            self.olimpiadaGames += ch
        elif(self.esTemporadaElement == True):
            self.olimpiadaTemporada += ch
        elif(self.esCiudadElement == True):
            self.olimpiadaCiudad += ch

    def endElement(self, name):
        self.esGamesElement = False;
        self.esTemporadaElement = False;
        self.esCiudadElement = False;
        if name == 'olimpiada':
            olimpiada = Olimpiada(self.olimpiadaYear,self.olimpiadaGames,self.olimpiadaTemporada,self.olimpiadaCiudad);
            with open('archivoSerializado.olimpiadas', 'ab') as f:
                pickle.dump(olimpiada, f)

class FicherosEJ4:
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
            self.crearFichSerialOlimpiadas()
        elif respuesta == 2:
            self.aniadirEdicionOlimpica()
        elif respuesta == 3:
            self.buscarOlimpiada()
        elif respuesta == 4:
            self.eliminarEdicionOlimpica()
        else:
            print("Programa Finalizado")

    def crearFichSerialOlimpiadas(self):
        FormData = cgi.FieldStorage()
        parser = make_parser()
        handler = XMLHandler()
        parser.setContentHandler(handler)

        f = open('archivoSerializado.olimpiadas', 'wb')
        f.close();

        parser.parse(open('olimpiadas.xml'))
        self.main()

    def aniadirEdicionOlimpica(self):
        print("\n-- Introduce datos sobre la olimpiada --")
        olimpiadaYear = input("Año de celebración: ");
        olimpiadaGames = input("Juegos: ");
        olimpiadaTemporada = input("Temporada: ");
        olimpiadaCiudad = input("Ciudad: ");
        olimpiada = Olimpiada(olimpiadaYear,olimpiadaGames,olimpiadaTemporada,olimpiadaCiudad);
        with open('archivoSerializado.olimpiadas', 'ab') as f:
            pickle.dump(olimpiada, f)
        print()
        self.main()

    def buscarOlimpiada(self):
        ciudadABuscar = input("\nIntroduce nombre de la ciudad a buscar: ")
        with open('archivoSerializado.olimpiadas', 'rb') as f:
            while True:
                try:
                    olimpiada = pickle.load(f)
                    if(olimpiada.ciudad == ciudadABuscar):
                        print(olimpiada.__str__())
                except EOFError:
                    break
        print()
        self.main()

    def eliminarEdicionOlimpica(self):
        print("\n-- Introduce datos de la edición olímpica a eliminar --")
        anio = input("Año: ")
        temporada = input("Temporada: ")

        #Pasar a un fichero auxiliar las olimpiadas de interes
        with open('archivoSerializado.olimpiadas', 'rb') as fEntrada:
            olimpiadaEliminado = False;
            while True:
                try:
                    olimpiada = pickle.load(fEntrada)
                    if(olimpiada.anio != anio or olimpiada.temporada != temporada):
                        with open('archivoSerializado-aux.olimpiadas', 'ab') as fSalida:
                            pickle.dump(olimpiada, fSalida)
                    else:
                        olimpiadaEliminado = True;
                except EOFError:
                    break

        #Borrado del contenido original
        fOriginal = open('archivoSerializado.olimpiadas', 'wb')
        fOriginal.close()

        #Pasar información del archivo auxiliar al original
        with open('archivoSerializado-aux.olimpiadas', 'rb') as fEntrada:
            while True:
                try:
                    olimpiada = pickle.load(fEntrada)
                    with open('archivoSerializado.olimpiadas', 'ab') as fSalida:
                        pickle.dump(olimpiada, fSalida)
                except EOFError:
                    break

        #Eliminar archivo auxiliar
        os.remove("archivoSerializado-aux.olimpiadas")

        #Output final
        if(olimpiadaEliminado == False):
            print("\nNo se ha encontrado ninguna olimpiada con los datos establecidos.\n")
        else:
            print("\nEliminación completada correctamente.\n")
        self.main()

ej4 = FicherosEJ4()
ej4.main()