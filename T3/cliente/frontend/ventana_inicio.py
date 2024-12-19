from funciones_utiles import cargar_data_json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5 import uic
import sys
import os

window_name, base_class = uic.loadUiType(os.path.join(
                                            *cargar_data_json("RUTA_VENTANA_INICIO")))

"""
Ventana que permite la verificacion del nombre de usuario del cliente que quiere ingresar
a una partida. En este caso, si acepta el usuario, verificará si: 1) existen jugadores 
presentes en la sala de espera; 2) si ya hay una partida iniciada. Si se cumple uno de 
los dos casos, el jugador tendrá que esperar en la ventana de inicio. En otro caso, este 
entrará a esta ventana a esperar otro jugador, o empezar directamente (si es que ya se 
encontraba un jugador), el juego. 
"""

class VentanaInicio(window_name, base_class):

    senal_enviar_login = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana de Inicio")
        self.move(200, 200)
        self.label_sala_llena.hide()
        self.label_partida_existente.hide()
        self.init_gui()

    def init_gui(self):
        
        self.label_usuario = QLabel('', self)
        self.label_usuario.move(300, 600)
        self.ingresar_usuario = QLineEdit('', self)
        self.ingresar_usuario.move(300, 600)
        self.ingresar_usuario.resize(400, 50)
        self.ingresar_usuario.setPlaceholderText('Ingresar tu nombre ...')
        self.ingresar_usuario.setStyleSheet("background-color:white;"
                                            "color: gray;"
                                            "font: bold;" 
                                            "font-size: 12px;" 
                                            "border-radius: 20px;")
        self.label_usuario.setVisible(True)
        self.ingresar_usuario.setVisible(True)
        self.boton_ingresar.clicked.connect(self.enviar_login)
        
        # ====================== Instanciamos los timers =========================
        self.timer_ocultar_anuncio = QTimer()
        self.timer_ocultar_anuncio.setSingleShot(True)
        self.timer_ocultar_anuncio.setInterval(3000)
        self.timer_ocultar_anuncio.timeout.connect(self.ocultar_aviso)
    
    def enviar_login(self):
        nombre_usuario = self.ingresar_usuario.text().replace(" ", "")
        datos = {
            "comando": "validar_login",
            "nombre usuario": nombre_usuario}
        self.senal_enviar_login.emit(datos)
    
    def login_rechazado(self, error):
        self.ingresar_usuario.setText("")
        #self.ingresar_usuario.setPlaceholderText("Ingresar tu nombre")
        self.ingresar_usuario.setPlaceholderText(error)
        
    def mostrar_aviso_sala_llena(self):
        self.label_sala_llena.show()
        self.timer_ocultar_anuncio.start()
        
    def mostrar_aviso_partida_existente(self):
        self.label_partida_existente.show()
        self.timer_ocultar_anuncio.start()
    
    def ocultar_aviso(self):
        self.label_sala_llena.hide()
        self.label_partida_existente.hide()
        self.boton_ingresar.setEnabled(True)

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()

    def salir(self):
        self.ingresar_usuario.setText("")
        self.close()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    sys.exit(app.exec_())
