"""Pipedrive SIMULADO para probar el webhook sin cuenta real.

Imita las 5 rutas que usa el proyecto y guarda en memoria las notas creadas.
Ejecutar:  uvicorn pruebas.pipedrive_simulado:app --port 9000
"""
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

DEALS = {
    101: {"id": 101, "title": "Prime Health - 120 ErgoPro Specialist", "org_id": 1, "person_id": 1,
          "custom_fields": {}},
    102: {"id": 102, "title": "Deal sin relato", "org_id": None, "person_id": None,
          "custom_fields": {}},
}
NOTAS = {
    101: [{"id": 1, "content": "<p>Renata (Superintendente RR. HH.) cuenta que tuvieron un proceso "
                               "laboral por LER de operadores de teleatención. La junta siempre "
                               "compró muebles baratos de acero y se resiste a invertir. Le "
                               "presentamos el costo de siniestralidad el 15/10. Quieren 120 sillas.</p>"}],
    102: [],
}
NOMBRES = {"organizations": {1: "Prime Health Operadora"}, "persons": {1: "Dra. Renata Beltrão"}}


def _token(x_api_token: str | None) -> None:
    if x_api_token != "token-de-prueba":
        raise HTTPException(401, "token inválido")


@app.get("/api/v2/deals/{deal_id}")
def deal(deal_id: int, x_api_token: str | None = Header(None)):
    _token(x_api_token)
    if deal_id not in DEALS:
        raise HTTPException(404)
    return {"success": True, "data": DEALS[deal_id]}


@app.get("/api/v2/{tipo}/{item_id}")
def nombre(tipo: str, item_id: int, x_api_token: str | None = Header(None)):
    _token(x_api_token)
    return {"success": True, "data": {"id": item_id, "name": NOMBRES[tipo][item_id]}}


@app.get("/api/v1/notes")
def notas(deal_id: int, x_api_token: str | None = Header(None)):
    _token(x_api_token)
    return {"success": True, "data": NOTAS.get(deal_id, [])}


@app.post("/api/v1/notes")
def crear(body: dict, x_api_token: str | None = Header(None)):
    _token(x_api_token)
    nueva = {"id": 1000 + sum(len(v) for v in NOTAS.values()), "content": body["content"]}
    NOTAS.setdefault(body["deal_id"], []).append(nueva)
    return {"success": True, "data": nueva}


@app.get("/_notas/{deal_id}")
def ver(deal_id: int):
    """Ruta auxiliar para inspeccionar qué notas quedaron."""
    return NOTAS.get(deal_id, [])
