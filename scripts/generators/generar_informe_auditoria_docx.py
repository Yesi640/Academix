#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_informe_auditoria_docx.py
Genera los documentos Word (DOCX) oficiales para:
1. INFORME_FINAL_AUDITORIA_CALIDAD_ACADEMIX.docx
2. GUION_EXPOSICION_PROCESO_CALIDAD_ACADEMIX.docx
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

# ─────────────────────────────────────────────────────────────────────────────
# 1. GENERACIÓN DEL INFORME FINAL DE AUDITORÍA (DOCX)
# ─────────────────────────────────────────────────────────────────────────────
def generate_audit_report_docx(output_path):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Encabezado SENA
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
    run_title = title_p.add_run("INFORME FINAL DE AUDITORÍA INTERNA DE CALIDAD DE SOFTWARE")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 76, 129)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Evaluación bajo ISO/IEC 25010, IEEE 730, IEEE 1028 y Marco Legal Colombiano\nPreparación para la Auditoría Externa del Instructor Técnico SENA\nProyecto Software: ACADEMIX v2.5.0")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(70, 70, 70)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = meta_p.add_run("Bogotá D.C., Colombia — Noviembre de 2026 | Dictamen: CONFORME SATISFACTORIO")
    run_meta.font.name = 'Arial'
    run_meta.font.size = Pt(9)
    run_meta.font.bold = True
    run_meta.font.color.rgb = RGBColor(46, 125, 50)

    doc.add_paragraph()

    # 1. DATOS GENERALES
    add_styled_heading(doc, "1. DATOS GENERALES Y FICHA TÉCNICA DE LA AUDITORÍA", level=1)
    ficha_data = [
        ("Código de Auditoría", "AUD-INT-ACAD-2026-01 | Fechas: 28 de Octubre a 03 de Noviembre de 2026"),
        ("Organización Auditada", "Proyecto Formativo ACADEMIX (Plataforma Web de Gestión Escolar)"),
        ("Programa y Ficha", "Tecnología en Análisis y Desarrollo de Software (ADSO) — Ficha: 3173430"),
        ("Equipo Auditor Interno", "Líder SQA, Líder Técnico de Arquitectura y Especialista en Datos/UX"),
        ("Auditor Externo Previsto", "Instructor Técnico SENA — Red de Conocimiento en Informática"),
        ("Entornos Evaluados", "Staging Cloud (Render + PostgreSQL) y Réplica On-Premise Local"),
        ("Línea Base del Código", "Línea Base v2.5.0-baseline (Commit d97d7a6) -> v2.5.1-baseline (Commit f4b82e1)"),
        ("Dictamen Final", "CONFORME SATISFACTORIO — 100% PREPARADO PARA AUDITORÍA EXTERNA")
    ]
    t_ficha = doc.add_table(rows=len(ficha_data) + 1, cols=2)
    t_ficha.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Parámetro de Auditoría", "Detalle Institucional y Operativo"]):
        cell = t_ficha.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    for r_idx, (p_text, d_text) in enumerate(ficha_data, start=1):
        c0 = t_ficha.cell(r_idx, 0)
        c1 = t_ficha.cell(r_idx, 1)
        c0.text = p_text
        c1.text = d_text
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        c0.paragraphs[0].runs[0].font.name = 'Arial'
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.name = 'Arial'
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        if r_idx % 2 == 0:
            set_cell_background(c0, "F4F6F9")
            set_cell_background(c1, "F4F6F9")

    doc.add_paragraph()

    # 2. OBJETIVOS Y ALCANCE
    add_styled_heading(doc, "2. OBJETIVOS Y ALCANCE DE LA AUDITORÍA", level=1)
    add_body_p(doc, "Planificar, ejecutar y documentar la auditoría interna de calidad a la plataforma Academix v2.5.0 bajo los estándares internacionales ISO/IEC 25010:2023, IEEE 730, IEEE 1028 y las normas técnicas y legales colombianas (ICONTEC, MinTIC y SIC), identificando brechas y consolidando la preparación para la auditoría externa del instructor técnico.", bold_prefix="Objetivo General: ")
    add_body_p(doc, "1) Auditar los 5 módulos críticos mediante pruebas SAST, DAST, rendimiento y accesibilidad. 2) Comprobar el acatamiento de la Ley 1581 de 2012 (datos de menores) y Res. 1519 de 2020 de MinTIC (WCAG 2.1 AA). 3) Clasificar hallazgos en No Conformidades y Fortalezas. 4) Ejecutar el Plan CAPA con análisis de causa raíz. 5) Preparar al equipo para la sustentación y evaluación externa.", bold_prefix="Objetivos Específicos: ")

    # 3. MARCO NORMATIVO
    add_styled_heading(doc, "3. MARCO NORMATIVO APLICADO", level=1)
    add_body_p(doc, "Estándar internacional de referencia para evaluar las 8 características del producto software.", bold_prefix="• ISO/IEC 25010:2023 (SQuaRE): ")
    add_body_p(doc, "Estándares que gobiernan las revisiones técnicas de software, auditorías formales y aseguramiento de calidad preventivo.", bold_prefix="• IEEE 1028-2008 & IEEE 730-2014: ")
    add_body_p(doc, "Obligatoriedad de accesibilidad web universal W3C WCAG 2.1 nivel AA (contraste, lectores de pantalla y navegación asistida).", bold_prefix="• MinTIC (Resolución 1519 de 2020): ")
    add_body_p(doc, "Habeas Data y régimen reforzado del Artículo 7 para Niños, Niñas y Adolescentes (cifrado robusto y confidencialidad).", bold_prefix="• Superintendencia de Industria y Comercio (Ley 1581 de 2012): ")

    # 4. RESULTADOS DE AUDITORÍA POR MÓDULOS
    add_styled_heading(doc, "4. RESULTADOS DE LA AUDITORÍA POR MÓDULOS CRÍTICOS", level=1)
    add_body_p(doc, "Cifrado PBKDF2/Argon2id conforme. RBAC validado al 100%. Desviación: Carencia inicial de Rate-Limiting en login_view.", bold_prefix="1. Autenticación y Control RBAC (apps.accounts): ")
    add_body_p(doc, "Savepoints atómicos con transaction.atomic que evitan corrupción de base de datos ante errores de formato. Datos de menores protegidos.", bold_prefix="2. Carga Masiva y Estudiantes (apps.students): ")
    add_body_p(doc, "Fórmula de RAPs ponderada al 100.00% con redondeo a dos decimales sin discrepancias. Integridad referencial PROTECT.", bold_prefix="3. Motor Curricular y Calificaciones (apps.grades): ")
    add_body_p(doc, "Generación con código QR dinámico y hash criptográfico SHA-256 para validación web sin divulgar datos sensibles.", bold_prefix="4. Boletines Oficiales PDF (apps.reports): ")
    add_body_p(doc, "Latencia media de 240 ms bajo carga concurrente de 100 usuarios (Locust). Cero secretos en código (.env en .gitignore).", bold_prefix="5. Infraestructura y Base de Datos (PostgreSQL): ")

    # 5. MATRIZ DE HALLAZGOS
    add_styled_heading(doc, "5. MATRIZ CONSOLIDADA DE HALLAZGOS DE AUDITORÍA", level=1)
    h_data = [
        ("HAL-01", "NC Mayor", "ISO 25010 / OWASP A07", "apps.accounts", "Falta de Rate-Limiting en login. Riesgo de fuerza bruta.", "ALTO"),
        ("HAL-02", "NC Menor", "MinTIC Res. 1519 (AA)", "login.html", "Falta de roles semánticos ARIA en mensajes de error.", "MEDIO"),
        ("HAL-03", "NC Menor", "ISO 25010 (Funcional)", "apps.grades", "Permisividad en cierre de periodo sin validación backend.", "MEDIO"),
        ("HAL-04", "Mejora", "ISO 25010 (Mantenibilidad)", "accounts/views.py", "Vistas densas con acoplamiento de configuración escolar.", "BAJO"),
        ("HAL-05", "Fortaleza", "SIC Ley 1581 (Privacidad)", "apps.reports", "Boletines con validación QR segura sin exponer datos de menores.", "DESTACADO"),
        ("HAL-06", "Fortaleza", "ISO 25010 (Fiabilidad)", "apps.students", "Savepoints atómicos ACID en carga masiva de estudiantes.", "DESTACADO"),
        ("HAL-07", "Fortaleza", "ISO 25010 (Exactitud)", "apps.grades", "Cómputo ponderado al 100% y redondeo a 2 decimales exacto.", "DESTACADO")
    ]
    t_h = doc.add_table(rows=len(h_data) + 1, cols=6)
    t_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_h = ["ID", "Tipo", "Norma", "Módulo", "Descripción del Hallazgo", "Riesgo"]
    for i, h in enumerate(headers_h):
        cell = t_h.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)

    for r_idx, (c0, c1, c2, c3, c4, c5) in enumerate(h_data, start=1):
        row_cells = [t_h.cell(r_idx, i) for i in range(6)]
        for i, val in enumerate([c0, c1, c2, c3, c4, c5]):
            row_cells[i].text = val
            set_cell_margins(row_cells[i], top=70, bottom=70, left=80, right=80)
            row_cells[i].paragraphs[0].runs[0].font.name = 'Arial'
            row_cells[i].paragraphs[0].runs[0].font.size = Pt(8)
        row_cells[1].paragraphs[0].runs[0].font.bold = True
        if "Mayor" in c1:
            row_cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(198, 40, 40)
        elif "Menor" in c1:
            row_cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(230, 81, 0)
        elif "Fortaleza" in c1:
            row_cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(46, 125, 50)
        if r_idx % 2 == 0:
            for cell in row_cells:
                set_cell_background(cell, "F4F6F9")

    doc.add_paragraph()

    # 6. PLAN CAPA
    add_styled_heading(doc, "6. PLAN DE ACCIONES CORRECTIVAS Y PREVENTIVAS (CAPA)", level=1)
    add_body_p(doc, "Implementación de estrangulamiento de 5 intentos/minuto por IP con respuesta HTTP 429. Tramitado en CR-005. Estado: CERRADA.", bold_prefix="• Acción AC-01 (Para HAL-01): ")
    add_body_p(doc, "Inclusión de atributos role=alert y aria-live=assertive en login.html. Score Lighthouse elevado a 96/100. Estado: CERRADA.", bold_prefix="• Acción AC-02 (Para HAL-02): ")
    add_body_p(doc, "Incorporación de decorador @period_is_open_required y migración is_locked. Tramitado en CR-004. Estado: CERRADA.", bold_prefix="• Acción AC-03 (Para HAL-03): ")

    # 7. PREPARACIÓN AUDITORÍA EXTERNA
    add_styled_heading(doc, "7. PREPARACIÓN PARA LA AUDITORÍA EXTERNA DEL INSTRUCTOR SENA", level=1)
    add_body_p(doc, "El equipo preparó un banco de preguntas técnicas fundamentadas y validó el cumplimiento del 100% de la lista de chequeo de evidencias (código fuente en Git, tags v2.5.0 y v2.5.1, solicitudes de cambio CR-004 y CR-005, checklists de Pull Request firmados, suite pytest con 88% de cobertura y software en vivo funcionando en la nube y On-Premise).")

    # 8. DICTAMEN FINAL
    add_styled_heading(doc, "8. DICTAMEN FINAL DEL EQUIPO AUDITOR", level=1)
    add_body_p(doc, "DICTAMEN OFICIAL: CONFORME SATISFACTORIO — 100% PREPARADO PARA AUDITORÍA EXTERNA. El sistema ACADEMIX v2.5.1 cumple a cabalidad con ISO/IEC 25010:2023, IEEE 730, IEEE 1028, la Ley 1581 de 2012 y la Resolución 1519 de 2020 de MinTIC.", bold_prefix="Resolución: ")

    # 9. REFERENCIAS
    add_styled_heading(doc, "9. REFERENCIAS BIBLIOGRÁFICAS (APA 7)", level=1)
    refs = [
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012 de Protección de Datos Personales. Diario Oficial No. 48.587.",
        "ICONTEC. (2013). Norma Técnica Colombiana NTC-ISO/IEC 25010: Requisitos de Calidad de Software (SQuaRE). Bogotá: ICONTEC.",
        "ISO. (2018). ISO 19011:2018 Guidelines for auditing management systems. Ginebra: ISO.",
        "ISO. (2023). ISO/IEC 25010:2023 Systems and software engineering — Product quality model. Ginebra: ISO.",
        "IEEE. (2008). IEEE Std 1028-2008: IEEE Standard for Software Reviews and Audits. Nueva York: IEEE Computer Society.",
        "IEEE. (2014). IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes. Nueva York: IEEE Computer Society.",
        "MinTIC. (2020). Resolución 1519 de 2020: Directrices de Accesibilidad Web (WCAG 2.1 AA). Bogotá: MinTIC.",
        "SENA. (2024). Norma Sectorial de Competencia Laboral 220501096. Bogotá: Dirección General SENA."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        run_r = p_ref.add_run(r)
        run_r.font.name = 'Arial'
        run_r.font.size = Pt(9)
        run_r.font.color.rgb = RGBColor(60, 60, 60)

    doc.save(output_path)
    print(f"Informe de Auditoría DOCX generado exitosamente en: {output_path}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. GENERACIÓN DEL GUION DE EXPOSICIÓN (DOCX)
# ─────────────────────────────────────────────────────────────────────────────
def generate_presentation_guide_docx(output_path):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA)\nTECNOLOGÍA EN ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)\nFICHA: 3173430")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph()

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("GUION Y ESTRUCTURA MAESTRA DE EXPOSICIÓN:\nPROCESO DE CALIDAD Y AUDITORÍA DE SOFTWARE")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 76, 129)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Sustentación de la Empresa Academix Software Solutions ante el Instructor Técnico SENA\nDuración: 15-20 Minutos | 3 Expositores | 10 Diapositivas + Live Demo")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(70, 70, 70)

    doc.add_paragraph()

    add_styled_heading(doc, "1. DISTRIBUCIÓN DE TIEMPOS Y ROLES DE LOS 3 INTEGRANTES", level=1)
    roles_data = [
        ("Expositor 1: Líder de Proyecto / SQA", "Diapositivas 1 y 2 (4 min)", "Apertura, identidad empresarial, ISO/IEC 25010 y marco legal colombiano."),
        ("Expositor 2: Líder Técnico / Arquitectura", "Diapositivas 3, 4 y 5 (7 min)", "Metodología de auditoría, herramientas SAST/DAST, hallazgos y causa raíz."),
        ("Expositor 3: Líder SCM y Despliegue", "Diapositivas 6, 7 y 8 (6.5 min)", "Plan CAPA, Solicitud de Cambio CR-005, PR #143 y Línea Base v2.5.1."),
        ("Equipo en Conjunto", "Diapositivas 9 y 10 (4.5 min)", "Demostración técnica en vivo (Live Demo), conclusiones y preguntas.")
    ]
    t_roles = doc.add_table(rows=len(roles_data) + 1, cols=3)
    t_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Expositor y Rol", "Diapositivas y Tiempo", "Enfoque Temático"]):
        cell = t_roles.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    for r_idx, (c0, c1, c2) in enumerate(roles_data, start=1):
        cell0 = t_roles.cell(r_idx, 0)
        cell1 = t_roles.cell(r_idx, 1)
        cell2 = t_roles.cell(r_idx, 2)
        cell0.text = c0
        cell1.text = c1
        cell2.text = c2
        set_cell_margins(cell0, top=70, bottom=70, left=80, right=80)
        set_cell_margins(cell1, top=70, bottom=70, left=80, right=80)
        set_cell_margins(cell2, top=70, bottom=70, left=100, right=100)
        cell0.paragraphs[0].runs[0].font.name = 'Arial'
        cell0.paragraphs[0].runs[0].font.bold = True
        cell0.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell1.paragraphs[0].runs[0].font.name = 'Arial'
        cell1.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell2.paragraphs[0].runs[0].font.name = 'Arial'
        cell2.paragraphs[0].runs[0].font.size = Pt(8.5)
        if r_idx % 2 == 0:
            for cell in (cell0, cell1, cell2):
                set_cell_background(cell, "F4F6F9")

    doc.add_paragraph()

    # GUION DIAPOSITIVA POR DIAPOSITIVA
    add_styled_heading(doc, "2. GUION TÉCNICO Y SPEECH POR DIAPOSITIVA", level=1)

    slides = [
        ("Diapositiva 1: Portada e Identidad Empresarial", "Expositor 1 (Líder SQA)",
         "Presentación de Academix Software Solutions, misión del proyecto y declaración del objetivo de la auditoría interna."),
        ("Diapositiva 2: Marco Normativo Internacional y Colombiano", "Expositor 1 (Líder SQA)",
         "ISO/IEC 25010:2023, IEEE 730, obligatoriedad de accesibilidad MinTIC Res. 1519 y protección de menores Ley 1581 SIC."),
        ("Diapositiva 3: Metodología y Arsenal de Pruebas de Auditoría", "Expositor 2 (Líder Técnico)",
         "Inspección bajo IEEE 1028: SAST con Bandit/flake8, DAST con OWASP ZAP, carga concurrente con Locust y Lighthouse CI."),
        ("Diapositiva 4: Resultados de Evaluación por Módulos Críticos", "Expositor 2 (Líder Técnico)",
         "Evidencias en login multi-escuela, carga masiva con savepoints atómicos, notas ponderadas al 100% y boletines QR."),
        ("Diapositiva 5: Matriz de Hallazgos y Causa Raíz (Ishikawa)", "Expositor 2 (Líder Técnico)",
         "No Conformidad Mayor HAL-01 (fuerza bruta en login) y NC Menor HAL-02 (ARIA). Análisis de los 5 Porqués."),
        ("Diapositiva 6: Plan CAPA (Acciones Correctivas y Preventivas)", "Expositor 3 (Líder SCM)",
         "Medidas técnicas aplicadas: limitador de 5 intentos/min por IP (HTTP 429) y etiquetas ARIA elevando Lighthouse a 96/100."),
        ("Diapositiva 7: Gestión de Configuración y Solicitud de Cambio", "Expositor 3 (Líder SCM)",
         "Trámite formal de CR-ACAD-2026-005, análisis multidimensional de impacto, plan de rollback y aprobación del CCB."),
        ("Diapositiva 8: Pull Request #143 y Línea Base v2.5.1", "Expositor 3 (Líder SCM)",
         "Flujo GitFlow, verificación de 15 ítems del Checklist de Code Review, merge --no-ff y congelamiento de v2.5.1-baseline."),
        ("Diapositiva 9: Demostración Técnica en Vivo (Live Demo)", "Equipo en Conjunto",
         "Prueba en vivo del bloqueo HTTP 429, registro en AuditLog, auditoría Lighthouse en vivo y escaneo de QR de boletín."),
        ("Diapositiva 10: Conclusiones y Preparación Auditoría Externa", "Todo el Equipo",
         "Dictamen de conformidad satisfactoria, lecciones aprendidas y apertura formal a la evaluación del instructor SENA.")
    ]

    for title, speaker, summary in slides:
        add_body_p(doc, f"{speaker} — Resumen: {summary}", bold_prefix=f"• {title}: ")

    doc.save(output_path)
    print(f"Guion de Exposición DOCX generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_dir = Path(r"C:\Academix\docs")
    out_dir.mkdir(parents=True, exist_ok=True)
    f1 = out_dir / "INFORME_FINAL_AUDITORIA_CALIDAD_ACADEMIX.docx"
    f2 = out_dir / "GUION_EXPOSICION_PROCESO_CALIDAD_ACADEMIX.docx"
    generate_audit_report_docx(str(f1))
    generate_presentation_guide_docx(str(f2))

