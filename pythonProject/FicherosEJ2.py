# -*- coding: utf-8 -*-
import csv

class FicherosEJ2:
    def main(self):
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input("¿Qué deseas hacer?\n1. Generar fichero CSV\n2. Buscar deportista\n3. Buscar deportistas por deporte y olimpiada\n4. Añadir deportista\n5. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 1 or respuesta > 5:
                    print("El número introducido escapa del rango (1-5)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.generarCSV()
        elif respuesta == 2:
            self.buscarDeportista()
        elif respuesta == 3:
            self.buscarDeportista_DepOli()
        elif respuesta == 4:
            self.aniadirDeportista()
        else:
            print("Programa Finalizado")

    def generarCSV(self):
        archivoSalida = open('olimpiadas.csv', 'w')
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
        print("Archivo generado\n")
        self.main()

    def buscarDeportista(self):
        deportistaEncontrado = False
        nomBuscar = input("Introduce nombre a buscar: ")
        with open('athlete_events.csv', newline='') as archivoEntrada:
            reader = csv.reader(archivoEntrada)
            for row in reader:
                if(row[1] == nomBuscar):
                    print(row)
                    deportistaEncontrado = True
        if (deportistaEncontrado == False):
            print("No se ha encontrado ningún deportista con este nombre")
        print()
        self.main()

    def buscarDeportista_DepOli(self):
        deportistaEncontrado = False
        deporteBuscar = input("Introduce nombre del deporte a buscar: ")
        anioBuscar = input("Introduce año a buscar: ")
        temporadaBuscar = input("Introduce temporada del año a buscar: ")

        print("\n"+anioBuscar+temporadaBuscar+ " - "+deporteBuscar+":")
        with open('athlete_events.csv', newline='') as archivoEntrada:
            reader = csv.reader(archivoEntrada)
            numDeportista = 1
            for row in reader:
                if( row[12] == deporteBuscar
                and row[9] == anioBuscar
                and row[10] == temporadaBuscar ):
                    print(str(numDeportista)+". "+row[1]+" EVENTO: "+row[13]+" MEDALLA: "+row[14])
                    numDeportista = numDeportista + 1
                    deportistaEncontrado = True
        if (deportistaEncontrado == False):
            print("No se ha encontrado ningún deportista que cumpla estas características\n")
        self.main()

    def aniadirDeportista(self):
        print("Introduce datos sobre el deportista a insertar")
        nomDep = input("Nombre: ")
        sexDep = input("Sexo: ")
        while (sexDep != "F" and sexDep != "M" and
               sexDep != "f" and sexDep != "m"):
            sexDep = input("Respuesta no válida, vuelve a intentarlo.\nLos valores permitidos son M y F\nSexo: ")

        edadDep = -1
        while (edadDep < 0 or edadDep > 200):
            try:
                edadDep = int(input("Edad: "))
            except:
                edadDep = -1

        altDep = -1
        while (altDep < 0 or altDep > 500):
            try:
                altDep = int(input("Altura: "))
            except:
                altDep = -1

        pesDep = -1
        while (pesDep < 0 or pesDep > 1000):
            try:
                pesDep = int(input("Peso: "))
            except:
                pesDep = -1

        equipoDep = input("Equipo: ")
        nocDep = input("NOC: ")
        juegosDep = input("Juego en el que ha participado: ")
        anioDep = input("Año de participación: ")
        tempDep = input("Temporada: ")
        ciuDep = input("Ciudad: ")
        deporteDep = input("Deporte: ")
        eventoDep = input("Evento: ")

        checkMedallaDep = input("¿Consiguió una medalla? S/N ")
        while(checkMedallaDep != "S" and checkMedallaDep != "s" and
              checkMedallaDep != "N" and checkMedallaDep != "n" ):
            checkMedallaDep = input("Resputa no válida, vuelve a intentarlo.\n¿Consiguió una medalla? S/N ")
        if(checkMedallaDep == "S" or checkMedallaDep == "s"):
            medallaDep = input("¿Qué medalla consiguió? ")
        else:
            medallaDep = "NA"

        id = 0
        with open('athlete_events.csv', newline='') as archivoEntrada:
            reader = csv.reader(archivoEntrada)
            primeraLinea = True
            for row in reader:
                 try:
                     if(primeraLinea == True):
                         primeraLinea = False
                     else:
                         id = int(float(row[0]))
                 except:
                     print("Valor no numérico encontrado en el campo ID del deportista encontrado")
        id = id + 1

        with open('athlete_events.csv', 'a') as archivoSalida:
            writer = csv.writer(archivoSalida)
            writer.writerow([str(id), str(nomDep), sexDep, edadDep, altDep, pesDep, equipoDep, nocDep, juegosDep, anioDep, tempDep, ciuDep, deporteDep, eventoDep, medallaDep])

        self.main()

ej2 = FicherosEJ2()
ej2.main()