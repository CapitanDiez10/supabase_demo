import web
import logging
from mvc.models.model_contactos import ModelContactos
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class ListaContactos:

    def GET(self):
        session = web.config._session
        # RNT01: valida la sesión antes de ejecutar
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        try:
            model_contactos = ModelContactos()

            # Almacena en datos los registros recibidos de Supabase
            datos = model_contactos.obtenerContactos()

            # Recorre cada registro y cambia el id por id_contacto:HASH
            for registro in datos:
                registro["id_contacto"] = model_contactos.generarHash(int(registro["id_contacto"]))

            # Envía a lista_contactos.html los datos ya firmados
            return render.lista_contactos(datos)  # type: ignore
        except Exception as error:
            logger.error("ERROR 430: %s", error)
            print(f"ERROR 430: {str(error)}")
            return render.mensaje("Ocurrió un error al cargar los contactos")  # type: ignore
