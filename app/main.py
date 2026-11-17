"""Servicio web (FastAPI) que recibe el webhook de Pipedrive.

Flujo:
  1. Pipedrive avisa: "se creó un deal" (evento v2: create.deal).
  2. Respondemos 200 en milisegundos (Pipedrive solo espera 10 s y si no, reintenta).
  3. En segundo plano: leemos el deal, pedimos el diagnóstico a Gemini y lo
     escribimos como nota en el mismo deal.

Ejecutar:  uvicorn app.main:app --port 8000
"""
import json
import logging
import secrets
import threading
import time
from pathlib import Path

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import config, pipedrive
from app.gemini import ErrorGemini, diagnosticar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("preventas")

app = FastAPI(title="Diagnóstico IA de Pre-Ventas — Taranis Black")
seguridad = HTTPBasic(auto_error=False)

# Segundos que esperamos antes de leer el deal: da tiempo a que el vendedor
# (o la automatización) agregue la nota con el relato justo después de crearlo.
ESPERA_ANTES_DE_LEER = config.ESPERA_ANTES_DE_LEER

# ---------- Protección contra webhooks duplicados ----------
# Pipedrive reintenta si no recibe 200 a tiempo, y puede mandar el mismo evento dos veces.
# Guardamos los deals ya procesados en un archivo para que sobreviva a reinicios.
ARCHIVO_PROCESADOS = Path(__file__).parent.parent / "eventos_procesados.json"
_candado = threading.Lock()


def _cargar_procesados() -> set:
    try:
        return set(json.loads(ARCHIVO_PROCESADOS.read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


_procesados = _cargar_procesados()


def _marcar_si_es_nuevo(deal_id: int) -> bool:
    """True si el deal no se había visto; lo marca en el mismo paso (sin carreras)."""
    with _candado:
        if deal_id in _procesados:
            return False
        _procesados.add(deal_id)
        ARCHIVO_PROCESADOS.write_text(json.dumps(sorted(_procesados)), encoding="utf-8")
        return True


def _olvidar(deal_id: int) -> None:
    """Si el proceso falló, quitamos la marca para permitir un nuevo intento."""
    with _candado:
        _procesados.discard(deal_id)
        ARCHIVO_PROCESADOS.write_text(json.dumps(sorted(_procesados)), encoding="utf-8")


# ---------- Autenticación básica (opcional pero recomendada) ----------
def verificar_credenciales(cred: HTTPBasicCredentials | None = Depends(seguridad)) -> None:
    if not config.WEBHOOK_USER:  # sin usuario configurado no se exige (modo aprendizaje)
        return
    valido = cred is not None and secrets.compare_digest(cred.username, config.WEBHOOK_USER) \
        and secrets.compare_digest(cred.password, config.WEBHOOK_PASSWORD)
    if not valido:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")


# ---------- Trabajo pesado (en segundo plano) ----------
def procesar_deal(deal_id: int) -> None:
    time.sleep(ESPERA_ANTES_DE_LEER)
    try:
        deal = pipedrive.leer_deal(deal_id)
        if deal["ya_diagnosticado"]:
            log.info("Deal %s ya tiene diagnóstico; no se repite.", deal_id)
            return
        if len(deal["relato"]) < 20:
            # Deal sin descripción: no llamamos a Gemini, dejamos una nota que lo explica.
            pipedrive.crear_nota(deal_id, (
                "## ⚠️ Diagnóstico no generado\n"
                "- El negocio no tiene descripción ni notas con el relato del cliente.\n"
                "- **Próximo paso:** registra la necesidad, cantidades y plazo; luego "
                "vuelve a solicitar el diagnóstico."))
            log.info("Deal %s sin relato: se dejó aviso.", deal_id)
            return
        texto = diagnosticar(deal["titulo"], deal["organizacion"], deal["persona"], deal["relato"])
        nota = pipedrive.crear_nota(deal_id, texto)
        log.info("Deal %s diagnosticado. Nota %s creada.", deal_id, nota)
    except (ErrorGemini, pipedrive.ErrorPipedrive) as e:
        log.error("Deal %s falló: %s", deal_id, e)
        _olvidar(deal_id)  # permite reintentarlo después
    except Exception:  # noqa: BLE001 - nunca dejar que un error tumbe el servidor
        log.exception("Error inesperado con el deal %s", deal_id)
        _olvidar(deal_id)


# ---------- Rutas HTTP ----------
@app.get("/")
def salud() -> dict:
    """Para comprobar rápido que el servidor está vivo."""
    return {"estado": "ok", "modelo": config.GEMINI_MODEL}


@app.post("/webhook/pipedrive", dependencies=[Depends(verificar_credenciales)])
async def webhook_pipedrive(request: Request, tareas: BackgroundTasks) -> dict:
    try:
        cuerpo = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El cuerpo no es JSON")

    meta = cuerpo.get("meta") or {}
    # Webhooks v2: meta.action = "create" y meta.entity = "deal".
    # Aceptamos también el formato v1 ("added" / "deal") por compatibilidad.
    accion, entidad = meta.get("action"), meta.get("entity") or meta.get("object")
    if entidad != "deal" or accion not in ("create", "added"):
        return {"ignorado": f"{accion}.{entidad}"}

    deal_id = meta.get("entity_id") or (cuerpo.get("data") or {}).get("id") \
        or (cuerpo.get("current") or {}).get("id")
    try:
        deal_id = int(deal_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=422, detail="No se encontró el id del deal")

    if not _marcar_si_es_nuevo(deal_id):
        log.info("Webhook duplicado para el deal %s (intento %s); se ignora.",
                 deal_id, meta.get("attempt"))
        return {"duplicado": deal_id}

    tareas.add_task(procesar_deal, deal_id)
    log.info("Deal %s recibido; diagnóstico en segundo plano.", deal_id)
    return {"recibido": deal_id}
