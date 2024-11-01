import sys
from PyQt6 import QtWidgets

from login import LoginWindow
from gestion_reservas import GestionReservas
from gestion_ciudades import GestionCiudades


class MainApp(QtWidgets.QMainWindow):
    def _init_(self):
        super()._init_()

        # Inicializar ventana de login
        self.login_window = LoginWindow()
        self.login_window.show()

        # Conectar la señal de login exitoso para abrir la ventana principal
        self.login_window.login_exitoso.connect(self.mostrar_ventana_principal)

    def mostrar_ventana_principal(self):
        self.login_window.close()
        self.show()

    def abrir_gestion_reservas(self):
        self.gestion_reservas = GestionReservas()
        self.gestion_reservas.show()

    def abrir_gestion_ciudades(self):
        self.gestion_ciudades = GestionCiudades()
        self.gestion_ciudades.show()


# Inicializar aplicación
app = QtWidgets.QApplication(sys.argv)
ventana = MainApp()
ventana.show()
sys.exit(app.exec())
