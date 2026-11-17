import web
from mvc.models.model_contactos import ModelContactos

render = web.template.render("mvc/views", base="template")


class ActualizarContacto:

    # Muestra el formulario con los datos actuales
    def GET(self, id_contacto):
        model_contactos = ModelContactos()
        contacto = model_contactos.buscarContacto(id_contacto)
        return render.actualizar_contacto(contacto)  # type: ignore

    # Recibe los datos nuevos y los guarda
    def POST(self, id_contacto):
        formulario = web.input()
        nombre = formulario['nombre']
        email = formulario['email']
        telefono = formulario['telefono']

        model_contactos = ModelContactos()
        model_contactos.actualizarContacto(id_contacto, nombre, email, telefono)

        html = """
            <h1>Contacto actualizado correctamente</h1>
            <a href='/contactos'>Regresar</a>
        """
        return html