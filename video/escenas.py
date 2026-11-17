"""Guion del video: cada escena = narración (voz Laomedeia) + contenido de la diapositiva.

tipo: portada | puntos | codigo | diagrama | terminal | tabla | cierre
"""

ESCENAS = [
    {
        "id": "01_portada", "tipo": "portada",
        "titulo": "Diagnóstico IA de Pre-Ventas",
        "subtitulo": "Taranis Black · Ruta 1: IA para Ventas · Challenge ONE G11",
        "narracion": (
            "Hola. Este es el anexo técnico de mi Challenge de ONE AI for Business. "
            "Construí, con código propio en Python, la automatización que en el curso se arma en Zapier: "
            "cada negocio nuevo en Pipedrive recibe, en segundos, un diagnóstico de pre-ventas hecho con Gemini. "
            "Te muestro el problema, cómo lo construí y cómo funciona por dentro cada pieza."
        ),
    },
    {
        "id": "02_problema", "tipo": "puntos",
        "titulo": "El problema",
        "puntos": [
            "El equipo B2B pierde más del 40 % de su semana en tareas manuales",
            "20 negocios abiertos en el CRM: USD 4,69 millones",
            "Los 20 llevan más de 30 días sin contacto",
            "9 de 20 están frenados por precio o presupuesto",
            "Notas informales: «Carlos otra vez pidiendo descuento…»",
        ],
        "narracion": (
            "Taranis Black vende sillas, escritorios elevables y cabinas acústicas a empresas. "
            "Según el kit de datos, el equipo comercial pierde más del cuarenta por ciento de su semana llenando el CRM. "
            "Hay veinte negocios abiertos por casi cuatro coma siete millones de dólares, y los veinte llevan más de un mes sin contacto. "
            "Las notas de los vendedores son informales, y nadie las convierte en algo accionable."
        ),
    },
    {
        "id": "03_arquitectura", "tipo": "diagrama",
        "titulo": "Arquitectura",
        "narracion": (
            "Así funciona. El vendedor crea el negocio en Pipedrive. Pipedrive dispara un webhook, "
            "que llega por un túnel seguro de ngrok a mi servicio en FastAPI. "
            "El servicio responde de inmediato, y en segundo plano lee el negocio, la persona, la organización y las notas. "
            "Se los entrega a Gemini con un rol de ingeniero de pre-ventas, y escribe el diagnóstico como una nota fijada en el mismo negocio."
        ),
    },
    {
        "id": "04_prompt", "tipo": "codigo",
        "titulo": "Componente 1 · El rol de sistema",
        "archivo": "app/prompt_sistema.py",
        "codigo": [
            "# ROL",
            "Eres Ingeniero(a) de Pre-Ventas Senior de Taranis Black...",
            "# CONOCIMIENTO (no inventes otros datos)",
            "- ErgoPro Specialist USD 2.490 | SmartDesk Studio USD 3.600",
            "- Flete CIF gratis sobre USD 35.000 · Piloto: 2 puestos x 15 días",
            "# REGLAS",
            "- Las fechas del relato son cosas que YA ocurrieron",
            "- Si falta información, dilo; no la inventes",
            "# SALIDA: Resumen Ejecutivo Técnico",
            "## 🎯 Necesidad  ## ⏱️ Urgencia  ## 📦 Solución",
            "## ⚠️ Riesgos    ## ❓ Faltante  ## ➡️ Próximo paso",
        ],
        "narracion": (
            "El cerebro es el rol de sistema. Le doy a Gemini una misión: convertir relatos confusos en diagnósticos accionables. "
            "Le doy el catálogo y las políticas comerciales reales del kit, para que no invente precios. "
            "Y le fijo siete secciones, siempre en el mismo orden, para que el vendedor sepa dónde mirar."
        ),
    },
    {
        "id": "05_gemini", "tipo": "codigo",
        "titulo": "Componente 2 · Conexión con Gemini",
        "archivo": "app/gemini.py",
        "codigo": [
            "from google import genai",
            "from google.genai import errors, types",
            "",
            "respuesta = cliente.models.generate_content(",
            "    model=config.GEMINI_MODEL,          # gemini-3.6-flash",
            "    contents=mensaje,",
            "    config=types.GenerateContentConfig(",
            "        system_instruction=PROMPT_SISTEMA,",
            "        temperature=0.3))",
            "",
            "except errors.APIError as e:",
            "    if e.code in {429, 500, 502, 503, 504}:",
            "        time.sleep(2 ** intento)   # 2, 4, 8 segundos",
        ],
        "narracion": (
            "La conexión usa el SDK oficial google genai. Temperatura baja, para respuestas consistentes. "
            "Si Google responde cuatrocientos veintinueve, límite de solicitudes, o un error temporal, "
            "el código espera dos, cuatro y ocho segundos, y reintenta. La clave vive en el archivo punto env y nunca se imprime."
        ),
    },
    {
        "id": "06_pipedrive", "tipo": "codigo",
        "titulo": "Componente 3 · Cliente de Pipedrive",
        "archivo": "app/pipedrive.py",
        "codigo": [
            "cabeceras = {'x-api-token': TOKEN}     # nunca en la URL",
            "",
            "GET  /api/v2/deals/{id}               # título, org_id, person_id",
            "GET  /api/v2/organizations/{id}       # nombre de la empresa",
            "GET  /api/v2/persons/{id}             # nombre del contacto",
            "GET  /api/v1/notes?deal_id={id}       # el relato del vendedor",
            "",
            "POST /api/v1/notes",
            "  { deal_id, content: <HTML>, pinned_to_deal_flag: 1 }",
        ],
        "narracion": (
            "El cliente de Pipedrive lo escribí después de leer la documentación oficial. "
            "El token va en un encabezado, no en la dirección, para que no quede en ningún registro. "
            "Leo el negocio con la API versión dos, junto el relato de las notas y de los campos personalizados, "
            "y escribo el diagnóstico convertido a HTML, como nota fijada."
        ),
    },
    {
        "id": "07_webhook", "tipo": "codigo",
        "titulo": "Componente 4 · El webhook (FastAPI)",
        "archivo": "app/main.py",
        "codigo": [
            "@app.post('/webhook/pipedrive')",
            "async def webhook_pipedrive(request, tareas):",
            "    meta = cuerpo['meta']",
            "    if meta['entity'] != 'deal' or meta['action'] != 'create':",
            "        return {'ignorado': ...}        # solo create.deal",
            "    if not _marcar_si_es_nuevo(deal_id):",
            "        return {'duplicado': deal_id}  # reintentos de Pipedrive",
            "    tareas.add_task(procesar_deal, deal_id)",
            "    return {'recibido': deal_id}       # 200 OK en ~170 ms",
        ],
        "narracion": (
            "El webhook tiene un detalle clave que encontré en la documentación: Pipedrive solo espera diez segundos. "
            "Si no recibe respuesta, reintenta. Gemini tarda unos quince. "
            "Por eso respondo en ciento setenta milisegundos y hago el trabajo en segundo plano. "
            "También descarto duplicados, y solo acepto el evento create punto deal, que es el nombre correcto en la versión dos."
        ),
    },
    {
        "id": "08_errores", "tipo": "tabla",
        "titulo": "Manejo de errores — probado",
        "filas": [
            ("Webhook válido", "200 en 174 ms → nota creada"),
            ("Webhook duplicado", "Ignorado"),
            ("Deal sin relato", "Nota: «Diagnóstico no generado»"),
            ("Evento change.deal", "Ignorado"),
            ("JSON roto / sin id", "400 / 422"),
            ("Gemini 429 o 5xx", "Reintento 2-4-8 s"),
        ],
        "narracion": (
            "Y todo esto lo probé con peticiones reales contra un Pipedrive simulado. "
            "Un webhook válido termina en nota. El duplicado se ignora. "
            "Un negocio sin relato no gasta una llamada a la IA: deja una nota pidiendo los datos. "
            "Y los eventos o mensajes inválidos se rechazan sin tumbar el servidor."
        ),
    },
    {
        "id": "09_demo", "tipo": "terminal",
        "titulo": "Modo demo · python demo.py",
        "lineas": [
            "PS> python demo.py",
            "▶ Caso 1042: FinCloud - 80 sillas ErgoPro Specialist",
            "  ✔ Guardado en ejemplos\\resultados\\1042.md",
            "▶ Caso 1043: LogiMax - estaciones monitoreo 24/7",
            "  ✔ Guardado en ejemplos\\resultados\\1043.md",
            "▶ Caso 1045: Vanguarda - 110 puestos para devs",
            "  ✔ Guardado en ejemplos\\resultados\\1045.md",
            "▶ Caso 1050: Atlas Manufatura - informe ABERGO",
            "  ✔ Guardado en ejemplos\\resultados\\1050.md",
            "▶ Caso 1059: Aurora Cosméticos - sede Wellbeing",
            "  ✔ Guardado en ejemplos\\resultados\\1059.md",
            "▶ Caso borde-sin-relato: Hub Criativo",
            "  ✔ Guardado en ejemplos\\resultados\\borde-sin-relato.md",
            "Listo: 6 generados, 0 con error.",
        ],
        "narracion": (
            "Además hay un modo demo que funciona sin Pipedrive. Lee seis casos reales del kit, "
            "uno por cada tipo de objeción y un caso borde, y guarda cada diagnóstico en Markdown."
        ),
    },
    {
        "id": "10_resultado", "tipo": "antes_despues",
        "titulo": "Entrada → Salida",
        "antes": "«Carlos de compras otra vez pidiendo descuento. Son 12 ErgoPro Core + 12 SmartDesk "
                 "Studio, como 65.880. Quiere 25 % de descuento… Ojo: los operadores de rastreo 24/7 "
                 "pasan 10 horas sentados y se van. Pidió contrapropuesta el 16/10.»",
        "despues": [
            "⏱️ Urgencia ALTA · 32 días sin contacto",
            "📦 12 × Core USD 22.680 + 12 × Studio USD 43.200",
            "⚠️ Objeción: Precio (silla de USD 800)",
            "➡️ Piloto de 2 puestos × 15 días + crédito 30/60/90",
        ],
        "narracion": (
            "Mira la diferencia. Entra una nota informal sobre un cliente que pide descuento. "
            "Sale un diagnóstico con prioridad alta, las cuentas exactas del catálogo, la objeción clasificada, "
            "y un próximo paso concreto: ofrecer un piloto en vez de regalar margen. "
            "Detecta además que el negocio lleva treinta y dos días frío."
        ),
    },
    {
        "id": "11_aprendizajes", "tipo": "puntos",
        "titulo": "Cómo se construyó: decisiones verificadas",
        "puntos": [
            "gemini-2.5-flash está obsoleto (redirige desde el 01/12/2026) → modelo configurable",
            "Webhooks v2: el evento es create.deal, no added.deal",
            "Pipedrive espera máx. 10 s → respuesta inmediata + segundo plano",
            "Error detectado en la 1.ª prueba: la IA leía fechas pasadas como plazos",
            "Corrección: la fecha de hoy entra al prompt → «32 días sin contacto»",
        ],
        "narracion": (
            "Lo más valioso fue verificar antes de suponer. "
            "El modelo del curso, gemini dos punto cinco flash, ya está marcado como obsoleto, así que lo dejé configurable. "
            "Y en la primera prueba encontré un error: la IA leía una fecha pasada como si fuera un plazo. "
            "Lo corregí pasándole la fecha de hoy, y ahora detecta los negocios que se enfrían."
        ),
    },
    {
        "id": "12_cierre", "tipo": "cierre",
        "titulo": "La IA propone. El vendedor decide.",
        "puntos": [
            "Supervisión humana en todo lo que llega al cliente",
            "Sin inventar precios: catálogo dentro del prompt",
            "Código, ejemplos y README en el repositorio",
        ],
        "narracion": (
            "La regla de oro: la IA propone y el vendedor decide. Nada llega al cliente sin revisión humana. "
            "El código, los ejemplos y las instrucciones están en el repositorio. Gracias por ver."
        ),
    },
]
