from PyQt5.QtCore import QObject
import parametros as p 


# Plantas
class Girasol(QObject):

    def __init__(self, pos, tipo):
        super().__init__()
        self.posicion = pos
        self.tipo = tipo
        self.lanza_proyectil = False
        self._vida = p.VIDA_PLANTA
        self.primer_movimiento = True
        self.movimiento_1 = p.RUTA_ICON_GIRASOL
        self.movimiento_2 = p.RUTA_ICON_GIRASOL_2
        self.soles = set()

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor

class PlantasVerdes(QObject):

    def __init__(self, pos, tipo):
        super().__init__()
        self.posicion = pos
        self.tipo = tipo
        self.lanza_proyectil = True
        self._vida = p.VIDA_PLANTA
        self.proyectiles = set()
        self.primer_movimiento = True
        self.segundo_movimiento = False
        self.movimiento_1 = p.RUTA_ICON_LANZAGUI_NORMAL
        self.movimiento_2 = p.RUTA_ICON_LANZAGUI_NORMAL_2
        self.movimiento_3 = p.RUTA_ICON_LANZAGUI_NORMAL_3
    
    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor
            

class PlantasAzules(QObject):

    def __init__(self, pos, tipo):
        super().__init__()
        self.posicion = pos
        self.tipo = tipo
        self.lanza_proyectil = True
        self._vida = p.VIDA_PLANTA
        self.proyectiles = set()
        self.primer_movimiento = True
        self.segundo_movimiento = False
        self.tercer_movimiento = False
        self.movimiento_1 = p.RUTA_ICON_LANZAGUI_HIELO
        self.movimiento_2 = p.RUTA_ICON_LANZAGUI_HIELO_2
        self.movimiento_3 = p.RUTA_ICON_LANZAGUI_HIELO_3

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor
    
    def perder_vida(self):
        self.timer_quitar_vida.start()

    def quitar_vida(self):
        self.vida -= p.DANO_MORDIDA
        if self.vida <= 0:
            self.timer_quitar_vida.stop()

class Patatas(QObject):

    def __init__(self, pos, tipo):
        super().__init__()
        self.posicion = pos
        self.tipo = tipo
        self.lanza_proyectil = False
        self._vida = p.VIDA_PLANTA * 2
        self.primer_movimiento = True
        self.segundo_movimiento = False
        self.movimiento_1 = p.RUTA_ICON_PATATA
        self.movimiento_2 = p.RUTA_ICON_PATATA_2
        self.movimiento_3 = p.RUTA_ICON_PATATA_3

    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            self._vida = 0
        else:
            self._vida = valor
