from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import uic
import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_PRINCIPAL)

class VentanaPrincipal(window_name, base_class):
    senal_escenario_seleccionado = pyqtSignal(str)
    senal_enviar_verificacion_boton = pyqtSignal(str)
    

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()
        self.musica = QMediaPlayer()
    
    def init_gui(self):
        self.setWindowTitle("Ventana Principal")
        self.move(210, 75)
        self.label_notificacion.hide()
        # Conectamos los botones para verificar el escenario elegido por el jugador.
        self.boton_jardin_abuela.clicked.connect(self.escenario_seleccionado)
        self.boton_salida_nocturna.clicked.connect(self.escenario_seleccionado)
        self.boton_iniciar_juego.clicked.connect(self.enviar_verificacion_boton)

    def abrir(self, usuario):
        self.usuario = usuario # Recibimos el nombre del usuario de la 'logica inicio'
        self.musica.setMedia(QMediaContent(QUrl.fromLocalFile(p.RUTA_MUSICA)))
        self.musica.play()
        self.show()
    # Obtenemos el escenario elegido y lo guardamos, enviando una señal al backend.
    def escenario_seleccionado(self): 
        boton = self.sender().text()
        self.senal_escenario_seleccionado.emit(boton) 
    # Verificamos si el jugador eligió un escenario. 
    def enviar_verificacion_boton(self):
        self.senal_enviar_verificacion_boton.emit(self.usuario)
    # Recibimos la validacion de la selección de algun escenario desde "logica principal".
    def recibir_notificacion(self, escenario_elegido):
        if escenario_elegido:
            self.label_notificacion.hide()
            self.musica.stop()
            self.hide()
        else:
            self.label_notificacion.show()
            
     


            



    
        