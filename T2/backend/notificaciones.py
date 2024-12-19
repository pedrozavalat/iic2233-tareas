from PyQt5.QtCore import QObject, QTimer, pyqtSignal 


"""La clase notificaciones permite mostrar un label en la ventana del juego
Notificando al usario sobre un suceso en el juego. Por ejemplo: Al ganar, se envia
una notificacion, mostrando un label de Crazy Ruz. Esta clase envia una senal que muestra 
la notificacion en el frontend, y luego se activa un Timer para ocultarla posteriormente.
"""
class Notificaciones(QObject):

    senal_enviar_notificacion = pyqtSignal(str)
    senal_ocultar_notificacion = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tipo_anuncio = ""
    
    def enviar_notificacion(self, tipo_anuncio, tiempo):
        self.tipo_anuncio = tipo_anuncio
        self.senal_enviar_notificacion.emit(tipo_anuncio)

        self.timer_ocultar_notificacion = QTimer()
        self.timer_ocultar_notificacion.setInterval(tiempo)
        self.timer_ocultar_notificacion.timeout.connect(self.ocultar_notificacion)
        self.timer_ocultar_notificacion.setSingleShot(True)
        self.timer_ocultar_notificacion.start()

    def ocultar_notificacion(self):
        self.senal_ocultar_notificacion.emit(self.tipo_anuncio)