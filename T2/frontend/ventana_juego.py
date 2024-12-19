from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import  QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import parametros as p


window_name, base_class = uic.loadUiType(p.RUTA_ESCENARIO_JUEGO)

class VentanaJuego(window_name, base_class):

    senal_iniciar_partida = pyqtSignal(dict) # Señal que inicia el juego. 
    senal_avanzar_ronda = pyqtSignal() # Señal que permite avanzar a otra ronda.
    senal_pausar_partida = pyqtSignal() # Señal que pausa todos los movimientos del juego.
    senal_alterar_partida = pyqtSignal() # Señal que permite pausar o renaudar el juego. 
    senal_salir = pyqtSignal() # Señal que cierra la ventana del juego y abre la de inicio. 
    senal_cargar_datos = pyqtSignal(str, str, int) # Señal que carga los datos del jugador. 
    senal_resetear_datos = pyqtSignal() # Señal que borra los datos del jugador. 
    senal_elegir_planta = pyqtSignal(str) # Señal que envia la eleccion de la planta de la tienda. 
    senal_elegir_casilla = pyqtSignal(QPushButton) # Señal que envia la posicion de la planta.
    senal_partida_ganada = pyqtSignal() # Señal que permite abrir la ventana Post-Ronda. Esta
                                        # permite al usuario seguir jugando. 
    senal_partida_perdida = pyqtSignal() # Señal que permite abrir la ventana Post-Ronda. Esta
                                        # no permite al usuario seguir jugando. 
    senal_click = pyqtSignal(int, int) # Señal que envia la posicion del click realizado. 
    senal_kil = pyqtSignal(str) # Señal que notifica si el usuario realizo la combinacion 
                                # de teclas CONSECUTIVAS K + I + L
    senal_sun = pyqtSignal(str) # Señal que notifica si el usuario realizo la combinacion 
                                # de teclas CONSECUTIVAS S + U + N
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle("Ventana de Juego")
        self.move(100, 100)
        self.boton_iniciar.clicked.connect(self.iniciar_partida) 
        self.boton_salir.clicked.connect(self.salir)
        self.boton_avanzar.clicked.connect(self.avanzar_ronda)
        self.boton_pausar.clicked.connect(self.pausar_partida)
        self.notificacion_roja.hide()
        self.notificacion_ronda.hide()
        self.notificacion_elegir_casilla.hide()
        self.fondo_jardin_abuela.hide()
        self.fondo_salida_nocturna.hide()
        self.label_anuncio = None
        self.imagen_crazy_cruz = None
        # Conectamos cada boton de la planta para asi posteriormente plantar
        # en la casilla que elegiremos posteriormente.   
        self.boton_girasoles.clicked.connect(self.elegir_planta)
        self.boton_lanzaguisantes_normal.clicked.connect(self.elegir_planta)
        self.boton_lanzaguisantes_hielo.clicked.connect(self.elegir_planta)
        self.boton_patata.clicked.connect(self.elegir_planta)
        # Antes de iniciar, conectamos cada boton de la casilla para elegir una planta. 
        self.posiciones = {
            0 : self.pos_0,
            1 : self.pos_1,
            2 : self.pos_2,
            3 : self.pos_3,
            4 : self.pos_4,
            5 : self.pos_5,
            6 : self.pos_6,
            7 : self.pos_7,
            8 : self.pos_8,
            9 : self.pos_9,
            10 : self.pos_10,
            11 : self.pos_11,
            12 : self.pos_12,
            13 : self.pos_13,
            14 : self.pos_14,
            15 : self.pos_15,
            16 : self.pos_16,
            17 : self.pos_17,
            18 : self.pos_18,
            19 : self.pos_19}
        for index in range(20):
            self.posiciones[index].clicked.connect(self.elegir_casilla)

        self.musica = QMediaPlayer()

    def iniciar_musica(self):
        self.musica.setMedia(QMediaContent(QUrl.fromLocalFile(p.RUTA_MUSICA)))
        self.musica.play()
        
    def renaudar_musica(self):
        self.musica.play()

    def pausar_musica(self):
        self.musica.pause()
        
    def abrir(self, usuario, escenario_elegido, ronda):
        self.show()
        self.iniciar_musica()
        if escenario_elegido == "Jardín de la abuela":
            self.fondo_jardin_abuela.show()
        elif escenario_elegido == "Salida Nocturna":
            self.fondo_salida_nocturna.show() 
        self.senal_cargar_datos.emit(usuario, escenario_elegido, ronda)
    
    def cerrar_ventana(self):
        self.pausar_musica()
        self.close()
        self.fondo_jardin_abuela.hide()
        self.fondo_salida_nocturna.hide() 
        
    def salir(self):
        self.pausar_musica()
        self.close()
        self.boton_iniciar.setEnabled(True)
        self.senal_resetear_datos.emit()
        self.senal_salir.emit()
        self.fondo_jardin_abuela.hide()
        self.fondo_salida_nocturna.hide() 
   
    def avanzar_ronda(self): 
        self.boton_iniciar.setEnabled(True)
        self.senal_avanzar_ronda.emit()
    
    def iniciar_partida(self):
        self.boton_iniciar.setEnabled(False)
        self.senal_iniciar_partida.emit(self.posiciones)

    def pausar_partida(self):
        self.senal_alterar_partida.emit()

    def actualizar_datos(self, datos):
        self.cant_soles_actuales.setText(datos["soles"])
        self.nivel.setText(datos["nivel"])
        self.puntaje.setText(datos["puntaje"])
        self.zombies_destruidos.setText(datos["zombies destruidos"])
        self.zombies_restantes.setText(datos["zombies restantes"])
   
    def elegir_planta(self):
        boton = self.sender().accessibleName()
        self.senal_elegir_planta.emit(boton)

    def elegir_casilla(self):
        boton_presionado = self.sender()
        self.senal_elegir_casilla.emit(boton_presionado)

    def cargar_casilla(self, casilla_elegida, planta_elegida):
        casilla_elegida.setIcon(QIcon(planta_elegida))
        
    def bloquear_tienda(self):
        self.boton_girasoles.setEnabled(False)
        self.boton_lanzaguisantes_normal.setEnabled(False)
        self.boton_lanzaguisantes_hielo.setEnabled(False)
        self.boton_patata.setEnabled(False)

    def desbloquear_tienda(self):
        self.boton_girasoles.setEnabled(True)
        self.boton_lanzaguisantes_normal.setEnabled(True)
        self.boton_lanzaguisantes_hielo.setEnabled(True)
        self.boton_patata.setEnabled(True)
    
    def recibir_notificacion(self, tipo_anuncio):
        if tipo_anuncio == "plantar":
            self.notificacion_roja.setText("NO TIENES MAS SOLES PARA PLANTAR")
            self.notificacion_roja.show()
        elif tipo_anuncio == "escoger planta":
            self.notificacion_roja.setText("DEBES ESCOGER UNA PLANTA ANTES DE PLANTAR")
            self.notificacion_roja.show()
        elif tipo_anuncio == "elegir casilla":
            self.notificacion_elegir_casilla.setText("Elige una casilla")
            self.notificacion_elegir_casilla.show()
        elif tipo_anuncio == "casilla ocupada":
            self.notificacion_elegir_casilla.setText("Casilla Ocupada")
            self.notificacion_elegir_casilla.show()
        elif tipo_anuncio == "crazy cruz":
            self.label_crazycruz.hide()
            self.senal_pausar_partida.emit()
            self.label_anuncio_crazy_cruz = QLabel('', self)
            self.label_anuncio_crazy_cruz.setGeometry(550, 190, 391, 171)
            self.label_anuncio_crazy_cruz.setText("¡Me HaS SalVad0 de LoS ZomBiezzzz!")
            self.label_anuncio_crazy_cruz.setStyleSheet("background-color: white;"
                                                        "color: forestgreen;"
                                                        "font-size: 20px;" 
                                                        "border-radius: 10px;" 
                                                        "font: italic;" 
                                                        "border: 3px solid forestgreen;")
            self.label_anuncio_crazy_cruz.setScaledContents(True)
            self.label_anuncio_crazy_cruz.setParent(self)
            self.label_anuncio_crazy_cruz.setVisible(True)
            self.imagen_crazy_cruz = QLabel('', self)
            self.imagen_crazy_cruz.setPixmap(QPixmap(p.RUTA_IMAGEN_CRAZYCRUZ))
            self.imagen_crazy_cruz.setGeometry(310, 250, 271, 231)
            self.imagen_crazy_cruz.setScaledContents(True)
            self.imagen_crazy_cruz.setParent(self)
            self.imagen_crazy_cruz.setVisible(True)
        elif tipo_anuncio == "pierde":
            self.label_perdedor = QLabel('The Zombies ate your brains !', self)
            self.label_perdedor.setGeometry(340, 150, 571, 221)
            self.label_perdedor.setAlignment(Qt.AlignCenter)
            self.label_perdedor.setStyleSheet("background-color: darkslategray;"
                                                "color: lime;"
                                                "font-size: 40px;"
                                                "border-radius: 10px;"
                                                "border: 3px solid forestgreen;" 
                                                "font: Bold;")
            self.label_perdedor.setParent(self)
            self.label_perdedor.setVisible(True)
        elif tipo_anuncio == "ronda":
            self.notificacion_ronda.setVisible(True)
            self.notificacion_ronda.show()

    def ocultar_notificacion(self, tipo_anuncio):
        if tipo_anuncio == "plantar":
            self.notificacion_roja.hide()
        elif tipo_anuncio == "escoger planta":
            self.notificacion_roja.hide()
        elif tipo_anuncio == "elegir casilla":
            self.notificacion_elegir_casilla.hide()
        elif tipo_anuncio == "casilla ocupada":
            self.notificacion_elegir_casilla.hide()
        elif tipo_anuncio == "ronda":
            self.notificacion_ronda.setVisible(False)
            self.notificacion_ronda.hide()
        elif tipo_anuncio == "crazy cruz":
            self.boton_iniciar.setEnabled(True)
            self.label_anuncio_crazy_cruz.setVisible(False)
            self.imagen_crazy_cruz.setVisible(False)
            self.senal_partida_ganada.emit()
        elif tipo_anuncio == "pierde":
            self.label_perdedor.setVisible(False)
            self.senal_partida_perdida.emit()
            
    def generar_movimiento_planta(self, posicion, movimiento):
        self.posiciones[int(posicion)].setIcon(QIcon(movimiento))

    def mostrar_proyectil(self, proyectil):
        proyectil.label.setParent(self)
        proyectil.label.setVisible(True)

    def mostrar_soles(self, sol):
        sol.label_sol.setParent(self)
        sol.label_sol.setVisible(True)

    def mostrar_zombie(self, zombie):
        zombie.label_zombie.setParent(self)
        zombie.label_zombie.setVisible(True)

    def ocultar_zombie(self, zombie):
        zombie.label_zombie.clear()

    def ocultar_plantas(self, posicion):
        self.posiciones[posicion].setIcon(QIcon())
        self.posiciones[posicion].setVisible(False)
    
    def ocultar_soles(self, soles):
        for sol in soles:
            sol.label_sol.setVisible(False)
            sol.label_sol.clear()

    def ocultar_sol_especifico(self, soles, posicion):
        for sol in soles:
            if (sol.pos_x, sol.pos_y) == posicion:
                sol.label_sol.setVisible(False)
                sol.label_sol.clear()
        
    def ocultar_proyectil_especifico(self, set_proyectiles, posicion):
        for proyectil in set_proyectiles:
            pos_x = proyectil.posicion.x()
            pos_y = proyectil.posicion.y()
            if (pos_x, pos_y) == posicion:
                proyectil.label.setVisible(False)
                proyectil.label.clear()

    def ocultar_proyectiles(self, set_proyectiles):
        for proyectil in set_proyectiles:
            proyectil.label.setVisible(False)
            proyectil.label.clear()

    def borrar_plantas(self):
        for casilla in self.posiciones.values():
            casilla.setIcon(QIcon())
            casilla.setVisible(True)
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.senal_click.emit(event.pos().x(), event.pos().y())
    
    def keyPressEvent(self, event):
        if event.text() == 'p':
            self.senal_alterar_partida.emit()
        
        if event.text() in ['k', 'i', 'l']:
            self.senal_kil.emit(event.text())
        if event.text() in ['s', 'u', 'n']:
            self.senal_sun.emit(event.text())

            




  
  
        
            
        

            



        
            


        


        

        

            
            
        
    



        