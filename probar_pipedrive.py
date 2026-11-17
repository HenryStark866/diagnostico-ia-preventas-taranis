"""Prueba la conexión con Pipedrive paso a paso (sin webhook).

Uso:
    python probar_pipedrive.py              # lista tus últimos deals (solo lectura)
    python probar_pipedrive.py 12           # lee el deal 12 y muestra lo que se enviaría a Gemini
    python probar_pipedrive.py 12 --nota    # además diagnostica con Gemini y escribe la nota
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

from app import pipedrive  # noqa: E402
from app.gemini import diagnosticar  # noqa: E402


def listar() -> None:
    datos = pipedrive._llamar("GET", "/api/v2/deals",
                              params={"limit": 10, "sort_by": "add_time", "sort_direction": "desc"})
    deals = datos.get("data") or []
    if not deals:
        print("Conexión OK, pero no hay deals. Crea uno en Pipedrive y vuelve a probar.")
    for d in deals:
        print(f"  #{d['id']}  {d.get('title')}")


def probar(deal_id: int, escribir: bool) -> None:
    deal = pipedrive.leer_deal(deal_id)
    print(f"Título:       {deal['titulo']}")
    print(f"Organización: {deal['organizacion'] or '(sin organización)'}")
    print(f"Persona:      {deal['persona'] or '(sin persona)'}")
    print(f"Relato:       {deal['relato'] or '(vacío)'}")
    print(f"Ya tenía diagnóstico: {deal['ya_diagnosticado']}")
    if escribir:
        if not deal["relato"]:
            print("\nEl deal no tiene relato: agrega una nota o completa el campo antes de diagnosticar.")
            return
        texto = diagnosticar(deal["titulo"], deal["organizacion"], deal["persona"], deal["relato"])
        nota_id = pipedrive.crear_nota(deal_id, texto)
        print(f"\nNota #{nota_id} creada en el deal {deal_id}. Ábrelo en Pipedrive para verla.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        listar()
    else:
        probar(int(sys.argv[1]), "--nota" in sys.argv)
