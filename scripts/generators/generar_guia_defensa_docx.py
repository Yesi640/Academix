#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar_guia_defensa_docx.py
Genera el documento Word (DOCX) de la:
GUÍA MAESTRA DE DEFENSA TÉCNICA Y RESOLUCIÓN DE SABOTAJES EN VIVO — ACADEMIX v2.5.1
Manual para la evaluación individual del instructor SENA (Ficha 3173430).
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
        run.font.color.rgb = RGBColor(15, 76, 129)  # Azul Institucional
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 125, 50)  # Verde Técnico
    else:
        run.font.size = Pt(10)
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
        r_bold.font.size = Pt(9.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(30, 30, 30)
    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(9.5)
    r_text.font.italic = italic
    r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_callout(doc, text, title=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "FBE9E7")  # Naranja claro de advertencia
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    if title:
        r_t = p.add_run(title + "\n")
        r_t.font.name = 'Arial'
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(198, 40, 40)
    r_b = p.add_run(text)
    r_b.font.name = 'Arial'
    r_b.font.size = Pt(9.5)
    r_b.font.bold = False
    r_b.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

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
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def generate_guia_docx(output_path):
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Encabezado
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SERVICIO NACIONAL DE APRENDIZAJE (SENA) — ADSO FICHA 3173430\nMANUAL DE CONOCIMIENTO TÉCNICO Y RESOLUCIÓN DE SABOTAJES EN VIVO")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph()
    
    # Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("GUÍA MAESTRA DE DEFENSA TÉCNICA DEL CÓDIGO DE ACADEMIX")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Explicación exacta de cada archivo, función y modelo, diagnóstico de errores provocados en vivo por el instructor y fórmulas de reparación inmediata")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(70, 70, 70)
    
    doc.add_paragraph()
    
    # Fórmula de respuesta
    add_callout(doc, 
        "1. QUÉ HACE: 'Profesor, ese bloque/función se encarga de [Función exacta en el sistema].'\n"
        "2. QUÉ DAÑÓ: 'Al modificar o borrar esa línea, usted acaba de romper [Mecanismo afectado].'\n"
        "3. QUÉ ERROR DA: 'En pantalla o consola saldrá un error [Nombre de la Excepción / Código HTTP].'\n"
        "4. CÓMO SE ARREGLA: 'Para solucionarlo, la línea correcta que debe restaurarse es [Código exacto].'",
        "LA FÓRMULA DE RESPUESTA EN 4 PASOS ANTE EL SABOTAJE DEL PROFESOR"
    )
    
    # SECCIÓN 1: CONFIG
    add_styled_heading(doc, "1. El Cerebro del Sistema: config/settings.py y config/urls.py", level=1)
    add_body_p(doc, "Le indica a Django que reemplace su tabla nativa de usuarios por nuestro modelo personalizado con roles institucionales (CustomUser). Si el profesor lo borra: salta InconsistentMigrationHistory y destruye todo el sistema de roles RBAC. Se arregla restaurando AUTH_USER_MODEL = 'accounts.CustomUser'.", bold_prefix="• AUTH_USER_MODEL = 'accounts.CustomUser': ")
    add_body_p(doc, "Lista las 15 micro-aplicaciones del sistema. Si el profesor borra 'apps.grades': salta LookupError: No installed app with label 'grades' y TemplateSyntaxError en pantallas de notas. Se arregla reincorporando la app a la lista.", bold_prefix="• INSTALLED_APPS: ")
    add_body_p(doc, "Filtros de cada petición HTTP. Si el profesor quita AuthenticationMiddleware: salta AttributeError: 'WSGIRequest' object has no attribute 'user' colapsando el 100% de las vistas. Si quita CsrfViewMiddleware: deja el sistema vulnerable a ataques de falsificación de sesión.", bold_prefix="• MIDDLEWARE: ")
    add_body_p(doc, "Si el profesor pone DEBUG = False sin configurar ALLOWED_HOSTS: sale Bad Request (400) - Invalid HTTP_HOST header y nadie puede acceder. Se arregla agregando ALLOWED_HOSTS = ['*'] o ['localhost'].", bold_prefix="• DEBUG y ALLOWED_HOSTS: ")
    add_body_p(doc, "Enrutador maestro. Si el profesor borra include('apps.grades.urls'): cualquier acceso a calificaciones devuelve HTTP 404 Page Not Found.", bold_prefix="• config/urls.py: ")
    
    # SECCIÓN 2: ACCOUNTS
    add_styled_heading(doc, "2. Autenticación y Control de Acceso: apps/accounts/", level=1)
    add_body_p(doc, "Define los 6 roles oficiales (ADMIN, RECTOR, SECRETARIA, TEACHER, STUDENT, PARENT) y el documento de identidad único. Las propiedades @property def is_teacher(self): evalúan el rol del usuario.", bold_prefix="• CustomUser en models.py: ")
    add_body_p(doc, "Si el profesor borra el decorador @property en is_teacher: las plantillas evalúan la función como objeto existente (True), otorgando permisos de docente a estudiantes; y en código Python salta TypeError: 'bool' object is not callable.", bold_prefix="⚠️ Sabotaje en is_teacher: ")
    add_body_p(doc, "Valida credenciales, aplica limitación de tasa (5 intentos/min por IP con HTTP 429) y crea la sesión. Si el profesor comenta login(request, user): el usuario digita clave correcta pero la página recarga y nunca entra al sistema.", bold_prefix="• login_view en views.py: ")
    add_body_p(doc, "Si el profesor quita el decorador @ratelimit(key='ip', rate='5/m', block=True): deja el sistema abierto a ataques automatizados de fuerza bruta (Violación OWASP Top 10 A07 y Hallazgo HAL-01).", bold_prefix="⚠️ Sabotaje en login_view: ")
    
    # SECCIÓN 3: GRADES
    add_styled_heading(doc, "3. Motor Curricular, Calificaciones y RAPs al 100%: apps/grades/", level=1)
    add_body_p(doc, "Modela las columnas de la planilla (los RAPs o actividades). Cada una tiene un porcentaje que debe sumar el 100.00% del periodo. El uso de Decimal(5,2) es obligatorio.", bold_prefix="• EvaluationCriterion en models.py: ")
    add_body_p(doc, "Si el profesor cambia Decimal por float: se introducen errores de precisión binaria (ej. 3.3000000000000003), los porcentajes nunca suman 100.00% exactos y el periodo no se puede cerrar.", bold_prefix="⚠️ Sabotaje con Float: ")
    add_body_p(doc, "Guarda la nota individual. Obliga a Decimal(4,2) entre 0.00 y 10.00. Tiene is_locked para congelar notas una vez finalizado el corte.", bold_prefix="• GradeRecord en models.py: ")
    add_body_p(doc, "Aplica la sumatoria ponderada: Nota * (Porcentaje / 100) con redondeo ROUND_HALF_UP. Si el profesor quita la división / Decimal('100.00'): una nota de 4.0 al 30% suma 120.00 en vez de 1.20, desbordando los 4 dígitos del campo (DataError: numeric field overflow).", bold_prefix="• calculate_period_final_grade en services.py: ")
    
    # SECCIÓN 4: PERIODS
    add_styled_heading(doc, "4. Control de Periodos y Bloqueo: apps/periods/", level=1)
    add_body_p(doc, "Controla los estados: ACTIVE (abierto), CLOSED (cerrado) y LOCKED (bloqueado). La propiedad is_editable valida self.status == Status.ACTIVE.", bold_prefix="• AcademicPeriod en models.py: ")
    add_body_p(doc, "Si el profesor cambia is_editable para que devuelva True: cualquier profesor puede alterar notas de periodos pasados que ya fueron entregados en boletines oficiales.", bold_prefix="⚠️ Sabotaje en is_editable: ")
    
    # SECCIÓN 5: STUDENTS BULK UPLOAD
    add_styled_heading(doc, "5. Carga Masiva Transaccional y Savepoints: apps/students/", level=1)
    add_body_p(doc, "Lee archivos Excel (.xlsx) y CSV. Crea usuarios, perfiles y matrículas automáticamente. Cada fila se procesa dentro de un Savepoint con with transaction.atomic():.", bold_prefix="• bulk_upload_students_view en views.py: ")
    add_body_p(doc, "Si el profesor borra with transaction.atomic(): si el estudiante de la fila 45 tiene un dato erróneo, los anteriores quedan creados pero sin matricular (usuarios huérfanos) y el sistema no permite reintentar por error de cédula duplicada.", bold_prefix="⚠️ Sabotaje de Transacciones ACID: ")
    add_body_p(doc, "Si el profesor borra la lectura de openpyxl: los archivos .xlsx (que son binarios comprimidos en ZIP con cabecera PK\\x03\\x04) se intentan leer como texto plano, arrojando UnicodeDecodeError y error 500.", bold_prefix="⚠️ Sabotaje en formato Excel: ")
    
    # SECCIÓN 6: REPORTS & QR
    add_styled_heading(doc, "6. Boletines Oficiales PDF y Verificación QR: apps/reports/", level=1)
    add_body_p(doc, "Permite verificar con celular la validez del boletín escaneando el código QR con un token criptográfico. Debe ser pública pero sin mostrar datos privados de menores.", bold_prefix="• verify_bulletin_view en views.py: ")
    add_body_p(doc, "Si el profesor le pone @login_required a verify_bulletin_view: pide contraseña a cualquier persona en la calle que escanee el QR, inutilizando la verificación externa.", bold_prefix="⚠️ Sabotaje en QR: ")
    add_body_p(doc, "Si el profesor expone cédula, teléfono o dirección en la pantalla del QR: viola el Artículo 7 de la Ley 1581 de 2012 (Protección reforzada de datos de menores) y genera sanciones de la SIC.", bold_prefix="⚠️ Sabotaje de Privacidad (Ley 1581): ")
    
    # SECCIÓN 7: TEMPLATES & CSRF
    add_styled_heading(doc, "7. Seguridad en Plantillas Web: templates/", level=1)
    add_body_p(doc, "Si el profesor borra {% csrf_token %} en el formulario de login o de notas: Django bloquea de inmediato la petición arrojando HTTP 403 Forbidden - CSRF verification failed. Se arregla escribiendo {% csrf_token %} dentro del form.", bold_prefix="⚠️ Sabotaje en {% csrf_token %}: ")
    add_body_p(doc, "Si el profesor borra role='alert' y aria-live='assertive' en login.html: incumple la Resolución 1519 de 2020 de MinTIC sobre accesibilidad web WCAG 2.1 AA (los lectores de pantalla para invidentes no leen los errores).", bold_prefix="⚠️ Sabotaje en Accesibilidad ARIA: ")
    add_body_p(doc, "Si el profesor cambia {% block content %} por {% block contenido %} en base.html: las páginas hijas no coinciden y la pantalla se ve completamente blanca o vacía.", bold_prefix="⚠️ Sabotaje en Herencia de Plantillas: ")
    
    # SECCIÓN 8: TABLA TOP 20
    add_styled_heading(doc, "8. Top 20 de Sabotajes Más Probables del Profesor", level=1)
    headers_top20 = ["#", "¿Qué va a dañar?", "Archivo", "Error en Pantalla", "Explicación y Solución Exacta"]
    data_top20 = [
        ["01", "Borra {% csrf_token %}", "templates/login.html", "HTTP 403 Forbidden", "Falta token contra falsificación CSRF. Se escribe {% csrf_token %}."],
        ["02", "Comenta AUTH_USER_MODEL", "config/settings.py", "InconsistentMigration", "Django usa User nativo sin roles. Restaurar AUTH_USER_MODEL."],
        ["03", "Cambia Decimal por float", "apps/grades/services.py", "Notas con 3.4999999", "Error de precisión binaria. La norma ISO 25010 exige Decimal."],
        ["04", "Borra transaction.atomic()", "apps/students/views.py", "Usuarios huérfanos / BD corrupta", "Quitó el Savepoint ACID. Restaurar with transaction.atomic()."],
        ["05", "Quita @login_required", "apps/grades/views.py", "Acceso anónimo a notas", "Vista desprotegida. Colocar decorador @login_required."],
        ["06", "Pone @login_required en QR", "apps/reports/views.py", "Pide login al escanear QR", "La verificación de autenticidad debe ser pública sin login."],
        ["07", "Cambia is_editable a True", "apps/periods/models.py", "Fraude en notas cerradas", "Permite modificar notas extemporáneas. Validar Status.ACTIVE."],
        ["08", "Quita unique_together", "apps/grades/models.py", "Columnas RAP duplicadas", "Quita restricción de unicidad relacional. Restaurar unique_together."],
        ["09", "Comenta login(request, user)", "apps/accounts/views.py", "Login no inicia sesión", "No guarda la cookie de sesión. Descomentar login(request, user)."],
        ["10", "Quita 'apps.grades' de apps", "config/settings.py", "LookupError: No installed app", "Desconecta la app del ecosistema Django. Agregar a INSTALLED_APPS."],
        ["11", "Quita AuthenticationMiddleware", "config/settings.py", "AttributeError: no attribute 'user'", "No inyecta el usuario en request. Restaurar en MIDDLEWARE."],
        ["12", "Quita división / 100", "apps/grades/services.py", "DataError: overflow (350.0)", "No normaliza a 1.0. Restaurar división entre Decimal('100.00')."],
        ["13", "Borra @property en is_teacher", "apps/accounts/models.py", "Alumnos ven menús de profesor", "Evalúa la función como True. Devolver decorador @property."],
        ["14", "DEBUG=False y ALLOWED_HOSTS=[]", "config/settings.py", "Bad Request (400)", "Modo producción sin hosts autorizados. Agregar '*' o 'localhost'."],
        ["15", "Borra .env o SECRET_KEY", "Raíz / .env", "ImproperlyConfigured", "Faltan variables secretas. Copiar .env.example a .env."],
        ["16", "CASCADE en escuela-usuario", "apps/accounts/models.py", "Borrar escuela borra alumnos", "Borrado destructivo. Cambiar a on_delete=models.SET_NULL."],
        ["17", "Quita validación financiera", "apps/reports/views.py", "Boletines sin paz y salvo", "Desactiva control de morosos. Restaurar decorador institucional."],
        ["18", "Cambia nombre de block content", "templates/base.html", "Pantalla vacía / blanca", "Rompe herencia MVT. Sincronizar nombre {% block content %}."],
        ["19", "Borra log_audit al calificar", "apps/grades/views.py", "Sin rastro de cambios", "Vulnera trazabilidad IEEE 730 y Ley 1581. Invocación obligatoria."],
        ["20", "Quita unique en cédula", "apps/accounts/models.py", "Cédulas duplicadas en BD", "Permite colisión de identidades. Restaurar unique=True."]
    ]
    build_table(doc, headers_top20, data_top20, [0.3, 1.4, 1.3, 1.4, 2.1], header_color="0F4C81")
    
    # SECCIÓN 9: COMANDOS DE CONSOLA
    add_styled_heading(doc, "9. Comandos de Rescate en Consola de Django", level=1)
    headers_cmd = ["Problema Provocado", "Comando de Consola", "Explicación Técnica"]
    data_cmd = [
        ["Tablas de BD no sincronizadas", "python manage.py migrate", "Aplica migraciones pendientes en db.sqlite3."],
        ["Modelos modificados sin migración", "python manage.py makemigrations", "Genera el archivo de migración en apps/*/migrations/."],
        ["Puerto 8000 ocupado o bloqueado", "python manage.py runserver 8080", "Levanta el servidor en el puerto alternativo 8080."],
        ["Faltan librerías que borró el profe", "pip install -r requirements.txt", "Reinstala todas las dependencias oficiales en lote."],
        ["Arrancar servidor para celulares", "python iniciar_servidor_red.py", "Detecta IP de la tarjeta de red y arranca en 0.0.0.0:8000."]
    ]
    build_table(doc, headers_cmd, data_cmd, [2.0, 2.2, 2.3], header_color="2E7D32")
    
    # SECCIÓN 10: ASIGNACIÓN DE INTEGRANTES
    add_styled_heading(doc, "10. Especialidades Asignadas a las 3 Integrantes", level=1)
    add_body_p(doc, "Defiende: Plantillas base.html, login.html, tokens CSRF, atributos semánticos ARIA de la Res. 1519 de MinTIC, estilos Bootstrap y prevención de pantallas en blanco.", bold_prefix="👩‍💻 Integrante 1 (Frontend, Formularios y Accesibilidad): ")
    add_body_p(doc, "Defiende: Fórmulas de cálculo de RAPs al 100.00% con Decimal, modelos de notas, bloqueo de periodos lectivos (is_editable) y unicidad en base de datos.", bold_prefix="👩‍💻 Integrante 2 (Lógica de Negocio, RAPs y Modelos Relacionales): ")
    add_body_p(doc, "Defiende: Carga masiva con savepoints atómicos (transaction.atomic), lectura de Excel con openpyxl, verificación pública del QR criptográfico y configuración en settings.py.", bold_prefix="👩‍💻 Integrante 3 (Arquitectura, Carga Masiva y Seguridad): ")
    
    doc.save(output_path)
    print(f"[OK] Guia de defensa DOCX generada en: {output_path}")

if __name__ == "__main__":
    out_f = r"C:\Academix\docs\GUIA_EXACTA_CODIGO_ACADEMIX_DEFENSA_Y_SABOTAJE.docx"
    generate_guia_docx(out_f)

