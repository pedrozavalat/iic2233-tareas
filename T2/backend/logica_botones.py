from PyQt5.QtCore import QObject, pyqtSignal 


class LogicaBotones(QObject):
    
    senal_pausar_juego = pyqtSignal()
    senal_renaudar_juego = pyqtSignal()
    senal_renaudar_musica = pyqtSignal()
    senal_desbloquear_tienda = pyqtSignal()
    senal_bloquear_tienda = pyqtSignal()
    senal_matar_zombies = pyqtSignal()
    senal_soles_extra = pyqtSignal() 
    senal_pausar_musica = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.contador = 0
        self.contador_kil = 0
        self.secuencia_kil = ''
        self.contador_sun = 0
        self.secuencia_sun = ''
    
    def boton_pausar(self):
        self.contador += 1
        # si el contador es impar, entonces 
        # se debe pausar el juego
        if self.contador % 2 == 1:
            self.senal_pausar_juego.emit()
            self.senal_pausar_musica.emit()
            self.senal_bloquear_tienda.emit()
        # en el caso que el contador es par
        else:
            self.senal_renaudar_juego.emit()
            self.senal_renaudar_musica.emit()
            self.senal_desbloquear_tienda.emit()
    
    def boton_kil(self, boton_presionado):
        self.contador_kil += 1
        self.secuencia_kil += boton_presionado
        if self.secuencia_kil == 'kil':
            self.senal_matar_zombies.emit()
        if self.contador_kil == 3:
            # Para que verificar teclas que apretamos, le hacemos print
            # a la secuencia realizada. 
            print(f'Secuencia de botones realizados: {self.secuencia_kil}')
            self.secuencia_kil = ''
            self.contador_kil = 0
    
    def boton_sun(self, boton_presionado):
        self.contador_sun += 1
        self.secuencia_sun += boton_presionado
        if self.secuencia_sun == 'sun':
            self.senal_soles_extra.emit()
        if self.contador_sun == 3:
            print(f'Secuencia de botones realizados: {self.secuencia_sun}')
            self.secuencia_sun = ''
            self.contador_sun = 0
            
        