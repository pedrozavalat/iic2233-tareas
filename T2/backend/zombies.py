from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import parametros as p 
from math import ceil

        
class ZombieClasico(QObject):

    def __init__(self, posicion):
        super().__init__()
        self._vida = p.VIDA_ZOMBIE
        self._velocidad = p.VELOCIDAD_ZOMBIE
        self.dano = p.DANO_MORDIDA
        self.posicion = posicion 
        self.tipo = "walker"
        self.primera_caminata = True
        self.mov_comiendo_1 = True
        self.mov_comiendo_2 = False
        self.caminata_1 = p.RUTA_ICON_ZOMBIE_WALKER
        self.caminata_2 = p.RUTA_ICON_ZOMBIE_WALKER_2
        self.comiendo_1 = p.RUTA_ICON_ZOMBIE_WALKER_EAT
        self.comiendo_2 = p.RUTA_ICON_ZOMBIE_WALKER_EAT_2
        self.comiendo_3 = p.RUTA_ICON_ZOMBIE_WALKER_EAT_3
        self.label_zombie = QLabel('')
        self.label_zombie.setPixmap(QPixmap(self.caminata_1))
        self.label_zombie.setScaledContents(True)
        self.label_zombie.resize(60, 70)
        self.label_zombie.move(self.posicion.x(), self.posicion.y())

        self.timer_caminata = QTimer()
        self.timer_caminata.setInterval(ceil(self.velocidad // 15)) 
        self.timer_caminata.timeout.connect(self.caminata)

        self.timer_desplazamiento = QTimer()
        self.timer_desplazamiento.setInterval(ceil(150 - self.velocidad // 100))
        self.timer_desplazamiento.timeout.connect(self.desplazamiento)

        self.timer_mordida = QTimer()
        self.timer_mordida.setInterval(ceil(self.velocidad))
        self.timer_mordida.setSingleShot(True)
        self.timer_mordida.timeout.connect(self.comiendo)

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor
    
    @property
    def velocidad(self):
        return self._velocidad
    @velocidad.setter
    def velocidad(self, valor):
        if valor < p.VELOCIDAD_ZOMBIE * p.RALENTIZAR_ZOMBIE:
            self._velocidad = p.VELOCIDAD_ZOMBIE * p.RALENTIZAR_ZOMBIE
    
    def desplazamiento(self):
        self.posicion.moveTo(self.posicion.x() - 2, self.posicion.y())
        self.label_zombie.move(self.posicion.x() - 2, self.posicion.y())
    
    def caminata(self):
        if self.primera_caminata:
            self.label_zombie.setPixmap(QPixmap(self.caminata_1))
            self.primera_caminata = False
        else:
            self.label_zombie.setPixmap(QPixmap(self.caminata_2))
            self.primera_caminata = True

    def comiendo(self):
        if self.mov_comiendo_1:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_1))
            self.mov_comiendo_1 = False
            self.mov_comiendo_2 = True
        elif self.mov_comiendo_2:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_2))
            self.mov_comiendo_2 = False
        else:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_3))
            self.mov_comiendo_1 = True

    def ralentizacion(self):
        self.velocidad *= p.RALENTIZAR_ZOMBIE
        self.timer_desplazamiento.setInterval(150 + ceil(self.velocidad // 100))

    def mover(self):
        self.timer_caminata.start()
        self.timer_desplazamiento.start()

    def detener(self):
        self.timer_caminata.stop()
        self.timer_desplazamiento.stop()


class ZombieRapido(QObject):

    def __init__(self, posicion):
        super().__init__()
        self._vida = p.VIDA_ZOMBIE
        self._velocidad = p.VELOCIDAD_ZOMBIE * 1.5
        self.dano = p.DANO_MORDIDA
        self.tipo = "runner"
        self.primera_caminata = True
        self.mov_comiendo_1 = True
        self.mov_comiendo_2 = False
        self.caminata_1 = p.RUTA_ICON_ZOMBIE_RUNNER
        self.caminata_2 = p.RUTA_ICON_ZOMBIE_RUNNER_2
        self.comiendo_1 = p.RUTA_ICON_ZOMBIE_RUNNER_EAT
        self.comiendo_2 = p.RUTA_ICON_ZOMBIE_RUNNER_EAT_2
        self.comiendo_3 = p.RUTA_ICON_ZOMBIE_RUNNER_EAT_3
        self.posicion = posicion 
        self.label_zombie = QLabel('')
        self.label_zombie.setPixmap(QPixmap(self.caminata_1))
        self.label_zombie.setScaledContents(True)
        self.label_zombie.resize(68, 70)
        self.label_zombie.move(self.posicion.x(), self.posicion.y())

        self.timer_caminata = QTimer()
        self.timer_caminata.setInterval(ceil(self.velocidad // 15)) 
        self.timer_caminata.timeout.connect(self.caminata)

        self.timer_desplazamiento = QTimer()
        self.timer_desplazamiento.setInterval(ceil(150 - self.velocidad // 100))
        self.timer_desplazamiento.timeout.connect(self.desplazamiento)
        
        self.timer_mordida = QTimer()
        self.timer_mordida.setInterval(ceil(self.velocidad))
        self.timer_mordida.setSingleShot(True)
        self.timer_mordida.timeout.connect(self.comiendo)

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor
    
    @property
    def velocidad(self):
        return self._velocidad
    @velocidad.setter
    def velocidad(self, valor):
        if valor < p.VELOCIDAD_ZOMBIE * 1.5 * p.RALENTIZAR_ZOMBIE:
            self._velocidad = p.VELOCIDAD_ZOMBIE * 1.5 * p.RALENTIZAR_ZOMBIE

    def caminata(self):
        if self.primera_caminata:
            self.label_zombie.setPixmap(QPixmap(self.caminata_1))
            self.primera_caminata = False
        else:
            self.label_zombie.setPixmap(QPixmap(self.caminata_2))
            self.primera_caminata = True

    def desplazamiento(self):
        self.posicion.moveTo(self.posicion.x() - 2, self.posicion.y())
        self.label_zombie.move(self.posicion.x() - 2, self.posicion.y())
    
    def comiendo(self):
        if self.mov_comiendo_1:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_1))
            self.mov_comiendo_1 = False
            self.mov_comiendo_2 = True
        elif self.mov_comiendo_2:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_2))
            self.mov_comiendo_2 = False
        else:
            self.label_zombie.setPixmap(QPixmap(self.comiendo_3))
            self.mov_comiendo_1 = True

    def ralentizacion(self):
        self.velocidad *= p.RALENTIZAR_ZOMBIE
        self.timer_desplazamiento.setInterval(ceil(150 + self.velocidad // 100))
        
        
    def mover(self):
        self.timer_caminata.start()
        self.timer_desplazamiento.start()
        
    def detener(self):
        self.timer_caminata.stop()
        self.timer_desplazamiento.stop()