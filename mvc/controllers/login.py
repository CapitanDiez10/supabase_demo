import web
import logging
from mvc.models.auth_users import AuthUsers
from mvc.models.model_sesiones import ModelSesiones

logger = logging.getLogger(__name__)

# El login no usa template.html porque no debe mostrar el menú
render = web.template.render("mvc/views")


class Login:

    def GET(self):
        session = web.config._session
        # Si ya tiene una sesión válida, lo manda directo al index
        if ModelSesiones().validarToken(session.get("token")):
            raise web.seeother("/")
        return render.login("")  # type: ignore

    def POST(self):
        session = web.config._session
        token: str | None = None
        email: str = ""
        try:
            formulario = web.input()
            email = formulario["email"].strip()
            password: str = formulario["password"]

            # Envía las credenciales a Supabase Authentication
            token = AuthUsers().iniciarSesion(email, password)

            # Registra el token en la tabla sesiones_abiertas
            if token and not ModelSesiones().registrarToken(token):
                token = None
        except Exception as error:
            logger.error("ERROR 400: %s", error)
            print(f"ERROR 400: {str(error)}")
            token = None

        if token:
            # Guarda el token en la variable de sesión (cookie)
            session.token = token
            session.email = email
            raise web.seeother("/")

        return render.login("Credenciales incorrectas, verifique sus datos")  # type: ignore
