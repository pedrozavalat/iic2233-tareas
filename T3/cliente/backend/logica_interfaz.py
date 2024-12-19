from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_espera import VentanaEspera
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_final import VentanaFinal
from frontend.ventana_error import VentanaError
from frontend.ventana_chat import VentanaChat
from PyQt5.QtCore import pyqtSignal, QObject
from funciones_utiles import cargar_data_json
from backend.elementos_del_juego import Carta
from collections import deque
from threading import Lock

"""
Modulo que permite la interaccion entre la logica del juego con las interfaces del cliente. 
En este sentido, permite interfactuar tanto con su interfaz, con el servidor, y otros 
usuarios. 
"""

class Interfaz(QObject):

    senal_cerrar_ventana_inicio = pyqtSignal()
    senal_cerrar_ventana_espera = pyqtSignal()
    senal_mostrar_ventana_espera = pyqtSignal()
    senal_login_rechazado = pyqtSignal(str)
    senal_usuarios_en_espera = pyqtSignal(dict)
    senal_eliminar_label_usuario = pyqtSignal(str)
    senal_start_cuenta_regresiva = pyqtSignal()
    senal_start_tiempo_ronda = pyqtSignal()
    senal_actualizar_sala_espera = pyqtSignal(list, str)
    senal_mostrar_ventana_juego = pyqtSignal(str, str)
    senal_enviar_cartas = pyqtSignal(deque) 
    senal_mostrar_aviso_sala_llena = pyqtSignal()
    senal_mostrar_aviso_partida_existente = pyqtSignal()
    senal_avisar_seleccion_oponente = pyqtSignal()
    senal_mostrar_ambas_cartas = pyqtSignal(list)
    senal_stop_tiempo_ronda = pyqtSignal()
    senal_verificar_ganador_ronda = pyqtSignal(dict)
    senal_solicitar_mazo_triunfo = pyqtSignal(dict)
    senal_actualizar_mazo_triunfo_jugador = pyqtSignal(str, list)
    senal_actualizar_mazo_triunfo_oponente = pyqtSignal(str, list)
    senal_actualizar_ronda = pyqtSignal()
    senal_preparar_siguiente_ronda = pyqtSignal()
    senal_actualizar_tablero = pyqtSignal(deque)
    senal_actualizar_baraja = pyqtSignal(deque)
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_enviar_ganador_partida = pyqtSignal(str, str)
    senal_abrir_ventana_error = pyqtSignal()
    senal_reset_ventana_espera = pyqtSignal()
    senal_reset_ventana_juego = pyqtSignal()
    senal_abrir_ventana_chat = pyqtSignal(str)
    senal_cerrar_ventana_chat = pyqtSignal()
    senal_actualizar_chat = pyqtSignal(str, str)
    senal_veo = pyqtSignal(dict)
    senal_enviar_cartas_VEO = pyqtSignal(dict)
    senal_mostrar_cartas_tablero_oponente = pyqtSignal(list)
    

    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.acceder_comando = Lock()
        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()
        self.ventana_final = VentanaFinal()
        self.ventana_error = VentanaError()
        self.ventana_chat = VentanaChat()

        # ============================= Conexiones ==========================================
        # ------------------------- Señales Ventana Inicio ----------------------------------
        self.ventana_inicio.senal_enviar_login.connect(self.cliente.enviar_mensaje)
        
        # ------------------------- Señales Ventana Espera ----------------------------------
        self.ventana_espera.senal_volver_inicio.connect(self.ventana_inicio.mostrar)
        self.ventana_espera.senal_abrir_juego.connect(self.abrir_ventana_juego)
        self.ventana_espera.senal_actualizar_ventana_espera.connect(self.cliente.enviar_mensaje)

        # ------------------------- Señales Ventana Juego -----------------------------------
        self.ventana_juego.senal_solicitar_cartas_interfaz.connect(self.cliente.enviar_mensaje)
        self.ventana_juego.senal_sacar_nueva_carta.connect(self.sacar_nueva_carta)
        self.ventana_juego.senal_notificar_carta_elegida.connect(self.cliente.enviar_mensaje)
        self.ventana_juego.senal_guardar_jugadores.connect(self.guardar_jugadores)
        self.ventana_juego.senal_empezar_siguiente_ronda.connect(self.empezar_siguiente_ronda)
        self.ventana_juego.senal_ver_baraja_oponente.connect(self.cheatcode)
        # ------------------------- Señales Ventana Final -----------------------------------
        self.ventana_final.senal_volver_inicio.connect(self.ventana_inicio.mostrar)
        self.ventana_final.senal_enviar_ganador_partida.connect(self.cliente.enviar_mensaje)
        
        # ------------------------- Señales Ventana Error -----------------------------------
        self.ventana_error.senal_cerrar_aplicacion.connect(self.cliente.salir)
        
        # ------------------------- Señales Ventana Chat ------------------------------------
        self.ventana_chat.senal_enviar_mensaje.connect(self.cliente.enviar_mensaje)

        # =========================== Señales Interfaz ======================================
        # --------------------------- Señales Interfaz - V. Inicio --------------------------
        self.senal_login_rechazado.connect(self.ventana_inicio.login_rechazado)
        self.senal_cerrar_ventana_inicio.connect(self.ventana_inicio.salir)
        self.senal_mostrar_aviso_partida_existente.connect(
                                        self.ventana_inicio.mostrar_aviso_partida_existente)
        self.senal_mostrar_aviso_sala_llena.connect(
                                        self.ventana_inicio.mostrar_aviso_sala_llena)
        
        # --------------------------- Señales Interfaz - V.Espera ---------------------------
        self.senal_start_cuenta_regresiva.connect(self.ventana_espera.start_cuenta_regresiva)
        self.senal_actualizar_sala_espera.connect(self.ventana_espera.actualizar_ventana)
        self.senal_mostrar_ventana_espera.connect(self.ventana_espera.mostrar)
        self.senal_cerrar_ventana_espera.connect(self.ventana_espera.salir)
        self.senal_eliminar_label_usuario.connect(
                                        self.ventana_espera.eliminar_label_usuario_retirado)
        self.senal_reset_ventana_espera.connect(self.ventana_espera.reset)

        # --------------------------- Señales Interfaz - V.Juego ----------------------------
        self.senal_mostrar_ventana_juego.connect(self.ventana_juego.mostrar)
        self.senal_start_tiempo_ronda.connect(self.ventana_juego.start_tiempo_ronda)
        self.senal_stop_tiempo_ronda.connect(self.ventana_juego.stop_tiempo_ronda)
        self.senal_enviar_cartas.connect(self.ventana_juego.recibir_cartas)
        self.senal_avisar_seleccion_oponente.connect(
                                            self.ventana_juego.notificar_seleccion_oponente)
        self.senal_mostrar_ambas_cartas.connect(self.ventana_juego.ilustrar_cartas_jugadores)
        self.senal_actualizar_mazo_triunfo_jugador.connect(
                                        self.ventana_juego.actualizar_mazo_triunfo_jugador)
        self.senal_actualizar_mazo_triunfo_oponente.connect(
                                        self.ventana_juego.actualizar_mazo_triunfo_oponente)
        self.senal_preparar_siguiente_ronda.connect(self.ventana_juego.preparar_siguiente_ronda)
        self.senal_actualizar_ronda.connect(self.ventana_juego.actualizar_ronda)
        self.senal_actualizar_tablero.connect(self.ventana_juego.actualizar_tablero)
        self.senal_actualizar_baraja.connect(self.ventana_juego.actualizar_baraja_actual)
        self.senal_cerrar_ventana_juego.connect(self.ventana_juego.salir)
        self.senal_reset_ventana_juego.connect(self.ventana_juego.reset)
        self.senal_mostrar_cartas_tablero_oponente.connect(
                                                    self.ventana_juego.mostrar_baraja_oponente)
        
        # --------------------------- Señales Interfaz - V.Final ----------------------------
        self.senal_enviar_ganador_partida.connect(self.ventana_final.recibir_ganador)
        
        # --------------------------- Señales Interfaz - V.Error ----------------------------
        self.senal_abrir_ventana_error.connect(self.ventana_error.mostrar)
        
        # --------------------------- Señales Interfaz - V.Chat ----------------------------
        self.senal_abrir_ventana_chat.connect(self.ventana_chat.mostrar)
        self.senal_actualizar_chat.connect(self.ventana_chat.actualizar_bandeja_entrada)
        self.senal_cerrar_ventana_chat.connect(self.ventana_chat.salir)
        # --------------------------- Señales Interfaz - Servidor ---------------------------
        self.senal_usuarios_en_espera.connect(self.cliente.enviar_mensaje)
        self.senal_verificar_ganador_ronda.connect(self.cliente.enviar_mensaje)
        self.senal_solicitar_mazo_triunfo.connect(self.cliente.enviar_mensaje)
        self.senal_veo.connect(self.cliente.enviar_mensaje)
        self.senal_enviar_cartas_VEO.connect(self.cliente.enviar_mensaje)
        
        # ============================= Atributos del jugador ===============================
        self.cartas_jugador = deque()
        self.cartas_interface = deque()
        self.jugador = ''
        self.oponente = ''
        self.mazo_triunfo_partida = {}
        self.ganador_partida = None      
        self.secuencia_veo = ''  
        self.contador_veo = 0

    def mostrar_ventana_inicio(self):
        self.ventana_inicio.mostrar()

    def cerrar_ventana_inicio(self):
        self.senal_cerrar_ventana_inicio.emit()

    def abrir_ventana_juego(self, jugador, oponente):
        self.senal_cerrar_ventana_espera.emit()
        self.senal_mostrar_ventana_juego.emit(jugador, oponente)
        self.senal_abrir_ventana_chat.emit(jugador)

    def manejar_mensaje(self, mensaje_recibido):
        with self.acceder_comando:
            try:
                comando = mensaje_recibido["comando"]
            except KeyError:
                return {}
            
            if comando == "respuesta_login_verificado":
                if mensaje_recibido["verificacion"] == "aceptada":
                    # si el login fue aceptado, hay que verificar si la sala de espera 
                    # esta llena. 
                    enviar_mensaje = {"comando": "verificar_personas_en_espera"}
                    self.senal_usuarios_en_espera.emit(enviar_mensaje) 
                else:
                    error = mensaje_recibido["error"]
                    self.senal_login_rechazado.emit(error)

            elif comando == "respuesta_sala_espera":
                # En el caso que la sala de espera no este llena, puede acceder. 
                if mensaje_recibido["verificacion"] == "aceptada":
                    self.senal_mostrar_ventana_espera.emit()
                    self.senal_cerrar_ventana_inicio.emit()

            elif comando == "respuesta_sala_espera_llena":
                self.senal_mostrar_aviso_sala_llena.emit()
            
            elif comando == "respuesta_partida_existente":
                self.senal_mostrar_aviso_partida_existente.emit()
            
            elif comando == "actualizar_sala_espera":
                usuarios_en_sala_espera = mensaje_recibido["usuarios"]
                nombre_usuario = mensaje_recibido["nombre usuario"]
                self.senal_actualizar_sala_espera.emit(usuarios_en_sala_espera,
                                                        nombre_usuario)

            elif comando == "actualizar_label_usuario_saliendo":
                usuario_retirado = mensaje_recibido["usuario"]
                self.senal_eliminar_label_usuario.emit(usuario_retirado)

            elif comando == "activar_timer_sala_espera":
                self.senal_start_cuenta_regresiva.emit()
            
            elif comando == "get_penguins":
                dicc_cartas = mensaje_recibido["cartas"]
                self.cartas_interface = self.crear_instancia_carta(dicc_cartas)
                self.senal_enviar_cartas.emit(self.cartas_interface)
                self.senal_start_tiempo_ronda.emit()

            elif comando == "activar_seleccion_carta_oponente":                
                self.senal_avisar_seleccion_oponente.emit()

            elif comando == "mostrar_todas_las_cartas":
                carta_oponente = mensaje_recibido["carta oponente"]
                self.senal_mostrar_ambas_cartas.emit(carta_oponente)
                self.senal_stop_tiempo_ronda.emit()
                datos = {"comando": "solicitar_ganador_ronda"}
                self.senal_verificar_ganador_ronda.emit(datos)

            elif comando == "recibir_ganador_ronda":
                nombre_ganador = mensaje_recibido["ganador ronda"][0]
                # Actualizamos el mazo triunfo de la partida
                self.mazo_triunfo_partida = mensaje_recibido["mazo triunfo"]
                if nombre_ganador != "empate":
                    # Actualizamos la interfaz segun el ganador
                    elemento = mensaje_recibido["ganador ronda"][1]
                    color = mensaje_recibido["ganador ronda"][2]
                    ruta_ficha = "{}_{}.png".format(elemento, color)
                    if nombre_ganador == self.jugador:
                        self.senal_actualizar_mazo_triunfo_jugador.emit(elemento, [ruta_ficha])
                    elif nombre_ganador == self.oponente:
                        self.senal_actualizar_mazo_triunfo_oponente.emit(elemento, [ruta_ficha])
                elif nombre_ganador == "empate":
                    pass # En el caso de empate se sigue la ronda
                # En el caso que exista un ganador que cumpla las condiciones para ganar, termina
                # el juego y se abre la ventana final 
                if self.partida_ganada() is not None:
                    self.senal_stop_tiempo_ronda.emit()
                    self.senal_cerrar_ventana_juego.emit()
                    self.senal_cerrar_ventana_chat.emit()
                    self.senal_enviar_ganador_partida.emit(self.jugador, self.ganador_partida)
                    self.reset_juego()
                else:
                    # Seguimos a la siguiente ronda (caso empate) o terminamos la partida segun 
                    # el mazo triunfo...
                    self.senal_preparar_siguiente_ronda.emit()       
            
            elif comando == "terminar_partida_por_desconexion":
                self.ganador_partida = self.jugador
                self.senal_stop_tiempo_ronda.emit()
                self.senal_cerrar_ventana_juego.emit()
                self.senal_enviar_ganador_partida.emit(self.jugador, self.ganador_partida)
                self.reset_juego()

            elif comando == "recibir_mensaje_chat":
                self.senal_actualizar_chat.emit(
                    mensaje_recibido["usuario"],
                    mensaje_recibido["mensaje"])

            elif comando == "solicitud_cartas_oponente_VEO":
                datos = {
                    "comando": "recibir_cartas_oponente_VEO",
                    "cartas": [carta.obtener_ruta() for carta in self.cartas_interface],
                    "usuario": self.jugador}
                self.senal_enviar_cartas_VEO.emit(datos)

            elif comando == "recibir_cartas_oponente_VEO":
                cartas_oponente = mensaje_recibido["cartas oponente"]
                self.senal_mostrar_cartas_tablero_oponente.emit(cartas_oponente)
            
            
            
    def crear_instancia_carta(self, dicc_cartas):
        # Creamos la lista que tendra todas las cartas del jugador
        for index, llave in dicc_cartas.items():
            elemento = llave["elemento"]
            color = llave["color"]
            poder = llave["puntos"]
            carta = Carta(color, elemento, poder)
            self.cartas_jugador.append(carta)
        # Obtenemos las primeras 5 cartas de las cartas del jugador, borrando estas 5
        # al mismo tiempo de las cartas disponibles.
        cartas_interface = deque(carta for index, carta in enumerate(self.cartas_jugador)
                                    if index < cargar_data_json("BARAJA_PANTALLA"))           
        # Dado que sacamos las primeras 5 cartas del total, entonces estas las agregamos
        # al final del la cola.
        for _ in range(5):
            carta_retirada = self.cartas_jugador.popleft() 
            self.cartas_jugador.append(carta_retirada)
        return cartas_interface

    def sacar_nueva_carta(self, carta_sacada):
        # notificamos que el usuario saco una carta para despues actualizar el tablero cuando 
        # corresponda
        self.cartas_interface.remove(carta_sacada) # Sacamos la carta
        nueva_carta = self.cartas_jugador.popleft()
        self.cartas_jugador.append(carta_sacada) # Movemos la carta sacada al final de la lista
        # Agregamos una nueva carta a las cartas de la interface, la cual es la primera que viene
        # en la lista de cartas 
        self.cartas_interface.append(nueva_carta)
        self.senal_actualizar_baraja.emit(self.cartas_interface)
        
    def guardar_jugadores(self, jugador, oponente):
        self.jugador = jugador
        self.oponente = oponente

    def empezar_siguiente_ronda(self):
        self.senal_actualizar_ronda.emit()
        self.senal_actualizar_tablero.emit(self.cartas_interface)

    def partida_ganada(self):
        for jugador, cartas in self.mazo_triunfo_partida.items():
            cartas_azules = cartas['azul']
            cartas_rojas = cartas['rojo']
            cartas_verdes = cartas['verde']
            # 1a condicion: Todas las cartas de distinto color
            if len(cartas_azules) > 0 and len(cartas_rojas) > 0 and len(cartas_verdes) > 0:
                cartas_totales = cartas_azules + cartas_rojas + cartas_verdes
                if self.primera_condicion(cartas_totales):
                    self.ganador_partida = jugador
                elif self.segunda_condicion(cartas_totales):
                    self.ganador_partida = jugador
        return self.ganador_partida
                
    def primera_condicion(self, cartas_totales) -> bool:
        todas_fuego = True if len(list(filter(lambda x: x == 'fuego',
                            cartas_totales))) > 0 else False
        todas_agua = True if len(list(filter(lambda x: x == 'agua',
                            cartas_totales))) > 0 else False
        todas_nieve = True if len(list(filter(lambda x: x == 'nieve',
                            cartas_totales))) > 0 else False
        if todas_fuego or todas_agua or todas_nieve:
            return True
        else:
            return False
    
    def segunda_condicion(self, cartas_totales) -> bool:
        hay_fuego = True if 'fuego' in cartas_totales else False
        hay_agua = True if 'agua' in cartas_totales else False
        hay_nieve = True if 'nieve' in cartas_totales else False
        if hay_fuego and hay_agua and hay_nieve:
            return True
        else:
            return False
        
    def cerrar_todas_las_ventanas(self):
        
        self.senal_cerrar_ventana_espera.emit()
        self.senal_cerrar_ventana_inicio.emit()
        self.senal_cerrar_ventana_juego.emit()
        self.senal_abrir_ventana_error.emit()
        self.senal_cerrar_ventana_chat.emit()

    def reset_juego(self):
        self.cartas_jugador = deque()
        self.cartas_interface = deque()
        self.jugador = ''
        self.oponente = ''
        self.mazo_triunfo_partida = {}
        self.ganador_partida = None
        self.senal_reset_ventana_espera.emit()
        self.senal_reset_ventana_juego.emit()
        self.senal_cerrar_ventana_chat.emit()

    def cheatcode(self, tecla):
        self.contador_veo += 1
        self.secuencia_veo += tecla
        if self.secuencia_veo == 'veo':
            datos = {
                "comando": "VEO",
                "usuario": self.jugador}
            self.senal_veo.emit(datos) 
        if self.contador_veo == 3:
            print(f'Secuencia de botones realizados: {self.secuencia_veo}')
            self.secuencia_veo = ''
            self.contador_veo = 0
            
            

            
          

        
