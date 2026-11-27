import web
import logging
from mvc.models.model_contactos import ModelContactos
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class BorrarContacto:

    # Muestra los datos del contacto a borrar (solo lectura)
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

            return render.borrar_contacto(contacto[0], id_hash)  # type: ignore
        except Exception as error:
            logger.error("ERROR 470: %s", error)
            print(f"ERROR 470: {str(error)}")
            return render.mensaje("Contacto no encontrado")  # type: ignore

    # Borra la foto y el contacto
    def POST(self, id_hash: str):
        session = web.config._session
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        try:
            model_contactos = ModelContactos()

            # Valida nuevamente la firma id_contacto:HASH
            id_contacto = model_contactos.validarHash(id_hash)
            if id_contacto is None:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            contacto = model_contactos.buscarContacto(id_contacto)
            if contacto == []:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            # Elimina el archivo de imagen (si existe y no es la de por defecto)
            model_contactos.borrarFoto(contacto[0].get("foto"))

            # Elimina el registro en Supabase
            model_contactos.borrarContacto(id_contacto)

            return render.mensaje("Contacto eliminado correctamente")  # type: ignore
        except Exception as error:
            logger.error("ERROR 471: %s", error)
            print(f"ERROR 471: {str(error)}")
            return render.mensaje("No se pudo eliminar el contacto")  # type: ignore
