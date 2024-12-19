from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import pyqtSignal, Qt, QUrl
import parametros as p


class VentanaRanking(QWidget):

    senal_pedir_ranking = pyqtSignal()
    senal_volver_ventana_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Caracteristicas ventana de inicio
        self.setGeometry(500, 150, 400, 660)
        self.setWindowTitle("Ranking de Puntajes")
        self.setMaximumSize(400, 660)
        self.setMinimumSize(400, 660)
        
        # Determinamos el fondo de pantalla usando QPalette de PyQt5.QtGui
        fondo_ventana = QPalette()
        fondo_ventana.setBrush(self.backgroundRole(), QBrush(QPixmap(p.RUTA_FONDO_MENU)))
        self.setPalette(fondo_ventana)
        self.musica = QMediaPlayer()
        

    def mostrar_elementos(self):
        # label usuario y boton volver
        self.label_titulo = QLabel('RANKING DE PUNTAJES', self)
        
        self.label_titulo.setStyleSheet("color: white;"
                                        "font-size: 32px;"
                                        "font-weight: bold;")

        
        self.boton_volver = QPushButton('Volver', self)
        self.boton_volver.move(160, 610)
        self.boton_volver.resize(100, 50)
        self.boton_volver.clicked.connect(self.volver_ventana_inicio)
        self.boton_volver.setStyleSheet("color: white;"
                                        "background-color: darkgrey;"
                                        "padding: 2px;"
                                        "border-radius: 10px;"
                                        "border: 3px solid slategray;")
        # layouts boton 
        self.layout_boton = QHBoxLayout() 
        self.layout_boton.addStretch(1)
        self.layout_boton.addWidget(self.boton_volver)
        self.layout_boton.addStretch(1)
        
        # layout principal que contendra los demas widgets
        self.label_puntajes = QVBoxLayout()
        self.label_puntajes.addStretch(1)
        self.label_puntajes.addWidget(self.label_titulo, Qt.AlignTop)
        self.label_puntajes.addStretch(1)
        self.senal_pedir_ranking.emit()
        self.label_puntajes.setAlignment(Qt.AlignCenter)
        self.label_puntajes.addStretch(1)
        self.label_puntajes.addLayout(self.layout_boton)
        self.setLayout(self.label_puntajes)
    
    # cada vez que abrimos el ranking, el metodo mostrar ranking actualizara los top 5 jugadores
    def mostrar_ranking(self, ranking):
        for usuario, puntaje in ranking:
            self.label_usuario = QLabel(f'{usuario}', self)
            self.label_usuario.setStyleSheet("font-weight: bold;"
                                             "font-size: 20px;")
            self.label_puntaje = QLabel(f'{puntaje}', self)
            self.label_puntaje.setStyleSheet("color: red;"
                                            "font-size: 20px;"
                                            "font-weight: bold;")
            self.layout_datos = QHBoxLayout()
            self.layout_datos.addStretch()
            self.layout_datos.addWidget(self.label_usuario)
            self.layout_datos.addStretch()
            self.layout_datos.addWidget(self.label_puntaje)
            self.layout_datos.addStretch()
            
            self.label_puntajes.addLayout(self.layout_datos, Qt.AlignTop)
            
    def abrir(self):
        self.show()
        self.musica.setMedia(QMediaContent(QUrl.fromLocalFile(p.RUTA_MUSICA)))
        self.musica.play()
        self.mostrar_elementos()
        

    def volver_ventana_inicio(self):
        self.musica.stop()
        self.hide()
        self.senal_volver_ventana_inicio.emit()


        
        



        