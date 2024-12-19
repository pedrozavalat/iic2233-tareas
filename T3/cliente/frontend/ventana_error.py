from funciones_utiles import cargar_data_json
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import sys
import os

"""
Ventana de 'emergencia'. Al momento de caerse el servidor, esta ventana es 
mostrada a todos los usuarios notificandoles sobre el error de conexion ocurrido. 
Luego de 3 segundos, todos los usuarios se les cerraran todas las interfaces abiertas, y se 
desconectara su conexion. 
"""

window_name, base_class = uic.loadUiType(os.path.join(
                                            *cargar_data_json("RUTA_VENTANA_ERROR_CONEXION")))


class VentanaError(window_name, base_class):

    senal_cerrar_aplicacion = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana perdida de conexión")
        self.move(200, 200)
        self.init_gui()

    def init_gui(self):
        self.timer_duracion_ventana = QTimer()
        self.timer_duracion_ventana.setSingleShot(True)
        self.timer_duracion_ventana.setInterval(3000)
        self.timer_duracion_ventana.timeout.connect(self.salir)

    def mostrar(self):
        self.show()
        self.timer_duracion_ventana.start()

    def salir(self):
        self.senal_cerrar_aplicacion.emit()
        self.close()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaError()
    sys.exit(app.exec_())
