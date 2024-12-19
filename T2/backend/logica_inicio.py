from PyQt5.QtCore import QObject, pyqtSignal
import parametros as p 

class LogicaInicio(QObject):
    senal_abrir_ventana_principal = pyqtSignal(str)
    senal_enviar_validacion = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
    # recibimos el usuario por parte del backend para validarlo
    def revisar_login(self, usuario):
        valido = True
        notificacion = ""
        if  usuario.isalpha() or usuario.isdigit():
            valido = False
            notificacion = "Usuario inválido: Debe contener numeros y letras"
        if len(usuario) not in list(range(p.MIN_CARACTERES, p.MAX_CARACTERES + 1)):
            valido = False
            notificacion = "El nombre de usuario debe contener entre "+\
                           f"{p.MIN_CARACTERES} a {p.MAX_CARACTERES} carácteres"
        if usuario == "":
            valido = False
            notificacion = "Debes ingresar un nombre de usuario"
        if valido:
            # Dado que es valido, abrimos la ventana principal.
            # (En el caso que el nombre de usuario se encuentre el archivo 
            # puntajes.txt, restablecemos el puntaje a 0.) 
            with open("puntajes.txt", 'r', encoding = 'utf-8') as puntajes:
                puntajes = puntajes.readlines()
                puntajes = [linea.strip("\n").split(",") for linea in puntajes]
                crear_puntajes = {puntaje[0] : puntaje[1] for puntaje in puntajes} 
                if usuario in crear_puntajes.keys():
                    crear_puntajes[usuario] = "0"
            archivo_actualizado = ""
            for jugador, puntaje in crear_puntajes.items():
                archivo_actualizado += f'{jugador},{puntaje}\n'
            with open("puntajes.txt", 'w', encoding = 'utf-8') as puntajes:
                puntajes.write(archivo_actualizado)
            self.senal_abrir_ventana_principal.emit(usuario) 
        # Enviamos la validacion del usuario al frontend - ventana inicio.
        self.senal_enviar_validacion.emit(valido, notificacion)
    

    