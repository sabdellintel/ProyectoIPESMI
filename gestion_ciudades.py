from PyQt5 import QtWidgets, uic
from conexion_db import ejecutar_consulta, ejecutar_comando

class GestionCiudades(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gestion_ciudades.ui', self)

        self.boton_agregar_ciudad.clicked.connect(self.agregar_ciudad)
        self.boton_editar_ciudad.clicked.connect(self.editar_ciudad)
        self.boton_eliminar_ciudad.clicked.connect(self.eliminar_ciudad)
        self.boton_activar_ciudad.clicked.connect(self.activar_ciudad)

        self.ver_ciudades()
        self.actualizar_estadisticas()

    def ver_ciudades(self):
        consulta = "SELECT id, nombre, pais, aeropuerto, codigo_ciudad, codigo_pais, activo FROM ciudades"
        ciudades = ejecutar_consulta(consulta)
        self.tabla_ciudades.setRowCount(len(ciudades))
        for row_num, ciudad in enumerate(ciudades):
            for col_num, data in enumerate(ciudad):
                self.tabla_ciudades.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))

    def agregar_ciudad(self):
        nombre, ok = QtWidgets.QInputDialog.getText(self, "Agregar Ciudad", "Nombre de la ciudad:")
        if not ok or not nombre:
            return
        pais, aeropuerto, codigo_ciudad, codigo_pais, activo = "PaisX", "AeropuertoY", "ABC", "XY", 1
        comando = "INSERT INTO ciudades (nombre, pais, aeropuerto, codigo_ciudad, codigo_pais, activo) VALUES (?, ?, ?, ?, ?, ?)"
        ejecutar_comando(comando, (nombre, pais, aeropuerto, codigo_ciudad, codigo_pais, activo))
        self.ver_ciudades()
        self.actualizar_estadisticas()

    def editar_ciudad(self):
        row = self.tabla_ciudades.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona una ciudad para editar")
            return
        ciudad_id = self.tabla_ciudades.item(row, 0).text()
        nuevo_nombre, ok = QtWidgets.QInputDialog.getText(self, "Editar Ciudad", "Nuevo nombre de la ciudad:", text=self.tabla_ciudades.item(row, 1).text())
        if not ok or not nuevo_nombre:
            return
        comando = "UPDATE ciudades SET nombre = ? WHERE id = ?"
        ejecutar_comando(comando, (nuevo_nombre, ciudad_id))
        self.ver_ciudades()

    def eliminar_ciudad(self):
        row = self.tabla_ciudades.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona una ciudad para eliminar")
            return
        ciudad_id = self.tabla_ciudades.item(row, 0).text()
        respuesta = QtWidgets.QMessageBox.question(self, "Eliminar Ciudad", "¿Seguro que deseas eliminar esta ciudad?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if respuesta == QtWidgets.QMessageBox.No:
            return
        comando = "DELETE FROM ciudades WHERE id = ?"
        ejecutar_comando(comando, (ciudad_id,))
        self.ver_ciudades()
        self.actualizar_estadisticas()
