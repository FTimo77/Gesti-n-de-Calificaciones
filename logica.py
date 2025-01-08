import sqlite3


class GestorCalificaciones:
    def __init__(self):
        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect('calificaciones.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla de alumnos si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                dni TEXT PRIMARY KEY,
                apellidos TEXT,
                nombre TEXT,
                nota REAL,
                calificacion TEXT
            )
        ''')
        self.conn.commit()

    def calcular_calificacion(self, nota):
        if nota < 5:
            return "SS"
        elif 5 <= nota < 7:
            return "AP"
        elif 7 <= nota < 9:
            return "NT"
        else:
            return "SB"

    def agregar_alumno(self, dni, apellidos, nombre, nota):
        # Verificar si el alumno ya existe
        self.cursor.execute('SELECT dni FROM alumnos WHERE dni = ?', (dni,))
        if self.cursor.fetchone():
            return "El DNI ya existe."

        # Calcular la calificación
        calificacion = self.calcular_calificacion(nota)

        # Insertar el nuevo alumno en la base de datos
        self.cursor.execute('''
            INSERT INTO alumnos (dni, apellidos, nombre, nota, calificacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (dni, apellidos, nombre, nota, calificacion))
        self.conn.commit()
        return "Alumno agregado correctamente."

    def eliminar_alumno(self, dni):
        # Eliminar el alumno de la base de datos
        self.cursor.execute('DELETE FROM alumnos WHERE dni = ?', (dni,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return "Alumno eliminado correctamente."
        return "El DNI no existe."

    def consultar_alumno(self, dni):
        # Consultar un alumno por DNI
        self.cursor.execute('SELECT * FROM alumnos WHERE dni = ?', (dni,))
        alumno = self.cursor.fetchone()

        if alumno:
            return {
                "dni": alumno[0],
                "apellidos": alumno[1],
                "nombre": alumno[2],
                "nota": alumno[3],
                "calificacion": alumno[4]
            }
        return "El DNI no existe."

    def modificar_nota(self, dni, nueva_nota):
        # Modificar la nota del alumno
        calificacion = self.calcular_calificacion(nueva_nota)
        self.cursor.execute('''
            UPDATE alumnos
            SET nota = ?, calificacion = ?
            WHERE dni = ?
        ''', (nueva_nota, calificacion, dni))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return "Nota modificada correctamente."
        return "El DNI no existe."

    def obtener_alumnos(self, criterio=None):
        # Obtener los alumnos según el criterio
        if criterio == "suspensos":
            self.cursor.execute('SELECT * FROM alumnos WHERE nota < 5')
        elif criterio == "aprobados":
            self.cursor.execute('SELECT * FROM alumnos WHERE nota >= 5')
        elif criterio == "mh":
            self.cursor.execute('SELECT * FROM alumnos WHERE nota = 10')
        else:
            self.cursor.execute('SELECT * FROM alumnos')

        alumnos = self.cursor.fetchall()

        # Devolver los alumnos en un formato adecuado (lista de diccionarios)
        alumnos_list = []
        for alumno in alumnos:
            alumnos_list.append({
                "dni": alumno[0],
                "apellidos": alumno[1],
                "nombre": alumno[2],
                "nota": alumno[3],
                "calificacion": alumno[4]
            })

        return alumnos_list

    def cerrar_conexion(self):
        # Cerrar la conexión con la base de datos
        self.conn.close()
