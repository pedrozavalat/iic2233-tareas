from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import uic
import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_POST_RONDA)

class VentanaPostRonda(window_name, base_class):
    
    senal_salir = pyqtSignal()
    senal_siguiente_ronda = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()
        self.musica = QMediaPlayer()
    
    def init_gui(self):
        self.setWindowTitle("Ventana Post-Ronda")
        self.move(400, 75)
        self.notificacion_perder.hide()
        self.notificacion_ganar.hide()
        self.boton_siguiente_ronda.clicked.connect(self.siguiente_ronda)
        self.boton_salir.clicked.connect(self.salir)
        
    def abrir(self):
        self.show()
        self.musica.setMedia(QMediaContent(QUrl.fromLocalFile(p.RUTA_MUSICA)))
        self.musica.play()

    def salir(self):
        self.musica.stop()
        self.notificacion_perder.hide()
        self.notificacion_ganar.hide()
        self.hide()
        self.senal_salir.emit()
        self.boton_siguiente_ronda.setEnabled(True)
    
    def cerrar_ventana(self):
        self.close()
        self.musica.stop()
    # En el caso que el usuario haya perdido, se le notifica con el anuncio rojo.
    def mostrar_notificacion_roja(self): 
        self.notificacion_perder.show()
        self.boton_siguiente_ronda.setEnabled(False)
    # En el caso que el usuario haya perdido, se le notifica con el anuncio verde.
    def mostrar_notificacion_verde(self):
        self.notificacion_ganar.show()

    def siguiente_ronda(self):
        self.cerrar_ventana()
        self.senal_siguiente_ronda.emit()
    # Actualiza en el tablero los datos del usuario. 
    def recibir_datos(self, datos):
        self.ronda_actual.setText(datos["nivel"])
        self.soles_restantes.setText(datos["soles"])
        self.zombies_destruidos.setText(datos["zombies destruidos"])
        self.puntaje_ronda.setText(datos["puntaje"])
        self.puntaje_total.setText(datos["puntaje_total"])
    
    