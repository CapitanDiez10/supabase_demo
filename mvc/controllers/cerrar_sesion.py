import web
import logging
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)


class CerrarSesion:

    def GET(self):
        session = web.config._session
        try:
            # Elimina el token de la tabla sesiones_abiertas
            ModelSesiones().borrarToken(session.get("token"))
            # Destruye la variable de sesión local
            session.kill()
        except Exception as error:
            logger.error("ERROR 410: %s", error)
            print(f"ERROR 410: {str(error)}")
        raise web.seeother("/login")
