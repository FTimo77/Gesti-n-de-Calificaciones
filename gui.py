import customtkinter
from logica import GestorCalificaciones

class GUI:
    def __init__(self):
        self.gestor = GestorCalificaciones()

        # Configuración de la ventana principal
        self.ventana = customtkinter.CTk()
        self.ventana.title("Gestor de Calificaciones")
        self.ventana.geometry("1000x700")

        self.crear_titulo()
        self.crear_botones()

        # Mantén el área de resultados como está
        self.resultado_texto = customtkinter.CTkTextbox(self.ventana, height=300, width=760)
        self.resultado_texto.pack(pady=10)

        self.ventana.mainloop()

    #def limpiar_ventana(self):
        """Función para destruir los widgets de la ventana actual, excluyendo el frame de resultados"""
        for widget in self.ventana.winfo_children():
            # No destruir el frame de resultados
            if widget != self.resultado_texto:
                widget.destroy()

        # Vuelve a cargar el título y los botones principales
        self.titulo_frame = customtkinter.CTkFrame(self.ventana, corner_radius=20, fg_color="slate blue")
        self.titulo_frame.pack(pady=10, padx=10, fill="x")

        self.titulo_label = customtkinter.CTkLabel(self.titulo_frame, text="GESTOR DE CALIFICACIONES",
                                                   font=("Arial", 24), text_color="white")
        self.titulo_label.pack(pady=10)

        # Frame para los botones en fila
        self.botones_frame = customtkinter.CTkFrame(self.ventana)
        self.botones_frame.pack(pady=10)

        # Botones en fila (usando grid)
        self.boton_agregar = customtkinter.CTkButton(self.botones_frame, text="Agregar Alumno",
                                                     command=self.mostrar_formulario_agregar,
                                                     fg_color="darkorchid4")
        self.boton_agregar.grid(row=0, column=0, padx=10)

        self.boton_mostrar = customtkinter.CTkButton(self.botones_frame, text="Mostrar Alumnos",
                                                     command=self.mostrar_alumnos,
                                                     fg_color="darkorchid4")
        self.boton_mostrar.grid(row=0, column=1, padx=10)

        self.boton_eliminar = customtkinter.CTkButton(self.botones_frame, text="Eliminar Alumno",
                                                      command=self.mostrar_formulario_eliminar,
                                                      fg_color="darkorchid4")
        self.boton_eliminar.grid(row=0, column=2, padx=10)

        self.boton_modificar_nota = customtkinter.CTkButton(self.botones_frame, text="Modificar Nota",
                                                            command=self.mostrar_formulario_modificar_nota,
                                                            fg_color="darkorchid4")
        self.boton_modificar_nota.grid(row=0, column=3, padx=10)

    def crear_titulo(self):
        """Crea el frame y el título principal"""
        self.titulo_frame = customtkinter.CTkFrame(self.ventana, corner_radius=20, fg_color="slate blue")
        self.titulo_frame.pack(pady=10, padx=10, fill="x")

        self.titulo_label = customtkinter.CTkLabel(self.titulo_frame, text="GESTOR DE CALIFICACIONES",
                                                   font=("Arial", 24), text_color="white")
        self.titulo_label.pack(pady=10)

    def crear_botones(self):
        """Crea el frame y los botones principales"""
        self.botones_frame = customtkinter.CTkFrame(self.ventana)
        self.botones_frame.pack(pady=10)

        # Botones en fila (usando grid)
        botones = [
            ("Agregar Alumno", self.mostrar_formulario_agregar, "darkorchid4"),
            ("Mostrar Alumnos", self.mostrar_alumnos, "darkorchid4"),
            ("Eliminar Alumno", self.mostrar_formulario_eliminar, "darkorchid4"),
            ("Modificar Nota", self.mostrar_formulario_modificar_nota, "darkorchid4"),
            ("Mostrar Aprobados", lambda: self.mostrar_alumnos("aprobados"), "darkgreen"),
            ("Mostrar Suspensos", lambda: self.mostrar_alumnos("suspensos"), "darkred"),
        ]

        for i, (text, command, color) in enumerate(botones):
            boton = customtkinter.CTkButton(self.botones_frame, text=text, command=command, fg_color=color)
            boton.grid(row=0, column=i, padx=10)

    def limpiar_ventana(self):
        """Limpia la ventana excepto el área de resultados y recarga el título y botones"""
        for widget in self.ventana.winfo_children():
            if widget != self.resultado_texto:
                widget.destroy()

        # Vuelve a cargar el título y los botones principales
        self.crear_titulo()
        self.crear_botones()

    def mostrar_formulario_modificar_nota(self):
        self.limpiar_ventana()  # Limpiar la ventana antes de mostrar el nuevo formulario

        # Crear un nuevo frame para el formulario
        self.formulario_frame = customtkinter.CTkFrame(self.ventana, corner_radius=20)
        self.formulario_frame.pack(pady=10, padx=10, fill="x")

        # Campo para el DNI
        customtkinter.CTkLabel(self.formulario_frame, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
        self.dni_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.dni_entry.grid(row=0, column=1, padx=10, pady=5)

        # Campo para la nueva nota
        customtkinter.CTkLabel(self.formulario_frame, text="Nueva Nota:").grid(row=1, column=0, padx=10, pady=5)
        self.nueva_nota_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.nueva_nota_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botón para modificar la nota
        modificar_button = customtkinter.CTkButton(self.formulario_frame, text="Modificar", command=self.modificar_nota)
        modificar_button.grid(row=2, column=0, columnspan=2, pady=10)

    def modificar_nota(self):
        dni = self.dni_entry.get()
        try:
            nueva_nota = float(self.nueva_nota_entry.get())
        except ValueError:
            self.resultado_texto.insert("0.0", "La nueva nota debe ser un número.\n")
            return

        mensaje = self.gestor.modificar_nota(dni, nueva_nota)
        self.resultado_texto.insert("0.0", mensaje + "\n")

        # Limpiar el formulario
        self.formulario_frame.destroy()

    def mostrar_formulario_agregar(self):
        self.limpiar_ventana()  # Limpiar la ventana antes de mostrar el nuevo formulario

        # Crear un nuevo frame para el formulario
        self.formulario_frame = customtkinter.CTkFrame(self.ventana, corner_radius=20)
        self.formulario_frame.pack(pady=10, padx=10, fill="x")

        # Campo para el DNI
        customtkinter.CTkLabel(self.formulario_frame, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
        self.dni_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.dni_entry.grid(row=0, column=1, padx=10, pady=5)

        # Campo para los apellidos
        customtkinter.CTkLabel(self.formulario_frame, text="Apellidos:").grid(row=1, column=0, padx=10, pady=5)
        self.apellidos_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.apellidos_entry.grid(row=1, column=1, padx=10, pady=5)

        # Campo para los nombres
        customtkinter.CTkLabel(self.formulario_frame, text="Nombres:").grid(row=2, column=0, padx=10, pady=5)
        self.nombres_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.nombres_entry.grid(row=2, column=1, padx=10, pady=5)

        # Campo para la nota
        customtkinter.CTkLabel(self.formulario_frame, text="Nota:").grid(row=3, column=0, padx=10, pady=5)
        self.nota_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.nota_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botón para guardar el alumno
        guardar_button = customtkinter.CTkButton(self.formulario_frame, text="Guardar", command=self.guardar_alumno)
        guardar_button.grid(row=4, column=0, columnspan=2, pady=10)

    def guardar_alumno(self):
        # Obtener los valores ingresados
        dni = self.dni_entry.get()
        apellidos = self.apellidos_entry.get()
        nombres = self.nombres_entry.get()
        try:
            nota = float(self.nota_entry.get())
        except ValueError:
            self.resultado_texto.insert("0.0", "La nota debe ser un número.\n")
            return

        # Agregar el alumno a la lógica
        mensaje = self.gestor.agregar_alumno(dni, apellidos, nombres, nota)
        self.resultado_texto.insert("0.0", mensaje + "\n")

        # Limpiar el formulario
        self.formulario_frame.destroy()

    def mostrar_formulario_eliminar(self):
        self.limpiar_ventana()  # Limpiar la ventana antes de mostrar el nuevo formulario

        # Crear un nuevo frame para el formulario
        self.formulario_frame = customtkinter.CTkFrame(self.ventana, corner_radius=20)
        self.formulario_frame.pack(pady=10, padx=10, fill="x")

        # Campo para el DNI
        customtkinter.CTkLabel(self.formulario_frame, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
        self.dni_entry = customtkinter.CTkEntry(self.formulario_frame)
        self.dni_entry.grid(row=0, column=1, padx=10, pady=5)

        # Botón para eliminar el alumno
        eliminar_button = customtkinter.CTkButton(self.formulario_frame, text="Eliminar", command=self.eliminar_alumno)
        eliminar_button.grid(row=1, column=0, columnspan=2, pady=10)

    def eliminar_alumno(self):
        self.mostrar_alumnos()
        dni = self.dni_entry.get()
        mensaje = self.gestor.eliminar_alumno(dni)
        self.resultado_texto.insert("0.0", mensaje + "\n")
        self.formulario_frame.destroy()

    def consultar_alumno(self):
        dni = self.dni_entry.get()
        alumno = self.gestor.consultar_alumno(dni)
        if isinstance(alumno, dict):
            self.resultado_texto.insert("0.0", f"{alumno['dni']} - {alumno['apellidos']} {alumno['nombre']}: Nota {alumno['nota']} - Calificación: {alumno['calificacion']}\n")
        else:
            self.resultado_texto.insert("0.0", alumno + "\n")
        self.formulario_frame.destroy()

    def mostrar_alumnos(self, criterio=None):
        """Función para mostrar alumnos según el criterio"""
        alumnos = self.gestor.obtener_alumnos(criterio)
        self.resultado_texto.delete("0.0", "end")
        if isinstance(alumnos, list) and alumnos:
            for alumno in alumnos:
                self.resultado_texto.insert("end", f"{alumno['dni']} - {alumno['apellidos']} {alumno['nombre']}: Nota {alumno['nota']} - Calificación: {alumno['calificacion']}\n")
        else:
            self.resultado_texto.insert("0.0", "No se encontraron alumnos con este criterio.\n")


if __name__ == "__main__":
    GUI()
