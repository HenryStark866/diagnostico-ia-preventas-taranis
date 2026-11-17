"""Registra (o lista) el webhook en Pipedrive usando la API oficial.

Documentación: POST /api/v1/webhooks  (subscription_url, event_action, event_object,
version 2.0 por defecto, http_auth_user, http_auth_password).

Uso:
    python registrar_webhook.py https://xxxx.ngrok-free.app   # registra create.deal
    python registrar_webhook.py --listar                       # muestra los existentes
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

from app import config, pipedrive  # noqa: E402


def listar() -> None:
    for w in pipedrive._llamar("GET", "/api/v1/webhooks").get("data") or []:
        print(f"  #{w['id']}  {w['event_action']}.{w['event_object']}  -> {w['subscription_url']}"
              f"  (v{w.get('version')}, activo={w.get('is_active')})")


def registrar(url_publica: str) -> None:
    cuerpo = {
        "subscription_url": url_publica.rstrip("/") + "/webhook/pipedrive",
        "event_action": "create",  # en webhooks v2 el evento "nuevo deal" es create.deal
        "event_object": "deal",
        "version": "2.0",
        "name": "Diagnóstico IA Pre-Ventas",
    }
    if config.WEBHOOK_USER:
        cuerpo["http_auth_user"] = config.WEBHOOK_USER
        cuerpo["http_auth_password"] = config.WEBHOOK_PASSWORD
    datos = pipedrive._llamar("POST", "/api/v1/webhooks", json=cuerpo).get("data") or {}
    print(f"Webhook #{datos.get('id')} registrado -> {cuerpo['subscription_url']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    listar() if sys.argv[1] == "--listar" else registrar(sys.argv[1])
