
import random
from verificaciones import coordenadas
import os

"""    
definimos dos funciones principales que formaran el tablero que posee las cantidades 
de bestias:

1. ubicar_bestias: recibe el tablero 'tablero_bestias', junto con sus medidas. Para así,
   retornar un tablero con una cantidad de bestias exactas ubicadas aleatoriamente. 
2. valores_casillas: recibe el tablero generado por la funcion ubicar_bestias, en donde asigna
   para cada casilla un valor segun la cantidad de bestias ubicadas alrededor de aquella. 

* comentarios: ambas funciones fueron implementadas gracias al codigo escrito
 en la siguiente fuente:
fuente: 
'How to program MineSweeper in Python' - https://replit.com/talk/learn

Esta página tenia el objetivo de crear el juego 'buscaminas', la cual fue
de gran ayuda para poder generar las funciones anteriores. :) 

"""
def ubicar_bestias(tablero, largo, ancho):
    x = random.randint(0, largo - 1)
    y = random.randint(0, ancho - 1)
    if not tablero[y][x] == 'N':
        tablero[y][x] = 'N'
    else:
        ubicar_bestias(tablero, largo, ancho)

def valores_casillas(tablero, celda, fila):
    # celda : posicion actual en el eje x
    # fila : posicion actual en el eje y 
    largo = len(tablero[0]) # eje x
    ancho = len(tablero)    # eje y
    # verificamos la fila superior
    
    if fila - 1 >= 0:
        fila_actual = tablero[fila - 1]
        #celda actual 'al principio' de la fila
        if celda - 1 >= 0:
            if fila_actual[celda - 1] != 'N':
                fila_actual[celda - 1] += 1
        #celda actual 'entre ambos extermos' de la fila
        if fila_actual[celda] != 'N':
            fila_actual[celda] += 1
        #celda actual 'al filal' de la fila
        if celda + 1 < largo: 
            if fila_actual[celda + 1] != 'N':
                fila_actual[celda + 1] += 1

    # verificamos la fila inferior
    if fila + 1 < ancho:
        fila_actual = tablero[fila + 1]
        #celda actual 'al principio' de la fila
        if celda - 1 > -1:
            if fila_actual[celda - 1] != 'N':
                fila_actual[celda - 1] += 1
        #celda actual 'entre ambos extermos' de la fila
        if fila_actual[celda] != 'N':
            fila_actual[celda] += 1
        #celda actual 'al filal' de la fila
        if celda + 1 < largo: # tablero[0] = ancho del tablero
            if fila_actual[celda + 1] != 'N':
                fila_actual[celda + 1] += 1
    
    #verificamos la fila actual
    fila_actual = tablero[fila]
    #celda actual 'entre ambos extermos' de la fila
    if celda - 1 >= 0:
            if fila_actual[celda - 1] != 'N':
                fila_actual[celda - 1] += 1
    #celda actual 'al filal' de la fila
    if celda + 1 < largo: # tablero[0] = ancho del tablero
            if fila_actual[celda + 1] != 'N':
                fila_actual[celda + 1] += 1

"""
La funcion flujo_juego nos permite verificar si la coordenada de la celda a descubrir
contiene una bestia, o no. Esta función retorna una actualizacion del tablero segun
el valor que contiene la celda a descubrir. 
"""

def flujo_juego(tablero, tablero_bestias, set_coords, nombre_jugador):
        # se entrega la posicion del tablero en terminos numéricos
        coordenada = coordenadas(tablero) # formato: (x,y)
        # verificamos si la coordenada no ha sido ingresada previamente
        set_coords.append(coordenada)
        continuar = set_coords.count(coordenada) > 1
        while continuar:
            print(
                '\nYa descubriste una casilla con la coordenada que ingresaste\n'
                'Porfavor, ingresa una coordenada que no hayas utilizado'
            )
            coordenada = coordenadas(tablero)
            if coordenada not in set_coords:
                set_coords.append(coordenada)
                set_coords = list(set(set_coords))
                continuar = False
        celda = int(coordenada[0]) # posicion eje x
        fila = int(coordenada[1]) # posicion eje y
        
        # en el caso que la celda 'contenga' una bestia, el jugador pierde
        if tablero_bestias[fila][celda] == 'N':
            set_coords = set()
            return "pierde", tablero 
        else: # en el caso que la celda no contenga a la bestia, el jugador sigue jugando ... 
            # modificamos las celdas del tablero que estan alrededor de la celda
            # que queremos descubrir (siempre y cuando, las posiciones de las celdas que 
            # rodean esten en el rango del tamaño del tablero) 
            largo = len(tablero[0])
            ancho = len(tablero)
            # verificamos la fila superior
            if fila - 1 >= 0:
                # verificamos la celda superior izquierda
                if celda - 1 >= 0:
                    tablero[fila - 1][celda - 1] = tablero_bestias[fila - 1][celda - 1]
                # verificamos la celda superior derecha
                if celda + 1 < largo:
                    tablero[fila - 1][celda + 1] = tablero_bestias[fila - 1][celda + 1]
                
                # despeja la celda superior central
                tablero[fila - 1][celda] = tablero_bestias[fila - 1][celda]

            # verifica la fila inferior
            if fila + 1 < ancho:
                # verificamos la celda inferior izquierda
                if celda - 1 >= 0:
                    tablero[fila + 1][celda - 1] = tablero_bestias[fila + 1][celda - 1]
                # verificamos la celda superior derecha
                if celda + 1 < largo:
                    tablero[fila + 1][celda + 1] = tablero_bestias[fila + 1][celda + 1]
                
                # despeja la celda superior central
                tablero[fila + 1][celda] = tablero_bestias[fila + 1][celda]
    
            # verifica la fila central de la celda actual
            # verificamos la celda central izquierda
            if celda - 1 >= 0:
                tablero[fila][celda - 1] = tablero_bestias[fila][celda - 1]
            # verificamos la celda central derecha
            if celda + 1 < largo:
                tablero[fila][celda + 1] = tablero_bestias[fila][celda + 1]
                
            # actualiza celda actual (celda central)
            tablero[fila][celda] = tablero_bestias[fila][celda]
            return "sigue", tablero

    






     

    




                









   


    
    







   









     

    




                









   


    
    







   

