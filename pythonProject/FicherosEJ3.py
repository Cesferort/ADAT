# -*- coding: utf-8 -*-
import csv
import lxml.etree as ET
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import cgi

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

class FicherosEJ3:
    def main(self):
        respuesta = 0
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input(
                "¿Qué deseas hacer?\n1. Crear XML de olimpiadas\n2. Crear XML de deportistas\n3. Listado de olimpiadas\n4. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 1 or respuesta > 4:
                    print("El número introducido escapa del rango (1-5)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.generarOlimpiadasXML()
        elif respuesta == 2:
            self.generarDeportistasXML()
        elif respuesta == 3:
            self.buscarListadoOlimpiadas()
        else:
            print("Programa Finalizado")

    def generarOlimpiadasXML(self):
        # Conseguir año mínimo y máximo
        anioMinimo = 3000
        anioMaximo = 0
        with open('olimpiadas.csv', newline='') as archivoEntrada:
            reader = csv.reader(archivoEntrada)
            headerTerminado = False
            for row in reader:
                if (headerTerminado == False):
                    headerTerminado = True
                else:
                    num = int(float(row[1]))
                    if (num > anioMaximo):
                        anioMaximo = num
                    elif (num < anioMinimo):
                        anioMinimo = num

        root = ET.Element('olimpiadas')
        anio = anioMinimo
        while (anio <= anioMaximo):
            temporada = "Winter"
            tempNum = 1
            while (tempNum <= 2):
                if (tempNum == 2):
                    temporada = "Summer"

                with open('olimpiadas.csv', newline='') as archivoEntrada:
                    reader = csv.reader(archivoEntrada)
                    headerTerminado = False
                    for row in reader:
                        if (headerTerminado == False):
                            headerTerminado = True
                        else:
                            if (anio == int(float(row[1])) and temporada == row[2]):
                                olimpiada = ET.SubElement(root, 'olimpiada')
                                olimpiada.set('year', row[1])
                                juegos = ET.SubElement(olimpiada, 'juegos')
                                juegos.text = row[0]
                                temporada = ET.SubElement(olimpiada, 'temporada')
                                temporada.text = row[2]
                                ciudad = ET.SubElement(olimpiada, 'ciudad')
                                ciudad.text = row[3]
                tempNum = tempNum + 1
            anio = anio + 1

        archivoSalida = open("olimpiadas.xml", "w")
        archivoSalida.write(ET.tostring(root, pretty_print=True).decode("utf-8"))
        archivoSalida.close()
        self.main()

    def generarDeportistasXML(self):
        root = ET.Element('deportistas')
        with open('athlete_events.csv', newline='') as archivoEntrada:
            reader = csv.reader(archivoEntrada)
            identificador = -1
            headerTerminado = False

            participaciones = "ParticipaciónRecipiente"
            for row in reader:
                if (headerTerminado == False):
                    headerTerminado = True
                else:
                    if (str(identificador) == row[0]):
                        # Nos encontramos en el mismo deportista
                        for deporte in participaciones.findall('deporte'):
                            if (deporte.get('nombre') == row[12]):
                                # Este deportista ya ha participado en ese deporte
                                participacion = ET.SubElement(deporte, 'participacion')
                                participacion.set('edad', row[3])
                                equipo = ET.SubElement(participacion, 'equipo')
                                equipo.text = row[11]
                                juegos = ET.SubElement(participacion, 'juegos')
                                juegos.text = row[8]
                                evento = ET.SubElement(participacion, 'evento')
                                evento.text = row[13]
                                if (row[14] != 'NA'):
                                    medalla = ET.SubElement(participacion, 'medalla')
                                    medalla.text = row[14]
                            else:
                                # Este deportista no ha participado en ese deporte
                                deporte = ET.SubElement(participaciones, 'deporte')
                                deporte.set('nombre', row[12])
                                participacion = ET.SubElement(deporte, 'participacion')
                                participacion.set('edad', row[3])
                                equipo = ET.SubElement(participacion, 'equipo')
                                equipo.text = row[11]
                                juegos = ET.SubElement(participacion, 'juegos')
                                juegos.text = row[8]
                                evento = ET.SubElement(participacion, 'evento')
                                evento.text = row[13]
                                if (row[14] != 'NA'):
                                    medalla = ET.SubElement(participacion, 'medalla')
                                    medalla.text = row[14]
                    else:
                        # Nos encontramos en otro nuevo deportista
                        identificador = row[0]
                        deportista = ET.SubElement(root, 'deportista')
                        deportista.set('id', row[0])
                        nombre = ET.SubElement(deportista, 'nombre')
                        nombre.text = row[1]
                        sexo = ET.SubElement(deportista, 'sexo')
                        sexo.text = row[2]
                        altura = ET.SubElement(deportista, 'altura')
                        altura.text = row[4]
                        peso = ET.SubElement(deportista, 'peso')
                        peso.text = row[5]
                        participaciones = ET.SubElement(deportista, 'participaciones')
                        deporte = ET.SubElement(participaciones, 'deporte')
                        deporte.set('nombre', row[12])
                        participacion = ET.SubElement(deporte, 'participacion')
                        participacion.set('edad', row[3])
                        equipo = ET.SubElement(participacion, 'equipo')
                        equipo.text = row[11]
                        juegos = ET.SubElement(participacion, 'juegos')
                        juegos.text = row[8]
                        evento = ET.SubElement(participacion, 'evento')
                        evento.text = row[13]
                        if (row[14] != 'NA'):
                            medalla = ET.SubElement(participacion, 'medalla')
                            medalla.text = row[14]
        archivoSalida = open("deportistas.xml", "w")
        archivoSalida.write(ET.tostring(root, pretty_print=True).decode("utf-8"))
        archivoSalida.close()
        self.main()

    def buscarListadoOlimpiadas(self):
        FormData = cgi.FieldStorage()
        parser = make_parser()
        handler = XMLHandler()
        parser.setContentHandler(handler)
        parser.parse(open('olimpiadas.xml'))
        self.main()

ej3 = FicherosEJ3()
ej3.main()