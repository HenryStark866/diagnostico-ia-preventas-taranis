# Informe ejecutivo — Taranis Black · Ruta 1: IA para Ventas y Gestión Comercial

> Borrador para copiar **campo por campo** en tu copia de `Plantilla_Ruta_1_ventas_ES`.
> Los textos entre [corchetes] los completas tú. Cifras tomadas del Mock Kit oficial
> (`01_Catalogo…` y `02_Prospectos_B2B_Comercial.xlsx`). Las estimaciones están marcadas como tales.

---

## 📋 IDENTIFICACIÓN DEL ESTUDIANTE
- **Nombre completo:** Henry Camilo Taborda Galeano
- **Correo electrónico:** [tu correo]
- **Ruta elegida:** [X] Ruta 1 — IA para ventas y gestión comercial

---

## Resumen ejecutivo (máx. 15 líneas — correo a la CEO)

**Asunto:** Cómo recuperar 16 horas por vendedor a la semana y reactivar USD 4,7 M en negociaciones

Estimada CEO:

Analizamos los 20 negocios abiertos del CRM: suman **USD 4,69 M** y **los 20 llevan más de 30 días
sin contacto**. Casi la mitad (9 de 20) está frenada por solo dos objeciones: precio y presupuesto.
Hoy el equipo dedica más del 40 % de su semana a tareas manuales y responde esas objeciones con
argumentos genéricos.

Recomendamos tres iniciativas, en este orden:
1. **Playbook consultivo con IA** (ChatGPT/Gemini): las 5 objeciones del kit con argumentos de valor
   y un "cliente simulado" para entrenar. Bajo esfuerzo, impacto inmediato.
2. **Diagnóstico automático en el CRM** (ya construido y probado): cada negocio nuevo recibe en
   segundos un resumen técnico con prioridad, solución del catálogo y próximo paso.
3. **Secuencias de correo segmentadas** por objeción, generadas con IA y aprobadas por el vendedor.

Impacto esperado a 90 días: **−50 % en tiempo administrativo**, **+5 puntos en tasa de cierre** y
ningún negocio sin contacto por más de 7 días. Todo bajo una política de IA responsable con
supervisión humana y protección de datos de clientes.

---

# 🧭 PARTE 1 — BASE ESTRATÉGICA (RUTA 0)

## Etapa 1 — AI Canvas e identificación de oportunidades

**Casos de uso (mín. 3)**

| # | Caso de uso | Problema que ataca | Dato del kit |
|---|---|---|---|
| 1 | **Diagnóstico automático de negocios en el CRM** | Notas informales que nadie analiza; priorización a ojo | 20 deals con "dolores" y objeciones en texto libre |
| 2 | **Playbook de objeciones + simulador de cliente** | Argumentos débiles ante precio/presupuesto | 9 de 20 deals frenados por Precio o Presupuesto |
| 3 | **Secuencias de nutrición personalizadas** | Correos genéricos y negocios que se enfrían | 5 deals esperando respuesta del cliente; los 20 con último contacto entre el 11 y el 18/10 |
| 4 | Pronóstico de cierre del pipeline (fase 2) | Sin previsibilidad de ingresos | Etapa de embudo y fechas de último contacto |

**Clasificación por tipo de IA**
- Casos 1, 2 y 3 → **IA Generativa**: interpretan lenguaje natural informal y producen texto
  (diagnósticos, argumentos, correos). Las reglas fijas no entienden "Carlos otra vez pidiendo
  descuento".
- Caso 4 → **IA Predictiva**: estima probabilidad de cierre a partir de datos históricos (requiere
  12+ meses de historial, por eso va en fase 2).
- Reglas de negocio (flete CIF > USD 35.000, piloto de 2 puestos, crédito 30/60/90) → **IA
  Tradicional / reglas**: se dan al modelo como conocimiento fijo para que no invente.

**Supervisión humana (Human-in-the-Loop)**
- **Siempre** antes de enviar algo al cliente: descuentos, plazos de entrega y condiciones de pago
  los aprueba el vendedor/gerente (la IA no compromete a la empresa).
- El diagnóstico del CRM es **interno**: se usa sin aprobación, pero el vendedor puede corregirlo.
- Correos: la IA redacta, el vendedor revisa y envía. Nunca envío automático en la fase 1.

## Etapa 2 — Priorización y gestión del cambio

**Matriz Esfuerzo × Impacto** *(pegar imagen de `docs/matriz.png` o esta tabla)*

| Iniciativa | Esfuerzo | Impacto | Cuadrante | Orden |
|---|---|---|---|---|
| Playbook de objeciones + simulador | Bajo | Alto | Victoria rápida | **1** (semana 1–2) |
| Diagnóstico IA en CRM | Medio | Alto | Proyecto estratégico | **2** (semana 2–4; prototipo listo) |
| Secuencias de correo IF/ELSE | Medio | Medio | Planificar | **3** (mes 2) |
| Pronóstico predictivo | Alto | Alto | Largo plazo | **4** (mes 4+) |

**Métricas de éxito** *(estimaciones; validar con la línea base del primer mes)*

| Iniciativa | Métrica | Meta 90 días |
|---|---|---|
| Playbook | Tasa de cierre en deals con objeción Precio/Presupuesto | +5 p.p. |
| Diagnóstico IA | Minutos de calificación por deal | De ~20 a ~5 min |
| Diagnóstico IA | Deals con >7 días sin contacto | 0 |
| Correos | Tasa de respuesta | +30 % vs. correo genérico |
| Adopción | Vendedores que usan las herramientas cada semana | ≥ 80 % |

**ROI estimado (supuestos explícitos):** 10 vendedores × 40 h × 40 % = 160 h/semana en tareas
manuales. Recuperar la mitad = **80 h/semana ≈ 4.000 h/año**. Costo de la solución: API de Gemini
(centavos por diagnóstico) + licencias de IA del equipo. Basta con cerrar **un** negocio más del
pipeline (ticket medio del kit ≈ USD 234.700) para pagar varios años de la solución.

**Plan de gestión del cambio**
1. **Campeones:** 2 vendedores pilotean el playbook y el diagnóstico durante 2 semanas.
2. **Mensaje claro:** "la IA quita el trabajo de oficina, no al vendedor"; el vendedor sigue
   aprobando todo.
3. **Capacitación de 1 h** con casos reales del CRM, no ejemplos genéricos.
4. **Medir y mostrar:** tablero semanal de horas ahorradas y negocios reactivados.
5. **Canal de feedback:** si un diagnóstico está mal, se reporta y se ajusta el prompt.

## Etapa 3 — Gobernanza, ética y cumplimiento

**Política de IA responsable (resumen)**

| ✅ Permitido | ⛔ Prohibido |
|---|---|
| Usar herramientas aprobadas (Gemini API corporativa, ChatGPT Team/Enterprise) | Pegar datos de clientes en cuentas personales/gratuitas de IA |
| Redactar borradores de correos, argumentos y resúmenes | Enviar al cliente texto generado sin revisión humana |
| Analizar notas del CRM para priorizar | Ofrecer descuentos, plazos o condiciones que no estén en la política comercial |
| Usar datos agregados o anonimizados para análisis | Subir bases completas con correos/teléfonos a herramientas no aprobadas |
| | Usar IA para decisiones de crédito sin revisión del comité financiero |

**Riesgos y protección de datos**
- **Normativa:** Taranis Black opera en Brasil (LGPD, Ley 13.709/2018) y Latinoamérica; en
  Colombia aplica la Ley 1581 de 2012 (Habeas Data). Los contactos B2B (nombre, cargo, correo) son
  datos personales.
- **Riesgo de fuga:** datos de clientes en herramientas sin acuerdo de tratamiento → *Mitigación:*
  solo APIs/planes empresariales que no entrenan con los datos; minimizar (el diagnóstico no
  necesita el correo del contacto).
- **Riesgo de alucinación:** la IA inventa precios o plazos → *Mitigación:* catálogo y políticas
  dentro del prompt, regla "si falta información, dilo" y revisión humana.
- **Riesgo de sesgo:** priorizar siempre a empresas grandes o sectores "de moda" → *Mitigación:*
  criterios de urgencia explícitos (riesgo legal, días sin contacto, dolor del cliente) y revisión
  mensual de qué deals se marcan ALTA.

**Comité y auditoría**
- **Comité de IA:** Dirección Comercial (presidente), TI/Seguridad, Jurídico/Protección de datos,
  RR. HH. y un vendedor campeón.
- **Auditoría mensual:** muestra de 10 diagnósticos vs. resultado real; incidentes de datos.
- **Revisión trimestral** de la política y de los proveedores de IA.

---

# 💼 PARTE 2 — ESPECIALIZACIÓN: IA PARA VENTAS

## Etapa 1 — Guía comercial y manejo de objeciones ✅

**Estructura de la guía comercial (venta consultiva Taranis Black)**
1. **Investigar** (antes de llamar): sector, tamaño, quién decide (RR. HH., Instalaciones, Compras,
   EHS) y el dolor registrado.
2. **Diagnosticar el dolor, no el mueble:** ausentismo, LER/lumbalgia, rotación, multas NR-17,
   ruido en open-space.
3. **Cuantificar el costo de no actuar:** días de incapacidad, multas, rotación.
4. **Proponer la solución del catálogo** ligada a ese dolor (ErgoPro, SmartDesk, Silence).
5. **Reducir el riesgo de decidir:** piloto de 2 puestos por 15 días, informe NR-17, garantía 5 años.
6. **Cerrar con un próximo paso con fecha.**

Criterios de calificación: ≥ 30 posiciones (personalización sin costo), dolor documentado, acceso a
quien decide, presupuesto o vía de financiamiento, plazo conocido.

**5 objeciones identificadas y sus argumentos** *(matriz del kit, con deals reales)*

| # | Objeción | Deals del kit | Argumento consultivo | Evidencia |
|---|---|---|---|---|
| 1 | **Precio** — "la competencia es 30 % más barata" | #1043, #1047, #1052, #1055, #1060 | Costo por día de uso: ErgoPro Specialist USD 2.490 ÷ (5 años × 250 días laborales) ≈ **USD 2 por día**; la silla barata dura ~14 meses y no trae informe NR-17 | Garantía 5 años, informe ABERGO, TCO |
| 2 | **Presupuesto congelado** | #1045, #1048, #1053, #1057 | No es gasto discrecional sino mitigación de riesgo y ausentismo; facturación 30/60/90 o cuotas que caben en OPEX | Crédito 30/60/90; ahorro por menos incapacidades |
| 3 | **Proveedor actual** | #1046, #1050, #1054, #1058 | No romper la relación: piloto en el área crítica y comparar resultados | Piloto 2 puestos × 15 días; ergonomistas certificados |
| 4 | **Plazo de entrega** | #1042, #1049, #1056, #1061 | Entrega escalonada desde el CD de Santa Catarina: lote esencial en 7 días hábiles | Stock regulador de modelos de alto giro |
| 5 | **Personalización** | #1044, #1051, #1059 | Ingeniería de aplicación con arquitectos; colores y FSC sin costo desde 30 posiciones; bloques BIM/3D | Biblioteca BIM, muestras en 48 h |

**Prompt de simulación del cliente** *(pegar en ChatGPT o Gemini, en una conversación nueva)*

```
Actúa como Carlos Eduardo Prado, Gerente de Compras de LogiMax Transportes (260 empleados).
Contexto: cotizaste 12 ErgoPro Core + 12 SmartDesk Studio (USD 65.880). Tu presupuesto del semestre
es rígido y viste en un catálogo una silla a USD 800. Tu objetivo es conseguir 25 % de descuento.
Tu dolor real (que no dirás de entrada): los operadores de rastreo 24/7 pasan 10 h sentados y la
rotación es alta.

Reglas:
- Eres escéptico, directo y hablas de precio primero.
- Solo cedes si el vendedor conecta la propuesta con la rotación y el costo total en el tiempo.
- Si ofrece un descuento sin justificación, pide más descuento.
- Respuestas de máximo 3 frases. Nunca salgas del personaje.
- Cuando el vendedor escriba "FIN", sal del personaje y evalúalo de 1 a 10 en: descubrimiento del
  dolor, argumento de valor, manejo de la objeción y cierre con próximo paso. Da 2 mejoras concretas.

Empieza tú: "Mira, ya vi una silla igual por 800 dólares. Si no me bajas 25 %, no hay negocio."
```

**Enlace o captura del entregable:** [pega el enlace compartido de la conversación en ChatGPT/Gemini
usando el prompt de arriba + 1 captura]

## Etapa 2 — Automatización de correos y nutrición de leads 🔓 (opcional)

**Estructura de la secuencia (IF/ELSE)**
```
SI objeción = Precio        → Correo A: TCO y costo por día (día 0), caso de éxito (día 3), oferta de piloto (día 7)
SI objeción = Presupuesto   → Correo B: ROI sobre ausentismo/rotación (día 0), opciones 30/60/90 (día 4)
SI objeción = Proveedor     → Correo C: invitación a piloto de 2 puestos sin compromiso (día 0), checklist NR-17 (día 5)
SI objeción = Plazo         → Correo D: entrega escalonada en 7 días hábiles (mismo día)
SI objeción = Personalización → Correo E: biblioteca BIM + muestras en 48 h (día 0)
SI no hay respuesta en 7 días → Correo de reactivación + alerta al vendedor en el CRM
SI responde                 → Detener secuencia y crear tarea de llamada
```
La objeción la clasifica automáticamente el diagnóstico IA del CRM (campo "Riesgos y objeciones").

**Prompts para asunto y cuerpo**
```
Eres redactor B2B de Taranis Black. Escribe un correo para {nombre}, {cargo} de {empresa}.
Objeción principal: {objecion}. Dolor registrado: {dolor}. Productos cotizados: {productos}.
Reglas: máximo 120 palabras, tono consultivo (no vendedor), un solo llamado a la acción con fecha,
usa solo datos del catálogo y la política comercial; nada de descuentos no aprobados.
Entrega: 3 opciones de asunto (máx. 50 caracteres, sin mayúsculas sostenidas) y el cuerpo.
```

**Ejemplo de correo generado:** [pegar uno generado con el prompt para #1045 Vanguarda]

---

## 📎 ANEXO DE EVIDENCIAS

| Entregable | Descripción | Enlace | Captura | Nota de uso |
|---|---|---|---|---|
| Servicio "Diagnóstico IA de Pre-Ventas" | Webhook Pipedrive → Gemini → nota en el deal (Python/FastAPI) | [GitHub] | Nota en Pipedrive | Se activa solo al crear un deal |
| Modo demo + 6 diagnósticos | Casos del Mock Kit y sus resultados | [GitHub/ejemplos] | Un .md | `python demo.py` |
| Simulador de cliente | Prompt de Carlos (LogiMax) para entrenar objeciones | [enlace ChatGPT] | Conversación | Escribir "FIN" para la evaluación |
| Playbook de objeciones | Tabla de 5 objeciones con argumentos | Este documento | — | Consultar antes de cada llamada |
| Video de demostración | Cómo funciona por dentro | [YouTube no listado] | — | 4–5 min |

## 🎬 VIDEO DE DEMOSTRACIÓN
[enlace]
