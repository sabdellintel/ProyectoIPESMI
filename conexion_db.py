# conexion_db.py
import sqlite3

def conectar():
    """
    Establece la conexión a la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect("db.db")  
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def ejecutar_consulta(consulta, parametros=()):
    """
    Ejecuta una consulta SELECT en la base de datos.
    
    :param consulta: La consulta SQL a ejecutar.
    :param parametros: Una tupla de parámetros para la consulta.
    :return: Una lista de resultados de la consulta.
    """
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return []
        finally:
            conn.close()
    else:
        return []

def ejecutar_comando(comando, parametros=()):
    """
    Ejecuta un comando de modificación en la base de datos (INSERT, UPDATE, DELETE).
    
    :param comando: El comando SQL a ejecutar.
    :param parametros: Una tupla de parámetros para el comando.
    :return: True si el comando se ejecuta correctamente, False si ocurre un error.
    """
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(comando, parametros)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar comando: {e}")
            return False
        finally:
            conn.close()
    else:
        return False
