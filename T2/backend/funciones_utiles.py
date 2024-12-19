import parametros as p
from math import ceil
# Funcion que retorna el puntaje al eliminar un zombie segun el escenario elegido.
def otorgar_ptje(escenario_elegido): 
    if escenario_elegido == "Jardín de la abuela":
        return p.PUNTAJE_ZOMBIE_DIURNO
    elif escenario_elegido == "Salida Nocturna":
        return p.PUNTAJE_ZOMBIE_NOCTURNO
# Funcion que otorga el puntaje extra al eliminar todos los zombies. 
def otorgar_ptje_extra(puntaje_ronda, ponderador_dificultad):
    puntaje_extra = puntaje_ronda * ponderador_dificultad
    return ceil(puntaje_extra)

