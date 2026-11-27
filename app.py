import web
import logging

from mvc.controllers.login import Login
from mvc.controllers.cerrar_sesion import CerrarSesion
from mvc.controllers.index import Index
from mvc.controllers.lista_contactos import ListaContactos
from mvc.controllers.ver_contacto import VerContacto
from mvc.controllers.insertar_contacto import InsertarContacto
from mvc.controllers.actualizar_contacto import ActualizarContacto
from mvc.controllers.borrar_contacto import BorrarContacto

logging.basicConfig(
    filename="aplicacion.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",  # Evita errores con tildes o caracteres especiales
)

# Las sesiones de web.py solo funcionan bien con debug en False
web.config.debug = False

urls = (
    '/login', 'Login',
    '/cerrar_sesion', 'CerrarSesion',
    '/', 'Index',
    '/lista_contactos', 'ListaContactos',
    '/ver_contacto/(.*)', 'VerContacto',
    '/insertar_contacto', 'InsertarContacto',
    '/actualizar_contacto/(.*)', 'ActualizarContacto',
    '/borrar_contacto/(.*)', 'BorrarContacto',
)

app = web.application(urls, globals())

# En Codespaces la app está detrás de un proxy y web.py cree que está en
# localhost:8080. Al dejar 'home' vacío, web.seeother("/login") manda solo
# "/login" y el navegador se queda en la URL donde ya está.
def corregirHost() -> None:
    web.ctx.home = web.ctx.homepath

app.add_processor(web.loadhook(corregirHost))

session = web.session.Session(
    app,
    web.session.DiskStore("sessions"),
    initializer={"token": None, "email": None},
)

# Se guarda en web.config para poder usarla desde los controladores
web.config._session = session

if __name__ == "__main__":
    app.run()
