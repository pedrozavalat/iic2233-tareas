from random import randint, choice
from parametros import MIN_AUMENTO_EXPERIENCIA, MAX_AUMENTO_EXPERIENCIA, \
                        MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO, \
                        AUMENTAR_VELOCIDAD_AGUA, AUMENTAR_VIDA_PLANTA, \
                        AUMENTAR_ATAQUE_FUEGO
from abc import ABC, abstractmethod
# clase abstracta Programon, define todas las caracteristicas de un programon. 
# Al mismo tiempo, hereda las subclases Agua, Fuego, y Planta (las cuales son 
# instanciadas)


class Programon(ABC):
    def __init__(self, nombre, tipo, nivel, vida, ataque, defensa, velocidad):
        self.nombre = nombre
        self.tipo = tipo
        self._vida = vida
        self._nivel = nivel
        self._ataque = ataque
        self._defensa = defensa
        self._velocidad = velocidad
        self._experiencia = 0
    # definimos como property todas las caracteristicas de un programon, dado que
    # estas poseen un valor minimo y maximo.   
    # luchar: metodo que retorna el programon ganador en una partida, el cual depende
    #         segun el tipo de programon (Planta, Fuego, Agua)
    @abstractmethod
    def luchar(self, rival): 
        pass

    @abstractmethod
    def ventaja(self, rival):
        pass

    def entrenamiento(self):
        self.experiencia += randint(MIN_AUMENTO_EXPERIENCIA, MAX_AUMENTO_EXPERIENCIA)
    # calcular_puntaje: Método que calcula el puntaje victoria cuyo define el programon
    #                   ganador en una partida. 
    def calcular_puntaje(self, otro):
        ventaja = self.ventaja(otro)
        puntaje_victoria = max(0, (self.vida * 0.2 + self.nivel * 0.3 \
            + self.ataque * 0.15 + self.defensa * 0.15 \
            + self.velocidad * 0.2 + ventaja * 40))
        return puntaje_victoria

    def subir_nivel(self):
        if self.nivel < 100:
            self.nivel += 1
            self.vida += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO) 
            self.ataque += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO) 
            self.defensa += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO) 
            self.velocidad += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO) 
        elif self.nivel == 100:
            self.experiencia = 0
    
    @property
    def nivel(self):
        return self._nivel
    @nivel.setter
    def nivel(self, valor):
        if valor > 100:
            self._nivel = 100
        else:
            self._nivel = valor
            
    @property
    def vida(self):
        return self._vida
    @vida.setter
    def vida(self, valor):
        if valor > 255:
            self._vida = 255
        elif valor < 1:
            self._vida = 1
        else:
            self._vida = valor

    @property
    def defensa(self):
        return self._defensa
    @defensa.setter
    def defensa(self, valor):
        if valor > 250:
            self._defensa = 250
        elif valor < 5:
            self._defensa = 5
        else:
            self._defensa = valor

    @property
    def ataque(self):
        return self._ataque
    @ataque.setter
    def ataque(self, valor):
        if valor > 190:
            self._ataque = 190
        elif valor < 5:
            self._ataque = 5
        else:
            self._ataque = valor
        
    @property
    def experiencia(self):
        return self._experiencia
    @experiencia.setter
    def experiencia(self, valor):
        if valor > 100:
            self.subir_nivel() # si su experiencia llega a 100, sube de nivel
            self._experiencia = abs(100 - valor) 
        elif valor < 0:
            self._experiencia = 0
        else:
            self._experiencia = valor
   
    @property
    def velocidad(self):
        return self._velocidad
    @velocidad.setter
    def velocidad(self, valor):
        if valor > 200:
            self._velocidad = 200
        else:
            self._velocidad = valor
    

class Planta(Programon):
    def __init__(self, *args):
        super().__init__(*args)
    
    def luchar(self, rival):
        puntaje_programon = self.calcular_puntaje(rival)
        puntaje_rival = rival.calcular_puntaje(self)
        # gana mi programon
        if puntaje_programon > puntaje_rival:
            self.velocidad += AUMENTAR_VIDA_PLANTA
            return self
        elif puntaje_programon > puntaje_rival:
            return rival 
        else:
            return choice([self, rival]) 

    def ventaja(self, rival):
        if self.tipo == rival.tipo:
            return 0
        elif rival.tipo == "Agua":
            return 1
        elif rival.tipo == "Fuego":
            return -1


class Agua(Programon):
    def __init__(self, *args):
        super().__init__(*args)
    
    def luchar(self, rival):
        puntaje_programon = self.calcular_puntaje(rival)
        puntaje_rival = rival.calcular_puntaje(self)
        # gana mi programon
        if puntaje_programon > puntaje_rival:
            self.velocidad += AUMENTAR_VELOCIDAD_AGUA
            return self
        elif puntaje_programon > puntaje_rival:
            return rival 
        else:
            return choice([self, rival]) 

    def ventaja(self, rival):
        if self.tipo == rival.tipo:
            return  0
        elif rival.tipo == "Fuego":
            return 1
        elif rival.tipo == "Planta":
            return -1

class Fuego(Programon):
    def __init__(self, *args):
        super().__init__(*args)

    def luchar(self, rival):
        puntaje_programon = self.calcular_puntaje(rival)
        puntaje_rival = rival.calcular_puntaje(self)
        # gana mi programon
        if puntaje_programon > puntaje_rival:
            self.velocidad += AUMENTAR_ATAQUE_FUEGO
            return self
        elif puntaje_programon > puntaje_rival:
            return rival 
        else:
            return choice([self, rival]) 

    def ventaja(self, rival):
        if self.tipo == rival.tipo:
            return 0
        elif rival.tipo == "Planta":
            return 1
        elif rival.tipo == "Agua":
            return -1 
            
        
