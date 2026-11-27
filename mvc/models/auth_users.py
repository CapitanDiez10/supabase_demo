import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Lee las variables de entorno
load_dotenv()

# Configura el sistema de logging
logger = logging.getLogger(__name__)


class AuthUsers:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", "")
            )
        except Exception as error:
            logger.error("ERROR 200: %s", error)
            print(f"ERROR 200: {str(error)}")

    def iniciarSesion(self, email: str, password: str) -> str | None:
        try:
            response = self.supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
            # Regresa el token JWT de la sesión generado por Supabase
            return response.session.access_token  # type: ignore
        except Exception as error:
            logger.error("ERROR 201: %s", error)
            print(f"ERROR 201: {str(error)}")
            return None

    def registrarUsuario(self, email: str, password: str) -> str | None:
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
            print("Usuario registrado exitosamente")
            return response.user.id  # type: ignore
        except Exception as error:
            logger.error("ERROR 202: %s", error)
            print(f"ERROR 202: {str(error)}")
            return None


if __name__ == "__main__":
    print("Autenticación de usuarios")
    objeto = AuthUsers()
    #print(objeto.iniciarSesion("correo@email.com","123456789"))
    #print(objeto.registrarUsuario("correo@email.com","123456789")) # Registra un usuario nuevo
