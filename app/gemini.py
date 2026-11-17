"""Conexión con Gemini (SDK oficial google-genai).

Documentación: https://googleapis.github.io/python-genai/
"""
import time

from google import genai
from google.genai import errors, types

from app import config
from app.prompt_sistema import PROMPT_SISTEMA, armar_mensaje

# Errores que vale la pena reintentar: 429 = límite de solicitudes, 5xx = falla temporal de Google.
CODIGOS_REINTENTABLES = {429, 500, 502, 503, 504}

_cliente = None


def _obtener_cliente() -> genai.Client:
    """Crea el cliente una sola vez y lo reutiliza."""
    global _cliente
    if _cliente is None:
        config.exigir("GEMINI_API_KEY")
        _cliente = genai.Client(api_key=config.GEMINI_API_KEY)
    return _cliente


class ErrorGemini(Exception):
    """Error propio para que quien llame sepa que falló la IA (no el CRM)."""


def diagnosticar(titulo: str, organizacion: str, persona: str, relato: str,
                 intentos: int = 4) -> str:
    """Envía el relato a Gemini y devuelve el diagnóstico en Markdown.

    Si Google responde 429 (límite) o un 5xx, espera y reintenta con espera
    creciente: 2 s, 4 s, 8 s...
    """
    mensaje = armar_mensaje(titulo, organizacion, persona, relato)
    configuracion = types.GenerateContentConfig(
        system_instruction=PROMPT_SISTEMA,
        temperature=0.3,  # baja = respuestas más consistentes entre un caso y otro
    )

    for intento in range(1, intentos + 1):
        try:
            respuesta = _obtener_cliente().models.generate_content(
                model=config.GEMINI_MODEL,
                contents=mensaje,
                config=configuracion,
            )
            texto = (respuesta.text or "").strip()
            if not texto:
                raise ErrorGemini("Gemini respondió vacío (posible bloqueo de seguridad).")
            return texto
        except errors.APIError as e:
            if e.code in CODIGOS_REINTENTABLES and intento < intentos:
                espera = 2 ** intento
                print(f"  Gemini respondió {e.code}; reintento {intento}/{intentos - 1} en {espera} s...")
                time.sleep(espera)
                continue
            # Solo se muestra el código y el mensaje de Google, nunca la clave.
            raise ErrorGemini(f"Gemini falló ({e.code}): {e.message}") from e

    raise ErrorGemini("Gemini no respondió después de varios intentos.")
