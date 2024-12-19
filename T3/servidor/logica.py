from threading import Lock
from cartas import get_penguins
from collections import deque, namedtuple
"""
Modulo principal de la logica del servidor el cual verifica todos los comandos recibidos
por parte de los clientes conectados. Asimismo, procesa aquellos comandos, generando cambios
en sus interfaces y luego les envia una respuesta a los clientes respectivos en el modulo
servidor.py.  
"""

class LogicaServidor:
    def __init__(self, servidor) -> None:
        self.servidor = servidor
        self.usuarios = {}
        self.usuarios_sala_espera = {}
        self.usuarios_sala_juego = []
        self.cartas_usuario = {}

        self.lock_sala_espera = Lock()
        self.lock_validar_usuario = Lock()
        self.lock_obtener_cartas = Lock()
        self.lock_timer_ronda = Lock()
        self.lock_verificar_ganador = Lock()
        self.lock_notificacion_cartas = Lock()
        self.lock_acceder_comandos = Lock()
        self.lock_vaciar_sala_espera = Lock()
        self.lock_recibir_mensaje = Lock()
        
        self.juego_iniciado = False
        self.rutas_cartas_elegidas = {}
        self.jugadores_y_cartas = deque()
        self.mazo_triunfo = {}
        self.crear_jugador = namedtuple('Jugador',['nombre', 'elemento', 'color', 'poder'])
        self.ganador_ronda = ''
        self.ganador_partida = ''
        self.contador_mensaje = 0
        self.contador_mensaje_2 = 0
        
    def procesar_comando(self, mensaje):
        with self.lock_acceder_comandos:
            try:
                comando = mensaje["comando"] 
            except KeyError:
                return {}
            
            if comando == "validar_login":
                respuesta_servidor = self.validar_login(mensaje["nombre usuario"])
                
            elif comando == "verificar_personas_en_espera":
                respuesta_servidor = self.usuarios_en_espera()

            elif comando == "usuario_saliendo_sala_espera":
                usuario = mensaje["usuario"]
                respuesta_servidor = {
                    "comando": "actualizar_label_usuario_saliendo",
                    "usuario": usuario}

            elif comando == "get_penguins":
                usuario = mensaje["usuario"]
                self.mazo_triunfo[usuario] = {
                    "azul": [],
                    "rojo": [],
                    "verde": []}
                respuesta_servidor = self.recibir_cartas(usuario)

            elif comando == "notificar_carta_elegida":
                respuesta_servidor = self.notificar_carta_elegida(mensaje)
                
            elif comando == "solicitar_ganador_ronda":
                with self.lock_verificar_ganador:
                    respuesta_servidor = self.notificar_ganador_ronda()

            elif comando == "recibir_ganador_partida":
                self.ganador_partida = mensaje["ganador partida"]
                self.servidor.log("SERVIDOR", "FIN DE LA PARTIDA",
                                        f"Ganador: {self.ganador_partida}")
                self.usuarios_sala_juego.clear()
                self.usuarios_sala_espera.clear()
                respuesta_servidor = {
                    "comando": "partida_ganada"}
            
            elif comando == "recibir_mensaje_chat":
                with self.lock_recibir_mensaje:
                    respuesta_servidor = {
                        "comando": "actualizar_chat_usuarios",
                        "mensaje": mensaje["mensaje"],
                        "usuario": mensaje["usuario"]}

            elif comando == "VEO":
                respuesta_servidor = {
                    "comando": "solicitar_cartas_oponente_VEO",
                    "usuario": mensaje["usuario"]}

            elif comando == "recibir_cartas_oponente_VEO":
                respuesta_servidor = {
                    "comando": "enviar_cartas_jugador_VEO",
                    "usuario": mensaje["usuario"],
                    "cartas": mensaje["cartas"]}
        
        return respuesta_servidor

    def notificar_carta_elegida(self, mensaje):
        with self.lock_notificacion_cartas:
            usuario_actual = mensaje["usuario"]    
            carta_elegida = mensaje["ruta carta"]
            elemento = mensaje["elemento"]
            color = mensaje["color"]
            poder = int(mensaje["poder"])
            jugador = self.crear_jugador(usuario_actual, elemento, color, poder)
            self.servidor.log(usuario_actual, "Carta lanzada", f"Carta tipo: {elemento} ")
            # Agregamos al jugador en una lista para luego comparar su carta con el oponente
            # al momento de terminar la ronda
            self.jugadores_y_cartas.append(jugador)
            # Ademas, agregamos de manera aparte la ruta de la carta con el usuario respectivo en 
            # un diccionario
            self.rutas_cartas_elegidas[usuario_actual] = carta_elegida
            # En el caso que el oponente haya elegido, ilustramos su carta sin mostrarla en el
            # usuario que aun no ha elegida alguna carta
            if len(self.rutas_cartas_elegidas) == 1:
                return {
                    "comando": "recibir_informacion_general_1",
                    "usuario actual": usuario_actual
                    }
            # En el caso que ya ambos usuarios hayan confirmado una carta, mostramos sus cartas 
            # respectivas a todos los clientes conectados en la ventana del juego. 
            else:
                self.ganador_ronda = self.verificar_ganador() 
                self.actualizar_mazo_triunfo(self.ganador_ronda)
                
                return {
                    "comando": "recibir_informacion_general_2"
                    }
    
    def recibir_cartas(self, usuario):
        with self.lock_obtener_cartas:
            dicc_cartas = get_penguins()
            self.cartas_usuario[usuario] = dicc_cartas
            
            self.contador_mensaje_2 += 1
            self.usuarios_sala_juego.append(usuario)
            if self.contador_mensaje_2 == 2:
                jugadores_actuales = " y ".join(list(self.usuarios_sala_espera.values()))
                self.servidor.log("SERVIDOR", "NUEVA RONDA",
                                            f'Usuarios: {jugadores_actuales}')
                self.contador_mensaje_2 = 0
                self.usuarios_sala_espera.clear()
            return {
                "comando": "get_penguins",
                "cartas": dicc_cartas}
    
    def notificar_ganador_ronda(self):
        self.contador_mensaje += 1
        if self.contador_mensaje == 2:
            if self.ganador_ronda.nombre == 'empate':
                self.servidor.log("SERVIDOR", "FIN DE LA RONDA",
                                        f"--- {self.ganador_ronda.nombre} ---")
            else:
                self.servidor.log("SERVIDOR", "FIN DE LA RONDA",
                                        f"Ganador: {self.ganador_ronda.nombre}")
            self.contador_mensaje = 0
        return {
            "comando": "recibir_ganador_ronda",
            "ganador ronda": self.ganador_ronda,
            "mazo triunfo": self.mazo_triunfo}

    def verificar_ganador(self):
        jugador_1 = self.jugadores_y_cartas[0]
        jugador_2 = self.jugadores_y_cartas[1]        
        return self.obtener_ganador(jugador_1, jugador_2) 
   
    def obtener_ganador(self, jugador_1, jugador_2): 
        if jugador_1.elemento != jugador_2.elemento:
            if jugador_1.elemento == 'fuego':
                # jugador 2 -> agua o nieve -> en el caso que sea agua, gana 2
                ganador = jugador_1 if jugador_2.elemento == 'nieve' else jugador_2 
            elif jugador_1.elemento == 'agua':
                # jugador 2 -> fuego o nieve -> en el caso que sea nieve, gana 2
                ganador = jugador_1 if jugador_2.elemento == 'fuego' else jugador_2 
            elif jugador_1.elemento == 'nieve':
                # jugador 2 -> fuego o agua -> en el caso que sea agua, gana 2
                ganador = jugador_1 if jugador_2.elemento == 'agua' else jugador_2 
        else:
            # Evaluamos los puntajes, en el caso que ampos puntajes sean iguales, empatan
            if jugador_1.poder == jugador_2.poder:
                ganador = self.crear_jugador('empate',"-","-","-")
            else:
                ganador = jugador_1 if max(jugador_1.poder,
                                        jugador_2.poder) == jugador_1.poder else jugador_2 
        return ganador
       
    def actualizar_mazo_triunfo(self, ganador_ronda):
        if ganador_ronda.nombre != 'empate':
            # Obtengo el diccionario con la cantidad de fichas ganadas
            fichas = self.mazo_triunfo[ganador_ronda.nombre] 
            fichas[ganador_ronda.color] += [ganador_ronda.elemento]
            # Actualizamos el diccionario respectivo 
            self.mazo_triunfo[ganador_ronda.nombre] = fichas 

    def usuarios_en_espera(self):
        with self.lock_sala_espera:
            id_cliente = list(self.servidor.clientes.keys())[-1] 
            nombre_usuario = self.usuarios[id_cliente]
            # Para el caso que el usuario quiera entrar a la sala de espera pero 
            # esta se encuentra llena, se rechazara su entrada.
            if len(self.usuarios_sala_espera.values()) == 2:
                self.servidor.log(nombre_usuario, "No ingresa Sala de Espera",
                                                        "Sala de espera llena")
                return {
                    "comando": "respuesta_sala_espera_llena"
                    }
            # Para el caso que la sala de espera este vacia pero existe una partida
            # ya iniciada, rechazamos la entrada a la sala de espera.
            elif len(self.usuarios_sala_juego) == 2:
                self.servidor.log(nombre_usuario, "No ingresa Sala de Espera",
                                                            "Partida existente")
                return {
                    "comando": "respuesta_partida_existente"
                }
            # En cualquier caso (i.e. No se ha iniciado una partida o la sala de 
            # espera se encuentra vacia) el usuario podra entrar a la sala de espera.
            else:
                self.usuarios_sala_espera[id_cliente] = nombre_usuario
                self.servidor.log(nombre_usuario, "Ingresa Sala de Espera", "-")
                # En el caso que se llene la sala de espera, activamos el timer 
                # para comenzar el juego
                if len(self.usuarios_sala_espera) == 2: 
                    self.activar_timer_sala_espera()
                    
                return {
                    "comando": "respuesta_sala_espera",
                    "verificacion": "aceptada"
                    }
   
    def activar_timer_sala_espera(self):
        with self.lock_timer_ronda:
            for id_cliente in self.usuarios_sala_espera.keys():
                socket_cliente = self.servidor.clientes[id_cliente]
                self.servidor.enviar_mensaje({
                    "comando": "activar_timer_sala_espera"}
                    , socket_cliente)
            
    def validar_login(self, nombre):
        # Verificamos si el nombre del usuario cumple las condiciones
        with self.lock_validar_usuario:
            valido, error = self.validar_usuario(nombre)
            if valido:
                self.usuarios[self.servidor.id_cliente - 1] = nombre
                self.servidor.log(nombre, "Ha ingresado a la partida",
                                        "*Nombre de usuario validado*")
                return {
                    "comando": "respuesta_login_verificado",
                    "verificacion": "aceptada",
                    "nombre": nombre}
            else:
                self.servidor.log(nombre, "No ha podido ingresar", f'*{error}*')
                return {
                    "comando": "respuesta_login_verificado",
                    "verificacion": "rechazada",
                    "error": error}

    def validar_usuario(self, usuario):
     # Validando si es alfanumerico...
        valido = True
        error = ""
        if usuario.isalpha() or usuario.isdigit():
            error = "Tu nombre de usuario debe ser alfanumerico"
            valido = False
        # Validando el nombre de usuario...
        if len(usuario) < 1 or len(usuario) > 10:
            error = "Tu nombre de usuario debe tener entre 1 y 10 carácteres"
            valido = False
        # Validando si el nombre ya existe (Case - sensitive)...
        usuarios = [usuario.lower() for usuario in self.usuarios.values()]
        if usuario.lower() in usuarios: 
            error = "Este nombre de usuario ya existe"
            valido = False
        # Retorna solo valido si cumple todas las condiciones, o en 
        # el caso que no cumpla, retornará el error
        return valido, error   
            
    def eliminar_usuario(self, id_cliente):
        if self.usuarios[id_cliente] in self.usuarios_sala_espera.values():
            del self.usuarios_sala_espera[id_cliente]
        del self.usuarios[id_cliente]


 
        
        


    
