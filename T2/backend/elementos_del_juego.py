from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import parametros as p 
from random import randint


# Elementos respectivos de cada planta 
class Soles(QObject):
    def __init__(self, posicion):
        super().__init__()
        self.label_sol = QLabel('')
        self.label_sol.setPixmap(QPixmap(p.RUTA_ICON_SOL))
        self.label_sol.setScaledContents(True)
        self.label_sol.resize(31, 31)
        self.posicion = posicion
        self.pos_x = posicion.x()
        self.pos_y = posicion.y()
    
    def posicionar_alrededor_girasol(self):
        self.pos_x = randint(self.posicion.x() - 10, self.posicion.x() + 10)
        self.pos_y = randint(self.posicion.y() - 10, self.posicion.y() + 10)
        self.label_sol.move(self.pos_x, self.pos_y)
        self.posicion.moveTo(self.pos_x, self.pos_y)

class ProyectilVerde(QObject):
    def __init__(self, posicion):
        super().__init__()
        self.movimiento_1 = p.RUTA_ICON_PROYECTIL_VERDE
        self.movimiento_2 = p.RUTA_ICON_PROYECTIL_VERDE_2
        self.movimiento_3 = p.RUTA_ICON_PROYECTIL_VERDE_3
        self.segundo_movimiento = True
        self.tercer_movimiento = False
        self.tipo = "verde"
        self.label = QLabel('')
        self.label.setPixmap(QPixmap(self.movimiento_1))
        self.label.setScaledContents(True)
        self.label.resize(30, 40)
        self.posicion = posicion
        # ajustamos la posicion para un disparo mas fluido
        self.posicion.moveTo(self.posicion.x() + 50, self.posicion.y())
        self.label.move(self.posicion.x(), self.posicion.y())

        self.timer_mover_proyectil = QTimer()
        self.timer_mover_proyectil.setInterval(16)
        self.timer_mover_proyectil.timeout.connect(self.mover)

    def mover(self):
        self.posicion.moveTo(self.posicion.x() + 1, self.posicion.y())
        self.label.move(self.posicion.x() + 1, self.posicion.y())    


class ProyectilAzul(QObject):
    def __init__(self, posicion):
        super().__init__()
        self.movimiento_1 = p.RUTA_ICON_PROYECTIL_AZUL
        self.movimiento_2 = p.RUTA_ICON_PROYECTIL_AZUL_2
        self.movimiento_3 = p.RUTA_ICON_PROYECTIL_AZUL_3
        self.posicion = posicion 
        self.tipo = "azul"
        self.label = QLabel('')
        self.label.setPixmap(QPixmap(self.movimiento_1))
        self.label.setScaledContents(True)
        self.label.resize(40, 40)
        # ajustamos la posicion para un disparo mas fluido
        self.posicion.moveTo(self.posicion.x() + 50, self.posicion.y())
        self.label.move(self.posicion.x(), self.posicion.y())

        self.timer_mover_proyectil = QTimer()
        self.timer_mover_proyectil.setInterval(16)
        self.timer_mover_proyectil.timeout.connect(self.mover)

    def mover(self):
        self.posicion.moveTo(self.posicion.x() + 1, self.posicion.y())
        self.label.move(self.posicion.x() + 1, self.posicion.y())

   