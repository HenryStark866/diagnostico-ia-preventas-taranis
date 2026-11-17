"""Lee la configuración desde el archivo .env.

Regla de oro: las claves se leen aquí y NUNCA se imprimen en pantalla ni en logs.
"""
import os

from dotenv import load_dotenv

# Carga las variables del archivo .env (si existe) sin pisar las que ya estén en el sistema.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

PIPEDRIVE_API_TOKEN = os.getenv("PIPEDRIVE_API_TOKEN", "")
PIPEDRIVE_DOMAIN = os.getenv("PIPEDRIVE_DOMAIN", "")

WEBHOOK_USER = os.getenv("WEBHOOK_USER", "")
WEBHOOK_PASSWORD = os.getenv("WEBHOOK_PASSWORD", "")

# Segundos de espera antes de leer el deal (para que alcance a guardarse la nota con el relato).
ESPERA_ANTES_DE_LEER = int(os.getenv("ESPERA_ANTES_DE_LEER", "20"))
# Solo para pruebas locales: permite apuntar a un Pipedrive simulado (ej. http://127.0.0.1:9000).
PIPEDRIVE_BASE_URL = os.getenv("PIPEDRIVE_BASE_URL", "")


def exigir(*nombres: str) -> None:
    """Detiene el programa con un mensaje claro si falta alguna variable."""
    faltan = [n for n in nombres if not globals().get(n)]
    if faltan:
        raise SystemExit(
            f"Faltan variables en .env: {', '.join(faltan)}. "
            "Copia .env.example como .env y complétalo."
        )
