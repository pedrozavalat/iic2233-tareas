"""
Modulo que presenta la clase Carta, en donde presenta como atributos
los colores de la carta, el elemento, y su poder respectivo. Asimismo, 
nos permite obtener su ruta para despues utilizarla al momento de actualizar la 
interfaces de los jugadores. 
"""

class Carta:
    def __init__(self, color, elemento, poder):
        self.color = color
        self.elemento = elemento
        self.poder = poder

    def obtener_ruta(self):
        return ["{}_{}_{}.png".format(
            self.color,
            self.elemento,
            self.poder)]