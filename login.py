from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from conexion_db import ejecutar_consulta

class LoginWindow(QtWidgets.QWidget):
    login_exitoso = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)  # Cargar la interfaz de login

        # Conectar botón de inicio de sesión
        self.boton_aceptar.clicked.connect(self.iniciar_sesion)

    def iniciar_sesion(self):
        usuario = self.usuario_input.text()
        contraseña = self.contraseña_input.text()
        
        consulta = "SELECT * FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?"
        resultado = ejecutar_consulta(consulta, (usuario, contraseña))

        if resultado:
            QtWidgets.QMessageBox.information(self, "Login", "Acceso exitoso")
            self.login_exitoso.emit()  # Emitir señal de login exitoso
        else:
            QtWidgets.QMessageBox.warning(self, "Login", "Usuario o contraseña incorrectos")
