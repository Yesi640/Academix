#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_tres_manuales_docx.py
Genera los 3 documentos oficiales en formato Microsoft Word (.docx) con diseño corporativo institucional:
1. MANUAL_DESPLIEGUE_Y_ACCESO_WEB_ACADEMIX.docx
2. docs/MANUAL_TECNICO_FINAL_ACADEMIX.docx
3. docs/MANUAL_DE_USUARIO_FINAL_ACADEMIX.docx
"""

import sys
import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PRIMARY_BLUE = RGBColor(15, 76, 129)       # #0F4C81
SECONDARY_PURPLE = RGBColor(124, 58, 237)  # #7C3AED
DARK_GRAY = RGBColor(40, 40, 40)
SUCCESS_GREEN = RGBColor(16, 149, 93)

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header_banner(doc, title, subtitle, status_text):
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_brand = title_p.add_run("ACADEMIX PLATFORM\n")
    run_brand.font.name = 'Arial'
    run_brand.font.size = Pt(24)
    run_brand.font.bold = True
    run_brand.font.color.rgb = PRIMARY_BLUE

    run_title = title_p.add_run(f"{title}\n")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    run_title.font.color.rgb = DARK_GRAY

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run(f"{subtitle}\n")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(10.5)
    run_sub.font.color.rgb = RGBColor(90, 90, 90)

    status_p = doc.add_paragraph()
    status_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_status = status_p.add_run(f"● {status_text}")
    run_status.font.name = 'Arial'
    run_status.font.size = Pt(9.5)
    run_status.font.bold = True
    run_status.font.color.rgb = SUCCESS_GREEN

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

def add_styled_heading(doc, text, level=1):
    h = doc.add_heading(level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    run = h.add_run(text)
    run.font.name = 'Arial'
    if level == 1:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_BLUE
    elif level == 2:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_PURPLE
    else:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = DARK_GRAY
    return h

def add_callout(doc, text, alert_type="INFO"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.7)

    cell = table.cell(0, 0)
    bg_color = "EBF5FB" if alert_type == "INFO" else "FDEDEC"
    border_color = "3498DB" if alert_type == "INFO" else "E74C3C"

    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(9.5)
    run.font.color.rgb = DARK_GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_credentials_table(doc):
    headers = ["Rol en el Selector", "Usuario / Documento", "ID Único Alumno", "Contraseña", "Perfil / Titular"]
    rows_data = [
        ("👑 Superadministrador", "admin", "N/A", "Academix2026!", "Administrador General de la Plataforma"),
        ("🏛️ Rector / Rectora", "rector", "N/A", "Academix2026!", "Rectoría y Dirección Institucional"),
        ("📋 Secretaría Académica", "nuryssecretaria", "N/A", "123456789", "Nurys - Secretaría y Admisiones"),
        ("👨‍🏫 Docente Titular", "docente", "N/A", "Academix2026!", "Docente Titular y Director de Grupo"),
        ("🎓 Alumno", "alumno", "ALU-2026-1001", "Academix2026!", "Alumno Ejemplar (Matriculado)"),
        ("👨‍👩‍👧 Padre de Familia", "padre", "ALU-2026-1001", "Academix2026!", "Acudiente Legal Vinculado"),
    ]

    table = doc.add_table(rows=len(rows_data) + 1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.6), Inches(1.2), Inches(1.2), Inches(1.1), Inches(1.6)]
    for i, col in enumerate(table.columns):
        col.width = col_widths[i]

    # Header Row
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.width = col_widths[col_idx]
        set_cell_background(cell, "0F4C81")
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.font.name = 'Arial'
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for row_idx, data in enumerate(rows_data):
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8F9FA"
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.name = 'Arial'
            run.font.size = Pt(8.5)
            if col_idx in (1, 2, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.bold = True
                if col_idx == 3:
                    run.font.color.rgb = RGBColor(180, 40, 40)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)


# ==============================================================================
# 1. GENERAR MANUAL DE DESPLIEGUE (.DOCX)
# ==============================================================================
def build_manual_despliegue():
    doc = Document()
    add_header_banner(
        doc,
        "MANUAL DE DESPLIEGUE, CONFIGURACIÓN Y ACCESO WEB",
        "Infraestructura Cloud, Integración Continua (CI/CD) y Acceso a Producción",
        "ESTADO: EN LÍNEA (LIVE) EN RENDER CLOUD | OCTUBRE 2026"
    )

    add_styled_heading(doc, "1. Datos Oficiales de Producción en Vivo", level=1)
    p = doc.add_paragraph()
    p.add_run("• Enlace Oficial en Internet: ").bold = True
    p.add_run("https://academix-q2g4.onrender.com\n")
    p.add_run("• Portal de Acceso (Login): ").bold = True
    p.add_run("https://academix-q2g4.onrender.com/accounts/login/\n")
    p.add_run("• Repositorio de Código en GitHub: ").bold = True
    p.add_run("https://github.com/Yesi640/Academix.git\n")

    add_styled_heading(doc, "2. Credenciales Maestras Permanentes Inicializadas", level=1)
    add_credentials_table(doc)
    add_callout(doc, "IMPORTANTE: Todas estas cuentas han sido provistas dentro del comando de arranque 'setup_production_init.py' de Render. Esto garantiza que nunca se borrarán incluso si el servidor gratuito entra en reposo temporal.", "INFO")

    add_styled_heading(doc, "3. Arquitectura y Pipeline de Despliegue en la Nube", level=1)
    p = doc.add_paragraph()
    p.add_run("El despliegue de ACADEMIX opera de forma totalmente automatizada mediante el siguiente flujo:\n")
    p.add_run("1. Commit & Push en GitHub: El desarrollador sube los cambios a la rama principal (main).\n")
    p.add_run("2. Detección Webhook: Render detecta la actualización y arranca un contenedor Linux de construcción.\n")
    p.add_run("3. Ejecución de build.sh: Actualiza pip, instala dependencias de requirements.txt, compila archivos estáticos (collectstatic) y aplica migraciones de base de datos.\n")
    p.add_run("4. Inicialización Maestra: Ejecuta setup_production_init asegurando escuelas, periodos y los 6 usuarios oficiales.\n")
    p.add_run("5. Arranque WSGI: Gunicorn inicia el servicio en el puerto asignado ($PORT) con soporte HTTPS nativo y WhiteNoise.")

    add_styled_heading(doc, "4. Variables de Entorno en el Dashboard de Render", level=1)
    vars_data = [
        ("DATABASE_URL", "postgresql://user:pass@host:5432/db", "Cadena de conexión PostgreSQL persistente."),
        ("USE_SQLITE_FALLBACK", "False", "Evita el uso de base de datos volátil en disco."),
        ("SECRET_KEY", "Generada en Render", "Clave criptográfica para firmas de sesión y CSRF."),
        ("DEBUG", "False", "Modo estricto de seguridad para ambiente de producción."),
        ("EMAIL_HOST_USER", "academix651@gmail.com", "Cuenta SMTP para envío de credenciales."),
        ("EMAIL_HOST_PASSWORD", "uzgn axgt yxpf mvvv", "Clave de aplicación Gmail de 16 caracteres."),
    ]
    t = doc.add_table(rows=len(vars_data) + 1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.columns[0].width = Inches(2.0)
    t.columns[1].width = Inches(2.3)
    t.columns[2].width = Inches(2.4)
    for i, h in enumerate(["Variable", "Valor Configurado", "Propósito"]):
        cell = t.cell(0, i)
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'; r.font.size = Pt(9); r.font.bold = True; r.font.color.rgb = RGBColor(255,255,255)
    for r_i, row in enumerate(vars_data):
        bg = "FFFFFF" if r_i % 2 == 0 else "F8F9FA"
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Arial'; r.font.size = Pt(8.5)
            if c_i == 0: r.font.bold = True

    try:
        output_path = Path("docs/MANUAL_DE_DESPLIEGUE_FINAL_ACADEMIX.docx")
        doc.save(str(output_path))
        print(f"[OK] Generado: {output_path}")
        root_path = Path("MANUAL_DESPLIEGUE_Y_ACCESO_WEB_ACADEMIX.docx")
        try:
            doc.save(str(root_path))
            print(f"[OK] Generado: {root_path}")
        except Exception:
            print(f"[AVISO] {root_path} está abierto en Word, se preserva en docs/MANUAL_DE_DESPLIEGUE_FINAL_ACADEMIX.docx")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar manual de despliegue: {e}")


# ==============================================================================
# 2. GENERAR MANUAL TÉCNICO (.DOCX)
# ==============================================================================
def build_manual_tecnico():
    doc = Document()
    add_header_banner(
        doc,
        "MANUAL TÉCNICO DE INGENIERÍA Y ARQUITECTURA DE SOFTWARE",
        "Especificación Técnica de Modelos de Datos, Seguridad, Concurrencia y API",
        "VERSIÓN: 2.5.0 | FRAMEWORK: DJANGO 5.x / PYTHON 3.10+ | PRODUCCIÓN"
    )

    add_styled_heading(doc, "1. Arquitectura General y Patrón Multi-Sede", level=1)
    p = doc.add_paragraph()
    p.add_run("ACADEMIX está desarrollado bajo una arquitectura modular limpia en capas (MVT - Modelo Vista Plantilla) extendida con capas de Servicios (Services) y Reglas de Negocio (Rules). La plataforma incorpora soporte nativo para múltiples sedes educativas (Multi-School SaaS) a través de la entidad ")
    p.add_run("School").bold = True
    p.add_run(", permitiendo que cada usuario pertenezca a su respectiva institución con aislamiento visual de colores institucionales, escudos y calendarios escolares.")

    add_styled_heading(doc, "2. Stack Tecnológico de Grado Corporativo", level=1)
    stack_data = [
        ("Lenguaje Backend", "Python 3.10 / 3.11 / 3.12", "Tipado dinámico estricto, async support y compatibilidad cloud."),
        ("Framework Web", "Django 5.0+ / 5.1+", "ORM relacional, autenticación segura, CSRF nativo y sistema de caché."),
        ("Servidor de Producción", "Gunicorn 22.0.0+", "Servidor WSGI pre-fork con manejo eficiente de workers y memoria."),
        ("Base de Datos", "PostgreSQL 15+ / SQLite WAL", "Transacciones atómicas (ATOMIC_REQUESTS=True) y concurrencia optimizada."),
        ("Distribución Estática", "WhiteNoise 6.8.0+", "Servidor de compresión Gzip y Brotli con hash de versiones para caché."),
        ("Generación Documental", "OpenPyXL, QRCode, python-docx", "Exportación de sábanas en Excel, QR en boletines y actas en Word."),
    ]
    t = doc.add_table(rows=len(stack_data) + 1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.columns[0].width = Inches(1.8)
    t.columns[1].width = Inches(2.0)
    t.columns[2].width = Inches(2.9)
    for i, h in enumerate(["Componente", "Tecnología / Versión", "Funcionalidad en ACADEMIX"]):
        cell = t.cell(0, i)
        set_cell_background(cell, "0F4C81")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'; r.font.size = Pt(9); r.font.bold = True; r.font.color.rgb = RGBColor(255,255,255)
    for r_i, row in enumerate(stack_data):
        bg = "FFFFFF" if r_i % 2 == 0 else "F8F9FA"
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Arial'; r.font.size = Pt(8.5)
            if c_i == 0: r.font.bold = True

    add_styled_heading(doc, "3. Modelo Relacional de Base de Datos y Entidades", level=1)
    p = doc.add_paragraph()
    p.add_run("Las entidades nucleares del sistema se dividen en los siguientes dominios:\n")
    p.add_run("• apps.accounts (CustomUser, School): ").bold = True
    p.add_run("Maneja la autenticación, tipo y número de documento, escuela y 6 roles institucionales.\n")
    p.add_run("• apps.students (StudentProfile, Enrollment): ").bold = True
    p.add_run("Expediente con ID único de estudiante, ficha médica, tipo de sangre, acudiente y matrícula en curso.\n")
    p.add_run("• apps.teachers (TeacherProfile, TeachingAssignment): ").bold = True
    p.add_run("Ficha profesional docente, asignación a grupos escolares y asignaturas con rol de director de grupo.\n")
    p.add_run("• apps.courses (GradeLevel, CourseSection, AcademicYear): ").bold = True
    p.add_run("Catálogo escolar de Transición a 11°, aulas físicas y periodos lectivos.\n")
    p.add_run("• apps.grades (Grade, EvaluationCriteria): ").bold = True
    p.add_run("Calificaciones en dimensiones SABER (40%), HACER (40%) y SER (20%) con equivalencia en escala nacional MEN.\n")
    p.add_run("• apps.audit (AuditLog): ").bold = True
    p.add_run("Registro inmutable de auditoría con fecha, hora, IP, usuario, tabla afectada y valores JSON previos/nuevos.")

    add_styled_heading(doc, "4. Seguridad y Hardening en Producción", level=1)
    add_callout(doc, "El sistema superó exitosamente la auditoría de despliegue 'python manage.py check --deploy' con redirección obligatoria a HTTPS (SECURE_SSL_REDIRECT), cookies HTTPOnly seguras, cabecera HSTS a 1 año y protección total contra clickjacking e inyecciones de cabecera.", "INFO")

    output_path = Path("docs/MANUAL_TECNICO_FINAL_ACADEMIX.docx")
    doc.save(str(output_path))
    print(f"[OK] Generado: {output_path}")


# ==============================================================================
# 3. GENERAR MANUAL DE USUARIO (.DOCX)
# ==============================================================================
def build_manual_usuario():
    doc = Document()
    add_header_banner(
        doc,
        "MANUAL DE USUARIO FINAL Y OPERACIÓN POR ROLES",
        "Guía Integral de Procedimientos Escolares para Directivos, Docentes, Alumnos y Padres",
        "VERSIÓN: 2.5.0 | GUÍA OFICIAL ACADEMIX | OCTUBRE 2026"
    )

    add_styled_heading(doc, "1. Introducción al Sistema", level=1)
    p = doc.add_paragraph()
    p.add_run("Bienvenido a ")
    p.add_run("ACADEMIX").bold = True
    p.add_run(", la solución tecnológica integral para la administración pedagógica y el control escolar. Esta guía le permitirá comprender de forma clara y paso a paso cómo ingresar y utilizar cada una de las funcionalidades de acuerdo con su rol dentro del plantel educativo.")

    add_styled_heading(doc, "2. Cuentas Oficiales y Credenciales de Acceso", level=1)
    add_credentials_table(doc)

    add_styled_heading(doc, "3. Procedimiento Paso a Paso para Iniciar Sesión", level=1)
    p = doc.add_paragraph()
    p.add_run("1. Abra su navegador web (Chrome, Edge o Firefox) e ingrese a la dirección: ")
    p.add_run("https://academix-q2g4.onrender.com/accounts/login/\n").bold = True
    p.add_run("2. En el campo 'Colegio / Escuela', confirme que se encuentra seleccionada su sede oficial.\n")
    p.add_run("3. En el selector 'ROL EN EL SISTEMA', elija exactamente el rol que le corresponde (Docente, Alumno, Padre, etc.).\n")
    p.add_run("4. Si seleccionó 'Alumno', ingrese su ID ÚNICO (ejemplo: ALU-2026-1001) y su contraseña.\n")
    p.add_run("5. Si seleccionó 'Padre de Familia', ingrese su usuario de acudiente y el ID ÚNICO de su hijo.\n")
    p.add_run("6. Presione 'Ingresar a la Plataforma' para acceder a su panel de control personalizado.")

    add_styled_heading(doc, "4. Guía Operativa por Roles Institucionales", level=1)

    add_styled_heading(doc, "A. Secretaría Académica (nuryssecretaria / 123456789)", level=2)
    p = doc.add_paragraph()
    p.add_run("• Admisión y Matrícula: Ingrese a 'Estudiantes' y haga clic en '+ Nuevo Alumno'. Diligencie los datos de identidad y seleccione el grupo escolar. El sistema generará el código ALU-2026-XXXX y enviará las credenciales por correo automáticamente.\n")
    p.add_run("• Cartera y Recibos: Registre cobros de matrícula o pensiones, expidiendo constancias de paz y salvo.\n")
    p.add_run("• Certificados de Estudio: Emita certificados escolares con sellos institucionales y códigos de verificación.")

    add_styled_heading(doc, "B. Docente Titular (docente / Academix2026!)", level=2)
    p = doc.add_paragraph()
    p.add_run("• Calificaciones Bimestrales: Ingrese a 'Calificaciones', seleccione su salón y digite las notas en las dimensiones Cognitiva (40%), Procedimental (40%) y Actitudinal (20%).\n")
    p.add_run("• Asistencia en Aula: Registre fallas, retardos o justificaciones médicas con un solo clic.\n")
    p.add_run("• Tareas y Trabajos: Publique actividades escolares con fecha de entrega y califique los archivos enviados por los estudiantes.\n")
    p.add_run("• Observador Convivencial: Anote reconocimientos o faltas disciplinarias según el manual de convivencia.")

    add_styled_heading(doc, "C. Estudiante (alumno / ALU-2026-1001 / Academix2026!)", level=2)
    p = doc.add_paragraph()
    p.add_run("• Mis Tareas: Consulte trabajos pendientes y suba sus archivos de respuesta antes del plazo límite.\n")
    p.add_run("• Mis Notas y Boletín: Revise sus notas acumuladas por periodo y descargue su boletín de calificaciones oficial con código QR.")

    add_styled_heading(doc, "D. Padre de Familia / Acudiente (padre / ALU-2026-1001 / Academix2026!)", level=2)
    p = doc.add_paragraph()
    p.add_run("• Seguimiento en Tiempo Real: Monitoree el rendimiento académico y las tareas de su acudiente.\n")
    p.add_run("• Novedades de Asistencia y Convivencia: Reciba alertas si su hijo falta a clases o tiene anotaciones en el observador escolar.")

    add_styled_heading(doc, "5. Preguntas Frecuentes", level=1)
    add_callout(doc, "¿Por qué el sistema dice 'No existe ningún usuario registrado con...'?\nVerifique que en el selector de 'ROL EN EL SISTEMA' haya elegido el rol correcto (por ejemplo, si es estudiante debe cambiar a 'Alumno'). Los alumnos y padres deben ingresar obligatoriamente con el ID ÚNICO (ejemplo: ALU-2026-1001).", "INFO")

    output_path = Path("docs/MANUAL_DE_USUARIO_FINAL_ACADEMIX.docx")
    doc.save(str(output_path))
    print(f"[OK] Generado: {output_path}")


if __name__ == "__main__":
    print("Iniciando generación de los 3 manuales oficiales en formato Word (.docx)...")
    build_manual_despliegue()
    build_manual_tecnico()
    build_manual_usuario()
    print("¡Todos los manuales fueron generados exitosamente!")
