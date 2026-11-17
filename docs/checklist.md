# ✅ Lista de verificación final — Challenge Taranis Black (Ruta 1)

Fuente de requisitos: curso «Entrega del Challenge Taranis Black» (video de Eric Monné, mapa del
Challenge, `Plantilla_Ruta_1_ventas_ES` y actividad de entrega). Plazo oficial: **29/11/2026**.

## Formato de entrega
| Requisito | Estado | Dónde |
|---|---|---|
| Copia propia de la plantilla de Ruta 1 en Google Docs | ⬜ Henry | Archivo → Hacer una copia |
| Permiso «Cualquier persona con el enlace — Lector» | ⬜ Henry | Compartir |
| Solo enlace de Google Docs/Drive en la actividad (5 intentos) | ⬜ Henry | Actividad «Entrega del Proyecto» |
| Identificación del estudiante y ruta marcada | 🟡 borrador | `docs/informe_taranis_black.md` |
| Resumen ejecutivo ≤ 15 líneas, tono para la CEO | ✅ borrador | informe |

## Parte 1 — Ruta 0 (obligatoria)
| Requisito | Estado |
|---|---|
| Etapa 1: ≥ 3 casos de uso | ✅ 4 casos |
| Etapa 1: clasificación Generativa/Predictiva/Tradicional justificada | ✅ |
| Etapa 1: supervisión humana (HITL) | ✅ |
| Etapa 2: matriz Esfuerzo × Impacto con orden | ✅ tabla (falta imagen opcional) |
| Etapa 2: métricas (ROI, horas, adopción) | ✅ con supuestos explícitos |
| Etapa 2: plan de gestión del cambio | ✅ |
| Etapa 3: política (permitido / prohibido) | ✅ |
| Etapa 3: riesgos de sesgo y protección de datos del país | ✅ LGPD + Ley 1581 |
| Etapa 3: comité y frecuencia de auditoría | ✅ |

## Parte 2 — Ruta 1 Ventas
| Requisito | Estado |
|---|---|
| Etapa 1: estructura de la guía comercial | ✅ |
| Etapa 1: 5 objeciones + argumentos/prompts | ✅ con deals reales del kit |
| Etapa 1: prompt de simulación del cliente | ✅ |
| Etapa 1: **enlace o captura de la conversación en ChatGPT** | ⬜ Henry (debe salir de su cuenta) |
| Etapa 2 (opcional): secuencia IF/ELSE | ✅ |
| Etapa 2 (opcional): prompts asunto/cuerpo | ✅ |
| Etapa 2 (opcional): ejemplo de correo generado | ⬜ generar y pegar |

## Anexo y extras
| Requisito | Estado |
|---|---|
| Anexo de evidencias con enlaces accesibles | 🟡 falta subir el código a GitHub y poner enlaces |
| Video opcional (≤ 5 min; YouTube no listado/Loom/Drive) | 🟡 generado en `video/`; falta subirlo |
| Usar datos del Mock Kit | ✅ catálogo + 20 prospectos + matriz de objeciones |

## Anexo técnico (código)
| Requisito propio | Estado |
|---|---|
| Webhook FastAPI `create.deal` | ✅ probado contra Pipedrive simulado |
| Gemini con rol de Pre-Ventas y secciones fijas | ✅ probado con Gemini real |
| Nota en el deal vía API | ✅ simulado · ⬜ cuenta real (faltan credenciales en `.env`) |
| Modo demo con JSON → Markdown | ✅ 6 casos |
| Errores: sin descripción, Gemini, 429, duplicado | ✅ |
| `.env.example`, `.env` en `.gitignore`, claves nunca impresas | ✅ |
| README con Mermaid, ejecución, ejemplos, mejoras | ✅ |
| Exposición con ngrok y registro del webhook | ✅ documentado · ⬜ probado en vivo |
