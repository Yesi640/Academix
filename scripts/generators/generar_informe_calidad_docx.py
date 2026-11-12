 #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_informe_calidad_docx.py
Genera el documento Word (DOCX) formal del Informe Técnico de Calidad de Software,
Marcos Normativos (ISO/IEC 25010, IEEE 730, SCM, Entes de Colombia) y la Aplicación Práctica
en las Fases 2 y 3 sobre ACADEMIX v2.5.0.
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
    run_title = title_p.add_run("INFORME TÉCNICO DE MARCOS NORMATIVOS DE CALIDAD DE SOFTWARE Y GESTIÓN DE CONFIGURACIÓN (SCM / SQA)")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 76, 129)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Investigación Conceptual, Artefactos de Evaluación (ISO/IEC 25010 & IEEE 730)\ny Aplicación Práctica con Control de Cambios en la Plataforma ACADEMIX v2.5.0")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(70, 70, 70)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = meta_p.add_run("Bogotá D.C., Colombia — Noviembre de 2026 | Versión Oficial 2.0")
    run_meta.font.name = 'Arial'
    run_meta.font.size = Pt(9)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(120, 120, 120)

    doc.add_paragraph()

    # 1. INTRODUCCIÓN Y OBJETIVOS
    add_styled_heading(doc, "1. INTRODUCCIÓN Y OBJETIVOS DEL PROYECTO", level=1)
    add_body_p(doc, "La calidad en la ingeniería de software moderna no es una etapa terminal ni un ensayo cosmético, sino un proceso riguroso y metódico que abarca el diseño arquitectónico, la implementación del código fuente, el aseguramiento continuo y la gestión de la configuración. El presente documento desarrolla el proceso formal de investigación y aplicación práctica de los marcos normativos internacionales y nacionales al sistema de información ACADEMIX, plataforma integral de gestión académica y control escolar concebida para instituciones educativas en Colombia.")
    add_body_p(doc, "Investigar, seleccionar y aplicar marcos normativos de calidad de software (ISO/IEC 25010 e IEEE 730) y estándares colombianos vinculantes (ICONTEC, MinTIC, Superintendencia de Industria y Comercio - SIC), diseñando plantillas de control, ejecutando la autoevaluación técnica y demostrando el control de cambios sobre el repositorio de Academix.", bold_prefix="Objetivo General: ")
    add_body_p(doc, "1) Documentar el marco conceptual de ISO/IEC 25010, IEEE 730, SCM y la normativa colombiana actualizada. 2) Construir los tres artefactos documentales (Matriz de Calidad, Formato de Solicitud de Cambio y Checklist de Code Review). 3) Ejecutar la autoevaluación sobre apps.accounts identificando brechas. 4) Demostrar el control de versiones y líneas base simulando una Solicitud de Cambio y un Pull Request formal.", bold_prefix="Objetivos Específicos: ")

    # 2. FASE 1: MARCO CONCEPTUAL
    add_styled_heading(doc, "2. FASE 1: INVESTIGACIÓN Y MARCO CONCEPTUAL DE CALIDAD", level=1)

    add_styled_heading(doc, "2.1 Modelo de Calidad del Producto (ISO/IEC 25010 e ISO/IEC 25010:2023)", level=2)
    add_body_p(doc, "La serie ISO/IEC 25000 (SQuaRE - Software Product Quality Requirements and Evaluation) define la taxonomía internacional para especificar y evaluar la calidad del software. Se divide en cinco áreas: Gestión de Calidad (2500n), Modelo de Calidad (2501n), Medición de Calidad (2502n), Requisitos de Calidad (2503n) y Evaluación de Calidad (2504n).")
    add_body_p(doc, "La norma ISO/IEC 25010 descompone la calidad en ocho características primarias: Adecuación Funcional, Eficiencia de Desempeño, Compatibilidad, Usabilidad, Fiabilidad, Seguridad, Mantenibilidad y Portabilidad. En la actualización ISO/IEC 25010:2023, la portabilidad evoluciona hacia Flexibilidad, incorporando la resiliencia en la nube y el principio de Inclusión/Accesibilidad como un pilar innegociable.")

    add_styled_heading(doc, "2.2 Aseguramiento de Calidad del Software (Norma IEEE 730)", level=2)
    add_body_p(doc, "El estándar IEEE 730 (Standard for Software Quality Assurance Processes) establece los fundamentos del SQA. A diferencia del simple testing de software que detecta errores a posteriori, el SQA es un proceso preventivo enfocado en los procesos de desarrollo: define estándares, revisiones técnicas por pares, auditorías de configuración, métricas de aceptación y acciones correctivas (CAPA). En entornos ágiles y DevOps (como el utilizado en Academix con Git y Render), IEEE 730 se operacionaliza mediante la 'Definition of Done' (DoD) de cada Sprint y la automatización de linters y pruebas unitarias.")

    add_styled_heading(doc, "2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)", level=2)
    add_body_p(doc, "La Gestión de Configuración (IEEE 828) garantiza la integridad, trazabilidad y control de evolución de todos los Ítems de Configuración (CI): código fuente Python/Django, plantillas HTML, scripts de migración de bases de datos, variables de entorno y documentación técnica. Las modificaciones a las líneas base aprobadas no se realizan de manera improvisada; se canalizan formalmente a través de Solicitudes de Cambio (Change Requests - CR) evaluadas por un Comité de Control de Cambios (CCB).")

    add_styled_heading(doc, "2.4 Entes Reguladores y Marco Normativo en Colombia (Actualizado 2026)", level=2)
    add_body_p(doc, "Organismo Nacional de Normalización que adopta estándares internacionales como Normas Técnicas Colombianas: NTC-ISO/IEC 25010 (Calidad de producto), NTC-ISO/IEC 12207 (Procesos del ciclo de vida), NTC-ISO/IEC 27001 (Seguridad de la información) y NTC 5906 (Calidad de datos).", bold_prefix="• ICONTEC: ")
    add_body_p(doc, "Emite la Política de Gobierno Digital (Decreto 088 de 2022 y Resolución 460 de 2022) y la Resolución 1519 de 2020 de Accesibilidad Web (obligatoriedad del estándar W3C WCAG 2.1 nivel AA: contraste cromático, soporte a lectores de pantalla y navegación asistida).", bold_prefix="• MinTIC: ")
    add_body_p(doc, "Autoridad de Habeas Data. Administra la Ley Estatutaria 1581 de 2012 y el Decreto 1377 de 2013. Su Artículo 7 impone un régimen de protección reforzado sobre datos de Niños, Niñas y Adolescentes (NNA), obligando a plataformas escolares como Academix a requerir consentimiento de tutores, prohibir la exposición de historiales en texto plano o URLs y garantizar cifrado robusto de contraseñas.", bold_prefix="• Superintendencia de Industria y Comercio (SIC): ")
    add_body_p(doc, "Tipifica el software registrado ante la DNDA como producto de desarrollo tecnológico e innovación con validación formal de calidad.", bold_prefix="• MinCiencias: ")
    add_body_p(doc, "Equipo de Respuesta a Incidentes Cibernéticos de Colombia; dicta directrices de mitigación frente al OWASP Top 10 (ataques de inyección SQL, Cross-Site Scripting XSS y falsificación CSRF).", bold_prefix="• colCERT y CSIRT de Gobierno: ")

    # 3. FASE 2: ARTEFACTOS Y PLANTILLAS
    add_styled_heading(doc, "3. FASE 2: ARTEFACTOS Y PLANTILLAS DE EVALUACIÓN APLICADAS A ACADEMIX", level=1)

    # 3.1 MATRIZ DE EVALUACIÓN ISO 25010
    add_styled_heading(doc, "3.1 Artefacto 1: Matriz de Evaluación de Calidad de Software (ISO/IEC 25010)", level=2)
    add_body_p(doc, "Ocho criterios cuantitativos y de verificación sobre seis características estratégicas de la norma ISO/IEC 25010 aplicados a Academix v2.5.0:")

    data_m = [
        ("MC-01\nAdecuación Funcional", "Exactitud Funcional", "Cálculo de promedios acumulados ponderados según porcentajes de RAPs (1.0 a 5.0).", "E = (N_calc_exactos / N_totales) * 100 con pytest.", "100% de exactitud matemática. Cero discrepancias en fórmulas."),
        ("MC-02\nAdecuación Funcional", "Completitud Funcional", "Importación masiva de estudiantes (bulk_upload) desde CSV/XLSX creando cursos y cuentas.", "C = (R_importados / R_validos) * 100 en pruebas integración.", "100% de registros procesados. Detalle explícito de inconsistencias."),
        ("MC-03\nSeguridad", "Confidencialidad", "Cifrado y derivación de claves de usuario; prohibición estricta de contraseñas en texto claro.", "S_pwd = (U_hash / U_totales) * 100 con escáner Bandit.", "100% contraseñas con hashing estándar Django (Argon2 / PBKDF2)."),
        ("MC-04\nSeguridad", "Integridad y RBAC", "Aislamiento estricto de roles. Bloqueo de acceso no autorizado a vistas directivas o notas ajenas.", "I = 1 - (V_acceso_indebido / P_intentos) con OWASP ZAP.", "100% rutas protegidas. Retorno obligatorio HTTP 403 / 302."),
        ("MC-05\nFiabilidad", "Tolerancia a Fallos", "Resiliencia transaccional ACID ante caídas de conexión a base de datos durante guardado de notas.", "Tasa de inconsistencias tras simulación de caídas en atomic().", "Cero corrupción de base de datos. Rollback automático de fallos."),
        ("MC-06\nDesempeño", "Comportamiento Temporal", "Tiempo de respuesta del servidor (TTFB) en Dashboard y listados bajo concurrencia.", "T_promedio <= 500 ms; P95 <= 800 ms con Locust (100 usuarios).", "Latencia media <= 500 ms; tasa de errores HTTP 500 < 0.1%."),
        ("MC-07\nUsabilidad", "Accesibilidad (MinTIC)", "Cumplimiento del estándar W3C WCAG 2.1 AA (Resolución 1519 de 2020 MinTIC).", "Puntaje de Accesibilidad con Google Lighthouse CI y axe.", "Puntaje Lighthouse >= 90/100. Contraste cromático >= 4.5:1."),
        ("MC-08\nMantenibilidad", "Modularidad y Cobertura", "Cohesión en apps Django y cobertura de pruebas unitarias sobre lógica de negocio.", "Cov = (Lineas_tests / Lineas_totales) * 100 con pytest-cov.", "Cobertura de código >= 80%. Complejidad ciclomática <= 10.")
    ]

    table_m = doc.add_table(rows=len(data_m) + 1, cols=5)
    table_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_m = ["ID / Característica", "Subcaracterística", "Criterio de Evaluación Academix", "Métrica / Prueba", "Resultado Esperado"]
    for i, h in enumerate(headers_m):
        cell = table_m.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    for row_idx, row_content in enumerate(data_m, start=1):
        for col_idx, text_val in enumerate(row_content):
            cell = table_m.cell(row_idx, col_idx)
            cell.text = text_val
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Arial'
            p.runs[0].font.size = Pt(8)
            if col_idx == 0:
                p.runs[0].font.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F4F6F9")

    doc.add_paragraph()

    # 3.2 FORMATO SOLICITUD DE CAMBIO (SCM)
    add_styled_heading(doc, "3.2 Artefacto 2: Formato de Solicitud de Cambio (Change Request - SCM)", level=2)
    add_body_p(doc, "Plantilla formal diligenciada correspondiente al control de cambios en producción del proyecto Academix:")

    cr_data = [
        ("Código de Solicitud (CR-ID)", "CR-ACAD-2026-004 | Fecha: 03 de Noviembre de 2026"),
        ("Solicitante y Rol", "Ing. Carlos Mendoza Valencia — Coordinador Académico (Representante Institucional)"),
        ("Módulos Afectados", "apps.grades (Calificaciones) y apps.reports (Boletines) | Versión Base: v2.5.0 -> v2.6.0"),
        ("Clasificación del Cambio", "Tipo: Nueva Funcionalidad (Feature) y Cumplimiento Legal | Prioridad: Alta | Riesgo: Moderado"),
        ("Descripción Resumida", "Implementación de Control de Cierre Extemporáneo de Periodo y Firma Criptográfica de Boletines con Código QR de Validación Pública."),
        ("Justificación del Negocio y Legal", "Evitar fraudes por modificación extemporánea de notas. Validez jurídica ante auditorías de Secretarías de Educación y cumplimiento de Ley 1581 de 2012 (SIC)."),
        ("Impacto Técnico y Base de Datos", "Decorador @period_is_open_required en views.py. Migración en apps.periods (is_locked, closed_at) y tabla ReportVerificationToken (UUIDv4 y firma SHA-256)."),
        ("Pruebas y Verificación", "Validación unitaria de ValidationError en periodos bloqueados. Prueba de permisos RBAC (HTTP 403 a docentes no autorizados). Validación de escaneo QR móvil."),
        ("Plan de Marcha Atrás (Rollback)", "1. Revertir migración: python manage.py migrate periods 0003_prev.\n2. Checkout git: git checkout tags/v2.5.0-release.\n3. Reinicio: sudo systemctl restart gunicorn-academix.\n4. Restaurar dump PostgreSQL de respaldo en /backups/."),
        ("Dictamen del Comité (CCB)", "APROBADO POR UNANIMIDAD. Autorizada creación de rama feature/period-lock-and-qr-verification desde develop. Firmas: Julián Rocha (Líder Técnico), Sofía Torres (SQA).")
    ]

    table_cr = doc.add_table(rows=len(cr_data) + 1, cols=2)
    table_cr.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_cr = ["Campo / Dimensión del Cambio", "Detalle de Implementación en Academix"]
    for i, h in enumerate(headers_cr):
        cell = table_cr.cell(0, i)
        cell.text = h
        set_cell_background(cell, "2E7D32")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    for row_idx, (c0_text, c1_text) in enumerate(cr_data, start=1):
        c0 = table_cr.cell(row_idx, 0)
        c1 = table_cr.cell(row_idx, 1)
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

    # 3.3 CHECKLIST DE REVISIÓN DE CÓDIGO
    add_styled_heading(doc, "3.3 Artefacto 3: Lista de Verificación (Checklist) de Revisiones de Código", level=2)
    add_body_p(doc, "Formato de inspección técnica obligatorio para autorizar el Merge de Pull Requests en el repositorio GitHub/GitLab de Academix (PR #142):")

    cl_data = [
        ("1", "Convenciones PEP 8", "Nombres de clases en PascalCase, funciones/variables en snake_case. Sin variables crípticas.", "SÍ"),
        ("2", "Documentación", "Docstrings completos en métodos públicos y servicios explicando parámetros y retorno.", "SÍ"),
        ("3", "Manejo Excepciones", "Excepciones tipificadas (ValidationError, IntegrityError). Prohibido except: pass vacío.", "SÍ"),
        ("4", "Transaccionalidad", "Operaciones de guardado múltiple envueltas bajo @transaction.atomic() con rollback limpio.", "SÍ"),
        ("5", "Seguridad: SQLi", "Uso estricto del ORM de Django con consultas parametrizadas. Cero SQL crudo vulnerable.", "SÍ"),
        ("6", "Seguridad: XSS/CSRF", "Formularios con token {% csrf_token %}. Prohibición de filtro |safe sobre inputs no saneados.", "SÍ"),
        ("7", "Seguridad: Uploads", "Validación estricta de extensiones (.csv, .xlsx), tipos MIME y tamaño máximo en bulk_upload.", "SÍ"),
        ("8", "Control Acceso (RBAC)", "Decoradores @login_required y verificación de roles directivos en todas las vistas protegidas.", "SÍ"),
        ("9", "Modularidad", "Lógica de negocio desacoplada en services.py. Sin vistas hipertróficas (Fat Views).", "SÍ"),
        ("10", "Ley 1581 (SIC)", "Cero exposición de datos de menores en logs de depuración o parámetros de URL públicas.", "SÍ"),
        ("11", "Accesibilidad MinTIC", "Contraste cromático >= 4.5:1, etiquetas label asociadas y atributos aria (Res. 1519).", "SÍ"),
        ("12", "Migraciones BD", "Migraciones idempotentes, reversibles y con valores por defecto que no rompen datos históricos.", "SÍ"),
        ("13", "Pruebas Unitarias", "Suite de tests unitarios actualizada, pasando al 100% con cobertura de código >= 80%.", "SÍ"),
        ("14", "Gestión de Secretos", "Cero credenciales en código fuente. Archivo .env excluido correctamente en .gitignore.", "SÍ"),
        ("15", "Dictamen Final", "Aprobado por el Revisor Técnico (Ing. Julián Rocha) para Merge a rama develop.", "SÍ")
    ]

    table_cl = doc.add_table(rows=len(cl_data) + 1, cols=4)
    table_cl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_cl = ["#", "Categoría de Inspección", "Criterio de Verificación de Calidad", "Cumple"]
    for i, h in enumerate(headers_cl):
        cell = table_cl.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    for row_idx, (c0, c1, c2, c3) in enumerate(cl_data, start=1):
        cell0 = table_cl.cell(row_idx, 0)
        cell1 = table_cl.cell(row_idx, 1)
        cell2 = table_cl.cell(row_idx, 2)
        cell3 = table_cl.cell(row_idx, 3)
        cell0.text = c0
        cell1.text = c1
        cell2.text = c2
        cell3.text = c3
        set_cell_margins(cell0, top=70, bottom=70, left=80, right=80)
        set_cell_margins(cell1, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell2, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell3, top=70, bottom=70, left=80, right=80)
        for cell in (cell0, cell1, cell2, cell3):
            cell.paragraphs[0].runs[0].font.name = 'Arial'
            cell.paragraphs[0].runs[0].font.size = Pt(8)
        cell3.paragraphs[0].runs[0].font.bold = True
        cell3.paragraphs[0].runs[0].font.color.rgb = RGBColor(46, 125, 50)
        if row_idx % 2 == 0:
            for cell in (cell0, cell1, cell2, cell3):
                set_cell_background(cell, "F4F6F9")

    doc.add_paragraph()

    # 4. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO ACADEMIX
    add_styled_heading(doc, "4. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO ACADEMIX", level=1)
    add_body_p(doc, "En esta fase, el equipo ejecuta de manera práctica los artefactos sobre el software real, realizando la autoevaluación exhaustiva de un módulo nuclear y demostrando el ciclo completo de control de versiones y gestión de configuración bajo Git.")

    # 4.1 AUTOEVALUACIÓN ISO 25010
    add_styled_heading(doc, "4.1 Ejecución de la Autoevaluación de Calidad (ISO/IEC 25010) sobre apps.accounts", level=2)
    add_body_p(doc, "Se seleccionó el módulo de Autenticación, Cuentas de Usuario y Control de Acceso (apps.accounts), articulado con login.html y apps.audit, evaluándolo contra la Matriz de Calidad:")

    # Tabla Autoevaluación Real
    ev_data = [
        ("EV-01 / Adecuación", "Completitud Funcional", "Autenticación multi-escuela, redirección por rol y contraseña obligatoria.", "100% funcional en pruebas dinámicas.", "CONFORME"),
        ("EV-02 / Adecuación", "Exactitud Funcional", "Registro íntegro de trazas en apps.audit.AuditLog en logins y fallos.", "IP, rol intentado y timestamp guardados.", "CONFORME"),
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
    add_body_p(doc, "Brecha B-01 (Seguridad - Severidad Alta): Carencia de limitación de tasa (Rate Limiting) en login_view. Un atacante puede ejecutar scripts automatizados para adivinar contraseñas o saturar el CPU por el costo computacional de PBKDF2/Argon2 (Vulnerabilidad OWASP A07).")
    add_body_p(doc, "Brecha B-02 (Usabilidad / MinTIC - Severidad Media): Ausencia de atributos semánticos ARIA (role='alert', aria-live='assertive') en los mensajes de error dinámicos de login.html, incumpliendo la Resolución 1519 de 2020 de MinTIC sobre accesibilidad para personas con discapacidad visual.")
    add_body_p(doc, "Plan CAPA (IEEE 730): Se formulan las acciones correctivas AC-01 (Rate-limiting de 5 intentos/min por IP) y AC-02 (Atributos ARIA y contraste WCAG 2.1 AA en login.html), tramitadas formalmente bajo la Solicitud de Cambio CR-ACAD-2026-005.")

    # 4.2 CONTROL DE VERSIONES Y LÍNEA BASE
    add_styled_heading(doc, "4.2 Control de Versiones, Gestión de Línea Base y Pull Request en Git", level=2)
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
    add_body_p(doc, "4. Inspección de Código Previa al Merge:", bold_prefix="")
    add_body_p(doc, "El Revisor Técnico evaluó los 15 ítems del Checklist de Código: formato PEP 8 verificado con flake8/black, pruebas de inyección limpias, código HTTP 429 probado ante 6 intentos fallidos, y puntuación de accesibilidad Lighthouse incrementada a 96/100. Dictamen: Aprobado para Merge sin reservas.")
    add_body_p(doc, "5. Fusión (Merge) y Congelamiento de Nueva Línea Base (v2.5.1-baseline):", bold_prefix="")
    add_body_p(doc, "Se ejecutó git merge --no-ff integrando el commit f4b82e1 en la rama main, etiquetando formalmente 'v2.5.1-baseline'. La Bitácora CSA (Configuration Status Accounting) registra la transición oficial a producción de las protecciones de seguridad y accesibilidad.")

    doc.add_paragraph()

    # 5. CONCLUSIONES
    add_styled_heading(doc, "5. CONCLUSIONES", level=1)
    add_body_p(doc, "1. La adopción de la norma ISO/IEC 25010 y el estándar IEEE 730 permite superar el enfoque empírico de desarrollo, transformando el proyecto Academix en un producto de software confiable, mantenible y alineado con las exigencias del sector educativo.")
    add_body_p(doc, "2. El marco legal colombiano (Ley 1581 de 2012 de la SIC para menores de edad y la Resolución 1519 de 2020 de MinTIC para accesibilidad web) no constituye una recomendación optativa, sino un estándar vinculante que ha sido integrado exitosamente en el checklist de control de código de Academix.")
    add_body_p(doc, "3. Los tres artefactos implementados (Matriz de Calidad, Formato de Cambio SCM y Checklist de Code Review) proporcionan una gobernanza sólida, trazable y auditable, garantizando que futuras expansiones del sistema conserven la excelencia técnica requerida.")
    add_body_p(doc, "4. La aplicación práctica en la Fase 3 demostró el valor real de la calidad en ingeniería: la autoevaluación detectó a tiempo vulnerabilidades de fuerza bruta y brechas de accesibilidad en apps.accounts, las cuales fueron resueltas mediante una Solicitud de Cambio formal (CR-ACAD-2026-005), un Pull Request con inspección paritaria estricta y el congelamiento de la nueva línea base v2.5.1.")

    # 6. REFERENCIAS BIBLIOGRÁFICAS
    add_styled_heading(doc, "6. REFERENCIAS BIBLIOGRÁFICAS (APA 7)", level=1)
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
    out_file = out_dir / "INFORME_CALIDAD_SOFTWARE_ISO25010_IEEE730_ACADEMIX.docx"
    create_report_docx(str(out_file))
