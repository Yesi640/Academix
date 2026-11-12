"""
Genera la presentación PowerPoint — Fase 1 Marco Conceptual
ISO/IEC 25010 · IEEE 730 · IEEE 828 · CMMI · Normativa Colombiana
Proyecto ACADEMIX — SENA ADSO Ficha 3173430
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Paleta de colores ──────────────────────────────────────────────────────────
AZUL_SENA      = RGBColor(0x00, 0x4A, 0x97)   # Azul SENA
VERDE_SENA     = RGBColor(0x00, 0x90, 0x00)   # Verde SENA
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

BLANK = prs.slide_layouts[6]  # Diapositiva en blanco

# ── Helpers ────────────────────────────────────────────────────────────────────

def add_rect(slide, left, top, width, height, fill_color, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=GRIS_OSCURO,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
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
    run.font.italic = italic
    run.font.color.rgb = color
    return txb

def add_textbox_multiline(slide, lines, left, top, width, height,
                          font_size=14, color=GRIS_OSCURO, bold_first=False):
    """lines = list of (text, bold, color_override)"""
    txb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, str):
            text, bold, col = item, False, color
        else:
            text = item[0]
            bold = item[1] if len(item) > 1 else False
            col  = item[2] if len(item) > 2 else color

        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = col
    return txb

def slide_header(slide, title, subtitle=None, accent=AZUL_SENA):
    """Banda superior estilo corporativo"""
    add_rect(slide, 0, 0, 13.33, 1.15, accent)
    add_text(slide, title, 0.3, 0.08, 11.5, 0.7,
             font_size=28, bold=True, color=BLANCO, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.3, 0.72, 11.5, 0.4,
                 font_size=14, bold=False, color=RGBColor(0xCC, 0xE0, 0xFF),
                 align=PP_ALIGN.LEFT)

def slide_footer(slide, slide_num, total=12):
    add_rect(slide, 0, 7.15, 13.33, 0.35, AZUL_SENA)
    add_text(slide, "ACADEMIX · SENA ADSO · Ficha 3173430", 0.3, 7.17, 9, 0.28,
             font_size=9, color=BLANCO)
    add_text(slide, f"{slide_num} / {total}", 12.5, 7.17, 0.8, 0.28,
             font_size=9, color=BLANCO, align=PP_ALIGN.RIGHT)

def simple_table(slide, headers, rows, left, top, col_widths, row_height=0.38,
                 header_fill=AZUL_SENA, alt_fill=AZUL_CLARO,
                 font_size=11, header_font_size=11):
    total_w = sum(col_widths)
    total_h = row_height * (len(rows) + 1)
    # header
    x = left
    for i, h in enumerate(headers):
        add_rect(slide, x, top, col_widths[i], row_height, header_fill)
        add_text(slide, h, x+0.05, top+0.04, col_widths[i]-0.1, row_height-0.06,
                 font_size=header_font_size, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
        x += col_widths[i]
    # rows
    for r_idx, row in enumerate(rows):
        y = top + row_height * (r_idx + 1)
        fill = alt_fill if r_idx % 2 == 0 else BLANCO
        x = left
        for i, cell in enumerate(row):
            add_rect(slide, x, y, col_widths[i], row_height, fill,
                     line_color=RGBColor(0xCC,0xCC,0xCC))
            add_text(slide, str(cell), x+0.05, y+0.03, col_widths[i]-0.1, row_height-0.05,
                     font_size=font_size, color=GRIS_OSCURO, align=PP_ALIGN.CENTER)
            x += col_widths[i]

def icon_card(slide, left, top, width, height, icon, label, sublabel, fill=AZUL_CLARO):
    add_rect(slide, left, top, width, height, fill, line_color=AZUL_SENA,
             line_width=Pt(1.5).emu if hasattr(Pt(1), 'emu') else 19050)
    add_text(slide, icon, left, top+0.05, width, 0.55,
             font_size=28, bold=True, color=AZUL_SENA, align=PP_ALIGN.CENTER)
    add_text(slide, label, left, top+0.6, width, 0.38,
             font_size=12, bold=True, color=AZUL_SENA, align=PP_ALIGN.CENTER)
    add_text(slide, sublabel, left, top+0.95, width, 0.5,
             font_size=9.5, color=GRIS_OSCURO, align=PP_ALIGN.CENTER, wrap=True)

# ══════════════════════════════════════════════════════════════════════════════
# D1 — PORTADA
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, AZUL_SENA)
add_rect(sl, 0, 4.5, 13.33, 3.0, GRIS_OSCURO)

add_rect(sl, 0.4, 0.3, 12.5, 0.08, AMARILLO)   # línea decorativa

add_text(sl, "SENA · Centro de Servicios Empresariales y Turismo",
         0.5, 0.5, 12.0, 0.5, font_size=13, color=AMARILLO, align=PP_ALIGN.CENTER)

add_text(sl, "MARCO NORMATIVO DE CALIDAD", 0.5, 1.15, 12.3, 0.9,
         font_size=42, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Y GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE", 0.5, 1.95, 12.3, 0.75,
         font_size=30, bold=True, color=AMARILLO, align=PP_ALIGN.CENTER)

add_text(sl, "ISO/IEC 25010  ·  IEEE 730  ·  IEEE 828  ·  CMMI-DEV",
         0.5, 2.85, 12.3, 0.55, font_size=16, color=RGBColor(0xCC,0xE4,0xFF), align=PP_ALIGN.CENTER)

add_rect(sl, 1.5, 3.55, 10.3, 0.06, AMARILLO)

add_text(sl, "Proyecto Formativo:", 0.5, 3.75, 2.8, 0.4,
         font_size=12, color=RGBColor(0xAA,0xCC,0xFF), align=PP_ALIGN.RIGHT)
add_text(sl, "ACADEMIX — Plataforma de Gestión Escolar (Django 5.x)",
         3.4, 3.75, 9.4, 0.4, font_size=13, bold=True, color=BLANCO)

add_text(sl, "Programa ADSO — Ficha 3173430", 0.5, 4.62, 12.3, 0.45,
         font_size=15, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Investigación Fase 1 — Marco Conceptual", 0.5, 5.05, 12.3, 0.4,
         font_size=13, color=RGBColor(0xCC,0xCC,0xCC), align=PP_ALIGN.CENTER)
add_text(sl, "Noviembre 2026", 0.5, 5.5, 12.3, 0.4,
         font_size=13, color=RGBColor(0xCC,0xCC,0xCC), align=PP_ALIGN.CENTER)

add_rect(sl, 0, 7.15, 13.33, 0.35, RGBColor(0x00,0x30,0x60))
add_text(sl, "ACADEMIX · SENA ADSO · Ficha 3173430", 0.3, 7.17, 12.7, 0.28,
         font_size=9, color=RGBColor(0x99,0xBB,0xFF), align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# D2 — ¿Qué es ISO/IEC 25010 y SQuaRE?
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "¿Qué es ISO/IEC 25010 y SQuaRE?",
             "La familia de normas para Requisitos y Evaluación de Calidad de Software")
slide_footer(sl, 2)

add_text(sl, "La familia SQuaRE (Systems & Software Quality Requirements and Evaluation)",
         0.4, 1.25, 12.5, 0.4, font_size=13, bold=True, color=AZUL_SENA)

divs = [
    ("25000–25010", "Gestión\nde Calidad", AZUL_SENA),
    ("25020–25030", "Requisitos\nde Calidad", VERDE_SENA),
    ("25040–25050", "Evaluación\nde Calidad", NARANJA),
    ("25010", "Modelo\nde Calidad ★", RGBColor(0x6A,0x1B,0x9A)),
    ("25060+", "Herramientas\nde Evaluación", RGBColor(0x01,0x57,0x9B)),
]
for i, (num, lbl, col) in enumerate(divs):
    x = 0.35 + i * 2.52
    add_rect(sl, x, 1.72, 2.35, 1.2, col)
    add_text(sl, num, x, 1.74, 2.35, 0.45, font_size=11, bold=True,
             color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, lbl, x, 2.15, 2.35, 0.7, font_size=12, bold=True,
             color=BLANCO, align=PP_ALIGN.CENTER)

add_rect(sl, 0.4, 3.1, 12.5, 0.06, AZUL_SENA)

# Línea de tiempo
add_text(sl, "Evolución:", 0.4, 3.25, 1.5, 0.35, font_size=12, bold=True, color=AZUL_SENA)
timeline = [
    ("ISO 9126\n2001", RGBColor(0x90,0xA4,0xAE)),
    ("ISO/IEC 25010\n2011 — 8 características", AZUL_SENA),
    ("ISO/IEC 25010\n2023 — Ajustes WCAG", VERDE_SENA),
]
for i, (lbl, col) in enumerate(timeline):
    x = 1.9 + i * 3.7
    add_rect(sl, x, 3.22, 3.3, 0.85, col)
    add_text(sl, lbl, x, 3.25, 3.3, 0.8, font_size=12, bold=True,
             color=BLANCO, align=PP_ALIGN.CENTER)
    if i < 2:
        add_text(sl, "→", x+3.3, 3.42, 0.4, 0.4, font_size=22, bold=True,
                 color=AZUL_SENA, align=PP_ALIGN.CENTER)

# 2 modelos
add_text(sl, "ISO/IEC 25010 define DOS modelos:", 0.4, 4.22, 12.5, 0.38,
         font_size=13, bold=True, color=AZUL_SENA)

add_rect(sl, 0.4, 4.65, 5.9, 1.15, AZUL_CLARO)
add_text(sl, "📦 Modelo de Calidad del Producto",
         0.5, 4.68, 5.7, 0.42, font_size=13, bold=True, color=AZUL_SENA)
add_text(sl, "Evalúa las características internas y externas\ndel software: funcionalidad, seguridad, usabilidad…",
         0.5, 5.08, 5.7, 0.65, font_size=11, color=GRIS_OSCURO)

add_rect(sl, 6.6, 4.65, 6.35, 1.15, RGBColor(0xE8,0xF5,0xE9))
add_text(sl, "👤 Modelo de Calidad en Uso",
         6.7, 4.68, 6.15, 0.42, font_size=13, bold=True, color=VERDE_SENA)
add_text(sl, "Evalúa la experiencia del usuario final\nen contexto real de operación.",
         6.7, 5.08, 6.15, 0.65, font_size=11, color=GRIS_OSCURO)

add_rect(sl, 0.4, 5.9, 12.5, 0.7, RGBColor(0xFF,0xF8,0xE1))
add_text(sl, "💡  En ACADEMIX aplicamos el Modelo de Calidad del Producto, evaluando el módulo de autenticación "
         "contra las 4 características seleccionadas: Fiabilidad, Seguridad, Usabilidad y Mantenibilidad.",
         0.55, 5.93, 12.2, 0.62, font_size=11, color=GRIS_OSCURO)

# ══════════════════════════════════════════════════════════════════════════════
# D3 — Las 8 Características de Calidad
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Las 8 Características de Calidad del Producto",
             "ISO/IEC 25010 — Modelo completo con subcaracterísticas")
slide_footer(sl, 3)

caract = [
    ("1", "Adecuación\nFuncional",   "Completitud · Corrección · Pertinencia",             AZUL_SENA,              False),
    ("2", "Eficiencia de\nDesempeño","Comportamiento temporal · Uso de recursos",           RGBColor(0x01,0x57,0x9B), False),
    ("3", "Compatibilidad",           "Coexistencia · Interoperabilidad",                  RGBColor(0x4A,0x14,0x8C), False),
    ("4", "Usabilidad ★",             "Reconocibilidad · Aprendizabilidad · Accesibilidad", VERDE_SENA,              True),
    ("5", "Fiabilidad ★",             "Madurez · Disponibilidad · Tolerancia · Recuperación",RGBColor(0xE6,0x5C,0x00),True),
    ("6", "Seguridad ★",              "Confidencialidad · Integridad · Autenticidad · Trazabilidad",ROJO_ALERTA,    True),
    ("7", "Mantenibilidad ★",         "Modularidad · Reusabilidad · Analizabilidad",        RGBColor(0x1A,0x73,0x7A), True),
    ("8", "Portabilidad",             "Adaptabilidad · Instalabilidad · Reemplazabilidad",  GRIS_OSCURO,            False),
]

cols = 4
for idx, (num, name, subs, col, selected) in enumerate(caract):
    row = idx // cols
    c   = idx % cols
    x = 0.3 + c * 3.2
    y = 1.22 + row * 2.2
    bg = col if selected else RGBColor(0xE0,0xE0,0xE0)
    txt_col = BLANCO if selected else RGBColor(0x55,0x55,0x55)
    add_rect(sl, x, y, 3.0, 1.95, bg)
    add_text(sl, num, x+0.08, y+0.05, 0.5, 0.45,
             font_size=18, bold=True, color=BLANCO if selected else RGBColor(0x88,0x88,0x88))
    add_text(sl, name, x+0.1, y+0.05, 2.8, 0.65,
             font_size=13, bold=True, color=txt_col, align=PP_ALIGN.LEFT)
    add_text(sl, subs, x+0.1, y+0.72, 2.8, 1.1,
             font_size=9.5, color=BLANCO if selected else RGBColor(0x66,0x66,0x66),
             wrap=True)

add_rect(sl, 0.3, 5.68, 12.7, 0.55, RGBColor(0xFF,0xF3,0xCD))
add_text(sl, "★ Características seleccionadas para ACADEMIX — mayor impacto de riesgo en sistema escolar con datos de menores",
         0.5, 5.72, 12.3, 0.45, font_size=11, color=GRIS_OSCURO, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# D4 — Métricas ISO/IEC 25010 en ACADEMIX
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Métricas ISO/IEC 25010 Aplicadas a ACADEMIX",
             "Módulo evaluado: apps/accounts — Autenticación y Control de Acceso")
slide_footer(sl, 4)

headers = ["Característica", "Métrica", "Fórmula / Método", "Resultado", "Estado"]
rows = [
    ("Fiabilidad\n(Disponibilidad)", "Uptime Render", "(T_total − T_caído)/T_total × 100%", "99.1%", "✅ Cumple"),
    ("Seguridad\n(Autenticidad)", "Cobertura Hash", "Usuarios Argon2/PBKDF2 ÷ Total", "100%", "✅ Cumple"),
    ("Seguridad\n(Rate Limiting)", "Intentos login", "Límite de intentos por IP / 15 min", "❌ Ninguno", "🔴 Brecha (HAL-01)"),
    ("Usabilidad\n(Accesibilidad)", "ARIA en errores", "Alerts con aria-live ÷ Total críticos", "40%", "⚠️ Brecha (HAL-02)"),
    ("Mantenibilidad\n(Modularidad)", "Acoplamiento vistas", "Líneas en views.py", "1 000+ líneas", "⚠️ Mejora (HAL-04)"),
]
simple_table(sl, headers, rows,
             left=0.25, top=1.22,
             col_widths=[2.3, 2.2, 3.2, 2.1, 2.8],
             row_height=0.82,
             font_size=10.5, header_font_size=11)

add_rect(sl, 0.25, 5.55, 12.8, 0.62, RGBColor(0xFF,0xEB,0xEE))
add_text(sl, "🔴  HAL-01 (NC Mayor): Sin rate limiting en /login — riesgo de ataque de fuerza bruta. "
         "Pendiente implementar django-ratelimit (CR-ACAD-2026-005)",
         0.4, 5.58, 12.5, 0.56, font_size=11, color=ROJO_ALERTA, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# D5 — IEEE 730: Aseguramiento de Calidad SQA
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "IEEE 730 — Aseguramiento de Calidad del Software (SQA)",
             "Standard for Software Quality Assurance Processes — IEEE Computer Society, 2014")
slide_footer(sl, 5)

# Comparación SQA vs Testing
add_text(sl, "SQA vs. Testing: la diferencia clave", 0.4, 1.22, 12.5, 0.42,
         font_size=15, bold=True, color=AZUL_SENA)

add_rect(sl, 0.35, 1.7, 5.85, 3.2, AZUL_CLARO)
add_text(sl, "🛡️  SQA — Preventivo", 0.45, 1.75, 5.6, 0.5,
         font_size=14, bold=True, color=AZUL_SENA)
items_sqa = [
    "• Define procesos ANTES de codificar",
    "• Estándares de código (PEP 8, naming)",
    "• Revisiones e inspecciones formales",
    "• Auditorías internas / externas",
    "• Plan de Calidad (SQAP)",
    "• Pregunta: ¿estamos trabajando bien?",
]
for i, txt in enumerate(items_sqa):
    add_text(sl, txt, 0.5, 2.3 + i*0.37, 5.6, 0.35, font_size=11.5, color=GRIS_OSCURO)

add_rect(sl, 6.6, 1.7, 6.35, 3.2, RGBColor(0xFF,0xEE,0xDD))
add_text(sl, "🐛  Testing — Reactivo", 6.7, 1.75, 6.1, 0.5,
         font_size=14, bold=True, color=NARANJA)
items_test = [
    "• Busca bugs en código ya escrito",
    "• Pruebas unitarias, integración, E2E",
    "• Ejecuta el software para verificar",
    "• Detecta problemas que ya existen",
    "• django.test, pytest, Selenium",
    "• Pregunta: ¿está funcionando bien?",
]
for i, txt in enumerate(items_test):
    add_text(sl, txt, 6.75, 2.3 + i*0.37, 6.1, 0.35, font_size=11.5, color=GRIS_OSCURO)

add_rect(sl, 0.35, 5.05, 12.6, 0.08, AZUL_SENA)
add_rect(sl, 0.35, 5.18, 12.6, 0.72, RGBColor(0xE3,0xF2,0xFD))
add_text(sl, "💡  IEEE 730 establece que el SQA debe ser INDEPENDIENTE del equipo de desarrollo y tener "
         "autoridad para escalar problemas no resueltos. En ACADEMIX: el revisor del PR nunca es el mismo "
         "desarrollador que escribió el código.",
         0.5, 5.2, 12.3, 0.65, font_size=11.5, color=GRIS_OSCURO)

# ══════════════════════════════════════════════════════════════════════════════
# D6 — Anatomía del SQAP
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Anatomía del Plan de Calidad (SQAP)",
             "IEEE 730 — 10 secciones obligatorias aplicadas a ACADEMIX")
slide_footer(sl, 6)

headers = ["#", "Sección IEEE 730", "Implementación en ACADEMIX"]
rows = [
    ("1", "Propósito y alcance",          "Sistema escolar Django 5.x — 15 módulos activos"),
    ("2", "Documentos de referencia",     "ISO/IEC 25010 · IEEE 828 · NTC-ISO/IEC 25010 ICONTEC · Ley 1581"),
    ("3", "Gestión del SQA",              "Tech Lead actúa como CCB · QA · Dev Team (3 integrantes)"),
    ("4", "Documentación SQA",            "Informe Auditoría · Matriz de Calidad · Checklist de Código"),
    ("5", "Estándares de código",         "PEP 8 · Naming conventions Django · Black · Flake8"),
    ("6", "Revisiones e inspecciones",    "Code Review obligatorio en Pull Request antes de merge a main"),
    ("7", "Pruebas",                      "django.test — 18 test cases en apps/accounts/tests.py"),
    ("8", "Reportes de problemas",        "Formato CR-ACAD-2026-00X con ID único y aprobación Tech Lead"),
    ("9", "Herramientas y métodos",       "Git · GitHub Actions · Black · Flake8 · django-ratelimit (propuesto)"),
    ("10","Gestión de riesgos",           "Tabla de hallazgos HAL-01 a HAL-04 con plan de acción CAPA"),
]
simple_table(sl, headers, rows,
             left=0.25, top=1.22,
             col_widths=[0.4, 3.3, 8.8],
             row_height=0.48,
             font_size=10, header_font_size=11)

add_rect(sl, 0.25, 6.15, 12.8, 0.55, RGBColor(0xE8,0xF5,0xE9))
add_text(sl, "✅  El SQAP no es un documento estático — se actualiza con cada sprint y con cada hallazgo encontrado en auditoría.",
         0.4, 6.18, 12.5, 0.48, font_size=11.5, color=VERDE_SENA, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# D7 — Marco Regulatorio Colombiano
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Marco Regulatorio Colombiano",
             "Normativa nacional vigente que rige el desarrollo de software en Colombia")
slide_footer(sl, 7)

headers = ["Norma / Entidad", "Tipo", "Obligación para ACADEMIX"]
rows = [
    ("NTC-ISO/IEC 25010\n(ICONTEC)", "Norma Técnica Nacional",
     "Adopción oficial de ISO 25010 en Colombia — marco de calidad del producto"),
    ("Ley 1581 / 2012\n(Congreso)", "Ley Habeas Data",
     "Protección obligatoria de datos de estudiantes (menores de edad) — cifrado y control de acceso"),
    ("Res. 1519 / 2020\n(MinTIC)", "Accesibilidad Web WCAG 2.1 AA",
     "Atributos ARIA obligatorios en interfaces de servicio público — Brecha HAL-02 detectada"),
    ("Circular 002 / 2021\n(SIC)", "Seguridad de Datos",
     "Controles de cifrado y acceso documentados — Argon2id cumple el estándar"),
    ("CONPES 3975 / 2019\n(DNP)", "Política Nacional IA",
     "Marco ético para sistemas digitales educativos — relevante para evolución futura"),
    ("colCERT\n(MinDefensa)", "Ciberseguridad Nacional",
     "Protocolos de respuesta a incidentes de seguridad en plataformas institucionales"),
]
simple_table(sl, headers, rows,
             left=0.25, top=1.22,
             col_widths=[2.5, 2.8, 7.5],
             row_height=0.68,
             font_size=10, header_font_size=11)

add_rect(sl, 0.25, 5.55, 12.8, 0.72, RGBColor(0xFF,0xEB,0xEE))
add_text(sl, "⚠️  En Colombia, cumplir ISO/IEC 25010 NO es suficiente. La Ley 1581 y la Res. 1519 tienen "
         "fuerza de ley y su incumplimiento puede generar sanciones administrativas de la SIC o el MinTIC.",
         0.4, 5.58, 12.5, 0.65, font_size=11.5, color=ROJO_ALERTA, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# D8 — SCM: IEEE 828 y Procesos Nucleares
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "SCM — IEEE 828: Los 5 Procesos Nucleares",
             "Standard for Configuration Management in Systems and Software Engineering")
slide_footer(sl, 8)

procesos = [
    ("1️⃣", "Identificación\nde Configuración",
     "Catalogar todos los CIs:\ncódigo, settings, BD, docs",
     "CIs ACADEMIX:\napps/, settings.py,\nrequirements.txt, templates/"),
    ("2️⃣", "Control\nde Cambios",
     "Proponer, evaluar, aprobar\ny registrar modificaciones",
     "Formato CR-ACAD-2026-00X\nCCB: Tech Lead del equipo"),
    ("3️⃣", "Contabilidad del\nEstado (CSA)",
     "Registro de qué versión\nestá en cada ambiente",
     "v2.5.0-baseline → dev\nv2.5.1-baseline → prod"),
    ("4️⃣", "Auditorías de\nConfiguración",
     "FCA: verifica requisitos\nPCA: verifica artefactos",
     "FCA: módulo autenticación\nPCA: tag vs Render"),
    ("5️⃣", "Gestión\nde Releases",
     "Controla qué versiones\nse entregan y cuándo",
     "Tags Git: v2.5.0\nv2.5.1-baseline"),
]
colors = [AZUL_SENA, VERDE_SENA, NARANJA, RGBColor(0x6A,0x1B,0x9A), RGBColor(0x00,0x7B,0x83)]
for i, (num, name, desc, academix) in enumerate(procesos):
    x = 0.28 + i * 2.56
    add_rect(sl, x, 1.22, 2.4, 0.52, colors[i])
    add_text(sl, num + " " + name, x+0.05, 1.25, 2.3, 0.45,
             font_size=11.5, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_rect(sl, x, 1.74, 2.4, 1.55, AZUL_CLARO if i % 2 == 0 else RGBColor(0xE8,0xF5,0xE9))
    add_text(sl, desc, x+0.08, 1.78, 2.25, 0.75,
             font_size=10, color=GRIS_OSCURO)
    add_rect(sl, x, 3.3, 2.4, 0.08, colors[i])
    add_rect(sl, x, 3.38, 2.4, 1.35, RGBColor(0xFF,0xF8,0xE1))
    add_text(sl, "📌 ACADEMIX:", x+0.08, 3.4, 2.25, 0.32,
             font_size=9.5, bold=True, color=NARANJA)
    add_text(sl, academix, x+0.08, 3.72, 2.25, 0.98,
             font_size=9.5, color=GRIS_OSCURO)

add_rect(sl, 0.28, 4.82, 12.75, 0.65, RGBColor(0xE3,0xF2,0xFD))
add_text(sl, "💡  Un CI (Ítem de Configuración) es cualquier elemento del proyecto que necesita ser controlado. "
         "En ACADEMIX los CIs principales son: los 15 módulos Django, el settings.py, "
         "el esquema de BD, los requirements.txt y los templates HTML.",
         0.42, 4.85, 12.45, 0.58, font_size=11, color=GRIS_OSCURO)

# ══════════════════════════════════════════════════════════════════════════════
# D9 — CMMI-DEV: Área CM
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "CMMI-DEV — Área de Práctica: Gestión de Configuración (CM)",
             "Capability Maturity Model Integration for Development — Carnegie Mellon SEI")
slide_footer(sl, 9)

# Pirámide de niveles como tabla horizontal
add_text(sl, "Niveles de Madurez CMMI:", 0.4, 1.22, 12.5, 0.38,
         font_size=13, bold=True, color=AZUL_SENA)
niveles = [
    ("1\nInicial", RGBColor(0x9E,0x9E,0x9E), False),
    ("2\nGestionado", AZUL_SENA, True),   # <-- ACADEMIX
    ("3\nDefinido", VERDE_SENA, False),
    ("4\nGest. Cuant.", NARANJA, False),
    ("5\nOptimización", RGBColor(0x6A,0x1B,0x9A), False),
]
for i, (lbl, col, current) in enumerate(niveles):
    x = 0.35 + i * 2.52
    add_rect(sl, x, 1.65, 2.35, 0.88, col)
    add_text(sl, lbl, x, 1.68, 2.35, 0.55, font_size=12, bold=True,
             color=BLANCO, align=PP_ALIGN.CENTER)
    if current:
        add_text(sl, "← ACADEMIX\n(estimado)", x, 2.52, 2.35, 0.42,
                 font_size=9.5, bold=True, color=AZUL_SENA, align=PP_ALIGN.CENTER)

add_rect(sl, 0.35, 2.72, 12.6, 0.06, AZUL_SENA)

# Tabla SG
add_text(sl, "Objetivos Específicos del Área CM en ACADEMIX:", 0.4, 2.85, 12.5, 0.38,
         font_size=13, bold=True, color=AZUL_SENA)

headers = ["Objetivo", "Descripción", "Práctica en ACADEMIX"]
rows_sg = [
    ("SG 1\nEstablecer Baselines",
     "Identificar CIs y crear líneas base\nformales y controladas",
     "Tag Git v2.5.0-baseline → commit d97d7a6\n(módulo recuperación contraseña completado)"),
    ("SG 2\nSeguir y Controlar Cambios",
     "Toda modificación pasa por proceso\nformal de solicitud y aprobación",
     "Formato CR-ACAD-2026-00X: ID único,\nimpacto técnico, riesgo, firma Tech Lead"),
    ("SG 3\nEstablecer Integridad",
     "Verificar que lo que está en producción\nes exactamente lo aprobado",
     "Pull Requests obligatorios + Checklist\nde código antes de merge a main"),
]
simple_table(sl, headers, rows_sg,
             left=0.35, top=3.3,
             col_widths=[2.4, 4.3, 5.85],
             row_height=0.88,
             font_size=10.5, header_font_size=11)

add_rect(sl, 0.35, 5.98, 12.6, 0.55, RGBColor(0xFF,0xF3,0xCD))
add_text(sl, "🎯  Meta del semestre: avanzar de CMMI Nivel 2 → Nivel 3, estandarizando los procesos de SCM "
         "en una biblioteca organizacional que todos los integrantes apliquen de la misma manera.",
         0.5, 6.01, 12.3, 0.48, font_size=11, color=GRIS_OSCURO, bold=True)

# ══════════════════════════════════════════════════════════════════════════════
# D10 — GitFlow, Baselines y Control de Cambios
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "GitFlow, Baselines y Control de Cambios en ACADEMIX",
             "Implementación práctica de SCM sobre el repositorio real del proyecto")
slide_footer(sl, 10)

# Commits recientes
add_text(sl, "📋 Últimos 5 commits del repositorio:", 0.4, 1.22, 7.5, 0.38,
         font_size=12, bold=True, color=AZUL_SENA)
commits = [
    ("d97d7a6", "main", "Implementar módulo completo de recuperación de contraseña", "✅"),
    ("0ac921a", "main", "Blindar carga masiva de estudiantes con savepoints atómicos", "✅"),
    ("25a46f7", "main", "Eliminar sección Estado SCRUM del dashboard", "✅"),
    ("4cdeb2d", "main", "Poblar catálogo oficial de asignaturas", "✅"),
    ("3829cb0", "main", "Configurar usuarios institucionales para Render", "✅"),
]
simple_table(sl, ["Commit", "Rama", "Descripción", ""],
             commits, left=0.35, top=1.65,
             col_widths=[1.3, 1.1, 6.5, 0.5],
             row_height=0.38, font_size=10, header_font_size=10.5)

# Baselines
add_text(sl, "🏷️ Baselines establecidas:", 0.4, 3.65, 7.5, 0.38,
         font_size=12, bold=True, color=VERDE_SENA)
add_rect(sl, 0.35, 4.08, 6.15, 0.52, RGBColor(0xE8,0xF5,0xE9))
add_text(sl, "v2.5.0-baseline  →  commit d97d7a6  (Módulo autenticación completo)",
         0.5, 4.12, 5.9, 0.42, font_size=11, color=VERDE_SENA, bold=True)
add_rect(sl, 0.35, 4.63, 6.15, 0.52, AZUL_CLARO)
add_text(sl, "v2.5.1-baseline  →  commit f4b82e1  (Correcciones CR-ACAD-2026-005)",
         0.5, 4.67, 5.9, 0.42, font_size=11, color=AZUL_SENA, bold=True)

# Ciclo CR
add_text(sl, "🔄 Ciclo de vida de un Change Request:", 7.1, 1.22, 6.0, 0.38,
         font_size=12, bold=True, color=AZUL_SENA)
steps_cr = [
    ("1. Detectar necesidad", AZUL_SENA),
    ("2. Llenar Formato CR", AZUL_SENA),
    ("3. CCB evalúa y aprueba", VERDE_SENA),
    ("4. Crear rama feature/CR-00X", VERDE_SENA),
    ("5. Implementar + Pull Request", NARANJA),
    ("6. Checklist código + Code Review", NARANJA),
    ("7. Merge a main + CSA actualizada", ROJO_ALERTA),
]
for i, (step, col) in enumerate(steps_cr):
    add_rect(sl, 7.1, 1.65 + i * 0.56, 5.95, 0.48, AZUL_CLARO if i % 2 == 0 else BLANCO,
             line_color=col)
    add_text(sl, step, 7.2, 1.68 + i * 0.56, 5.75, 0.4,
             font_size=11, color=col, bold=True)

add_rect(sl, 0.35, 5.3, 12.6, 0.65, RGBColor(0xFF,0xF8,0xE1))
add_text(sl, "💡  Diferencia CMMI Nivel 1 vs Nivel 2: En nivel 1 los commits van directamente a main sin proceso. "
         "En nivel 2 CADA cambio tiene un CR aprobado, una rama controlada y una revisión formal antes del merge.",
         0.5, 5.33, 12.3, 0.58, font_size=11, color=GRIS_OSCURO)

# ══════════════════════════════════════════════════════════════════════════════
# D11 — Conclusiones
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Conclusiones y Relación con ACADEMIX",
             "Lo que aprendimos y cómo transforma nuestro proyecto formativo")
slide_footer(sl, 11)

conclusiones = [
    (AZUL_SENA, "ISO/IEC 25010",
     "Nos dio el vocabulario preciso para medir la calidad. "
     "Pasamos de 'el sistema funciona' a '99.1% disponibilidad, "
     "100% cobertura hash, brecha ARIA al 40%'.",
     "📐"),
    (VERDE_SENA, "IEEE 730 — SQA",
     "La calidad se PLANIFICA, no se verifica al final. "
     "El checklist y los PR obligatorios son nuestro SQAP en acción.",
     "🛡️"),
    (NARANJA, "Normativa Colombiana",
     "Ley 1581 y Res. 1519 no son opcionales. "
     "Tenemos una brecha real (HAL-02) que viola una obligación legal de accesibilidad.",
     "🇨🇴"),
    (RGBColor(0x6A,0x1B,0x9A), "IEEE 828 + CMMI",
     "Formalizamos lo que ya hacíamos con Git. "
     "Ahora cada commit, PR y tag es parte de un proceso SCM auditable y reproducible.",
     "⚙️"),
    (ROJO_ALERTA, "ACADEMIX: Nivel CMMI 2",
     "Estimamos nivel 2 — Gestionado. Meta: nivel 3 estandarizando procesos "
     "en biblioteca organizacional para todo el equipo.",
     "🎯"),
]
for i, (col, titulo, texto, icon) in enumerate(conclusiones):
    x = 0.3 + (i % 3) * 4.3
    y = 1.22 if i < 3 else 3.8
    if i == 3: x = 0.3
    if i == 4: x = 4.6
    add_rect(sl, x, y, 4.0, 2.2, RGBColor(0xF5,0xF5,0xF5), line_color=col)
    add_rect(sl, x, y, 4.0, 0.55, col)
    add_text(sl, icon + "  " + titulo, x+0.1, y+0.05, 3.8, 0.45,
             font_size=12, bold=True, color=BLANCO)
    add_text(sl, texto, x+0.12, y+0.62, 3.76, 1.45,
             font_size=10.5, color=GRIS_OSCURO, wrap=True)

add_rect(sl, 0.3, 6.1, 12.7, 0.62, AZUL_SENA)
add_text(sl, "La investigación Fase 1 no fue solo leer normas: fue aplicarlas al código real, "
         "encontrar brechas reales, y tener el lenguaje técnico para documentarlas y corregirlas.",
         0.5, 6.13, 12.4, 0.55, font_size=12, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# D12 — Preguntas
# ══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, AZUL_SENA)
add_rect(sl, 0, 3.8, 13.33, 3.7, GRIS_OSCURO)
add_rect(sl, 0.4, 2.8, 12.5, 0.08, AMARILLO)

add_text(sl, "¿PREGUNTAS?", 0.5, 1.0, 12.3, 1.3,
         font_size=60, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_text(sl, "Estamos listos para la auditoría externa.", 0.5, 2.2, 12.3, 0.55,
         font_size=20, color=AMARILLO, align=PP_ALIGN.CENTER)

preguntas = [
    "¿Diferencia ISO 9126 vs 25010?",
    "¿Por qué esas 4 características?",
    "¿Qué es una baseline en Git?",
    "¿Qué es el CCB?",
    "¿Hallazgo más crítico y solución?",
    "¿Nivel CMMI actual?",
]
for i, q in enumerate(preguntas):
    col = i % 3
    row = i // 3
    x = 0.5 + col * 4.1
    y = 4.05 + row * 0.85
    add_rect(sl, x, y, 3.85, 0.72, RGBColor(0x00,0x30,0x60))
    add_text(sl, q, x+0.12, y+0.08, 3.65, 0.58,
             font_size=11, color=BLANCO, bold=True, wrap=True)

add_rect(sl, 0, 7.15, 13.33, 0.35, RGBColor(0x00,0x30,0x60))
add_text(sl, "ACADEMIX · SENA ADSO · Ficha 3173430 · Noviembre 2026", 0.3, 7.17, 12.7, 0.28,
         font_size=9, color=RGBColor(0x99,0xBB,0xFF), align=PP_ALIGN.CENTER)

# ── Guardar ────────────────────────────────────────────────────────────────────
output = r"C:\Academix\docs\PRESENTACION_MARCO_CONCEPTUAL_FASE1.pptx"
prs.save(output)
print(f"[OK] Presentacion guardada en: {output}")


