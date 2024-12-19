from abc import ABC, abstractmethod
from random import randint
from parametros import AUMENTO_DEFENSA

# clase Entrenador: define los atributoa de cada entrenador del DCCampeonato
class Entrenador:
    def __init__(self, nombre, programones, energia, objetos):
        self.nombre = nombre
        self._energia = energia
        self.programones = programones
        self.objetos = objetos
    
    @property
    def energia(self):
        return self._energia
    @energia.setter
    def energia(self, valor):
        if valor < 0:
            self._energia = 0
        elif valor > 100:
            self._energia = 100
        else:
            self._energia = valor
        

# clase abstracta Objetos que hereda las subclases Baya, Pocion y Caramelo
class Objetos(ABC):
    def __init__(self, nombre, tipo_objeto, costo, probabilidad_exito):
        self.nombre = nombre
        self.tipo = tipo_objeto
        self.costo = costo
        self.probabilidad_exito = probabilidad_exito
    
    @abstractmethod
    def aplicar_objeto(self, programon):
        pass


class Baya(Objetos):
    def __init__(self, *args):
        super().__init__(*args)
    
    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        vida_programon = programon.vida # vida inicial 
        aumento_vida = randint(1, 10)
        programon.vida += aumento_vida # vida aumentada
        # el entrenador pierde energia
        print(
            f"Aumento vida: {aumento_vida}\n"
            f"La vida subió de {vida_programon} a {programon.vida}\n")


class Pocion(Objetos):
    def __init__(self, *args):
        super().__init__(*args)
    
    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        ataque_programon = programon.ataque # ataque inicial
        aumento_ataque = randint(1, 7)
        programon.ataque += aumento_ataque # ataque aumentado
        print(
            f"Aumento ataque: {aumento_ataque}\n"
            f"El ataque subió de {ataque_programon} a {programon.ataque}\n")

    
class Caramelo(Baya, Pocion):
    def __init__(self, *args):
        super().__init__(*args)

    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        defensa_programon = programon.defensa
        programon.defensa += AUMENTO_DEFENSA
        print(
            f"Aumento defensa: {AUMENTO_DEFENSA}\n"
            f"El ataque subió de {defensa_programon} a {programon.defensa}\n")
