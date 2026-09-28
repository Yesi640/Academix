# -*- coding: utf-8 -*-
"""
Script to cleanly populate KnowledgeArea, Subject, GradeSubject,
and sanitize GradeLevel, CourseSection, AcademicYear names.
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import GradeLevel, CourseSection, AcademicYear, InstitutionSetting
from apps.subjects.models import KnowledgeArea, Subject, GradeSubject

INST = 'COLEGIO'

# Ensure InstitutionSetting is set to COLEGIO
setting = InstitutionSetting.get_settings()
setting.institution_type = INST
setting.term_grade = 'Grado'
setting.term_section = 'Curso'
setting.term_teacher = 'Docente'
setting.term_subject = 'Asignatura'
setting.term_rector = 'Rector(a)'
setting.term_coordinator = 'Coordinador(a)'
setting.save()
print("InstitutionSetting updated.")

# 1. Sanitize AcademicYear
for y in AcademicYear.objects.all():
    name = y.name
    # Replace corrupted characters
    name = name.replace('Ao', 'Año').replace('Ao', 'Año')
    y.name = name
    y.save()
print("AcademicYears sanitized.")

# 2. Sanitize GradeLevels
GRADE_NAMES = {
    'GR-00': 'Transicion',
    'GR-01': 'Primero',
    'GR-02': 'Segundo',
    'GR-03': 'Tercero',
    'GR-04': 'Cuarto',
    'GR-05': 'Quinto',
    'GR-06': 'Sexto',
    'GR-07': 'Septimo',
    'GR-08': 'Octavo',
    'GR-09': 'Noveno',
    'GR-10': 'Decimo',
    'GR-11': 'Once',
}

for code, clean_name in GRADE_NAMES.items():
    gl = GradeLevel.objects.filter(code=code).first()
    if gl:
        gl.name = clean_name
        gl.institution_type = INST
        gl.save()
print("GradeLevels sanitized.")

# 3. Sanitize CourseSections
SECTION_NAMES = {
    'GR-00': 'Transicion A',
    'GR-01': '1-A',
    'GR-02': '2-A',
    'GR-03': '3-A',
    'GR-04': '4-A',
    'GR-05': '5-A',
    'GR-06': '6-A',
    'GR-07': '7-A',
    'GR-08': '8-A',
    'GR-09': '9-A',
    'GR-10': '10-A',
    'GR-11': '11-A',
}

for cs in CourseSection.objects.all():
    code = cs.grade_level.code if cs.grade_level else None
    if code in SECTION_NAMES:
        cs.name = SECTION_NAMES[code]
        cs.save()
print("CourseSections sanitized.")

# 4. Clean and Reseed KnowledgeAreas, Subjects, GradeSubjects
GradeSubject.objects.all().delete()
Subject.objects.all().delete()
KnowledgeArea.objects.all().delete()
print("Subject tables cleared.")

AREAS = [
    (1, 'Matematicas'),
    (2, 'Lengua Castellana e Idiomas'),
    (3, 'Ciencias Naturales y Educacion Ambiental'),
    (4, 'Ciencias Sociales, Historia y Geografia'),
    (5, 'Educacion Etica y Valores Humanos'),
    (6, 'Educacion Religiosa'),
    (7, 'Educacion Fisica, Recreacion y Deporte'),
    (8, 'Educacion Artistica y Cultural'),
    (9, 'Idioma Extranjero Ingles'),
    (10, 'Tecnologia e Informatica'),
    (11, 'Ciencias Economicas y Politicas'),
    (12, 'Filosofia'),
]

area_objs = {}
for order, name in AREAS:
    a = KnowledgeArea.objects.create(institution_type=INST, name=name, order=order)
    area_objs[name] = a
print(f"Created {len(area_objs)} KnowledgeAreas.")

SUBJECTS = [
    ('COL-MAT', 'Matematicas',                         'PRINCIPAL',    'Matematicas',                            4),
    ('COL-LEN', 'Lengua Castellana',                   'PRINCIPAL',    'Lengua Castellana e Idiomas',            4),
    ('COL-CNT', 'Ciencias Naturales',                  'PRINCIPAL',    'Ciencias Naturales y Educacion Ambiental', 4),
    ('COL-BIO', 'Biologia',                            'PRINCIPAL',    'Ciencias Naturales y Educacion Ambiental', 3),
    ('COL-FIS', 'Fisica',                              'PRINCIPAL',    'Ciencias Naturales y Educacion Ambiental', 3),
    ('COL-QUI', 'Quimica',                             'PRINCIPAL',    'Ciencias Naturales y Educacion Ambiental', 3),
    ('COL-SOC', 'Ciencias Sociales',                   'PRINCIPAL',    'Ciencias Sociales, Historia y Geografia',  3),
    ('COL-HIS', 'Historia y Geografia',                'PRINCIPAL',    'Ciencias Sociales, Historia y Geografia',  3),
    ('COL-CON', 'Constitucion Politica',               'HUMANISTICA',  'Ciencias Sociales, Historia y Geografia',  2),
    ('COL-ETI', 'Etica y Valores',                     'HUMANISTICA',  'Educacion Etica y Valores Humanos',       1),
    ('COL-REL', 'Educacion Religiosa',                 'HUMANISTICA',  'Educacion Religiosa',                     1),
    ('COL-EFI', 'Educacion Fisica',                    'ARTE_DEPORTE', 'Educacion Fisica, Recreacion y Deporte',  2),
    ('COL-ART', 'Educacion Artistica',                 'ARTE_DEPORTE', 'Educacion Artistica y Cultural',         2),
    ('COL-MUS', 'Musica',                              'ARTE_DEPORTE', 'Educacion Artistica y Cultural',         1),
    ('COL-ING', 'Ingles',                              'PRINCIPAL',    'Idioma Extranjero Ingles',                3),
    ('COL-TIC', 'Tecnologia e Informatica',            'PRINCIPAL',    'Tecnologia e Informatica',                2),
    ('COL-ECO', 'Economia y Politica',                 'HUMANISTICA',  'Ciencias Economicas y Politicas',         2),
    ('COL-FIL', 'Filosofia',                           'HUMANISTICA',  'Filosofia',                               2),
]

sub_objs = {}
for code, name, cat, area_name, credits in SUBJECTS:
    area = area_objs[area_name]
    s = Subject.objects.create(
        institution_type=INST,
        code=code,
        name=name,
        category=cat,
        area=area,
        credits=credits
    )
    sub_objs[code] = s
print(f"Created {len(sub_objs)} Subjects.")

CURRICULUM = {
    'GR-00': [('COL-MAT',4),('COL-LEN',5),('COL-CNT',3),('COL-SOC',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',2),('COL-TIC',1)],
    'GR-01': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
    'GR-02': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
    'GR-03': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
    'GR-04': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
    'GR-05': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
    'GR-06': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',4),('COL-TIC',2)],
    'GR-07': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',4),('COL-TIC',2)],
    'GR-08': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',1),('COL-ING',4),('COL-TIC',2)],
    'GR-09': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',1),('COL-ING',4),('COL-TIC',2)],
    'GR-10': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-CON',2),('COL-FIL',2),('COL-ECO',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ING',4),('COL-TIC',2)],
    'GR-11': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-CON',2),('COL-FIL',2),('COL-ECO',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ING',4),('COL-TIC',2)],
}

total_gs = 0
for code, subjs in CURRICULUM.items():
    grade = GradeLevel.objects.filter(code=code).first()
    if not grade:
        print(f"Warning: Grade {code} not found.")
        continue
    for sub_code, hours in subjs:
        s = sub_objs.get(sub_code)
        if s:
            GradeSubject.objects.create(
                grade_level=grade,
                subject=s,
                weekly_hours=hours,
                weight_percentage=Decimal('100.00')
            )
            total_gs += 1
print(f"Created {total_gs} GradeSubject curriculum mappings.")
