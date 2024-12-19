from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import sys
import os
from funciones_utiles import cargar_data_json

window_name, base_class = uic.loadUiType(os.path.join(
                                            *cargar_data_json("RUTA_VENTANA_FINAL")))

"""
Ventana que se abre unicamente cuando finaliza la partida de DCCard-Jitsu, esta informara
a cada jugador que de la partida si fue el 'ganador', o el 'perdedor'. 
"""

class VentanaFinal(window_name, base_class):

    senal_volver_inicio = pyqtSignal()
    senal_enviar_ganador_partida = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana Final")
        self.move(200, 200)
        self.init_gui()

    def init_gui(self):
        self.boton_aceptar.clicked.connect(self.volver_inicio)

    def mostrar(self):
        self.show()

    def recibir_ganador(self, usuario, ganador):
        self.mostrar()
        if usuario == ganador:
            self.label_notificacion.setText("¡Has Ganado!")
            datos = {
                "comando": "recibir_ganador_partida",
                "ganador partida": ganador}
            self.senal_enviar_ganador_partida.emit(datos)
        else:
            self.label_notificacion.setText("Has Perdido :(")

    def volver_inicio(self):
        self.label_notificacion.setText('')
        self.ocultar()
        self.senal_volver_inicio.emit()

    def ocultar(self):
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFinal()
    sys.exit(app.exec_())
