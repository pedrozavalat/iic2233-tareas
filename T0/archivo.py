import os
from random import randint, choice
from verificaciones import (
    coordenadas,
    medidas,
    opcion_usuario,
    )
from casillas import (
    ubicar_bestias,
    valores_casillas,
    flujo_juego
)
from parametros import POND_PUNT, PROB_BESTIA
from tablero import (
    print_tablero_con_utf8,
    print_tablero_sin_utf8,
    print_tablero)
from partida import (
    calcular_puntaje,
    cargar_partida,
    nueva_partida,
    guardar_partida,
    partida_ganada,
)

# definimos nuestra clase Main, la cual permitira la interaccion entre el usuario
# y el programa. Esta clase posee dos metodos princiapales (menu_inicio y menu_juego), 
# los cuales permiten el funcionamiento del juego, dada su interaccion entre sí. 
# La clase Main es instanciada en la linea 236, en donde nos permite iniciar el juego 
# en el terminal. 

class Main:
    # definimos el nombre del jugador y su puntaje para utilizarlos posteriormente
    # en los métodos de  menu de inicio y de menu de juego. 
    def __init__(self) -> None:
        self.nombre_jugador = ""
        self.puntaje = 0
    

    def menu_inicio(self):
        print()
        print(" START ADVANCED ".center(50, "="))
        print("Seleccione una opción:".center(50, " "))
        print('\n' * 4)
        print("""
        [1] Nueva partida
        [2] Cargar partida
        [3] Visualizar ranking de puntajes
        [0] Salir del juego
        """)
        print('\n' * 2)
        respuesta = ""
        respuesta = opcion_usuario(3)
        
        while respuesta != 0:

            if respuesta == 1:
                tablero = []
                tablero_bestias, usuario = nueva_partida() 
                # obtenemos el tablero y el nombre de usuario del jugador
                self.nombre_jugador = usuario   
                return self.menu_juego(tablero_bestias, tablero)
                break
            elif respuesta == 2:
                # solicitamos el nombre del usuario para verificar si
                # ha jugado previamente Start Advanced. Si existe un archivo
                # con su nombre en la carpeta partidas, entonces se abre 
                # respectivamente la partida guardada para seguir jugandola.  
                nombre_usuario = input("Nombre de usuario?: ")
                partida = f'{nombre_usuario.replace(" ", "")}.txt'
                ruta = os.path.join('partidas', partida)
                existe_partida = os.path.isfile(ruta)
                if existe_partida:
                    self.nombre_jugador = nombre_usuario
                    tablero, tablero_bestias = cargar_partida(ruta)
                    return self.menu_juego(tablero_bestias, tablero)
                    
                else:
                    print(f"La partida del usuario {nombre_usuario} no existe")
                    input('Apreta cualquier tecla para volver al menu de incio ...')
                    return self.menu_inicio()
                    
            elif respuesta == 3:
                # definimos la lista ranking, la cual contendra los puntajes de 
                # todos los jugadores que han finalizado una partida en el juego
                # (esta partida finalizada puede ser por una partida perdida, o
                # ganada. Pero, no guardada)
                ranking = []
                with open("puntajes.txt", 'r') as file:
                    archivo = file.readlines()
                    for linea in archivo:
                        linea = linea.strip().split(",")
                        nombre, puntaje = linea[0], int(linea[1])
                        ranking.append([nombre, puntaje])
                # ordenamos la lista segun la magnitud del puntaje
                def puntaje(lista):
                    return lista[1] * -1
                ranking.sort(key = puntaje)
                # mostramos la tabla del ranking de partidas, en contiene en 
                # cada fila: la posicion del jugador, su nombre, y el puntaje
                # de partida. 
                print('\n' * 3)
                print('TOP 10 JUGADORES'.center(50, "="))
                print('-' * 43)
                print('| Lugar | Nombre        | Puntaje         |')
                print('-' * 43)

                for i in range(len(ranking[:10])):
                    lugar = i + 1
                    nombre = ranking[i][0]
                    puntaje = ranking[i][1]
                    cadena = '|{:^7d}|{:15}|{:^17}|'.format(lugar, nombre, puntaje)
                    print(cadena)
                    print('-' * 43)

                input("\nPresione cualquier tecla para volver al inicio")
                return self.menu_inicio()


        print("Gracias por jugar Start Advanced ;)")
    
    def menu_juego(self, tablero_bestias, tablero):
        """
        Primero que todo, es importante definir que el tablero "tablero_bestias"
        contiene todos los valores de las celdas del juego, junto con las
        posiciones de las bestias. Mientras que el tablero "tablero" actualiza 
        los valores de cada celda segun los sectores que quiere descubrir el
        jugador. 
        """
        largo = len(tablero_bestias[0])
        ancho = len(tablero_bestias)
        # verifico si el tablero es guardado o es nuevo.
        # en el caso de que se inicie una nueva partida, entonces creamos un tablero
        if tablero == []:
            tablero = [[' ' for item in range(largo)] for item in range(ancho)]
        
        respuesta_2 = ""
        # definimos set_coords como el set que contiene las coordenadas de las casillas
        # que el jugador ha descubierto. 
        set_coords = list() 
        # mientras el jugador no quiere salir del menu de juego, puede guardar aquella
        # partida iniciada (o recuperada), o descubrir un nuevo sector (celda)
        while respuesta_2 != 0:
            print()
            print(" START ADVANCED".center(50, "="))
            print()
            print("¡Encuentra a las Bestias!")
            print()
            print_tablero(tablero)
            print("\nSeleccione una opción:")
            print(
                "\n[1] Descubir un sector\n"
                "[2] Guardar la partida\n"
                "[0] Salir de la partida\n"
            )    
            # si el jugador ha descubierto todas las casillas del tablero
            # y ha finalizado la partida sin haber descubierto ninguna
            # casilla con una bestia. Entonces, el jugador es ganador. 
            ha_ganado = partida_ganada(tablero)
            if ha_ganado:
                print('*' * 25)
                print('¡HAS GANADO LA PARTIDA!')
                print('*' * 25)
                print('\n' * 1)
                self.puntaje = calcular_puntaje(tablero, tablero_bestias, self.nombre_jugador)
                print(f'Tu puntaje obtenido fue de {self.puntaje}')
                print(f'Felicidades {self.nombre_jugador} :D')
                input('Precione una tecla para continuar ...')

                partida = f'{self.nombre_jugador.replace(" ", "")}.txt'
                ruta = os.path.join('partidas', partida)
                existe_ruta = os.path.isfile(ruta)
                # en el caso que el jugador haya ganado, borramos su archivo de la partida
                # finalizada de la carpeta 'partidas'. 
                if existe_ruta:
                    os.remove(ruta)
                break
            # en el caso que no haya ganado, el jugador sigue jugando ...
            respuesta_2 = opcion_usuario(2)

            if respuesta_2 == 1: # opcion para abrir una nueva celda
                # la funcion flujo_tablero nos entrega una actualizacion del tablero
                # segun el sector que el jugador quiere descubrir
                resultado, tablero = flujo_juego(
                    tablero,
                    tablero_bestias, 
                    set_coords, 
                    self.nombre_jugador)
                if resultado == "pierde": # si el jugador pierde (encontró una bestia) ...
                    print()
                    print_tablero(tablero_bestias)
                    self.puntaje = calcular_puntaje(tablero, tablero_bestias, self.nombre_jugador)
                    print("¡HAS ENCONTRADO UNA BESTIA!")
                    print("Perdiste :'(")
                    print()
                    print(f'Tu puntaje obtenido fue de {self.puntaje}')
                    print('\n' * 2)
                    input('Precione cualquier tecla para continuar ...')
                    partida = f'{self.nombre_jugador.replace(" ", "")}.txt'
                    ruta = os.path.join('partidas', partida)
                    existe_ruta = os.path.isfile(ruta)
                    # en el caso que el jugador haya perdido, borramos su archivo de la partida
                    # finalizada de la carpeta 'partidas'. 
                    if existe_ruta:
                        os.remove(ruta)
                    respuesta_2 = 0
                 # en el caso que no haya encontrado una bestia, se sigue jugando
                # (permanece en el menu de juego)
                elif resultado == "sigue":
                    pass
            
            # si el jugador quiere guardar la partida
            elif respuesta_2 == 2:
                # guardamos la partida del jugador como "nombre usuario".txt en la 
                # carpeta partidas
                partida = f'{self.nombre_jugador.replace(" ", "")}.txt'
                ruta = os.path.join('partidas', partida)
                existe_ruta = os.path.isfile(ruta)
                # en el caso que el jugador ya haya guardado anteriormente una partida
                if existe_ruta:
                    partida_actual =  guardar_partida(tablero, tablero_bestias)
                    with open(ruta, 'w') as file:
                        file.write(partida_actual)
                else:
                    partida_actual =  guardar_partida(tablero, tablero_bestias)
                    with open(ruta, 'w') as file:
                        file.write(partida_actual)

                print('\n' * 4)
                print('*' * 50)
                print('¡La partida se ha guardado de forma exitosa!'.center(50, " "))
                print('*' * 50)
                print('\n' * 4)
                input('Precione una tecla para continuar ...')
        # si el jugador quiere salir del juego, el metodo menu de juego retorna hacia
        # el metodo de menu de inicio. En este caso, seleccionaría la opción [0]
        self.menu_inicio()


# en el caso que nuestro archivo no ha sido importado
# (nuestro archivo principal: archivo.py), entonces iniciamos el juego,
# instanciando la clase Main, y luego llamamos el metodo menu_inicio
if __name__ == "__main__":
    start_advanced = Main()
    start_advanced.menu_inicio()
    
    
    

