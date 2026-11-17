"""MODO DEMO: genera diagnósticos con Gemini SIN necesitar Pipedrive.

Lee los casos de ejemplos/casos.json, llama a Gemini y guarda un Markdown por caso
en ejemplos/resultados/. Sirve para grabar la demo aunque venza la prueba de Pipedrive.

Uso:
    python demo.py              # todos los casos
    python demo.py 1042 1050    # solo esos casos (por id)
"""
import json
import sys
from datetime import datetime
from pathlib import Path

# En Windows la consola usa cp1252 y se rompe con emojis; forzamos UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

from app import config  # noqa: E402
from app.gemini import ErrorGemini, diagnosticar  # noqa: E402

CARPETA = Path(__file__).parent / "ejemplos"
SALIDA = CARPETA / "resultados"
MIN_CARACTERES = 20  # menos que esto no alcanza para diagnosticar nada


def procesar(caso: dict) -> str:
    """Devuelve el Markdown del caso (diagnóstico o aviso de por qué no se hizo)."""
    relato = (caso.get("relato") or "").strip()
    encabezado = (
        f"# Diagnóstico — {caso['titulo']}\n\n"
        f"- **Organización:** {caso['organizacion']}\n"
        f"- **Contacto:** {caso['persona']}\n"
        f"- **Generado:** {datetime.now():%Y-%m-%d %H:%M} con `{config.GEMINI_MODEL}`\n\n"
        f"### Relato original\n> {relato or '(vacío)'}\n\n---\n\n"
    )
    # Caso borde: sin relato no llamamos a Gemini (no gastamos cuota ni inventamos).
    if len(relato) < MIN_CARACTERES:
        return encabezado + (
            "## ⚠️ Diagnóstico no generado\n"
            "- El negocio no tiene descripción ni notas suficientes.\n"
            "- **Próximo paso:** el vendedor debe registrar la necesidad, cantidades y "
            "plazo del cliente antes de solicitar el diagnóstico.\n"
        )
    return encabezado + diagnosticar(caso["titulo"], caso["organizacion"], caso["persona"], relato)


def main() -> None:
    config.exigir("GEMINI_API_KEY")
    casos = json.loads((CARPETA / "casos.json").read_text(encoding="utf-8"))
    filtro = set(sys.argv[1:])
    if filtro:
        casos = [c for c in casos if c["id"] in filtro]

    SALIDA.mkdir(parents=True, exist_ok=True)
    ok = fallos = 0
    for caso in casos:
        print(f"\n▶ Caso {caso['id']}: {caso['titulo']}")
        try:
            texto = procesar(caso)
        except ErrorGemini as e:
            print(f"  ✖ {e}")
            fallos += 1
            continue  # un caso fallido no detiene los demás
        archivo = SALIDA / f"{caso['id']}.md"
        archivo.write_text(texto, encoding="utf-8")
        print(f"  ✔ Guardado en {archivo.relative_to(Path(__file__).parent)}")
        ok += 1

    print(f"\nListo: {ok} generados, {fallos} con error.")


if __name__ == "__main__":
    main()
