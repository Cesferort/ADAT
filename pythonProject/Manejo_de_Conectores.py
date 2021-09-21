# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode
import os
import csv
import sqlite3

class Manejo_de_Conectores:
    def main(self):
        respuesta = -1
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input("¿Qué deseas hacer?\n1. Crear BBDD MySQL\n2. Crear BBDD SQLite\n3. Listar deportistas en diferentes deportes\n4. Listar deportistas participantes\n5. Modificar medalla\n6. Añadir deportista/participación\n7. Eliminar participación\n0. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 0 or respuesta > 7:
                    print("El número introducido escapa del rango (0-7)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.crearBBDD(1)
        elif respuesta == 2:
            self.crearBBDD(2)
        elif respuesta == 3:
            self.deportistasDifDeportes()
        elif respuesta == 4:
            self.deportistasParticipantes()
        elif respuesta == 5:
            self.modificarMedalla()
        elif respuesta == 6:
            self.aniadirParticipacion()
        elif respuesta == 7:
            self.eliminarParticipacion()
        else:
            print("Programa Finalizado")

    def vaciarBBDDMysql(self, cursor, con):
        tablasABorrar = {}
        tablasABorrar['Participacion']  = "DROP TABLE IF EXISTS Participacion"
        tablasABorrar['Evento']         = "DROP TABLE IF EXISTS Evento"
        tablasABorrar['Olimpiada']      = "DROP TABLE IF EXISTS Olimpiada"
        tablasABorrar['Deporte']        = "DROP TABLE IF EXISTS Deporte"
        tablasABorrar['Deportista']     = "DROP TABLE IF EXISTS Deportista"
        tablasABorrar['Equipo']         = "DROP TABLE IF EXISTS Equipo"

        for numQuery in tablasABorrar:
            query = tablasABorrar[numQuery]
            cursor.execute(query)
        con.commit()

    def crearTablas(self, cursor, con, check):
        if(check == 1):
            with open('olimpiadas.sql', 'r') as fSQL:
                fSQLString = fSQL.read()
                var = cursor.execute(fSQLString, multi=True)
                for x in var:
                    if x.with_rows:
                        x.fetchall()
        else:
            with open('olimpiadas-lite.sql', 'r') as fSQL:
                fSQLString = fSQL.read()
                cursor.executescript(fSQLString)
        con.commit()

    def crearConexion(self):
        # Preguntamos por base de datos a utilizar y validamos
        check = -1
        primeraVez = True
        while check != 1 and check != 2:
            try:
                if (primeraVez == True):
                    primeraVez = False
                    check = int(input("¿Cúal será la base de datos a utilizar?\n1 - MySQL\n2 - SQLite\n"))
                else:
                    check = int(input("Valor introducido no permitido. Vuelve a intentarlo:\n¿Cúal será la base de datos a utilizar?\n1 - MySQL\n2 - SQLite\n"))
            except:
                check = -1

        # Conectamos a la base de datos escogida
        if check == 1:
            self.con = mysql.connector.connect(
                user='usuOlimpiadas',
                password='dm2',
                host='127.0.0.1',
                database='olimpiadas'
            )
            self.cursor = self.con.cursor(buffered=True)
            self.comodin = "%s"
        elif check == 2:
            self.con = sqlite3.connect("olimpiadas.db")
            self.cursor = self.con.cursor()
            self.comodin = "?"

    def crearBBDD(self, check):
        finalizadoCorrectamente = False
        try:
            if(check == 1):
                self.con = mysql.connector.connect  (
                                                        user='usuOlimpiadas',
                                                        password='dm2',
                                                        host='127.0.0.1',
                                                        database='olimpiadas'
                                                    )

                self.cursor = self.con.cursor(buffered=True)
                comodin = "%s"
            else:
                self.con = sqlite3.connect("olimpiadas.db")
                self.cursor = self.con.cursor()
                comodin = "?"

            try:
                self.vaciarBBDDMysql(self.cursor, self.con)
                print("Base de datos vaciada correctamente.")
                try:
                    self.crearTablas(self.cursor, self.con, check)
                    print("Estructura de la base de datos creada correctamente.")
                except:
                    print("No se ha podido crear la estructura de la base de datos.")
            except:
                print("No se ha podido vaciar la base de datos.")

            # Pedir fichero CSV
            dirFich = input("Introduce dirección del csv con toda la información a insertar: ")

            if not os.path.exists(dirFich):
                print("La dirección de archivo especificada no existe.")
            else:
                print("Accediendo al archivo csv...")
                with open(dirFich, newline='') as archivoEntrada:
                    headerTerminado = False
                    reader = csv.reader(archivoEntrada)

                    deportistas = {}
                    participaciones = {}
                    olimpiadas = {}
                    deportes = {}
                    eventos = {}
                    equipos = {}

                    ai_olimpiadas = 1
                    ai_deportes = 1
                    ai_eventos = 1
                    ai_equipos = 1

                    pk_deportista = 0
                    pk_olimpiadas = 0
                    pk_deportes = 0
                    pk_eventos = 0
                    pk_equipos = 0

                    for row in reader:
                        if(headerTerminado == True):
                            """Datos Deportista:                            
                            idDep = row[0]
                            nomDep = row[1]
                            sexDep = row[2]
                            pesDep = row[5]
                            altDep = row[4]
                            """
                            pk_deportista = row[0]
                            if not row[0] in deportistas:
                                sexDep = row[2] if(not row[2] == 'NA') else 'F'
                                altDep = row[4] if(not row[4] == 'NA') else 0
                                pesDep = row[5] if(not row[5] == 'NA') else 0
                                deportistas[row[0]] = (row[0], row[1], sexDep, pesDep, altDep)

                            """Datos Equipo:                           
                            idEquipo es un autoincremental
                            nomEquipo = row[6]
                            iniEquipo = row[7]
                            """
                            if not row[6] in equipos:
                                equipos[row[6]] = (ai_equipos, row[6], row[7])
                                pk_equipos = ai_equipos
                                ai_equipos = ai_equipos + 1
                            else:
                                pk_equipos = equipos[row[6]][0]

                            """Datos Olimpiada:                            
                            idOlimpiada es un autoincremental
                            nomOlimpiada = row[8]
                            anioOlimpiada = row[9]
                            tempOlimpiada = row[10]
                            ciuOlimpiada = row[11]
                            """
                            if not row[8] in olimpiadas:
                                olimpiadas[row[8]] = (ai_olimpiadas, row[8], row[9], row[10], row[11])
                                pk_olimpiadas = ai_olimpiadas
                                ai_olimpiadas = ai_olimpiadas + 1
                            else:
                                pk_olimpiadas = olimpiadas[row[8]][0]

                            """Datos Deporte:
                            idDeporte es un autoincremental
                            nomDeporte = row[12]
                            """
                            if not row[12] in deportes:
                                deportes[row[12]] = (ai_deportes, row[12])
                                pk_deportes = ai_deportes
                                ai_deportes = ai_deportes + 1
                            else:
                                pk_deportes = deportes[row[12]][0]

                            """Datos Evento:
                            idEvento es un autoincremental
                            nomEvento = row[13]
                            idOlimpiada clave ajena
                            idDeporte clave ajena
                            """
                            if not row[13] in eventos:
                                eventos[row[13]] = (ai_eventos, row[13], pk_olimpiadas, pk_deportes)
                                pk_eventos = ai_eventos
                                ai_eventos = ai_eventos + 1
                            else:
                                pk_eventos = eventos[row[13]][0]

                            """Datos Participacion:
                            idDeportista clave ajena
                            idEvento clave ajena
                            idEquipo clave ajena
                            edadParticipacion = row[3]
                            medaParticipacion = row[14]
                            """
                            idParticipacion = str(pk_deportista)+"-"+str(pk_eventos)
                            if not idParticipacion in participaciones:
                                participaciones[idParticipacion] = (pk_deportista, pk_eventos, pk_equipos, row[3], row[14])
                        else:
                            headerTerminado = True;

                    # Inserción de deportistas
                    query = "INSERT INTO `Deportista` (`id_deportista`, `nombre`, `sexo`, `peso`, `altura`) VALUES"
                    query += " ("+comodin+", "+comodin+", "+comodin+", "+comodin+", "+comodin+");"
                    list_deportistas = deportistas.values()
                    self.cursor.executemany(query, list_deportistas)

                    # Inserción de equipos
                    query = "INSERT INTO `Equipo` (`id_equipo`, `nombre`, `iniciales`) VALUES"
                    query += " (" + comodin + ", " + comodin + ", " + comodin + ");"
                    list_equipos = equipos.values()
                    self.cursor.executemany(query, list_equipos)

                    # Inserción de olimpiadas
                    query = "INSERT INTO `Olimpiada` (`id_olimpiada`, `nombre`, `anio`, `temporada`, `ciudad`) VALUES"
                    query += " (" + comodin + ", " + comodin + ", " + comodin + ", "+ comodin + ", "+ comodin + ");"
                    list_olimpiadas = olimpiadas.values()
                    self.cursor.executemany(query, list_olimpiadas)

                    # Inserción de deportes
                    query = "INSERT INTO `Deporte` (`id_deporte`, `nombre`) VALUES"
                    query += " (" + comodin + ", " + comodin + ");"
                    list_deportes = deportes.values()
                    self.cursor.executemany(query, list_deportes)

                    # Inserción de eventos
                    query = "INSERT INTO `Evento` (`id_evento`, `nombre`, `id_olimpiada`, `id_deporte`) VALUES"
                    query += " (" + comodin + ", " + comodin + ", " + comodin + ", " + comodin + ");"
                    list_eventos = eventos.values()
                    self.cursor.executemany(query, list_eventos)

                    # Inserción de participaciones
                    query = "INSERT INTO `Participacion` (`id_deportista`, `id_evento`, `id_equipo`, `edad`, `medalla`) VALUES"
                    query += " (" + comodin + ", " + comodin + ", " + comodin + ", " + comodin + ", " + comodin + ");"
                    list_participaciones = participaciones.values()
                    self.cursor.executemany(query, list_participaciones)

                    finalizadoCorrectamente = True

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Nombre de usuario o contraseña incorrectos.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe.")
            else:
                print("Ha ocurrido un error en la inserción de datos.")

        if(finalizadoCorrectamente == True):
            print("Creación de Base de datos terminada correctamente.")
        else:
            try:
                print("La ejecución no ha podido completarse. Debido a ello la base de datos será vaciada.")
                self.vaciarBBDDMysql(self.cursor, self.con)
                print("Base de datos vaciada correctamente.")
            except:
                print("No se ha podido vaciar la base de datos.")

        # Cierre del cursor y del conector
        self.con.commit()
        self.cursor.close()
        self.con.close()

        print()
        self.main()

    def deportistasDifDeportes(self):
        self.crearConexion()

        query = """
                    SELECT  Deportista.nombre, sexo, altura, peso,
                            Deporte.nombre,
                            Participacion.edad, 
                            Evento.nombre,
                            Equipo.nombre,
                            Olimpiada.nombre,
                            Participacion.medalla
                    FROM Deportista, Participacion, Evento, Deporte, Equipo, Olimpiada
                    WHERE Deportista.id_deportista = Participacion.id_deportista
                    AND Evento.id_evento = Participacion.id_evento
                    AND Deporte.id_deporte = Evento.id_deporte
                    AND Equipo.id_equipo = Participacion.id_equipo
                    AND Olimpiada.id_olimpiada = Evento.id_olimpiada
                    AND 1 < 
                    (
                        SELECT count(Distinct Evento.id_deporte)
                        FROM Participacion, Evento
                        WHERE Participacion.id_evento = Evento.id_evento 
                        AND Deportista.id_deportista = Participacion.id_deportista
                    );                    
                """
        self.cursor.execute(query)

        cont = 1
        for row in self.cursor:
            print("\n" + str(cont) + ".\nDatos personales:\n\t-Nombre:" + str(row[0]) + "\n\t-Sexo:" + str(row[1]) + "\n\t-Altura:" + str(row[2]) + "\n\t-Peso:" + str(row[3]))
            print("Datos olímpicos:\n\t-Deporte:" + str(row[4]) + "\n\t-Edad:" + str(row[5]) + "\n\t-Evento:" + str(row[6]) + "\n\t-Equipo:" + str(row[7]) + "\n\t-Juegos:" + str(row[8]) + "\n\t-Medalla:" + str(row[9]))
            cont = cont + 1

        #Cierre del conector y del cursor
        self.cursor.close()
        self.con.close()

        print()
        self.main()

    def deportistasParticipantes(self):
        self.crearConexion()

        #Pedimos una temporada
        temporada = input("Introduce temporada Winter o Summer (W/S)\n")
        while(temporada.upper() != "W" and temporada.upper() != "S"):
            temporada = input("Valor introducido no permitido. Vuelve a intentarlo:\nIntroduce temporada Winter o Summer (W/S)\n")
        if(temporada.upper()=="W"):
            temporada = "Winter"
        else:
            temporada = "Summer"

        #Seleccionamos información de las olimpiadas celebradas en la temporada escogida
        query =  "SELECT nombre, id_olimpiada "
        query += "FROM Olimpiada "
        query += "WHERE " + self.comodin + " = temporada "
        query += "ORDER BY nombre;"
        self.cursor.execute(query, (temporada,))

        #Guardamos estas ediciones dentro de un diccionario y visualizamos el
        #identificador que nos permite acceder a cada edición dentro del diccionario
        #al usuario para que este pueda escoger la edición que desea
        ediciones = {}
        contEdicion = 0
        for row in self.cursor:
            print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica:" + str(row[0]))
            ediciones[contEdicion] = (row[0], row[1])
            contEdicion += 1

        #El usuario escoge una edición válida del diccionario
        edicionValida = False
        while(edicionValida == False):
            try:
                numEdicion = int(input("\nNúmero de la edición deseada:"))
                if(numEdicion < 0):
                    print("Valores negativos no permitidos")
                elif(numEdicion >= contEdicion):
                    print("El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(contEdicion-1))
                else:
                    edicion = ediciones[numEdicion]
                    edicionValida = True
            except:
                edicionValida = False

        #Seleccionamos todos los deportes celebrados en la edición escogida
        print("Estos son todos los deportes celebrados en la edición " + edicion[0] + ":")
        query =  "SELECT Deporte.nombre, Deporte.id_deporte "
        query += "FROM Evento, Deporte "
        query += "WHERE Evento.id_deporte = Deporte.id_deporte "
        query += "AND " + self.comodin + " = id_olimpiada "
        query += "GROUP BY Deporte.id_deporte "
        query += "ORDER BY Deporte.nombre;"
        self.cursor.execute(query, (edicion[1],))

        #Guardamos en un diccionario todos los deportes y mostramos al usuario el
        #identificador que podrá utilizar para escoger el deporte que más desee
        deportes = {}
        contDeporte = 0
        for row in self.cursor:
            print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row[0]))
            deportes[contDeporte] = (row[0], row[1])
            contDeporte += 1

        #El usuario escoge un deporte válido
        deporteValido = False
        while (deporteValido == False):
            try:
                numDeporte = int(input("\nNúmero del deporte deseado:"))
                if (numDeporte < 0):
                    print("Valores negativos no permitidos")
                elif (numDeporte >= contDeporte):
                    print("El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(contDeporte - 1))
                else:
                    deporte = deportes[numDeporte]
                    deporteValido = True
            except:
                deporteValido = False

        #Seleccionamos todos los eventos celebrados en la edición y deporte escogidos
        print("Estos son todos los eventos celebrados en el deporte " + deporte[0] + ":")
        query =  "SELECT nombre, id_evento "
        query += "FROM Evento "
        query += "WHERE " + self.comodin + " = id_deporte "
        query += "AND " + self.comodin + " = id_olimpiada;"
        self.cursor.execute(query, (deporte[1], edicion[1]))

        #Primera parte del resultado final
        nom_evento = ""
        id_evento = ""
        for row in self.cursor:
            nom_evento = row[0]
            id_evento = row[1]
        print("-- Resumen --\nTemporada: " + temporada + "\nEdición Olímpica: " + edicion[0] + "\nDeporte: " + deporte[0])
        print("Evento: " + nom_evento)

        #Seleccionamos a los deportistas participantes en ese evento
        print("Deportistas participantes:")
        query =  "SELECT Deportista.nombre, altura, peso, edad, Equipo.nombre, medalla "
        query += "FROM Participacion, Deportista, Equipo "
        query += "WHERE " + self.comodin + " = id_evento "
        query += "AND Participacion.id_deportista = Deportista.id_deportista "
        query += "AND Participacion.id_equipo = Equipo.id_equipo "
        query += "ORDER BY Deportista.nombre;"
        self.cursor.execute(query, (id_evento,))

        #Segunda parte del resultado final
        contResultDep = 1
        for row in self.cursor:
            print(str(contResultDep) + ". " + str(row[0]) + "\n\t-Altura:" + str(row[1]) + "\n\t-Peso:" + str(row[2]) + "\n\t-Edad:" + str(row[3]) + "\n\t-Equipo:" + str(row[4]) + "\n\t-Medalla:" + str(row[5]) + "\n")
            contResultDep += 1

        #Cierre del conector y del cursor
        self.cursor.close()
        self.con.close()

        print()
        self.main()

    def modificarMedalla(self):
        self.crearConexion()

        texto = input("Introduce texto a buscar en tabla deportista: ")
        query =  "SELECT nombre, id_deportista "
        query += "FROM Deportista;"
        self.cursor.execute(query)

        deportistas = {}
        contDeportista = 0
        for row in self.cursor:
            if(row[0].upper().__contains__(texto.upper())):
                deportistas[contDeportista] = (row[0], row[1])
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t-Deportista: " + str(row[0]))
                contDeportista += 1

        deportistaValido = False
        while (deportistaValido == False):
            try:
                numDeportista = int(input("\nNúmero del deportista deseado: "))
                if (numDeportista < 0):
                    print("Valores negativos no permitidos")
                elif (numDeportista >= contDeportista):
                    print("El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(contDeportista - 1))
                else:
                    deportista = deportistas[numDeportista]
                    deportistaValido = True
            except:
                deportistaValido = False

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

        medalla = input("Introduce nueva información para el campo medalla del deportista y evento seleccionado: ")
        medallaValida = False
        while(medallaValida == False):
            if(     medalla.upper() != "NA"
                and medalla.upper() != "BRONZE"
                and medalla.upper() != "SILVER"
                and medalla.upper() != "GOLD"):
                print("Valor no permitido, vuelve a intentarlo. Los valores permitidos son: NA, Bronze, Silver y Gold.")
                medalla = input(
                    "Introduce nueva información para el campo medalla del deportista y evento seleccionado: ")
            else:
                medallaValida = True

        query =  "UPDATE Participacion "
        query += "SET medalla = " + self.comodin + " "
        query += "WHERE " + self.comodin + " = id_deportista "
        query += "AND " + self.comodin + " = id_evento;"
        self.cursor.execute(query, (medalla, deportista[1], evento[1]))

        #Cierre del conector y del cursor
        self.con.commit()
        self.cursor.close()
        self.con.close()

        print("Actualización terminada correctamente\n")
        self.main()

    def aniadirParticipacion(self):
        self.crearConexion()

        nomDeportista = input("Introduce texto a buscar en tabla deportista: ")
        query = "SELECT nombre, id_deportista "
        query += "FROM Deportista;"
        self.cursor.execute(query)

        deportistas = {}
        contDeportista = 0
        for row in self.cursor:
            if (row[0].upper().__contains__(nomDeportista.upper())):
                deportistas[contDeportista] = (row[0], row[1])
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t-Deportista: " + str(row[0]))
                contDeportista += 1

        if contDeportista == 0:
            print("\nDeportista no encontrado.\nInsertando nuevo deportista en la tabla...\n")
            query =  "SELECT max(id_deportista) "
            query += "FROM Deportista;"
            self.cursor.execute(query)
            for row in self.cursor:
                idDeportista = 1 + int(row[0])

            sexoValido = False
            while sexoValido == False:
                sexo = input("Introduce sexo del nuevo deportista: ")
                if(sexo.upper() != "M" and sexo.upper() != "F"):
                    print("Sexo no permitido.\nValores aceptados: M, F")
                else:
                    sexoValido = True

            pesoValido = False
            while pesoValido == False:
                try:
                    peso = int(input("Introduce peso del nuevo deportista: "))
                    if(peso < 0):
                        print("Valor negativo no permitido")
                    elif(peso > 1000):
                        print("Valor demasiado alto")
                    else:
                        pesoValido = True
                except:
                    pesoValido = False

            alturaValida = False
            while alturaValida == False:
                try:
                    altura = int(input("Introduce altura del nuevo deportista: "))
                    if (altura < 0):
                        print("Valor negativo no permitido")
                    elif (altura > 500):
                        print("Valor demasiado alto")
                    else:
                        alturaValida = True
                except:
                    alturaValida = False

            #Insertar deportista
            query =  "INSERT INTO Deportista (id_deportista, nombre, sexo, peso, altura) "
            query += "VALUES (" + self.comodin + ", " + self.comodin + ", " + self.comodin + ", " + self.comodin + ", " + self.comodin + ");"
            self.cursor.execute(query, ((str(idDeportista)), nomDeportista, sexo, peso, altura))
            self.con.commit()
            print("Deportista insertado\n")
        else:
            deportistaValido = False
            while (deportistaValido == False):
                try:
                    numDeportista = int(input("\nNúmero del deportista deseado: "))
                    if (numDeportista < 0):
                        print("Valores negativos no permitidos")
                    elif (numDeportista >= contDeportista):
                        print(
                            "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                                contDeportista - 1))
                    else:
                        deportista = deportistas[numDeportista]
                        deportistaValido = True
                except:
                    deportistaValido = False
            idDeportista = deportista[1]

        # Pedimos una temporada
        temporada = input("Introduce temporada Winter o Summer (W/S)\n")
        while (temporada.upper() != "W" and temporada.upper() != "S"):
            temporada = input("Valor introducido no permitido. Vuelve a intentarlo:\nIntroduce temporada Winter o Summer (W/S)\n")
        if (temporada.upper() == "W"):
            temporada = "Winter"
        else:
            temporada = "Summer"

        # Seleccionamos información de las olimpiadas celebradas en la temporada escogida
        query = "SELECT nombre, id_olimpiada "
        query += "FROM Olimpiada "
        query += "WHERE " + self.comodin + " = temporada "
        query += "ORDER BY nombre;"
        self.cursor.execute(query, (temporada,))

        # Guardamos estas ediciones dentro de un diccionario y visualizamos el
        # identificador que nos permite acceder a cada edición dentro del diccionario
        # para que el usuario pueda escoger la edición que desea
        ediciones = {}
        contEdicion = 0
        for row in self.cursor:
            print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica:" + str(row[0]))
            ediciones[contEdicion] = (row[0], row[1])
            contEdicion += 1

        # El usuario escoge una edición válida del diccionario
        edicionValida = False
        while (edicionValida == False):
            try:
                numEdicion = int(input("\nNúmero de la edición deseada:"))
                if (numEdicion < 0):
                    print("Valores negativos no permitidos")
                elif (numEdicion >= contEdicion):
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contEdicion - 1))
                else:
                    edicion = ediciones[numEdicion]
                    edicionValida = True
            except:
                edicionValida = False

        # Seleccionamos todos los deportes celebrados en la edición escogida
        print("Estos son todos los deportes celebrados en la edición " + edicion[0] + ":")
        query = "SELECT Deporte.nombre, Deporte.id_deporte "
        query += "FROM Evento, Deporte "
        query += "WHERE Evento.id_deporte = Deporte.id_deporte "
        query += "AND " + self.comodin + " = id_olimpiada "
        query += "GROUP BY Deporte.id_deporte "
        query += "ORDER BY Deporte.nombre;"
        self.cursor.execute(query, (edicion[1],))

        # Guardamos en un diccionario todos los deportes y mostramos al usuario el
        # identificador que podrá utilizar para escoger el deporte que más desee
        deportes = {}
        contDeporte = 0
        for row in self.cursor:
            print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t-Deporte:" + str(row[0]))
            deportes[contDeporte] = (row[0], row[1])
            contDeporte += 1

        # El usuario escoge un deporte válido
        deporteValido = False
        while (deporteValido == False):
            try:
                numDeporte = int(input("\nNúmero del deporte deseado:"))
                if (numDeporte < 0):
                    print("Valores negativos no permitidos")
                elif (numDeporte >= contDeporte):
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contDeporte - 1))
                else:
                    deporte = deportes[numDeporte]
                    deporteValido = True
            except:
                deporteValido = False

        # Seleccionamos todos los eventos celebrados en la edición y deporte escogidos
        print("Estos son todos los eventos celebrados en el deporte " + deporte[0] + ":")
        query = "SELECT nombre, id_evento "
        query += "FROM Evento "
        query += "WHERE " + self.comodin + " = id_deporte "
        query += "AND " + self.comodin + " = id_olimpiada;"
        self.cursor.execute(query, (deporte[1], edicion[1]))

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
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contEvento - 1))
                else:
                    evento = eventos[numEvento]
                    eventoValido = True
            except:
                eventoValido = False

        idEvento = evento[1]

        medalla = input("Introduce información para el campo medalla del deportista: ")
        medallaValida = False
        while (medallaValida == False):
            if (medalla.upper() != "NA"
                    and medalla.upper() != "BRONZE"
                    and medalla.upper() != "SILVER"
                    and medalla.upper() != "GOLD"):
                print("Valor no permitido, vuelve a intentarlo. Los valores permitidos son: NA, Bronze, Silver y Gold.")
                medalla = input(
                    "Introduce nueva información para el campo medalla del deportista y evento seleccionado: ")
            else:
                medallaValida = True

        edadValida = False
        while edadValida == False:
            try:
                edad = int(input("Introduce edad del deportista al celebrarse la participacion: "))
                if (edad < 0):
                    print("Valor negativo no permitido")
                elif (edad > 200):
                    print("Valor demasiado alto")
                else:
                    edadValida = True
            except:
                edadValida = False

        query =  "SELECT nombre, id_equipo "
        query += "FROM Equipo;"
        self.cursor.execute(query)

        equipos = {}
        contEquipo = 0
        for row in self.cursor:
            equipos[contEquipo] = (row[0], row[1])
            print("\nEscribe " + str(contEquipo) + " para seleccionar:\n\t-Evento: " + str(row[0]))
            contEquipo += 1

        equipoValido = False
        while (equipoValido == False):
            try:
                numEquipo = int(input("\nNúmero del equipo deseado: "))
                if (numEquipo < 0):
                    print("Valores negativos no permitidos")
                elif (numEquipo >= contEquipo):
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contEquipo - 1))
                else:
                    equipo = equipos[numEquipo]
                    equipoValido = True
            except:
                equipoValido = False
        idEquipo = equipo[1]

        #Insertar participacion
        query = "INSERT INTO Participacion (id_deportista, id_evento, id_equipo, edad, medalla) "
        query += "VALUES (" + self.comodin + ", " + self.comodin + ", " + self.comodin + ", " + self.comodin + ", " + self.comodin + ");"
        self.cursor.execute(query, ((str(idDeportista)), idEvento, idEquipo, edad, medalla))

        #Cierre del conector y del cursor
        self.con.commit()
        self.cursor.close()
        self.con.close()

        print("Inserción de participación terminada correctamente\n")
        self.main()

    def eliminarParticipacion(self):
        self.crearConexion()

        nomDeportista = input("Introduce texto a buscar en tabla deportista: ")
        query = "SELECT nombre, id_deportista "
        query += "FROM Deportista;"
        self.cursor.execute(query)

        deportistas = {}
        contDeportista = 0
        for row in self.cursor:
            if (row[0].upper().__contains__(nomDeportista.upper())):
                deportistas[contDeportista] = (row[0], row[1])
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n\t-Deportista: " + str(row[0]))
                contDeportista += 1

        deportistaValido = False
        while (deportistaValido == False):
            try:
                numDeportista = int(input("\nNúmero del deportista deseado: "))
                if (numDeportista < 0):
                    print("Valores negativos no permitidos")
                elif (numDeportista >= contDeportista):
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contDeportista - 1))
                else:
                    deportista = deportistas[numDeportista]
                    deportistaValido = True
            except:
                deportistaValido = False
        idDeportista = deportista[1]

        query =  "SELECT Evento.nombre, Evento.id_evento "
        query += "FROM Evento, Participacion "
        query += "WHERE Evento.id_evento = Participacion.id_evento "
        query += "AND Participacion.id_deportista = " + self.comodin + ";"
        self.cursor.execute(query, (idDeportista, ))

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
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contEvento - 1))
                else:
                    evento = eventos[numEvento]
                    eventoValido = True
            except:
                eventoValido = False
        idEvento = evento[1]

        query =  "SELECT Equipo.nombre, Participacion.edad, medalla, id_deportista, id_evento, Participacion.id_equipo "
        query += "FROM Participacion, Equipo "
        query += "WHERE id_evento = " + self.comodin + " "
        query += "AND id_deportista = " + self.comodin + " "
        query += "AND Participacion.id_equipo = Equipo.id_equipo;"
        self.cursor.execute(query, (idEvento, idDeportista))

        participaciones = {}
        contParticipacion = 0
        for row in self.cursor:
            participaciones[contParticipacion] = (row[0], row[1], row[2], row[3], row[4], row[5])
            print("\nEscribe " + str(contParticipacion) + " para seleccionar la participación jugada para el equipo:" + str(row[0]) + "\n\t-Ganando la medalla: " + str(row[2]) +"\n\t-Con la edad: " + str(row[1]))
            contParticipacion += 1

        participacionValida = False
        while (participacionValida == False):
            try:
                numParticipacion = int(input("\nNúmero de la participacion deseada: "))
                if (numParticipacion < 0):
                    print("Valores negativos no permitidos")
                elif (numParticipacion >= contParticipacion):
                    print(
                        "El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contParticipacion - 1))
                else:
                    participacion = participaciones[numParticipacion]
                    participacionValida = True
            except:
                participacionValida = False
        idDeportista = participacion[3]
        idEvento = participacion[4]
        idEquipo = participacion[5]

        query =  "DELETE FROM Participacion "
        query += "WHERE id_deportista = " + self.comodin + " "
        query += "AND id_evento = " + self.comodin + " "
        query += "AND id_equipo = " + self.comodin + ";"
        self.cursor.execute(query, (idDeportista, idEvento, idEquipo))
        print("Participacion eliminada correctamente")

        if contParticipacion <= 1:
            print("Al ser esta la única participación del deportista borraremos la información sobre el deportista")
            query = "DELETE FROM Deportista "
            query += "WHERE id_deportista = " + self.comodin + ";"
            self.cursor.execute(query, (idDeportista,))
            print("Deportista eliminado correctamente")

        # Cierre del conector y del cursor
        self.con.commit()
        self.cursor.close()
        self.con.close()

        print()
        self.main()

ejConectores = Manejo_de_Conectores()
ejConectores.main()