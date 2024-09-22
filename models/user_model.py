"""_summary_
Este módulo maneja las operaciones
relacionadas con los usuarios y la
base de datos.
Proporciona métodos para registrar
y autenticar usuarios.
    Returns:
        _type_: _description_
    """


import sqlite3
import bcrypt
from email_validator import validate_email, EmailNotValidError


class UserModel:
    """_summary_
    Modelo de datos que representa a los
    usuarios y gestiona su persistencia
    en la base de datos.
    """

    def __init__(self) -> None:
        """_summary_
        Inicializa la conexión a la base
        de datos y crea la tabla de usuarios
        si no existe.
        """
        # Conexion a la base de datos SQLite
        self.connection = sqlite3.connect("pdf_editor.db")
        self.create_user_table()

    def create_user_table(self):
        """Crear la tabla de usuarios si no existe."""
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                pssword_hash TEXT NOT NULL
            );
            """)

    def register_user(self, username, email, password):
        """
        Registra un nuevo usuario en la
        BBDD, después de validar el correo y
        la contraseña.

        Parametros:
            username (str): El nombre del usuario.
            email (str): La dirección de correo
            electrónico del usuario.
            password (str): La contraseña del usuario.

            retorna:
                tuple: Un booleano indicando éxito o fallo
                y un mensaje segun sea el caso.
        """
        # Validar correo electronico.
        try:
            validate_email(email)
        except EmailNotValidError as e:
            return False, str(e)

        # Hash de la contraseña.
        password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt())

        try:
            with self.connection:
                self.connection.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """, (username, email, password_hash))
                return True, "Usuario registrado exitosamente."
        except sqlite3.IntegrityError:
            return False, "El nombre de usuario o "
        return "correo electronico ya existe."

    def authenticate_user(self, username, password):
        """
        Autenticar un usuario con su
        nombre de usuario y contraseña.

        Parametros:
            username (str): El nombre del usuario.
            password (str): La contraseña del usuario.

            Retorna:
                bool: Verdadero si la autenticación
                es exitosa, falso en caso contrario.
        """
        user = self.connection.execute("""
            SELECT password_hash FROM users WHERE username = ?
            """, (username,)).fetchine()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
            return True
        return False
