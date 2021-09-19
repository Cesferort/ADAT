# -*- coding: utf-8 -*-
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from pyexistdb.db import ExistDB

class Socio:
    def __init__(self, nombre, codigo, fecha_alt, dir, cuota_fija):
        self.nombre = nombre
        self.codigo = codigo
        self.fecha_alt = fecha_alt
        self.dir = dir
        self.cuota_fija = cuota_fija

    def getNombre(self):
        return self.nombre
    def getCuotaFija(self):
        return self.cuota_fija

class Actividad:
    def __init__(self, cod, tipo, nombre):
        self.cod = cod
        self.tipo = tipo
        self.nombre = nombre

    def getTipo(self):
        return self.tipo
    def getNombre(self):
        return self.nombre

class DatosIntermediarios:
    def __init__(self, codSocio, nomSocio, codActividad, nomActividad, horas, tipoActividad, cuotaFija, cuotaAdic):
        self.codSocio = codSocio
        self.nomSocio = nomSocio
        self.codActividad = codActividad
        self.nomActividad = nomActividad
        self.horas = horas
        self.tipoActividad = tipoActividad
        self.cuotaFija = cuotaFija
        self.cuotaAdic = cuotaAdic

    def getCodSocio(self):
        return self.codSocio
    def getNomSocio(self):
        return self.nomSocio
    def getCodActividad(self):
        return self.codActividad
    def getNomActividad(self):
        return self.nomActividad
    def getHoras(self):
        return self.horas
    def getTipoActividad(self):
        return self.tipoActividad
    def getCuotaFija(self):
        return self.cuotaFija
    def getCuotaAdic(self):
        return self.cuotaAdic

class DatoFinal:
    def __init__(self, codSocio, nomSocio, cuotaFija, sumaCuotaAdic, cuotaTotal):
        self.codSocio = codSocio
        self.nomSocio = nomSocio
        self.cuotaFija = cuotaFija
        self.sumaCuotaAdic = sumaCuotaAdic
        self.cuotaTotal = cuotaTotal

    def getCodSocio(self):
        return self.codSocio
    def getNomSocio(self):
        return self.nomSocio
    def getCuotaFija(self):
        return self.cuotaFija
    def getSumaCuotaAdic(self):
        return self.sumaCuotaAdic
    def getCuotaTotal(self):
        return self.cuotaTotal
    def setSumaCuotaAdic(self, sumaCuotaAdic):
        self.sumaCuotaAdic = sumaCuotaAdic
    def setCuotaTotal(self, cuotaTotal):
        self.cuotaTotal = cuotaTotal

class ColeccionGimnasio:
    COLLECTION = 'GIMNASIO'
    socios = {}
    def main(self):
        self.db = ExistDB(server_url='http://localhost:8080/exist/xmlrpc',
                          username='admin', password='dm2')
        self.db.createCollection(self.COLLECTION, True)

        self.db.load(open(r'F:\Program Files (x86)\PycharmProjects\Segundo Trimestre\UD6\xml\actividades_gim.xml'), self.COLLECTION + '/actividades_gim.xml')
        self.db.load(open(r'F:\Program Files (x86)\PycharmProjects\Segundo Trimestre\UD6\xml\socios_gim.xml'), self.COLLECTION + '/socios_gim.xml')
        self.db.load(open(r'F:\Program Files (x86)\PycharmProjects\Segundo Trimestre\UD6\xml\uso_gimnasio.xml'), self.COLLECTION + '/uso_gimnasio.xml')

        self.resolver1()
        self.resolver2()

    def resolver1(self):
        self.socios = {}
        # Recuperar todos los socios y guardarlos en un diccionario con
        # su codigo como identificador
        qs = self.db.executeQuery('//fila_socios')
        hits = self.db.getHits(qs)
        for i in range(hits):
            try:
                datos = str(self.db.retrieve(qs, i))
                codigo = int(self.getDatos(datos, "COD"))
                nombre = self.getDatos(datos, "NOMBRE")
                fecha_alt = self.getDatos(datos, "FECHA_ALT")
                dir = self.getDatos(datos, "DIRECCION")
                cuota_fija = int(self.getDatos(datos, "CUOTA_FIJA"))

                socio = Socio(nombre, codigo, fecha_alt, dir, cuota_fija)

                codigo = int(codigo)
                self.socios[codigo] = socio
            except:
                print("El identificador o la cuota del socio '" + nombre + "' está mal formateado. Comprueba su formato: " + self.getDatos(datos, "COD"))

        # Recuperar todas las actividades y guardarlas en un diccionario con
        # su codigo como identificador
        qs = self.db.executeQuery('//fila_actividades')
        hits = self.db.getHits(qs)
        actividades = {}
        for i in range(hits):
            try:
                datos = str(self.db.retrieve(qs, i))
                cod = int(self.getDatos_Atributo(datos, "cod"))
                tipo = int(self.getDatos_Atributo(datos, "tipo"))
                nombre = self.getDatos(datos, "NOMBRE")

                actividad = Actividad(cod, tipo, nombre)
                actividades[cod] = actividad
            except:
                print("Los valores de tipo y/o identificador de la actividad '" + nombre + "' están mal formateado. Comprueba su formato")

        # Recuperar todos los usos del gimnasio y procesar la información a un
        # diccionario intermedio
        qs = self.db.executeQuery('//fila_uso')
        hits = self.db.getHits(qs)
        listaDatosIntermediarios = {}
        for i in range(hits):
            try:
                datos = str(self.db.retrieve(qs, i))
                codSoci = int(self.getDatos(datos, "CODSOCIO"))
                codActi = int(self.getDatos(datos, "CODACTIV"))
                horaIni = int(self.getDatos(datos, "HORAINICIO"))
                horaFin = int(self.getDatos(datos, "HORAFINAL"))

                socio = self.socios[codSoci]
                actividad = actividades[codActi]

                horas = horaFin - horaIni;
                tipo = actividad.getTipo();
                cuotaFija = socio.getCuotaFija()

                cuotaAdic = 0;
                if tipo == 2:
                    cuotaAdic = 2;
                elif tipo == 3:
                    cuotaAdic = 4;

                datosIntermediarios = DatosIntermediarios(codSoci, socio.getNombre(), codActi, actividad.getNombre(), horas, tipo, cuotaFija, cuotaAdic)
                listaDatosIntermediarios[i] = datosIntermediarios
            except:
                print("Los valores número '" + str(i) + "' de uso están mal formateados.")

        # Crear XML intermedio y subirlo
        top = Element('datos_intermedio')
        comment = Comment('Datos intermedio para el cálculo de cuotas finales')
        top.append(comment)
        for cont in listaDatosIntermediarios:
            datos = listaDatosIntermediarios[cont]

            codSocio = str(datos.getCodSocio())
            nomSocio = str(datos.getNomSocio())
            codActividad = str(datos.getCodActividad())
            nomActividad = str(datos.getNomActividad())
            horas = str(datos.getHoras())
            tipoActividades = str(datos.getTipoActividad())
            cuotaAdicional = str(datos.getCuotaAdic())

            eleDatos = SubElement(top, 'datos')

            eleCod = SubElement(eleDatos, 'COD')
            eleCod.text = codSocio
            eleNombreSocio = SubElement(eleDatos, 'NOMBRESOCIO')
            eleNombreSocio.text = nomSocio
            eleCodActiv = SubElement(eleDatos, 'CODACTIV')
            eleCodActiv.text = codActividad
            eleNombreActividad = SubElement(eleDatos, 'NOMBREACTIVIDAD')
            eleNombreActividad.text = nomActividad
            eleHoras = SubElement(eleDatos, 'horas')
            eleHoras.text = horas
            eleTipoAct = SubElement(eleDatos, 'tipoact')
            eleTipoAct.text = tipoActividades
            eleCuotaAdicional = SubElement(eleDatos, 'cuota_adicional')
            eleCuotaAdicional.text = cuotaAdicional

        rough_string = ElementTree.tostring(top, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        with open("../xml/datos_intermedios.xml", "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + reparsed.toprettyxml(indent="  ").split("\n",1)[1])

        self.db.load(open(r'F:\Program Files (x86)\PycharmProjects\Segundo Trimestre\UD6\xml\datos_intermedios.xml'), self.COLLECTION + '/datos_intermedios.xml')

    def resolver2(self):
        # Recuperar información intermedia
        qs = self.db.executeQuery('//datos_intermedio/datos')
        hits = self.db.getHits(qs)
        datosFinales = {}
        for i in range(hits):
            try:
                datos = str(self.db.retrieve(qs, i))
                codSocio = int(self.getDatos(datos, "COD"))
                nomSocio = self.getDatos(datos, "NOMBRESOCIO")
                horas = int(self.getDatos(datos, "horas"))
                cuotaAdicional = int(self.getDatos(datos, "cuota_adicional"))

                if not codSocio in datosFinales:
                    socio = self.socios[codSocio]
                    cuotaFija = socio.getCuotaFija()
                    sumaCuotaAdic = horas * cuotaAdicional
                    cuotaTotal = sumaCuotaAdic + cuotaFija

                    datoFinal = DatoFinal(codSocio, nomSocio, cuotaFija, sumaCuotaAdic, cuotaTotal)
                    datosFinales[codSocio] = datoFinal
                else:
                    datoFinal = datosFinales[codSocio]

                    sumaCuotaAdic = datoFinal.getSumaCuotaAdic()
                    sumaCuotaAdic = sumaCuotaAdic + (horas * cuotaAdicional)
                    cuotaTotal = sumaCuotaAdic + cuotaFija

                    datoFinal.setSumaCuotaAdic(sumaCuotaAdic)
                    datoFinal.setCuotaTotal(cuotaTotal)
            except:
                print("Formato incorrecto.")

        # Crear XML intermedio y subirlo
        top = Element('datos_finales')
        comment = Comment('Datos finales')
        top.append(comment)
        for cont in datosFinales:
            datos = datosFinales[cont]

            codSocio = str(datos.getCodSocio())
            nomSocio = str(datos.getNomSocio())
            cuotaFija = str(datos.getCuotaFija())
            sumaCuotaAdic = str(datos.getSumaCuotaAdic())
            cuotaTotal = str(datos.getCuotaTotal())

            eleDatos = SubElement(top, 'datos')

            eleCod = SubElement(eleDatos, 'COD')
            eleCod.text = codSocio
            eleNombreSocio = SubElement(eleDatos, 'NOMBRESOCIO')
            eleNombreSocio.text = nomSocio
            eleCuotaFija = SubElement(eleDatos, 'CUOTA_FIJA')
            eleCuotaFija.text = cuotaFija
            eleSumaCuotaAdic = SubElement(eleDatos, 'suma_cuota_adic')
            eleSumaCuotaAdic.text = sumaCuotaAdic
            eleCuotaTotal = SubElement(eleDatos, 'cuota_total')
            eleCuotaTotal.text = cuotaTotal

        rough_string = ElementTree.tostring(top, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        with open("../xml/datos_finales.xml", "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + reparsed.toprettyxml(indent="  ").split("\n",1)[1])

        self.db.load(open(r'F:\Program Files (x86)\PycharmProjects\Segundo Trimestre\UD6\xml\datos_finales.xml'), self.COLLECTION + '/datos_finales.xml')

    def getDatos(self, datos, texto):
        datos_cortarPrimeraParte = datos.split("<" + texto + ">")
        datos_cortarSegundaParte = datos_cortarPrimeraParte[1].split("</" + texto + ">")
        datos_refinados = datos_cortarSegundaParte[0]
        return datos_refinados

    def getDatos_Atributo(self, datos, texto):
        datos_cortarPrimeraParte = datos.split(texto + "=\"")
        datos_cortarSegundaParte = datos_cortarPrimeraParte[1]
        datos_refinados = datos_cortarSegundaParte[: datos_cortarSegundaParte.find('"')]

        return datos_refinados

ejColeccionGimnasio = ColeccionGimnasio()
ejColeccionGimnasio.main()