# -*- coding: utf-8 -*-
import os, shutil

class FicherosEJ1:
    def main(self):
        respuestaValida = False
        while respuestaValida == False:
            respuesta = input("¿Qué deseas hacer?\n1. Crea un directorio\n2. Listar un directorio\n3. Copiar un archivo\n4. Mover un archivo\n5. Eliminar un archivo/directorio\n6. Salir del programa\n")
            try:
                respuesta = int(respuesta)
                if respuesta < 1 or respuesta > 6:
                    print("El número introducido escapa del rango (1-6)")
                else:
                    respuestaValida = True
            except ValueError:
                print("Valor no númerico introducido")
        if respuesta == 1:
            self.crearDirectorio()
        elif respuesta == 2:
            self.listarDirectorio()
        elif respuesta == 3:
            self.copiarArchivo()
        elif respuesta == 4:
            self.moverArchivo()
        elif respuesta == 5:
            self.eliminarArchivo()
        else:
            print("Programa Finalizado")

    def crearDirectorio(self):
        try:
            rutaDir = input("Introduce ruta en la que deseas introducir este nuevo directorio: ")
            nombreDir = input("Introduce nombre del directorio: ")
            os.makedirs(rutaDir + '/' + nombreDir)
            print("Directorio creado correctamente.\n")
        except:
            print("Esta carpeta ya existe.\n")
        self.main()

    def listarDirectorio(self):
        rutaDir = input("Introduce la ruta del directorio que deseas listar: ")

        with os.scandir(rutaDir) as ficheros:
            for fichero in ficheros:
                isFile = os.path.isfile(rutaDir+"/"+fichero.name)
                if isFile == True:
                    print("\t"+fichero.name)
                else:
                    print("DIR "+fichero.name)
        print()
        self.main()

    def copiarArchivo(self):
        rutaOriginal = input("Introduce ruta del archivo original: ")
        rutaDestino = input("Introduce ruta a la que deseas copiar el archivo: ")
        if not os.path.exists(rutaOriginal):
            print("La ruta original no existe.")
        else:
            shutil.copyfile(rutaOriginal, rutaDestino)
        print()
        self.main()

    def moverArchivo(self):
        rutaOriginal = input("Introduce ruta del archivo original: ")
        rutaDestino = input("Introduce ruta a la que deseas mover el archivo: ")
        if not os.path.exists(rutaOriginal):
            print("La ruta original no existe.")
        else:
            shutil.move(rutaOriginal, rutaDestino)
        print()
        self.main()

    def eliminarArchivo(self):
        #os.remove()        -> borra un archivo
        #os.rmdir()         -> borra una carpeta VACÍA
        #shutil.rmtree()    -> borra una carpeta Y SU CONTENIDO
        ruta = input("Introduce ruta del archivo o directorio a eliminar: ")
        if(os.path.exists(ruta)):
            if(os.path.isfile(ruta) == True):
                os.remove(ruta)
                print("Archivo eliminado")
            else:
                if not os.listdir(ruta):
                    os.rmdir(ruta)
                    print("Carpeta eliminada")
                else:
                    print("La carpeta no se pudo eliminar porque no está vacía")
        else:
            print("La ruta especificada no existe")
        print()
        self.main()

ej1 = FicherosEJ1()
ej1.main()