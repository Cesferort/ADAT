# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Olimpiada(Base):
    __tablename__ = 'Olimpiada'
    id_olimpiada = Column(Integer, primary_key=True)
    nombre = Column(String)
    anio = Column(String)
    temporada = Column(String)
    ciudad = Column(String)

    def getId(self):
        return self.id_olimpiada

    def getNombre(self):
        return self.nombre

    def getTemporada(self):
        return self.temporada

    def __str__(self):
        return "Nombre: " + self.nombre + "\n" \
               "Año: " + str(self.anio) + "\n" \
               "Temporada: " + self.temporada + "\n" \
               "Ciudad: " + self.ciudad

class Deporte(Base):
    __tablename__ = 'Deporte'
    id_deporte = Column(Integer, primary_key=True)
    nombre = Column(String)

    def __str__(self):
        return "Deporte: " + self.nombre

    def getId(self):
        return self.id_deporte

class Deportista(Base):
    __tablename__ = 'Deportista'
    id_deportista = Column(Integer, primary_key=True)
    nombre = Column(String)
    sexo = Column(String)
    peso = Column(Integer)
    altura = Column(Integer)

    def __init__(self, id_deportista, nombre, sexo, peso, altura):
        self.id_deportista = id_deportista
        self.nombre = nombre
        self.sexo = sexo
        self.peso = peso
        self.altura = altura

    def getId(self):
        return self.id_deportista
    def getNombre(self):
        return self.nombre
    def __str__(self):
        return "Nombre Deportista: " + self.nombre + "\n" \
               "Sexo: " + self.sexo + "\n" \
               "Peso: " + str(self.peso) + "\n" \
               "Altura: " + str(self.altura)

class Equipo(Base):
    __tablename__ = 'Equipo'
    id_equipo = Column(Integer, primary_key=True)
    nombre = Column(String)
    iniciales = Column(String)

    def getId(self):
        return self.id_equipo
    def getNombre(self):
        return self.nombre
    def __str__(self):
        return "Equipo: " + self.nombre + "\n" \
               "Iniciales: " + self.iniciales

class Evento(Base):
    __tablename__ = 'Evento'
    id_evento = Column(Integer, primary_key=True)
    nombre = Column(String)
    id_olimpiada = Column(Integer, ForeignKey('Olimpiada.id_olimpiada'))
    id_deporte = Column(Integer, ForeignKey('Deporte.id_deporte'))
    olimpiada = relation(Olimpiada, backref='Evento')
    deporte = relation(Deporte, backref='Evento')

    def __str__(self):
        return "Evento: " + self.nombre
    def getId(self):
        return self.id_evento

class Participacion(Base):
    __tablename__ = 'Participacion'
    id_deportista = Column(Integer, ForeignKey('Deportista.id_deportista'), primary_key=True)
    id_evento = Column(Integer, ForeignKey('Evento.id_evento'), primary_key=True)
    id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'), primary_key=True)
    deportista = relation(Deportista, backref='Participacion')
    evento = relation(Evento, backref='Participacion')
    equipo = relation(Equipo, backref='Participacion')
    edad = Column(Integer)
    medalla = Column(String)

    def __init__(self, id_deportista, id_evento, id_equipo, edad, medalla):
        self.id_deportista = id_deportista
        self.id_evento = id_evento
        self.id_equipo = id_equipo
        self.edad = edad
        self.medalla = medalla

    def getIdDeportista(self):
        return self.id_deportista
    def getIdEvento(self):
        return self.id_evento
    def getIdEquipo(self):
        return self.id_equipo
    def getEdad(self):
        return self.edad
    def getMedalla(self):
        return self.medalla
    def __str__(self):
        return "Edad: " + str(self.edad) + "\n" \
        "Medalla: " + self.medalla

class ORM:
    def main(self):
        respuesta = -1
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input("¿Qué deseas hacer?\n1. Listar deportistas participantes\n2. Modificar medalla\n3. Añadir deportista/participación\n4. Eliminar participación\n0. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 0 or respuesta > 4:
                    print("El número introducido escapa del rango (0-4)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.deportistasParticipantes()
        elif respuesta == 2:
            self.modificarMedalla()
        elif respuesta == 3:
            self.aniadirParticipacion()
        elif respuesta == 4:
            self.eliminarParticipacion()
        else:
            print("Programa Finalizado")

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
            engine = create_engine("mysql://user:pwd@localhost/college", echo=True)
            #engine = create_engine("mysql://user:usuOlimpiadas/dm2", echo=True)
        elif check == 2:
            engine = create_engine('sqlite:///olimpiadas.db', echo=True)

        self.Session = sessionmaker(bind=engine)
        self.con = engine.connect()

    def deportistasParticipantes(self):
        self.crearConexion()

        session = self.Session()

        #Pedimos una temporada
        temporada = input("Introduce temporada Winter o Summer (W/S)\n")
        while(temporada.upper() != "W" and temporada.upper() != "S"):
            temporada = input("Valor introducido no permitido. Vuelve a intentarlo:\nIntroduce temporada Winter o Summer (W/S)\n")
        if(temporada.upper()=="W"):
            temporada = "Winter"
        else:
            temporada = "Summer"

        # Recuperamos todas las Olimpiadas
        result_olimpiadas = session.query(Olimpiada).all()

        # Guardamos estas ediciones dentro de un diccionario y visualizamos el
        # identificador que nos permite acceder a cada edición dentro del diccionario
        # al usuario para que este pueda escoger la edición que desea
        ediciones = {}
        contEdicion = 0
        for row in result_olimpiadas:
            if row.getTemporada() == temporada:
                print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica: " + row.getNombre())
                ediciones[contEdicion] = (row)
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

        print("\nDatos de la Olimpiada escogida:\n" + str(edicion))
        result_DeporteEvento = session.query(Deporte, Evento).join(Evento).filter(Evento.id_olimpiada == edicion.getId()).all()

        # Filtramos los deportes para evitar repetidos
        deportes = {}
        for deporte, evento in result_DeporteEvento:
            if not deporte.getId() in deportes:
                deportes[deporte.getId()] = (deporte)

        # Guardamos en un diccionario ordenado todos los deportes y mostramos al usuario el
        # identificador que podrá utilizar para escoger el deporte que más desee
        contDeporte = 0
        deportesOrdenados = {}
        for deporteId in deportes:
            deportesOrdenados[contDeporte] = deportes[deporteId]
            print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t" + str(deportes[deporteId]))
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
                    deporte = deportesOrdenados[numDeporte]
                    deporteValido = True
            except:
                deporteValido = False

        print("\nDatos del Deporte seleccionado:\n" + str(deporte))
        result_eventos = session.query(Evento).filter(Evento.id_deporte == deporte.getId(), Evento.id_olimpiada == edicion.getId()).all()

        # Primera parte del resultado final
        for row in result_eventos:
            evento = row
        print("-- Resumen --\nTemporada: " + temporada + "\nEdición Olímpica: " + str(edicion) + "\nDeporte: " + str(deporte))
        print(evento)

        # Seleccionamos a los deportistas participantes en ese evento
        result_deportistas = session.query(Participacion, Deportista, Equipo).join(Deportista).join(Equipo).filter(Participacion.id_evento == evento.getId()).all()

        #Segunda parte del resultado final
        contResultDep = 1
        for participacion, deportista, equipo in result_deportistas:
            print(str(contResultDep) + ". " + str(deportista) + "\n" + str(equipo) + "\n" + str(participacion) + "\n")
            contResultDep += 1

        #Cierre del conector y de la sesión
        self.con.close()

        print()
        self.main()

    def modificarMedalla(self):
        self.crearConexion()

        session = self.Session()

        # Guardamos deportistas y mostramos identificador del diccionario
        texto = input("Introduce texto a buscar en tabla deportista: ")
        result_deportistas = session.query(Deportista).all()
        deportistas = {}
        contDeportista = 0
        for deportista in result_deportistas:
            if deportista.getNombre().upper().__contains__(texto.upper()):
                deportistas[contDeportista] = deportista
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n" + str(deportista))
                contDeportista += 1

        # El usuario elige un deportista válido
        deportistaValido = False
        while (deportistaValido == False):
            try:
                numDeportista = int(input("\nNúmero del deportista deseado: "))
                if (numDeportista < 0):
                    print("Valores negativos no permitidos")
                elif (numDeportista >= contDeportista):
                    print("El valor introducido escapa de los límites establecidos.\nPrueba con un número entre el 0 y " + str(
                            contDeportista - 1))
                else:
                    deportista = deportistas[numDeportista]
                    deportistaValido = True
            except:
                deportistaValido = False
        print("Deportista seleccionado:\n" + str(deportista))

        result_EventoParticipacion = session.query(Evento, Participacion).join(Participacion).filter(Participacion.id_deportista == deportista.getId()).all()
        eventos = {}
        contEvento = 0
        for evento, participacion in result_EventoParticipacion:
            eventos[contEvento] = (evento)
            print("\nEscribe " + str(contEvento) + " para seleccionar:\n" + str(evento))
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

        print("Evento seleccionado:\n" + str(evento))

        medalla = input("Introduce nueva información para el campo medalla del deportista y evento seleccionado: ")
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

        # Update
        session.query(Participacion).filter(Participacion.id_deportista == deportista.getId(), Participacion.id_evento == evento.getId()).update({Participacion.medalla: medalla}, synchronize_session=False)

        # Cierre del conector
        session.commit()
        self.con.close()

        print("Actualización terminada correctamente\n")
        self.main()

    def aniadirParticipacion(self):
        self.crearConexion()

        session = self.Session()

        # Guardamos deportistas y mostramos identificador del diccionario
        texto = input("Introduce texto a buscar en tabla deportista: ")
        result_deportistas = session.query(Deportista).all()
        deportistas = {}
        contDeportista = 0
        for deportista in result_deportistas:
            if deportista.getNombre().upper().__contains__(texto.upper()):
                deportistas[contDeportista] = deportista
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n" + str(deportista))
                contDeportista += 1

        # Validar si existe un deportista con dicho nombre
        if contDeportista == 0:
            print("\nDeportista no encontrado.\nInsertando nuevo deportista en la tabla...\n")
            result_deportistas = session.query(Deportista).all()
            for deportista in result_deportistas:
                idDeportista = 1 + deportista.getId()

            sexoValido = False
            while sexoValido == False:
                sexo = input("Introduce sexo del nuevo deportista: ")
                if (sexo.upper() != "M" and sexo.upper() != "F"):
                    print("Sexo no permitido.\nValores aceptados: M, F")
                else:
                    sexoValido = True

            pesoValido = False
            while pesoValido == False:
                try:
                    peso = int(input("Introduce peso del nuevo deportista: "))
                    if (peso < 0):
                        print("Valor negativo no permitido")
                    elif (peso > 1000):
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

            # Insertar deportista
            deportista = Deportista(idDeportista, texto, sexo, peso, altura)
            session.add(deportista)
            session.commit()
            print("Deportista insertado\n")
        else:
            # El usuario elige un deportista válido
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
        print("Deportista seleccionado:\n" + str(deportista))

        # Pedimos una temporada
        temporada = input("Introduce temporada Winter o Summer (W/S)\n")
        while (temporada.upper() != "W" and temporada.upper() != "S"):
            temporada = input("Valor introducido no permitido. Vuelve a intentarlo:\nIntroduce temporada Winter o Summer (W/S)\n")
        if (temporada.upper() == "W"):
            temporada = "Winter"
        else:
            temporada = "Summer"

        # Recuperamos todas las Olimpiadas
        result_olimpiadas = session.query(Olimpiada).all()

        # Guardamos estas ediciones dentro de un diccionario y visualizamos el
        # identificador que nos permite acceder a cada edición dentro del diccionario
        # al usuario para que este pueda escoger la edición que desea
        ediciones = {}
        contEdicion = 0
        for row in result_olimpiadas:
            if row.getTemporada() == temporada:
                print("\nEscribe " + str(contEdicion) + " para seleccionar:\n\t-Edición Olímpica: " + row.getNombre())
                ediciones[contEdicion] = (row)
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

        print("\nDatos de la Olimpiada escogida:\n" + str(edicion))

        result_DeporteEvento = session.query(Deporte, Evento).join(Evento).filter(Evento.id_olimpiada == edicion.getId()).all()

        # Filtramos los deportes para evitar repetidos
        deportes = {}
        for deporte, evento in result_DeporteEvento:
            if not deporte.getId() in deportes:
                deportes[deporte.getId()] = (deporte)

        # Guardamos en un diccionario ordenado todos los deportes y mostramos al usuario el
        # identificador que podrá utilizar para escoger el deporte que más desee
        contDeporte = 0
        deportesOrdenados = {}
        for deporteId in deportes:
            deportesOrdenados[contDeporte] = deportes[deporteId]
            print("\nEscribe " + str(contDeporte) + " para seleccionar:\n\t" + str(deportes[deporteId]))
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
                    deporte = deportesOrdenados[numDeporte]
                    deporteValido = True
            except:
                deporteValido = False

        print("\nDatos del Deporte seleccionado:\n" + str(deporte))
        result_eventos = session.query(Evento).filter(Evento.id_deporte == deporte.getId(), Evento.id_olimpiada == edicion.getId()).all()

        eventos = {}
        contEvento = 0
        for evento in result_eventos:
            eventos[contEvento] = (evento)
            print("\nEscribe " + str(contEvento) + " para seleccionar:\n\t" + str(evento))
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

        result_equipos = session.query(Equipo).all()

        equipos = {}
        contEquipo = 0
        for equipo in result_equipos:
            equipos[contEquipo] = (equipo)
            print("\nEscribe " + str(contEquipo) + " para seleccionar:\n\t" + str(equipo))
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

        participacion = Participacion(deportista.getId(), evento.getId(), equipo.getId(), edad, medalla)
        session.add(participacion)
        session.commit()
        print("Participación añadida\n")

        # Cierre del conector
        self.con.close()

        print("Inserción de participación terminada correctamente\n")
        self.main()

    def eliminarParticipacion(self):
        self.crearConexion()

        session = self.Session()

        # Guardamos deportistas y mostramos identificador del diccionario
        texto = input("Introduce texto a buscar en tabla deportista: ")
        result_deportistas = session.query(Deportista).all()
        deportistas = {}
        contDeportista = 0
        for deportista in result_deportistas:
            if deportista.getNombre().upper().__contains__(texto.upper()):
                deportistas[contDeportista] = deportista
                print("\nEscribe " + str(contDeportista) + " para seleccionar:\n" + str(deportista))
                contDeportista += 1

        # El usuario elige un deportista válido
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
        print("Deportista seleccionado:\n" + str(deportista))

        result_EventoParticipacion = session.query(Evento, Participacion).join(Participacion).filter(
            Participacion.id_deportista == deportista.getId()).all()
        eventos = {}
        contEvento = 0
        for evento, participacion in result_EventoParticipacion:
            eventos[contEvento] = (evento)
            print("\nEscribe " + str(contEvento) + " para seleccionar:\n" + str(evento))
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

        print("Evento seleccionado:\n" + str(evento))

        result_participaciones = session.query(Participacion, Evento, Deportista, Equipo).join(Evento).join(Deportista).join(Equipo).filter(
            Participacion.id_deportista == deportista.getId(),
            Deportista.id_deportista == deportista.getId(),
            Participacion.id_evento == evento.getId(),
            Evento.id_evento == evento.getId()).all()

        participaciones = {}
        contParticipacion = 0
        for participacion, evento, deportista, equipo in result_participaciones:
            participaciones[contParticipacion] = (participacion)
            print("\nEscribe " + str(contParticipacion) + " para seleccionar la participación jugada para el equipo:" +
                equipo.getNombre() + "\n\t-Ganando la medalla: " + participacion.getMedalla() + "\n\t-Con la edad: " + str(participacion.getEdad()))

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

        session.delete(participacion)
        session.commit()
        print("Participacion eliminada correctamente")

        result_DeportistaParticipacion = session.query(Deportista, Participacion).join(Participacion).filter(Deportista.id_deportista == deportista.getId(), Participacion.id_deportista == deportista.getId()).all()
        cont = 0
        for row in result_DeportistaParticipacion:
            cont += 1
        if cont <= 0:
            # Este deportista no tiene más participaciones en la tabla Participación
            session.delete(deportista)
            session.commit()
            print("Deportista eliminado correctamente")

        # Cierre del conector
        self.con.close()

        print()
        self.main()

ejORM = ORM()
ejORM.main()