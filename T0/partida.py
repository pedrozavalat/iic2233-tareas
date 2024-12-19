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
from math import ceil
from parametros import POND_PUNT, PROB_BESTIA
import os

"""
La funcion nueva_partida es llamada desde el menu de inicio, con el objetivo
de crear una nueva partida del usuario. En este caso, retorna el nombre del jugador
y el tablero segun las medidas que él indica. 
"""
def nueva_partida():
    # el nombre de usuario debe poseer un maximo de 15 carácteres para
    # asi no alterar la tabla del ranking de puntajes
    continuar = True
    while continuar:
        print("Debes considerar un nombre de usuario de 1 a 15 carácteres")
        nombre_usuario = str(input("Nombre de usuario?: "))
        if len(nombre_usuario) <= 15:
                continuar = False
        else:
            print(
                "El nombre de usuario debe tener 15 carácteres como máximo"
                "y 1 caracter como mínimo")
            nombre_usuario = input("Nombre de usuario?: ")
              
    print("=" * 50)
    print("\n" * 1)
    print( "\n" * 1)
    print(" CREA TU TABLERO ".center(50, "="))
    print(f"¡Hola {nombre_usuario}!".center(50, " "))
    print("Indica las medidas de su tablero\n".center(50, " "))
    print("Los valores tanto para el ancho como para el largo")
    print("del tablero debenestar entre 3 y 15, incluyéndolos")
    print()
    # funcion que verifica si las medidas del tablero son pertinentes al rango
    # establecido (entre 3 y 15)
    par = medidas() # en el caso que cumpla la condición,
                    # recibimos el par de medidas (x,y), como tupla 

    largo = par[0] # largo del tablero (X)
    ancho = par[1] # ancho del tablero (Y)
        
    tablero_bestias = [[0 for item in range(largo)] for item in range(ancho)]
        
    # obtenemos la cantidad de bestias 
    cantidad_bestias = ceil(largo * ancho * PROB_BESTIA) 

    # ubicamos aleatoriamente las posiciones de la bestias
    for veces in range(0, cantidad_bestias):
        ubicar_bestias(tablero_bestias, largo, ancho)
        
    # y ubicamos para cada casilla la cantidad de minas
    # que se ubican en su alrededor 
    for fila in range(ancho):
        for celda in range(largo):
            if tablero_bestias[fila][celda] == 'N':
                valores_casillas(tablero_bestias, celda, fila)
    return tablero_bestias, nombre_usuario

"""
funcion que retorna todas las posiciones de las bestias del tablero y las posiciones 
de las casillas descubiertas de la partida actual. El formato en que se guarda 
cada posicion en el archivo es:
posicion x1, posicion y1 : valor1  ...  posicion xn, posicion yn : valorn 
cada linea de texto que contiene una posicion y su valor, presenta un salto
de línea al final
"""

def guardar_partida(tablero, tablero_bestias):
    # texto que contendrá todas las posiciones de las celdas descubiertas
    # del tablero, junto con sus valores, de la partida actual que se quiere
    # guardar:
    pos_tablero = ""
    # texto que contendrá todas las posiciones de las celdas, junto con sus
    # valores, del tablero de la partida actual que se quiere guardar:  
    pos_tablero_bestias = ""

    largo = len(tablero[0]) # eje x
    ancho = len(tablero)    # eje y

    for fila in range(ancho):
        for celda in range(largo):
            # agregamos en una string los valores de cada celda
            # descubierta del tablero con sus posiciones respectivas.  
            # con el formato (posicion) : valor en el tablero
            
            pos_tablero += f'{celda},{fila}:{tablero[fila][celda]}\n'

            # analogamente, se guardan las posiciones de todas las celdas
            # junto con sus valores respectivos (tablero_bestias)
            pos_tablero_bestias += f'{celda},{fila}:{tablero_bestias[fila][celda]}\n'

    
    
    # guardamos tanto las posiciones del tablero, como las posiciones del 
    # tablero_bestias. Estos archivos los unimos en uno solo con un '#'
    # donde pos_tablero: posiciones del tablero
    #       pos_tablero_bestias: posiciones de las bestias (junto con los valores
    #       que indican la cantidad de bestias que estan alrededor  una celda)
    pos_tableros = f'{pos_tablero}\n#\n{pos_tablero_bestias}'

    return pos_tableros

"""
funcion que retorna el tablero (tablero) de la partida consultada y el tablero que
contiene todas las celdas con las posiciones de las bestias (tabero_bestias). 
Ambos tableros se retornan en listas de listas.
"""

def cargar_partida(ruta):
    # cargamos la ruta entregada para visualizar los datos del archivo 
    with open(ruta, 'r') as archivo:
        largo = set() 
        ancho = set()
        archivo = archivo.readlines()
        lista_archivos = [linea.strip() for linea in archivo]
        # El archivo esta separado con un #, el cual representa
        # la division entre el contenido del 'tablero' y el del
        # 'tablero_bestias'
        limite = lista_archivos.index('#')
        # separamos el archivo en dos y luego generamos dos subarchivos:
        # arch_tablero: archivo que contiene informacion del tablero con 
        # las posiciones guardadas
        # arch_tablero_bestias: archivo que contiene informacion del tablero 
        # con todas las posiciones de las bestias. 
        arch_tablero = lista_archivos[:limite - 1]
        arch_tablero_bestias = lista_archivos[limite + 1:]
        lista_tab = [item.split(":") for item in arch_tablero]
        lista_tab_bestias = [item.split(":") for item in arch_tablero_bestias]

        # Por otro lado, identificamos las medidas de los tableros (ya que, tienen
        # la misma medida)
        
        for fila in lista_tab:
            pos = fila[0].split(",")
            
            # obtenemos las coordenadas
            # (dado que esta en formato strings, calculamos 
            # la posicion del caracter que representa la posicion)
            
            pos_x, pos_y = int(pos[0]), int(pos[1])
            largo.add(pos_x)
            ancho.add(pos_y)
        # segun los valores de coordenadas entregados para
        # cada eje, el largo de los sets ancho y largo nos entregara 
        # las medidas del tablero
        ancho = len(ancho)
        largo = len(largo)

        # en segundo lugar, creamos los tableros vacios con las medidas obtenidos
        tablero = [[' ' for celda in range(largo)] for fila in range(ancho)]
        tablero_bestias = [[' ' for celda in range(largo)] for fila in range(ancho)]

        # y finalmente, rellenamos cada tablero con sus valores correspondientes
        # a cada posicion, respectivamente. 
    
        for fila in lista_tab:
            pos, valor = fila[0].split(","), fila[1]
            pos_x, pos_y = int(pos[0]), int(pos[1])

            if valor.isdigit():
                tablero[pos_y][pos_x] = int(valor)
            elif valor != 'N' and not valor.isdigit():
                tablero[pos_y][pos_x] = ' '
            else:
                tablero[pos_y][pos_x] = 'N'

        for fila in lista_tab_bestias:
            pos, valor = fila[0].split(","), fila[1]
            pos_x, pos_y = int(pos[0]), int(pos[1])

            if valor.isdigit():
                tablero_bestias[pos_y][pos_x] = int(valor)
            else:
                tablero_bestias[pos_y][pos_x] = valor
        
    return tablero, tablero_bestias
    

"""
función que calcula el puntaje de un jugador cuando ya ha finalizado su partida 
(para los casos que el jugador haya perdido, o ganado)
"""
def calcular_puntaje(tablero, tablero_bestias, nombre_jugador):
    cant_bestias = 0
    celdas_descubiertas = 0
    puntaje = 0
    # cuento la cantidad de bestias en el tablero
    for fila in tablero_bestias:
        cant_bestias += fila.count('N')
    # cuento la cantidad de celdas descubiertas
    for fila in tablero:
        for celda in fila:
            if celda != 'N' and celda != ' ':
                celdas_descubiertas += 1
    # calculamos el puntaje
    puntaje = cant_bestias * celdas_descubiertas * POND_PUNT
    ruta = 'puntajes.txt'
    texto = f'{nombre_jugador},{puntaje}\n' 
    
    # escribimos el nombre de usuario, su puntaje de la partida
    # y el tamaño el tablero jugado.
    with open(ruta, 'a') as file:
        file.write(texto)

    return puntaje 
"""
funcion que verifica si la partida es ganada. Retorna un booleano segun
las cantidades de celdas vacias, cuyas se encuentras como ' ' en el tablero
que esta en constante actualizacion (tablero "tablero")
"""
def partida_ganada(tablero):
    celdas_vacias = 0
    for fila in tablero:
        celdas_vacias += fila.count(' ')
    # si todas las celdas del tablero actual estan
    # descubiertas, entonces el usuario gano
    if celdas_vacias == 0:
            return True
    else:
        return False
    
