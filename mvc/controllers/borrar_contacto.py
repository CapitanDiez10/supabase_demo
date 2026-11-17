import web
from mvc.models.model_contactos import ModelContactos

render = web.template.render("mvc/views", base="template")


class BorrarContacto:

    # Muestra los datos del contacto a borrar
    def GET(self, id_contacto):
        model_contactos = ModelContactos()
        contacto = model_contactos.buscarContacto(id_contacto)
        return render.borrar_contacto(contacto)  # type: ignore

    # Borra el contacto
    def POST(self, id_contacto):
        model_contactos = ModelContactos()
        model_contactos.borrarContacto(id_contacto)

        html = """
            <h1>Contacto borrado correctamente</h1>
            <a href='/contactos'>Regresar</a>
        """
        return html