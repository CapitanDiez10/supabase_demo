import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Lee las variables de entorno del archivo .env
load_dotenv()

# Logger con el nombre del módulo para identificarlo en el log
logger = logging.getLogger(__name__)


class ModelSesiones:
    """Maneja la tabla sesiones_abiertas de Supabase."""

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", "")
            )
        except Exception as error:
            logger.error("ERROR 300: %s", error)
            print(f"ERROR 300: {str(error)}")

    def registrarToken(self, token: str) -> bool:
        try:
            # INSERT INTO sesiones_abiertas(token) VALUES(?);
            self.supabase.table("sesiones_abiertas").insert({"token": token}).execute()
            return True
        except Exception as error:
            logger.error("ERROR 301: %s", error)
            print(f"ERROR 301: {str(error)}")
            return False

    def validarToken(self, token: str | None) -> bool:
        try:
            # Si no hay token en la sesión, no está autenticado
            if not token:
                return False
            # SELECT token FROM sesiones_abiertas WHERE token = ?;
            response = (
                self.supabase.table("sesiones_abiertas")
                .select("token")
                .eq("token", token)
                .execute()
            )
            # Es válido solo si el token existe en la tabla
            return len(response.data) > 0
        except Exception as error:
            logger.error("ERROR 302: %s", error)
            print(f"ERROR 302: {str(error)}")
            return False

    def borrarToken(self, token: str | None) -> bool:
        try:
            if not token:
                return False
            # DELETE FROM sesiones_abiertas WHERE token = ?;
            self.supabase.table("sesiones_abiertas").delete().eq("token", token).execute()
            return True
        except Exception as error:
            logger.error("ERROR 303: %s", error)
            print(f"ERROR 303: {str(error)}")
            return False
