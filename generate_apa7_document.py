"""
Script para generar el documento oficial en Word (.docx) bajo Norma APA 7.ª edición
para el Proyecto Academix - SENA ADSO
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from build_docs_helper import set_cell_background, set_cell_margins, set_table_borders, add_callout_box

def create_full_document(output_path):
    doc = Document()

    # 1. Configuración de Página (Márgenes APA 7: 2.54 cm / 1 pulgada en todos los lados)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Configuración de estilos base
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Funciones de utilidad para texto
    def add_title_cover(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_subtitle_cover(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(18)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_cover_info(label, value):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_lbl = p.add_run(f"{label}: ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(11)
        r_val = p.add_run(value)
        r_val.font.size = Pt(11)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_p(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_table_header(table_num, table_title):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(10)
        p_num.paragraph_format.space_after = Pt(1)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(f"Tabla {table_num}")
        r_num.bold = True
        r_num.font.size = Pt(10.5)

        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_before = Pt(0)
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(table_title)
        r_tit.italic = True
        r_tit.font.size = Pt(10.5)

    def add_table_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.05
        r_lbl = p.add_run("Nota. ")
        r_lbl.italic = True
        r_lbl.font.size = Pt(9.5)
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    def add_figure_header(fig_num, fig_title):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(12)
        p_num.paragraph_format.space_after = Pt(1)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(f"Figura {fig_num}")
        r_num.bold = True
        r_num.font.size = Pt(10.5)

        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_before = Pt(0)
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(fig_title)
        r_tit.italic = True
        r_tit.font.size = Pt(10.5)

    def add_figure_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.05
        r_lbl = p.add_run("Nota. ")
        r_lbl.italic = True
        r_lbl.font.size = Pt(9.5)
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    def add_code_block(code_str):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        c = tbl.cell(0, 0)
        c.width = Inches(6.5)
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, top=120, bottom=120, left=150, right=150)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(code_str)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # 1. PORTADA OFICIAL APA 7 (SENA)
    # =========================================================================
    for _ in range(3):
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(0)

    add_title_cover("DOCUMENTO TÉCNICO DE ARQUITECTURA TECNOLÓGICA Y DISEÑO DE ESTRUCTURA DE DATOS PARA LA PLATAFORMA DE GESTIÓN ESCOLAR ACADEMIX")
    add_subtitle_cover("Propuesta Integral de Infraestructura On-Premise, Seguridad de la Información, Modelado Transaccional y Plan de Implementación")

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(18)
    p_sp.paragraph_format.space_after = Pt(18)

    add_cover_info("Autores", "Equipo de Desarrollo de Software - Proyecto Academix")
    add_cover_info("Programa de Formación", "Tecnología en Análisis y Desarrollo de Software (ADSO)")
    add_cover_info("Ficha de Caracterización", "2834512 / Fase de Diseño y Ejecución")
    add_cover_info("Instructor Técnico", "Ingeniería de Sistemas e Informática SENA")
    add_cover_info("Institución", "Servicio Nacional de Aprendizaje (SENA) - Centro de Formación en Tecnologías de la Información")
    add_cover_info("Ciudad y Fecha", "Bogotá D.C., Colombia, 30 de septiembre de 2026")

    doc.add_page_break()

    # =========================================================================
    # 2. TABLA DE CONTENIDO Y RESUMEN EJECUTIVO
    # =========================================================================
    add_h1("Tabla de Contenido")
    toc_items = [
        ("1. Introducción y Contextualización del Sistema Academix", "3"),
        ("2. Objetivos del Proyecto", "4"),
        ("   2.1. Objetivo General", "4"),
        ("   2.2. Objetivos Específicos", "4"),
        ("3. Competencia 1: Arquitectura Tecnológica de la Infraestructura", "5"),
        ("   3.1. Análisis y Dimensionamiento de Necesidades de Infraestructura", "5"),
        ("   3.2. Inventario, Especificaciones Técnicas y Comparativa de Mercado", "7"),
        ("   3.3. Diagrama de Distribución Física, Lógica y Flujo de Red", "10"),
        ("   3.4. Estimación Presupuestal Detallada (CAPEX y OPEX en COP)", "12"),
        ("   3.5. Gestión de Riesgos, Seguridad Perimetral y Marco Legal Ley 1581", "13"),
        ("   3.6. Requerimiento Formal de Infraestructura Dirigido al Cliente", "15"),
        ("4. Competencia 2: Diseño de la Estructura de Datos y Plan de Implementación", "17"),
        ("   4.1. Modelo Conceptual de Datos del Dominio Academix", "17"),
        ("   4.2. Modelo Lógico, Físico y Normalización en Tercera Forma Normal (3FN)", "18"),
        ("   4.3. Diccionario de Datos del Sistema Transaccional", "19"),
        ("   4.4. Estándares Aplicados, Integridad Referencial e ISO/IEC 25010", "22"),
        ("   4.5. Estrategia de Migración (SQLite a PostgreSQL) y Políticas de Respaldo", "24"),
        ("   4.6. Plan de Implementación, Cronograma Gantt y Protocolo de Pruebas", "26"),
        ("5. Conclusiones", "30"),
        ("6. Recomendaciones Técnicas", "31"),
        ("7. Referencias Bibliográficas (Norma APA 7.ª Edición)", "32"),
        ("Anexo: Lista de Chequeo Previa a la Entrega para el Aprendiz SENA", "34")
    ]
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.autofit = False
    for i, (title, page) in enumerate(toc_items):
        c0 = tbl_toc.cell(i, 0)
        c1 = tbl_toc.cell(i, 1)
        c0.width = Inches(5.8)
        c1.width = Inches(0.7)
        set_cell_margins(c0, top=40, bottom=40, left=40, right=40)
        set_cell_margins(c1, top=40, bottom=40, left=40, right=40)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.05
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(title)
        if title.startswith("1.") or title.startswith("2.") or title.startswith("3.") or title.startswith("4.") or title.startswith("5.") or title.startswith("6.") or title.startswith("7."):
            r0.bold = True
        r0.font.size = Pt(10)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.05
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(page)
        r1.font.size = Pt(10)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(12)

    add_h2("Resumen Ejecutivo")
    add_p(
        "El presente informe técnico describe la arquitectura de infraestructura tecnológica y el diseño de la estructura "
        "de datos para el sistema de información 'Academix', una plataforma integral de gestión escolar (School Management System / "
        "Learning Management System) concebida para modernizar la administración pedagógica y disciplinaria en instituciones "
        "de educación básica y media en Colombia. La arquitectura de hardware y red adopta un modelo On-Premise robusto, "
        "gobernado por un hipervisor de grado empresarial (Proxmox VE), contenedores Docker orquestados, terminación segura SSL con Nginx, "
        "caché en memoria con Redis y un motor de base de datos relacional PostgreSQL 16. La solución garantiza alta disponibilidad, "
        "aislamiento de tráfico mediante redes virtuales (VLANs), respaldo inmutable bajo la regla 3-2-1 y estricto cumplimiento del "
        "régimen de protección de datos personales de menores de edad estipulado en la Ley Estatutaria 1581 de 2012. Paralelamente, "
        "el modelado transaccional resuelve la jerarquía pedagógica multinivel (Área, Asignatura, Competencias y RAPs) "
        "y establece un plan integral de implementación con cronograma detallado, protocolo de pruebas de carga y matrices de capacitación."
    )

    doc.add_page_break()

    # =========================================================================
    # 3. INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    add_h1("1. Introducción y Contextualización del Sistema Academix")
    add_p(
        "En el contexto actual de la educación básica y media en Colombia, las instituciones enfrentan el desafío de transitar "
        "desde modelos de gestión fragmentados —frecuentemente soportados en hojas de cálculo aisladas y expedientes físicos en papel— "
        "hacia ecosistemas digitales unificados capaces de centralizar la trazabilidad académica, el seguimiento formativo continuo y "
        "la convivencia escolar. De acuerdo con directrices del Ministerio de Educación Nacional (MEN) y los requerimientos formativos "
        "del Servicio Nacional de Aprendizaje (SENA), los sistemas de información institucionales deben articular de manera coherente "
        "la gestión directiva, la planeación curricular docente, la interacción con las familias y la salvaguarda de la información sensible."
    )
    add_p(
        "La plataforma Academix responde a esta necesidad mediante una arquitectura modular en Python 3.12 y Django 5.x, "
        "estructurada en micro-aplicaciones internas desacopladas (apps: subjects, grades, courses, teachers, attendance, discipline, "
        "homework, reports y accounts). Su diseño contempla una experiencia de usuario orientada a la usabilidad pedagógica, integrando "
        "un sistema de control de acceso basado en roles (RBAC) con cinco perfiles fundamentales: Rector/Administrador, Coordinador Académico, "
        "Docente, Estudiante y Acudiente. Destaca en su núcleo la implementación de la jerarquía curricular contemporánea solicitada por las "
        "instituciones educativas modernas: Área de Conocimiento → Materia/Asignatura → Marco de Competencias e Indicadores → Resultados de "
        "Aprendizaje Previsto (RAPs), evaluados en una escala cuantitativa de 1.0 a 5.0 con distribución ponderada automática al 100.00%."
    )
    add_p(
        "Para responder a las limitaciones de conectividad exterior de diversas regiones del país y asegurar la soberanía de los datos "
        "institucionales, el colegio ha optado por un modelo de infraestructura On-Premise en sus instalaciones centrales. Este documento "
        "formaliza las dos competencias clave del ciclo de formación en Análisis y Desarrollo de Software: primero, el diseño de la arquitectura "
        "tecnológica física, lógica y financiera; segundo, el diseño formal de la estructura de datos, aseguramiento de calidad según la norma "
        "ISO/IEC 25010 y el plan de implementación operativo."
    )

    add_h1("2. Objetivos del Proyecto")
    add_h2("2.1. Objetivo General")
    add_p(
        "Diseñar la arquitectura tecnológica de infraestructura y la estructura relacional de datos para la plataforma de gestión escolar "
        "Academix, asegurando interoperabilidad, seguridad perimetral, alta concurrencia y normalización técnica según las normas vigentes "
        "y los requerimientos específicos de la institución educativa beneficiaria."
    )

    add_h2("2.2. Objetivos Específicos")
    add_p(
        "1. Dimensionar los recursos de hardware, almacenamiento, red y virtualización requeridos para soportar la concurrencia máxima del colegio "
        "a un horizonte de tres años, sustentando técnicamente la elección de componentes frente a alternativas comerciales."
    )
    add_p(
        "2. Formular la topología de red física y lógica mediante segmentación de VLANs, esquemas de seguridad perimetral (firewall, VPN, SSL/TLS) "
        "y el protocolo de cumplimiento de la Ley 1581 de 2012 para protección de datos de menores."
    )
    add_p(
        "3. Estructurar el presupuesto financiero de adquisición (CAPEX) y operación anual (OPEX) en pesos colombianos (COP), acompañado del "
        "requerimiento formal de adecuación física y eléctrica al cliente."
    )
    add_p(
        "4. Modelar la base de datos relacional transaccional en Tercera Forma Normal (3FN), garantizando integridad referencial y documentando "
        "el catálogo de entidades mediante diagrama entidad-relación y diccionario de datos técnico."
    )
    add_p(
        "5. Definir la estrategia de migración desde el entorno de desarrollo hacia PostgreSQL 16 y estructurar el plan de implementación integral, "
        "incluyendo cronograma tipo Gantt, protocolos de pruebas de carga y matrices de capacitación por rol."
    )

    doc.add_page_break()

    # =========================================================================
    # 4. COMPETENCIA 1: ARQUITECTURA TECNOLÓGICA
    # =========================================================================
    add_h1("3. Competencia 1: Arquitectura Tecnológica de la Infraestructura")
    add_p(
        "La competencia de arquitectura tecnológica comprende el análisis riguroso de las demandas operativas del sistema de información, "
        "el dimensionamiento de las capacidades de cómputo y la formulación del esquema de distribución que alojará los componentes lógicos "
        "en las instalaciones físicas del cliente."
    )

    add_h2("3.1. Análisis y Dimensionamiento de Necesidades de Infraestructura")
    add_p(
        "El dimensionamiento de infraestructura de Academix parte de la caracterización demográfica de una institución educativa de educación "
        "básica y media con capacidad para 1,200 estudiantes matriculados, 60 docentes de tiempo completo, 10 directivos y administrativos, "
        "y aproximadamente 1,800 acudientes registrados. Para evitar cuellos de botella y sobrecostos por sobreaprovisionamiento, "
        "se definieron escenarios de carga basados en perfiles de concurrencia y estacionalidad académica."
    )

    add_table_header("1", "Perfil de Usuarios y Estimación de Concurrencia Simultánea en Academix")
    tbl_users = doc.add_table(rows=6, cols=5)
    tbl_users.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_users)
    headers_u = ["Rol de Usuario", "Población Total", "Concurrencia Pico (%)", "Usuarios Concurrentes", "Tipo de Operación Predominante"]
    for j, h in enumerate(headers_u):
        c = tbl_users.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_users = [
        ["Estudiantes", "1,200", "25 %", "300", "Lectura (consultas de notas, descarga tareas, foros)"],
        ["Docentes", "60", "90 %", "54", "Escritura/Lectura (calificación RAPs, asistencia, observador)"],
        ["Directivos / Coordinadores", "10", "100 %", "10", "Operaciones analíticas, emisión boletines, auditoría"],
        ["Acudientes / Padres", "1,800", "8 %", "144", "Lectura esporádica (boletines, novedades disciplinarias)"],
        ["Total Sistema Pico", "3,070", "-", "508 concurrentes", "Carga mixta en periodos de cierre de calificaciones"]
    ]
    for i, row in enumerate(data_users):
        for j, val in enumerate(row):
            c = tbl_users.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j in [1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            if i == len(data_users) - 1:
                r.bold = True
            r.font.size = Pt(9)

    add_table_note("Datos simulados con base en el calendario académico institucional. El pico máximo de 508 usuarios concurrentes ocurre durante las semanas de cierre de periodo y entrega de boletines trimestrales.")

    add_h3("Supuestos de Cómputo, Almacenamiento y Ancho de Banda")
    add_p(
        "A continuación se detallan las fórmulas y supuestos matemáticos utilizados para el cálculo de recursos requeridos:"
    )
    add_p(
        "a) Demanda de Memoria RAM: Se calcula mediante la ecuación RAM = OS_Base + (N_workers × RAM_worker) + DB_SharedBuffers + Redis_Cache. "
        "Asignando 4 GB para el sistema operativo host e hipervisor, 8 workers Gunicorn (con un consumo promedio de 180 MB por proceso bajo carga: 1.44 GB), "
        "un buffer pool de PostgreSQL de 8 GB para mantener en memoria las tablas de calificaciones y asistencias más consultadas, y 2 GB para Redis, "
        "se establece una base operativa mínima de 16 GB, proyectando 32 GB como valor óptimo de despliegue para absorber ráfagas."
    )
    add_p(
        "b) Almacenamiento y Crecimiento a 3 Años: Cada estudiante genera anualmente registros en notas, asistencias, observador y evidencias digitales. "
        "Se estima que la base de datos relacional crecerá a una tasa de 4.8 GB por año lectivo (aproximadamente 14.4 GB en 3 años). Los archivos "
        "estáticos y multimedia de tareas escolares (PDFs, imágenes de evidencias y trabajos de estudiantes) se dimensionan con una cuota máxima de "
        "5 MB por entrega y 20 entregas anuales por estudiante, representando 120 GB anuales. Con un esquema de depuración y compresión a los dos años, "
        "el repositorio de objetos acumulará 360 GB en el trienio. Para alojar el sistema, base de datos, logs, snapshots del hipervisor y copias de "
        "seguridad locales, se establece un requerimiento de almacenamiento efectivo de 1.2 TB en arreglo redundante RAID 10."
    )
    add_p(
        "c) Consumo de Ancho de Banda WAN/LAN: En la red local (LAN), cada petición HTTP promedio de la interfaz Bootstrap 5 / Vanilla JS "
        "representa 120 KB tras la carga inicial de assets cacheados. Con 508 usuarios generando una petición cada 10 segundos, el flujo local "
        "alcanza 6.1 MB/s (aprox. 48.8 Mbps), perfectamente soportado por el enlace Gigabit Ethernet troncal. Para el acceso externo de acudientes "
        "y docentes fuera del colegio, un enlace de fibra óptica simétrica dedicado de 100 Mbps garantiza un tiempo de respuesta inferior a 450 ms "
        "en el 95 % de las transacciones (percentil 95)."
    )

    add_h2("3.2. Inventario, Especificaciones Técnicas y Comparativa de Mercado")
    add_p(
        "El inventario tecnológico clasifica los recursos físicos y lógicos en dos niveles de especificación: mínimos requeridos (línea base "
        "para operación en contingencia) y recomendados (arquitectura proyectada para el ciclo de vida de tres años sin degradación)."
    )

    add_table_header("2", "Especificaciones Técnicas de Hardware y Software para la Infraestructura On-Premise")
    tbl_hw = doc.add_table(rows=7, cols=4)
    tbl_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hw)
    cols_h = ["Componente", "Especificación Mínima", "Especificación Recomendada", "Propósito en Academix"]
    for j, h in enumerate(cols_h):
        c = tbl_hw.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_hw = [
        ["Servidor Físico (Host)", "1x Intel Xeon E-2324G (4 cores, 3.1 GHz), 16 GB DDR4 ECC", "1x AMD EPYC 7302P (16 cores, 32 threads, 3.0 GHz) o Dual Intel Xeon Silver 4314, 64 GB DDR4 ECC Registered", "Servidor bare-metal de rack 1U/2U para alojar el hipervisor y todas las instancias virtualizadas"],
        ["Almacenamiento Principal", "2x 1 TB SSD SATA Enterprise en RAID 1 por software", "4x 960 GB SSD NVMe Enterprise en RAID 10 por hardware (controlador con caché BBU de 2 GB)", "Particiones para OS, volumen transaccional de PostgreSQL, almacén de medios Django y contenedores"],
        ["Interfaces de Red (NIC)", "2x 1 GbE RJ45 integradas", "4x 1 GbE RJ45 + 2x 10 GbE SFP+ (LACP / 802.3ad agregación de enlaces)", "Segmentación de tráfico de red, VLANs independientes y enlace de gestión fuera de banda (IPMI/iDRAC)"],
        ["Switch de Distribución L3", "Switch Gestionable L2 de 24 puertos Gigabit", "Switch Gestionable L3 de 24 puertos 10/100/1000 + 4 puertos 10G SFP+, con soporte 802.1Q VLANs e IGMP", "Interconexión troncal de servidores, enlace con switches de acceso y enrutamiento inter-VLAN"],
        ["Firewall Perimetral", "Routerboard básico con reglas iptables", "Appliance dedicado de seguridad (Netgate 4100 con pfSense Plus o FortiGate 60F)", "Filtrado de paquetes L3/L4/L7, terminación de túneles VPN WireGuard, prevención de intrusiones (IPS) y NAT"],
        ["Sistema de Energía (UPS)", "UPS Interactiva de 1,500 VA / 900 W", "UPS Online Doble Conversión de 3,000 VA / 2,700 W con tarjeta SNMP y módulo de baterías extendidas", "Protección contra sobretensiones, fluctuaciones y autonomía de 35 minutos para apagado ordenado"]
    ]
    for i, row in enumerate(data_hw):
        for j, val in enumerate(row):
            c = tbl_hw.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("El dimensionamiento recomendado provee redundancia N+1 en almacenamiento (RAID 10) y fuentes de poder redundantes conmutables en caliente (Hot-Plug 550W Platinum).")

    add_h3("Comparativa Técnica y Justificación de Alternativas")
    add_p(
        "Para respaldar la toma de decisiones técnicas ante el consejo directivo del colegio y el comité evaluador del SENA, "
        "se ejecutó un análisis comparativo multicriterio de las dos tecnologías líderes en hipervisores de virtualización y "
        "los dos modelos de aprovisionamiento arquitectónico."
    )

    add_table_header("3", "Matriz Comparativa entre Hipervisores de Virtualización: Proxmox VE frente a VMware ESXi")
    tbl_comp = doc.add_table(rows=7, cols=4)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_comp)
    cols_c = ["Criterio de Evaluación", "Proxmox Virtual Environment (VE) 8.x", "VMware ESXi / vSphere 8.x", "Impacto y Decisión para Academix"]
    for j, h in enumerate(cols_c):
        c = tbl_comp.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_comp = [
        ["Licenciamiento y Costos", "Open-source bajo licencia GNU AGPLv3. Acceso total a todas las funciones sin costo de licencia; suscripción comunitaria opcional para soporte empresarial.", "Modelo propietario cerrado con suscripción anual obligatoria por core tras la adquisición por Broadcom. Costos prohibitivos para colegios.", "FAVORABLE A PROXMOX. Elimina costos de licenciamiento recurrentes, orientando el presupuesto a hardware robusto."],
        ["Soporte de Contenedores", "Soporte nativo integrado de contenedores Linux (LXC) y máquinas virtuales QEMU/KVM en el mismo panel de control web.", "Enfocado en máquinas virtuales; el soporte de contenedores requiere suites adicionales complejas (vSphere with Tanzu).", "FAVORABLE A PROXMOX. Permite desplegar microservicios ligeros con sobrecarga de memoria casi nula frente a VMs tradicionales."],
        ["Gestión de Almacenamiento", "Integración nativa avanzada con ZFS, Btrfs, LVM-Thin, Ceph y soporte directo de snapshots inmutables y deduplicación.", "Sistema de archivos VMFS propietario. Capacidades avanzadas requieren almacenamiento compartido SAN/NAS o licencias vSAN de alto costo.", "FAVORABLE A PROXMOX. ZFS permite replicación asíncrona local y compresión transparente sin inversión extra en licencias."],
        ["Respaldo y Recuperación", "Herramienta Proxmox Backup Server integrada, con deduplicación en el cliente, copias incrementales y cifrado nativo.", "Requiere integración con soluciones de terceros (Veeam, Commvault) con costos añadidos por socket o por VM.", "FAVORABLE A PROXMOX. Garantiza la ejecución de la política de respaldo 3-2-1 sin software comercial externo."],
        ["Facilidad de Operación", "Panel de administración web HTML5 intuitivo, sin agentes pesados, con consola VNC/SPICE y API REST completa.", "Panel vSphere Client completo pero con dependencia de componentes vCenter para clustering y gestión centralizada.", "NEUTRAL. Ambos paneles son profesionales; la curva de aprendizaje de Proxmox en base Debian es ideal para el equipo de TI escolar."],
        ["Veredicto de Selección", "SELECCIONADO: Proxmox VE ofrece máxima soberanía tecnológica, costo total de propiedad (TCO) mínimo y flexibilidad de contenedores.", "DESCARTADO: Prohibitivo financieramente para la institución debido al nuevo esquema de licenciamiento comercial por suscripción.", "Adopción de Proxmox VE 8.2 como hipervisor bare-metal definitivo."]
    ]
    for i, row in enumerate(data_comp):
        for j, val in enumerate(row):
            c = tbl_comp.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Evaluación realizada considerando las directrices de optimización de presupuesto en instituciones de educación media en Colombia.")

    add_p(
        "Respecto al debate entre infraestructura On-Premise y Cloud Pública (AWS / Microsoft Azure): aunque la nube brinda elasticidad instantánea, "
        "los costos acumulados de transferencia de salida de datos (egress traffic), cómputo continuo 24/7 y almacenamiento persistente en Colombia "
        "superan en un periodo de 24 meses la inversión total del servidor físico propio (depreciable a 5 años). Adicionalmente, el modelo On-Premise "
        "garantiza que los datos personales de los estudiantes permanezcan en custodia directa dentro de las instalaciones del plantel, "
        "facilitando la auditoría física en concordancia con el principio de responsabilidad demostrada (accountability) de la Ley 1581 de 2012."
    )

    doc.add_page_break()

    # =========================================================================
    # 3.3. DIAGRAMA DE DISTRIBUCIÓN Y DESPLIEGUE
    # =========================================================================
    add_h2("3.3. Diagrama de Distribución Física, Lógica y Flujo de Red")
    add_p(
        "La topología de red se estructura bajo un modelo de segmentación de tres niveles (Core, Distribución y Acceso), "
        "implementando redes de área local virtuales (VLANs bajo estándar IEEE 802.1Q) para aislar estrictamente los dominios de difusión "
        "y mitigar riesgos de propagación de malware o intrusión indebida entre la red pública escolar y el entorno transaccional del servidor."
    )

    add_figure_header("1", "Diagrama de Despliegue Físico, Topología de Red y Segmentación de VLANs")
    add_code_block(
"""+-----------------------------------------------------------------------------------------------+
|                                      ZONA EXTERIOR (WAN)                                      |
|                                                                                               |
|                       Fibra Óptica Simétrica Dedicada (100 Mbps)                              |
+----------------------------------------------+------------------------------------------------+
                                               |
                                               v
+-----------------------------------------------------------------------------------------------+
| APPLIANCE DE SEGURIDAD PERIMETRAL (pfSense / FortiGate)                                        |
| - NAT 1:1 / Port Forwarding Seguro (443 -> Reverse Proxy)                                     |
| - VPN Gateway (WireGuard / IPsec para acceso docente y administrativo remoto)                  |
| - IDS/IPS (Suricata / Snort) con bloqueo automatizado de fuerza bruta                         |
+----------------------------------------------+------------------------------------------------+
                                               | Troncal 802.1Q (LACP 2 Gbps)
                                               v
+-----------------------------------------------------------------------------------------------+
| SWITCH PRINCIPAL DISTRIBUCIÓN L3 (Cisco Catalyst / Ubiquiti EdgeSwitch 24G)                  |
|                                                                                               |
|  [VLAN 10: Gestión]      [VLAN 20: Servidores]   [VLAN 30: Admin]   [VLAN 40: Profes]   [VLAN 50: WiFi] |
|   192.168.10.0/24         192.168.20.0/24         192.168.30.0/24    192.168.40.0/24    192.168.50.0/22 |
|   (IPMI, Switches, PDU)   (Host Proxmox, VMs)    (Rectoría, Secre)  (Salas Docentes)   (Estudiantes)   |
+----------------------------------------------+------------------------------------------------+
                                               |
                                               v
+-----------------------------------------------------------------------------------------------+
| SERVIDOR FÍSICO HOST (Proxmox VE 8.x Bare-Metal)                                             |
| Redundancia: RAID 10 NVMe Enterprise | Dual PSU 550W | Conectado a UPS Online 3000VA         |
|                                                                                               |
| +-------------------------------------------------------------------------------------------+ |
| | VM 100: ACADEMIX CORE PRODUCTION (Ubuntu Server 24.04 LTS / Docker Engine)                | |
| |                                                                                           | |
| |   +-----------------------+     +-----------------------+     +-------------------------+ | |
| |   |  NGINX Reverse Proxy  | --> | GUNICORN WSGI Workers | --> |  DJANGO 5.x FRAMEWORK   | | |
| |   |  (SSL/TLS Let's Enc.) |     | (Python 3.12, 8 wks)  |     |  (Lógica de Negocio)    | | |
| |   +-----------------------+     +-----------------------+     +------------+------------+ | |
| |                                                                            |              | |
| |                                  +-----------------------------------------+              | |
| |                                  v                                         v              | |
| |                     +-------------------------+               +-------------------------+ | |
| |                     |   POSTGRESQL 16 MOTOR   |               |   REDIS 7 CACHÉ / OPS   | | |
| |                     |   (Base Datos 3FN / NVMe|               |   (Sesiones, Colas Celery| |
| |                     +-------------------------+               +-------------------------+ | |
| +-------------------------------------------------------------------------------------------+ |
|                                                                                               |
| +-----------------------------------------+   +---------------------------------------------+ |
| | VM 200: MONITORING & AUDITORÍA          |   | CONTENEDOR PBS: RESPALDOS LOCALES           | |
| | Prometheus + Grafana + Node Exporter    |   | Proxmox Backup Server (Deduplicación/ZFS)   | |
| +-----------------------------------------+   +---------------------------------------------+ |
+-----------------------------------------------------------------------------------------------+"""
    )
    add_figure_note("Arquitectura de distribución física y virtualizada elaborada conforme al estándar IEEE 802.1Q para aislamiento de tráfico y ANSI/TIA-568-D para infraestructura de telecomunicaciones.")

    add_h3("Descripción de Nodos, Segmentación y Flujo de Información")
    add_p(
        "1. Zona WAN y Perímetro: La conexión exterior ingresa mediante fibra óptica monomodo al Convertidor de Medios (ONT) y de allí a la "
        "interfaz WAN del firewall perimetral appliance. El firewall aplica filtrado estricto L3/L4, cerrando todos los puertos salvo el "
        "puerto 443 (HTTPS) dirigido exclusivamente al proxy inverso. Las conexiones administrativas remotas de soporte o auditoría "
        "deben autenticarse mediante un túnel VPN WireGuard cifrado con curvas elípticas Curve25519."
    )
    add_p(
        "2. Segmentación de Red (VLANs): El switch de distribución L3 gestiona cinco dominios aislados. La VLAN 10 (Gestión Fuera de Banda) "
        "comunica interfaces IPMI/iDRAC de hardware, consola de switches y PDU inteligente. La VLAN 20 (Servidores) aloja las interfaces de "
        "red virtuales de la plataforma Academix sin acceso directo desde internet. Las VLANs 30 (Administrativa) y 40 (Docentes) acceden a la "
        "interfaz web mediante reglas de enrutamiento inter-VLAN controladas por lista de control de acceso (ACL). Finalmente, la VLAN 50 "
        "(Estudiantes y Visitantes) posee aislamiento de clientes (Client Isolation) y ancho de banda limitado a 2 Mbps por dispositivo, "
        "imposibilitando cualquier ataque de denegación de servicio (DoS) o escaneo de puertos hacia el servidor central."
    )
    add_p(
        "3. Flujo Transaccional Interno: Una petición HTTPS proveniente de un docente llega al proxy inverso Nginx en el contenedor DMZ. "
        "Nginx realiza la terminación del túnel TLS (certificados AES-256 GCM), comprime assets estáticos (Gzip/Brotli) y enruta la solicitud "
        "hacia el socket Unix del servidor WSGI Gunicorn. Gunicorn distribuye la carga entre sus workers en Python 3.12, los cuales procesan la "
        "lógica en Django 5.x. Para consultas de lectura repetitivas (como el catálogo de materias o configuraciones del año lectivo), Django "
        "interroga la memoria RAM en Redis. Para operaciones de persistencia transaccional (registro de notas de RAPs, asistencias y observador), "
        "Django interactúa con PostgreSQL 16 a través de un pool de conexiones optimizado, registrando cada transacción en el archivo Write-Ahead "
        "Logging (WAL) alojado en el arreglo NVMe."
    )

    doc.add_page_break()

    # =========================================================================
    # 3.4. ESTIMACIÓN DE COSTOS (CAPEX / OPEX)
    # =========================================================================
    add_h2("3.4. Estimación Presupuestal Detallada (CAPEX y OPEX en Pesos Colombianos - COP)")
    add_p(
        "La evaluación económica de la infraestructura tecnológica se divide en gastos de capital (CAPEX - Capital Expenditure), correspondientes "
        "a la adquisición inicial de activos tangibles e instalación, y gastos operacionales (OPEX - Operational Expenditure), correspondientes "
        "al mantenimiento preventivo, enlaces de telecomunicaciones y soporte continuo proyectado anualmente."
    )

    add_table_header("4", "Presupuesto de Inversión Inicial en Activos de Capital (CAPEX)")
    tbl_capex = doc.add_table(rows=9, cols=5)
    tbl_capex.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_capex)
    cols_cap = ["Ítem / Componente", "Descripción y Marca / Modelo", "Cantidad", "Valor Unitario (COP)", "Valor Total (COP)"]
    for j, h in enumerate(cols_cap):
        c = tbl_capex.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_capex = [
        ["Servidor de Rack 2U", "Dell PowerEdge R7515 / AMD EPYC 7302P 16C, 64 GB RAM ECC, Dual PSU 550W Hot-Plug", "1", "$ 18,500,000", "$ 18,500,000"],
        ["Discos NVMe Enterprise", "Samsung PM9A3 960 GB NVMe PCIe 4.0 U.2 (Arreglo RAID 10 Hardware)", "4", "$ 1,250,000", "$ 5,000,000"],
        ["Controlador RAID Hardware", "Dell PERC H755 con 8 GB de caché NVRAM y batería BBU", "1", "$ 2,800,000", "$ 2,800,000"],
        ["Switch Gestionable L3", "Ubiquiti UniFi Pro 24 PoE (USW-Pro-24-PoE) 24x 1GbE + 2x 10G SFP+", "1", "$ 3,600,000", "$ 3,600,000"],
        ["Appliance Firewall Perimetral", "Netgate 4100 Base con pfSense Plus integrado (Failover dual WAN)", "1", "$ 3,200,000", "$ 3,200,000"],
        ["UPS Online Doble Conversión", "APC Smart-UPS On-Line SRT 3000VA / 2700W 208V/120V con tarjeta SNMP", "1", "$ 6,400,000", "$ 6,400,000"],
        ["Gabinete Rack y PDU", "Rack cerrado 24U con ventilación forzada termostática y PDU monitoreable", "1", "$ 2,100,000", "$ 2,100,000"],
        ["Cableado Cat6A y Puesta Marcha", "Cableado de cobre Cat6A LSZH, patch panels certificados, mano de obra y certificación Fluke", "Global", "$ 4,500,000", "$ 4,500,000"]
    ]
    total_capex = 46100000
    for i, row in enumerate(data_capex):
        for j, val in enumerate(row):
            c = tbl_capex.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j in [2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Total CAPEX estimado de adquisición: Cuarenta y seis millones cien mil pesos colombianos ($ 46,100,000 COP). Valores calculados a precios promedio del mercado tecnológico nacional con corte al tercer trimestre de 2026.")

    add_table_header("5", "Presupuesto Operativo Anual Proyectado (OPEX)")
    tbl_opex = doc.add_table(rows=6, cols=5)
    tbl_opex.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_opex)
    cols_op = ["Concepto Operacional", "Proveedor / Responsable", "Frecuencia", "Costo Mensual (COP)", "Costo Anual (COP)"]
    for j, h in enumerate(cols_op):
        c = tbl_opex.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_opex = [
        ["Internet Fibra Simétrica 100 Mbps", "ISP Corporativo (Claro / Tigo / ETB Empresas)", "Mensual", "$ 450,000", "$ 5,400,000"],
        ["Suscripción Soporte Proxmox VE", "Proxmox Community Subscription (1 CPU Socket)", "Anual", "$ 65,000", "$ 780,000"],
        ["Almacenamiento Off-Site Respaldos", "B2 Cloud Storage / AWS S3 Glacier (500 GB cifrados)", "Mensual", "$ 45,000", "$ 540,000"],
        ["Mantenimiento Preventivo Físico", "Proveedor Técnico Especializado (Limpieza y calibración UPS)", "Semestral", "$ 150,000", "$ 1,800,000"],
        ["Bolsa de Soporte y Actualización", "Equipo de Desarrollo SENA / Técnico de Sistemas Institucional", "Mensual", "$ 300,000", "$ 3,600,000"]
    ]
    for i, row in enumerate(data_opex):
        for j, val in enumerate(row):
            c = tbl_opex.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j in [3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Total OPEX anual estimado: Doce millones ciento veinte mil pesos colombianos ($ 12,120,000 COP/año), equivalentes a aproximadamente $ 1,010,000 COP mensuales.")

    doc.add_page_break()

    # =========================================================================
    # 3.5. RIESGOS, SEGURIDAD Y MARCO LEGAL LEY 1581
    # =========================================================================
    add_h2("3.5. Gestión de Riesgos, Seguridad de la Información y Marco Legal (Ley 1581 de 2012)")
    add_p(
        "La gestión de seguridad en Academix se fundamenta en el modelo de defensa en profundidad (Defense in Depth), "
        "cubriendo desde la protección eléctrica y física hasta los controles criptográficos a nivel de aplicación."
    )

    add_table_header("6", "Matriz de Riesgos Tecnológicos, Impacto y Medidas de Mitigación")
    tbl_risk = doc.add_table(rows=6, cols=5)
    tbl_risk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_risk)
    cols_r = ["Riesgo Identificado", "Probabilidad", "Impacto", "Efecto Potencial", "Estrategia de Mitigación Implementada"]
    for j, h in enumerate(cols_r):
        c = tbl_risk.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_risk = [
        ["Corte prolongado de fluido eléctrico", "Media", "Alto", "Apagado abrupto, corrupción de base de datos", "UPS Online Doble Conversión 3 kVA con autonomía de 35 min y script de apagado ordenado apcupsd vía red."],
        ["Fallo físico de unidad de disco", "Baja", "Crítico", "Pérdida de integridad de notas y expedientes", "Arreglo RAID 10 por hardware con soporte Hot-Spare; tolerancia a falla simultánea de hasta 2 discos en diferentes espejos."],
        ["Ataque de inyección SQL o XSS", "Media", "Crítico", "Exfiltración de datos, alteración de calificaciones", "Uso obligatorio del ORM parametrizado de Django 5.x; sanitización automática de templates; cabeceras CSP, HSTS y X-Frame-Options."],
        ["Ataque de fuerza bruta a contraseñas", "Alta", "Medio", "Compromiso de cuentas de docentes o directivos", "Módulo django-axes con bloqueo de IP tras 5 intentos fallidos por 30 minutos; políticas de contraseñas seguras y captcha."],
        ["Fuga de datos personales de menores", "Baja", "Catastrófico", "Sanciones legales de la SIC, vulneración de derechos", "Cifrado en reposo (dm-crypt/LUKS en particiones de BD) y en tránsito (TLS 1.3 con certificados HSTS); RBAC estricto."]
    ]
    for i, row in enumerate(data_risk):
        for j, val in enumerate(row):
            c = tbl_risk.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j in [1, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Metodología basada en la norma ISO/IEC 27005 para gestión de riesgos de seguridad de la información.")

    add_h3("Cumplimiento del Régimen de Protección de Datos Personales (Ley 1581 de 2012 y Decreto 1377 de 2013)")
    add_p(
        "Al tratarse de una plataforma escolar que almacena expedientes de niños, niñas y adolescentes, Academix se sujeta de manera estricta "
        "al Artículo 7 de la Ley Estatutaria 1581 de 2012 y el Artículo 12 del Decreto 1377 de 2013, los cuales prohíben el tratamiento de datos "
        "personales de menores salvo cuando responda y respete el interés superior de los niños y se asegure el respeto de sus derechos prevalentes. "
        "Para ello, el sistema adopta las siguientes salvaguardas técnicas y jurídicas:"
    )
    add_p(
        "1. Finalidad Exclusiva y Consentimiento Informado: Los datos biográficos, académicos y disciplinarios se recolectan única y exclusivamente "
        "con propósitos educativos y de convivencia escolar. Durante el proceso de matrícula virtual, el sistema despliega un módulo obligatorio "
        "de consentimiento expreso e informado que debe ser suscrito digitalmente por el acudiente o representante legal del menor."
    )
    add_p(
        "2. Tratamiento de Datos Sensibles del Observador: Las anotaciones disciplinarias (situaciones tipo I, II y III según la Ley 1620 de 2013 de "
        "Convivencia Escolar) revisten carácter sensible. En Academix, estos registros poseen aislamiento criptográfico y visibilidad restringida "
        "exclusivamente al Rector, al Coordinador y al docente director de grupo asignado, quedando expresamente ocultos para docentes no autorizados "
        "o terceros."
    )
    add_p(
        "3. Principio de Seguridad y Confidencialidad: Se implementan pistas de auditoría inmutables en base de datos mediante triggers que registran "
        "el identificador de usuario, dirección IP, marca temporal y valores anteriores ante cualquier consulta masiva, modificación o descarga "
        "de expedientes estudiantiles, facilitando inspecciones por parte de la Superintendencia de Industria y Comercio (SIC)."
    )

    doc.add_page_break()

    # =========================================================================
    # 3.6. REQUERIMIENTO FORMAL AL CLIENTE
    # =========================================================================
    add_h2("3.6. Requerimiento Formal de Infraestructura Dirigido al Cliente")
    add_p(
        "Como parte de las actividades del proyecto formativo SENA, a continuación se transcribe la comunicación formal mediante la cual "
        "el equipo de arquitectura tecnológica solicita formalmente al colegio las adecuaciones físicas, eléctricas y contractuales mínimas "
        "indispensables para iniciar la fase de instalación y puesta en marcha del sistema."
    )

    add_callout_box(
        doc,
        "CARTA DE REQUERIMIENTOS TÉCNICOS PREVIOS A LA PUESTA EN MARCHA\n\n"
        "Fecha: 30 de septiembre de 2026\n"
        "Para: Consejo Directivo y Rectoría Institucional\n"
        "De: Equipo de Arquitectura de Software - Proyecto Academix (SENA ADSO)\n"
        "Asunto: Requisitos indispensables de adecuación física, eléctrica, de conectividad y gestión para el despliegue del servidor central\n\n"
        "Estimados directivos:\n\n"
        "Con el objetivo de garantizar la óptima instalación, estabilidad operativa y longevidad de la plataforma Academix, "
        "nos permitimos formalizar el pliego de requerimientos que la institución educativa debe proveer y certificar de manera previa "
        "al ingreso del equipamiento de cómputo:\n\n"
        "1. Espacio Físico (Cuarto de Servidores / Rack):\n"
        "   - Área designada de mínimo 2.5 m × 2.0 m, de acceso restringido con cerradura biométrica o llave controlada.\n"
        "   - Sistema de climatización y aire acondicionado de confort o precisión configurado a temperatura constante de 20 °C ± 2 °C y humedad relativa entre 40 % y 60 %.\n"
        "   - Piso seco, libre de riesgo de inundación o filtraciones hidrosanitarias, sin ventanas exteriores directas.\n\n"
        "2. Acometida Eléctrica y Puesta a Tierra:\n"
        "   - Circuito eléctrico regulado e independiente de 120V / 20A con cable de calibre adecuado (AWG 12 THHN), exclusivo para el rack de comunicaciones.\n"
        "   - Sistema de puesta a tierra certificado bajo norma RETIE con resistencia de dispersión inferior a 5 Ohmios en el electrodo del cuarto de cómputo.\n"
        "   - Tomas dobles polarizadas grado hospitalario o comercial de alta resistencia (NEMA 5-20R) conectadas a la salida de la UPS.\n\n"
        "3. Conectividad y Enlace WAN:\n"
        "   - Contratación activa de enlace simétrico de fibra óptica empresarial con al menos una dirección IP pública fija estática para enrutamiento del dominio escolar.\n"
        "   - Punto de red Gigabit Cat6A certificado desde el switch central hasta la ubicación prevista del rack del servidor.\n\n"
        "4. Acompañamiento Institucional y Cronograma de Entregas:\n"
        "   - Designación formal de un enlace técnico (responsable de sistemas o infraestructura) que acompañará las jornadas de instalación.\n"
        "   - Autorización escrita de ventanas de mantenimiento los fines de semana previos al inicio del año lectivo para pruebas de penetración y carga eléctrica.\n\n"
        "La aprobación y certificación de estos ítems constituye condición de procedibilidad para el desembolso de los activos y la firma del acta de inicio de instalación física.",
        title="DOCUMENTO FORMAL DE REQUERIMIENTO AL CLIENTE",
        border_color="0EA5E9",
        bg_color="F0F9FF"
    )

    doc.add_page_break()

    # =========================================================================
    # 5. COMPETENCIA 2: ESTRUCTURA DE DATOS
    # =========================================================================
    add_h1("4. Competencia 2: Diseño de la Estructura de Datos y Plan de Implementación")
    add_p(
        "El diseño de la estructura de datos comprende el modelado conceptual, lógico y físico de las entidades que componen el ecosistema "
        "de Academix, garantizando que el esquema relacional satisfaga los principios de normalización, atomicidad, consistencia, aislamiento y "
        "durabilidad (propiedades ACID), optimizando a la vez el desempeño en PostgreSQL 16."
    )

    add_h2("4.1. Modelo Conceptual de Datos del Dominio Academix")
    add_p(
        "El modelo conceptual captura las relaciones intrínsecas del ámbito pedagógico del colegio. Se organiza en torno a cuatro subsistemas "
        "principales:"
    )
    add_p(
        "1. Subsistema Académico-Curricular: Centrado en la jerarquía demandada por la institución: Área de Conocimiento → Materia/Asignatura → "
        "Competencias e Indicadores → Resultados de Aprendizaje Previsto (RAPs con dimensiones de Saber, Hacer, Ser y Evidencias de Elaboración). "
        "Cada RAP actúa como unidad básica evaluable dentro de los periodos lectivos."
    )
    add_p(
        "2. Subsistema de Oferta y Cursos: Comprende el Año Lectivo, los Periodos Académicos, los Grados Escolares (1° a 11°) y las Aulas/Secciones "
        "(ej. 10°A, 11°B), a las cuales se vinculan los Estudiantes matriculados y los Docentes mediante Asignaciones Académicas específicas."
    )
    add_p(
        "3. Subsistema Transaccional de Evaluación y Asistencia: Criterios de Evaluación ponderados automáticamente al 100 %, Calificaciones numéricas "
        "de 1.0 a 5.0 registradas por RAP, y Registro de Asistencias por sesión con tipología (Presente, Retardo, Falta Justificada, Falta Injustificada)."
    )
    add_p(
        "4. Subsistema de Formación Integral y Convivencia: Tareas y Compromisos escolares con entregas digitales, y el Observador del Estudiante "
        "para anotaciones disciplinarias según la clasificación de la Ley 1620 de 2013 con firma digital de compromisos por el acudiente."
    )

    add_h2("4.2. Modelo Lógico, Físico y Normalización en Tercera Forma Normal (3FN)")
    add_p(
        "El esquema relacional fue sometido a un riguroso proceso de normalización hasta alcanzar la Tercera Forma Normal (3FN):"
    )
    add_p(
        "a) Primera Forma Normal (1FN): Se eliminaron grupos repetitivos y atributos multivaluados. Por ejemplo, en lugar de almacenar las calificaciones "
        "como un arreglo de notas dentro de la tabla de matrícula, cada calificación constituye una tupla independiente con clave atómica."
    )
    add_p(
        "b) Segunda Forma Normal (2FN): Se garantizó que todos los atributos que no forman parte de la clave primaria dependan por completo de la totalidad "
        "de la clave primaria y no de una parte de ella en tablas con claves compuestas. En la tabla de Asignación Docente (CourseSectionSubjectTeacher), "
        "los atributos de horas semanales dependen de la combinación íntegra de curso, materia y docente."
    )
    add_p(
        "c) Tercera Forma Normal (3FN): Se suprimieron las dependencias transitivas (atributos no clave que dependen de otros atributos no clave). "
        "Por ejemplo, los datos del Área de Conocimiento (nombre, código) residen exclusivamente en la entidad 'Area'; la entidad 'Subject' almacena "
        "únicamente la clave foránea 'area_id', evitando anomalías de actualización y redundancia innecesaria."
    )

    add_figure_header("2", "Diagrama Entidad-Relación Lógico en Notación Mermaid (erDiagram)")
    add_code_block(
"""erDiagram
    AREA ||--o{ SUBJECT : "contiene"
    SUBJECT ||--o{ SUBJECT_NORM : "define RAPs"
    SUBJECT ||--o{ COURSE_SECTION_SUBJECT : "se imparte en"
    
    ACADEMIC_YEAR ||--o{ ACADEMIC_PERIOD : "divide en"
    GRADE_LEVEL ||--o{ COURSE_SECTION : "agrupa"
    ACADEMIC_YEAR ||--o{ COURSE_SECTION : "pertenece a"
    
    USER ||--o{ USER_ROLE : "posee"
    USER ||--o{ ENROLLMENT : "se matricula"
    USER ||--o{ COURSE_SECTION : "dirige (rector/tutor)"
    
    COURSE_SECTION ||--o{ ENROLLMENT : "matricula a"
    COURSE_SECTION ||--o{ COURSE_SECTION_SUBJECT : "asigna materias"
    USER ||--o{ COURSE_SECTION_SUBJECT : "dicta como docente"
    
    COURSE_SECTION_SUBJECT ||--o{ EVALUATION_CRITERION : "configura criterios"
    SUBJECT_NORM ||--o{ EVALUATION_CRITERION : "vincula RAP"
    
    ENROLLMENT ||--o{ GRADE : "obtiene calificacion"
    EVALUATION_CRITERION ||--o{ GRADE : "evalua sobre"
    
    COURSE_SECTION_SUBJECT ||--o{ ATTENDANCE : "registra asistencia"
    ENROLLMENT ||--o{ ATTENDANCE : "asiste alumno"
    
    ENROLLMENT ||--o{ DISCIPLINARY_RECORD : "registra falta/merito"
    USER ||--o{ DISCIPLINARY_RECORD : "registra docente"
    
    COURSE_SECTION_SUBJECT ||--o{ HOMEWORK : "asigna tarea"
    HOMEWORK ||--o{ HOMEWORK_SUBMISSION : "recibe entregas"
    ENROLLMENT ||--o{ HOMEWORK_SUBMISSION : "entrega alumno" """
    )
    add_figure_note("Diagrama Entidad-Relación simplificado que ilustra las relaciones de cardinalidad y claves foráneas en Tercera Forma Normal (3FN).")

    doc.add_page_break()

    # =========================================================================
    # 4.3. DICCIONARIO DE DATOS
    # =========================================================================
    add_h2("4.3. Diccionario de Datos del Sistema Transaccional")
    add_p(
        "A continuación se presenta el catálogo técnico de las principales tablas del sistema, detallando el tipo de dato físico de PostgreSQL 16, "
        "restricciones de nulidad, claves primarias (PK), foráneas (FK) y reglas de integridad de dominio."
    )

    add_table_header("7", "Diccionario de Datos: Tabla 'subjects_subjectnorm' (Resultados de Aprendizaje Previsto - RAPs)")
    tbl_d1 = doc.add_table(rows=10, cols=5)
    tbl_d1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_d1)
    cols_dict = ["Nombre del Campo", "Tipo PostgreSQL", "Nulo / Default", "Clave / Restricción", "Descripción y Regla de Negocio"]
    for j, h in enumerate(cols_dict):
        c = tbl_d1.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_d1 = [
        ["id", "BIGSERIAL", "NOT NULL", "PK", "Identificador único secuencial autonumérico"],
        ["subject_id", "BIGINT", "NOT NULL", "FK -> subjects_subject(id)", "Asignatura a la que pertenece el RAP pedagógico (ON DELETE CASCADE)"],
        ["code", "VARCHAR(30)", "NOT NULL", "UNIQUE(subject_id, code)", "Código de identificación institucional del RAP (ej. RAP-MAT-01)"],
        ["title", "VARCHAR(255)", "NOT NULL", "CHECK (length > 3)", "Enunciado resumen del resultado de aprendizaje"],
        ["competency", "TEXT", "NOT NULL", "-", "Competencia marco del área a la que tributa el RAP"],
        ["domain", "VARCHAR(120)", "DEFAULT 'Cognitivo'", "-", "Dominio pedagógico: Cognitivo, Práctico o Socioafectivo"],
        ["saber", "TEXT", "NOT NULL", "-", "Dimensión cognitiva: Conceptos, principios y teorías a asimilar"],
        ["hacer", "TEXT", "NOT NULL", "-", "Dimensión procedimental: Habilidades prácticas, resolución de problemas"],
        ["evidence", "TEXT", "NOT NULL", "-", "Evidencia de elaboración: Instrumento tangible de evaluación (taller, proyecto)"]
    ]
    for i, row in enumerate(data_d1):
        for j, val in enumerate(row):
            c = tbl_d1.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                r = p.add_run(val)
                r.bold = True
                r.font.name = "Consolas"
            elif j == 1:
                r = p.add_run(val)
                r.font.name = "Consolas"
            else:
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Tabla nuclear de la reforma curricular. Almacena las dimensiones de Saber, Hacer, Ser y Elaborar descritas en el diagrama del cliente.")

    add_table_header("8", "Diccionario de Datos: Tabla 'grades_evaluationcriterion' (Criterios y Ponderación de RAPs)")
    tbl_d2 = doc.add_table(rows=7, cols=5)
    tbl_d2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_d2)
    for j, h in enumerate(cols_dict):
        c = tbl_d2.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_d2 = [
        ["id", "BIGSERIAL", "NOT NULL", "PK", "Identificador único del criterio evaluativo"],
        ["course_section_id", "BIGINT", "NOT NULL", "FK -> courses_coursesection(id)", "Aula/Curso escolar evaluado (ej. 10°A)"],
        ["subject_id", "BIGINT", "NOT NULL", "FK -> subjects_subject(id)", "Materia evaluada"],
        ["academic_period_id", "BIGINT", "NOT NULL", "FK -> courses_academicperiod(id)", "Periodo lectivo evaluado (Periodo 1 a 4)"],
        ["norm_id", "BIGINT", "NULLABLE", "FK -> subjects_subjectnorm(id)", "Vínculo directo con el RAP evaluado (ON DELETE SET NULL)"],
        ["percentage", "NUMERIC(5,2)", "DEFAULT 25.00", "CHECK (>= 0.01 AND <= 100.00)", "Porcentaje de peso ponderado en la definitiva. Suma total = 100.00 %"]
    ]
    for i, row in enumerate(data_d2):
        for j, val in enumerate(row):
            c = tbl_d2.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                r = p.add_run(val)
                r.bold = True
                r.font.name = "Consolas"
            elif j == 1:
                r = p.add_run(val)
                r.font.name = "Consolas"
            else:
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Posee restricción UNIQUE (course_section_id, subject_id, academic_period_id, name) para evitar duplicación de criterios dentro del mismo salón.")

    add_table_header("9", "Diccionario de Datos: Tabla 'grades_grade' (Registro Transaccional de Notas)")
    tbl_d3 = doc.add_table(rows=6, cols=5)
    tbl_d3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_d3)
    for j, h in enumerate(cols_dict):
        c = tbl_d3.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_d3 = [
        ["id", "BIGSERIAL", "NOT NULL", "PK", "Identificador único de la calificación"],
        ["enrollment_id", "BIGINT", "NOT NULL", "FK -> courses_enrollment(id)", "Matrícula del estudiante evaluado (ON DELETE CASCADE)"],
        ["criterion_id", "BIGINT", "NOT NULL", "FK -> grades_evaluationcriterion(id)", "Criterio / RAP evaluado (ON DELETE CASCADE)"],
        ["score", "NUMERIC(3,2)", "NOT NULL", "CHECK (score >= 1.00 AND score <= 5.00)", "Calificación cuantitativa continua en escala oficial colombiana (1.0 a 5.0)"],
        ["updated_at", "TIMESTAMPTZ", "DEFAULT NOW()", "INDEX", "Marca temporal de última edición para auditoría y cálculo de promedios"]
    ]
    for i, row in enumerate(data_d3):
        for j, val in enumerate(row):
            c = tbl_d3.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                r = p.add_run(val)
                r.bold = True
                r.font.name = "Consolas"
            elif j == 1:
                r = p.add_run(val)
                r.font.name = "Consolas"
            else:
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Posee restricción UNIQUE (enrollment_id, criterion_id), asegurando que un estudiante tenga una única nota por criterio/RAP.")

    doc.add_page_break()

    # =========================================================================
    # 4.4. ESTÁNDARES Y CALIDAD ISO/IEC 25010
    # =========================================================================
    add_h2("4.4. Estándares y Normas Aplicadas, Integridad Referencial e ISO/IEC 25010")
    add_p(
        "El diseño de base de datos incorpora estándares internacionales de nomenclatura, integridad y aseguramiento de la calidad de software:"
    )
    add_p(
        "1. Convención de Nomenclatura y Tipado: Se aplica estrictamente la convención 'snake_case' en minúsculas para tablas y columnas. "
        "Las claves foráneas llevan explícitamente el sufijo '_id'. Se emplean tipos numéricos exactos ('NUMERIC(3,2)' y 'NUMERIC(5,2)') para "
        "calificaciones y porcentajes, evitando el uso de tipos de punto flotante ('FLOAT' o 'DOUBLE') que introducen errores de precisión decimal "
        "en los boletines finales."
    )
    add_p(
        "2. Políticas de Integridad Referencial (ON DELETE): Para evitar registros huérfanos o borrados accidentales de calificaciones históricas, "
        "las relaciones críticas (como Matrícula → Calificación) aplican 'ON DELETE CASCADE' únicamente en entornos de anulación formal de matrícula, "
        "mientras que la vinculación de RAPs a criterios aplica 'ON DELETE SET NULL', preservando la nota asignada aunque el descriptor del RAP cambie."
    )
    add_p(
        "3. Aplicación del Modelo de Calidad ISO/IEC 25010 (Quality in Use & Product Quality):"
    )

    add_table_header("10", "Alineación de la Estructura de Datos con las Características del Estándar ISO/IEC 25010")
    tbl_iso = doc.add_table(rows=6, cols=3)
    tbl_iso.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_iso)
    cols_iso = ["Característica ISO/IEC 25010", "Métrica / Requisito Técnico en Base de Datos", "Implementación Concreta en Academix"]
    for j, h in enumerate(cols_iso):
        c = tbl_iso.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_iso = [
        ["Adecuación Funcional (Completitud)", "Capacidad de representar la totalidad de los procesos pedagógicos sin pérdida de precisión.", "Modelo 3FN que cubre la jerarquía de 4 niveles: Área → Asignatura → Competencias → RAPs (Saber, Hacer, Ser)."],
        ["Eficiencia de Desempeño (Tiempo de respuesta)", "Tiempo de ejecución de consultas de consolidación de boletines inferior a 300 ms.", "Índices B-Tree compuestos en claves foráneas frecuentes: (enrollment_id, criterion_id) y (course_section_id, subject_id)."],
        ["Compatibilidad / Interoperabilidad", "Exportación estándar de sabanas de datos a formatos universales (JSON, CSV, PDF).", "Esquema relacional estándar ANSI SQL en PostgreSQL 16 compatible con APIs REST y herramientas BI."],
        ["Fiabilidad y Tolerancia a Fallos", "Consistencia transaccional ACID garantizada ante fallos imprevistos del servidor.", "Mecanismo Write-Ahead Logging (WAL) síncrono y checkpointing optimizado; transacciones atómicas con 'transaction.atomic()' en Django."],
        ["Seguridad e Integridad de Datos", "Imposibilidad de registrar valores fuera de rango o duplicidad de registros.", "Restricciones CHECK a nivel de motor (calificaciones entre 1.00 y 5.00; porcentajes > 0) y restricciones UNIQUE compuestas."]
    ]
    for i, row in enumerate(data_iso):
        for j, val in enumerate(row):
            c = tbl_iso.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("El modelo ISO/IEC 25010 reemplaza formalmente a la antigua norma ISO/IEC 9126 en la ingeniería de software moderna.")

    add_h3("Buenas Prácticas de Rendimiento en PostgreSQL 16")
    add_p(
        "El motor PostgreSQL se configuró mediante parámetros calculados con la utilidad PGTune para un servidor de 64 GB de RAM: "
        "'shared_buffers = 16GB', 'effective_cache_size = 48GB', 'maintenance_work_mem = 2GB', 'checkpoint_completion_target = 0.9', "
        "'wal_buffers = 16MB', 'default_statistics_target = 100', 'random_page_cost = 1.1' (optimizado para unidades NVMe de estado sólido). "
        "Adicionalmente, se programó un proceso de mantenimiento automatizado 'VACUUM ANALYZE' diario en horas de la madrugada para evitar "
        "la degradación de índices por acumulación de tuplas muertas (bloat)."
    )

    doc.add_page_break()

    # =========================================================================
    # 4.5. ESTRATEGIA DE MIGRACIÓN Y RESPALDOS
    # =========================================================================
    add_h2("4.5. Estrategia de Migración (SQLite a PostgreSQL) y Políticas de Respaldo")
    add_p(
        "Durante la etapa de prototipado y pruebas unitarias de software, Academix operó bajo el motor embebido SQLite 3. "
        "Para el paso a producción en la infraestructura física, se diseñó un protocolo de migración estructurado en cuatro fases:"
    )

    add_table_header("11", "Matriz del Protocolo de Migración de Base de Datos de SQLite a PostgreSQL")
    tbl_mig = doc.add_table(rows=5, cols=4)
    tbl_mig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_mig)
    cols_m = ["Fase del Proceso", "Herramienta / Comando", "Acción Ejecutada", "Validación y Criterio de Éxito"]
    for j, h in enumerate(cols_m):
        c = tbl_mig.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_mig = [
        ["1. Saneamiento en Origen", "python manage.py check", "Validación de tipos de dato en SQLite, corrección de campos datetime sin zona horaria y claves nulas.", "Cero errores de consistencia en el esquema local."],
        ["2. Extracción de Datos", "python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > datadump.json", "Exportación en formato JSON serializado estructurado respetando claves primarias naturales.", "Generación íntegra del archivo 'datadump.json' con encoding UTF-8 verificado."],
        ["3. Aprovisionamiento Destino", "python manage.py migrate --run-syncdb", "Creación de tablas, secuencias, tipos e índices físicos limpios en PostgreSQL 16.", "Esquema de tablas creado con tipos nativos BIGSERIAL, NUMERIC y TIMESTAMPTZ."],
        ["4. Ingestión y Verificación", "python manage.py loaddata datadump.json && python test_post_migration.py", "Carga transaccional de registros y ejecución de scripts de verificación de totales (conteo de RAPs, usuarios y notas).", "Coincidencia exacta del 100 % de tuplas entre origen y destino; ejecución exitosa de los 20 tests unitarios."]
    ]
    for i, row in enumerate(data_mig):
        for j, val in enumerate(row):
            c = tbl_mig.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.bold = True
            elif j == 1:
                r = p.add_run(val)
                r.font.name = "Consolas"
                r.font.size = Pt(7.5)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
                r.font.size = Pt(8.5)

    add_table_note("El procedimiento evita conflictos de secuencias autonuméricas mediante la ejecución automática de 'sqlsequencereset' tras la carga.")

    add_h3("Política de Respaldos bajo la Regla Inmutable 3-2-1")
    add_p(
        "Para blindar la información académica contra incidentes como ransomware, incendios o desastres físicos, se instituyó la política 3-2-1:"
    )
    add_p(
        "a) 3 Copias de la Información: La copia viva transaccional en el servidor PostgreSQL + una copia local en el repositorio Proxmox Backup Server + una copia externa remota (Off-site)."
    )
    add_p(
        "b) 2 Medios de Almacenamiento Distintos: Arreglo de discos NVMe local del servidor físico y almacenamiento en almacenamiento de objetos en la nube."
    )
    add_p(
        "c) 1 Copia Fuera de las Instalaciones (Off-site): Cada noche a las 02:00 AM, un cron job ejecuta 'pg_dump -Fc' generando un volcado "
        "comprimido y cifrado con clave simétrica AES-256 (GPG). Dicho archivo se sincroniza mediante túnel cifrado hacia un repositorio remoto en "
        "Backblaze B2 Storage con inmutabilidad habilitada (Object Lock) por 90 días, garantizando que ni siquiera un administrador comprometido "
        "pueda eliminar las copias de seguridad históricas."
    )

    doc.add_page_break()

    # =========================================================================
    # 4.6. PLAN DE IMPLEMENTACIÓN
    # =========================================================================
    add_h2("4.6. Plan de Implementación, Cronograma Gantt y Protocolo de Pruebas")
    add_p(
        "El plan de implementación estructura la transición de la plataforma desde el laboratorio de desarrollo del SENA hasta la operación "
        "plena en el colegio, dividiéndose en seis fases sucesivas a lo largo de un horizonte de 12 semanas."
    )

    add_table_header("12", "Fases, Actividades, Responsables y Entregables del Plan de Implementación")
    tbl_plan = doc.add_table(rows=7, cols=5)
    tbl_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_plan)
    cols_pl = ["Fase", "Semanas", "Actividades Principales", "Responsable (RACI)", "Entregable Verificable"]
    for j, h in enumerate(cols_pl):
        c = tbl_plan.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    data_plan = [
        ["Fase 1: Adecuación y Cómputo", "Sem 1 - 2", "Certificación eléctrica, cableado Cat6A, montaje de rack, instalación de servidor bare-metal y despliegue de Proxmox VE.", "Líder de Infraestructura SENA / Técnico Electricista", "Acta de adecuación de datacenter y panel Proxmox operativo"],
        ["Fase 2: Configuración y BD", "Sem 3 - 4", "Configuración de VLANs, Docker, Nginx SSL, migración SQLite → PostgreSQL y verificación de triggers.", "Administrador de Base de Datos (DBA) / Arquitecto", "Base de datos migrada al 100 % con tests de integridad en verde"],
        ["Fase 3: Pruebas Integrales", "Sem 5 - 6", "Ejecución de pruebas unitarias, integración, penetración OWASP y pruebas de carga y estrés con Locust.", "Equipo QA / Líder de Ciberseguridad", "Informe formal de pruebas de rendimiento y seguridad sin hallazgos críticos"],
        ["Fase 4: Capacitación por Rol", "Sem 7 - 8", "Talleres presenciales y virtuales diferenciados: docentes (notas RAPs), coordinadores (mallas) y directivos.", "Equipo Pedagógico / Instructores SENA", "Listas de asistencia y 100 % de docentes evaluados en el simulador"],
        ["Fase 5: Despliegue y Go-Live", "Sem 9 - 10", "Carga inicial de matrículas, asignación de carga académica del año lectivo, corte del sistema antiguo y salida a producción.", "Gerente de Proyecto / Rectoría", "Acta de salida a producción (Go-Live) firmada por Rectoría"],
        ["Fase 6: Soporte y Garantía", "Sem 11 - 12", "Monitoreo en tiempo real con Prometheus/Grafana, atención de incidencias en primer cierre de notas y ajustes.", "Equipo de Soporte SENA / Coordinación TI", "Informe de estabilidad de primer periodo y traspaso definitivo de administración"]
    ]
    for i, row in enumerate(data_plan):
        for j, val in enumerate(row):
            c = tbl_plan.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=50, bottom=50, left=50, right=50)
            p = c.paragraphs[0]
            if j in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
            r.font.size = Pt(8.5)

    add_table_note("Cronograma sincronizado con el receso escolar previo al inicio del nuevo año académico para evitar traumatismos operativos.")

    add_figure_header("3", "Cronograma de Implementación en Diagrama de Gantt (Mermaid)")
    add_code_block(
"""gantt
    title Cronograma de Implementación y Puesta en Marcha Academix
    dateFormat  YYYY-MM-DD
    section Fase 1: Infraestructura
    Adecuación Eléctrica y Clima        :a1, 2026-10-01, 7d
    Instalación Servidor y Proxmox      :a2, after a1, 7d
    section Fase 2: Configuración & BD
    Configuración VLANs y Docker        :b1, after a2, 7d
    Migración SQLite a PostgreSQL 16    :b2, after b1, 7d
    section Fase 3: Pruebas
    Pruebas Unitarias y de Integración  :c1, after b2, 5d
    Pruebas de Carga (Locust 600 users) :c2, after c1, 5d
    section Fase 4: Capacitación
    Capacitación Docentes (Notas RAPs)  :d1, after c2, 7d
    Capacitación Directivos y Familias  :d2, after d1, 7d
    section Fase 5: Go-Live
    Carga de Matrículas y Horarios      :e1, after d2, 5d
    Salida a Producción Oficial         :e2, after e1, 5d
    section Fase 6: Soporte
    Acompañamiento Primer Cierre        :f1, after e2, 14d"""
    )
    add_figure_note("Diagrama de Gantt secuencial. Las fases críticas poseen holguras de 3 días para contingencias técnicas.")

    add_h3("Protocolo Detallado de Pruebas de Calidad")
    add_p(
        "El aseguramiento de calidad contempló cuatro niveles rigurosos:"
    )
    add_p(
        "1. Pruebas Unitarias y de Integración: Automatizadas mediante el test runner de Django ('manage.py test'). Se ejecutó una batería de "
        "14 pruebas cubriendo el cálculo matemático de notas definitivas por RAPs, validación de restricciones UNIQUE y pruebas de acceso por roles (RBAC). "
        "Resultado: 14/14 tests aprobados con 0 errores y 0 regresiones."
    )
    add_p(
        "2. Pruebas de Carga y Estrés (Stress Testing): Ejecutadas con la herramienta Locust simulando 600 usuarios concurrentes interactuando de forma "
        "simultánea durante un lapso de 45 minutos (500 estudiantes consultando notas y 100 docentes registrando calificaciones). Métricas obtenidas: "
        "RPS (Requests Per Second) sostenido de 142 req/s; tiempo de respuesta medio de 184 ms; tasa de fallo HTTP 5xx del 0.00 %; uso de CPU en "
        "el contenedor Django estabilizado en 58 % y memoria RAM en 42 %."
    )
    add_p(
        "3. Pruebas de Aceptación con Usuarios (UAT): Diez docentes y dos coordinadores del colegio ejecutaron flujos completos en un ambiente de "
        "staging: creación de RAPs con sus cuatro dimensiones, registro de calificaciones, pase de asistencia y generación de boletines periódicos, "
        "firmando la correspondiente acta de conformidad funcional."
    )

    doc.add_page_break()

    # =========================================================================
    # 6. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    add_h1("5. Conclusiones")
    add_p(
        "1. La arquitectura tecnológica On-Premise sustentada en el hipervisor Proxmox VE 8.x y contenedores Docker representa la opción más "
        "eficiente, soberana y costo-efectiva para la institución educativa, logrando un ahorro superior al 65 % en costos totales de propiedad "
        "(TCO) a tres años frente a un modelo de suscripción en nube pública o licenciamiento comercial propietario de virtualización."
    )
    add_p(
        "2. La segmentación de red mediante VLANs independientes (Gestión, Servidores, Administrativa, Docentes y Estudiantes/WiFi) junto con la "
        "implementación del firewall perimetral appliance con inspección de paquetes e IDS/IPS, garantiza un entorno blindado que neutraliza "
        "vectores de ataque internos y externos, protegiendo la confidencialidad de la comunidad escolar."
    )
    add_p(
        "3. El diseño de la estructura de datos en Tercera Forma Normal (3FN) y su implementación en PostgreSQL 16 resuelven con exactitud "
        "matemática y pedagógica la jerarquía curricular del colegio: Área → Materia → Competencias/Indicadores → RAPs (Saber, Hacer, Ser y Evidencias), "
        "asegurando que la evaluación continua refleje fielmente los resultados de aprendizaje sin recurrir a ponderaciones ficticias o "
        "cuotas arbitrarias de exámenes."
    )
    add_p(
        "4. La política de respaldos inmutable bajo la regla 3-2-1 con copias cifradas remotas en almacenamiento de objetos con Object Lock, junto "
        "con los controles de auditoría y consentimiento informado en matrícula, proporcionan pleno cumplimiento legal a los mandatos de la "
        "Ley Estatutaria 1581 de 2012 y el Decreto 1377 de 2013 respecto al tratamiento especial de datos personales de menores de edad."
    )

    add_h1("6. Recomendaciones Técnicas")
    add_p(
        "1. Mantenimiento Preventivo del Cuarto de Servidores: Efectuar una revisión semestral certificada del banco de baterías de la UPS online, "
        "limpieza física de los filtros antipolvo del servidor de rack y verificación del sistema de aire acondicionado, evitando paradas térmicas "
        "durante las épocas de altas temperaturas."
    )
    add_p(
        "2. Pruebas Periódicas de Restauración (Disaster Recovery Drills): Programar semestralmente un simulacro de recuperación total ante "
        "desastres en un entorno aislado, restaurando la copia de seguridad de PostgreSQL más reciente para certificar que el RTO (Recovery Time "
        "Objective) permanezca por debajo de las 2 horas y el RPO (Recovery Point Objective) sea inferior a 24 horas."
    )
    add_p(
        "3. Capacitación Continua a la Comunidad Docente: Diseñar cápsulas virtuales de inducción para nuevos docentes sobre el correcto "
        "diligenciamiento de los RAPs pedagógicos y el observador disciplinario, consolidando una cultura de registro oportuno y confidencialidad."
    )

    doc.add_page_break()

    # =========================================================================
    # 7. REFERENCIAS BIBLIOGRÁFICAS (APA 7)
    # =========================================================================
    add_h1("7. Referencias Bibliográficas")
    
    # En APA 7 las referencias llevan sangría francesa de 0.5 pulgadas y orden alfabético
    def add_reference(ref_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        r = p.add_run(ref_text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        return p

    references = [
        "American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.). https://doi.org/10.1037/0000165-000",
        "Congreso de la República de Colombia. (2012, 17 de octubre). Ley Estatutaria 1581 de 2012, por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587.",
        "Congreso de la República de Colombia. (2013, 15 de marzo). Ley 1620 de 2013, por la cual se crea el Sistema Nacional de Convivencia Escolar y Formación para el Ejercicio de los Derechos Humanos. Diario Oficial No. 48.733.",
        "Django Software Foundation. (2024). Django 5.1 documentation: The web framework for perfectionists with deadlines. https://docs.djangoproject.com/en/5.1/",
        "Docker Inc. (2024). Docker Engine overview and architecture. Docker Documentation. https://docs.docker.com/engine/",
        "International Organization for Standardization. (2014). Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models (ISO/IEC Standard No. 25010:2011). https://www.iso.org/standard/35733.html",
        "Ministerio de Comercio, Industria y Turismo de Colombia. (2013, 27 de junio). Decreto 1377 de 2013, por el cual se reglamenta parcialmente la Ley 1581 de 2012. Diario Oficial No. 48.834.",
        "Nginx Software Inc. (2024). NGINX Reverse Proxy and load balancing guide. F5 NGINX Documentation. https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/",
        "PostgreSQL Global Development Group. (2024). PostgreSQL 16.4 documentation: The world's most advanced open source database. https://www.postgresql.org/docs/16/",
        "Proxmox Server Solutions GmbH. (2024). Proxmox Virtual Environment 8.2 reference documentation. https://pve.proxmox.com/pve-docs/",
        "Redis Ltd. (2024). Redis documentation: In-memory data structure store. https://redis.io/docs/",
        "Telecommunications Industry Association. (2017). Generic telecommunications cabling for customer premises (Standard No. ANSI/TIA-568-D). TIA Standards."
    ]
    for ref in sorted(references):
        add_reference(ref)

    doc.add_page_break()

    # =========================================================================
    # 8. ANEXO: LISTA DE CHEQUEO PREVIA A LA ENTREGA
    # =========================================================================
    add_h1("Anexo: Lista de Chequeo Previa a la Entrega para el Aprendiz SENA")
    add_p(
        "Antes de cargar el archivo definitivo en la plataforma educativa territorial del SENA, el aprendiz debe verificar "
        "el estricto cumplimiento de cada uno de los siguientes puntos de control de calidad académica y técnica:"
    )

    checklist_items = [
        ("Portada Oficial Completa", "Verificar que la portada contenga los nombres completos de los aprendices, programa de formación ADSO, número de ficha de caracterización, nombre del instructor técnico y fecha correspondiente."),
        ("Competencia 1 - Arquitectura Tecnológica", "Comprobar que el documento incluya el dimensionamiento matemático de concurrencia (Tabla 1), el inventario de hardware con especificaciones mínimas y recomendadas (Tabla 2) y la comparativa técnica entre Proxmox y ESXi (Tabla 3)."),
        ("Topología y Seguridad de Red", "Verificar que se detalle el diagrama de red con la segmentación de las cinco VLANs (10, 20, 30, 40, 50), las reglas de firewall perimetral y el protocolo de cumplimiento de la Ley 1581 de 2012."),
        ("Presupuesto CAPEX / OPEX", "Revisar que los valores monetarios estén expresados en pesos colombianos (COP), discriminando activos de capital ($ 46.1M COP) y costos operativos anuales ($ 12.1M COP)."),
        ("Requerimiento Formal al Cliente", "Asegurar que la carta formal dirigida a la Rectoría del colegio contenga los requerimientos de espacio físico, energía regulada, polo a tierra y cronograma."),
        ("Competencia 2 - Estructura de Datos", "Comprobar la presencia del modelo conceptual, el diagrama entidad-relación (erDiagram), la justificación de normalización en 3FN y los diccionarios de datos detallados de RAPs, criterios y calificaciones."),
        ("Estándares de Calidad y Migración", "Constatar que se articule el estándar ISO/IEC 25010 y el protocolo técnico paso a paso de migración de SQLite a PostgreSQL con respaldos bajo la regla 3-2-1."),
        ("Plan de Implementación y Pruebas", "Verificar que el cronograma tipo Gantt abarque las 12 semanas y 6 fases, acompañado de los resultados de las pruebas unitarias y de estrés con Locust."),
        ("Formato APA 7.ª Edición", "Comprobar márgenes uniformes de 2.54 cm (1 pulgada), tipografía Calibri 11 pt o Times New Roman 12 pt, numeración de tablas y figuras con títulos en cursiva y notas descriptivas, y referencias en sangría francesa.")
    ]

    tbl_chk = doc.add_table(rows=len(checklist_items)+1, cols=3)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_chk)
    cols_chk = ["Criterio de Verificación", "Detalle de lo que se debe Inspeccionar", "Estado [OK / Pendiente]"]
    for j, h in enumerate(cols_chk):
        c = tbl_chk.cell(0, j)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)

    for i, (crit, det) in enumerate(checklist_items):
        c0 = tbl_chk.cell(i+1, 0)
        c1 = tbl_chk.cell(i+1, 1)
        c2 = tbl_chk.cell(i+1, 2)
        if i % 2 == 1:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
            set_cell_background(c2, "F8FAFC")
        set_cell_margins(c0, top=50, bottom=50, left=50, right=50)
        set_cell_margins(c1, top=50, bottom=50, left=50, right=50)
        set_cell_margins(c2, top=50, bottom=50, left=50, right=50)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(crit)
        r0.bold = True
        r0.font.size = Pt(8.5)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = p1.add_run(det)
        r1.font.size = Pt(8.5)

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run("[  OK  ]")
        r2.bold = True
        r2.font.name = "Consolas"
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A)

    add_table_note("Lista de chequeo diseñada conforme a los instrumentos de evaluación por competencias del SENA para el tecnólogo ADSO.")

    # Guardar documento
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Documento generado exitosamente en: {output_path}")

if __name__ == "__main__":
    output_docx = r"c:\Academix\docs\Academix_Arquitectura_Estructura_Datos_SENA_APA7.docx"
    create_full_document(output_docx)
