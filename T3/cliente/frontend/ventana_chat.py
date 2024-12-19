from funciones_utiles import cargar_data_json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from collections import deque
from PyQt5 import uic
import sys
import os

"""
Ventana que permite la comunicacion entre jugadores de la partida en tiempo real
"""


window_name, base_class = uic.loadUiType(os.path.join(
                                            *cargar_data_json("RUTA_VENTANA_CHAT")))

class VentanaChat(window_name, base_class):

    senal_enviar_mensaje = pyqtSignal(dict)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana Chat")
        self.move(1003, 0)
        self.init_gui()
        self.usuario = ''
        self.chat = ''
        self.lineas_chat = deque()

    def init_gui(self):
        self.boton_enviar.clicked.connect(self.enviar_mensaje)
        self.label_chat = QLabel('', self)
        self.label_chat.setGeometry(10, 15, 281, 191)
        self.label_chat.setStyleSheet("background-color:midnightblue;" 
                            "background-color: rgba(0, 100, 200,180);"
                            "border-radius: 20px;"
                            "color: white;"
                            "font-size: 8 px;")
        self.label_chat.setVisible(True)



        self.label_mensaje = QLabel('', self)
        self.label_mensaje.setStyleSheet("background-color:white;"
                                        "color: gray;"
                                        "font-size: 12px;"
                                        "border-radius: 10px;")
        self.label_mensaje.setGeometry(10, 220, 100, 70)
        self.label_mensaje.move(10, 220)
        self.label_mensaje.setVisible(True)
        self.escribir_mensaje = QLineEdit('', self)
        self.escribir_mensaje.setStyleSheet("background-color:white;"
                                        "color: gray;"
                                        "font-size: 12px;"
                                        "border-radius: 10px;")
        self.escribir_mensaje.setGeometry(10, 220, 200, 70)
        self.escribir_mensaje.move(10, 220)
        self.escribir_mensaje.setPlaceholderText('Escribe un mensaje...')
        self.escribir_mensaje.setVisible(True)
    
    def enviar_mensaje(self):
        mensaje = self.escribir_mensaje.text()
        datos = {
            "comando": "recibir_mensaje_chat",
            "mensaje": mensaje,
            "usuario": self.usuario
            }
        self.senal_enviar_mensaje.emit(datos)
        self.escribir_mensaje.setText('')
        self.escribir_mensaje.setPlaceholderText("Escribe un mensaje...")
        self.actualizar_bandeja_entrada(self.usuario, mensaje)

    def actualizar_bandeja_entrada(self, usuario, mensaje):
        linea = f'{usuario}: {mensaje}\n'
        self.chat += linea
        self.lineas_chat.append(linea)
        self.label_chat.setText(self.chat)
        if len(self.lineas_chat) == 10:
            self.lineas_chat.popleft()
            self.chat = "".join(self.lineas_chat)
        
    def mostrar(self, usuario):
        self.show()
        self.usuario = usuario

    def ocultar(self):
        self.hide()

    def salir(self):
        self.label_chat.setText("")
        self.close()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaChat()
    sys.exit(app.exec_())
