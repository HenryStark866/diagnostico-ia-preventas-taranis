"""Cliente mínimo de la API de Pipedrive.

Documentación oficial:
- Autenticación: header `x-api-token` (https://pipedrive.readme.io/docs/core-api-concepts-authentication)
- Deals/Personas/Organizaciones: API v2  ->  GET /api/v2/deals/{id}, /persons/{id}, /organizations/{id}
- Notas: API v1  ->  GET /api/v1/notes?deal_id=  y  POST /api/v1/notes {content (HTML), deal_id}
"""
import html
import re
import time

import requests

from app import config

TIEMPO_ESPERA = 15  # segundos máximos por llamada HTTP
MARCA_DIAGNOSTICO = "Diagnóstico IA — Pre-Ventas"  # para reconocer notas que ya escribimos


class ErrorPipedrive(Exception):
    pass


def _url(ruta: str) -> str:
    base = config.PIPEDRIVE_BASE_URL or f"https://{config.PIPEDRIVE_DOMAIN}.pipedrive.com"
    return f"{base}{ruta}"


def _llamar(metodo: str, ruta: str, intentos: int = 3, **kwargs) -> dict:
    """Hace la llamada HTTP con el token en el header y reintenta si hay 429 o 5xx."""
    config.exigir("PIPEDRIVE_API_TOKEN", "PIPEDRIVE_DOMAIN")
    cabeceras = {"x-api-token": config.PIPEDRIVE_API_TOKEN}
    for intento in range(1, intentos + 1):
        try:
            r = requests.request(metodo, _url(ruta), headers=cabeceras,
                                 timeout=TIEMPO_ESPERA, **kwargs)
        except requests.RequestException as e:
            if intento < intentos:
                time.sleep(2 ** intento)
                continue
            # type(e).__name__ y no str(e): el mensaje podría incluir la URL completa.
            raise ErrorPipedrive(f"Sin conexión con Pipedrive ({type(e).__name__})") from e

        if r.status_code == 429 or r.status_code >= 500:
            if intento < intentos:
                # Pipedrive puede indicar cuánto esperar; si no, espera creciente.
                espera = int(r.headers.get("Retry-After", 2 ** intento))
                time.sleep(min(espera, 30))
                continue
        if not r.ok:
            raise ErrorPipedrive(f"Pipedrive respondió {r.status_code} en {metodo} {ruta}")
        return r.json()
    raise ErrorPipedrive("Pipedrive no respondió tras varios intentos")


def _nombre(ruta: str) -> str:
    """Devuelve el nombre de una persona u organización, o '' si no se puede leer."""
    try:
        return _llamar("GET", ruta).get("data", {}).get("name", "") or ""
    except ErrorPipedrive:
        return ""


def _texto_plano(contenido_html: str) -> str:
    """Las notas vienen en HTML; las pasamos a texto para Gemini."""
    sin_etiquetas = re.sub(r"<br\s*/?>|</p>|</li>", "\n", contenido_html or "")
    sin_etiquetas = re.sub(r"<[^>]+>", "", sin_etiquetas)
    return html.unescape(sin_etiquetas).strip()


def leer_deal(deal_id: int) -> dict:
    """Reúne título, organización, persona y el relato (notas previas del deal)."""
    deal = _llamar("GET", f"/api/v2/deals/{deal_id}").get("data") or {}
    if not deal:
        raise ErrorPipedrive(f"El deal {deal_id} no existe o fue borrado")

    org_id, persona_id = deal.get("org_id"), deal.get("person_id")
    organizacion = _nombre(f"/api/v2/organizations/{org_id}") if org_id else ""
    persona = _nombre(f"/api/v2/persons/{persona_id}") if persona_id else ""

    notas = _llamar("GET", "/api/v1/notes",
                    params={"deal_id": deal_id, "limit": 50}).get("data") or []
    # Ignoramos nuestros propios diagnósticos para no analizarlos otra vez.
    relatos = [_texto_plano(n.get("content", "")) for n in notas
               if MARCA_DIAGNOSTICO not in (n.get("content") or "")]

    # Campos personalizados de texto (por ejemplo un campo "Relato del cliente").
    # En la API v2 vienen dentro de "custom_fields" con una clave tipo hash.
    personalizados = [v.strip() for v in (deal.get("custom_fields") or {}).values()
                      if isinstance(v, str) and len(v.strip()) > 20]

    return {
        "id": deal_id,
        "titulo": deal.get("title", ""),
        "organizacion": organizacion,
        "persona": persona,
        "relato": "\n\n".join(r for r in personalizados + relatos if r),
        "ya_diagnosticado": len(relatos) < len(notas),
    }


def markdown_a_html(texto: str) -> str:
    """Conversión sencilla de Markdown a HTML para que la nota se vea ordenada."""
    lineas = []
    for linea in html.escape(texto).splitlines():
        linea = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", linea)
        if linea.startswith("## "):
            lineas.append(f"<p><b>{linea[3:]}</b></p>")
        elif re.match(r"^\s*[\*\-] ", linea):
            lineas.append(f"<p>• {re.sub(r'^\s*[\*\-] ', '', linea)}</p>")
        elif linea.strip():
            lineas.append(f"<p>{linea}</p>")
    return "\n".join(lineas)


def crear_nota(deal_id: int, diagnostico_md: str) -> int:
    """Escribe el diagnóstico como nota fijada en el deal. Devuelve el id de la nota."""
    contenido = f"<p><b>🤖 {MARCA_DIAGNOSTICO}</b></p>\n" + markdown_a_html(diagnostico_md)
    datos = _llamar("POST", "/api/v1/notes", json={
        "deal_id": deal_id,
        "content": contenido,
        "pinned_to_deal_flag": 1,
    }).get("data") or {}
    return datos.get("id", 0)
