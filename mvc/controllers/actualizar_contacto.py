import web
import logging
from mvc.models.model_contactos import ModelContactos
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class ActualizarContacto:

    # Muestra el formulario con los datos actuales
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

            return render.actualizar_contacto(contacto[0], id_hash)  # type: ignore
        except Exception as error:
            logger.error("ERROR 460: %s", error)
            print(f"ERROR 460: {str(error)}")
            return render.mensaje("Contacto no encontrado")  # type: ignore

    # Recibe los datos nuevos y los guarda
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

            formulario = web.input(foto={})
            nombre: str = formulario["nombre"].strip()
            email: str = formulario["email"].strip()
            telefono: str = formulario["telefono"].strip()

            if nombre == "" or email == "" or telefono == "":
                return render.mensaje("Todos los campos son obligatorios")  # type: ignore

            # Por defecto conserva la foto actual
            foto_actual: str = contacto[0].get("foto") or "default.png"
            foto: str | None = foto_actual

            # Solo cambia la foto si se cargó una nueva
            nombre_archivo: str = getattr(formulario.foto, "filename", "") or ""
            if nombre_archivo != "":
                if not model_contactos.extensionValida(nombre_archivo):
                    return render.mensaje("Formato de imagen no válido (solo .jpg, .jpeg, .png, .webp)")  # type: ignore
                foto = model_contactos.guardarFoto(nombre_archivo, formulario.foto.file.read())
                if foto is None:
                    return render.mensaje("No se pudo guardar la imagen")  # type: ignore

            datos = model_contactos.actualizarContacto(id_contacto, nombre, email, telefono, foto)
            if datos == []:
                if foto != foto_actual:
                    model_contactos.borrarFoto(foto)
                return render.mensaje("No se pudo actualizar el contacto")  # type: ignore

            # Si se subió una foto nueva, borra el archivo anterior
            if foto != foto_actual:
                model_contactos.borrarFoto(foto_actual)

            return render.mensaje("Contacto actualizado correctamente")  # type: ignore
        except Exception as error:
            logger.error("ERROR 461: %s", error)
            print(f"ERROR 461: {str(error)}")
            return render.mensaje("No se pudo actualizar el contacto")  # type: ignore
