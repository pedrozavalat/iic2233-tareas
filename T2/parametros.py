import os
# Los intervalos están en milisegundos
INTERVALO_DISPARO = 2000 
INTERVALO_SOLES_GIRASOL = 20000
INTERVALO_TIEMPO_MORDIDA = 5000
INTERVALO_MOVIMIENTO_PLANTAS = 590
INTERVALO_APARICION_SOLES = 15000 
INTERVALO_ANUNCIO_VERDE = 500
INTERVALO_ANUCIO_ROJO = 500
INTERVALO_ANUNCIO_CRAZY_CRUZ = 2500
INTERVALO_ANUNCIO_PERDEDOR = 4000
INTERVALO_AVANZAR = 2500
# El daño y la vida tienen las mismas medidas
DANO_PROYECTIL = 5
DANO_MORDIDA = 5
VIDA_PLANTA = 100
VIDA_ZOMBIE = 80
# Número de zombies por carril
N_ZOMBIES = 7
# Porcentaje de ralentización
RALENTIZAR_ZOMBIE = 0.25
# Soles iniciales por ronda
SOLES_INICIALES = 250
# Número de soles generados por planta
CANTIDAD_SOLES = 2
# Número de soles agregados a la cuenta por recolección
SOLES_POR_RECOLECCION = 50
# Número de soles agregados a la cuenta por Cheatcode
SOLES_EXTRA = 25
# Ponderadores de escenarios
PONDERADOR_NOCTURNO = 0.8
PONDERADOR_DIURNO = 0.9
# La velocidad del zombie en milisegundos
VELOCIDAD_ZOMBIE = 5000
# Puntaje por eliminar zombie
PUNTAJE_ZOMBIE_DIURNO = 50
PUNTAJE_ZOMBIE_NOCTURNO = 100
# Costo por avanzar de ronda
COSTO_AVANZAR = 500
# Costo tiendas
COSTO_LANZAGUISANTE = 50
COSTO_LANZAGUISANTE_HIELO = 100
COSTO_GIRASOL = 50
COSTO_PAPA = 75
# Caracteres de nombre usuario
MIN_CARACTERES = 3
MAX_CARACTERES = 15

# Rutas 
RUTA_FONDO_MENU = os.path.join('sprites', 'Fondos', 'fondoMenu.png') 
RUTA_LOGO_JUEGO = os.path.join('sprites', 'Fondos', 'titulo.png') 
RUTA_IMAGEN_DIA = os.path.join('sprites', 'Fondos', 'jardinAbuela.png')
RUTA_IMAGEN_NOCHE =  os.path.join('sprites', 'Fondos', 'salidaNocturna.png')
RUTA_IMAGEN_CRAZYCRUZ = os.path.join('sprites', 'CrazyRuz', 'crazyCruz.png')
RUTA_VENTANA_PRINCIPAL = os.path.join('frontend', 'assets', 'ventana_principal.ui') 
RUTA_ESCENARIO_JUEGO = os.path.join('frontend', 'assets', 'escenario_diurno.ui')
RUTA_VENTANA_POST_RONDA = os.path.join('frontend', 'assets', 'ventana_postjuego.ui') 

RUTA_ICON_GIRASOL = os.path.join('sprites', 'Plantas', 'girasol_1.png') 
RUTA_ICON_GIRASOL_2 = os.path.join('sprites', 'Plantas', 'girasol_2.png') 
RUTA_ICON_LANZAGUI_NORMAL = os.path.join('sprites', 'Plantas', 'lanzaguisantes_1.png') 
RUTA_ICON_LANZAGUI_NORMAL_2 = os.path.join('sprites', 'Plantas', 'lanzaguisantes_2.png') 
RUTA_ICON_LANZAGUI_NORMAL_3 = os.path.join('sprites', 'Plantas', 'lanzaguisantes_3.png') 
RUTA_ICON_LANZAGUI_HIELO = os.path.join('sprites', 'Plantas', 'lanzaguisantesHielo_1.png') 
RUTA_ICON_LANZAGUI_HIELO_2 = os.path.join('sprites', 'Plantas', 'lanzaguisantesHielo_2.png') 
RUTA_ICON_LANZAGUI_HIELO_3 = os.path.join('sprites', 'Plantas', 'lanzaguisantesHielo_3.png') 
RUTA_ICON_PATATA = os.path.join('sprites', 'Plantas', 'papa_1.png') 
RUTA_ICON_PATATA_2 = os.path.join('sprites', 'Plantas', 'papa_2.png') 
RUTA_ICON_PATATA_3 = os.path.join('sprites', 'Plantas', 'papa_3.png') 

RUTA_ICON_PROYECTIL_VERDE = os.path.join('sprites', 'Elementos de juego', 'guisante_1.png') 
RUTA_ICON_PROYECTIL_VERDE_2 = os.path.join('sprites', 'Elementos de juego', 'guisante_2.png') 
RUTA_ICON_PROYECTIL_VERDE_3 = os.path.join('sprites', 'Elementos de juego', 'guisante_3.png') 
RUTA_ICON_PROYECTIL_AZUL = os.path.join('sprites', 'Elementos de juego', 'guisanteHielo_1.png') 
RUTA_ICON_PROYECTIL_AZUL_2 = os.path.join('sprites', 'Elementos de juego', 'guisanteHielo_2.png') 
RUTA_ICON_PROYECTIL_AZUL_3 = os.path.join('sprites', 'Elementos de juego', 'guisanteHielo_3.png') 

RUTA_ICON_SOL = os.path.join('sprites', 'Elementos de juego', 'sol.png') 

RUTA_ICON_ZOMBIE_RUNNER = os.path.join('sprites', 'Zombies',
                                                'Caminando', 'zombieHernanRunner_1.png') 
RUTA_ICON_ZOMBIE_RUNNER_2 = os.path.join('sprites', 'Zombies',
                                                'Caminando', 'zombieHernanRunner_2.png') 
RUTA_ICON_ZOMBIE_WALKER = os.path.join('sprites', 'Zombies',
                                                'Caminando', 'zombieNicoWalker_1.png') 
RUTA_ICON_ZOMBIE_WALKER_2 = os.path.join('sprites', 'Zombies',
                                                'Caminando', 'zombieNicoWalker_2.png') 

RUTA_ICON_ZOMBIE_RUNNER_EAT = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieHernanComiendo_1.png') 
RUTA_ICON_ZOMBIE_RUNNER_EAT_2 = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieHernanComiendo_2.png') 
RUTA_ICON_ZOMBIE_RUNNER_EAT_3 = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieHernanComiendo_3.png') 
RUTA_ICON_ZOMBIE_WALKER_EAT = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieNicoComiendo_1.png') 
RUTA_ICON_ZOMBIE_WALKER_EAT_2 = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieNicoComiendo_2.png') 
RUTA_ICON_ZOMBIE_WALKER_EAT_3 = os.path.join('sprites', 'Zombies',
                                                'Comiendo', 'zombieNicoComiendo_3.png') 
RUTA_MUSICA = os.path.join('musica2.wav')
