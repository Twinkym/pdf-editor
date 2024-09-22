"""_summary_
    Este módulo contiene el controlador
    para la autenticación de usuarios
    en la aplicación.

    Returns:
        _type_: _description_
    """

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.user_model import UserModel
import config


class AuthController:
    """_summary_
    Controlador que maneja la lógica de autenticación y registro de usuarios.
    """

    def __init__(self):
        """_summary_
        Inicializa el controlador y configura el modelo de usuario.
        """
        self.user_model = UserModel()

    def register_user(self, username, email, password):
        """_summary_
        Registra un nuevo usuario en el sistema
        Args:
            username (str): Nombre de usuario.
            email (str): Dirección de correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            tuple: Un booleano indicando éxito
            o fallo y un mensaje segun sea el caso.
        """
        return self.user_model.register_user(username, email, password)

    def send_confirmation_email(self, email, username):
        """_summary_
        Envía un correo de confirmación de
        registro al usuario.

        Args:
            email (str): El correo electrónico del usuario
            username (str): El nombre del usuario.
        """
        # Crear el mensaje del correo
        msg = MIMEMultipart()
        msg['From'] = config.SMTP_USER
        msg['to'] = email
        msg['subject'] = "Confirmación de Registro - PDF Editor"

        # Cuerpo del mensaje
        body = f"Hola {username},\n\nGracias por"
        body = "registrarte en PDF editor.\n\nSaludos,"
        body = "\nEl equipo de PDF Editor"
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Conectar al servidor SMTP.
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            server.starttls()  # Iniciar cifrado TLS
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)

            # Enviar el correo
            server.send_message(msg)
            server.quit()
            print(f"Correo de confirmación enviado a {email}")

        # Envio de errores detallado.
        except smtplib.SMTPAuthenticationError:
            print("""Error de autenticación SMTP
                  por favor verifica las credenciales.
                  """)
        except smtplib.SMTPConnectError:
            print("Error al conectarse al servidor SMTP" +
                  "Verifica la conexión."
                  )
        except smtplib.SMTPRecipientsRefused:
            print(f"El correo a {email} due rechzado por el servidor")
        except smtplib.SMTPException as e:
            print(f"No se pudo enviar el correo: {e}")
        except ConnectionError:
            print("Error de conexión. No se pudo enviar el correo.")
        except OSError as e:
            print(f"Error relacionado con el sistema operativo: {e}")
