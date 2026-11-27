import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import hmac
from typing import Any, cast
import logging

# Lee las variables de entorno del archivo .env
load_dotenv()

# Logger con el nombre del módulo para identificarlo en el log
logger = logging.getLogger(__name__)

# Clave secreta para firmar los id (Nota: hardcodeada no es la mejor opción)
CLAVE_SECRETA: bytes = b"hola"

# Carpeta donde se guardan las fotos y extensiones permitidas
CARPETA_FOTOS: str = "static/fotos"
EXTENSIONES_VALIDAS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")
FOTO_DEFAULT: str = "default.png"


class ModelContactos:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", "")
            )
        except Exception as error:
            logger.error("ERROR 100: %s", error)
            print(f"ERROR 100: {str(error)}")

    # ---------------- Firmas HASH (Anti-IDOR) ----------------

    def generarHash(self, id: int) -> str:
        try:
            """Genera la cadena id_contacto:HASH a partir del ID."""
            mensaje = str(id).encode("utf-8")
            firma = hmac.new(CLAVE_SECRETA, mensaje, hashlib.sha256).hexdigest()
            # Concatena el id:firma
            return f"{id}:{firma}"
        except Exception as error:
            logger.error("ERROR 106: %s", error)
            print(f"ERROR 106: {str(error)}")
            return ""

    def validarHash(self, hash_a_validar: str) -> int | None:
        try:
            # Separa el id, separador y la firma
            id_str, sep, _ = hash_a_validar.partition(":")
            resultado_id = None

            # Solo calculamos el hash si la estructura básica es válida
            if sep and id_str.isdigit():
                token_esperado = self.generarHash(int(id_str))
                if hmac.compare_digest(token_esperado, hash_a_validar):
                    resultado_id = int(id_str)

            return resultado_id
        except Exception as error:
            logger.error("ERROR 107: %s", error)
            print(f"ERROR 107: {str(error)}")
            return None

    # ---------------- CRUD contactos ----------------

    def obtenerContactos(self) -> list[dict[str, Any]]:
        try:
            # SELECT id_contacto, nombre, email, telefono, foto FROM contactos;
            response = (
                self.supabase.table("contactos")
                .select("id_contacto, nombre, email, telefono, foto")
                .order("id_contacto")
                .execute()
            )
            return cast(list[dict[str, Any]], response.data or [])
        except Exception as error:
            logger.error("ERROR 101: %s", error)
            print(f"ERROR 101: {str(error)}")
            return []

    def buscarContacto(self, id_contacto: int) -> list[dict[str, Any]]:
        try:
            # SELECT * FROM contactos WHERE id_contacto = ?;
            response = self.supabase.table("contactos").select("*").eq("id_contacto", id_contacto).execute()
            return cast(list[dict[str, Any]], response.data or [])
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            print(f"ERROR 102: {str(error)}")
            return []

    def insertarContacto(self, nombre: str, email: str, telefono: str, foto: str) -> list[dict[str, Any]]:
        try:
            # INSERT INTO contactos(nombre,email,telefono,foto) VALUES(?,?,?,?);
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "foto": foto
            }
            response = self.supabase.table("contactos").insert(data).execute()
            return cast(list[dict[str, Any]], response.data or [])
        except Exception as error:
            logger.error("ERROR 103: %s", error)
            print(f"ERROR 103: {str(error)}")
            return []

    def borrarContacto(self, id_contacto: int) -> list[dict[str, Any]]:
        try:
            # DELETE FROM contactos WHERE id_contacto = ?;
            response = self.supabase.table("contactos").delete().eq("id_contacto", id_contacto).execute()
            return cast(list[dict[str, Any]], response.data or [])
        except Exception as error:
            logger.error("ERROR 104: %s", error)
            print(f"ERROR 104: {str(error)}")
            return []

    def actualizarContacto(self, id_contacto: int, nombre: str, email: str, telefono: str, foto: str) -> list[dict[str, Any]]:
        try:
            # UPDATE contactos SET nombre=?, email=?, telefono=?, foto=? WHERE id_contacto=?;
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "foto": foto
            }
            response = self.supabase.table("contactos").update(data).eq("id_contacto", id_contacto).execute()
            return cast(list[dict[str, Any]], response.data or [])
        except Exception as error:
            logger.error("ERROR 105: %s", error)
            print(f"ERROR 105: {str(error)}")
            return []

    # ---------------- Archivos de imagen (RTT04) ----------------

    def extensionValida(self, nombre_archivo: str) -> bool:
        try:
            # os.path.splitext separa "foto.PNG" en ("foto", ".PNG")
            extension = os.path.splitext(nombre_archivo)[1].lower()
            return extension in EXTENSIONES_VALIDAS
        except Exception as error:
            logger.error("ERROR 108: %s", error)
            print(f"ERROR 108: {str(error)}")
            return False

    def guardarFoto(self, nombre_archivo: str, contenido: bytes) -> str | None:
        ruta: str = ""
        try:
            # Quita rutas y espacios del nombre original
            nombre_limpio = os.path.basename(nombre_archivo).replace(" ", "_")
            # Prefija un timestamp para evitar colisiones de nombres
            nombre_final = f"{int(time.time())}_{nombre_limpio}"
            ruta = os.path.join(CARPETA_FOTOS, nombre_final)
            with open(ruta, "wb") as archivo:
                archivo.write(contenido)
            return nombre_final
        except Exception as error:
            logger.error("ERROR 109: %s", error)
            print(f"ERROR 109: {str(error)}")
            # Si quedó un archivo a medias, lo elimina
            if ruta != "" and os.path.exists(ruta):
                os.remove(ruta)
            return None

    def borrarFoto(self, nombre_archivo: str | None) -> bool:
        try:
            # Nunca se borra la imagen por defecto
            if not nombre_archivo or nombre_archivo == FOTO_DEFAULT:
                return False
            ruta = os.path.join(CARPETA_FOTOS, os.path.basename(nombre_archivo))
            # Verifica que exista antes de borrarla
            if os.path.exists(ruta):
                os.remove(ruta)
                return True
            return False
        except Exception as error:
            logger.error("ERROR 110: %s", error)
            print(f"ERROR 110: {str(error)}")
            return False


if __name__ == "__main__":
    model_contactos = ModelContactos()
    print(model_contactos.obtenerContactos())
    # Pruebas que MODIFICAN la base de datos: descomentar solo si se quieren usar
    #print(model_contactos.buscarContacto(1))
    #print(model_contactos.insertarContacto("Carthoris","carthoris@email","333333","default.png"))
    #print(model_contactos.borrarContacto(4))
    #print(model_contactos.actualizarContacto(5,"Juan","juan@email","8888888","default.png"))
