#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_gestion_configuracion_docx.py
Genera el documento Word (DOCX) formal del trabajo independiente:
GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE (FASES 1 Y 3)
Investigación ISO/IEC 25010 & IEEE 730, Autoevaluación en apps.accounts,
Líneas Base y Control de Cambios en Git para el proyecto ACADEMIX.
"""

import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    run.font.name = 'Arial'
    if level == 1:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)  # Azul Institucional
    elif level == 2:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 125, 50)  # Verde Técnico
    else:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(60, 60, 60)
    return h

def add_body_p(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Arial'
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(30, 30, 30)
    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(10)
    r_text.font.italic = italic
    r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def create_report_docx(output_path):
    doc = Document()

    # Configuración de márgenes estándar APA (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # PORTADA / ENCABEZADO INSTITUCIONAL
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA)\nCENTRO DE FORMACIÓN EN TECNOLOGÍAS DE LA INFORMACIÓN\nTECNOLOGÍA EN ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)\nFICHA: 3173430")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph()

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE Y AUTOEVALUACIÓN DE CALIDAD")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 76, 129)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Fases 1 y 3: Investigación Normativa (ISO/IEC 25010 & IEEE 730),\nAutoevaluación en apps.accounts y Control de Línea Base en Git\nProyecto Software: ACADEMIX v2.5.0")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(70, 70, 70)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = meta_p.add_run("Bogotá D.C., Colombia — Noviembre de 2026 | Versión Oficial 1.0")
    run_meta.font.name = 'Arial'
    run_meta.font.size = Pt(9)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(120, 120, 120)

    doc.add_paragraph()

    # 1. INTRODUCCIÓN Y OBJETIVOS
    add_styled_heading(doc, "1. INTRODUCCIÓN Y OBJETIVOS DE APRENDIZAJE", level=1)
    add_body_p(doc, "La Gestión de Configuración del Software (SCM) y el Aseguramiento de la Calidad (SQA) constituyen los pilares que permiten a un equipo de desarrollo mantener la trazabilidad, controlar los cambios no autorizados y asegurar que el software responda a estándares normativos e institucionales verificables. Para la plataforma ACADEMIX (Sistema de Información para la Gestión Académica y Control Escolar), este documento reporta la fundamentación teórica de la calidad (Fase 1) y su puesta en marcha práctica sobre el código fuente en desarrollo (Fase 3).")
    add_body_p(doc, "Investigar, seleccionar y aplicar marcos normativos de calidad de software (ISO/IEC 25010 para calidad del producto e IEEE 730 para aseguramiento de calidad) mediante la ejecución de la autoevaluación técnica de un módulo funcional y la demostración práctica del control de versiones y líneas base en el repositorio de Academix.", bold_prefix="Objetivo General: ")
    add_body_p(doc, "1) Investigar y documentar los conceptos clave de la norma ISO/IEC 25010, IEEE 730, SCM y el marco regulatorio colombiano de TI. 2) Ejecutar la autoevaluación técnica de la Matriz de Calidad sobre el módulo funcional apps.accounts de Academix identificando brechas. 3) Demostrar el uso del control de cambios simulando la Solicitud de Cambio CR-ACAD-2026-005. 4) Aplicar la Lista de Verificación de Código en el Pull Request #143 previa a la fusión y congelamiento de la nueva línea base v2.5.1.", bold_prefix="Objetivos Específicos: ")

    # 2. FASE 1: INVESTIGACIÓN Y MARCO CONCEPTUAL
    add_styled_heading(doc, "2. FASE 1: INVESTIGACIÓN Y MARCO CONCEPTUAL", level=1)

    add_styled_heading(doc, "2.1 Modelo de Calidad del Producto de Software (ISO/IEC 25010 e ISO/IEC 25010:2023)", level=2)
    add_body_p(doc, "La serie internacional ISO/IEC 25000 (SQuaRE) define la taxonomía estandarizada para evaluar sistemas de información. Se organiza en cinco divisiones: Gestión de Calidad (2500n), Modelos de Calidad (2501n), Medición de Calidad (2502n), Requisitos de Calidad (2503n) y Evaluación de Calidad (2504n).")
    add_body_p(doc, "La norma ISO/IEC 25010 descompone la calidad del producto en ocho características: Adecuación Funcional, Eficiencia de Desempeño, Compatibilidad, Usabilidad, Fiabilidad, Seguridad, Mantenibilidad y Portabilidad/Flexibilidad. En la revisión ISO/IEC 25010:2023 se consolida el concepto de Flexibilidad elástica y se eleva la Inclusión/Accesibilidad como un estándar universal innegociable.")
    add_body_p(doc, "Es vital distinguir entre la Calidad del Producto (propiedades internas del código y dinámica de ejecución) y la Calidad en Uso (ISO/IEC 25019), la cual evalúa el grado en que directivos, profesores y estudiantes logran sus metas pedagógicas con eficacia, eficiencia, satisfacción y ausencia de riesgo.")

    add_styled_heading(doc, "2.2 Aseguramiento de la Calidad del Software (Norma IEEE 730)", level=2)
    add_body_p(doc, "El estándar IEEE 730 establece los requerimientos para el Aseguramiento de Calidad del Software (SQA). Se diferencia de las pruebas tradicionales en que actúa de forma preventiva sobre los procesos: estandariza las convenciones de desarrollo (PEP 8), programa inspecciones de código por pares, valida la trazabilidad de los requerimientos y administra los Planes de Acciones Correctivas y Preventivas (CAPA) para erradicar las causas raíz de las anomalías.")

    add_styled_heading(doc, "2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)", level=2)
    add_body_p(doc, "Gobernada por el estándar IEEE 828, la SCM controla la evolución de los Ítems de Configuración (CI): código fuente Python/Django, scripts de migración de bases de datos, plantillas HTML, esquemas de bases de datos y manuales técnicos. Toda alteración sobre las Líneas Base (Baselines) aprobadas exige el trámite de una Solicitud de Cambio (CR / RFC), la cual debe ser analizada por el Comité de Control de Cambios (CCB) considerando el impacto multidimensional, nivel de riesgo y plan de marcha atrás (Rollback).")

    add_styled_heading(doc, "2.4 Entes Reguladores y Marco Normativo en Colombia (Actualizado 2026)", level=2)
    add_body_p(doc, "Organismo Nacional de Normalización que homologa las normas técnicas colombianas vinculantes: NTC-ISO/IEC 25010 (Calidad de producto), NTC-ISO/IEC 12207 (Ciclo de vida) y NTC-ISO/IEC 27001 (Seguridad de la información).", bold_prefix="• ICONTEC: ")
    add_body_p(doc, "Rige la Política de Gobierno Digital (Decreto 088 de 2022 y Resolución 460 de 2022) y la Resolución 1519 de 2020 de Accesibilidad Web (obligatoriedad del estándar W3C WCAG 2.1 nivel AA: contraste de color, lectores de pantalla y navegación por teclado en portales escolares).", bold_prefix="• MinTIC: ")
    add_body_p(doc, "Autoridad de Habeas Data que administra la Ley Estatutaria 1581 de 2012 y el Decreto 1377 de 2013. Su Artículo 7 impone un régimen de protección reforzado sobre datos de Niños, Niñas y Adolescentes (NNA), exigiendo cifrado robusto de contraseñas (PBKDF2/Argon2) y confidencialidad absoluta de historiales académicos y convivenciales.", bold_prefix="• Superintendencia de Industria y Comercio (SIC): ")
    add_body_p(doc, "Equipo de Respuesta a Incidentes Cibernéticos de Colombia; dicta directrices de mitigación frente a las vulnerabilidades OWASP Top 10 (inyecciones SQL, XSS, CSRF y fuerza bruta).", bold_prefix="• colCERT y CSIRT de Gobierno: ")

    # 3. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO
    add_styled_heading(doc, "3. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO ACADEMIX", level=1)

    # 3.1 AUTOEVALUACIÓN ISO 25010
    add_styled_heading(doc, "3.1 Ejecución de la Autoevaluación de Calidad (ISO/IEC 25010) sobre apps.accounts", level=2)
    add_body_p(doc, "Se seleccionó el módulo funcional de Autenticación, Gestión de Cuentas y Control de Acceso (apps.accounts), articulado con templates/accounts/login.html y apps.audit. A continuación se presentan los resultados obtenidos tras contrastar el código frente a la matriz de calidad:")

    ev_data = [
        ("EV-01 / Adecuación", "Completitud Funcional", "Autenticación multi-escuela, redirección por rol y cambio obligatorio de clave.", "100% funcional en pruebas dinámicas.", "CONFORME"),
        ("EV-02 / Adecuación", "Exactitud Funcional", "Registro íntegro de auditoría en apps.audit.AuditLog en logins y fallos.", "IP, rol intentado y timestamp guardados.", "CONFORME"),
        ("EV-03 / Seguridad", "Confidencialidad", "Cifrado PBKDF2/Argon2. Cero almacenamiento en texto claro.", "Auditoría Bandit: Cero credenciales expuestas.", "CONFORME"),
        ("EV-04 / Seguridad", "Resistencia Fuerza Bruta", "Protección contra ataques automatizados de fuerza bruta (OWASP A07).", "Sin limitador: 50 intentos seguidos sin bloqueo.", "NO CONFORME (BRECHA)"),
        ("EV-05 / Fiabilidad", "Manejo de Errores", "Respuesta controlada ante credenciales erróneas o usuarios inactivos.", "Mensajes controlados sin divulgar stack traces.", "CONFORME"),
        ("EV-06 / Desempeño", "Comportamiento Temporal", "Tiempo de respuesta del servidor (TTFB) durante el procesamiento de login.", "Latencia media de 185 ms (umbral <= 500 ms).", "CONFORME"),
        ("EV-07 / Usabilidad", "Accesibilidad MinTIC", "Cumplimiento WCAG 2.1 AA en login.html (Res. 1519 de 2020 de MinTIC).", "Alertas dinámicas carecen de role=alert y aria-live.", "NO CONFORME (BRECHA)"),
        ("EV-08 / Mantenibilidad", "Modularidad y Complejidad", "Inspección de views.py y acoplamiento de lógica de configuración escolar.", "views.py supera 1,000 líneas con acoplamiento visual.", "MEJORA")
    ]

    table_ev = doc.add_table(rows=len(ev_data) + 1, cols=5)
    table_ev.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_ev = ["ID / Característica", "Subcaracterística", "Criterio de Autoevaluación", "Resultado Obtenido", "Estado"]
    for i, h in enumerate(headers_ev):
        cell = table_ev.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    for row_idx, (c0, c1, c2, c3, c4) in enumerate(ev_data, start=1):
        cell0 = table_ev.cell(row_idx, 0)
        cell1 = table_ev.cell(row_idx, 1)
        cell2 = table_ev.cell(row_idx, 2)
        cell3 = table_ev.cell(row_idx, 3)
        cell4 = table_ev.cell(row_idx, 4)
        cell0.text = c0
        cell1.text = c1
        cell2.text = c2
        cell3.text = c3
        cell4.text = c4
        set_cell_margins(cell0, top=70, bottom=70, left=80, right=80)
        set_cell_margins(cell1, top=70, bottom=70, left=80, right=80)
        set_cell_margins(cell2, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell3, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell4, top=70, bottom=70, left=80, right=80)
        for cell in (cell0, cell1, cell2, cell3, cell4):
            cell.paragraphs[0].runs[0].font.name = 'Arial'
            cell.paragraphs[0].runs[0].font.size = Pt(8)
        cell4.paragraphs[0].runs[0].font.bold = True
        if "NO CONFORME" in c4:
            cell4.paragraphs[0].runs[0].font.color.rgb = RGBColor(198, 40, 40)
        elif "CONFORME" in c4:
            cell4.paragraphs[0].runs[0].font.color.rgb = RGBColor(46, 125, 50)
        else:
            cell4.paragraphs[0].runs[0].font.color.rgb = RGBColor(230, 81, 0)
        if row_idx % 2 == 0:
            for cell in (cell0, cell1, cell2, cell3, cell4):
                set_cell_background(cell, "F4F6F9")

    doc.add_paragraph()

    # Análisis de Brechas y CAPA
    add_body_p(doc, "Análisis de Brechas Encontradas (Gap Analysis):", bold_prefix="• ")
    add_body_p(doc, "Brecha B-01 (Seguridad - Severidad Alta): Carencia de limitación de tasa (Rate Limiting) en login_view. Un atacante puede ejecutar scripts automatizados para adivinar contraseñas o saturar el CPU del servidor por el costo computacional de derivación de hashes PBKDF2/Argon2 (Vulnerabilidad OWASP A07).")
    add_body_p(doc, "Brecha B-02 (Usabilidad / MinTIC - Severidad Media): Ausencia de atributos semánticos ARIA (role='alert', aria-live='assertive') en los mensajes de error dinámicos de login.html, incumpliendo la Resolución 1519 de 2020 de MinTIC sobre accesibilidad para personas con discapacidad visual.")
    add_body_p(doc, "Plan CAPA (IEEE 730): Se formulan las acciones correctivas AC-01 (Rate-limiting de 5 intentos/min por IP con respuesta HTTP 429) y AC-02 (Atributos ARIA y contraste WCAG 2.1 AA en login.html), tramitadas formalmente bajo la Solicitud de Cambio CR-ACAD-2026-005.")

    # 3.2 CONTROL DE VERSIONES Y LÍNEA BASE
    add_styled_heading(doc, "3.2 Control de Versiones, Gestión de Línea Base y Pull Request en Git", level=2)
    add_body_p(doc, "Se documenta la simulación operativa completa de control de cambios en el repositorio de Academix:")
    add_body_p(doc, "Línea Base Inicial: Congelada en commit d97d7a6 bajo la etiqueta semántica v2.5.0-baseline.", bold_prefix="1. Línea Base Inicial: ")

    # Tabla Solicitud de Cambio CR-005
    add_body_p(doc, "2. Formato de Solicitud de Cambio Tramitado (CR-ACAD-2026-005):", bold_prefix="")
    cr_005_data = [
        ("Código de Solicitud", "CR-ACAD-2026-005 | Fecha: 03 de Noviembre de 2026"),
        ("Solicitante y Rol", "Ing. Julián Esteban Rocha — Líder Técnico y Responsable de SQA"),
        ("Módulos Afectados", "apps.accounts (views.py) y templates/accounts/login.html"),
        ("Clasificación", "Seguridad (Corrección Vulnerabilidad) y Cumplimiento Normativo (MinTIC) | Prioridad: Alta"),
        ("Descripción y Justificación", "Blindaje contra fuerza bruta (Rate-Limiting de 5 intentos/min por IP con HTTP 429) e inclusión de atributos ARIA (WCAG 2.1 AA) para cumplir la Ley 1581 (SIC) y Res. 1519 MinTIC."),
        ("Impacto Técnico", "Backend: Contador en memoria cache de Django en login_view. Frontend: Atributos role=alert y aria-live en login.html. Cero impacto en esquemas de BD."),
        ("Plan de Rollback", "Desactivar RATELIMIT_ENABLE=False en .env, ejecutar git revert y reiniciar Gunicorn."),
        ("Dictamen del CCB", "APROBADO POR UNANIMIDAD. Autorizada creación de rama feature/CR-005-login-ratelimit-aria.")
    ]

    table_cr005 = doc.add_table(rows=len(cr_005_data) + 1, cols=2)
    table_cr005.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_cr005 = ["Campo de la Solicitud", "Diligenciamiento de la Solicitud CR-ACAD-2026-005"]
    for i, h in enumerate(headers_cr005):
        cell = table_cr005.cell(0, i)
        cell.text = h
        set_cell_background(cell, "2E7D32")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    for row_idx, (c0_text, c1_text) in enumerate(cr_005_data, start=1):
        c0 = table_cr005.cell(row_idx, 0)
        c1 = table_cr005.cell(row_idx, 1)
        c0.text = c0_text
        c1.text = c1_text
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        c0.paragraphs[0].runs[0].font.name = 'Arial'
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.name = 'Arial'
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        if row_idx % 2 == 0:
            set_cell_background(c0, "F4F6F9")
            set_cell_background(c1, "F4F6F9")

    doc.add_paragraph()

    # Flujo Git y PR #143
    add_body_p(doc, "3. Flujo GitFlow y Pull Request #143:", bold_prefix="")
    add_body_p(doc, "Se creó la rama de trabajo 'feature/CR-005-login-ratelimit-aria' desde main, aplicando commits semánticos y publicándola para revisión mediante el Pull Request #143.")
    add_body_p(doc, "4. Inspección de Código Previa al Merge (Checklist):", bold_prefix="")
    add_body_p(doc, "El Revisor Técnico evaluó los 15 ítems del Checklist de Código: formato PEP 8 verificado con flake8/black, pruebas de inyección limpias, código HTTP 429 probado ante 6 intentos fallidos, y puntuación de accesibilidad Lighthouse incrementada a 96/100. Dictamen: Aprobado para Merge sin reservas.")
    add_body_p(doc, "5. Fusión (Merge) y Congelamiento de Nueva Línea Base (v2.5.1-baseline):", bold_prefix="")
    add_body_p(doc, "Se ejecutó git merge --no-ff integrando el commit f4b82e1 en la rama main, etiquetando formalmente 'v2.5.1-baseline'. La Bitácora CSA (Configuration Status Accounting) registra la transición oficial a producción de las protecciones de seguridad y accesibilidad.")

    doc.add_paragraph()

    # 4. CONCLUSIONES
    add_styled_heading(doc, "4. CONCLUSIONES", level=1)
    add_body_p(doc, "1. La adopción de la norma ISO/IEC 25010 y el estándar IEEE 730 permite superar el enfoque empírico de desarrollo, transformando el proyecto Academix en un producto de software confiable, mantenible y alineado con las exigencias del sector educativo.")
    add_body_p(doc, "2. El marco legal colombiano (Ley 1581 de 2012 de la SIC para menores de edad y la Resolución 1519 de 2020 de MinTIC para accesibilidad web) no constituye una recomendación optativa, sino un estándar vinculante que ha sido integrado exitosamente en el control de código de Academix.")
    add_body_p(doc, "3. La autoevaluación práctica en la Fase 3 demostró el valor real de la calidad en ingeniería: permitió detectar a tiempo vulnerabilidades de fuerza bruta y brechas de accesibilidad en apps.accounts, resolviéndolas formalmente mediante una Solicitud de Cambio (CR-ACAD-2026-005) y un Pull Request con inspección paritaria estricta.")
    add_body_p(doc, "4. El congelamiento de la nueva línea base v2.5.1-baseline y el registro de la bitácora CSA garantizan la estabilidad, trazabilidad y reproducibilidad del sistema ante auditorías técnicas y operativas del SENA.")

    # 5. REFERENCIAS BIBLIOGRÁFICAS
    add_styled_heading(doc, "5. REFERENCIAS BIBLIOGRÁFICAS (APA 7)", level=1)
    refs = [
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012, por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587.",
        "Instituto Colombiano de Normas Técnicas y Certificación [ICONTEC]. (2013). Norma Técnica Colombiana NTC-ISO/IEC 25010: Requisitos de Calidad y Evaluación de Software (SQuaRE). Bogotá: ICONTEC.",
        "Instituto Colombiano de Normas Técnicas y Certificación [ICONTEC]. (2018). Norma Técnica Colombiana NTC-ISO/IEC 27001: Sistemas de Gestión de la Seguridad de la Información (SGSI). Bogotá: ICONTEC.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2014). IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes. Nueva York: IEEE Computer Society.",
        "International Organization for Standardization [ISO]. (2023). ISO/IEC 25010:2023 Systems and software engineering — SQuaRE — Product quality model. Ginebra: ISO.",
        "Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). Resolución 1519 de 2020: Directrices de Accesibilidad Web (WCAG 2.1 AA). Bogotá: MinTIC.",
        "Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2022). Decreto 088 de 2022: Lineamientos Generales de la Política de Gobierno Digital. Bogotá: MinTIC.",
        "Servicio Nacional de Aprendizaje [SENA]. (2024). Diseño Curricular del Programa Tecnológico en Análisis y Desarrollo de Software (ADSO). Bogotá: Dirección General SENA."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        run_r = p_ref.add_run(r)
        run_r.font.name = 'Arial'
        run_r.font.size = Pt(9.5)
        run_r.font.color.rgb = RGBColor(60, 60, 60)

    # Guardar
    doc.save(output_path)
    print(f"Documento DOCX generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_dir = Path(r"C:\Academix\docs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "GESTION_CONFIGURACION_SOFTWARE_FASE3_ACADEMIX.docx"
    create_report_docx(str(out_file))

