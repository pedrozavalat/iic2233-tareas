import json 
import os

def cargar_data_json(llave):
    ruta = os.path.join("parametros.json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    valor = datos[llave]
    return valor