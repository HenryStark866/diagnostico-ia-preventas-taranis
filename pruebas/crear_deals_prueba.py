"""Crea en tu Pipedrive deals de prueba con los casos del Mock Kit (dispara el webhook real).

Por cada caso crea: organización, persona, deal y una nota con el relato del vendedor.
Uso:  python pruebas/crear_deals_prueba.py 1043 1050 borde-sin-relato
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import pipedrive  # noqa: E402

VALORES = {"1042": 199200, "1043": 65880, "1045": 801900, "1050": 224100, "1059": 180500,
           "borde-sin-relato": 96000}


def crear(caso: dict) -> int:
    org = pipedrive._llamar("POST", "/api/v2/organizations",
                            json={"name": caso["organizacion"].split(" (")[0]})["data"]["id"]
    persona = pipedrive._llamar("POST", "/api/v2/persons",
                                json={"name": caso["persona"].split(" - ")[0], "org_id": org})["data"]["id"]
    deal = pipedrive._llamar("POST", "/api/v2/deals", json={
        "title": caso["titulo"], "value": VALORES.get(caso["id"], 0), "currency": "USD",
        "org_id": org, "person_id": persona})["data"]["id"]
    if caso["relato"]:
        pipedrive._llamar("POST", "/api/v1/notes",
                          json={"deal_id": deal, "content": f"<p>{caso['relato']}</p>"})
    return deal


if __name__ == "__main__":
    casos = json.loads((Path(__file__).parent.parent / "ejemplos" / "casos.json").read_text(encoding="utf-8"))
    for c in casos:
        if c["id"] in sys.argv[1:]:
            print(f"Deal #{crear(c)} creado: {c['titulo']}")
