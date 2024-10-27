from PyQt5 import QtWidgets, uic
from conexion_db import ejecutar_consulta, ejecutar_comando

class GestionReservas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gestion_reservas.ui', self)

        # Conectar botones a las funciones
        self.boton_agregar_reserva.clicked.connect(self.agregar_reserva)
        self.boton_editar_reserva.clicked.connect(self.editar_reserva)
        self.boton_eliminar_reserva.clicked.connect(self.eliminar_reserva)

        self.ver_reservas()

    def ver_reservas(self):
        consulta = "SELECT id, vuelo_id, pasajero_id, fecha_creacion, fecha_confirmacion_pago, estado, asiento_id FROM reservas"
        reservas = ejecutar_consulta(consulta)
        self.tabla_reservas.setRowCount(len(reservas))
        for row_num, reserva in enumerate(reservas):
            for col_num, data in enumerate(reserva):
                self.tabla_reservas.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

    def agregar_reserva(self):
        pasajero_id, ok = QtWidgets.QInputDialog.getInt(self, "Agregar Reserva", "ID del Pasajero:")
        if not ok or not pasajero_id:
            return
        vuelo_id, estado, asiento_id = 1, "en espera", None  # Valores de ejemplo
        comando = "INSERT INTO reservas (vuelo_id, pasajero_id, fecha_creacion, estado, asiento_id) VALUES (?, ?, datetime('now'), ?, ?)"
        ejecutar_comando(comando, (vuelo_id, pasajero_id, estado, asiento_id))
        self.ver_reservas()

    def editar_reserva(self):
        row = self.tabla_reservas.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona una reserva para editar")
            return
        reserva_id = self.tabla_reservas.item(row, 0).text()
        nuevo_estado, ok = QtWidgets.QInputDialog.getText(self, "Editar Reserva", "Nuevo estado (pagada/en espera):", text=self.tabla_reservas.item(row, 5).text())
        if not ok or nuevo_estado not in ["pagada", "en espera"]:
            return
        comando = "UPDATE reservas SET estado = ? WHERE id = ?"
        ejecutar_comando(comando, (nuevo_estado, reserva_id))
        self.ver_reservas()

    def eliminar_reserva(self):
        row = self.tabla_reservas.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona una reserva para eliminar")
            return
        reserva_id = self.tabla_reservas.item(row, 0).text()
        respuesta = QtWidgets.QMessageBox.question(self, "Eliminar Reserva", "¿Seguro que deseas eliminar esta reserva?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if respuesta == QtWidgets.QMessageBox.No:
            return
        comando = "DELETE FROM reservas WHERE id = ?"
        ejecutar_comando(comando, (reserva_id,))
        self.ver_reservas()
