from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect
from backend.elementos_del_juego import ProyectilAzul, ProyectilVerde, Soles
from backend.zombies import ZombieClasico, ZombieRapido
from backend.plantas import Patatas, PlantasAzules, PlantasVerdes, Girasol
from aparicion_zombies import intervalo_aparicion
from backend.notificaciones import Notificaciones
from backend.funciones_utiles import otorgar_ptje, otorgar_ptje_extra
from PyQt5.QtWidgets import QPushButton
from random import randint, choice
import parametros as p 
from math import ceil

class LogicaJuego(QObject):

    senal_actualizar_datos = pyqtSignal(dict) # Actualiza los datos en el frontend.
    senal_guardar_datos = pyqtSignal(str, int) # Guarda los datos del jugador.
    senal_cargar_casilla = pyqtSignal(QPushButton, str) # Actualiza la casilla elegida en frontend.
    senal_actualizar_casillas = pyqtSignal(int) # Actualiza la planta comida por el zombie. 
    senal_mover_planta = pyqtSignal(str, str) # Actualiza los movimientos de las plantas
    senal_borrar_plantas = pyqtSignal() # Actualiza todas las casillas del jardin. 
    senal_lanzar_proyectil = pyqtSignal(QObject) # Realiza la aparicion de los proyectiles creados.
    senal_mover_proyectil = pyqtSignal(QObject, tuple) # Actualiza la posicion de los proyectiles.
    senal_actualizar_proyectil = pyqtSignal(set, tuple) # Elimina label del proyectil en frontend.
    senal_ocultar_proyectiles = pyqtSignal(set) # Elimina todos los proyectiles del mapa
    senal_mostrar_zombie = pyqtSignal(QObject) # Muestra el label del zombie en la ventana. 
    senal_ocultar_zombie = pyqtSignal(QObject) # Oculta el label del zombie en la ventana. 
    senal_crear_soles = pyqtSignal(QObject) # Muestra los soles en la ventana.
    senal_ocultar_soles = pyqtSignal(set) # Oculta todos los soles de la ventana. 
    senal_ocultar_sol_especifico = pyqtSignal(set, tuple) # Oculta solo "un sol" en la ventana 
    senal_avanzar_ronda = pyqtSignal() # Permite avanzar a la siguiente ronda
    senal_terminar_ronda = pyqtSignal(dict, str, str, str) # Termina la ronda actual. 
    senal_cerrar_ventana = pyqtSignal() 

    def __init__(self):
        super().__init__()# ---- Datos del jugador y de la partida actual
        self.nombre = None 
        self.puntaje = 0 
        self._cantidad_soles = p.SOLES_INICIALES
        self.ronda = 0 
        self.escenario_actual = None
        self.dificultad = None 
        self.soles_plantas = {
            "girasol" : 50,
            "planta verde" : 100,
            "planta azul" : 150,
            "patata" : 75} 
        self.zombies_creados = set() 
        self.zombies_actuales = set()
        self.zombies_destruidos = 0
        self.zombies_restantes = p.N_ZOMBIES * 2
        self.soles_jardin = set()
        self.proyectiles = set()
        self.planta_elegida = ""
        self.posiciones_plantas = {} # -- Posiciones actuales de las plantas
        self.posiciones_casillas = None # -- Casillas donde se posicionaran las plantas
        self.carril_1 = [] # -- Carril 1 y 2: Carriles donde se posicionaran los zombies
        self.carril_2 = []
        self.notificacion = Notificaciones()

    def instanciar_timers(self): 
        self.timer_movimiento_plantas = QTimer() # -- Timer de movimientos de las plantas.
        self.timer_movimiento_plantas.setInterval(p.INTERVALO_MOVIMIENTO_PLANTAS)
        self.timer_movimiento_plantas.timeout.connect(self.movimiento_planta)
        self.timer_lanzar_proyectil = QTimer() # -- Timer proyectiles plantas lanzaguisantes.
        self.timer_lanzar_proyectil.setInterval(p.INTERVALO_DISPARO)
        self.timer_lanzar_proyectil.timeout.connect(self.movimiento_proyectiles)
        self.timer_verificar_pos_proyectil = QTimer()  # -- Timer verifica posicion del proyectil 
        self.timer_verificar_pos_proyectil.setInterval(1) # al colisionar.
        self.timer_verificar_pos_proyectil.timeout.connect(self.verificar_proyectiles)
        self.timer_generar_soles = QTimer() # -- Timer que genera soles alrededor de girasol.
        self.timer_generar_soles.setInterval(p.INTERVALO_SOLES_GIRASOL)
        self.timer_generar_soles.timeout.connect(self.generar_soles_girasol)
        self.timer_generar_lluvia_soles = QTimer( )# -- Timer que genera soles dentro del jardin.
        self.timer_generar_lluvia_soles.setInterval(p.INTERVALO_APARICION_SOLES)
        self.timer_generar_lluvia_soles.timeout.connect(self.generar_soles_lluvia)
        self.timer_aparicion_zombies = QTimer() # -- Timer que posiciona a los zombies.
        self.aparicion_zombies = intervalo_aparicion(self.ronda, self.dificultad) * 10000 
        self.timer_aparicion_zombies.setInterval(ceil(self.aparicion_zombies))  
        self.timer_aparicion_zombies.timeout.connect(self.posicionar_zombies)
        self.timer_ataque_zombie = QTimer() # -- Timer que verifica las posiciones de un zombie.
        self.timer_ataque_zombie.setInterval(500)
        self.timer_ataque_zombie.timeout.connect(self.verificar_zombies)
        self.timer_actualizar_datos = QTimer() # -- Timer que actualiza los datos de la ventana.
        self.timer_actualizar_datos.setInterval(1)
        self.timer_actualizar_datos.timeout.connect(self.cargar_datos_partida)
        
    @property
    def cantidad_soles(self):
        return self._cantidad_soles
    @cantidad_soles.setter
    def cantidad_soles(self, valor):
        if valor < 0:
            self._cantidad_soles = 0
        else:
            self._cantidad_soles = valor

    def actualizar_datos(self):
        return {"soles" : str(self.cantidad_soles), "puntaje" : str(self.puntaje),
                "nivel" : str(self.ronda), "zombies destruidos" : str(self.zombies_destruidos),
                "zombies restantes" : str(p.N_ZOMBIES * 2 - self.zombies_destruidos)}

    def cargar_datos(self, nombre, escenario_elegido, ronda): # -> Método que actualiza los datos 
        self.nombre = nombre #                                     del usuario. 
        self.ronda = ronda
        self.escenario_actual = escenario_elegido
        self.dificultad = p.PONDERADOR_DIURNO if escenario_elegido == "Jardín de la abuela" \
                                                else p.PONDERADOR_NOCTURNO # "Salida Nocturna"
        datos = self.actualizar_datos()
        self.senal_actualizar_datos.emit(datos)

    def cargar_datos_partida(self): # -> Metodo que carga constantemente todos los datos de 
        self.cargar_datos(self.nombre, self.escenario_actual, self.ronda) # la partida a la ventana 
    
    def recibir_opcion_plantar(self, boton): # -> Metodo que notifica si es que el usuario 
        self.planta_elegida = boton #             puede plantar o no. 
        if self.cantidad_soles >= self.soles_plantas[self.planta_elegida]:
            self.notificacion.enviar_notificacion("elegir casilla", p.INTERVALO_ANUNCIO_VERDE)
        else:
            self.notificacion.enviar_notificacion("plantar", p.INTERVALO_ANUCIO_ROJO)
            self.planta_elegida = ""

    def cargar_casilla_elegida(self, casilla_elegida): # -> Metodo que actualiza en el frontend
        if self.planta_elegida == "": # la planta elegida por el usario en al tienda.                     
            self.notificacion.enviar_notificacion("escoger planta", p.INTERVALO_ANUCIO_ROJO)
        else:
            indice = casilla_elegida.accessibleName()
            if indice not in self.posiciones_plantas.keys():
                if self.planta_elegida == "girasol":
                    self.posiciones_plantas[indice] = Girasol(indice, self.planta_elegida)
                    self.senal_cargar_casilla.emit(casilla_elegida, p.RUTA_ICON_GIRASOL)            
                elif self.planta_elegida == "planta verde":
                    self.posiciones_plantas[indice] = PlantasVerdes(indice, self.planta_elegida)
                    self.senal_cargar_casilla.emit(casilla_elegida, p.RUTA_ICON_LANZAGUI_NORMAL)            
                elif self.planta_elegida == "planta azul":
                    self.posiciones_plantas[indice] = PlantasAzules(indice, self.planta_elegida)
                    self.senal_cargar_casilla.emit(casilla_elegida, p.RUTA_ICON_LANZAGUI_HIELO)            
                elif self.planta_elegida == "patata":
                    self.posiciones_plantas[indice] = Patatas(indice, self.planta_elegida)
                    self.senal_cargar_casilla.emit(casilla_elegida, p.RUTA_ICON_PATATA)        
                self.cantidad_soles -= self.soles_plantas[self.planta_elegida]
                self.planta_elegida = ""
                self.cargar_datos(self.nombre, self.escenario_actual, self.ronda)
            else:
                self.notificacion.enviar_notificacion("casilla ocupada", p.INTERVALO_ANUNCIO_VERDE)
        
    def movimiento_planta(self): # -> Metodo que genera el movimiento de las plantas.
        for posicion, planta in self.posiciones_plantas.items():
            if planta.lanza_proyectil: 
                if planta.primer_movimiento:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_1)
                    planta.primer_movimiento = False
                elif planta.segundo_movimiento:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_2)
                    planta.segundo_movimiento = False
                else:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_3)
                    planta.primer_movimiento = True
            elif not planta.lanza_proyectil and planta.tipo != "patata": 
                if planta.primer_movimiento:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_1)
                    planta.primer_movimiento = False
                else:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_2)
                    planta.primer_movimiento = True
            elif planta.tipo == "patata":
                if 50 <= planta.vida <= 120: 
                    self.senal_mover_planta.emit(posicion, planta.movimiento_2)
                elif planta.vida < 50:
                    self.senal_mover_planta.emit(posicion, planta.movimiento_3)

    def movimiento_proyectiles(self): # -> Metodo que genera el movimiento de los proyectiles.
        for posicion, planta in self.posiciones_plantas.items():
            if planta.lanza_proyectil:
                pos_x = self.posiciones_casillas[int(posicion)].x()
                pos_y = self.posiciones_casillas[int(posicion)].y()
                posicion_proyectil = QRect(pos_x, pos_y, 30, 40)
                if planta.tipo == "planta verde":
                    proyectil = ProyectilVerde(posicion_proyectil)
                    self.senal_lanzar_proyectil.emit(proyectil)
                elif planta.tipo == "planta azul":
                    proyectil = ProyectilAzul(posicion_proyectil)
                    self.senal_lanzar_proyectil.emit(proyectil)
                proyectil.timer_mover_proyectil.start()
                self.proyectiles.add(proyectil)
                planta.proyectiles.add(proyectil)

    def verificar_proyectiles(self): # -> Metodo que verifica la colision de los proyectiles sobre
        set_proyectiles = {proyectil for proyectil in self.proyectiles} #  los zombies en el juego.
        set_zombies_creados = {zombie for zombie in self.zombies_creados}
        for proyectil in set_proyectiles:
            pos_x = proyectil.posicion.x()
            pos_y = proyectil.posicion.y()
            if proyectil.posicion.x() >= 1270:
                self.senal_actualizar_proyectil.emit(self.proyectiles, (pos_x, pos_y))
                self.proyectiles.discard(proyectil) 
            else:
                for zombie in set_zombies_creados:
                    pos_x_zombie, pos_y_zombie = zombie.posicion.x(), zombie.posicion.y()
                    condicion_1 = pos_x in list(range(pos_x_zombie - 20, pos_x_zombie + 20))
                    condicion_2 = pos_y in list(range(pos_y_zombie - 20, pos_y_zombie + 20))
                    if condicion_1 and condicion_2:
                        zombie.vida -= p.DANO_PROYECTIL
                        proyectil.timer_mover_proyectil.stop()
                        if proyectil.tipo == "azul":
                            zombie.ralentizacion()
                        self.senal_actualizar_proyectil.emit(self.proyectiles, (pos_x, pos_y))
                        self.proyectiles.discard(proyectil) 
                        if zombie.vida <= 0:
                            zombie.detener()
                            self.senal_ocultar_zombie.emit(zombie)
                            self.zombies_destruidos += 1
                            self.zombies_creados.discard(zombie)
                            self.puntaje += otorgar_ptje(self.escenario_actual)

    def crear_zombies(self): # -> Metodo que crea los zombies aleatoriamente en cada carril. 
        for _ in range(p.N_ZOMBIES):
            posicion_zombie = QRect(1300, 160, 60, 70)
            zombie = choice([ZombieClasico(posicion_zombie), ZombieRapido(posicion_zombie)])
            self.carril_1.append(zombie)
        for _ in range(p.N_ZOMBIES):
            posicion_zombie = QRect(1300, 250, 60, 70)
            zombie = choice([ZombieClasico(posicion_zombie), ZombieRapido(posicion_zombie)])
            self.carril_2.append(zombie)
        zombies_creados = self.carril_1 + self.carril_2
        self.zombies_creados = set(zombies_creados)

    def posicionar_zombies(self): # -> Metodo que posiciona a los zombies en un intervalo de
        carril_elegido  = choice([1,2]) #            de tiempo determinado durante la ronda. 
        carril_elegido = 1 if len(self.carril_2) == 0 else choice([1,2])
        carril_elegido = 2 if len(self.carril_1) == 0 else choice([1,2])
        if carril_elegido == 1 and len(self.carril_1) > 0:
            zombie = choice(self.carril_1)
            zombie.mover()
            self.carril_1.remove(zombie)
            self.senal_mostrar_zombie.emit(zombie)
            self.zombies_actuales.add(zombie) # Agregamos al zombie mostrado en juego
        elif carril_elegido == 2 and len(self.carril_2) > 0:
            zombie = choice(self.carril_2) 
            zombie.mover()
            self.carril_2.remove(zombie)
            self.senal_mostrar_zombie.emit(zombie)
            self.zombies_actuales.add(zombie) # Agregamos al zombie mostrado en juego
        if self.zombies_restantes == 0:
            self.timer_aparicion_zombies.stop()
        else:
            self.zombies_restantes -= 1

    def verificar_zombies(self): # -> Metodo que verifica la posicion de los zombies en cada 
        set_zombies_creados = {zombie for zombie in self.zombies_creados} #  en cada momento.
        set_plantas_restantes = {planta for planta in self.posiciones_plantas.values()}
        if self.zombies_destruidos == p.N_ZOMBIES * 2: # --> En el caso que el jugador gana 
            self.puntaje += otorgar_ptje_extra(self.puntaje, self.dificultad) #  la partida. 
            self.notificacion.enviar_notificacion("crazy cruz", p.INTERVALO_ANUNCIO_CRAZY_CRUZ)
        for zombie in set_zombies_creados:
            if zombie.posicion.x() <= 280: # --> En el caso que un zombie llegue a la casa. Es
                self.pausar_juego() # decir, el jugador pierde. 
                self.notificacion.enviar_notificacion("pierde", p.INTERVALO_ANUNCIO_PERDEDOR)
            else:
                for planta in set_plantas_restantes: 
                    pos_x = self.posiciones_casillas[int(planta.posicion)].x()
                    pos_y = self.posiciones_casillas[int(planta.posicion)].y()
                    condicion_1 = zombie.posicion.x() in list(range(pos_x - 20, pos_x + 20))
                    condicion_2 = zombie.posicion.y() in list(range(pos_y - 20, pos_y + 20))
                    if condicion_1 and condicion_2: # --> Si una planta esta en la posicion
                        planta.vida -= zombie.dano  #     del zombie, entonces el zombie 
                        if planta.vida > 0: #             empieza a comérsela.
                            zombie.detener()
                            zombie.comiendo()
                        elif planta.vida <= 0: # --> Si la planta muere, se elimina de la ventana. 
                            self.senal_actualizar_casillas.emit(int(planta.posicion))   
                            if planta.lanza_proyectil: # --> Si la planta es un lanzaguisante, sus
                                proyectiles_planta = {proyectil for proyectil in #     proyectiles
                                                                planta.proyectiles} #   dejaran de
                                planta.lanza_proyectil = False  #                         moverse. 
                                for proyectil in proyectiles_planta:
                                    proyectil.timer_mover_proyectil.stop()
                                    self.senal_actualizar_proyectil.emit(
                                                        proyectiles_planta, (pos_x, pos_y))
                                    planta.proyectiles.discard(proyectil)
                            zombie.mover()
        
    def generar_soles_girasol(self): # -> Metodo que genera los soles alrededor de los
        for planta in self.posiciones_plantas.values(): #                   girasoles.
            if planta.tipo == "girasol": # Posicion de la planta. 
                posicion_planta = self.posiciones_casillas[int(planta.posicion)].pos()
                pos_x, pos_y = posicion_planta.x(), posicion_planta.y()
                posicion_sol = QRect(pos_x, pos_y, 31, 31)
                for _ in range(p.CANTIDAD_SOLES):
                    sol = Soles(posicion_sol)
                    sol.posicionar_alrededor_girasol()
                    self.senal_crear_soles.emit(sol)
                    planta.soles.add(sol)
                    self.soles_jardin.add(sol)

    def generar_soles_lluvia(self): # -> Metodo que genera los soles en el jardin durante
        if self.escenario_actual == "Jardín de la abuela": #       el escenario 'diurno'.
            pos_x, pos_y = randint(360, 940), randint(60, 410) # -> Posicionamos aleatoriamente
            posicion_sol = QRect(pos_x, pos_y, 31, 31)            
            sol = Soles(posicion_sol)
            sol.label_sol.move(pos_x, pos_y)
            sol.posicion.moveTo(pos_x, pos_y)
            self.senal_crear_soles.emit(sol)
            self.soles_jardin.add(sol)

    def comenzar_juego(self, posiciones_casillas): # -> Metodo que permite el comienzo del juego. 
        self.posiciones_casillas = posiciones_casillas
        self.crear_zombies()
        self.reaunudar_juego()

    def reaunudar_juego(self): # -> Metodo que permite reaunudar la partida (nos sirve en el caso)
        self.instanciar_timers() #  que el usuario pausa la partida. 
        self.timer_actualizar_datos.start()
        self.timer_movimiento_plantas.start()
        self.timer_lanzar_proyectil.start()
        self.timer_verificar_pos_proyectil.start()
        self.timer_generar_soles.start()
        self.timer_generar_lluvia_soles.start()
        self.timer_aparicion_zombies.start()
        self.timer_ataque_zombie.start()
        for zombie in self.zombies_actuales:
            zombie.mover()
        for proyectil in self.proyectiles:
            proyectil.timer_mover_proyectil.start()

    def pausar_juego(self): # -> Metodo que pausa todo el movimiento involucrado en el juego. 
        self.timer_actualizar_datos.stop()
        self.timer_generar_lluvia_soles.stop()
        self.timer_lanzar_proyectil.stop()
        self.timer_movimiento_plantas.stop()
        self.timer_verificar_pos_proyectil.stop()
        self.timer_generar_soles.stop()
        self.timer_aparicion_zombies.stop()
        self.timer_ataque_zombie.stop()
        for zombie in self.zombies_creados:
            zombie.detener()
        for proyectil in self.proyectiles:
            proyectil.timer_mover_proyectil.stop()

    def resetear_datos(self): # -> Metodo que borra todos los datos de la partida actual. 
        self.instanciar_timers()
        self.pausar_juego()
        for zombie in self.zombies_creados:
            zombie.detener()
            self.senal_ocultar_zombie.emit(zombie)
        for planta in self.posiciones_plantas.values():
            if planta.lanza_proyectil:
                planta.proyectiles.clear()
            elif planta.tipo == "girasol":
                self.senal_ocultar_soles.emit(planta.soles)
        self.senal_ocultar_proyectiles.emit(self.proyectiles)
        self.senal_ocultar_soles.emit(self.soles_jardin)
        self.senal_borrar_plantas.emit()
        self.soles_jardin.clear()
        self.carril_1.clear()
        self.carril_2.clear()
        self.posiciones_plantas.clear()
        self.proyectiles.clear()
        self.zombies_creados.clear()
        self.puntaje = 0
        self.zombies_destruidos = 0
        self.zombies_restantes = p.N_ZOMBIES * 2
        self.cantidad_soles = p.SOLES_INICIALES
        self.posiciones_casillas = None
    
    def cerrar_ventana(self): # -> Metodo que cierra la ventana actual abrir la ventana Post-Ronda.
        self.senal_cerrar_ventana.emit()
        self.senal_avanzar_ronda.emit()

    def partida_ganada(self): # -> Metodo que envia los datos de la partida ganada a la tabla de
        self.cerrar_ventana() #    de contenidos que se presenta en la ventana Post-Ronda
        datos = self.actualizar_datos()
        self.resetear_datos()
        self.senal_terminar_ronda.emit(datos, self.nombre, self.escenario_actual, "gano")

    def partida_perdida(self): # -> Metodo que envia los datos de la partida perdida a la tabla de
        self.cerrar_ventana() #    de contenidos que se presenta en la ventana Post-Ronda.
        datos = self.actualizar_datos()
        self.resetear_datos()
        self.senal_terminar_ronda.emit(datos, self.nombre, self.escenario_actual, "pierde")

    def avanzar_ronda(self): # -> Metodo que permite al usuario avanzar la partida al apretar el 
        if self.cantidad_soles >= p.COSTO_AVANZAR: #     boton 'avanzar' de la ventana del juego.
            self.partida_ganada()
        else:
            self.notificacion.enviar_notificacion("ronda", p.INTERVALO_AVANZAR)
        
    def recoger_soles(self, pos_x, pos_y): # -> Metodo que agrega soles a nuestra cantidad de soles
        for sol in self.soles_jardin: #         al hacerle click sobre ellos. 
            if sol.posicion.x() in list(range(pos_x - 40, pos_x + 40)) \
                and sol.posicion.y() in list(range(pos_y - 40, pos_y + 40)):
                self.cantidad_soles += p.SOLES_POR_RECOLECCION
                self.senal_ocultar_sol_especifico.emit(self.soles_jardin, (sol.pos_x, sol.pos_y))

    def matar_zombies(self): # -> Metodo que elimina a todos los zombies al apretar las teclas
        self.zombies_destruidos = p.N_ZOMBIES * 2 #                 K, I, L, consecutivamente.
        self.zombies_restantes = 0
    
    def soles_extra(self): # -> Metodo que agrega soles a nuestra cantidad de soles al apretar las
        self.cantidad_soles += p.SOLES_EXTRA #                   teclas S, U, N, consecutivamente.
        
            

  

    

        
            

        

            


        

    



    
        
        
    



    












































































