
from PyQt5.QtCore import QObject, pyqtSignal 
class LogicaPrincipal(QObject):

    senal_enviar_notificacion = pyqtSignal(bool)
    senal_abrir_escenario_diurno = pyqtSignal(str)
    senal_abrir_escenario_nocturno = pyqtSignal(str)
    senal_abrir_juego = pyqtSignal(str, str, int)
    

    def __init__(self):
        super().__init__()
        self.escenario_elegido = "Aun no hay seleccion"
    # Guardamos la seleccion del escenario elegido.
    def verificar_seleccion(self, boton):
        self.escenario_elegido = boton
    # Verificamos que se haya seleccionado algún escenario.
    def recibibir_verificacion(self, usuario):
        escenario_elegido = True
        if self.escenario_elegido == "Aun no hay seleccion":
            escenario_elegido = False
        else:
            ronda = 0
            # Abrimos el juego junto con:
            # - Nombre de usuario del jugador
            # - El escenario elegido (Jardin de la abuela o Salida Nocturna)
            # - El numero de la ronda (En este caso, la ronda inicial)
            self.senal_abrir_juego.emit(usuario, self.escenario_elegido, ronda)         
        # Enviamos la señal de la eleccion del escenario a la ventanta principal.
        # En el caso que no se haya elegido algun escenario, se le notificará al jugador.
        self.senal_enviar_notificacion.emit(escenario_elegido) 
            
            

    

        
    
        


        
