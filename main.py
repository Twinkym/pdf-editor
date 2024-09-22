"""_summary_
    Este es el punto de entrada principal de
la aplicación de lector y editor de PDF's.
Aquí se inicializan el controlador de autenticación y la interfaz gráfica.

"""

import tkinter as tk
from controllers.auth_controller import AuthController
from views.main_view import MainView

if __name__ == "__main__":
    # Inicializa la aplicación y ejecuta la ventana principal.
    root = tk.Tk()
    auth_controller = AuthController()
    app = MainView(root, auth_controller)
    root.mainloop()
