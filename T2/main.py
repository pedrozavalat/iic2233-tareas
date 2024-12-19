import sys
from PyQt5.QtWidgets import QApplication

"""Archivo que realizara las conexiones principales entre frontend y backend"""
""",y ejecutará e inicializará el juego"""

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_post_ronda import VentanaPostRonda
from backend.logica_ranking import LogicaRanking
from backend.logica_principal import LogicaPrincipal
from backend.logica_inicio import LogicaInicio
from backend.logica_juego import LogicaJuego
from backend.logica_post_ronda import LogicaPostRonda
from backend.logica_botones import LogicaBotones
if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])

    # Instanciamos las ventanas. 
    # ----- Frontend ------
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_principal = VentanaPrincipal()
    ventana_post_ronda = VentanaPostRonda()
    ventana_juego = VentanaJuego()
    # ------ Backend ------
    logica_principal = LogicaPrincipal()
    logica_ranking = LogicaRanking()
    logica_inicio = LogicaInicio()
    logica_juego = LogicaJuego()
    logica_post_ronda = LogicaPostRonda()
    logica_botones = LogicaBotones()
    
    

    # Realizamos conexiones entre frontends y backends respectivos. 
    # ------ Conexion Ventana inicio (frontend) con backend respectivo (logica inicio) --------
    ventana_inicio.senal_abrir_ranking.connect(ventana_ranking.abrir)
    ventana_inicio.senal_enviar_login.connect(logica_inicio.revisar_login)
    logica_inicio.senal_enviar_validacion.connect(ventana_inicio.recibir_validacion)
    logica_inicio.senal_abrir_ventana_principal.connect(ventana_principal.abrir)
    

    # ------ Conexion Ventana ranking (frontend) con backend respectivo (logica ranking) ------
    ventana_ranking.senal_volver_ventana_inicio.connect(ventana_inicio.abrir)
    ventana_ranking.senal_pedir_ranking.connect(logica_ranking.generar_ranking)
    logica_ranking.senal_enviar_ranking.connect(ventana_ranking.mostrar_ranking)
    

    # ------ Conexion Ventana principal (frontend) con backend respectivo (logica principal) --
    ventana_principal.senal_escenario_seleccionado.connect(logica_principal.verificar_seleccion)
    ventana_principal.senal_enviar_verificacion_boton.connect(
                                                        logica_principal.recibibir_verificacion) 
    logica_principal.senal_enviar_notificacion.connect(ventana_principal.recibir_notificacion)
    logica_principal.senal_abrir_juego.connect(ventana_juego.abrir)


    # -- Conexion entre Ventana juego (frontend) con backend respectivo (logica juego) -------- 
    ventana_juego.senal_salir.connect(ventana_inicio.abrir)
    ventana_juego.senal_avanzar_ronda.connect(logica_juego.avanzar_ronda)
    ventana_juego.senal_iniciar_partida.connect(logica_juego.comenzar_juego)
    ventana_juego.senal_cargar_datos.connect(logica_juego.cargar_datos)
    ventana_juego.senal_elegir_planta.connect(logica_juego.recibir_opcion_plantar)
    ventana_juego.senal_elegir_casilla.connect(logica_juego.cargar_casilla_elegida)
    ventana_juego.senal_pausar_partida.connect(logica_juego.pausar_juego)
    ventana_juego.senal_alterar_partida.connect(logica_botones.boton_pausar)
    ventana_juego.senal_click.connect(logica_juego.recoger_soles)
    ventana_juego.senal_resetear_datos.connect(logica_juego.resetear_datos)
    ventana_juego.senal_partida_ganada.connect(logica_juego.partida_ganada)
    ventana_juego.senal_partida_perdida.connect(logica_juego.partida_perdida)
    ventana_juego.senal_kil.connect(logica_botones.boton_kil)
    ventana_juego.senal_sun.connect(logica_botones.boton_sun)
    
    logica_botones.senal_soles_extra.connect(logica_juego.soles_extra)
    logica_botones.senal_matar_zombies.connect(logica_juego.matar_zombies)
    logica_botones.senal_pausar_juego.connect(logica_juego.pausar_juego)
    logica_botones.senal_renaudar_juego.connect(logica_juego.reaunudar_juego)
    logica_botones.senal_bloquear_tienda.connect(ventana_juego.bloquear_tienda)
    logica_botones.senal_desbloquear_tienda.connect(ventana_juego.desbloquear_tienda)
    logica_botones.senal_renaudar_musica.connect(ventana_juego.renaudar_musica)
    logica_botones.senal_pausar_musica.connect(ventana_juego.pausar_musica)
    
    logica_juego.senal_actualizar_datos.connect(ventana_juego.actualizar_datos)
    logica_juego.notificacion.senal_enviar_notificacion.connect(
                                                        ventana_juego.recibir_notificacion)
    logica_juego.notificacion.senal_ocultar_notificacion.connect(
                                                        ventana_juego.ocultar_notificacion)
    logica_juego.senal_cargar_casilla.connect(ventana_juego.cargar_casilla)
    logica_juego.senal_actualizar_casillas.connect(ventana_juego.ocultar_plantas)
    logica_juego.senal_actualizar_proyectil.connect(ventana_juego.ocultar_proyectil_especifico)
    logica_juego.senal_ocultar_proyectiles.connect(ventana_juego.ocultar_proyectiles)
    logica_juego.senal_borrar_plantas.connect(ventana_juego.borrar_plantas)
    logica_juego.senal_ocultar_soles.connect(ventana_juego.ocultar_soles)
    logica_juego.senal_ocultar_sol_especifico.connect(ventana_juego.ocultar_sol_especifico)
    logica_juego.senal_mover_planta.connect(ventana_juego.generar_movimiento_planta)
    logica_juego.senal_lanzar_proyectil.connect(ventana_juego.mostrar_proyectil)
    logica_juego.senal_crear_soles.connect(ventana_juego.mostrar_soles)
    logica_juego.senal_mostrar_zombie.connect(ventana_juego.mostrar_zombie)
    logica_juego.senal_ocultar_zombie.connect(ventana_juego.ocultar_zombie)
    logica_juego.senal_avanzar_ronda.connect(ventana_post_ronda.abrir)
    logica_juego.senal_terminar_ronda.connect(logica_post_ronda.recibir_datos)
    logica_juego.senal_cerrar_ventana.connect(ventana_juego.cerrar_ventana)
    
    
    # -- Conexion entre Ventana Post-Juego (frontend) con backend respectivo (logica juego) ---
    ventana_post_ronda.senal_salir.connect(ventana_inicio.abrir) 
    ventana_post_ronda.senal_siguiente_ronda.connect(logica_post_ronda.cargar_siguiente_ronda)
    logica_post_ronda.senal_enviar_datos.connect(ventana_post_ronda.recibir_datos)
    logica_post_ronda.senal_mostrar_anuncio_ganador.connect(
                                                ventana_post_ronda.mostrar_notificacion_verde)
    logica_post_ronda.senal_mostrar_anuncio_perdedor.connect(
                                                ventana_post_ronda.mostrar_notificacion_roja)
    logica_post_ronda.senal_cargar_ronda.connect(ventana_juego.abrir)

    # ---- INICIO DEL JUEGO -------- #
    ventana_inicio.mostrar_elementos()
    ventana_inicio.abrir()
    
    app.exec()

    

    