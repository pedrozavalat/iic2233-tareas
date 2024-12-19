from backend.logica_interfaz import Interfaz
from cripto import desencriptar, encriptar
from threading import Thread
import socket 
import json
import sys
"""
Modulo que presenta la conexion directa con el servidor. 
Permite la codificacion y decodificacion del envio o recibimiento de mensajes, 
respectivamente
"""
class Cliente:

    def __init__(self, host, port) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.interfaz = Interfaz(self)
        self.coneccion_activa = False
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.iniciar_cliente()

    def iniciar_cliente(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.coneccion_activa = True
            self.interfaz.mostrar_ventana_inicio()
            self.comenzar_a_escuchar_servidor()
        except ConnectionError:
            print("Servidor no disponible")
    
    def comenzar_a_escuchar_servidor(self):
        escuchar_servidor = Thread(target=self.escuchar_servidor, daemon=True)
        escuchar_servidor.start()
        
    def escuchar_servidor(self):
        try:
            while self.coneccion_activa:
                mensaje_recibido = self.recibir_mensaje()
                if mensaje_recibido is not None:
                    self.interfaz.manejar_mensaje(mensaje_recibido)
        except ConnectionError:
            self.manejar_error_conexion()
            
    def recibir_mensaje(self):
        # Recibimos el mensaje del cliente, decodificandolo (y a la vez, 
        # desencriptandolo)
        mensaje_bytes = bytearray()
        largo_bytes_mensaje = self.socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_bytes_mensaje, byteorder='big')

        while len(mensaje_bytes) < largo_mensaje:
            eliminar_numero = self.socket_cliente.recv(4)
            chunk_sucio = self.socket_cliente.recv(min(32, largo_mensaje - len(mensaje_bytes)))
            while chunk_sucio.endswith(b'\x00'): # Le sacamos los bytes 0 si cumple la condicion
                chunk_sucio = chunk_sucio[:-1]
            mensaje_bytes += chunk_sucio
        return self.decodificar_mensaje(bytes(mensaje_bytes))

    def enviar_mensaje(self, mensaje):
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
        self.socket_cliente.sendall(bytes(mensaje_bytes))

    def codificar_mensaje(self, mensaje):
        # Serializamos y codificamos el mensaje en una serie de bytes usando JSON.
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode('utf-8')
            #mensaje_encriptado = encriptar(mensaje_bytes)
            return mensaje_bytes #mensaje_encriptado
        except json.JSONDecodeError:
            print("no se pudo codificar el mensaje")
            return b''
        
    def decodificar_mensaje(self, mensaje):
        try:
            # Desencriptamos el mensaje y lo decodificamos usando JSON.
            #mensaje_desencriptado = desencriptar(bytearray(mensaje))
            mensaje_decodificado = json.loads(mensaje) #json.loads(mensaje_desencriptado) 
            return mensaje_decodificado
        except json.JSONDecodeError:
            return {}

    def manejar_error_conexion(self):
        self.interfaz.cerrar_todas_las_ventanas()
    
    def salir(self):
        sys.exit()
