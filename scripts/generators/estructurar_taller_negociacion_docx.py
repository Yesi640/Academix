#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
estructurar_taller_negociacion_docx.py
Toma exactamente todo el contenido del Taller de Negociación Tecnológica
y lo estructura con diseño institucional ejecutivo de alta calidad para presentación
al líder de proyecto e instructor SENA (Anybal López - Ficha 3173430).
"""

import os
import shutil
import docx
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
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)  # Azul Institucional SENA
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 125, 50)  # Verde Técnico
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(60, 60, 60)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Arial'
        r_bold.font.size = Pt(9.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(30, 30, 30)
    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(9.5)
    r_text.font.italic = italic
    r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_callout(doc, text, title="", bg_color="EBF3FA", title_color="0F4C81"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
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
    r_b.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def build_table(doc, headers, data, col_widths, header_color="0F4C81"):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        set_cell_background(cell, header_color)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = 'Arial'
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Rows
    for i, row_data in enumerate(data):
        bg = "F4F6F9" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = tbl.cell(i + 1, j)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
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
            
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return tbl

def build_document(output_path):
    doc = Document()
    
    # Configuración de márgenes estándar APA (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ══════════════════════════════════════════════════════════════════
    # PORTADA INSTITUCIONAL SENA
    # ══════════════════════════════════════════════════════════════════
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA)\nCENTRO DE FORMACIÓN EN TECNOLOGÍAS DE LA INFORMACIÓN\nTECNOLOGÍA EN ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO)\nFICHA DE CARACTERIZACIÓN: 3173430")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph()
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("TALLER: PROCESO DE NEGOCIACIÓN DE TECNOLOGÍA INFORMÁTICA")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Dossier Completo de Evidencias Técnicas, Financieras, Contractuales y de Cierre\nAplicadas al Proyecto Formativo ACADEMIX v2.5.1")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(70, 70, 70)
    
    doc.add_paragraph()
    
    # Ficha de identificación
    tbl_id = doc.add_table(rows=6, cols=2)
    tbl_id.alignment = WD_TABLE_ALIGNMENT.CENTER
    data_id = [
        ["Proyecto de Software:", "ACADEMIX — Plataforma Web de Gestión Académica y Control Escolar (Django 5.x / PostgreSQL 16)"],
        ["Competencia Asociada:", "220501096 — Desarrollar el sistema informático según requisitos y diseño tecnológico"],
        ["Instructor Asignado:", "Anybal López — Centro de Formación SENA"],
        ["Equipo de Desarrollo:", "Academix Software Solutions (Aprendices ADSO Ficha 3173430)"],
        ["Representante / Líder:", "Sofia Helena Torres (Líder SQA) y Julián Esteban Rocha (Líder Técnico)"],
        ["Fecha de Entrega:", "Noviembre de 2026"]
    ]
    for i, (k, v) in enumerate(data_id):
        cell_k = tbl_id.cell(i, 0)
        cell_v = tbl_id.cell(i, 1)
        set_cell_background(cell_k, "F0F4F8")
        set_cell_background(cell_v, "FFFFFF")
        set_cell_margins(cell_k, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_v, top=60, bottom=60, left=100, right=100)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_after = Pt(0)
        rk = pk.add_run(k)
        rk.font.name = 'Arial'
        rk.font.size = Pt(8.5)
        rk.font.bold = True
        rk.font.color.rgb = RGBColor(15, 76, 129)
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_after = Pt(0)
        rv = pv.add_run(v)
        rv.font.name = 'Arial'
        rv.font.size = Pt(8.5)
        rv.font.color.rgb = RGBColor(50, 50, 50)
        
    for row in tbl_id.rows:
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.3)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    add_callout(doc,
        "Instrucción de Trabajo: Con base en las características del software a desarrollar, realice las siguientes evidencias:\n"
        "1. Documento de Términos de Referencia (TDR): Especificaciones técnicas de equipos, licencias y hosting.\n"
        "2. Cuadro comparativo de cotizaciones: Evaluación de al menos 3 proveedores reales con criterios ponderados y justificación.\n"
        "3. Minuta de contrato informático o acuerdo de nivel de servicio: Borrador con cláusulas técnicas, garantías y propiedad intelectual.\n"
        "4. Acta o informe de cierre: Verificación de cumplimiento frente a lo solicitado inicialmente.",
        "ESTRUCTURA GENERAL DEL TALLER EVALUATIVO"
    )

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════
    # EVIDENCIA 1: TÉRMINOS DE REFERENCIA (TDR)
    # ══════════════════════════════════════════════════════════════════
    add_styled_heading(doc, "EVIDENCIA 1: Documento de Términos de Referencia (TDR)", level=1)
    add_body_p(doc, "Especificaciones técnicas de los equipos, licencias, entorno de software y hosting que requiere el proyecto ACADEMIX v2.5.1 para su puesta en marcha y operación institucional continua.")
    
    # A. Hardware
    add_styled_heading(doc, "A. Prerrequisitos de Hardware", level=2)
    headers_t0 = ["Componente", "Especificación Mínima (LAN hasta 30 usuarios)", "Especificación Recomendada (LAN > 30 usuarios / Servidor Dedicado)"]
    data_t0 = [
        ["Procesador (CPU)", "Intel Core i3 de 7ª generación o AMD Ryzen 3 (4 núcleos a 2.4 GHz)", "Intel Core i5 / AMD Ryzen 5 (6 a 8 núcleos a 3.0 GHz)"],
        ["Memoria RAM", "4 GB DDR3/DDR4 (mínimo 2 GB libres para el sistema)", "8 GB a 16 GB DDR4"],
        ["Almacenamiento", "20 GB de espacio libre en disco rígido", "50 GB de espacio disponible en unidad de estado sólido (SSD NVMe/SATA)"],
        ["Interfaz de Red", "Tarjeta de red Ethernet 10/100/1000 Mbps o Wi-Fi 802.11n", "Tarjeta Gigabit Ethernet 1000 Mbps cableada (categoría 6 recomendada)"],
        ["Alimentación Eléctrica", "Toma con polo a tierra", "Sistema de Alimentación Ininterrumpida (UPS) de 750VA a 1000VA (autonomía 20 min)"]
    ]
    build_table(doc, headers_t0, data_t0, [1.8, 2.3, 2.4], header_color="0F4C81")

    # B. Software
    add_styled_heading(doc, "B. Prerrequisitos de Software del Sistema y Entorno", level=2)
    headers_t1 = ["Software", "Versión Requerida", "Propósito Técnico"]
    data_t1 = [
        ["Sistema Operativo", "Windows 10/11 Pro (64 bits) o Linux Ubuntu Server 22.04 LTS", "Plataforma anfitriona para ejecución de servicios"],
        ["Python", "3.11.x o 3.12.x", "Intérprete para la lógica de negocio y backend de Django"],
        ["Navegadores Clientes", "Google Chrome 115+, Microsoft Edge 115+, Mozilla Firefox 115+", "Renderizado de interfaz Bootstrap 5 y ejecución de scripts cliente"],
        ["Herramienta de Compresión", "7-Zip, WinRAR o utilitario ZIP nativo de Windows", "Empaquetamiento de expedientes y backups periódicos"]
    ]
    build_table(doc, headers_t1, data_t1, [2.0, 2.0, 2.5], header_color="2E7D32")

    # C. Licenciamiento
    add_styled_heading(doc, "C. Inventario de Licenciamiento (Cumplimiento Legal y Costo Cero)", level=2)
    headers_t2 = ["Componente Tecnológico", "Tipo de Licencia", "Costo de Licencia", "Observación Legal"]
    data_t2 = [
        ["Django Framework", "Licencia BSD de 3 cláusulas", "$0 COP", "Software libre y de código abierto; autoriza uso comercial e institucional."],
        ["Python Runtime", "PSF (Python Software Foundation License)", "$0 COP", "Licencia libre compatible con GPL."],
        ["Bootstrap 5 UI", "Licencia MIT", "$0 COP", "Permite uso y personalización total de estilos y componentes."],
        ["SQLite 3 Engine", "Dominio Público (*Public Domain*)", "$0 COP", "Libre de regalías; no requiere contratos de software de terceros."],
        ["ReportLab / WeasyPrint", "Licencia BSD / LGPL", "$0 COP", "Generación de boletines y consolidados en formato PDF."],
        ["Windows Pro OS", "Licencia OEM / Retail existente", "$0 COP", "Reutilización de la licencia ya adquirida por la institución educativa."]
    ]
    build_table(doc, headers_t2, data_t2, [1.8, 1.6, 1.1, 2.0], header_color="0F4C81")

    # D. Red
    add_styled_heading(doc, "D. Recursos de Red y Conectividad", level=2)
    headers_t3 = ["Parámetro de Red", "Valor Configurado", "Justificación"]
    data_t3 = [
        ["Direccionamiento IP", "Estática privada (Ejemplo: `192.168.1.50`)", "Facilita a los docentes guardar el enlace de acceso fijo en sus marcadores."],
        ["Subred Institucional", "`255.255.255.0` (`/24`)", "Todos los equipos de secretaría y salas deben estar en el mismo segmento de red."],
        ["Puerto de Servicio", "TCP `8000` (Red local) / TCP `80` (Producción HTTP)", "Puerto autorizado en el cortafuegos para la escucha de solicitudes web."],
        ["Regla de Firewall", "Regla de entrada: `Academix_Server_Port8000`", "Creada automáticamente mediante el script `firewall.bat`."]
    ]
    build_table(doc, headers_t3, data_t3, [1.8, 2.2, 2.5], header_color="2E7D32")

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════
    # EVIDENCIA 2: CUADRO COMPARATIVO DE COTIZACIONES
    # ══════════════════════════════════════════════════════════════════
    add_styled_heading(doc, "EVIDENCIA 2: Cuadro Comparativo de Cotizaciones de Infraestructura Cloud", level=1)
    add_body_p(doc, "Evaluación de al menos 3 proveedores reales con criterios ponderados y justificación de la elección.")
    add_body_p(doc, "La plataforma ACADEMIX v2.5.1, desarrollada en Django 5.x y PostgreSQL 16, requiere infraestructura de alta disponibilidad para atender a una comunidad promedio de 1,200 estudiantes, 60 docentes y 1,000 padres de familia. Para su despliegue comercial y operativo, se evaluaron tres proveedores de clase mundial: Render Cloud, Amazon Web Services (AWS) y DigitalOcean.")
    
    # 1.1 Criterios
    add_styled_heading(doc, "1.1 Criterios Técnicos de Selección y Ponderación", level=2)
    headers_t4 = ["Criterio de Selección", "Peso (%)", "Justificación del Peso Técnico"]
    data_t4 = [
        ["1. Costo Total (TCO) y Previsibilidad", "25%", "Vital para colegios con presupuestos fijos anuales regulados por el MEN."],
        ["2. Rendimiento, Latencia y Uptime SLA", "25%", "Garantiza operatividad continua en cierres de periodo y emisión de boletines."],
        ["3. Seguridad y Ley 1581 (Menores)", "20%", "Cifrado en reposo/tránsito y aislamiento de datos de niños y adolescentes."],
        ["4. Facilidad de Despliegue CI/CD", "15%", "Automatización de despliegues vía GitHub con render.yaml sin sysadmin dedicado."],
        ["5. Soporte y Recuperación ante Fallos", "15%", "Métricas de consumo, backups diarios continuos y tiempo de recuperación RTO <= 2h."]
    ]
    build_table(doc, headers_t4, data_t4, [2.2, 1.0, 3.3], header_color="0F4C81")

    # 1.2 Comparación
    add_styled_heading(doc, "1.2 Comparación Técnica y Financiera de Proveedores Reales", level=2)
    headers_t5 = ["Componente / Métrica", "Render Cloud (PaaS)", "AWS (Elastic Beanstalk / RDS)", "DigitalOcean (App Platform)"]
    data_t5 = [
        ["Cómputo Web", "Standard (2 GB RAM, 1 vCPU)", "EC2 t4g.small Graviton2 (2GB, 2vCPU)", "App Platform Pro (2 GB RAM, 1 vCPU)"],
        ["Costo Cómputo Web", "$25.00 USD / mes", "$14.60 USD / mes", "$25.00 USD / mes"],
        ["Base de Datos PostgreSQL", "Managed 1 GB RAM, 10 GB SSD", "RDS db.t4g.micro (1 GB RAM, 20 GB gp3)", "Managed 1 Node (1 GB RAM, 10 GB NVMe)"],
        ["Costo Base de Datos", "$20.00 USD / mes", "$18.25 USD / mes", "$15.00 USD / mes"],
        ["Costos de Red / Load Balancer", "$0.00 (Incluido SSL + 100GB)", "$12.50 USD / mes (ALB + Data transfer)", "$0.00 (Incluido SSL + 100GB)"],
        ["Costo Total Mensual (USD)", "$45.00 USD / mes", "$45.35 USD / mes", "$40.00 USD / mes"],
        ["Costo Mensual Estimado (COP)", "$191,250 COP / mes", "$192,738 COP / mes", "$170,000 COP / mes"],
        ["Costo Anual Proyectado (COP)", "$2,295,000 COP / año", "$2,312,856 COP / año", "$2,040,000 COP / año"],
        ["Uptime Garantizado (SLA)", "99.90% mensual", "99.95% mensual", "99.90% mensual"],
        ["Latencia a Colombia", "85 - 105 ms (Oregon)", "65 - 75 ms (Virginia us-east-1)", "75 - 90 ms (NYC / Miami)"],
        ["Backups de Base de Datos", "Diarios automáticos (7 días retención)", "Continuos Point-in-Time (hasta 35 días)", "Diarios automáticos (7 días retención)"],
        ["Despliegue CI/CD GitHub", "Nativo inmediato con render.yaml", "Complejo: AWS CodePipeline e IAM", "Nativo con GitHub Apps"]
    ]
    build_table(doc, headers_t5, data_t5, [1.8, 1.6, 1.6, 1.5], header_color="2E7D32")

    # 1.3 Matriz cuantitativa
    add_styled_heading(doc, "1.3 Matriz de Calificación Cuantitativa Ponderada", level=2)
    headers_t6 = ["Criterio de Evaluación", "Peso", "Render Cloud", "Amazon Web Services", "DigitalOcean"]
    data_t6 = [
        ["1. Costo Total y Previsibilidad", "25%", "4.6 (1.15)", "3.5 (0.88)", "4.8 (1.20)"],
        ["2. Rendimiento, Latencia y Uptime", "25%", "4.5 (1.13)", "4.9 (1.23)", "4.4 (1.10)"],
        ["3. Seguridad y Ley 1581 (Menores)", "20%", "4.7 (0.94)", "5.0 (1.00)", "4.5 (0.90)"],
        ["4. Facilidad CI/CD y Mantenibilidad", "15%", "5.0 (0.75)", "3.2 (0.48)", "4.6 (0.69)"],
        ["5. Soporte y Recuperación ante Fallos", "15%", "4.4 (0.66)", "4.6 (0.69)", "4.3 (0.65)"],
        ["CALIFICACIÓN FINAL TOTAL", "100%", "4.63 / 5.00", "4.28 / 5.00", "4.54 / 5.00"],
        ["POSICIÓN DE SELECCIÓN", "—", "1er PUESTO (GANADOR)", "3er PUESTO", "2do PUESTO"]
    ]
    build_table(doc, headers_t6, data_t6, [2.3, 0.7, 1.2, 1.2, 1.1], header_color="0F4C81")

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════
    # EVIDENCIA 3: MINUTA DE CONTRATO INFORMÁTICO Y SLA
    # ══════════════════════════════════════════════════════════════════
    add_styled_heading(doc, "EVIDENCIA 3: Minuta de Contrato Informático y Acuerdo de Nivel de Servicio (SLA)", level=1)
    add_body_p(doc, "Borrador con cláusulas técnicas, garantías y propiedad intelectual.")
    
    add_styled_heading(doc, "Minuta de Contrato Informático de Suministro y SaaS", level=2)
    add_body_p(doc, "CONTRATO No. ACAD-SENA-2026-088 celebrado entre ACADEMIX SOFTWARE SOLUTIONS, representada legalmente por SOFIA HELENA TORRES (en adelante EL CONTRATISTA), y el COLEGIO TÉCNICO PILOTO INSTITUCIONAL, representado por el Rector DR. CARLOS EDUARDO RAMÍREZ HOYOS (en adelante EL CONTRATANTE).")
    
    clauses = [
        ("Cláusula Primera (Objeto):", " Suministrar, desplegar en infraestructura cloud, configurar, poner en marcha y mantener la plataforma web de gestión escolar ACADEMIX v2.5.1, garantizando los estándares de calidad ISO/IEC 25010 y el Acuerdo de Nivel de Servicio adjunto."),
        ("Cláusula Segunda (Alcance Funcional):", " El software comprende los 7 módulos activos: 1) Autenticación RBAC y Rate Limiting (apps.accounts); 2) Carga masiva transaccional con savepoints atómicos (apps.students); 3) Malla curricular y notas RAPs al 100.00% con Decimal (apps.grades); 4) Boletines oficiales PDF con QR criptográfico sin exposición de menores (apps.reports); 5) Control de periodos y bloqueo is_locked (apps.periods); 6) Asistencia y observador convivencial (apps.attendance/discipline); y 7) Bitácora inmutable de auditoría (apps.audit)."),
        ("Cláusula Tercera (Valor y Forma de Pago):", " El valor total anual del servicio SaaS, hosting cloud, backups y soporte asciende a la suma de DOS MILLONES SEISCIENTOS MIL PESOS MONEDA CORRIENTE ($2,600,000 COP), exento de IVA (Art. 476 Numeral 21 Estatuto Tributario). Pagaderos: 30% al inicio ($780,000 COP), 40% a la carga de estudiantes y capacitación ($1,040,000 COP) y 30% al cierre del año lectivo ($780,000 COP)."),
        ("Cláusula Cuarta (Obligaciones del Contratista):", " 1) Garantizar disponibilidad mensual >= 99.50% según SLA; 2) Mantenimiento preventivo/correctivo de fallas; 3) Custodia de backups diarios; 4) Capacitación al personal docente y administrativo; y 5) Mantener el software libre de vulnerabilidades OWASP Top 10."),
        ("Cláusula Quinta (Obligaciones del Contratante):", " 1) Pagar el valor acordado; 2) Suministrar información fidedigna de matrícula; 3) Custodiar credenciales de acceso rectoral; y 4) Obtener consentimiento informado de acudientes para el tratamiento de datos de menores de edad."),
        ("Cláusula Sexta (Propiedad Intelectual y Licenciamiento):", " Conforme a la Ley 23 de 1982 y la Decisión Andina 351 de 1993, los derechos morales y patrimoniales sobre el código fuente de ACADEMIX pertenecen a sus desarrolladores (EL CONTRATISTA). EL CONTRATANTE recibe una Licencia de Uso no exclusiva, intransferible y temporal. Sin embargo, EL CONTRATANTE es el único dueño de la base de datos de calificaciones y expedientes, la cual será entregada en formato abierto (.sql/CSV) al liquidar el contrato."),
        ("Cláusula Séptima (Protección de Datos de Menores y Habeas Data):", " En estricto cumplimiento del Artículo 7 de la Ley 1581 de 2012 y Circular 002 de 2021 de la SIC, las partes reconocen el régimen especial de protección reforzada de datos de Niños, Niñas y Adolescentes (NNA). Todas las contraseñas se almacenan con hashes Argon2id/PBKDF2, el canal fuerza TLS 1.3 y la verificación pública por QR jamás divulga números de documento, teléfonos o direcciones de estudiantes menores."),
        ("Cláusula Octava (Gestión de Configuración - SCM):", " Cualquier modificación o nuevo requerimiento funcional solicitado por el colegio que exceda el alcance de la versión 2.5.1 deberá tramitarse obligatoriamente mediante Formato de Solicitud de Cambio (Change Request - SCM) según IEEE 828 ante el Comité de Control de Cambios (CCB)."),
        ("Cláusula Novena (Vigencia y Terminación):", " Duración de 12 meses prorrogables. Al término, EL CONTRATISTA suministrará volcado íntegro de base de datos y procederá al borrado seguro de la instancia institucional en nube en máximo 30 días calendario. Controversias se someterán a centro de conciliación de Buga o Cali bajo leyes de la República de Colombia.")
    ]
    for pref, text in clauses:
        add_body_p(doc, text, bold_prefix=pref)
        
    add_styled_heading(doc, "PARTE III: Anexo Técnico — Acuerdo de Nivel de Servicio (SLA)", level=2)
    add_body_p(doc, "Establece los compromisos vinculantes de disponibilidad, tiempos máximos de respuesta ante incidentes, penalizaciones financieras por caída y políticas de respaldo:")
    add_body_p(doc, "EL CONTRATISTA garantiza un Uptime mensual >= 99.50% (máximo 216 minutos de indisponibilidad imprevista al mes). Fórmula: Disponibilidad (%) = [(Minutos Totales Mes - Minutos Caída) / Minutos Totales Mes] * 100.", bold_prefix="• Métrica de Uptime: ")
    
    headers_t7 = ["Severidad", "Criterio de Impacto", "Respuesta (MTTA)", "Solución (MTTR)", "Acción Técnica"]
    data_t7 = [
        ["1 (Crítica)", "Caída total del sistema o base de datos inaccesible", "<= 30 min", "<= 2 horas", "DevOps inmediato / Activación réplica local"],
        ["2 (Alta)", "Fallo de módulo crítico (ej. docentes no guardan notas)", "<= 1 hora", "<= 4 horas", "Asignación Backend / Reinicio de workers WSGI"],
        ["3 (Media)", "Fallo parcial menor que no frena la operación", "<= 2 horas", "<= 12 horas", "Solución en ciclo ordinario mediante rama fix/"],
        ["4 (Baja)", "Consultas de interfaz o dudas de manejo de usuarios", "<= 4 horas", "<= 24 horas", "Mesa de ayuda ordinaria (Lunes a Viernes 7am-5pm)"]
    ]
    build_table(doc, headers_t7, data_t7, [1.0, 2.3, 1.0, 1.0, 1.2], header_color="0F4C81")

    headers_t8 = ["Disponibilidad Mensual Alcanzada", "Compensación / Descuento sobre Factura Siguiente"]
    data_t8 = [
        ["Entre 99.00% y 99.49%", "10% de descuento sobre el canon mensual"],
        ["Entre 97.00% y 98.99%", "25% de descuento sobre el canon mensual"],
        ["Inferior al 97.00%", "50% de descuento y causal de terminación unilateral del contrato"]
    ]
    build_table(doc, headers_t8, data_t8, [3.2, 3.3], header_color="2E7D32")

    add_body_p(doc, "Backups automáticos diarios a las 02:00 am (Zona horaria Colombia). RPO (Punto de Recuperación Objetivo): Máximo 24 horas de datos. RTO (Tiempo de Recuperación Objetivo): Máximo 2 horas para restaurar el servicio en su totalidad.", bold_prefix="• Políticas de Respaldo y Recuperación (RPO / RTO): ")
    add_body_p(doc, "Mantenimientos mayores se ejecutarán exclusivamente en días domingos o festivos entre las 22:00 y las 04:00 horas, avisando al colegio con mínimo 48 horas de antelación.", bold_prefix="• Ventanas de Mantenimiento: ")

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════
    # EVIDENCIA 4: ACTA DE ENTREGA Y RECIBO A SATISFACCIÓN
    # ══════════════════════════════════════════════════════════════════
    add_styled_heading(doc, "EVIDENCIA 4: Acta o Informe de Cierre", level=1)
    add_body_p(doc, "Verificación de cumplimiento frente a lo solicitado inicialmente.")
    
    # Marco formal del Acta
    tbl_acta = doc.add_table(rows=1, cols=1)
    tbl_acta.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_acta = tbl_acta.cell(0, 0)
    set_cell_background(c_acta, "FAFAFA")
    set_cell_margins(c_acta, top=140, bottom=140, left=180, right=180)
    
    p_acta_title = c_acta.paragraphs[0]
    p_acta_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_acta_title.paragraph_format.space_after = Pt(2)
    r_at = p_acta_title.add_run("ACTA FORMAL DE ENTREGA Y RECIBO A SATISFACCIÓN\nSISTEMA DE GESTIÓN ACADÉMICA Y CONTROL ESCOLAR \"ACADEMIX\"")
    r_at.font.name = 'Arial'
    r_at.font.size = Pt(11)
    r_at.font.bold = True
    r_at.font.color.rgb = RGBColor(15, 76, 129)
    
    p_dt = c_acta.add_paragraph()
    p_dt.paragraph_format.space_after = Pt(4)
    r_dt = p_dt.add_run("LUGAR Y FECHA: __________________________, _____ de ____________________ de 2026.")
    r_dt.font.name = 'Arial'
    r_dt.font.size = Pt(9)
    r_dt.font.bold = True
    
    p_in = c_acta.add_paragraph()
    p_in.paragraph_format.space_after = Pt(4)
    p_in.paragraph_format.line_spacing = 1.15
    r_in = p_in.add_run(
        "En las instalaciones de la institución beneficiaria se reúnen los abajo firmantes con el propósito de "
        "formalizar la entrega técnica, administrativa y operativa del software ACADEMIX, desarrollado en el marco "
        "del programa de formación Análisis y Desarrollo de Software (ADSO) del SENA."
    )
    r_in.font.name = 'Arial'
    r_in.font.size = Pt(9)
    
    p_c1 = c_acta.add_paragraph()
    p_c1.paragraph_format.space_after = Pt(2)
    r_c1 = p_c1.add_run("1. DECLARACIÓN DE CONFORMIDAD:")
    r_c1.font.name = 'Arial'
    r_c1.font.size = Pt(9.5)
    r_c1.font.bold = True
    r_c1.font.color.rgb = RGBColor(46, 125, 50)
    
    p_c1_sub = c_acta.add_paragraph()
    p_c1_sub.paragraph_format.space_after = Pt(4)
    r_c1_sub = p_c1_sub.add_run("La institución educativa receptora declara haber recibido a entera satisfacción los siguientes elementos:")
    r_c1_sub.font.name = 'Arial'
    r_c1_sub.font.size = Pt(9)
    
    items = [
        "[X] Código fuente completo y documentado del sistema ACADEMIX (15 módulos funcionales).",
        "[X] Base de datos institucional inicializada con el catálogo escolar y parametrización de Decreto 1290.",
        "[X] Scripts ejecutables de despliegue en red (iniciar_servidor_red.bat y firewall.bat).",
        "[X] Script automatizado de copias de seguridad (backup_diario.bat) configurado en el servidor.",
        "[X] Documento técnico formal: Informe Administrativo, Planes de Instalación, Respaldo y Migración.",
        "[X] Jornada de transferencia técnica y capacitación a los usuarios líderes del sistema."
    ]
    for it in items:
        p_it = c_acta.add_paragraph()
        p_it.paragraph_format.space_after = Pt(2)
        p_it.paragraph_format.left_indent = Inches(0.2)
        r_it = p_it.add_run(it)
        r_it.font.name = 'Arial'
        r_it.font.size = Pt(8.5)
        r_it.font.color.rgb = RGBColor(40, 40, 40)
        
    p_c2 = c_acta.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(4)
    p_c2.paragraph_format.space_after = Pt(2)
    r_c2 = p_c2.add_run("2. ACEPTACIÓN Y COMPROMISOS:")
    r_c2.font.name = 'Arial'
    r_c2.font.size = Pt(9.5)
    r_c2.font.bold = True
    r_c2.font.color.rgb = RGBColor(46, 125, 50)
    
    p_c2_txt = c_acta.add_paragraph()
    p_c2_txt.paragraph_format.space_after = Pt(6)
    p_c2_txt.paragraph_format.line_spacing = 1.15
    r_c2_txt = p_c2_txt.add_run(
        "El equipo de desarrollo garantiza el funcionamiento óptimo de la solución conforme a las especificaciones pactadas "
        "y se compromete a brindar el soporte técnico durante el periodo de garantía establecido. La institución asume la "
        "custodia del servidor, las contraseñas de superusuario y la ejecución rutinaria de las políticas de respaldo documentadas en este informe."
    )
    r_c2_txt.font.name = 'Arial'
    r_c2_txt.font.size = Pt(9)
    
    p_c3 = c_acta.add_paragraph()
    p_c3.paragraph_format.space_after = Pt(6)
    r_c3 = p_c3.add_run("Para constancia de lo anterior, se firma la presente acta:")
    r_c3.font.name = 'Arial'
    r_c3.font.size = Pt(9)
    r_c3.font.italic = True

    # Firmas en cuadrícula 2x2 elegante
    tbl_sig = c_acta.add_table(rows=2, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    sigs = [
        ("_____________________________________________\nNOMBRE DEL APRENDIZ LÍDER DE PROYECTO\nC.C. _____________________________________\nLíder de Desarrollo - Programa ADSO SENA",
         "_____________________________________________\nREPRESENTANTE INSTITUCIÓN BENEFICIARIA\nC.C. _____________________________________\nInstitución Educativa Beneficiaria"),
        ("_____________________________________________\nINSTRUCTOR ASIGNADO SENA\nC.C. _____________________________________\nAnybal López - Centro de Formación SENA",
         "_____________________________________________\nCOORDINACIÓN ACADÉMICA / ADMINISTRADOR\nC.C. _____________________________________\nResponsable de Operación y Soporte TI")
    ]
    
    for r_idx, (sig_l, sig_r) in enumerate(sigs):
        cell_l = tbl_sig.cell(r_idx, 0)
        cell_r = tbl_sig.cell(r_idx, 1)
        set_cell_background(cell_l, "FAFAFA")
        set_cell_background(cell_r, "FAFAFA")
        set_cell_margins(cell_l, top=80, bottom=80, left=80, right=80)
        set_cell_margins(cell_r, top=80, bottom=80, left=80, right=80)
        
        pl = cell_l.paragraphs[0]
        pl.paragraph_format.space_after = Pt(0)
        pl.paragraph_format.line_spacing = 1.15
        rl = pl.add_run(sig_l)
        rl.font.name = 'Arial'
        rl.font.size = Pt(8)
        rl.font.bold = True
        rl.font.color.rgb = RGBColor(40, 40, 40)
        
        pr = cell_r.paragraphs[0]
        pr.paragraph_format.space_after = Pt(0)
        pr.paragraph_format.line_spacing = 1.15
        rr = pr.add_run(sig_r)
        rr.font.name = 'Arial'
        rr.font.size = Pt(8)
        rr.font.bold = True
        rr.font.color.rgb = RGBColor(40, 40, 40)
        
    for row in tbl_sig.rows:
        row.cells[0].width = Inches(3.1)
        row.cells[1].width = Inches(3.1)

    # Ancho del contenedor del acta
    for row in tbl_acta.rows:
        row.cells[0].width = Inches(6.5)

    doc.save(output_path)
    print(f"[OK] Documento estructurado guardado en: {output_path}")

if __name__ == "__main__":
    downloads_path = r"c:\Users\SENA\Downloads\TALLER PROCESO DE NEGOCIACIÓN DE TECNOLOGÍA INFORMÁTICA.docx"
    backup_path = r"c:\Users\SENA\Downloads\TALLER PROCESO DE NEGOCIACIÓN DE TECNOLOGÍA INFORMÁTICA_BACKUP.docx"
    repo_path = r"C:\Academix\docs\TALLER_PROCESO_NEGOCIACION_TECNOLOGIA_INFORMATICA_ACADEMIX.docx"
    
    # 1. Crear backup de seguridad del archivo original
    if os.path.exists(downloads_path) and not os.path.exists(backup_path):
        shutil.copy2(downloads_path, backup_path)
        print(f"[OK] Backup creado en: {backup_path}")
        
    # 2. Generar el documento estructurado en Downloads
    build_document(downloads_path)
    
    # 3. Guardar copia en el repositorio de Academix
    build_document(repo_path)
