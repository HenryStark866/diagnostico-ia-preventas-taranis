"""Llena la plantilla oficial (Plantilla_Ruta_1_ventas_ES.docx) con el informe del Challenge.

Uso:  python docs/llenar_plantilla.py <plantilla.docx> <salida.docx>
Mantiene el diseño de la plantilla: solo reemplaza el texto guía de cada celda.
"""
import sys
from pathlib import Path

import docx
from docx.shared import Cm, Pt, RGBColor

RAIZ = Path(__file__).parent
REPO = "https://github.com/HenryStark866/diagnostico-ia-preventas-taranis"
VIDEO = "https://youtu.be/UsSla74ugck"


def poner(celda, lineas, imagen=None):
    """Reemplaza el contenido de una celda por varias líneas (las que empiezan con '- ' van con viñeta)."""
    if isinstance(lineas, str):
        lineas = [lineas]
    base = celda.paragraphs[0]
    for p in celda.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    for r in base.runs[1:]:
        r._element.getparent().remove(r._element)
    primero = True
    for linea in lineas:
        p = base if primero else celda.add_paragraph()
        if primero and base.runs:
            run = base.runs[0]
            run.text = ""
        else:
            run = p.add_run()
        negrita = linea.startswith("**")
        texto = linea.strip("*")
        if texto.startswith("- "):
            texto = "• " + texto[2:]
        run.text = texto
        run.italic = False
        run.bold = negrita
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x1F, 0x23, 0x2B)
        primero = False
    if imagen:
        celda.add_paragraph().add_run().add_picture(str(imagen), width=Cm(9))


RESUMEN = [
    "Asunto: Cómo recuperar 16 horas por vendedor a la semana y reactivar USD 4,7 M en negociaciones",
    "Estimada CEO:",
    "Analizamos los 20 negocios abiertos del CRM: suman USD 4,69 M y los 20 llevan más de 30 días sin contacto.",
    "Casi la mitad (9 de 20) está frenada por solo dos objeciones: precio y presupuesto.",
    "Hoy el equipo dedica más del 40 % de su semana a tareas manuales y responde esas objeciones con argumentos genéricos.",
    "Recomendamos tres iniciativas, en este orden:",
    "1. Playbook consultivo con IA: las 5 objeciones del kit con argumentos de valor y un cliente simulado para entrenar.",
    "2. Diagnóstico automático en el CRM (ya construido y probado en Pipedrive): cada negocio nuevo recibe en segundos prioridad, solución del catálogo y próximo paso.",
    "3. Secuencias de correo segmentadas por objeción, generadas con IA y aprobadas por el vendedor.",
    "Impacto esperado a 90 días: −50 % en tiempo administrativo, +5 puntos en tasa de cierre y ningún negocio sin contacto por más de 7 días.",
    "Todo bajo una política de IA responsable, con supervisión humana y protección de datos de clientes.",
    "Quedo atento para presentar la demostración en vivo.",
    "Henry Taborda — Consultor de IA para Negocios",
]

CAMPOS = {
    # Ruta 0 · Etapa 1
    (10, 1): [
        "**1. Diagnóstico automático de negocios en el CRM",
        "- Las notas informales de los vendedores se convierten en un diagnóstico (necesidad, urgencia, solución, objeción, próximo paso). Implementado y probado en Pipedrive.",
        "**2. Playbook de objeciones + simulador de cliente",
        "- 9 de 20 negocios del kit están frenados por precio o presupuesto; se entrena la respuesta con un cliente simulado en ChatGPT.",
        "**3. Secuencias de nutrición personalizadas",
        "- Correos por tipo de objeción, redactados por IA y aprobados por el vendedor.",
        "**4. Pronóstico de cierre del pipeline (fase 2)",
        "- Predicción de probabilidad de cierre con el historial del CRM.",
    ],
    (10, 2): [
        "- Casos 1, 2 y 3 → IA Generativa: interpretan lenguaje informal y producen texto (diagnósticos, argumentos, correos).",
        "- Caso 4 → IA Predictiva: requiere 12+ meses de historial de cierres; por eso va en fase 2.",
        "- Reglas de negocio (flete CIF > USD 35.000, piloto de 2 puestos, crédito 30/60/90) → IA Tradicional/reglas: se entregan al modelo como conocimiento fijo para que no invente.",
    ],
    (10, 3): [
        "- Siempre antes de que algo llegue al cliente: descuentos, plazos y condiciones de pago los aprueba el vendedor o gerente.",
        "- El diagnóstico del CRM es interno: se usa sin aprobación, pero el vendedor puede corregirlo.",
        "- Correos: la IA redacta, el vendedor revisa y envía. Nunca envío automático en la fase 1.",
    ],
    # Ruta 0 · Etapa 2
    (11, 1): [
        "- 1.º Playbook de objeciones + simulador — esfuerzo BAJO, impacto ALTO (victoria rápida, semanas 1–2).",
        "- 2.º Diagnóstico IA en el CRM — esfuerzo MEDIO, impacto ALTO (semanas 2–4; prototipo ya funcionando).",
        "- 3.º Secuencias de correo IF/ELSE — esfuerzo MEDIO, impacto MEDIO (mes 2).",
        "- 4.º Pronóstico predictivo — esfuerzo ALTO, impacto ALTO (mes 4 en adelante).",
    ],
    (11, 2): [
        "- Playbook: +5 p.p. en tasa de cierre de negocios con objeción de precio/presupuesto.",
        "- Diagnóstico IA: de ~20 a ~5 minutos de calificación por negocio; 0 negocios con más de 7 días sin contacto.",
        "- Correos: +30 % de tasa de respuesta frente al correo genérico.",
        "- Adopción: ≥ 80 % de vendedores usando las herramientas cada semana.",
        "- ROI (supuestos explícitos): 10 vendedores × 40 h × 40 % = 160 h/semana manuales; recuperar la mitad = ~4.000 h/año. Cerrar un solo negocio más del pipeline (ticket medio del kit ≈ USD 234.700) paga varios años de la solución.",
    ],
    (11, 3): [
        "- Campeones: 2 vendedores pilotean durante 2 semanas.",
        "- Mensaje claro: la IA quita trabajo de oficina, no al vendedor; el vendedor sigue aprobando todo.",
        "- Capacitación de 1 hora con casos reales del CRM.",
        "- Tablero semanal de horas ahorradas y negocios reactivados.",
        "- Canal de feedback: un diagnóstico equivocado se reporta y se ajusta el prompt.",
    ],
    # Ruta 0 · Etapa 3
    (12, 1): [
        "**Permitido:",
        "- Herramientas aprobadas (Gemini API corporativa, ChatGPT Team/Enterprise).",
        "- Borradores de correos, argumentos y resúmenes; análisis de notas del CRM; datos agregados o anonimizados.",
        "**Prohibido:",
        "- Pegar datos de clientes en cuentas personales o gratuitas de IA.",
        "- Enviar al cliente texto generado sin revisión humana.",
        "- Ofrecer descuentos, plazos o condiciones fuera de la política comercial.",
        "- Usar IA para decisiones de crédito sin revisión del comité financiero.",
    ],
    (12, 2): [
        "- Normativa: LGPD (Brasil, Ley 13.709/2018) y, en Colombia, Ley 1581 de 2012 (Habeas Data). Nombre, cargo y correo de contactos B2B son datos personales.",
        "- Fuga de datos → solo APIs/planes empresariales que no entrenan con los datos; minimizar (el diagnóstico no necesita el correo del contacto).",
        "- Alucinación (precios o plazos inventados) → catálogo y políticas dentro del prompt, regla «si falta información, dilo» y revisión humana.",
        "- Sesgo (priorizar solo empresas grandes) → criterios de urgencia explícitos (riesgo legal, días sin contacto, dolor) y revisión mensual de los negocios marcados ALTA.",
    ],
    (12, 3): [
        "- Comité de IA: Dirección Comercial (presidencia), TI/Seguridad, Jurídico/Protección de datos, RR. HH. y un vendedor campeón.",
        "- Auditoría mensual: muestra de 10 diagnósticos frente al resultado real e incidentes de datos.",
        "- Revisión trimestral de la política y de los proveedores de IA.",
    ],
    # Ruta 1 · Etapa 1
    (14, 1): [
        "1. Investigar: sector, tamaño, quién decide (RR. HH., Instalaciones, Compras, EHS) y el dolor registrado.",
        "2. Diagnosticar el dolor, no el mueble: ausentismo, LER/lumbalgia, rotación, multas NR-17, ruido.",
        "3. Cuantificar el costo de no actuar: incapacidades, multas, rotación.",
        "4. Proponer la solución del catálogo ligada a ese dolor (ErgoPro, SmartDesk, Silence).",
        "5. Reducir el riesgo de decidir: piloto de 2 puestos por 15 días, informe NR-17, garantía.",
        "6. Cerrar con un próximo paso con fecha.",
        "Criterios de calificación: ≥ 30 posiciones, dolor documentado, acceso a quien decide, presupuesto o vía de financiación y plazo conocido.",
    ],
    (14, 2): [
        "**1. Precio — «la competencia es 30 % más barata» (#1043, #1047, #1052, #1055, #1060)",
        "- Costo por uso: ErgoPro Specialist USD 2.490 ÷ (5 años × 250 días) ≈ USD 2 por día; la silla barata dura ~14 meses y no trae informe NR-17.",
        "**2. Presupuesto congelado (#1045, #1048, #1053, #1057)",
        "- No es gasto discrecional sino mitigación de riesgo y ausentismo; facturación 30/60/90 que cabe en OPEX.",
        "**3. Proveedor actual (#1046, #1050, #1054, #1058)",
        "- No romper la relación: piloto en el área crítica y comparar resultados.",
        "**4. Plazo de entrega (#1042, #1049, #1056, #1061)",
        "- Entrega escalonada desde el CD de Santa Catarina: lote esencial en 7 días hábiles.",
        "**5. Personalización (#1044, #1051, #1059)",
        "- Ingeniería de aplicación con arquitectos; colores y FSC sin costo desde 30 posiciones; bloques BIM/3D.",
    ],
    (14, 3): [
        "Actúa como Carlos Eduardo Prado, Gerente de Compras de LogiMax Transportes (260 empleados). "
        "Contexto: te cotizaron 12 ErgoPro Core + 12 SmartDesk Studio 140 = USD 65.880. Tu presupuesto del semestre "
        "es rígido y viste una silla a USD 800. Quieres 25 % de descuento pagando de contado. Tu dolor real (que no "
        "dirás de entrada): los operadores de rastreo 24/7 pasan 10 h sentados y la rotación es alta.",
        "Reglas: escéptico y directo; hablas de precio primero; solo cedes si el vendedor conecta la propuesta con la "
        "rotación y el costo total; si te ofrece descuento sin justificación, pides más; máximo 3 frases; nunca sales "
        "del personaje. Cuando el vendedor escriba «FIN», lo evalúas de 1 a 10 en descubrimiento del dolor, argumento "
        "de valor, manejo de la objeción y cierre, con 2 mejoras concretas.",
    ],
    (14, 4): [
        "Simulación completa en ChatGPT (5 turnos). Resultado: el cliente aceptó un piloto sin costo en lugar del 25 % "
        "de descuento, con facturación 30/60/90 y revisión del flete CIF.",
        "Evaluación del simulador: 8/10 (descubrimiento 8, valor 9, objeción 8, cierre 7). Mejora aplicada al playbook: "
        "definir criterios de éxito medibles del piloto antes de instalarlo.",
    ],
    # Ruta 1 · Etapa 2 (opcional)
    (15, 1): [
        "- SI objeción = Precio → Correo A: costo total y costo por día (día 0), caso de éxito (día 3), oferta de piloto (día 7).",
        "- SI objeción = Presupuesto → Correo B: ROI sobre ausentismo y rotación (día 0), opciones 30/60/90 (día 4).",
        "- SI objeción = Proveedor actual → Correo C: piloto de 2 puestos sin compromiso (día 0), checklist NR-17 (día 5).",
        "- SI objeción = Plazo → Correo D: entrega escalonada en 7 días hábiles (mismo día).",
        "- SI objeción = Personalización → Correo E: biblioteca BIM + muestras en 48 h (día 0).",
        "- SI no responde en 7 días → reactivación + alerta al vendedor en el CRM. SI responde → se detiene la secuencia y se crea tarea de llamada.",
        "La objeción la clasifica automáticamente el diagnóstico IA del CRM.",
    ],
    (15, 2): [
        "Eres redactor B2B de Taranis Black. Escribe un correo para {nombre}, {cargo} de {empresa}. Objeción principal: "
        "{objecion}. Dolor registrado: {dolor}. Productos cotizados: {productos}. Reglas: máximo 120 palabras, tono "
        "consultivo, un solo llamado a la acción con fecha, solo datos del catálogo y de la política comercial, nada de "
        "descuentos no aprobados. Entrega 3 opciones de asunto (máx. 50 caracteres) y el cuerpo.",
    ],
    # Correo generado de verdad con Gemini usando el prompt de arriba (caso #1045 Vanguarda).
    (15, 3): ["Generado con Gemini a partir del prompt (caso #1045 Vanguarda):"] + [
        l for l in (RAIZ / "correo_generado.md").read_text(encoding="utf-8").splitlines() if l.strip()],
    (15, 4): [f"Prompt y ejemplo incluidos arriba. Código del proyecto: {REPO}"],
}

EVIDENCIAS = [
    ("Servicio «Diagnóstico IA de Pre-Ventas»", "Webhook Pipedrive → Gemini → nota fijada en el deal (Python/FastAPI)",
     REPO, "Nota real en Pipedrive", "Se activa solo al crear un deal"),
    ("Modo demo + 6 diagnósticos", "Casos del Mock Kit (5 objeciones + caso sin relato) y sus resultados",
     REPO + "/tree/main/ejemplos", "—", "python demo.py"),
    ("Simulador de cliente (ChatGPT)", "Prompt de Carlos (LogiMax) para entrenar objeciones",
     "Captura en Etapa 1", "Evaluación 8/10", "Escribir «FIN» para la evaluación"),
    ("Playbook de objeciones", "5 objeciones del kit con argumentos y evidencias", "Este documento", "—",
     "Consultar antes de cada llamada"),
]


def main(plantilla: str, salida: str) -> None:
    d = docx.Document(plantilla)
    t = d.tables
    poner(t[2].rows[0].cells[1], "Henry Camilo Taborda Galeano")
    poner(t[2].rows[1].cells[1], "[correo]")
    for p in t[3].rows[0].cells[0].paragraphs:
        for r in p.runs:
            if "Ruta 1" in p.text and "[ ]" in r.text:
                r.text = r.text.replace("[ ]", "[X]")
    for i, linea in enumerate(RESUMEN):
        poner(t[7].rows[i].cells[0], linea)
    for (ti, fila), texto in CAMPOS.items():
        imagen = None
        if (ti, fila) == (14, 4):
            imagen = RAIZ / "capturas" / "chatgpt_evaluacion.jpg"
        if (ti, fila) == (15, 4):
            imagen = None
        poner(t[ti].rows[fila].cells[1], texto, imagen)
    for i, fila in enumerate(EVIDENCIAS, start=1):
        for j, valor in enumerate(fila):
            poner(t[18].rows[i].cells[j], valor)
    poner(t[18].rows[1].cells[3], "Nota real en Pipedrive", RAIZ / "capturas" / "pipedrive_nota.jpg")
    poner(t[21].rows[0].cells[1], VIDEO)
    d.save(salida)
    print("Guardado:", salida)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
