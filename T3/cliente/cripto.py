from math import ceil, floor
def encriptar(msg : bytearray) -> bytearray:
    # Completar con el proceso de encriptación
    lista_piezas = []

    for inicio in range(3):
        pedazo = bytearray(msg[i] for i in range(inicio, len(msg), 3))
        lista_piezas.append(pedazo)
    bytes_a = lista_piezas[0] # Parte A
    bytes_b = lista_piezas[1] # Parte B
    bytes_c = lista_piezas[2] # Parte C
    # Primer byte de A
    primer_byte_a = bytes_a[0]
    # Byte(s) Central(es) de B 
    if len(bytes_b) % 2 != 0: # Si es impar
        byte_central_b = bytes_b[len(bytes_b) // 2]
    else: 
        byte_central_b = bytes_b[len(bytes_b) // 2] + (bytes_b[len(bytes_b) // 2] + 1)
    # Ultimo byte de C
    byte_final_c = bytes_c[-1]
    if (primer_byte_a + byte_central_b + byte_final_c) % 2 == 0: # Es par
        
        return bytes(b'\x00' + bytes_c + bytes_a + bytes_b)

    else:
        return bytes(b'\x01' + bytes_a + bytes_c + bytes_b)

def desencriptar(msg : bytearray) -> bytearray:
    # Completar con el proceso de desencriptación
    if msg == bytearray(b''):
        return b''
    primer_elemento = msg[:1][0]
    msg = msg[1:]
    largo_msg = len(msg)
    numero = floor(largo_msg / 3) if (largo_msg % 3 == 0 or largo_msg % 3 == 1) \
                                                        else ceil(largo_msg / 3) 
    # 1. Verificamos el orden en que vienen las partes A, B, y C. 
    #  n = 0 -> CAB
    if primer_elemento == 0:
        # 2. Luego, verificamos el resto que da al dividir por 3
        if largo_msg % 3 == 0 or largo_msg % 3 == 1: # OK
            # Caso 1: por ejemplo 9:3 = 3 / resto 0
            # cada parte tendra de largo
            # A = 3, B = 3, C = 3
            # Caso 2: por ejemplo 10:3 = 3.3 / resto = 1
            # por lo tanto cada parte del mensaje tendrá de largo
            # A = 4, B = 3, C = 3
            parte_a = msg[numero:-numero]
            parte_b = msg[-numero:]
            parte_c = msg[:numero]
        elif largo_msg % 3 == 2: # OK
            # Caso 3: Por ejemplo: 11:3 = 3.6 / resto = 2
            # por lo tanto cada parte del mensaje tendrá de largo
            # A = 4, B = 4, C = 3
            # Es decir, cortamos en base al numero aproximado superiormente
            parte_a = msg[-numero * 2:-numero]
            parte_b = msg[-numero:]
            parte_c = msg[:-numero * 2]
    #  n = 1 -> ACB  
    # Analogamente, realizamos el mismo procedimiento, pero para A, B, C 
    # en diferente orden           
    elif primer_elemento == 1:
        if largo_msg % 3 == 0: 
            # numero 10 o 9 : 3 ~ 3
            # A = 3, B = 3, C = 3
            parte_a = msg[:numero]
            parte_b = msg[-numero:]
            parte_c = msg[numero:-numero]
        elif largo_msg % 3 == 1: 
            # A = 4, B = 3, C = 3
            parte_a = msg[:-numero * 2]
            parte_b = msg[-numero:]
            parte_c = msg[-numero * 2:-numero]
        elif largo_msg  % 3 == 2: 
            # A = 4, B = 4, C = 3 
            parte_a = msg[:numero]
            parte_b = msg[-numero:]
            parte_c = msg[numero:-numero]
    msg_desencriptado = bytearray()
    try:
        for i in range(0, max(len(parte_a), len(parte_b), len(parte_c))):
            msg_desencriptado.append(parte_a[i])
            msg_desencriptado.append(parte_b[i])
            msg_desencriptado.append(parte_c[i])
    except IndexError:
        pass
    return msg_desencriptado



if __name__ == "__main__":
    # Testear encriptar
    
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')

    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
