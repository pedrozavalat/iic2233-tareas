from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtCore import pyqtSignal, QUrl
import parametros as p
import os
import sys

class VentanaInicio(QWidget):
    senal_abrir_ranking = pyqtSignal()
    senal_enviar_login = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Caracteristicas ventana de inicio
        self.setGeometry(400, 150, 600, 620)
        self.setWindowTitle("Ventana de Inicio")
        self.setMaximumSize(600, 620)
        self.setMinimumSize(600, 620)
        # Determinamos el fondo de pantalla usando QPalette de PyQt5.QtGui
        fondo_ventana = QPalette()
        fondo_ventana.setBrush(self.backgroundRole(), QBrush(QPixmap(p.RUTA_FONDO_MENU)))
        self.setPalette(fondo_ventana)
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl(p.RUTA_MUSICA)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.musica = QMediaPlayer()
        self.musica.setPlaylist(self.playlist)
        self.musica.play()

    def mostrar_elementos(self):
        # logo juego
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(p.RUTA_LOGO_JUEGO))
        self.logo.setGeometry(20, 50, 500, 300)
        self.logo.setScaledContents(True)
        # label usuario y caracteristicas
        self.label_usuario = QLabel('', self)
        self.ingresar_usuario = QLineEdit('', self)
        self.ingresar_usuario.setPlaceholderText('Ingresar Usuario')
        self.label_usuario.move(100, 380)
        self.ingresar_usuario.move(100, 380)
        self.ingresar_usuario.resize(400, 50)
        self.ingresar_usuario.setStyleSheet("color: white;"
                                        "font-weight: bold;"
                                        "font-size: 10px;"
                                        "background-color: darkslategray;"
                                        "padding: 10px;"
                                        "border-radius: 10px;"
                                        "border: 3px solid slategray;")
        # botones jugar, ranking y salir (con sus caracteristicas respectivas)
        self.boton_jugar = QPushButton('Jugar', self)
        self.boton_jugar.move(100, 460)
        self.boton_jugar.resize(100, 40)
        self.boton_jugar.clicked.connect(self.validar_login)
        self.boton_jugar.setStyleSheet("color: white;"
                                        "background-color: darkgrey;"
                                        "padding: 2px;"
                                        "border-radius: 10px;"
                                        "border: 3px solid slategray;")
        self.boton_ranking = QPushButton('Ranking', self)
        self.boton_ranking.move(250, 460)
        self.boton_ranking.resize(100, 40)
        self.boton_ranking.clicked.connect(self.abrir_ventana_ranking)
        self.boton_ranking.setStyleSheet("color: white;"
                                        "background-color: darkgrey;"
                                        "border-radius: 10px;"
                                        "border: 3px solid slategray;")
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.move(400, 460)
        self.boton_salir.resize(100, 40)
        self.boton_salir.clicked.connect(self.salir)
        self.boton_salir.setStyleSheet("color: white;"
                                        "background-color: darkgrey;"
                                        "padding: 2px;"
                                        "border-radius: 10px;"
                                        "border: 3px solid slategray;")
    # Se abre la ventana inicio
    def abrir(self):
        self.show()
        
        
    # Se cierra la ventana inicio 
    def salir(self):
        sys.exit()
    # Abre la ventana del ranking a partir del boton 'ranking'
    def abrir_ventana_ranking(self):
        self.musica.stop()
        self.hide()
        self.senal_abrir_ranking.emit()
    # Validamos el nombre de usuario, enviando el usuario al backend - logica inicio. 
    def validar_login(self):
        usuario = self.ingresar_usuario.text()
        self.senal_enviar_login.emit(usuario)
    # Recibimos la validacion del nombre de usuario por parte del backend - logica inicio.
    def recibir_validacion(self, valido, notificacion):
        if valido:
            self.ingresar_usuario.setText("") 
            self.musica.stop()
            self.hide()
        else:
            self.ingresar_usuario.setText("")
            self.ingresar_usuario.setPlaceholderText(notificacion)


    
        

        

        

       
        
        


        


