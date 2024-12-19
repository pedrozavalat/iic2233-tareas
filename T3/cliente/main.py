from funciones_utiles import cargar_data_json
from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from backend.logica_interfaz import Interfaz
import sys

if __name__ == "__main__":
    HOST = cargar_data_json("HOST") 
    PORT = cargar_data_json("PORT")
    try: 
        # ***** Iniciamos la aplicación ******
        app = QApplication(sys.argv)

        cliente = Cliente(HOST, PORT)
        sys.exit(app.exec_())

    except ConnectionError:
        print("Error de conexion :(")
    
