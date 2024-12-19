
from PyQt5.QtCore import QObject, pyqtSignal

class LogicaPostRonda(QObject):

    senal_enviar_datos = pyqtSignal(dict)
    senal_mostrar_anuncio_ganador = pyqtSignal()
    senal_mostrar_anuncio_perdedor = pyqtSignal()
    senal_cargar_ronda = pyqtSignal(str, str, int)

    def __init__(self):
        super().__init__()
        self.escenario = None
        self.datos = None
        self.nombre = None
    
    def recibir_datos(self, datos, nombre, escenario, estado):
        with open("puntajes.txt", 'r', encoding = 'utf-8') as puntajes:
            puntajes = puntajes.readlines()
            puntajes = [linea.strip("\n").split(",") for linea in puntajes]
            # Creamos un diccionario para verificar que no se repitan los nombres
            # de usuario. 
            crear_puntajes = {puntaje[0] : puntaje[1] for puntaje in puntajes} 
            # Si no se encuentra en el archivo, consideramos el puntaje total como
            # el puntaje de la ronda.
            if nombre not in crear_puntajes.keys():
                crear_puntajes[nombre] = datos["puntaje"]
            # Si se encuentra en el archivo, el puntaje de la ronda es sumado al 
            # puntaje total.
            else:
                puntaje_total = int(crear_puntajes[nombre]) + int(datos["puntaje"]) 
                crear_puntajes[nombre] = str(puntaje_total)
            datos["puntaje_total"] = crear_puntajes[nombre]
        # 'Actualizamos' el archivo puntajes.txt con el nuevo puntaje del jugador
        # respectivo.
        archivo_actualizado = ""
        for jugador, puntaje in crear_puntajes.items():
            archivo_actualizado += f'{jugador},{puntaje}\n'
        with open("puntajes.txt", 'w', encoding = 'utf-8') as puntajes:
            puntajes.write(archivo_actualizado)  
        self.escenario = escenario
        self.datos = datos  
        self.nombre = nombre
        self.senal_enviar_datos.emit(datos)
        if estado == "gano":
            self.senal_mostrar_anuncio_ganador.emit()
        elif estado == "pierde":
            self.senal_mostrar_anuncio_perdedor.emit()
    
    def cargar_siguiente_ronda(self): # Permite actualizar la ronda actual. 
        ronda_anterior = int(self.datos["nivel"])
        ronda_actual = ronda_anterior + 1
        self.senal_cargar_ronda.emit(self.nombre, self.escenario, ronda_actual)
        


        
        
            
        
        
        


