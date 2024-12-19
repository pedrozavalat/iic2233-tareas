from entrenadores import Entrenador, Baya, Pocion, Caramelo
from programon import Planta, Fuego, Agua
from parametros import PROB_EXITO_BAYA, PROB_EXITO_CARAMELO,\
                        PROB_EXITO_POCION, GASTO_ENERGIA_BAYA, \
                        GASTO_ENERGIA_CARAMELO, GASTO_ENERGIA_POCION
from random import choice, choices


class LigaProgramon:
    def __init__(self):
        self.entrenadores = []
        self.jugadores_actuales = set()
        self.ronda_actual = 1
        self.campeon = ""
        self.lista_programones = []
        self.perdedores = []
        self.lista_objetos = []

    # seleccion_opcion: metodo que verifica que la respuesta entregada frente
    # a la alternativas de opciones pertenece al rango total de opciones. 
    def seleccionar_opcion(self, numero):
        elegir_opciones = [str(item) for item in range(1, numero + 1)]
        # quiero mostrar la lista de opciones que el jugador debe indicar
        # de esta manera -> (1, 2, 3, o 4). 
        # Considero todas las opciones excepto la ultima, ya que esta la uniré con un "o"
        ultima_opcion = elegir_opciones[-1]
        opciones = ", ".join(elegir_opciones[0:-1])
        opcion = input(f"\nIndique su opcion ({opciones}, o {ultima_opcion}) =>")
        while opcion not in elegir_opciones:
            print("Su opcion debe estar en el rango prestablecido")
            opcion = input("Porfavor, introduzca correctamente >>>")
        return int(opcion)

    # estado_del_campeonato: metodo que muestra el estado actual del entrenador
    def estado_del_campeonato(self, entrenador_elegido):
        print("\n\n**** {: ^30s} ****".format("Resumen del campeonato"))
        print("-" * 40)
        participantes = ""
        jugadores_actuales = ""
        # muestro si nuestro entrenador elegido sigue en juego
        print(f'Entrenador elegido: {entrenador_elegido.nombre}\n')
        # muestro los participantes del campeonato
        for entrenador in self.entrenadores:
            participantes += f", {entrenador.nombre}"
        print(f'Participantes: {participantes}')
        print(f'Ronda Actual: {self.ronda_actual}')
        for entrenador in self.jugadores_actuales:
            jugadores_actuales += f", {entrenador.nombre}"
        if self.ronda_actual == 1:
            print(f'Entrenadores que siguen en la competencia: {participantes}')
        else:
            print(f'Entrenadores que siguen en la competencia: {jugadores_actuales}')
        input('\nSelecciona cualquier tecla para volver atrás ...')


    # simular_ronda: metodo que simula los enfrentamientos entre dos entrenadores, 
    #                en donde forma partidas entre dos jugadores y luego las imprime
    #                en el terminal.
    def simular_ronda(self, entrenador_elegido):
        # elijo mi programon
        print("\n\n**** {: ^30s} ****".format("¡Elige tu luchador!"))
        print("=" * 40)
        for programon in entrenador_elegido.programones:
            index = entrenador_elegido.programones.index(programon) + 1
            print(f'[{index}] {programon.nombre}')
        cant_programones = len(entrenador_elegido.programones)
        print(
            f"[{cant_programones + 1}] Volver\n"
            f"[{cant_programones + 2}] Salir\n")
        opcion_volver = cant_programones + 1
        opcion_salir = cant_programones + 2
        respuesta = self.seleccionar_opcion(cant_programones + 2)
        # observacion: los terminos sumativos "+ 1" o "+ 2" los utilice para evitar 
        #               un IndexError    
        while respuesta != opcion_salir: 
            if respuesta < opcion_volver:
                entrenador_elegido.programon_ronda = entrenador_elegido.programones[respuesta - 1]
                # las parejas no deben repetirse, por ello usamos un set
                parejas_ronda_actual = set() 
                # si es la ronda 1, formamos parejas con todos los entrenadores disponibles
                if self.ronda_actual == 1:
                    self.jugadores_actuales = [jugador for jugador in self.entrenadores]
                # si es una ronda distinta a la primera, formamos parejas segun los jugadores
                # actuales
                # para evitar la repeticion de parejas al formarlas, ordenaremos
                # la dupla alfabeticamente
                
                print(f"Ronda {self.ronda_actual}".center(40, " "))
                print("-" * 40)
                # creamos las parejas
                # elegir_jugadores: set que incluye todos los jugadores actuales de la ronda, y
                #                   lo utilizamos para formar las parejas 
                elegir_jugadores = self.jugadores_actuales
                # formarmos las parejas hasta que el momento que se hayan elegido 
                # todos los jugadores. 
                while len(parejas_ronda_actual) != (len(self.jugadores_actuales) / 2):
                    pareja_aleatoria = choices(elegir_jugadores, k = 2)            
                    dupla = (pareja_aleatoria[0], pareja_aleatoria[1])
                    def por_nombre(entrenador):
                        return entrenador.nombre
                    # evitamos que se repitan las duplas
                    pareja_aleatoria.sort(key = por_nombre) 
                    if dupla[0].nombre != dupla[1].nombre:
                        parejas_ronda_actual.add(dupla)
                        elegir_jugadores = set(elegir_jugadores)
                        elegir_jugadores.remove(dupla[0])
                        elegir_jugadores.remove(dupla[1])
                        elegir_jugadores = list(elegir_jugadores)
                        # convertimos elegir_jugadores de set a lista para luego utilizar 
                        # la funcion choices
                # simulamos la batalla entre cada pareja
                for pareja in parejas_ronda_actual: 
                    jugador_1 = pareja[0]
                    jugador_2 = pareja[1]
                    # en el caso que uno de los dos jugadores sea nuestro entrenador seleccionado
                    if jugador_1 == entrenador_elegido:
                        programon_jugador_1 = entrenador_elegido.programon_ronda
                        programon_jugador_2 = choice(jugador_2.programones)
                    elif jugador_2 == entrenador_elegido:
                        programon_jugador_1 = choice(jugador_1.programones)
                        programon_jugador_2 = entrenador_elegido.programon_ronda
                    else:
                        programon_jugador_1 = choice(jugador_1.programones)
                        programon_jugador_2 = choice(jugador_2.programones)
                    print(
                        f'{jugador_1.nombre} usando al '
                        f'programon {programon_jugador_1.nombre}, se enfrenta'
                        f'a {jugador_2.nombre} usando al programon '
                        f'{programon_jugador_2.nombre}')
                    # dado el método luchar (explicado en el archivo programon.py), 
                    # definimos nuestro ganador 
                    programon_ganador = programon_jugador_1.luchar(programon_jugador_2)
                    if programon_ganador == programon_jugador_1:
                        ganador = jugador_1
                        print(f'{jugador_1.nombre} ha ganado la batalla\n')
                        self.perdedores.append(jugador_2)
                        self.jugadores_actuales.remove(jugador_2)
                    else:
                        ganador = jugador_2
                        print(f'{jugador_2.nombre} ha ganado la batalla\n')
                        self.perdedores.append(jugador_1)
                        self.jugadores_actuales.remove(jugador_1)
                #reiniciamos la energia al máximo de los entrenadores que siguen en el campeonato
                for entrenador in self.jugadores_actuales:
                    entrenador.energia = 100

                self.ronda_actual += 1
                # en el caso que sea la ultima ronda ... 
                if self.ronda_actual == 4:
                    self.campeon = ganador.nombre 
                    print("\n\n\n")
                    if self.campeon == entrenador_elegido.nombre: # en el caso que ganemos
                        print("* {:^30s} *".format("Felicidades, has ganado el DCCampeonato"))
                    else:
                        print("* {:^30s} *".format(f"{self.campeon} ha ganado el DCCampeonato"))
                    print("\n\n\n")
                # si el jugador pierde, puede salir del juego o optar una nueva partida
                if entrenador_elegido in self.perdedores:
                    print("~" * 50)
                    print(f"\n\n Has perdido el DCCampeonato :(\n\n")
                    print("~" * 50)
                    print(
                        "\n[1] Nueva partida\n"
                        "[2] Salir del juego")
                    respuesta = self.seleccionar_opcion(2)
                    if respuesta == 1: # si comienza una nueva partida
                        # restauramos todos los datos de la partida
                        # es decir, comenzamos desde cero. 
                        self.ronda_actual = 1
                        self.perdedores = []
                        self.entrenadores = []
                        self.lista_objetos = []
                        self.lista_programones = []
                        self.crear_programones()
                        self.crear_entrenadores()
                        self.crear_objetos()
                        return self.menu_inicio()
                    else:
                        break 
                # en el caso que haya ganado, vuelve nuevamente al menu del entrenador
                input("Seleccione cualquier tecla para continuar ...")
                return self.menu_entrenador(entrenador_elegido)
            else:
                return self.menu_entrenador(entrenador_elegido)
        print("Gracias por jugar :)")

    # crear_programones: metodo que instacia los programones del juego 
    def crear_programones(self):
        with open("programones.csv") as archivo_2:
            archivo_2 = archivo_2.readlines()
            lista_programones = [linea.strip().split(",") for linea in archivo_2]
            lista_programones = lista_programones[1:]
            for dato in lista_programones:
                nombre = dato[0] 
                tipo = dato[1].capitalize()
                nivel = int(dato[2])
                vida = int(dato[3])
                ataque = int(dato[4])
                defensa = int(dato[5])
                velocidad = int(dato[6])
                if tipo == "Planta":
                    programon = Planta(nombre, tipo, nivel, vida, ataque, defensa, velocidad)
                elif tipo == "Fuego":
                    programon = Fuego(nombre, tipo, nivel, vida, ataque, defensa, velocidad)
                elif tipo == "Agua":
                    programon = Agua(nombre, tipo, nivel, vida, ataque, defensa, velocidad)
                self.lista_programones.append(programon)

    # crear_entrenadores: metodo que instancia los entrenadores del juego
    def crear_entrenadores(self):
        with open ("entrenadores.csv") as archivo:
            archivo = archivo.readlines()
            lista_de_datos = [linea.strip().split(",") for linea in archivo]
            lista_de_datos = lista_de_datos[1:]
            # Instanciamos cada entrenador y lo agregamos a la lista de entrenadores
            for dato in lista_de_datos:
                nombre = dato[0]
                programones = dato[1].split(";")
                energia = int(dato[2])
                objetos = dato[3].split(";")
                entrenador = Entrenador(nombre, programones, energia, objetos)
                self.entrenadores.append(entrenador)
        # agregamos a cada entrenador sus programones respectivos (ya instanciados)
        for entrenador in self.entrenadores: 
            programones_entrenador = []
            for programon in self.lista_programones:
                if programon.nombre in entrenador.programones:
                    programones_entrenador.append(programon)
            entrenador.programones = programones_entrenador
            
    # crear_objeto: metodo que instancia los objetos respectivos de cada entrenador
    def crear_objetos(self):
        with open("objetos.csv") as archivo:
            archivo = archivo.readlines()
            lista_de_datos = [linea.strip().split(",") for linea in archivo]
            lista_de_datos = lista_de_datos[1:]
            # verificamos el tipo de objeto
            for dato in lista_de_datos:
                nombre = dato[0]
                tipo = dato[1]
                # segun el tipo de objeto, este tendrá características especificas que
                # difieren en respecto a los otros tipos de objetos.
                if tipo == "pocion":
                    costo = GASTO_ENERGIA_POCION
                    prob_exito = PROB_EXITO_POCION
                    self.lista_objetos.append(Pocion(nombre, tipo, costo, prob_exito))
                elif tipo == "caramelo":
                    costo = GASTO_ENERGIA_CARAMELO
                    prob_exito = PROB_EXITO_CARAMELO
                    self.lista_objetos.append(Caramelo(nombre, tipo, costo, prob_exito))
                elif tipo == "baya":
                    costo = GASTO_ENERGIA_BAYA
                    prob_exito = PROB_EXITO_BAYA
                    self.lista_objetos.append(Baya(nombre, tipo, costo, prob_exito))
        # agregamos a cada entrenador sus objetos respectivos (ya instanciados)
        for entrenador in self.entrenadores:
            objetos_entrenador = []
            for objeto in self.lista_objetos:
                if objeto.nombre in entrenador.objetos:
                    objetos_entrenador.append(objeto)
            entrenador.objetos = objetos_entrenador
        
