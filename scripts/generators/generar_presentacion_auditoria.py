"""
Genera la presentación PowerPoint — Auditoría de Calidad y Exposición
Proyecto ACADEMIX — SENA ADSO Ficha 3173430
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

AZUL_SENA      = RGBColor(0x00, 0x4A, 0x97)
VERDE_SENA     = RGBColor(0x00, 0x90, 0x00)
GRIS_OSCURO    = RGBColor(0x2D, 0x2D, 0x2D)
BLANCO         = RGBColor(0xFF, 0xFF, 0xFF)
AMARILLO       = RGBColor(0xFF, 0xC1, 0x07)
ROJO_ALERTA    = RGBColor(0xDC, 0x35, 0x45)
VERDE_OK       = RGBColor(0x19, 0x87, 0x54)
GRIS_CLARO     = RGBColor(0xF0, 0xF4, 0xF8)
AZUL_CLARO     = RGBColor(0xE8, 0xF1, 0xFB)
NARANJA        = RGBColor(0xE6, 0x5C, 0x00)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height, font_size=18, bold=False, color=GRIS_OSCURO, align=PP_ALIGN.LEFT, wrap=True):
    txb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txb

def slide_header(slide, title, subtitle=None, accent=AZUL_SENA):
    add_rect(slide, 0, 0, 13.33, 1.15, accent)
    add_text(slide, title, 0.3, 0.08, 11.5, 0.7, font_size=28, bold=True, color=BLANCO)
    if subtitle:
        add_text(slide, subtitle, 0.3, 0.72, 11.5, 0.4, font_size=14, color=RGBColor(0xCC, 0xE0, 0xFF))

def slide_footer(slide, slide_num, total=10):
    add_rect(slide, 0, 7.15, 13.33, 0.35, AZUL_SENA)
    add_text(slide, "ACADEMIX · Auditoría de Calidad · SENA ADSO Ficha 3173430", 0.3, 7.17, 9, 0.28, font_size=9, color=BLANCO)
    add_text(slide, f"{slide_num} / {total}", 12.5, 7.17, 0.8, 0.28, font_size=9, color=BLANCO, align=PP_ALIGN.RIGHT)

def simple_table(slide, headers, rows, left, top, col_widths, row_height=0.45, header_fill=AZUL_SENA, alt_fill=AZUL_CLARO, font_size=10.5):
    x = left
    for i, h in enumerate(headers):
        add_rect(slide, x, top, col_widths[i], row_height, header_fill)
        add_text(slide, h, x+0.05, top+0.05, col_widths[i]-0.1, row_height-0.08, font_size=font_size+0.5, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
        x += col_widths[i]
    for r_idx, row in enumerate(rows):
        y = top + row_height * (r_idx + 1)
        fill = alt_fill if r_idx % 2 == 0 else BLANCO
        x = left
        for i, cell in enumerate(row):
            add_rect(slide, x, y, col_widths[i], row_height, fill, line_color=RGBColor(0xCC,0xCC,0xCC))
            add_text(slide, str(cell), x+0.05, y+0.04, col_widths[i]-0.1, row_height-0.06, font_size=font_size, color=GRIS_OSCURO, align=PP_ALIGN.CENTER)
            x += col_widths[i]

# D1 - Portada Auditoria
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, AZUL_SENA)
add_rect(sl, 0, 4.5, 13.33, 3.0, GRIS_OSCURO)
add_rect(sl, 0.4, 0.3, 12.5, 0.08, AMARILLO)
add_text(sl, "SENA · Centro de Servicios Empresariales y Turismo · ADSO", 0.5, 0.5, 12.3, 0.5, font_size=13, color=AMARILLO, align=PP_ALIGN.CENTER)
add_text(sl, "PROCESO DE AUDITORÍA DE CALIDAD", 0.5, 1.15, 12.3, 0.9, font_size=40, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Y GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE", 0.5, 1.95, 12.3, 0.75, font_size=28, bold=True, color=AMARILLO, align=PP_ALIGN.CENTER)
add_text(sl, "Informe Final de Auditoría y Dictamen de Calidad — Proyecto ACADEMIX", 0.5, 2.85, 12.3, 0.55, font_size=16, color=RGBColor(0xCC,0xE4,0xFF), align=PP_ALIGN.CENTER)
add_rect(sl, 1.5, 3.55, 10.3, 0.06, AMARILLO)
add_text(sl, "Módulo Auditado: apps.accounts (Autenticación, RBAC y Recuperación de Credenciales)", 0.5, 3.75, 12.3, 0.4, font_size=13, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Ficha 3173430 · Exposición previa a la Auditoría Externa del Instructor", 0.5, 4.65, 12.3, 0.4, font_size=14, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Equipo de Auditoría Interna · Noviembre 2026", 0.5, 5.15, 12.3, 0.4, font_size=13, color=RGBColor(0xCC,0xCC,0xCC), align=PP_ALIGN.CENTER)

# D2 - Marco Metodologico
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Marco Metodológico de la Auditoría", "Normas internacionales y regulación nacional aplicadas")
slide_footer(sl, 2)
cards = [
    ("ISO/IEC 25010:2023", "Calidad del Producto", "Evaluación de 4 características:\nFiabilidad, Seguridad, Usabilidad y Mantenibilidad con métricas cuantitativas.", AZUL_SENA),
    ("IEEE 730-2014 (SQA)", "Aseguramiento de Calidad", "Revisión formal de procesos preventivos, cobertura de tests, checklist de inspección y trazabilidad.", VERDE_SENA),
    ("IEEE 828-2012 (SCM)", "Gestión de Configuración", "Verificación de línea base v2.5.0-baseline, control de ramas GitFlow y Formatos de Solicitud de Cambio.", NARANJA),
    ("Regulación Colombiana", "MinTIC & Habeas Data", "Ley 1581/2012 (datos de menores), Res. 1519/2020 (accesibilidad WCAG 2.1 AA) y Circular 002 SIC.", RGBColor(0x6A,0x1B,0x9A))
]
for i, (title, sub, desc, col) in enumerate(cards):
    x = 0.4 + i * 3.15
    add_rect(sl, x, 1.5, 2.95, 4.8, AZUL_CLARO, line_color=col)
    add_rect(sl, x, 1.5, 2.95, 0.8, col)
    add_text(sl, title, x+0.1, 1.55, 2.75, 0.4, font_size=12, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, sub, x+0.1, 1.95, 2.75, 0.3, font_size=10, color=RGBColor(0xEE,0xEE,0xEE), align=PP_ALIGN.CENTER)
    add_text(sl, desc, x+0.15, 2.5, 2.65, 3.6, font_size=11, color=GRIS_OSCURO)

# D3 - Matriz de Evaluación ISO 25010
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Matriz de Evaluación de Calidad (ISO/IEC 25010)", "Resultados cuantitativos obtenidos sobre el módulo apps.accounts")
slide_footer(sl, 3)
h = ["Característica", "Métrica / Prueba", "Esperado", "Obtenido", "Estado"]
rows = [
    ["Fiabilidad", "Disponibilidad del servidor en Render", "≥ 99.0%", "99.1% uptime mensual", "✅ Cumple"],
    ["Seguridad", "Algoritmo de Hash para contraseñas", "Argon2id / PBKDF2 (100%)", "100% usuarios hasheados", "✅ Cumple"],
    ["Seguridad", "Rate Limiting en endpoint de Login", "≤ 5 intentos fallidos / 15m", "Sin límite (ilimitado)", "🔴 Brecha (HAL-01)"],
    ["Usabilidad", "Mensajes accesibles ARIA WCAG 2.1", "100% alerts con aria-live", "40% alerts accesibles", "⚠️ Brecha (HAL-02)"],
    ["Mantenibilidad", "Acoplamiento y tamaño de vistas", "≤ 200 líneas / vista", "views.py > 1 000 líneas", "⚠️ Mejora (HAL-04)"]
]
simple_table(sl, h, rows, 0.35, 1.35, [2.4, 3.4, 2.5, 2.6, 2.0], row_height=0.9, font_size=11)

# D4 - Resumen de Hallazgos
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Resumen Ejecutivo de Hallazgos de Auditoría", "4 hallazgos detectados: 1 No Conformidad Mayor, 2 Menores, 1 Observación de Mejora")
slide_footer(sl, 4)
h2 = ["ID", "Tipo", "Descripción del Hallazgo", "Norma Afectada", "Nivel Riesgo"]
rows2 = [
    ["HAL-01", "NC Mayor", "Ausencia de Rate Limiting en endpoint de Login", "ISO 25010 (Seguridad) · OWASP A07", "CRÍTICO"],
    ["HAL-02", "NC Menor", "Falta de atributos ARIA role='alert' en errores", "ISO 25010 (Usabilidad) · Res. 1519 MinTIC", "MEDIO"],
    ["HAL-03", "NC Menor", "Cierre estricto de períodos académicos no forzado", "ISO 25010 (Integridad de datos)", "MEDIO"],
    ["HAL-04", "Obs. Mejora", "Alto acoplamiento en accounts/views.py (Fat View)", "ISO 25010 (Mantenibilidad / Modularidad)", "BAJO"]
]
simple_table(sl, h2, rows2, 0.35, 1.35, [1.3, 1.8, 4.8, 3.3, 1.7], row_height=1.05, font_size=11)

# D5 - Plan de Accion CAPA
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Plan de Acción Correctiva y Preventiva (CAPA)", "Mitigación y cierre de los hallazgos encontrados")
slide_footer(sl, 5)
h3 = ["Hallazgo", "Acción Correctiva (CAPA)", "Mecanismo de Verificación", "Plazo"]
rows3 = [
    ["HAL-01 (Rate Limit)", "Integrar django-ratelimit (5 intentos / 15 min por IP)", "Test de estrés automatizado + HTTP 429", "Inmediato (Sprint 4)"],
    ["HAL-02 (ARIA / MinTIC)", "Refactorizar login.html agregando role='alert' y aria-live", "Auditoría Lighthouse Accessibility = 100", "3 días (Sprint 4)"],
    ["HAL-03 (Bloqueo Notas)", "Middleware que valide periodo_cerrado antes de POST", "Intento de edición con período cerrado bloqueado", "Sprint 5"],
    ["HAL-04 (Fat Views)", "Desacoplar vistas en módulos AuthService y ProfileService", "Análisis con Radon / Complejidad ciclomática < 10", "Sprint 5"]
]
simple_table(sl, h3, rows3, 0.35, 1.35, [2.2, 4.3, 4.4, 2.0], row_height=1.1, font_size=11)

# D6 - Simulacion SCM
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Gestión de Configuración: Simulación de Cambio", "Formato CR-ACAD-2026-005 aplicado al repositorio Git")
slide_footer(sl, 6)
add_rect(sl, 0.4, 1.35, 6.1, 5.4, AZUL_CLARO, line_color=AZUL_SENA)
add_text(sl, "📄 Solicitud de Cambio (CR-ACAD-2026-005)", 0.6, 1.45, 5.7, 0.4, font_size=12, bold=True, color=AZUL_SENA)
cr_info = [
    "• ID: CR-ACAD-2026-005",
    "• Título: Rate Limiting & Accesibilidad ARIA en Login",
    "• Justificación: Corregir hallazgos HAL-01 y HAL-02",
    "• Impacto Técnico: apps/accounts/views.py y login.html",
    "• Nivel de Riesgo: Medio (afecta endpoint de acceso)",
    "• Solicitante: Equipo de Auditoría Interna",
    "• Aprobación: APROBADO por Comité de Control de Cambios (CCB)"
]
for i, line in enumerate(cr_info):
    add_text(sl, line, 0.6, 1.95 + i*0.42, 5.7, 0.38, font_size=11, color=GRIS_OSCURO)

add_rect(sl, 6.8, 1.35, 6.1, 5.4, RGBColor(0xE8,0xF5,0xE9), line_color=VERDE_SENA)
add_text(sl, "🌿 Trazabilidad Git & Pull Request #143", 7.0, 1.45, 5.7, 0.4, font_size=12, bold=True, color=VERDE_SENA)
git_info = [
    "• Línea Base Inicial: v2.5.0-baseline (commit d97d7a6)",
    "• Rama Creada: feature/CR-005-login-ratelimit-aria",
    "• Pull Request: PR #143 hacia rama 'main'",
    "• Checklist de Código: 16 de 16 ítems verificados",
    "• Code Review: Aprobado por revisor independiente",
    "• Merge: Squash & Merge sin conflictos",
    "• Nueva Línea Base: v2.5.1-baseline (commit f4b82e1)"
]
for i, line in enumerate(git_info):
    add_text(sl, line, 7.0, 1.95 + i*0.42, 5.7, 0.38, font_size=11, color=GRIS_OSCURO)

# D7 - Checklist de Codigo
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Checklist de Verificación de Código (Code Review)", "Estándares evaluados obligatoriamente antes de cada Merge a main")
slide_footer(sl, 7)
h4 = ["Categoría", "Criterio Evaluado", "Estándar / Regla", "Resultado"]
rows4 = [
    ["Naming Conventions", "Nombres de funciones, variables y modelos", "PEP 8 · Clases PascalCase, funciones snake_case", "✅ APROBADO"],
    ["Manejo de Excepciones", "Bloques try/except sin 'except Exception: pass'", "Captura explícita de IntegrityError y ValidationError", "✅ APROBADO"],
    ["Seguridad", "Protección contra inyección SQL y XSS", "Django ORM parametrizado + CSRF Token en formularios", "✅ APROBADO"],
    ["Modularidad", "Separación de responsabilidades MVT", "Lógica de negocio en modelos/servicios, templates limpios", "⚠️ CON OBSERVACIÓN"],
    ["Accesibilidad Web", "Etiquetas form-label con 'for' y mensajes ARIA", "WCAG 2.1 AA · Res. 1519/2020 MinTIC", "✅ SUBSANADO (CR-005)"]
]
simple_table(sl, h4, rows4, 0.35, 1.35, [2.5, 3.8, 4.3, 2.0], row_height=1.0, font_size=11)

# D8 - Demostracion Practica
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Demostración Práctica en Vivo", "Puntos a proyectar al Instructor durante la exposición")
slide_footer(sl, 8)
demo_boxes = [
    ("1. Repositorio y Ramas Git", "Demostrar en vivo el comando 'git log --oneline --graph' mostrando la rama feature, el PR #143 y los tags v2.5.0-baseline y v2.5.1-baseline.", AZUL_SENA),
    ("2. Formato de Solicitud de Cambio", "Exhibir el artefacto CR-ACAD-2026-005 diligenciado con su matriz de impacto, riesgo y la firma de aprobación del Tech Lead (CCB).", VERDE_SENA),
    ("3. Checklist de Inspección Diligenciado", "Mostrar la lista de chequeo de 16 puntos marcada y firmada por el revisor previa al Merge en GitHub.", NARANJA),
    ("4. Sistema en Ejecución en Render / Local", "Ejecutar inicio de sesión con credenciales institucionales seguras y demostrar los logs de auditoría en apps.audit.", RGBColor(0x6A,0x1B,0x9A))
]
for i, (title, desc, col) in enumerate(demo_boxes):
    x = 0.5 + (i % 2) * 6.3
    y = 1.5 + (i // 2) * 2.6
    add_rect(sl, x, y, 6.0, 2.3, AZUL_CLARO, line_color=col)
    add_rect(sl, x, y, 6.0, 0.55, col)
    add_text(sl, title, x+0.15, y+0.07, 5.7, 0.4, font_size=12, bold=True, color=BLANCO)
    add_text(sl, desc, x+0.2, y+0.7, 5.6, 1.45, font_size=11.5, color=GRIS_OSCURO)

# D9 - Dictamen Final de Auditoria
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Dictamen Final de Auditoría Interna", "Conclusión general sobre la calidad y madurez del sistema")
slide_footer(sl, 9)
add_rect(sl, 0.6, 1.4, 12.1, 1.6, RGBColor(0xE8,0xF5,0xE9), line_color=VERDE_SENA)
add_text(sl, "DICTAMEN: CONFORME CON CONDICIONES DE MEJORA", 0.8, 1.55, 11.7, 0.5, font_size=20, bold=True, color=VERDE_SENA, align=PP_ALIGN.CENTER)
add_text(sl, "El sistema ACADEMIX satisface los requisitos esenciales de Adecuación Funcional, Cifrado de Datos y Control de Acceso por Roles. "
         "Las no conformidades detectadas cuentan con planes de acción correctiva (CAPA) y su mitigación está en marcha.",
         0.8, 2.15, 11.7, 0.7, font_size=12, color=GRIS_OSCURO, align=PP_ALIGN.CENTER)

dict_cards = [
    ("Nivel de Cumplimiento ISO 25010", "85% de conformidad global sobre las 4 características seleccionadas.", AZUL_SENA),
    ("Nivel de Madurez CMMI-DEV", "Nivel 2 (Gestionado) consolidado, con procesos de SCM e inspección activos.", VERDE_SENA),
    ("Estado para Auditoría Externa", "LISTOS Y PREPARADOS para la evaluación del Instructor del SENA.", NARANJA)
]
for i, (title, desc, col) in enumerate(dict_cards):
    x = 0.6 + i * 4.1
    add_rect(sl, x, 3.4, 3.9, 3.3, AZUL_CLARO, line_color=col)
    add_rect(sl, x, 3.4, 3.9, 0.6, col)
    add_text(sl, title, x+0.1, 3.48, 3.7, 0.45, font_size=11.5, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, desc, x+0.2, 4.3, 3.5, 2.0, font_size=12, color=GRIS_OSCURO, align=PP_ALIGN.CENTER)

# D10 - Preguntas y Apertura
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, AZUL_SENA)
add_rect(sl, 0, 4.2, 13.33, 3.3, GRIS_OSCURO)
add_rect(sl, 0.4, 3.2, 12.5, 0.08, AMARILLO)
add_text(sl, "¿PREGUNTAS DEL INSTRUCTOR?", 0.5, 1.0, 12.3, 1.2, font_size=50, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "El equipo de desarrollo y aseguramiento de calidad de ACADEMIX queda a su entera disposición.", 0.5, 2.3, 12.3, 0.55, font_size=16, color=AMARILLO, align=PP_ALIGN.CENTER)

add_text(sl, "Artefactos Disponibles para Revisión Inmediata:", 0.5, 4.4, 12.3, 0.4, font_size=13, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
arts = [
    "1. Informe Final de Auditoría Completo (DOCX / MD)",
    "2. Matriz de Evaluación ISO 25010 Cuantitativa",
    "3. Formato de Solicitud de Cambio CR-ACAD-2026-005",
    "4. Checklist de Inspección de Código Pre-Merge",
    "5. Trazabilidad en Repositorio Git y Pull Requests"
]
for i, art in enumerate(arts):
    add_text(sl, art, 1.0, 4.85 + i*0.4, 11.3, 0.35, font_size=11, color=RGBColor(0xCC,0xE4,0xFF))

output2 = r"C:\Academix\docs\PRESENTACION_AUDITORIA_PROCESO_CALIDAD.pptx"
prs.save(output2)
print(f"[OK] Presentacion guardada en: {output2}")

