# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
class Prueba_XML:
    def main(self):
        tree = ET.parse('datos_prueba.xml')
        root = tree.getroot()

        for datos in root.findall('datos'):                                 # SubElementos
            idDatos = datos.get('id')                                       # Atributo
            print("IdDatos: " + idDatos)
            codSocio = datos.find('COD').text                               # SubElemento
            print("COD: " + codSocio)
            #Prueba subelemento de un subelemento
            elePrueba = datos.find('prueba')
            eleSubPrueba = elePrueba.find('sub_prueba').text
            print("EleSubPrueba: " + eleSubPrueba)

prueba_XML = Prueba_XML()
prueba_XML.main()