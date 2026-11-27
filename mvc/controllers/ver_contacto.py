import web
import logging
from mvc.models.model_contactos import ModelContactos
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class VerContacto:

    def GET(self, id_hash: str):
        session = web.config._session
        # RNT01: valida la sesión antes de ejecutar
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        try:
            model_contactos = ModelContactos()

            # Verifica la firma id_contacto:HASH
            id_contacto = model_contactos.validarHash(id_hash)
            if id_contacto is None:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            contacto = model_contactos.buscarContacto(id_contacto)
            if contacto == []:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            return render.ver_contacto(contacto[0])  # type: ignore
        except Exception as error:
            logger.error("ERROR 440: %s", error)
            print(f"ERROR 440: {str(error)}")
            return render.mensaje("Contacto no encontrado")  # type: ignore
