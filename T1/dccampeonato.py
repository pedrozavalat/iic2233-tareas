from ligaprogramon import LigaProgramon     
from parametros import ENERGIA_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO,\
                     MIN_AUMENTO_ENTRENAMIENTO
from random import randint, choice, random


class DCCampeonato(LigaProgramon):
    def __init__(self, *args):
        super().__init__(*args)

    def menu_inicio(self):
        print("**** {: ^30s} ****".format("Menu de inicio"))
        print("=" * 40)
        for entrenador in self.entrenadores:
            index = self.entrenadores.index(entrenador) + 1
            mostrar_programones = [programon.nombre for programon in entrenador.programones]
            print(f'[{index}] {entrenador.nombre}: {", ".join(mostrar_programones)}')
        print(f'[{len(self.entrenadores) + 1}] Salir')
        print("\nSelecciona tu entrenador! ")
        # verifico que la opcion se encuentra en el rango de opciones del menu
        respuesta = self.seleccionar_opcion(17) # retorna el indice del entrenador elegido
        while respuesta != 17:  # en el caso que no quiera salir del programa
            # consideramos que la lista de entrenadores va desde 0 a 15 (por eso se resta 1)
            entrenador_elegido = self.entrenadores[respuesta - 1]
            return self.menu_entrenador(entrenador_elegido)
        print("Gracias por jugar")
    
    #método menu_entrenador: permite dirigir la accion del jugador a otro menús
    def menu_entrenador(self, entrenador_elegido):
        print("\n**** {: ^30s} ****".format("Menu Entrenador"))
        print("=" * 40)
        print(f"¡Hola {entrenador_elegido.nombre}!\n\n"
            "[1] Entrenamiento\n"
            "[2] Simular ronda\n"
            "[3] Resumen campeonato\n"
            "[4] Crear objetos\n"
            "[5] Utilizar objeto\n"
            "[6] Estado entrenador\n"
            "[7] Volver al menu de inicio\n"
            "[8] Salir del juego")
        respuesta = self.seleccionar_opcion(8)
        while respuesta != 8:
            if respuesta == 1:
                return self.menu_de_entrenamiento(entrenador_elegido)
            elif respuesta == 2:
                return self.simular_ronda(entrenador_elegido)
            elif respuesta == 3:
                self.estado_del_campeonato(entrenador_elegido)
                return self.menu_entrenador(entrenador_elegido)
            elif respuesta == 4:
                return self.crear_objeto(entrenador_elegido)
            elif respuesta == 5:
                return self.utilizar_objeto(entrenador_elegido)
            elif respuesta == 6:
                return self.estado_entrenador(entrenador_elegido)
            elif respuesta == 7:
                return self.menu_inicio()
        print("Gracias por jugar :)")
    
    # método menu_de_entrenamiento: Permite mejorar habilidades del programon
    def menu_de_entrenamiento(self, entrenador_elegido):
        print("\n\n**** {: ^30s} ****".format("Menu de Entrenamiento"))
        print("=" * 40)
        print("¡Elige un Programon para entrenarlo!\n")
        #imprimimos los programones del entrenador
        for programon in entrenador_elegido.programones: 
            index = entrenador_elegido.programones.index(programon) + 1
            print(f'[{index}] {programon.nombre}')
        cant_programones = len(entrenador_elegido.programones)
        respuesta = self.seleccionar_opcion(cant_programones)
        programon_elegido = entrenador_elegido.programones[respuesta - 1] 
        # si el entrenador no tiene energia, no será posible entrenar
        # sus programones.
        # si el programon tiene nivel 100, el entrenamiento no hara efecto
        if programon_elegido.nivel == 100:
            print(f"Tu programon tiene nivel 100, está muy entrenado :o")
            pass
        else: 
            if entrenador_elegido.energia < ENERGIA_ENTRENAMIENTO:
                print("X" * 80)
                print(
                    "\nNo cuentas con la energia suficiente "
                    "para entrenar a tu programon :(\n"
                    f"Tienes {entrenador_elegido.energia} de energia y requieres "
                    f"{ENERGIA_ENTRENAMIENTO} de energia para entrenar\n")
                print("X" * 80)
                    
            else: # en el caso que el entrenador tiene energia suficiente
                entrenador_elegido.energia -= ENERGIA_ENTRENAMIENTO
                # se le aumenta la experiencia del programon, de forma aleatoria
                aumento_xp_programon = randint(MIN_AUMENTO_ENTRENAMIENTO,\
                                                MAX_AUMENTO_ENTRENAMIENTO)
                programon_elegido.experiencia += aumento_xp_programon
                print("*" * 80)
                print(
                    "\n¡Vaya! Que buen entrenamiento\n"
                    f"Has gastado {ENERGIA_ENTRENAMIENTO} puntos de energia "
                    f"y tu programón {programon_elegido.nombre}\n"
                    f"ha aumentado {aumento_xp_programon} "
                    "puntos de experiencia!\n")
                print("*" * 80)
        input("\n\nSelecciona cualquier tecla para continuar...\n")
        return self.menu_entrenador(entrenador_elegido)        
    
    # crear_objeto: metodo que crea un nuevo objeto para nuestro entrenador elegido
    def crear_objeto(self, entrenador_elegido):
        print("\n\n**** {: ^30s} ****".format("Menu Objeto"))
        print("=" * 40)
        print(
                "[1] Baya\n"
                "[2] Pocion\n"
                "[3] Caramelo\n"
                "[4] Volver\n"
                "[5] Salir")
        respuesta = self.seleccionar_opcion(5)
        while respuesta != 5:
            if respuesta == 1: 
                # elegimos aleatoriamente un objeto de tipo baya
                obj_random = choice([obj for obj in self.lista_objetos if (obj.tipo == "baya")\
                                    and (obj not in entrenador_elegido.objetos)])
                # en el caso que la energia del entrenador no es suficiente
                # para crear un objeto ... 
                if entrenador_elegido.energia < obj_random.costo:
                    print(
                        "No puedes crear el objeto, tu energia "
                        "es insuficiente :(")
                else:
                    entrenador_elegido.energia -= obj_random.costo
                    # definimos 'prob_random' a la probabilidad aleatoria..
                    # ..de crear un objeto. En el caso que, la probabilidad prob_random.. 
                    # ..sea mayor o igual a la probabilidad de exito del objeto, entonces..
                    # ..éste se creará. 
                    prob_random = round(random(), 1)
                    if prob_random < obj_random.probabilidad_exito:
                        print("\n\n ERROR: No se ha podido crear el objeto :(\n\n")
                    else:
                        print("*" * 40)
                        print("\n¡El objeto ha sido creado exitosamente!")
                        print(f"OBJETO ADQUIRIDO => {obj_random.nombre}\n")
                        print("*" * 40)
                        entrenador_elegido.objetos.append(obj_random) 
            elif respuesta == 2:
                obj_random = choice([obj for obj in self.lista_objetos if (obj.tipo == "pocion")\
                                    and (obj not in entrenador_elegido.objetos)])
                if entrenador_elegido.energia < obj_random.costo:
                    print(
                        "No puedes crear el objeto, tu energia "
                        "es insuficiente :(")
                else:
                    entrenador_elegido.energia -= obj_random.costo
                    prob_random = round(random(), 1)
                    if prob_random < obj_random.probabilidad_exito:
                        print("\n\n ERROR: No se ha podido crear el objeto :(\n\n")
                    else:
                        print("*" * 40)
                        print("\n¡El objeto ha sido creado exitosamente!")
                        print(f"OBJETO ADQUIRIDO => {obj_random.nombre}\n")
                        print("*" * 40)
                        entrenador_elegido.objetos.append(obj_random) 
            elif respuesta == 3:
                obj_random = choice([obj for obj in self.lista_objetos if (obj.tipo == "caramelo")\
                                    and (obj not in entrenador_elegido.objetos)])
                if entrenador_elegido.energia < obj_random.costo:
                    print(
                        "No puedes crear el objeto, tu energia "
                        "es insuficiente :(")
                else:
                    entrenador_elegido.energia -= obj_random.costo
                    prob_random = round(random(), 1)
                    if prob_random < obj_random.probabilidad_exito:
                        print("\n\n ERROR: No se ha podido crear el objeto :(\n\n")
                    else:
                        print("*" * 40)
                        print("\n¡El objeto ha sido creado exitosamente!")
                        print(f"OBJETO ADQUIRIDO => {obj_random.nombre}\n")
                        print("*" * 40)
                        entrenador_elegido.objetos.append(obj_random) 
            elif respuesta == 4:
                return self.menu_entrenador(entrenador_elegido)
            input("\n\n selecciona cualquier tecla para continuar...")  
            return self.crear_objeto(entrenador_elegido)
        print("Gracias por jugar :)")
    
    # utilizar_objeto: metodo que permite al entrenador aplicar los beneficios
    #                  de sus objetos sobre sus programones
    def utilizar_objeto(self, entrenador_elegido):
        print("\n\n**** {: ^30s} ****".format("Objetos Disponibles"))
        print("=" * 40)
        print('\nSelecciona el objeto que quieres utilizar:')
        for objeto in entrenador_elegido.objetos:
            index = entrenador_elegido.objetos.index(objeto) + 1
            print(f'[{index}] {objeto.nombre} (tipo: {objeto.tipo})')
        cant_objetos = len(entrenador_elegido.objetos)
        print(
            f"[{cant_objetos + 1}] Volver\n"
            f"[{cant_objetos + 2}] Salir\n")
        respuesta_1 = self.seleccionar_opcion(cant_objetos + 2)
        opcion_volver = cant_objetos + 1
        opcion_salir = cant_objetos + 2

        while respuesta_1 != opcion_salir:
            if respuesta_1 < opcion_volver:
                obj_elegido = entrenador_elegido.objetos[respuesta_1 - 1] 
                # en el caso que el entrenador no tenga la energia suficiente 
                # para utilizar un objeto 
                print(
                    f'\nHas elegido el objeto {obj_elegido.nombre}\n'
                    'Selecciona el programon que quieres aplicarle '
                    'el objeto :)\n')
                for programon in entrenador_elegido.programones:
                    index = entrenador_elegido.programones.index(programon) + 1
                    print(f'[{index}] {programon.nombre}')
                cant_programones = len(entrenador_elegido.programones)
                respuesta_2 = self.seleccionar_opcion(cant_programones)

                programon_elegido = entrenador_elegido.programones[respuesta_2 - 1]
                
                print("-"*40)
                print( 
                    f"Programon beneficiado: {programon_elegido.nombre}\n"
                    f"Objeto utilizado: {obj_elegido.nombre} (tipo {obj_elegido.tipo})\n")
                # metodo que atribuye los beneficios del objeto elegido a un programon,
                # el cual varía segun el tipo de programon 
                obj_elegido.aplicar_objeto(programon_elegido)
                print("-"*40)
                input("\n Selecciona cualquier tecla para continuar...\n")
                return self.utilizar_objeto(entrenador_elegido)
            else:
                return self.menu_entrenador(entrenador_elegido)
        print("Gracias por jugar :)")

    # estado_entrenador: metodo que muestra el estado del entrenador 
    #                    y las características de sus programones. 
    def estado_entrenador(self, entrenador_elegido):
        print("\n\n**** {: ^45s} ****".format("Objetos Disponibles"))
        lista_objetos = ", ".join([objeto.nombre for objeto in entrenador_elegido.objetos])
        print("-" * 60)
        print(
            f"Nombre: {entrenador_elegido.nombre}\n"
            f"Energia: {entrenador_elegido.energia}\n"
            f"Objetos: {lista_objetos}\n"
            )
        print("-" * 60)
        print("{: ^60s}".format("Programones"))
        print("-" * 60)    
        print("|{:^25}|{:^10}|{:^10}|{:^10}|".format("Nombre", "Tipo", "Nivel", "Vida"))
        print("-" * 60)    
        for programon in entrenador_elegido.programones:
            nombre = programon.nombre
            tipo = programon.tipo
            nivel = programon.nivel  
            vida = programon.vida
            cadena = "|{:<25}|{:^10}|{:^10}|{:^10}|".format(nombre, tipo, nivel, vida)
            print(cadena)
        input("\n\nSelecciona cualquier tecla para volver atrás...")
        return self.menu_entrenador(entrenador_elegido)
        
        
    
    