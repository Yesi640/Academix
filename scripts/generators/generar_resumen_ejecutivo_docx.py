"""
Generador del Resumen Ejecutivo e Informe Administrativo Oficial en formato Word (.docx)
para la plataforma multi-escuela ACADEMIX y su despliegue web en Render / GitHub.
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="none"/></w:tblBorders>')
        tblPr[0].append(borders)

def build_executive_summary_docx(output_path):
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Estilos de fuentes y colores
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    COLOR_PRIMARY = RGBColor(0x4C, 0x1D, 0x95)    # Violet 900
    COLOR_SECONDARY = RGBColor(0x02, 0x84, 0xC7)  # Sky 600
    COLOR_DARK = RGBColor(0x0F, 0x17, 0x2A)       # Slate 900
    COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)      # Slate 500

    # ── PORTADA EJECUTIVA ──
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(36)
    p_pre.paragraph_format.space_after = Pt(4)
    run_pre = p_pre.add_run("INFORME EJECUTIVO & ADMINISTRATIVO")
    run_pre.bold = True
    run_pre.font.size = Pt(12)
    run_pre.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run("ACADEMIX — Plataforma Web Multi-Institucional")
    run_title.bold = True
    run_title.font.size = Pt(24)
    run_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(20)
    run_sub = p_sub.add_run("Gestión Académica Integral, Multi-Sedes/Colegios, Branding Dinámico, Auditoría Inmutable y Despliegue en la Nube (Render & GitHub)")
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_MUTED

    # Ficha técnica
    table_meta = doc.add_table(rows=5, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False
    for row in table_meta.rows:
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.3)

    meta_data = [
        ("Estado de la Plataforma", "🟢 EN LÍNEA Y OPERATIVO (Producción Cloud Render)"),
        ("URL de Producción", "https://academix-q2g4.onrender.com"),
        ("Repositorio GitHub", "https://github.com/Yesi640/Academix.git"),
        ("Versión del Sistema", "v2.5 Enterprise Multi-Tenant (Django 5.1 + PostgreSQL/SQLite)"),
        ("Fecha de Informe", "16 de Octubre de 2026"),
    ]

    for idx, (label, val) in enumerate(meta_data):
        c0, c1 = table_meta.rows[idx].cells
        c0.text = label
        c1.text = val
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c0, "EDE9FE")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)

    set_table_borders(table_meta, color="C4B5FD")

    doc.add_page_break()

    def add_section_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_section_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(12.5)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.size = Pt(10.5)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.size = Pt(10)
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        return p

    # ── 1. RESUMEN EJECUTIVO DE LA SOLUCIÓN ──
    add_section_h1("1. Resumen Ejecutivo del Proyecto")
    add_body(
        "ACADEMIX ha evolucionado de ser una solución de gestión escolar monopuesto a convertirse en una "
        "plataforma SaaS (Software as a Service) multi-institucional capaz de operar en la nube para múltiples colegios, "
        "sedes educativas e institutos de formación. La plataforma ofrece soporte completo a los roles de Rector, Docente, "
        "Estudiante, Acudiente/Padre de Familia, Administrador y Secretaria, asegurando segregación de datos, auditoría forense "
        "inmutable y personalización completa de identidad de marca."
    )

    # ── 2. ARQUITECTURA MULTI-ESCUELA Y MARCA PERSONALIZADA ──
    add_section_h1("2. Nueva Arquitectura Multi-Escuela y Personalización de Marca")
    add_body(
        "En cumplimiento de los requerimientos estratégicos de comercialización y despliegue a diferentes instituciones, "
        "se implementó el módulo de gestión de escuelas y personalización de interfaz:"
    )

    add_bullet(" Almacena el nombre oficial, código único interno, código DANE, ciudad, teléfono, correo de contacto, logotipo oficial y esquema de colores primario y secundario en formato hexadecimal.", "Modelo Institucional (School):")
    add_bullet(" En la pantalla de bienvenida y acceso, si la plataforma cuenta con múltiples escuelas activas, los usuarios seleccionan visualmente su colegio mediante tarjetas interactivas que reflejan el logo y colores de cada plantel.", "Selector de Escuela en Login:")
    add_bullet(" Al momento de registrarse un nuevo estudiante, padre o docente, el formulario permite elegir obligatoriamente a qué plantel educativo pertenece, asignándole su ID Único Institucional.", "Selector de Escuela en Registro:")
    add_bullet(" Disponible exclusivamente para el Administrador de la Plataforma en /accounts/schools/, permitiendo crear nuevas instituciones, subir sus logos, definir su paleta de color y activar o suspender el acceso de forma inmediata.", "Panel de Gestión de Escuelas:")
    add_bullet(" Endpoint REST en /accounts/api/schools/ que expone el listado de planteles activos en JSON para integraciones externas, apps móviles o portales web institucionales.", "API de Escuelas:")

    # ── 3. DATOS DE DESPLIEGUE EN LA NUBE Y REPOSITORIO ──
    add_section_h1("3. Infraestructura de Producción en Render y GitHub")
    add_body(
        "El sistema se encuentra integrado en un flujo de Entrega Continua (CI/CD) conectado al repositorio central en GitHub:"
    )

    table_links = doc.add_table(rows=6, cols=2)
    table_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_links.autofit = False
    for row in table_links.rows:
        row.cells[0].width = Inches(2.4)
        row.cells[1].width = Inches(4.1)

    links_info = [
        ("Plataforma Web en Vivo", "https://academix-q2g4.onrender.com"),
        ("Portal de Ingreso (Login)", "https://academix-q2g4.onrender.com/accounts/login/"),
        ("Registro Institucional", "https://academix-q2g4.onrender.com/accounts/register/"),
        ("Gestión de Escuelas (Admin)", "https://academix-q2g4.onrender.com/accounts/schools/"),
        ("Repositorio GitHub", "https://github.com/Yesi640/Academix.git"),
        ("Proveedor Cloud / Hosting", "Render.com (Web Service Linux + Gunicorn + WhiteNoise)"),
    ]

    for idx, (label, val) in enumerate(links_info):
        c0, c1 = table_links.rows[idx].cells
        c0.text = label
        c1.text = val
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c0, "EDE9FE")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)

    set_table_borders(table_links, color="C4B5FD")

    # ── 4. SEGURIDAD Y PERMISOS DE ACCESO ──
    add_section_h1("4. Credenciales de Alta Dirección y Control de Acceso")
    add_body(
        "El sistema cuenta con usuarios administrativos inicializados de forma segura para la supervisión y entrega:"
    )

    table_users = doc.add_table(rows=3, cols=4)
    table_users.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_users.autofit = False
    for row in table_users.rows:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(1.3)
        row.cells[2].width = Inches(1.4)
        row.cells[3].width = Inches(2.0)

    headers = ["Rol Institucional", "Usuario", "Contraseña", "Alcance de Control"]
    for idx, h in enumerate(headers):
        c = table_users.rows[0].cells[idx]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c, "4C1D95")
        set_cell_margins(c, 120, 120, 120, 120)

    rows_data = [
        ("Superadministrador", "admin", "Academix2026!", "Control total, escuelas, marcas, auditoría y base de datos."),
        ("Rector General", "rector", "Academix2026!", "Supervisión pedagógica, observaciones, reportes y cierres."),
    ]

    for r_idx, r_data in enumerate(rows_data):
        for c_idx, val in enumerate(r_data):
            c = table_users.rows[r_idx + 1].cells[c_idx]
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 100, 100, 120, 120)

    set_table_borders(table_users, color="E2E8F0")

    # ── 5. MANUAL OPERATIVO PARA EL ADMINISTRADOR ──
    add_section_h1("5. Manual Operativo: Cómo Registrar y Vender a una Nueva Escuela")
    add_body(
        "Cuando se concrete la venta o adopción del software para una nueva institución educativa, el Administrador debe seguir estos sencillos pasos:"
    )

    add_bullet(" Iniciar sesión con la cuenta de Administrador o Rector y dirigirse en el menú lateral a 'Administración y Marca' > 'Gestión de Escuelas'.", "Paso 1: Acceso al Módulo:")
    add_bullet(" Hacer clic en el botón '+ Nueva Escuela' e ingresar el Nombre Oficial, Código Corto (ej: COL-02) y Ciudad de la institución.", "Paso 2: Registro de Datos Básicos:")
    add_bullet(" En la columna derecha, seleccionar el color primario y secundario que identifican el escudo o bandera del colegio, y cargar el archivo de imagen de su Logo Institucional.", "Paso 3: Personalización de Marca:")
    add_bullet(" Guardar el formulario. De manera automática, la nueva escuela aparecerá disponible tanto en la pantalla de bienvenida y Login como en el formulario de Registro público.", "Paso 4: Publicación Inmediata:")
    add_bullet(" Los alumnos que se registren en esa institución recibirán su código ID ÚNICO personalizado, y los docentes quedarán vinculados a las asignaturas de dicho plantel.", "Paso 5: Vinculación de Comunidad:")

    # ── 6. CIERRE Y FIRMA ──
    add_section_h1("6. Conclusión y Estado de Entrega")
    add_body(
        "El aplicativo ACADEMIX cumple a cabalidad con las directrices de inmutabilidad académica, blindaje de seguridad "
        "conforme a la norma ISO/IEC 27001, capacidad multi-inquilino institucional y despliegue automatizado en internet. "
        "Se encuentra listo para su presentación y explotación comercial en cualquier entidad educativa básica, media o técnica."
    )

    p_firm = doc.add_paragraph()
    p_firm.paragraph_format.space_before = Pt(30)
    r_firm = p_firm.add_run("Equipo de Desarrollo e Ingeniería ACADEMIX\nDespliegue y Aseguramiento de Calidad de Software — 2026")
    r_firm.bold = True
    r_firm.font.size = Pt(10)
    r_firm.font.color.rgb = COLOR_PRIMARY

    doc.save(output_path)
    print(f"Documento guardado exitosamente en: {output_path}")

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RESUMEN_EJECUTIVO_INFORME_ADMINISTRATIVO.docx')
    build_executive_summary_docx(target)
