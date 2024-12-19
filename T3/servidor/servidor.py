from threading import Thread, Lock
import socket
import json 
from pyparsing import Optional
from logica import LogicaServidor
from cripto import encriptar, desencriptar
"""
Modulo en donde el servidor se conecta con cada usuario y presenta todos los
metodos descritos que permiten comunicarse con todos los usuarios presentes en el juego. 
"""

class Servidor:

    def __init__(self, host, port):
        self.host = host
        self.port = port 
        self.socket_servidor : Optional[socket.socket] = None
        self.logica = LogicaServidor(self)
        self.id_cliente = 0
        self.clientes = {}
        self.creando_cliente_lock = Lock()
        self.iniciar_servidor() # Iniciamos el servidor.
        
    def iniciar_servidor(self):
        # Enlazamos el socket del servidor y empezamos a escuchar.
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.log("-", "Iniciando servidor", f"Escuchando en {self.host} : {self.port}")
        self.log("Entidad", "Evento", "Detalles")
        self.comenzar_a_aceptar_conexiones()
        
    def comenzar_a_aceptar_conexiones(self):
        aceptar_cliente = Thread(target=self.aceptar_clientes, daemon=True)
        aceptar_cliente.start()

    def aceptar_clientes(self):
        with self.creando_cliente_lock:
            # Empezamos a estar siempre conectados, escuchando a los clientes.
            while True:
                try:
                    socket_cliente, _ = self.socket_servidor.accept()
                    escuchando_cliente = Thread(
                        target=self.escuchar_cliente,
                        args=(socket_cliente, self.id_cliente, _),
                        daemon=True)
                    escuchando_cliente.start()
                    # Contabilizamos el cliente y guardamos su socket 
                    self.clientes[self.id_cliente] = socket_cliente
                    # Guardamos el id del cliente para que no se repita
                    self.logica.usuarios[self.id_cliente] = ''
                    
                    self.id_cliente += 1
                except ConnectionError:
                    self.log("-", "Error de Conexion", "Cerrando Servidor") 
        
    def escuchar_cliente(self, socket_cliente, id_cliente, address):
        # Escuchamos a cada cliente de forma individual, siempre y cuando el 
        # servidor este conectado. 
        self.log("-", "Cliente Online", "Se ha conectado un nuevo usuario")
        print(address)
        try:
            while True:
                mensaje_cliente = self.recibir_mensaje(socket_cliente)
                if mensaje_cliente is None:
                    raise ConnectionError
                respuesta_servidor = self.logica.procesar_comando(mensaje_cliente)
                if respuesta_servidor:
                    self.enviar_mensaje(respuesta_servidor, socket_cliente)
                    self.actualizar_sala_espera(respuesta_servidor)
                    self.actualizar_seleccion_carta_oponente(respuesta_servidor)
                    self.mostrar_cartas_cada_jugador(respuesta_servidor)
                    self.actualizar_label_usuario_espera(respuesta_servidor)     
                    self.actualizar_chat(respuesta_servidor)
                    self.comando_veo(respuesta_servidor)
                    self.enviar_cartas_oponente_VEO(respuesta_servidor)

        except ConnectionError:
            self.eliminando_cliente(socket_cliente, id_cliente)

        except ConnectionResetError:
            pass
    
    def actualizar_sala_espera(self, respuesta_servidor):
        # Solo se ejecutara para el caso que se quiera actualizar la interfaz 
        # de la ventana de espera para los jugadores presentes en aquella. 
        if "respuesta_sala_espera" not in respuesta_servidor.values():
            return 
        usuarios_sala_espera = list(self.logica.usuarios_sala_espera.values())
        
        for id, socket in self.clientes.items():
            nombre_usuario = self.logica.usuarios[id]

            self.enviar_mensaje({
                "comando": "actualizar_sala_espera",
                "usuarios": usuarios_sala_espera,
                "nombre usuario": nombre_usuario}
                ,socket)

    def actualizar_seleccion_carta_oponente(self, respuesta_servidor):
        if "recibir_informacion_general_1" not in respuesta_servidor.values():
            return 
        usuario_actual = respuesta_servidor["usuario actual"]
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] != usuario_actual:
                self.enviar_mensaje({
                    "comando": "activar_seleccion_carta_oponente"}
                    , socket_cliente)

    def mostrar_cartas_cada_jugador(self, respuesta_servidor):
        if "recibir_informacion_general_2" not in respuesta_servidor.values():
            return
        
        for id, socket_cliente in self.clientes.items():
            usuario = self.logica.usuarios[id]  # Obtengo el nombre de cada jugador conectado
            for usuario_juego, carta in self.logica.rutas_cartas_elegidas.items():
                if usuario != usuario_juego:
                    self.enviar_mensaje({
                        "comando": "mostrar_todas_las_cartas",
                        "carta oponente": carta}
                        , socket_cliente)
        # Cuando termina la ronda, vaciamos las listas con la informacion de la partida para 
        # comenzar otra nueva ronda. 
        self.logica.rutas_cartas_elegidas.clear()
        self.logica.jugadores_y_cartas.clear()
    
    def enviar_ganador_ronda(self):
        for socket_cliente in self.clientes.values():
            self.enviar_mensaje({
                "comando": "recibir_ganador_ronda",
                "ganador ronda": self.logica.ganador_ronda,
                "mazo triunfo": self.logica.mazo_triunfo}
                , socket_cliente)    

    def actualizar_label_usuario_espera(self, respuesta_servidor):
        if "actualizar_label_usuario_saliendo" not in respuesta_servidor.values():
            return
        usuario = respuesta_servidor["usuario"]
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] == usuario:
                # Retiramos al usuario del diccionario de la sala de espera
                del self.logica.usuarios_sala_espera[id] 
            self.enviar_mensaje({
                "comando": "actualizar_label_usuario_saliendo",
                "usuario": usuario}
                , socket_cliente)
        
    def terminar_partida_por_desconexion(self, usuario_desconectado):
        usuario_aun_conectado = list(filter(lambda x: x != usuario_desconectado,
                                            self.logica.usuarios_sala_juego))[0]
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] == usuario_aun_conectado:
                self.enviar_mensaje({
                    "comando": "terminar_partida_por_desconexion"}
                    , socket_cliente)

    def resetar_interfaces(self, respuesta_servidor):
        if "partida_ganada" not in respuesta_servidor.values():
            return
        # Es el comando que envia el servidor cuando se gana una partida, para
        # evitar bugs. 
        pass

    def actualizar_chat(self, respuesta_servidor):
        if "actualizar_chat_usuarios" not in respuesta_servidor.values():
            return
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] != respuesta_servidor["usuario"]:
                self.enviar_mensaje({
                    "comando": "recibir_mensaje_chat",
                    "usuario": respuesta_servidor["usuario"],
                    "mensaje": respuesta_servidor["mensaje"]}
                    , socket_cliente)

    def comando_veo(self, respuesta_servidor):
        if "solicitar_cartas_oponente_VEO" not in respuesta_servidor.values():
            return
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] != respuesta_servidor["usuario"]:
                self.enviar_mensaje({
                    "comando": "solicitud_cartas_oponente_VEO"}
                    , socket_cliente)

    def enviar_cartas_oponente_VEO(self, respuesta_servidor):
        if "enviar_cartas_jugador_VEO" not in respuesta_servidor.values():
            return
        for id, socket_cliente in self.clientes.items():
            if self.logica.usuarios[id] != respuesta_servidor["usuario"]:
                self.enviar_mensaje({
                    "comando": "recibir_cartas_oponente_VEO",
                    "cartas oponente": respuesta_servidor["cartas"] }
                    , socket_cliente)

    def recibir_mensaje(self, socket_cliente):
        # Recibimos el mensaje del cliente, decodificandolo (y a la vez, 
        # desencriptandolo)
        mensaje_bytes = bytearray()
        largo_bytes_mensaje = socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_bytes_mensaje, byteorder='big')
        
        while len(mensaje_bytes) < largo_mensaje:
            eliminar_numero = socket_cliente.recv(4) 
            chunk_sucio = socket_cliente.recv(min(32, largo_mensaje - len(mensaje_bytes)))
            while chunk_sucio.endswith(b'\x00'): # Le sacamos los bytes 0 si cumple la condicion
                chunk_sucio = chunk_sucio[:-1]
            mensaje_bytes += chunk_sucio

        return self.decodificar_mensaje(mensaje_bytes)

    def enviar_mensaje(self, mensaje, socket_cliente):
        # Envia un mensaje hacia el cliente, codificandolo en base 
        # al protocolo prestablecido. 
        mensaje_codificado = self.codificar_mensaje(mensaje)
        mensaje_bytes = bytearray()
        largo_mensaje = len(mensaje_codificado).to_bytes(4, byteorder='big')
        mensaje_bytes += largo_mensaje
        indice = 1
        for i in range(0, len(mensaje_codificado), 32):
            indice_chunk = indice.to_bytes(4, byteorder='little')
            chunk = bytearray(mensaje_codificado[i:i + 32])
            while len(chunk) < 32:
                chunk += b'\x00' 
            mensaje_bytes += (indice_chunk + bytes(chunk))
            indice += 1
        socket_cliente.sendall(bytes(mensaje_bytes))

    def codificar_mensaje(self, mensaje):
        # Serializamos y codificamos el mensaje en una serie de bytes usando JSON.
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode('utf-8')
            #mensaje_encriptado = encriptar(mensaje_bytes)
            return mensaje_bytes #mensaje_encriptado
        except json.JSONDecodeError:
            return b''
    
    def decodificar_mensaje(self, mensaje):
        try:
            # Desencriptamos el mensaje y lo decodificamos usando JSON.
            #mensaje_desencriptado = desencriptar(bytearray(mensaje))
            mensaje_decodificado = json.loads(mensaje) #json.loads(mensaje_desencriptado) 
            return mensaje_decodificado
        except json.JSONDecodeError:
            return {}

    def eliminando_cliente(self, socket_cliente, id_cliente):
        self.log("-", "Usuario Offline", "Se ha desconectado un usuario")
        usuario_desconectado = self.logica.usuarios[id_cliente]
        if usuario_desconectado in self.logica.usuarios_sala_juego:
            self.terminar_partida_por_desconexion(usuario_desconectado)

        del self.clientes[id_cliente]
        self.logica.eliminar_usuario(id_cliente)
        socket_cliente.close() 

    def log(self, cliente, evento, detalles):
        print("|{:^30}|{:^30}|{:^60}|".format(cliente, evento, detalles))
        print("|{:^30}|{:^30}|{:^60}|".format("-" * 30, "-" * 30, "-" * 60))
        