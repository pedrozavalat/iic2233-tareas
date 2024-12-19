import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from os.path import join
from funciones_utiles import cargar_data_json
from random import choice
from backend.elementos_del_juego import Carta

window_name, base_class = uic.loadUiType(join(*cargar_data_json("RUTA_VENTANA_JUEGO")))

"""
Ventana que permita la interaccion del jugador contra su oponente, realizando cambios en 
la interfaz con respecto a las acciones del jugador. 
"""

class VentanaJuego(window_name, base_class):
    senal_solicitar_cartas_interfaz = pyqtSignal(dict)
    senal_notificar_carta_elegida = pyqtSignal(dict)
    senal_sacar_nueva_carta = pyqtSignal(Carta)
    senal_guardar_jugadores = pyqtSignal(str, str)
    senal_empezar_siguiente_ronda = pyqtSignal()
    senal_solicitar_tablero = pyqtSignal()
    senal_ver_baraja_oponente = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Ventana de Juego")
        self.move(0, 0)
        self.init_gui()
        self.botones_cartas = {}
        self.jugador = ''
        self.oponente = ''
        self.baraja_actual = None
        self.ronda_actual = 0
        self.pos_fichas_jugador = {
            'fuego': (50, 40),
            'agua': (110, 40),
            'nieve': (170, 40)}
        self.pos_fichas_oponente = {
            'fuego': (780, 40),
            'agua': (840, 40),
            'nieve': (900, 40)}
        self.fichas_partida = []
        self.pos_y_fuego_jugador = 0 # No habia otra manera mas que esta que me resultara xd
        self.pos_y_agua_jugador = 0
        self.pos_y_nieve_jugador = 0
        self.pos_y_fuego_oponente = 0
        self.pos_y_agua_oponente = 0
        self.pos_y_nieve_oponente = 0
        self.segundos_de_espera = 0 
        self.labels_cartas_oponente = [
            self.carta_1_oponente,
            self.carta_2_oponente,
            self.carta_3_oponente,
            self.carta_4_oponente,
            self.carta_5_oponente,]
        self.cartas_oponente = []
    
    def init_gui(self):
        self.label_carta_jugador.hide()
        self.label_carta_oponente.hide()
        self.boton_seleccionar.clicked.connect(self.carta_seleccionada)
        self.carta_elegida = None

        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_JUEGO"))]
        self.timer_ronda = QTimer()
        self.timer_ronda.setInterval(1000) 
        self.timer_ronda.timeout.connect(self.mostrar_timer_ronda)

        self.timer_preparando_sig_ronda = QTimer()
        self.timer_preparando_sig_ronda.setInterval(1000)
        self.timer_preparando_sig_ronda.timeout.connect(self.preprarando_sig_ronda)

        self.timer_ocultar_baraja_oponente = QTimer()
        self.timer_ocultar_baraja_oponente.setInterval(3000)
        self.timer_ocultar_baraja_oponente.setSingleShot(True)
        self.timer_ocultar_baraja_oponente.timeout.connect(self.ocultar_baraja_oponente)

    def recibir_cartas(self, cartas_interfaz):
        self.baraja_actual = cartas_interfaz
        pos_x = 70
        for index, carta in enumerate(cartas_interfaz):
            boton_carta = QPushButton('', self)
            boton_carta.setGeometry(pos_x, 590, 90, 105)
            ruta_carta = cargar_data_json("RUTA_CARTAS") + carta.obtener_ruta()
            boton_carta.setIcon(QIcon(join(*ruta_carta)))
            boton_carta.setIconSize(QSize(90, 105))
            boton_carta.setVisible(True)
            boton_carta.setAccessibleName(f'boton_{index}')
            pos_x += 80
            self.botones_cartas[index] = boton_carta
        for carta_tablero in self.botones_cartas.values():
            carta_tablero.clicked.connect(self.recibir_notificacion_boton)

    def actualizar_tablero(self, cartas_interface):
        for index, boton in self.botones_cartas.items():
            ruta_carta = cargar_data_json("RUTA_CARTAS") + cartas_interface[index].obtener_ruta()
            boton.setIcon(QIcon(join(*ruta_carta)))
            boton.setVisible(True)
            boton.setEnabled(True)
        self.carta_elegida = None
    
    def actualizar_ronda(self):
        self.label_ronda_actual.setText(str(self.ronda_actual))
        self.label_tiempo_ronda.setText(str(20))
        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_JUEGO"))]
        self.timer_ronda.start()
        self.label_carta_jugador.hide()
        self.label_carta_oponente.hide()
        self.label_carta_jugador.setPixmap(QPixmap(join(*cargar_data_json("RUTA_CARTA_BACK"))))
        self.label_carta_oponente.setPixmap(QPixmap(join(*cargar_data_json("RUTA_CARTA_BACK"))))
        self.boton_seleccionar.setEnabled(True)
        
    def actualizar_mazo_triunfo_jugador(self, elemento, ruta_ficha):
        # Variamos la posicion de la ficha de 10 en 10
        label_ficha = QLabel('', self)
        if elemento == "fuego":
            pos_x, pos_y = self.pos_fichas_jugador['fuego']
            pos_y += self.pos_y_fuego_jugador
            self.pos_y_fuego_jugador += 10
        elif elemento == "agua":
            pos_x, pos_y = self.pos_fichas_jugador['agua']
            pos_y += self.pos_y_agua_jugador
            self.pos_y_agua_jugador += 10
        elif elemento == "nieve":
            pos_x, pos_y = self.pos_fichas_jugador['nieve']
            pos_y += self.pos_y_nieve_jugador
            self.pos_y_nieve_jugador += 10
        label_ficha.setGeometry(pos_x, pos_y, 50, 50)
        label_ficha.setPixmap(QPixmap(join(*(cargar_data_json("RUTA_FICHAS") + ruta_ficha))))
        label_ficha.setScaledContents(True)
        label_ficha.move(pos_x, pos_y)
        label_ficha.setVisible(True)
        self.fichas_partida.append(label_ficha)
    
    def actualizar_mazo_triunfo_oponente(self, elemento, ruta_ficha):
        label_ficha = QLabel('', self)
        if elemento == "fuego":
            pos_x, pos_y = self.pos_fichas_oponente['fuego']
            pos_y += self.pos_y_fuego_oponente
            self.pos_y_fuego_oponente += 10
        elif elemento == "agua":
            pos_x, pos_y = self.pos_fichas_oponente['agua']
            pos_y += self.pos_y_agua_oponente
            self.pos_y_agua_oponente += 10
        elif elemento == "nieve":
            pos_x, pos_y = self.pos_fichas_oponente['nieve']
            pos_y += self.pos_y_nieve_oponente
            self.pos_y_nieve_oponente += 10
        label_ficha.setGeometry(pos_x, pos_y, 50, 50)
        label_ficha.setPixmap(QPixmap(join(*(cargar_data_json("RUTA_FICHAS") + ruta_ficha))))
        label_ficha.setScaledContents(True)
        label_ficha.move(pos_x, pos_y)
        label_ficha.setVisible(True)
        self.fichas_partida.append(label_ficha)
        
    def comenzar_juego(self):
        datos = {"comando": "get_penguins",
                "usuario": self.jugador}
        self.senal_solicitar_cartas_interfaz.emit(datos)

    def recibir_notificacion_boton(self):
        self.carta_elegida = self.sender().accessibleName()

    def carta_seleccionada(self):
        # Bloqueamos las cartas al momento de confirmar la carta por parte
        # del jugador
        if self.carta_elegida: 
            
            self.bloquear_tablero()
            # Obtenemos el objeto de la carta elegida
            index = int(self.carta_elegida[(self.carta_elegida.find("_") + 1):])
            self.carta_elegida = self.baraja_actual[index]
            self.notificar_seleccion_jugador()
            self.informar_carta_elegida()
            self.boton_seleccionar.setEnabled(False)
    
    def bloquear_tablero(self):
        for carta in self.botones_cartas.values():
                carta.setEnabled(False)

    def informar_carta_elegida(self):
        # Cualquier carta que saque en todo tipo de caso, va a llegar a este metodo
        datos = {
            "comando": "notificar_carta_elegida",
            "usuario": self.jugador,
            "ruta carta": self.carta_elegida.obtener_ruta(),
            "elemento": self.carta_elegida.elemento,
            "color": self.carta_elegida.color,
            "poder": self.carta_elegida.poder}
        # Borramos la carta elegida de la interfaz, y sacamos otras de las cartas
        # que tenemos en el mazo
        self.senal_sacar_nueva_carta.emit(self.carta_elegida)
        self.senal_notificar_carta_elegida.emit(datos)

    def notificar_seleccion_oponente(self):
        self.label_carta_oponente.show()

    def notificar_seleccion_jugador(self):
        ruta_carta = cargar_data_json("RUTA_CARTAS") + self.carta_elegida.obtener_ruta()
        self.label_carta_jugador.setPixmap(QPixmap(join(*ruta_carta)))
        self.label_carta_jugador.setVisible(True)
        self.label_carta_jugador.show()

    def ilustrar_cartas_jugadores(self, ruta_carta_oponente):
        self.label_carta_oponente.setPixmap(QPixmap(
            join(*(cargar_data_json("RUTA_CARTAS") + ruta_carta_oponente))))
        self.label_carta_oponente.setScaledContents(True)
        self.label_carta_oponente.show()
        
    def start_tiempo_ronda(self):
        self.timer_ronda.start()
    
    def stop_tiempo_ronda(self):
        self.timer_ronda.stop()
        
    def mostrar_timer_ronda(self):
        segundo = self.tiempo.pop() 
        self.label_tiempo_ronda.setText(f'{segundo}')
        if segundo == 0:
            self.stop_tiempo_ronda()
            self.bloquear_tablero()

            if self.carta_elegida is None:
                # Sacamos una carta de la baraja aleatoriamente
                self.carta_elegida = choice(self.baraja_actual)
                self.notificar_seleccion_jugador()
                self.informar_carta_elegida()

    def actualizar_baraja_actual(self, nueva_baraja):
        self.baraja_actual = nueva_baraja

    def preparar_siguiente_ronda(self):
        self.timer_preparando_sig_ronda.start()

    def preprarando_sig_ronda(self):
        # Metodo que nos permite que la ventana se congele por unos 3 segundos,
        # asi los jugadores ven mejor el resultado de quien gano. 
        self.segundos_de_espera += 1
        if self.segundos_de_espera == 1: 
            self.segundos_de_espera = 0
            self.timer_preparando_sig_ronda.stop()
            self.ronda_actual += 1
            self.senal_empezar_siguiente_ronda.emit()

    def mostrar(self, jugador, oponente):
        self.show()
        self.jugador = jugador
        self.oponente = oponente
        self.label_jugador.setText(jugador)
        self.label_oponente.setText(oponente)
        self.senal_guardar_jugadores.emit(jugador, oponente)
        self.comenzar_juego()

    def ocultar(self):
        self.hide()

    def salir(self):
        self.close()

    def reset(self):
        self.botones_cartas = {}
        self.jugador = ''
        self.oponente = ''
        self.baraja_actual = None
        self.ronda_actual = 0
        self.pos_y_fuego_jugador = 0 
        self.pos_y_agua_jugador = 0
        self.pos_y_nieve_jugador = 0
        self.pos_y_fuego_oponente = 0
        self.pos_y_agua_oponente = 0
        self.pos_y_nieve_oponente = 0
        self.segundos_de_espera = 0 
        for fichas in self.fichas_partida:
            fichas.setVisible(False)
        self.fichas_partida.clear()
        self.label_carta_jugador.hide()
        self.label_carta_oponente.hide()
        self.tiempo = [seg for seg in range(cargar_data_json("CUENTA_REGRESIVA_JUEGO"))]
        
    def mostrar_baraja_oponente(self, cartas_oponente):
        self.cartas_oponente = cartas_oponente
        cartas_y_rutas_oponente = zip(self.labels_cartas_oponente, cartas_oponente)
        for label_carta, ruta in cartas_y_rutas_oponente:
            ruta_carta = join(*(cargar_data_json("RUTA_CARTAS") + ruta))
            label_carta.setPixmap(QPixmap(ruta_carta))
            label_carta.setScaledContents(True)
            label_carta.setVisible(True)
        self.timer_ocultar_baraja_oponente.start()

    def ocultar_baraja_oponente(self):
        for label_carta_oponente in self.labels_cartas_oponente:
            label_carta_oponente.setPixmap(QPixmap(join(*cargar_data_json("RUTA_CARTA_BACK"))))
    
    def keyPressEvent(self, event):
        if event.text() in ['v', 'e', 'o']:
            self.senal_ver_baraja_oponente.emit(event.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaJuego()
    sys.exit(app.exec_())