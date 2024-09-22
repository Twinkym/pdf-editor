"""_summary_
    Este módulo gestiona la vista principal
    del programa, que incluye la interfaz
    gráfica de usuario. La interfaz permite
    a los usuarios registrarse en el sistema.
    """

import tkinter as tk
from tkinter import messagebox
import json


class MainView:
    """
    Clase que representa la vista principal
    de la aplicación y contiene la interfaz
    gráfica de usuario.
    """

    def __init__(self, root, controller, language="en"):
        """
        Inicializa la ventana principal y
        crea los elementos gráficos de la interfaz.

        Parámetros:
            root (Tk): La ventana raíz de tkinter.
            controller (AuthController): El controlador
            de autenticación para manejar la lógica de negocio.
        """
        self.root = root
        self.controller = controller
        self.language = language
        self.load_translations()
        self.root.title(
            "PDF Editor - Creado por David De La Puente Enriquez")
        self.root.geometry("500x400")

        # Interfaz de registro.
        self.register_frame = tk.Frame(root)
        self.login_frame = tk.Frame(root)

        self.create_register_view()

    def load_translations(self):
        """_summary_
        Carga las traducciones del archivo de idioma seleccionado.
        """
        with open(f"i18n/{self.language}.json",
                  "r", encoding="utf-8"
                  ) as file:
            self.translations = json.load(file)

    def create_register_view(self):
        """Crear la interfaz de registro."""
        self.clear_frame(self.register_frame)

        tk.Label(self.register_frame,
                 text=self.translations["register_title"],
                 font=("Helvetica", 20)).pack(pady=20)

        tk.Label(self.register_frame,
                 text=self.translations["username"]).pack()
        self.username_entry = tk.Entry(self.register_frame)
        self.username_entry.pack()

        tk.Label(self.register_frame, text=self.translations["email"]).pack()
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.pack()

        tk.Label(self.register_frame,
                 text=self.translations["password"]).pack()
        self.password_entry = tk.Entry(self.register_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.register_frame,
                  text=self.translations["register_button"],
                  command=self.register).pack()

    def register(self):
        """
            Manejador para el registro de usuarios,
        invocado cuando el usuario hace clic
        en el botón "Registrar".
        """
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        success, message = self.controller.register_user(
            username, email, password)
        if success:
            messagebox.showinfo("Exito", message)
        else:
            messagebox.showerror("Error", message)

    def clear_frame(self, frame):
        """
            Elimina todos los elementos gráficos de un frame.

            Parámetros:
            frame (Frame): El frame de tkinter a limpiar.
        """
        for widget in frame.winfo_children():
            widget.destroy()
