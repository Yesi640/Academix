#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_cotizaciones_contrato_sla_docx.py
Genera el documento Word (DOCX) formal de:
- Cuadro comparativo de cotizaciones de infraestructura cloud (Render vs AWS vs DigitalOcean).
- Minuta de contrato informático de suministro, licenciamiento SaaS y mantenimiento.
- Anexo técnico de Acuerdo de Nivel de Servicio (SLA / Service Level Agreement).
Proyecto ACADEMIX v2.5.1 - SENA ADSO Ficha 3173430
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
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129)  # Azul Institucional SENA
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 125, 50)  # Verde Técnico
    else:
        run.font.size = Pt(10)
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
        r_t.font.color.rgb = RGBColor.from_string(title_color) if hasattr(RGBColor, 'from_string') else RGBColor(15, 76, 129)
    r_b = p.add_run(text)
    r_b.font.name = 'Arial'
    r_b.font.size = Pt(9)
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
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(40, 40, 40)
            if j == 0:
                run.font.bold = True
                
    # Column widths
    for row in tbl.rows:
        for j, w in enumerate(col_widths):
            row.cells[j].width = Inches(w)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return tbl

def generate_docx(output_path):
    doc = Document()
    
    # Márgenes 1 pulgada
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Encabezado institucional
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA)\nCENTRO DE FORMACIÓN EN TECNOLOGÍAS DE LA INFORMACIÓN\nTECNOLOGÍA EN ANÁLISIS Y DESARROLLO DE SOFTWARE (ADSO) — FICHA: 3173430")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph()
    
    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("CUADRO COMPARATIVO DE COTIZACIONES PONDERADAS,\nMINUTA DE CONTRATO INFORMÁTICO Y ACUERDO DE NIVEL DE SERVICIO (SLA)")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Evaluación Multicriterio de Proveedores Cloud (Render vs AWS vs DigitalOcean), Instrumento Legal con Cláusulas de Propiedad Intelectual (Ley 23 de 1982), Protección de Datos de Menores (Ley 1581) y Anexo Técnico de SLA")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(70, 70, 70)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Proyecto Formativo: Plataforma Web de Gestión Escolar ACADEMIX v2.5.1\nNoviembre de 2026")
    r_meta.font.name = 'Arial'
    r_meta.font.size = Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(46, 125, 50)
    
    doc.add_paragraph()
    
    # PARTE I: COTIZACIONES
    add_styled_heading(doc, "PARTE I: Cuadro Comparativo de Cotizaciones de Infraestructura Cloud", level=1)
    add_body_p(doc, "La plataforma ACADEMIX v2.5.1, desarrollada en Django 5.x y PostgreSQL 16, requiere infraestructura de alta disponibilidad para atender a una comunidad promedio de 1,200 estudiantes, 60 docentes y 1,000 padres de familia. Para su despliegue comercial y operativo, se evaluaron tres proveedores de clase mundial: Render Cloud, Amazon Web Services (AWS) y DigitalOcean.")
    
    add_styled_heading(doc, "1.1 Criterios Técnicos de Selección y Ponderación", level=2)
    headers_criterios = ["Criterio de Selección", "Peso (%)", "Justificación del Peso Técnico"]
    data_criterios = [
        ["1. Costo Total (TCO) y Previsibilidad", "25%", "Vital para colegios con presupuestos fijos anuales regulados por el MEN."],
        ["2. Rendimiento, Latencia y Uptime SLA", "25%", "Garantiza operatividad continua en cierres de periodo y emisión de boletines."],
        ["3. Seguridad y Ley 1581 (Menores)", "20%", "Cifrado en reposo/tránsito y aislamiento de datos de niños y adolescentes."],
        ["4. Facilidad de Despliegue CI/CD", "15%", "Automatización de despliegues vía GitHub con render.yaml sin sysadmin dedicado."],
        ["5. Soporte y Recuperación ante Fallos", "15%", "Métricas de consumo, backups diarios continuos y tiempo de recuperación RTO <= 2h."]
    ]
    build_table(doc, headers_criterios, data_criterios, [2.2, 1.0, 3.3], header_color="0F4C81")
    
    add_styled_heading(doc, "1.2 Comparación Técnica y Financiera de Proveedores Reales", level=2)
    headers_comp = ["Componente / Métrica", "Render Cloud (PaaS)", "AWS (Elastic Beanstalk / RDS)", "DigitalOcean (App Platform)"]
    data_comp = [
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
    build_table(doc, headers_comp, data_comp, [1.8, 1.6, 1.6, 1.5], header_color="2E7D32")
    
    add_styled_heading(doc, "1.3 Matriz de Calificación Cuantitativa Ponderada", level=2)
    headers_eval = ["Criterio de Evaluación", "Peso", "Render Cloud", "Amazon Web Services", "DigitalOcean"]
    data_eval = [
        ["1. Costo Total y Previsibilidad", "25%", "4.6 (1.15)", "3.5 (0.88)", "4.8 (1.20)"],
        ["2. Rendimiento, Latencia y Uptime", "25%", "4.5 (1.13)", "4.9 (1.23)", "4.4 (1.10)"],
        ["3. Seguridad y Ley 1581 (Menores)", "20%", "4.7 (0.94)", "5.0 (1.00)", "4.5 (0.90)"],
        ["4. Facilidad CI/CD y Mantenibilidad", "15%", "5.0 (0.75)", "3.2 (0.48)", "4.6 (0.69)"],
        ["5. Soporte y Recuperación ante Fallos", "15%", "4.4 (0.66)", "4.6 (0.69)", "4.3 (0.65)"],
        ["CALIFICACIÓN FINAL TOTAL", "100%", "4.63 / 5.00", "4.28 / 5.00", "4.54 / 5.00"],
        ["POSICIÓN DE SELECCIÓN", "—", "1er PUESTO (GANADOR)", "3er PUESTO", "2do PUESTO"]
    ]
    build_table(doc, headers_eval, data_eval, [2.3, 0.7, 1.2, 1.2, 1.1], header_color="0F4C81")
    
    add_callout(doc, 
        "JUSTIFICACIÓN DE LA ELECCIÓN: Se selecciona a RENDER CLOUD como proveedor oficial de hosting por obtener la mayor calificación (4.63/5.00). Ofrece previsibilidad presupuestal plana de $45.00 USD/mes (~$191,250 COP) sin sobrecostos imprevistos, compatibilidad nativa con el archivo render.yaml ya integrado en el repositorio Git de ACADEMIX, base de datos PostgreSQL en red privada segura (Ley 1581) y cero sobrecarga de administración de infraestructura para el equipo desarrollador.",
        "DICTAMEN FORMAL DE SELECCIÓN DE PROVEEDOR"
    )
    
    # PARTE II: CONTRATO INFORMÁTICO
    add_styled_heading(doc, "PARTE II: Minuta de Contrato Informático de Suministro y SaaS", level=1)
    add_body_p(doc, "CONTRATO No. ACAD-SENA-2026-088 celebrado entre ACADEMIX SOFTWARE SOLUTIONS, representada legalmente por SOFIA HELENA TORRES (en adelante EL CONTRATISTA), y el COLEGIO TÉCNICO PILOTO INSTITUCIONAL, representado por el Rector DR. CARLOS EDUARDO RAMÍREZ HOYOS (en adelante EL CONTRATANTE).")
    
    add_body_p(doc, "Suministrar, desplegar en infraestructura cloud, configurar, poner en marcha y mantener la plataforma web de gestión escolar ACADEMIX v2.5.1, garantizando los estándares de calidad ISO/IEC 25010 y el Acuerdo de Nivel de Servicio adjunto.", bold_prefix="Cláusula Primera (Objeto): ")
    
    add_body_p(doc, "El software comprende los 7 módulos activos: 1) Autenticación RBAC y Rate Limiting (apps.accounts); 2) Carga masiva transaccional con savepoints atómicos (apps.students); 3) Malla curricular y notas RAPs al 100.00% con Decimal (apps.grades); 4) Boletines oficiales PDF con QR criptográfico sin exposición de menores (apps.reports); 5) Control de periodos y bloqueo is_locked (apps.periods); 6) Asistencia y observador convivencial (apps.attendance/discipline); y 7) Bitácora inmutable de auditoría (apps.audit).", bold_prefix="Cláusula Segunda (Alcance Funcional): ")
    
    add_body_p(doc, "El valor total anual del servicio SaaS, hosting cloud, backups y soporte asciende a la suma de DOS MILLONES SEISCIENTOS MIL PESOS MONEDA CORRIENTE ($2,600,000 COP), exento de IVA (Art. 476 Numeral 21 Estatuto Tributario). Pagaderos: 30% al inicio ($780,000 COP), 40% a la carga de estudiantes y capacitación ($1,040,000 COP) y 30% al cierre del año lectivo ($780,000 COP).", bold_prefix="Cláusula Tercera (Valor y Forma de Pago): ")
    
    add_body_p(doc, "1) Garantizar disponibilidad mensual >= 99.50% según SLA; 2) Mantenimiento preventivo/correctivo de fallas; 3) Custodia de backups diarios; 4) Capacitación al personal docente y administrativo; y 5) Mantener el software libre de vulnerabilidades OWASP Top 10.", bold_prefix="Cláusula Cuarta (Obligaciones del Contratista): ")
    
    add_body_p(doc, "1) Pagar el valor acordado; 2) Suministrar información fidedigna de matrícula; 3) Custodiar credenciales de acceso rectoral; y 4) Obtener consentimiento informado de acudientes para el tratamiento de datos de menores de edad.", bold_prefix="Cláusula Quinta (Obligaciones del Contratante): ")
    
    add_body_p(doc, "Conforme a la Ley 23 de 1982 y la Decisión Andina 351 de 1993, los derechos morales y patrimoniales sobre el código fuente de ACADEMIX pertenecen a sus desarrolladores (EL CONTRATISTA). EL CONTRATANTE recibe una Licencia de Uso no exclusiva, intransferible y temporal. Sin embargo, EL CONTRATANTE es el único dueño de la base de datos de calificaciones y expedientes, la cual será entregada en formato abierto (.sql/CSV) al liquidar el contrato.", bold_prefix="Cláusula Sexta (Propiedad Intelectual y Licenciamiento): ")
    
    add_body_p(doc, "En estricto cumplimiento del Artículo 7 de la Ley 1581 de 2012 y Circular 002 de 2021 de la SIC, las partes reconocen el régimen especial de protección reforzada de datos de Niños, Niñas y Adolescentes (NNA). Todas las contraseñas se almacenan con hashes Argon2id/PBKDF2, el canal fuerza TLS 1.3 y la verificación pública por QR jamás divulga números de documento, teléfonos o direcciones de estudiantes menores.", bold_prefix="Cláusula Séptima (Protección de Datos de Menores y Habeas Data): ")
    
    add_body_p(doc, "Cualquier modificación o nuevo requerimiento funcional solicitado por el colegio que exceda el alcance de la versión 2.5.1 deberá tramitarse obligatoriamente mediante Formato de Solicitud de Cambio (Change Request - SCM) según IEEE 828 ante el Comité de Control de Cambios (CCB).", bold_prefix="Cláusula Octava (Gestión de Configuración - SCM): ")
    
    add_body_p(doc, "Duración de 12 meses prorrogables. Al término, EL CONTRATISTA suministrará volcado íntegro de base de datos y procederá al borrado seguro de la instancia institucional en nube en máximo 30 días calendario. Controversias se someterán a centro de conciliación de Buga o Cali bajo leyes de la República de Colombia.", bold_prefix="Cláusula Novena (Vigencia y Terminación): ")
    
    # PARTE III: ANEXO SLA
    add_styled_heading(doc, "PARTE III: Anexo Técnico — Acuerdo de Nivel de Servicio (SLA)", level=1)
    add_body_p(doc, "Establece los compromisos vinculantes de disponibilidad, tiempos máximos de respuesta ante incidentes, penalizaciones financieras por caída y políticas de respaldo:")
    
    add_body_p(doc, "EL CONTRATISTA garantiza un Uptime mensual >= 99.50% (máximo 216 minutos de indisponibilidad imprevista al mes). Fórmula: Disponibilidad (%) = [(Minutos Totales Mes - Minutos Caída) / Minutos Totales Mes] * 100.", bold_prefix="• Métrica de Uptime: ")
    
    headers_sla = ["Severidad", "Criterio de Impacto", "Respuesta (MTTA)", "Solución (MTTR)", "Acción Técnica"]
    data_sla = [
        ["1 (Crítica)", "Caída total del sistema o base de datos inaccesible", "<= 30 min", "<= 2 horas", "DevOps inmediato / Activación réplica local"],
        ["2 (Alta)", "Fallo de módulo crítico (ej. docentes no guardan notas)", "<= 1 hora", "<= 4 horas", "Asignación Backend / Reinicio de workers WSGI"],
        ["3 (Media)", "Fallo parcial menor que no frena la operación", "<= 2 horas", "<= 12 horas", "Solución en ciclo ordinario mediante rama fix/"],
        ["4 (Baja)", "Consultas de interfaz o dudas de manejo de usuarios", "<= 4 horas", "<= 24 horas", "Mesa de ayuda ordinaria (Lunes a Viernes 7am-5pm)"]
    ]
    build_table(doc, headers_sla, data_sla, [1.0, 2.3, 1.0, 1.0, 1.2], header_color="0F4C81")
    
    headers_penal = ["Disponibilidad Mensual Alcanzada", "Compensación / Descuento sobre Factura Siguiente"]
    data_penal = [
        ["Entre 99.00% y 99.49%", "10% de descuento sobre el canon mensual"],
        ["Entre 97.00% y 98.99%", "25% de descuento sobre el canon mensual"],
        ["Inferior al 97.00%", "50% de descuento y causal de terminación unilateral del contrato"]
    ]
    build_table(doc, headers_penal, data_penal, [3.2, 3.3], header_color="2E7D32")
    
    add_body_p(doc, "Backups automáticos diarios a las 02:00 am (Zona horaria Colombia). RPO (Punto de Recuperación Objetivo): Máximo 24 horas de datos. RTO (Tiempo de Recuperación Objetivo): Máximo 2 horas para restaurar el servicio en su totalidad.", bold_prefix="• Políticas de Respaldo y Recuperación (RPO / RTO): ")
    add_body_p(doc, "Mantenimientos mayores se ejecutarán exclusivamente en días domingos o festivos entre las 22:00 y las 04:00 horas, avisando al colegio con mínimo 48 horas de antelación.", bold_prefix="• Ventanas de Mantenimiento: ")
    
    # FIRMAS
    add_styled_heading(doc, "Formalización y Firmas Contractuales", level=1)
    add_body_p(doc, "En señal de conformidad y aceptación, se suscribe en la ciudad de Guadalajara de Buga (Valle del Cauca), a los veinticinco (25) días del mes de Noviembre de 2026.")
    
    doc.add_paragraph()
    p_sig = doc.add_paragraph()
    r_sig1 = p_sig.add_run("_________________________________________\nEL CONTRATISTA:\nSOFIA HELENA TORRES\nC.C. No. 1.118.234.567 de Buga\nRepresentante Legal Academix Software Solutions\nLíder de Aseguramiento de Calidad (SQA Lead)\nPrograma ADSO — Ficha 3173430\n\n")
    r_sig1.font.name = 'Arial'
    r_sig1.font.size = Pt(9)
    
    r_sig2 = p_sig.add_run("_________________________________________\nEL CONTRATANTE:\nDR. CARLOS EDUARDO RAMÍREZ HOYOS\nC.C. No. 16.789.012 de Cali\nRector y Ordenador del Gasto\nColegio Técnico Piloto Institucional\nNIT: 890.123.456-7")
    r_sig2.font.name = 'Arial'
    r_sig2.font.size = Pt(9)
    
    # REFERENCIAS
    add_styled_heading(doc, "Referencias Normativas y Bibliográficas (APA 7.ª Edición)", level=1)
    refs = [
        "Amazon Web Services. (2026). AWS Service Level Agreement and RDS Pricing Calculator. Seattle: AWS Inc.",
        "Comunidad Andina de Naciones [CAN]. (1993). Decisión 351: Régimen Común sobre Derecho de Autor y Derechos Conexos para Programas de Ordenador. Comisión del Acuerdo de Cartagena.",
        "Congreso de la República de Colombia. (1982). Ley 23 de 1982 sobre derechos de autor y propiedad intelectual en obras de software. Diario Oficial No. 35.939.",
        "Congreso de la República de Colombia. (1999). Ley 527 de 1999: Por medio de la cual se define y reglamenta el acceso y uso de los mensajes de datos, del comercio electrónico y de las firmas digitales. Diario Oficial No. 43.673.",
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012: Por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587.",
        "DigitalOcean. (2026). App Platform and Managed Databases SLA and Pricing Structure. Nueva York: DigitalOcean Holdings.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2012). IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering. Nueva York: IEEE Computer Society.",
        "Institute of Electrical and Electronics Engineers [IEEE]. (2014). IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes. Nueva York: IEEE Computer Society.",
        "International Organization for Standardization [ISO]. (2023). ISO/IEC 25010:2023: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model. Ginebra: ISO.",
        "Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). Resolución 1519 de 2020: Lineamientos de accesibilidad web universal (WCAG 2.1 AA). Bogotá: MinTIC.",
        "Render Services. (2026). Render Cloud Platform Pricing and Master Service Agreement. San Francisco: Render Inc.",
        "Superintendencia de Industria y Comercio [SIC]. (2021). Circular Externa 002 de 2021: Deberes y directrices de seguridad técnica en el tratamiento de datos de niños, niñas y adolescentes. Bogotá: SIC."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        run_ref = p_ref.add_run(r)
        run_ref.font.name = 'Arial'
        run_ref.font.size = Pt(8.5)
        run_ref.font.color.rgb = RGBColor(60, 60, 60)
        
    doc.save(output_path)
    print(f"[OK] Documento de cotizaciones, contrato y SLA generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Academix\docs\CUADRO_COMPARATIVO_COTIZACIONES_Y_MINUTA_CONTRATO_SLA_ACADEMIX.docx"
    generate_docx(out_file)
