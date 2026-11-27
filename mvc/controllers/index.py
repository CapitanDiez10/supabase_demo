import web
import logging
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class Index:

    def GET(self):
        session = web.config._session
        # RNT01: valida la sesión antes de ejecutar
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        try:
            return render.index(session.get("email"))  # type: ignore
        except Exception as error:
            logger.error("ERROR 420: %s", error)
            print(f"ERROR 420: {str(error)}")
            return "Ocurrió un error al cargar la página"
