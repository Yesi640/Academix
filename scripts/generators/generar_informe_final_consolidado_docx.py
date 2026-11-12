#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_informe_final_consolidado_docx.py
Genera el documento Word (DOCX) del:
INFORME FINAL DEL PROCESO DE GESTIÓN DE CALIDAD EN EL DESARROLLO DE SOFTWARE
Consolidación integral de evidencias, hallazgos, novedades de seguimiento, control de configuración,
artefactos (Matriz ISO 25010, Change Request, Checklist Pre-Merge), auditoría interna y preparación
para la auditoría externa del instructor SENA.
Proyecto ACADEMIX v2.5.1 - Ficha 3173430
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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
        run.font.color.rgb = RGBColor(15, 76, 129)  # Azul Institucional SENA
    elif level == 2:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 125, 50)  # Verde Técnico
    else:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(50, 50, 50)
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

def add_callout(doc, text, title=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EBF3FA")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    if title:
        r_t = p.add_run(title + "\n")
        r_t.font.name = 'Arial'
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(15, 76, 129)
    r_b = p.add_run(text)
    r_b.font.name = 'Arial'
    r_b.font.size = Pt(9.5)
    r_b.font.italic = True
    r_b.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def build_table(doc, headers, data, col_widths, header_color="0F4C81"):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        set_cell_background(cell, header_color)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = 'Arial'
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Rows
    for i, row_data in enumerate(data):
        bg = "F4F6F9" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = tbl.cell(i + 1, j)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(str(val))
            run.font.name = 'Arial'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(40, 40, 40)
            if j == 0:
                run.font.bold = True
                
    # Column widths
    for row in tbl.rows:
        for j, w in enumerate(col_widths):
            row.cells[j].width = Inches(w)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def generate_consolidated_docx(output_path):
    doc = Document()
    
    # Configuración de márgenes estándar APA (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # ENCABEZADO INSTITUCIONAL
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA)\nCENTRO DE FORMACIÓN EN TECNOLOGÍAS DE LA INFORMACIÓN\nTECNOLOGÍA EN ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)\nFICHA DE CARACTERIZACIÓN: 3173430")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph()
    
    # TÍTULO DEL DOCUMENTO
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("INFORME FINAL DEL PROCESO DE GESTIÓN DE CALIDAD EN EL DESARROLLO DE SOFTWARE")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Consolidación Integral de Evidencias, Hallazgos, Novedades de Seguimiento y Control de Productos bajo Normas Internacionales (ISO/IEC 25010, IEEE 730, IEEE 828, CMMI-DEV) y Protocolos de la Organización")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(70, 70, 70)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Proyecto Formativo: Plataforma Web de Gestión Escolar ACADEMIX v2.5.1\nNoviembre de 2026")
    r_meta.font.name = 'Arial'
    r_meta.font.size = Pt(10)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(46, 125, 50)
    
    doc.add_paragraph()
    
    # FICHA TÉCNICA
    add_styled_heading(doc, "1. Datos Generales y Ficha Técnica del Proyecto", level=1)
    add_body_p(doc, "El presente informe consolida el ciclo completo de gestión de calidad, aseguramiento de procesos (SQA), control de configuración (SCM), autoevaluación práctica sobre el código fuente y auditoría interna de calidad aplicada a la plataforma web ACADEMIX. Constituye la evidencia técnica formal preparatoria para la evaluación y auditoría externa por parte del instructor técnico del SENA.")
    
    headers_ficha = ["Parámetro de Control", "Especificación Institucional y Operativa"]
    data_ficha = [
        ["Código de Auditoría", "AUD-INT-ACAD-2026-01"],
        ["Nombre del Software", "ACADEMIX — Sistema de Gestión Académica y Control Escolar"],
        ["Versión Auditada / Congelada", "Versión 2.5.1 (Línea Base: v2.5.1-baseline, Commit f4b82e1)"],
        ["Stack Tecnológico", "Python 3.14 / Django 5.x / PostgreSQL 16 / SQLite 3 / Bootstrap 5.3"],
        ["Programa de Formación", "Tecnología en Análisis y Desarrollo de Software (ADSO) — Ficha 3173430"],
        ["Equipo Desarrollador", "Academix Software Solutions — Aprendices ADSO SENA"],
        ["Líder SQA / Auditor", "Sofia Helena Torres (Aprendiz SQA Lead)"],
        ["Líder Técnico / CCB", "Julián Esteban Rocha (Aprendiz Líder de Arquitectura)"],
        ["Líder de UX y Pruebas", "David Camilo Morales (Aprendiz Especialista en Datos y UX)"],
        ["Auditor Externo Evaluador", "Instructor Técnico SENA — Especialidad Teleinformática y Software"],
        ["Normas de Referencia", "ISO/IEC 25010:2023, IEEE 730-2014, IEEE 828-2012, IEEE 1028-2008, CMMI-DEV v2.0"],
        ["Marco Legal Colombiano", "Ley 1581 de 2012 (Datos de Menores SIC), MinTIC Res. 1519 de 2020 (WCAG 2.1 AA)"],
        ["Estado del Dictamen", "CONFORME SATISFACTORIO — APTO PARA AUDITORÍA EXTERNA"]
    ]
    build_table(doc, headers_ficha, data_ficha, [2.5, 4.0], header_color="0F4C81")
    
    # OBJETIVOS
    add_styled_heading(doc, "2. Objetivos y Alcance de la Gestión de Calidad", level=1)
    add_body_p(doc, "Planificar, documentar y consolidar la gestión de calidad y configuración de la plataforma ACADEMIX, verificando la conformidad del producto frente a estándares internacionales (ISO/IEC 25010, IEEE 730, IEEE 828, CMMI-DEV) y normativas colombianas, mitigando brechas de seguridad y accesibilidad mediante acciones correctivas (CAPA) y garantizando la preparación para la auditoría externa del instructor.", bold_prefix="Objetivo General: ")
    
    add_styled_heading(doc, "2.1 Objetivos Específicos", level=2)
    add_body_p(doc, "1. Investigar y estructurar el marco normativo internacional y nacional aplicable al ciclo de vida del software escolar.")
    add_body_p(doc, "2. Diseñar e implementar los artefactos documentales obligatorios: Matriz de Evaluación de Calidad, Formato de Solicitud de Cambio (CR) y Checklist de Código Pre-Merge.")
    add_body_p(doc, "3. Ejecutar la autoevaluación práctica sobre el módulo de autenticación (apps.accounts), registrando métricas cuantitativas reales.")
    add_body_p(doc, "4. Simular el flujo de control de configuración (SCM) mediante GitFlow, Pull Request #143 y congelamiento de líneas base.")
    add_body_p(doc, "5. Realizar la auditoría interna de calidad con matriz de hallazgos, análisis de causa raíz (Ishikawa/5 Porqués) y plan de acción CAPA.")
    add_body_p(doc, "6. Estructurar la preparación para la sustentación externa del instructor mediante un banco de preguntas y lista de evidencias.")
    
    add_styled_heading(doc, "2.2 Alcance del Sistema Evaluado", level=2)
    add_body_p(doc, "La gestión de calidad abarcó 15 micro-aplicaciones en Django, destacando: autenticación y control de acceso RBAC (apps.accounts), bitácoras de auditoría institucional (apps.audit), carga masiva transaccional de estudiantes (apps.students), motor curricular y calificaciones RAPs al 100% (apps.grades), verificación de boletines oficiales PDF con QR criptográfico (apps.reports), infraestructura en Render Cloud y scripts de despliegue local.")
    
    # MARCO NORMATIVO
    add_styled_heading(doc, "3. Marco Normativo Internacional y Regulación Colombiana", level=1)
    add_body_p(doc, "La calidad de software en ACADEMIX se fundamenta en cuatro pilares normativos rigurosamente articulados:")
    
    add_body_p(doc, "Define 8 características de calidad del producto: Adecuación Funcional, Eficiencia de Desempeño, Compatibilidad, Usabilidad, Fiabilidad, Seguridad, Mantenibilidad y Portabilidad. Para el proyecto se priorizaron: Seguridad (protección de datos de menores), Fiabilidad (disponibilidad del 99% y transacciones atómicas), Usabilidad (accesibilidad WCAG 2.1 AA) y Mantenibilidad (arquitectura modular MVT).", bold_prefix="1. Modelo de Calidad del Producto (ISO/IEC 25010:2023 / SQuaRE): ")
    
    add_body_p(doc, "Establece el enfoque preventivo del aseguramiento de calidad. A diferencia de las pruebas reactivas, el SQA define estándares de código (PEP 8), revisiones formales por pares, trazabilidad de requerimientos y auditorías periódicas antes de cada entrega.", bold_prefix="2. Aseguramiento de Calidad del Software (IEEE 730-2014): ")
    
    add_body_p(doc, "Regula los 5 procesos nucleares de SCM: Identificación de CIs (código, BD, configuración, docs), Control de Cambios (Change Requests evaluados por el CCB), Contabilidad del Estado de Configuración (CSA), Auditorías de Configuración (FCA/PCA) y Gestión de Releases. En CMMI-DEV v2.0, ACADEMIX consolida el Nivel 2 (Gestionado) cumpliendo SG 1 (Baselines), SG 2 (Seguimiento de Cambios) y SG 3 (Integridad).", bold_prefix="3. Gestión de Configuración (IEEE 828-2012 y CMMI-DEV): ")
    
    add_body_p(doc, "En Colombia, la calidad se complementa con normas de obligatorio cumplimiento: ICONTEC NTC-ISO/IEC 25010 (adopción nacional), Ley Estatutaria 1581 de 2012 de la SIC (régimen especial de protección para menores de edad en plataformas escolares), Resolución 1519 de 2020 de MinTIC (accesibilidad web obligatoria WCAG 2.1 AA con atributos ARIA) y colCERT (mitigación de vulnerabilidades OWASP Top 10).", bold_prefix="4. Regulación Nacional Obligatoria en Colombia: ")
    
    # ARTEFACTOS DILIGENCIADOS
    add_styled_heading(doc, "4. Artefactos y Plantillas de Control de Calidad Diligenciados", level=1)
    add_body_p(doc, "A continuación se presentan los tres artefactos documentales obligatorios, completamente diligenciados con información real y verificable del proyecto:")
    
    add_styled_heading(doc, "4.1 Artefacto 1: Matriz de Evaluación de Calidad (ISO/IEC 25010)", level=2)
    headers_matriz = ["Característica", "Subcaracterística", "Criterio de Evaluación", "Métrica / Método", "Resultado Esperado", "Resultado Obtenido", "Estado"]
    data_matriz = [
        ["Seguridad", "Confidencialidad", "Hash criptográfico de contraseñas", "Inspección DB y settings.py", "100% hashes con sal", "100% Argon2id / PBKDF2", "CONFORME"],
        ["Seguridad", "Resistencia Ataques", "Protección fuerza bruta en login", "50 POST consecutivos", "Bloqueo tras 5 intentos", "Bloqueo HTTP 429 a 5to intento", "CONFORME"],
        ["Fiabilidad", "Disponibilidad", "Uptime mensual Render Cloud", "Fórmula Uptime estándar", "Disponibilidad >= 99.0%", "99.12% Uptime mensual", "CONFORME"],
        ["Fiabilidad", "Tolerancia Fallos", "Rollback ante errores masivos", "Inyección 3 filas corruptas", "0 corruptos insertados", "Rollback íntegro (savepoint)", "CONFORME"],
        ["Usabilidad", "Accesibilidad Web", "Pautas WCAG 2.1 AA (MinTIC)", "Google Lighthouse CI", "100% alerts con ARIA", "100% ARIA (Lighthouse: 96)", "CONFORME"],
        ["Usabilidad", "Operabilidad", "Tiempo registro notas RAPs", "Prueba con 5 docentes", "Tiempo <= 5 min / planilla", "Promedio: 3m 42s por planilla", "CONFORME"],
        ["Mantenibilidad", "Modularidad", "Líneas de código por vista", "Inspección views.py", "Líneas <= 250 por vista", "views.py acoplaba temas (Obs)", "OBSERVACIÓN"],
        ["Mantenibilidad", "Testabilidad", "Cobertura pruebas unitarias", "pytest y pytest-cov", "Cobertura >= 75%", "82.4% cobertura en módulos", "CONFORME"]
    ]
    build_table(doc, headers_matriz, data_matriz, [1.0, 1.0, 1.1, 1.1, 1.1, 1.2, 0.9], header_color="0F4C81")
    
    add_styled_heading(doc, "4.2 Artefacto 2: Formato de Solicitud de Cambio (Change Request - CR-ACAD-2026-005)", level=2)
    headers_cr = ["Campo de Control SCM", "Información Técnica del Registro Oficial"]
    data_cr = [
        ["ID del Cambio", "CR-ACAD-2026-005"],
        ["Título del Cambio", "Blindaje contra Fuerza Bruta en Autenticación y Accesibilidad ARIA en Login"],
        ["Fecha de Solicitud", "01 de Noviembre de 2026"],
        ["Solicitante / Rol", "Sofia Helena Torres — Líder de Aseguramiento de Calidad (SQA Lead)"],
        ["Tipo de Modificación", "Corrección de Seguridad (Bugfix) y Ajuste Normativo Legal (MinTIC)"],
        ["Nivel de Prioridad", "Urgente / Crítica (Afecta seguridad y cumplimiento normativo)"],
        ["Módulos Afectados", "apps/accounts/views.py, templates/accounts/login.html, requirements.txt"],
        ["Línea Base Afectada", "v2.5.0-baseline (Commit d97d7a6)"],
        ["Descripción Técnica", "1. Integración de django-ratelimit: límite de 5 intentos fallidos por IP / 15 min con respuesta HTTP 429.\n2. Adición de directivas semánticas role='alert' y aria-live='assertive' en login.html."],
        ["Justificación", "Subsanación de No Conformidad Mayor HAL-01 (OWASP A07) y No Conformidad Menor HAL-02 (Res. 1519/2020 MinTIC)."],
        ["Impacto y Riesgo", "Impacto bajo en arquitectura; riesgo medio-bajo de bloqueo indebido; latencia < 2ms."],
        ["Plan de Rollback", "Reversión mediante Git checkout a v2.5.0-baseline sobre apps/accounts/ y reinicio."],
        ["Decisión del CCB", "APROBADO POR UNANIMIDAD"],
        ["Firmas de Aprobación", "Julián Esteban Rocha (Líder Técnico) y Sofia Helena Torres (Líder SQA)"],
        ["Rama Git / PR", "Rama: feature/CR-005-login-ratelimit-aria | Pull Request: #143 (Merge a main)"],
        ["Nueva Línea Base", "v2.5.1-baseline (Commit f4b82e1)"]
    ]
    build_table(doc, headers_cr, data_cr, [2.2, 4.3], header_color="2E7D32")
    
    add_styled_heading(doc, "4.3 Artefacto 3: Lista de Verificación (Checklist) de Revisiones de Código Pre-Merge", level=2)
    headers_cl = ["#", "Categoría", "Criterio Específico de Verificación", "Estándar", "Estado", "Observación Técnica"]
    data_cl = [
        ["01", "Naming", "Clases PascalCase, variables y funciones snake_case", "PEP 8", "CUMPLE", "Modelos CustomUser, Student y vistas acordes"],
        ["02", "Naming", "URLs semánticas sin verbos redundantes", "Django URLs", "CUMPLE", "Rutas limpias /accounts/login/, /verify-report/"],
        ["03", "Excepciones", "Prohibición de bloques genéricos 'except Exception: pass'", "Clean Code", "CUMPLE", "Capturas explícitas de IntegrityError y ValidationError"],
        ["04", "Excepciones", "Mensajes comprensibles al usuario y registro en log", "ISO 25010", "CUMPLE", "Fallas registradas en AuditLog con IP y timestamp"],
        ["05", "Seguridad", "Protección contra Inyección SQL mediante ORM", "OWASP A03", "CUMPLE", "100% consultas parametrizadas con ORM de Django"],
        ["06", "Seguridad", "Token CSRF presente en todos los formularios POST", "OWASP A01", "CUMPLE", "Verificado {% csrf_token %} en todas las plantillas"],
        ["07", "Seguridad", "Cero contraseñas o secretos en duro (hardcoded)", "12-Factor", "CUMPLE", "Variables de entorno .env debidamente excluidas en git"],
        ["08", "Seguridad", "Hashes robustos para contraseñas de usuarios", "SIC Ley 1581", "CUMPLE", "Argon2id y PBKDF2 activos en CustomUser"],
        ["09", "Modularidad", "Lógica de cálculo en capas de servicio", "MVT Pattern", "CUMPLE", "Cálculo de RAPs extraído a CalculationService"],
        ["10", "Modularidad", "Funciones y vistas con extensión menor a 60 líneas", "PEP 8", "CUMPLE", "Métodos auxiliares implementados en vistas"],
        ["11", "Transacciones", "Operaciones críticas con transacciones atómicas ACID", "ISO 25010", "CUMPLE", "bulk_upload con savepoints garantizando consistencia"],
        ["12", "Accesibilidad", "Etiquetas label asociadas con 'for' a los inputs", "Res. 1519", "CUMPLE", "Subsanado en CR-005 con contraste 4.8:1"],
        ["13", "Accesibilidad", "Alertas provistas de role='alert' y aria-live", "WCAG 2.1 AA", "CUMPLE", "Subsanado en CR-005: lectores de pantalla asistidos"],
        ["14", "Protección Datos", "Cero exposición de datos de menores en QR público", "Ley 1581", "CUMPLE", "QR dinámico solo muestra estado y grado escolar"],
        ["15", "Pruebas", "Pruebas unitarias actualizadas para validar cambio", "IEEE 730", "CUMPLE", "4 pruebas unitarias de penetración en tests_spec_v2.py"],
        ["16", "Git SCM", "Commit semántico referenciando el CR", "IEEE 828", "CUMPLE", "Commit f4b82e1 referenciando formalmente CR-005"]
    ]
    build_table(doc, headers_cl, data_cl, [0.4, 1.0, 2.2, 0.9, 0.8, 1.2], header_color="0F4C81")
    
    add_callout(doc, "Dictamen del Revisor de Código: Se verificaron favorablemente los 16 criterios de la lista de chequeo sobre la rama feature/CR-005-login-ratelimit-aria. El código satisface estándares de seguridad, transaccionalidad, estilo PEP 8 y accesibilidad WCAG 2.1 AA. SE AUTORIZA EL MERGE A LA RAMA MAIN mediante Pull Request #143.", "APROBACIÓN DE INSPECCIÓN FORMAL")
    
    # SEGUIMIENTO Y NOVEDADES SCM
    add_styled_heading(doc, "5. Seguimiento, Control y Novedades del Producto (Fase Práctica SCM)", level=1)
    add_body_p(doc, "En cumplimiento de la Fase 3 formativa, se ejecutó la autoevaluación práctica sobre el código fuente, la simulación de cambios en el repositorio Git y la gestión formal de líneas base:")
    
    add_styled_heading(doc, "5.1 Novedades y Trazabilidad de Líneas Base (CSA)", level=2)
    headers_csa = ["Línea Base", "Commit Hash", "Fecha", "Estado CCB", "Descripción Técnica del Estado del Sistema"]
    data_csa = [
        ["v2.4.9-release", "3829cb0", "24-Oct-2026", "Aprobado", "Configuración de usuarios institucionales y persistencia en Render Cloud."],
        ["v2.5.0-baseline", "d97d7a6", "28-Oct-2026", "Aprobado", "Línea Base Inicial Auditada: Módulo de recuperación de contraseña finalizado."],
        ["v2.5.1-baseline", "f4b82e1", "02-Nov-2026", "Aprobado", "Línea Base Final Oficial: Cierre de CR-005 (Rate Limit y ARIA). Congelada."]
    ]
    build_table(doc, headers_csa, data_csa, [1.3, 1.0, 1.0, 1.0, 2.2], header_color="2E7D32")
    
    add_body_p(doc, "La simulación demostró el flujo completo de SCM: detección de la brecha en la autoevaluación -> diligenciamiento del formato CR-ACAD-2026-005 -> aprobación del CCB -> creación de rama temática feature/CR-005-login-ratelimit-aria -> implementación -> apertura de Pull Request #143 -> diligenciamiento de Checklist de 16 puntos -> aprobación y merge -> congelamiento de la nueva línea base v2.5.1-baseline.")
    
    # AUDITORÍA INTERNA Y HALLAZGOS
    add_styled_heading(doc, "6. Auditoría Interna de Calidad: Inspección, Hallazgos y Causa Raíz", level=1)
    add_body_p(doc, "Se ejecutó la auditoría interna aplicando técnicas SAST (Bandit), inspección de linters (flake8/black), análisis dinámico de penetración y pruebas de accesibilidad con Google Lighthouse CI. Se levantaron 8 hallazgos formales:")
    
    headers_findings = ["ID", "Clasificación", "Norma / Requisito", "Módulo", "Descripción Técnica del Hallazgo", "Riesgo", "Estado"]
    data_findings = [
        ["HAL-01", "NC Mayor", "ISO 25010 / OWASP A07", "apps.accounts", "Ausencia de rate limit en login: peticiones POST infinitas.", "ALTO", "CERRADO"],
        ["HAL-02", "NC Menor", "MinTIC Res. 1519 / WCAG", "templates/accounts", "Alertas sin atributos semánticos role='alert' y aria-live.", "MEDIO", "CERRADO"],
        ["HAL-03", "NC Menor", "ISO 25010 Adecuación", "apps.periods", "Permisividad en fechas límite de periodos cerrados.", "MEDIO", "CERRADO"],
        ["HAL-04", "Obs. Mejora", "ISO 25010 Mantenibilidad", "apps.accounts", "Vistas densas (Fat Views): views.py acoplaba temas escolares.", "BAJO", "PROGRAMADO"],
        ["HAL-05", "Obs. Mejora", "ISO 25010 Seguridad", "templates/students", "Validación MIME frontend ausente antes de subir Excel.", "BAJO", "PROGRAMADO"],
        ["HAL-06", "Fortaleza", "SIC Ley 1581 / ISO 25010", "apps.reports", "Verificación QR dinámica con cero exposición de datos de menores.", "DESTACADO", "CONFORME"],
        ["HAL-07", "Fortaleza", "ISO 25010 Fiabilidad", "apps.students", "Savepoints atómicos ACID con rollback ante fallos en carga.", "DESTACADO", "CONFORME"],
        ["HAL-08", "Fortaleza", "ISO 25010 Exactitud", "apps.grades", "Cálculo ponderado de notas RAPs exacto al 100.00% con redondeo.", "DESTACADO", "CONFORME"]
    ]
    build_table(doc, headers_findings, data_findings, [0.7, 0.9, 1.2, 1.0, 1.7, 0.6, 0.7], header_color="0F4C81")
    
    add_styled_heading(doc, "6.1 Análisis de Causa Raíz (5 Porqués e Ishikawa)", level=2)
    add_body_p(doc, "Para la No Conformidad Mayor HAL-01 (Fuerza Bruta en Login):")
    add_body_p(doc, "1. ¿Por qué el sistema no bloqueaba las peticiones consecutivas? Porque login_view procesaba directamente cada petición contra authenticate().")
    add_body_p(doc, "2. ¿Por qué no había limitador de tasa? Porque Django delega la limitación a middlewares o cachés que deben configurarse explícitamente.")
    add_body_p(doc, "3. ¿Por qué no se configuró? Porque no se incluyó un Requerimiento No Funcional (RNF) explícito de seguridad en la planificación del sprint.")
    add_body_p(doc, "4. ¿Por qué no se incluyó el RNF? Porque el equipo priorizó la autenticación multi-colegio y la recuperación de contraseñas.")
    add_body_p(doc, "5. Causa Raíz: Ausencia de un protocolo formal de verificación de requerimientos no funcionales de ciberseguridad basados en OWASP Top 10 durante la planificación del sprint.", italic=True)
    
    # PLAN CAPA
    add_styled_heading(doc, "7. Plan de Acciones Correctivas y Preventivas (CAPA — IEEE 730)", level=1)
    add_body_p(doc, "Para erradicar las causas raíz y subsanar las no conformidades, se implementó el Plan CAPA:")
    
    headers_capa = ["Código", "Hallazgo", "Tipo", "Medida Técnica Implementada", "Responsable", "Plazo", "Evidencia de Cierre"]
    data_capa = [
        ["AC-01", "HAL-01", "Correctiva", "Integrar django-ratelimit (5 peticiones/minuto por IP con HTTP 429).", "Julián Rocha", "24 Horas", "Petición 6 bloqueada en test de estrés y log en AuditLog."],
        ["AC-02", "HAL-02", "Correctiva", "Agregar role='alert', aria-live y labels vinculados en login.html.", "David Morales", "24 Horas", "Lighthouse Accessibility elevado de 88 a 96/100."],
        ["AC-03", "HAL-03", "Correctiva", "Decorador @period_is_open_required y validación is_locked en BD.", "Julián Rocha", "48 Horas", "ValidationError ante intentos de edición en periodos cerrados."],
        ["AP-01", "HAL-04", "Preventiva", "Trasladar configuración temática a context_processors.py.", "Equipo Dev", "Sprint 5", "Reducción de 85 líneas acopladas en views.py."],
        ["AP-02", "HAL-05", "Preventiva", "Validador JavaScript de firma binaria MIME en carga de estudiantes.", "David Morales", "Sprint 5", "Bloqueo preventivo en navegador de archivos inválidos."]
    ]
    build_table(doc, headers_capa, data_capa, [0.7, 0.7, 0.8, 1.8, 0.9, 0.7, 1.3], header_color="2E7D32")
    
    # PREPARACIÓN AUDITORÍA EXTERNA SENA
    add_styled_heading(doc, "8. Preparación para la Auditoría Externa del Instructor SENA", level=1)
    add_body_p(doc, "A fin de asegurar el éxito en la sustentación y evaluación presencial del instructor, el equipo estructuró el banco de respuestas técnicas y el inventario de evidencias verificables:")
    
    add_styled_heading(doc, "8.1 Banco de Preguntas Técnicas y Respuestas Fundamentadas", level=2)
    add_body_p(doc, "Garantizamos el cumplimiento mediante cuatro barreras de control técnico: primero, almacenamiento criptográfico irreversible de credenciales con Argon2id y PBKDF2; segundo, control de acceso basado en roles (RBAC) que aísla los expedientes académicos para que solo docentes y acudientes autorizados accedan a ellos; tercero, la verificación pública de boletines mediante código QR utiliza un identificador UUIDv4 con firma SHA-256 sin divulgar números de documento, teléfonos ni historiales convivenciales; y cuarto, los registros de auditoría institucional anonimizan datos confidenciales en entornos de desarrollo y logs.", bold_prefix="P1: ¿De qué manera ACADEMIX acata la Ley 1581 de 2012 respecto a los datos de estudiantes menores de edad?\n")
    
    add_body_p(doc, "Seleccionamos dos subcaracterísticas nucleares: Exactitud Funcional y Tolerancia a Fallos. En exactitud funcional, auditamos el cálculo ponderado de notas RAPs al 100.00% con redondeo a dos decimales, logrando un 100% de coincidencia matemática en 50 casos de prueba con pytest. En tolerancia a fallos, evaluamos la transaccionalidad atómica ACID en la carga masiva de estudiantes: inyectamos 3 filas corruptas en un Excel de 100 registros y el sistema ejecutó rollback íntegro sin corromper la base de datos.", bold_prefix="P2: ¿Qué métricas de ISO/IEC 25010 seleccionaron para evaluar la fiabilidad y qué resultados obtuvieron?\n")
    
    add_body_p(doc, "La auditoría interna detectó una No Conformidad Mayor (HAL-01) en el módulo de autenticación: la ausencia de limitación de tasa contra ataques de fuerza bruta. Asimismo, detectó una No Conformidad Menor (HAL-02) por falta de atributos semánticos ARIA en los mensajes de error según la Resolución 1519 de MinTIC. Activamos el Plan CAPA y tramitamos formalmente la Solicitud de Cambio CR-ACAD-2026-005, implementando un limitador en memoria caché de 5 intentos por minuto por IP con código HTTP 429, y actualizamos las plantillas HTML elevando el puntaje de accesibilidad Lighthouse a 96/100. Todo el proceso fue validado en el Pull Request #143 y congelado en la línea base v2.5.1-baseline.", bold_prefix="P3: ¿Cuáles fueron los hallazgos críticos de la auditoría interna y cómo se subsanaron?\n")
    
    add_body_p(doc, "Adoptamos GitFlow para asegurar que la rama main sea inmutable y siempre represente código estable en producción. Ningún desarrollador puede realizar commits directos a main. Toda modificación se implementa en ramas temáticas (feature/ o fix/) y se somete a un Pull Request formal. La Lista de Verificación de Código de 16 ítems actúa como un filtro de calidad que obliga a verificar estándares PEP 8, transaccionalidad atómica, ausencia de inyecciones SQL/XSS, cobertura de pruebas unitarias >= 80% y directrices de protección de datos de la SIC antes de autorizar la fusión.", bold_prefix="P4: ¿Por qué adoptaron GitFlow y qué garantiza el Checklist en los Merges a main?\n")
    
    add_styled_heading(doc, "8.2 Inventario de Evidencias Verificables en Repositorio", level=2)
    headers_evidencias = ["#", "Artefacto o Evidencia Técnica", "Ubicación en Repositorio", "Estado"]
    data_evidencias = [
        ["01", "Código Fuente Modular en Django 5.x", "c:\\Academix\\apps\\", "VERIFICADO"],
        ["02", "Historial de Commits Semánticos y Ramas Git", "git log --oneline --graph", "VERIFICADO"],
        ["03", "Etiquetas de Línea Base v2.5.0 y v2.5.1", "git tag -l", "VERIFICADO"],
        ["04", "Matriz de Calidad ISO 25010 Cuantitativa", "docs/INFORME_FINAL_GESTION_CALIDAD_Y_AUDITORIA_ACADEMIX.docx", "VERIFICADO"],
        ["05", "Formatos de Solicitud de Cambio CR-004 y CR-005", "Tramitados y aprobados por CCB", "VERIFICADO"],
        ["06", "Checklist de Revisiones de Código diligenciado", "Pull Request #143 en GitHub", "VERIFICADO"],
        ["07", "Suite de Pruebas Unitarias automatizadas", "apps/accounts/tests.py, tests_spec_v2.py (pytest)", "VERIFICADO"],
        ["08", "Reportes de Seguridad SAST y Linters PEP 8", "Bandit, flake8, black", "VERIFICADO"],
        ["09", "Auditoría de Accesibilidad Web (96/100)", "Google Lighthouse CI y axe DevTools", "VERIFICADO"],
        ["10", "Despliegue en Vivo en la Nube y Script Local", "Render Cloud HTTPS / iniciar_servidor_red.bat", "VERIFICADO"]
    ]
    build_table(doc, headers_evidencias, data_evidencias, [0.5, 3.2, 2.3, 0.8], header_color="0F4C81")
    
    # DICTAMEN FINAL Y CONCLUSIONES
    add_styled_heading(doc, "9. Dictamen Final de Calidad y Conclusiones de la Organización", level=1)
    
    add_callout(doc, "DICTAMEN OFICIAL DEL EQUIPO AUDITOR INTERNO: CONFORME SATISFACTORIO — APTO PARA AUDITORÍA EXTERNA\n\nHabiendo verificado el cierre efectivo de las acciones correctivas AC-01 y AC-02 (hallazgos HAL-01 y HAL-02), la consolidación de la línea base v2.5.1-baseline en el commit f4b82e1, y el cumplimiento de ISO/IEC 25010, IEEE 730, IEEE 828, CMMI Nivel 2 y la legislación colombiana (Ley 1581 de 2012 y Res. 1519 de 2020 MinTIC), la empresa formativa dictamina que la plataforma ACADEMIX se encuentra 100% PREPARADA Y APTA para someterse con éxito a la Auditoría Externa de Evaluación por parte del Instructor Técnico SENA.", "DECLARACIÓN OFICIAL DE CONFORMIDAD")
    
    add_body_p(doc, "Firmas de Responsabilidad del Proceso:")
    add_body_p(doc, "• Sofia Helena Torres — Líder de Aseguramiento de Calidad (SQA Lead) [Firma Registrada]")
    add_body_p(doc, "• Julián Esteban Rocha — Líder Técnico y de Arquitectura (CCB Lead) [Firma Registrada]")
    add_body_p(doc, "• David Camilo Morales — Líder de Pruebas y Experiencia de Usuario (UX) [Firma Registrada]")
    add_body_p(doc, "• Fecha de Emisión Oficial: 09 de Noviembre de 2026")
    
    # REFERENCIAS
    add_styled_heading(doc, "10. Referencias Bibliográficas (Normas APA 7.ª Edición)", level=1)
    refs = [
        "CMMI Institute. (2018). CMMI for Development, Version 2.0 (CMMI-DEV v2.0). Carnegie Mellon University.",
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012: Por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587.",
        "Instituto Colombiano de Normas Técnicas y Certificación [ICONTEC]. (2013). Norma Técnica Colombiana NTC-ISO/IEC 25010: Ingeniería de software - Requisitos de calidad y evaluación de software (SQuaRE) - Modelos de calidad de sistemas y software. Bogotá: ICONTEC.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2008). IEEE Std 1028-2008: IEEE Standard for Software Reviews and Audits. Nueva York: IEEE Computer Society.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2012). IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering. Nueva York: IEEE Computer Society.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2014). IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes. Nueva York: IEEE Computer Society.",
        "International Organization for Standardization [ISO]. (2018). ISO 19011:2018: Guidelines for auditing management systems. Ginebra: ISO.",
        "International Organization for Standardization [ISO]. (2023). ISO/IEC 25010:2023: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model. Ginebra: ISO.",
        "Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). Resolución 1519 de 2020: Por la cual se determinan los estándares y directrices para publicar la información señalada en la Ley 1712 del 2014 y se definen los criterios de accesibilidad web. Bogotá: MinTIC.",
        "OWASP Foundation. (2021). OWASP Top 10: The Ten Most Critical Web Application Security Risks. Open Web Application Security Project.",
        "Servicio Nacional de Aprendizaje [SENA]. (2024). Diseño Curricular del Programa Tecnólogo en Análisis y Desarrollo de Software (ADSO). Dirección de Formación Profesional, Bogotá D.C.",
        "Superintendencia de Industria y Comercio [SIC]. (2021). Circular Externa 002 de 2021: Instrucciones para la adopción de medidas de seguridad en el tratamiento de datos personales de menores de edad. Bogotá: SIC."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        run_ref = p_ref.add_run(r)
        run_ref.font.name = 'Arial'
        run_ref.font.size = Pt(9.5)
        run_ref.font.color.rgb = RGBColor(60, 60, 60)
        
    doc.save(output_path)
    print(f"[OK] Documento consolidado generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Academix\docs\INFORME_FINAL_GESTION_CALIDAD_Y_AUDITORIA_ACADEMIX.docx"
    generate_consolidated_docx(out_file)

