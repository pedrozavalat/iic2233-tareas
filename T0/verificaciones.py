
import string

"""
Funcion que verifica si las opciones elegidas por el usuario pertenecen
al rango establecido segun el tipo de menu. 
"""
def opcion_usuario(numeros):
    opciones = [str(item) for item in range(0,numeros + 1)]
    opciones_a = ",".join(opciones[0:-1]).replace("", " ")
    opciones_b = str(opciones[-1])
    frase = opciones_a+ ", o "+ opciones_b 
    opcion = input(f"Indique su opcion ({frase} ):")
    while opcion not in opciones:
        print("\nOpción no válida :(")
        print("Ingrese la opción nuevamente de la manera correcta porfavor.\n")
        opcion = input("Ingresa la coordenada >>>     ")
        print()
    return int(opcion)    
    
"""
Funcion que verifica si las coordenadas elegidas por el usuario, para descubrir
una nueva celda, se encuentran dentro de las posiciones posibles que presenta 
el tablero.
"""
def coordenadas(tablero):
    # el usuario comenta la coordenada de la celda a descubrir
    respuesta = input(
        "\nDebes ingresar la posicion de la casilla dentro del rango\n"
        "establecido por el tablero. Como por ejemplo: a0, b0, c1, etc..\n"
        ">>>    ")
    # letra -> coordenada en eje x
    # numero -> coordenada en eje y
    letra, numero = respuesta[0], respuesta[1:]
    # Definimos las condiciones. En este caso, la letra recibida debe
    # pertenecer al rango máximo de letras que presenta el tablero (es decir,
    # desde A, hasta O). Y también, si el numero (coordenada y), esta 
    # segun el rango establecido por el ancho del tablero.

    # set de numeros de 0 hasta n (siendo el "ancho - 1" del tablero)
    numeros = {str(numero) for numero in range(0,len(tablero))}
    # string de letras desde a hasta o.
    letras = string.ascii_lowercase[0:15]
    # diccionario de letras desde a hasta o, en donde cada letra se le asigna
    # como valor su posicion en el string de letras
    diccionario = {caracter : int(letras.index(caracter)) for caracter in letras}

    cond_1 = letra.isalpha() and numero.isdigit() # condicion 1
    cond_2 = numero in numeros and letra in letras # condicion 2
    
    # mientras no se cumplan las condiciones, el usuario debe elegir una nueva coordenada
    while (not cond_1) or (not cond_2):
        print("Coordenada no válida :(")
        print()
        respuesta = input(
            "Ingrese la coordenada de la forma correcta\n"
            ">>>    ")
        letra, numero = respuesta[0], respuesta[1:]
        cond_1 = letra.isalpha() and numero.isdigit()
        cond_2 = numero in numeros and letra in letras
    return (diccionario[letra], numero)
    
"""
Funcion que verifica si las medidas del ancho y el largo del tablero, solicitado
por el usuario al crear una nueva partida, cumplen que pertenezcan al rango numero
entre 3 y 15, considerando ambos números. 
"""
def medidas():
    x = input("=> Largo:".center(50, " ")) # Largo del tablero 
    y = input("=> Ancho:".center(50, " ")) # Ancho del tablero
    rango_establecido = {str(numero) for numero in range(3,16)}
    condicion_1 = x not in rango_establecido
    condicion_2 = y not in rango_establecido

    while (condicion_1 or condicion_2):
        print("Error: Los valores no están entre [3,15]")
        print("Ingrese los valores correctamente ...")
        x = input("=> Largo:".center(50, " "))
        y = input("=> Ancho:".center(50, " "))
        condicion_1 = x not in rango_establecido #verificamos si x pertenece a [3,5]
        condicion_2 = y not in rango_establecido #verificamos si y pertenece a [3,5]
    return int(x), int(y)




