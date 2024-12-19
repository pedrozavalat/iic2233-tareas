from funciones_utiles import cargar_data_json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5 import uic
import sys
import os

window_name, base_class = uic.loadUiType(os.path.join(*cargar_data_json("RUTA_VENTANA_ESPERA")))

"""
Ventana que permite la espera de jugadores antes de iniciar el juego. Al momento 
de conectarse dos jugadores, esta generara una cuenta regresiva de 10 segundos antes de 
comenzar el juego. 
"""

class VentanaEspera(window_name, base_class):

    senal_volver_inicio = pyqtSignal()
    senal_abrir_juego = pyqtSignal(str, str)
    senal_comienzo_del_juego = pyqtSignal(dict)
    senal_actualizar_ventana_espera = pyqtSignal(dict)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana de Espera")
        self.move(200, 200)
        self.init_gui()
        self.usuario = ''
        self.oponente = ''

    def init_gui(self):
        self.boton_volver.clicked.connect(self.volver)
        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_INICIO"))]
        self.label_tiempo.hide()
        self.timer_cuenta_regresiva = QTimer()
        self.timer_cuenta_regresiva.setInterval(1000)
        self.timer_cuenta_regresiva.timeout.connect(self.mostrar_tiempo_espera)

    def actualizar_ventana(self, usuarios, usuario):
        self.usuario = usuario
        if len(usuarios) > 1:
            self.oponente = list(filter(lambda x: x != self.usuario, usuarios))[0]
            self.label_jugador_2.setText(usuarios[1])
        self.label_jugador_1.setText(usuarios[0])

    def eliminar_label_usuario_retirado(self, usuario_retirado):
        self.timer_cuenta_regresiva.stop()
        self.label_tiempo.hide()
        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_INICIO"))]
        if usuario_retirado == self.usuario:
            self.label_jugador_1.setText(self.oponente)
        else:
            self.label_jugador_1.setText(self.usuario)
        self.label_jugador_2.setText('Jugador 2')
        
    def start_cuenta_regresiva(self):
        self.timer_cuenta_regresiva.start()
    
    def mostrar_tiempo_espera(self):
        segundo = self.tiempo.pop()
        self.label_tiempo.show()
        self.label_tiempo.setText(f'{segundo}')
        self.label_tiempo.setVisible(True)
        
        # En el caso que el tiempo sea 0, implica que termino el tiempo de espera.
        if not self.tiempo:     
            self.timer_cuenta_regresiva.stop()
            self.label_tiempo.setText(str(10))
            self.label_tiempo.hide()
            self.senal_abrir_juego.emit(self.usuario, self.oponente)
            self.usuario = ''
            self.oponente = ''
            
    def volver(self):
        self.salir()
        self.senal_volver_inicio.emit()
        datos = {
            "comando": "usuario_saliendo_sala_espera",
            "usuario": self.usuario
            }
        self.senal_actualizar_ventana_espera.emit(datos)
        self.eliminar_label_usuario_retirado(self.usuario)
    
    def mostrar(self):
        self.show()
    
    def salir(self):
        self.hide()
        self.reset()    

    def reset(self):
        self.usuario = ''
        self.oponente = ''
        self.label_tiempo.setText(str(10))
        self.label_jugador_1.setText("Jugador 1")
        self.label_jugador_2.setText("Jugador 2")
        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_INICIO"))]
        self.label_tiempo.hide()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaEspera()
    sys.exit(app.exec_())