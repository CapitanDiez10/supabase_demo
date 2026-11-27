import web
import logging
from mvc.models.model_contactos import ModelContactos, FOTO_DEFAULT
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


class InsertarContacto:

    # Renderiza el formulario insertar_contacto.html
    def GET(self):
        session = web.config._session
        # RNT01: valida la sesión antes de ejecutar
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        return render.insertar_contacto()  # type: ignore

    # Recibe los datos del formulario, sube la foto e inserta el contacto
    def POST(self):
        session = web.config._session
        if not ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/login")
        try:
            # foto={} le indica a web.py que 'foto' es un archivo
            formulario = web.input(foto={})
            nombre: str = formulario["nombre"].strip()
            email: str = formulario["email"].strip()
            telefono: str = formulario["telefono"].strip()

            # Valida que los campos obligatorios no estén vacíos
            if nombre == "" or email == "" or telefono == "":
                return render.mensaje("Todos los campos son obligatorios")  # type: ignore

            model_contactos = ModelContactos()

            # Si no se sube foto se usa la imagen por defecto
            foto: str | None = FOTO_DEFAULT
            nombre_archivo: str = getattr(formulario.foto, "filename", "") or ""
            if nombre_archivo != "":
                if not model_contactos.extensionValida(nombre_archivo):
                    return render.mensaje("Formato de imagen no válido (solo .jpg, .jpeg, .png, .webp)")  # type: ignore
                foto = model_contactos.guardarFoto(nombre_archivo, formulario.foto.file.read())
                if foto is None:
                    return render.mensaje("No se pudo guardar la imagen")  # type: ignore

            datos = model_contactos.insertarContacto(nombre, email, telefono, foto)
            if datos == []:
                # Si falló la inserción, borra la foto que se acababa de subir
                model_contactos.borrarFoto(foto)
                return render.mensaje("No se pudo insertar el contacto")  # type: ignore

            return render.mensaje("Contacto insertado correctamente")  # type: ignore
        except Exception as error:
            logger.error("ERROR 450: %s", error)
            print(f"ERROR 450: {str(error)}")
            return render.mensaje("No se pudo insertar el contacto")  # type: ignore
