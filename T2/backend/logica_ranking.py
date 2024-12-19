from PyQt5.QtCore import QObject, pyqtSignal

class LogicaRanking(QObject):

    senal_enviar_ranking = pyqtSignal(list)

    def __init__(self):
        super().__init__()
    # Método que actualiza el ranking cada vez que se consulta por aquel.
    def generar_ranking(self):
        def por_puntaje(lista):
                    return lista[1] * -1
        ranking = []

        with open('puntajes.txt', 'r', encoding = 'utf-8') as puntajes:
            puntajes = puntajes.readlines()
            for puntaje in puntajes:
                puntaje = puntaje.strip("\n").split(",")
                usuario, puntos = puntaje[0], int(puntaje[1])
                ranking.append([usuario, puntos])
        ranking.sort(key = por_puntaje)
        ranking = ranking[:5]
        # Señal que actualiza el ranking en la Ventana del ranking.
        self.senal_enviar_ranking.emit(ranking)



    