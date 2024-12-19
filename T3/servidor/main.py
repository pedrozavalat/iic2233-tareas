import sys
from servidor import Servidor
from funciones_utiles import cargar_data_json
"""
Modulo principal que instancia el servidor 
"""

if __name__ == "__main__":
    HOST = cargar_data_json("HOST")
    PORT = cargar_data_json("PORT")
    servidor = Servidor(HOST, PORT)
    try:
        while True:
            input("Presione [Ctr + C] para cerrar el servidor".center(124, "="))
        
    except KeyboardInterrupt:
        print("*" * 122)
        print()
        print(" Cerrando servidor  ".center(124, "="))
        print()
        print("*" * 124)
        servidor.socket_servidor.close()
        sys.exit()




    