#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_marco_conceptual_docx.py
Genera el documento Word (DOCX) formal del informe independiente:
INFORME TÉCNICO: MARCO CONCEPTUAL DE CALIDAD DE SOFTWARE Y GESTIÓN DE CONFIGURACIÓN (SCM)
Investigación exhaustiva de ISO/IEC 25010, IEEE 730, IEEE 828, CMMI y Normativa Colombiana.
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
    run_title = title_p.add_run("INFORME TÉCNICO: MARCO CONCEPTUAL DE CALIDAD DE SOFTWARE Y GESTIÓN DE CONFIGURACIÓN (SCM)")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(15.5)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 76, 129)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Fase 1: Investigación Normativa Exhaustiva (ISO/IEC 25010, IEEE 730, IEEE 828, CMMI y Regulación Colombiana)\nArticulación con el Código Fuente y Arquitectura de ACADEMIX v2.5.0")
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
    add_body_p(doc, "La calidad del software y la gestión de configuración son disciplinas sistemáticas que aseguran la trazabilidad, robustez, seguridad y mantenibilidad de los sistemas modernos de información. Para la plataforma ACADEMIX (Sistema de Gestión Académica y Control Escolar), este informe técnico desarrolla la investigación formal de la Fase 1, fundamentando los modelos normativos internacionales y nacionales orientados a la ingeniería de software.")
    add_body_p(doc, "Investigar, seleccionar y documentar los marcos normativos de calidad de software (ISO/IEC 25010 para calidad de producto, IEEE 730 para aseguramiento de calidad, e IEEE 828 y CMMI para gestión de configuración), estableciendo su relación directa con las métricas y la arquitectura de Academix.", bold_prefix="Objetivo General: ")
    add_body_p(doc, "1) Investigar las 8 características principales de ISO/IEC 25010:2023 y relacionarlas con métricas cuantitativas en el código. 2) Analizar la estructura de un Plan de Calidad de Software (SQAP) bajo IEEE 730. 3) Investigar los procesos de control de versiones, control de cambios y líneas base según IEEE 828 y CMMI. 4) Contextualizar el marco regulatorio colombiano (ICONTEC, MinTIC, SIC y colCERT).", bold_prefix="Objetivos Específicos: ")

    # 2. PILAR 1: MODELO ISO/IEC 25010
    add_styled_heading(doc, "2. PILAR 1: MODELO DE CALIDAD DEL PRODUCTO DE SOFTWARE (ISO/IEC 25010)", level=1)
    add_styled_heading(doc, "2.1 La Familia de Normas ISO/IEC 25000 (SQuaRE) y Evolución a ISO 25010:2023", level=2)
    add_body_p(doc, "La serie ISO/IEC 25000 (SQuaRE) sustituyó a las normas ISO 9126 e ISO 14598. Se organiza en cinco divisiones: Gestión (2500n), Modelos de Calidad (2501n), Medición (2502n), Requisitos (2503n) y Evaluación (2504n). La revisión ISO/IEC 25010:2023 evoluciona la portabilidad hacia Flexibilidad elástica, profundiza la Inclusión/Accesibilidad universal y se articula estrechamente con ISO/IEC 25012 para la calidad intrínseca de datos.")

    add_styled_heading(doc, "2.2 Las 8 Características Principales de Calidad del Producto", level=2)
    chars = [
        ("1. Adecuación Funcional", "Completitud, corrección/exactitud y pertinencia funcional."),
        ("2. Eficiencia de Desempeño", "Comportamiento temporal (latencia/TTFB), utilización de recursos (CPU/RAM) y capacidad concurrente."),
        ("3. Compatibilidad", "Coexistencia en el mismo servidor e interoperabilidad de datos (CSV, XLSX, PDF)."),
        ("4. Usabilidad", "Reconocimiento de idoneidad, aprendizaje, operabilidad, protección contra errores y accesibilidad universal."),
        ("5. Fiabilidad", "Madurez, disponibilidad de servicio, tolerancia a fallos y recuperabilidad transaccional."),
        ("6. Seguridad", "Confidencialidad, integridad, no repudio, trazabilidad (auditoría) y autenticidad."),
        ("7. Mantenibilidad", "Modularidad, reusabilidad, analizabilidad, modificabilidad y capacidad de prueba (testabilidad)."),
        ("8. Flexibilidad / Portabilidad", "Adaptabilidad, facilidad de instalación y facilidad de sustitución de entornos.")
    ]
    for c_title, c_desc in chars:
        add_body_p(doc, c_desc, bold_prefix=f"• {c_title}: ")

    add_styled_heading(doc, "2.3 Matriz de Relación: Características ISO 25010 vs. Métricas en Academix", level=2)

    data_m = [
        ("Adecuación Funcional", "Exactitud Funcional", "E = (N_calc_exactos / N_totales) * 100", "Cálculo de RAPs en apps.grades.services", "100.00% exactitud matemática."),
        ("Eficiencia Desempeño", "Comportamiento Temporal", "T_medio <= 500 ms ; P95 <= 800 ms", "Dashboard y boletines bajo carga Locust", "Latencia media <= 500 ms."),
        ("Compatibilidad", "Interoperabilidad", "Conformidad RFC 4180 / OpenXML", "Exportación/importación en students y reports", "100% interoperable con Excel/LibreOffice."),
        ("Usabilidad", "Accesibilidad (MinTIC)", "Puntaje WCAG 2.1 AA y contraste >= 4.5:1", "Plantillas HTML5, login.html y formularios", "Puntaje Lighthouse >= 90/100."),
        ("Fiabilidad", "Tolerancia a Fallos", "Tasa de inconsistencias tras fallos en BD", "Bloques @transaction.atomic en notas y matrículas", "0 registros corruptos. Rollback 100%."),
        ("Seguridad", "Confidencialidad", "S_pwd = (U_hash / U_totales) * 100", "Hasheo criptográfico en accounts_customuser", "100% contraseñas con Argon2id/PBKDF2."),
        ("Seguridad", "Integridad / RBAC", "I = 1 - (V_no_autorizados / P_intentos)", "Aislamiento de 5 roles institucionales", "100% rutas protegidas (HTTP 403/302)."),
        ("Mantenibilidad", "Testabilidad / Cobertura", "Cov = (L_probadas / L_totales) * 100", "Suite pytest-cov sobre micro-apps Django", "Cobertura de código >= 80%."),
        ("Mantenibilidad", "Modularidad / McCabe", "v(G) = E - N + 2P <= 10 por función", "Servicios de negocio en services.py", "v(G) <= 10. Cero métodos con v(G) > 12."),
        ("Flexibilidad", "Adaptabilidad", "Tiempo medio de despliegue (MTTD)", "Docker, render.yaml y scripts On-Premise", "Despliegue operativo en < 10 minutos.")
    ]

    t_m = doc.add_table(rows=len(data_m) + 1, cols=5)
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_m = ["Característica", "Subcaracterística", "Métrica Formal", "Componente en Academix", "Umbral de Aceptación"]
    for i, h in enumerate(headers_m):
        cell = t_m.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.runs[0].font.name = 'Arial'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)

    for r_idx, row_content in enumerate(data_m, start=1):
        for c_idx, val in enumerate(row_content):
            cell = t_m.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            cell.paragraphs[0].runs[0].font.name = 'Arial'
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            if c_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
        if r_idx % 2 == 0:
            for c_idx in range(5):
                set_cell_background(t_m.cell(r_idx, c_idx), "F4F6F9")

    doc.add_paragraph()

    # 3. PILAR 2: SQA E IEEE 730
    add_styled_heading(doc, "3. PILAR 2: ASEGURAMIENTO DE LA CALIDAD (SQA) Y NORMA IEEE 730", level=1)
    add_body_p(doc, "El estándar IEEE 730 define los requerimientos para iniciar, planificar, ejecutar y evaluar los procesos de Aseguramiento de Calidad del Software (SQA). Su valor radica en su carácter preventivo: asegura que los procesos, estándares y controles se apliquen durante todo el ciclo de vida, otorgando autoridad de veto al equipo auditor ante despliegues no conformes.")
    add_body_p(doc, "Estructura Obligatoria de un Plan de Calidad de Software (SQAP - IEEE 730):", bold_prefix="Anatomía del SQAP: ")
    sqap_sections = [
        ("1. Propósito y Alcance", "Productos cubiertos, metas cuantificables y fases del ciclo de vida."),
        ("2. Documentos de Referencia", "Normas internacionales (ISO 25010, IEEE 828) y leyes colombianas (Ley 1581, Res. 1519)."),
        ("3. Gestión y Organización", "Roles, responsabilidades e independencia del auditor de calidad frente al equipo de desarrollo."),
        ("4. Actividades de SQA", "Revisiones técnicas de requisitos (SRR), arquitectura (PDR/CDR) e inspecciones paritarias de código."),
        ("5. Estándares y Convenciones", "Guía de codificación PEP 8, Conventional Commits y Definition of Done (DoD)."),
        ("6. Gestión de Pruebas (V&V)", "Estrategia de verificación y validación: pruebas unitarias, integración, carga y pentesting."),
        ("7. Procedimiento CAPA", "Acciones Correctivas y Preventivas estructuradas mediante diagramas de Ishikawa y 5 Porqués."),
        ("8. Herramientas de Apoyo", "Linters (flake8/black), analizadores SAST (Bandit), escáneres DAST (OWASP ZAP) y CI/CD."),
        ("9. Control de Medios y Seguridad", "Seguridad del repositorio Git, gestión de secretos en .env y backups 3-2-1 de bases de datos."),
        ("10. Registros de Calidad", "Trazabilidad de actas de CCB, listas de chequeo firmadas y reportes de cobertura conservados.")
    ]
    for s_title, s_desc in sqap_sections:
        add_body_p(doc, s_desc, bold_prefix=f"• {s_title}: ")

    add_body_p(doc, "En entornos ágiles y DevOps, IEEE 730 se operacionaliza como la Definition of Done (DoD) de cada Sprint y se automatiza en pipelines CI/CD que ejecutan linters, escaneos de seguridad y suites de pruebas en cada commit.")

    # 4. PILAR 3: GESTIÓN DE CONFIGURACIÓN (SCM)
    add_styled_heading(doc, "4. PILAR 3: GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE (SCM)", level=1)
    add_styled_heading(doc, "4.1 Procesos Nucleares de SCM según el Estándar IEEE 828-2012", level=2)
    add_body_p(doc, "El estándar IEEE 828-2012 define los cinco procesos esenciales de SCM: 1) Identificación de Ítems de Configuración (CIs: código, migraciones, plantillas, .env.example, manuales); 2) Control de Cambios mediante solicitudes formales (CR/RFC); 3) Contabilidad del Estado de la Configuración (CSA); 4) Auditorías de Configuración Funcional (FCA) y Física (PCA); y 5) Gestión de Entregas y Despliegues.")

    add_styled_heading(doc, "4.2 Enfoque de SCM según el Modelo CMMI-DEV (Área de Proceso CM)", level=2)
    cmmi_goals = [
        ("Meta SG 1: Establecer Líneas Base", "Identificar CIs (SP 1.1), establecer el sistema de gestión en Git (SP 1.2) y congelar líneas base (SP 1.3)."),
        ("Meta SG 2: Seguir y Controlar Cambios", "Seguir las solicitudes de cambio CR (SP 2.1) y controlar los ítems de configuración en ramas (SP 2.2)."),
        ("Meta SG 3: Establecer la Integridad", "Mantener los registros de estado CSA (SP 3.1) y ejecutar auditorías de configuración FCA/PCA (SP 3.2).")
    ]
    for g_title, g_desc in cmmi_goals:
        add_body_p(doc, g_desc, bold_prefix=f"• {g_title}: ")

    add_styled_heading(doc, "4.3 Control de Versiones, Ramificación GitFlow y Commits Semánticos", level=2)
    add_body_p(doc, "Se adopta un modelo distribuido (DVCS) bajo Git con flujo GitFlow: rama main inmutable para producción, develop para integración, y ramas feature/ y hotfix/ aisladas. Los commits siguen la convención Conventional Commits (feat, fix, test, docs) garantizando trazabilidad histórica.")

    add_styled_heading(doc, "4.4 Control de Cambios, Comité (CCB) y Plan de Rollback", level=2)
    add_body_p(doc, "Ningún cambio ingresa a producción sin una Solicitud de Cambio (CR/RFC) que contenga: justificación técnica/legal, análisis de impacto en BD y arquitectura, nivel de riesgo y Plan de Marcha Atrás (Rollback Plan) paso a paso en caso de fallo, evaluada formalmente por el Comité de Control de Cambios (CCB).")

    add_styled_heading(doc, "4.5 Líneas Base (Baselines) y Auditorías FCA/PCA", level=2)
    add_body_p(doc, "Las Líneas Base representan estados congelados y auditados identificados mediante etiquetas Git (ej. v2.5.0-baseline). Antes de su liberación se audita que cumpla con los requisitos especificados (FCA) y que todos los binarios y archivos existan en el repositorio (PCA).")

    # 5. PILAR 4: MARCO COLOMBIANO
    add_styled_heading(doc, "5. PILAR 4: MARCO REGULATORIO Y ENTES DE CALIDAD EN COLOMBIA (2026)", level=1)
    add_body_p(doc, "Organismo de normalización que adopta NTC-ISO/IEC 25010 (calidad de producto), NTC-ISO/IEC 12207 (ciclo de vida) y NTC-ISO/IEC 27001 (SGSI).", bold_prefix="• ICONTEC: ")
    add_body_p(doc, "Emite la Política de Gobierno Digital (Decreto 088 de 2022) y la Resolución 1519 de 2020 de Accesibilidad Web Universal (W3C WCAG 2.1 nivel AA: contraste >= 4.5:1, etiquetas y tags ARIA obligatorios).", bold_prefix="• MinTIC: ")
    add_body_p(doc, "Autoridad de Habeas Data (Ley 1581 de 2012). El Artículo 7 impone un régimen reforzado para Niños, Niñas y Adolescentes: exige consentimiento de tutores, prohíbe la divulgación de notas en texto claro y sanciona el almacenamiento inseguro de credenciales.", bold_prefix="• Superintendencia de Industria y Comercio (SIC): ")
    add_body_p(doc, "Equipo de Respuesta a Incidentes Cibernéticos de Colombia; dicta directrices de mitigación obligatoria frente al OWASP Top 10.", bold_prefix="• colCERT / CSIRT de Gobierno: ")
    add_body_p(doc, "Rige la formación técnica y tecnológica bajo la Norma Sectorial de Competencia Laboral 220501096.", bold_prefix="• SENA: ")

    # 6. CONCLUSIONES
    add_styled_heading(doc, "6. CONCLUSIONES", level=1)
    add_body_p(doc, "1. La norma ISO/IEC 25010:2023 proporciona un marco de medición cuantitativo que permite transformar los requerimientos de calidad en métricas tangibles y verificables en el código fuente de Academix.")
    add_body_p(doc, "2. El estándar IEEE 730 formaliza el aseguramiento de calidad como un proceso preventivo e integral, articulado armónicamente con metodologías ágiles a través de la Definition of Done y auditorías de configuración.")
    add_body_p(doc, "3. La gestión de configuración bajo IEEE 828 y CMMI asegura la integridad y trazabilidad del código mediante el flujo GitFlow, comités de control de cambios (CCB) y líneas base reproducibles.")
    add_body_p(doc, "4. En Colombia, el software escolar está sujeto a un estricto cumplimiento legal: la Ley 1581 de 2012 de la SIC para protección de datos de menores y la Resolución 1519 de 2020 de MinTIC para accesibilidad web universal son estándares vinculantes innegociables.")

    # 7. REFERENCIAS
    add_styled_heading(doc, "7. REFERENCIAS BIBLIOGRÁFICAS (APA 7)", level=1)
    refs = [
        "CMMI Product Team. (2018). CMMI for Development, Version 2.0 (CMMI-DEV v2.0). Pittsburgh, PA: Software Engineering Institute, Carnegie Mellon University.",
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012 de Protección de Datos Personales. Diario Oficial No. 48.587.",
        "ICONTEC. (2013). Norma Técnica Colombiana NTC-ISO/IEC 25010: Requisitos de Calidad de Software (SQuaRE). Bogotá: ICONTEC.",
        "ISO. (2023). ISO/IEC 25010:2023 Systems and software engineering — Product quality model. Ginebra: ISO.",
        "IEEE. (2012). IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering. Nueva York: IEEE Computer Society.",
        "IEEE. (2014). IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes. Nueva York: IEEE Computer Society.",
        "MinTIC. (2020). Resolución 1519 de 2020: Directrices de Accesibilidad Web (WCAG 2.1 AA). Bogotá: MinTIC.",
        "OWASP Foundation. (2021). OWASP Top 10: The Ten Most Critical Web Application Security Risks. Open Web Application Security Project.",
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
    print(f"Informe de Marco Conceptual DOCX generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_dir = Path(r"C:\Academix\docs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "INFORME_TECNICO_MARCO_CONCEPTUAL_ISO25010_IEEE730_SCM.docx"
    create_report_docx(str(out_file))

