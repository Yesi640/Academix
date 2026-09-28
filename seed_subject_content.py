# -*- coding: utf-8 -*-
"""
Script to populate description and standard SubjectNorms for subjects.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.subjects.models import Subject, SubjectNorm

SUBJECT_DATA = {
    'COL-MAT': {
        'desc': 'Formación en el pensamiento lógico-matemático a través de los cinco pensamientos: numérico, espacial, métrico, aleatorio y variacional. Desarrollo de competencias para formular, plantear y resolver problemas de la vida cotidiana y científica.',
        'norms': [
            ('MAT-DBA1', 'Pensamiento Numérico y Sistemas Numéricos', 'Usa los números reales y sus propiedades para formular y resolver situaciones cuantitativas y operacionales.'),
            ('MAT-DBA2', 'Pensamiento Espacial y Geométrico', 'Aplica transformaciones geométricas y conceptos de proporcionalidad en la resolución de problemas espaciales.'),
            ('MAT-DBA3', 'Pensamiento Variacional y Funciones', 'Modela situaciones de cambio con expresiones algebraicas, funciones, patrones y ecuaciones.'),
        ]
    },
    'COL-LEN': {
        'desc': 'Desarrollo integral de las cuatro habilidades comunicativas fundamentales: hablar, escuchar, leer y escribir. Fomento de la lectura crítica, la producción de textos continuos y discontinuos, y la apreciación de la literatura universal y colombiana.',
        'norms': [
            ('LEN-DBA1', 'Comprensión e Interpretación Textual', 'Comprende y analiza el sentido global de textos informativos, expositivos y literarios identificando su intencionalidad y estructura.'),
            ('LEN-DBA2', 'Producción Textual Oral y Escrita', 'Produce textos con coherencia, cohesión y pertinencia discursiva, atendiendo a las reglas ortográficas y semánticas.'),
            ('LEN-DBA3', 'Ética y Estética de la Comunicación', 'Valora el diálogo y la literatura como medios de construcción de identidad, pensamiento crítico y convivencia pacífica.'),
        ]
    },
    'COL-CNT': {
        'desc': 'Aproximación al conocimiento de las ciencias naturales mediante la indagación, la formulación de hipótesis y el cuidado del entorno vivo, físico y ambiental.',
        'norms': [
            ('CNT-DBA1', 'Entorno Vivo y Ecosistemas', 'Explica la relación entre la estructura de los seres vivos y su adaptación al medio ambiente.'),
            ('CNT-DBA2', 'Entorno Físico y Materia', 'Reconoce las propiedades fundamentales de la materia, la energía y las fuerzas en el movimiento.'),
            ('CNT-DBA3', 'Ciencia, Tecnología y Sociedad', 'Propone acciones para el uso responsable de los recursos naturales y la preservación de la biodiversidad.'),
        ]
    },
    'COL-BIO': {
        'desc': 'Estudio riguroso de la biología celular, molecular, la genética, la evolución de las especies y el funcionamiento homeostático de los organismos.',
        'norms': [
            ('BIO-DBA1', 'Genética y Mecanismos Moleculares', 'Explica los procesos de replicación celular, transcripción del ADN y las leyes de la herencia mendeliana.'),
            ('BIO-DBA2', 'Evolución y Diversidad Biológica', 'Relaciona la variabilidad genética con los procesos de adaptación y selección natural en las poblaciones.'),
        ]
    },
    'COL-FIS': {
        'desc': 'Estudio de los principios fundamentales del movimiento mecánico, la conservación de la energía, la termodinámica, las ondas y el electromagnetismo.',
        'norms': [
            ('FIS-DBA1', 'Mecánica Clásica y Conservación', 'Aplica las leyes de Newton y los teoremas de conservación del momento y la energía a fenómenos cotidianos.'),
            ('FIS-DBA2', 'Termodinámica y Ondas', 'Analiza la propagación de ondas mecánicas y electromagnéticas y las transformaciones de calor y trabajo.'),
        ]
    },
    'COL-QUI': {
        'desc': 'Análisis de la materia, su estructura electrónica, el enlace químico, las reacciones estequiométricas y la química orgánica e inorgánica.',
        'norms': [
            ('QUI-DBA1', 'Estructura Atómica y Enlace', 'Explica la tabla periódica y la formación de enlaces químicos según la configuración electrónica.'),
            ('QUI-DBA2', 'Reacciones Químicas y Estequiometría', 'Balancea ecuaciones químicas y calcula cantidades molares en reacciones de síntesis y descomposición.'),
        ]
    },
    'COL-SOC': {
        'desc': 'Formación en la comprensión del espacio geográfico, las dinámicas históricas, los derechos humanos y la participación democrática en Colombia y el mundo.',
        'norms': [
            ('SOC-DBA1', 'Historia y Sociedades Humanas', 'Analiza las transformaciones políticas, sociales y económicas en diferentes épocas históricas.'),
            ('SOC-DBA2', 'Espacio Geográfico y Población', 'Interpreta la distribución de la población y el impacto ambiental de las actividades socioeconómicas.'),
            ('SOC-DBA3', 'Competencias Ciudadanas', 'Promueve el respeto a la diversidad cultural y el ejercicio de la democracia participativa.'),
        ]
    },
    'COL-HIS': {
        'desc': 'Estudio en profundidad de los procesos históricos, la geografía humana y la geopolítica contemporánea.',
        'norms': [
            ('HIS-DBA1', 'Procesos Históricos Contemporáneos', 'Comprende las causas y consecuencias de los grandes conflictos y transformaciones del siglo XX y XXI.'),
        ]
    },
    'COL-CON': {
        'desc': 'Conocimiento de la Constitución Política de Colombia de 1991, los mecanismos de participación ciudadana y la estructura del Estado.',
        'norms': [
            ('CON-DBA1', 'Derechos Fundamentales y Tutela', 'Identifica y hace uso de los mecanismos constitucionales para la protección de derechos civiles.'),
        ]
    },
    'COL-ETI': {
        'desc': 'Educación ética, deliberación moral, empatía, dignidad de la persona humana y resolución no violenta de conflictos en el ámbito escolar y familiar.',
        'norms': [
            ('ETI-DBA1', 'Autonomía y Juicio Moral', 'Reconoce la importancia de la coherencia ética entre pensamientos, palabras y acciones.'),
        ]
    },
    'COL-REL': {
        'desc': 'Reflexión antropológica y espiritual sobre el sentido trascendente de la vida humana y el respeto a la libertad religiosa.',
        'norms': [
            ('REL-DBA1', 'Valores Espirituales y Convivencia', 'Comprende el valor del perdón, la solidaridad y la espiritualidad en la vida personal y comunitaria.'),
        ]
    },
    'COL-EFI': {
        'desc': 'Cultura física, capacidades coordinativas y condicionales, motricidad, trabajo en equipo y hábitos de vida activa y saludable.',
        'norms': [
            ('EFI-DBA1', 'Condición Física y Motricidad', 'Ejecuta patrones de movimiento con coordinación, agilidad, resistencia y control postural.'),
        ]
    },
    'COL-ART': {
        'desc': 'Apreciación artística, expresión plástica, visual y diseño. Desarrollo de la creatividad, la sensibilidad y el sentido estético.',
        'norms': [
            ('ART-DBA1', 'Expresión Visual y Creatividad', 'Aplica técnicas de dibujo, pintura y composición en la creación de proyectos artísticos personales.'),
        ]
    },
    'COL-MUS': {
        'desc': 'Educación musical, audición guiada, ritmo, afinación vocal y apreciación de los ritmos folclóricos y contemporáneos.',
        'norms': [
            ('MUS-DBA1', 'Ritmo y Práctica Musical', 'Interpreta patrones rítmicos y melódicos con instrumentos escolares o la voz en ensamble coral.'),
        ]
    },
    'COL-ING': {
        'desc': 'Aprendizaje de la lengua inglesa según el Marco Común Europeo de Referencia. Fortalecimiento de la comprensión auditiva, lectura, interacción oral y redacción básica.',
        'norms': [
            ('ING-DBA1', 'Listening and Reading Comprehension', 'Identifica la idea principal y detalles específicos en textos orales y escritos en lengua inglesa.'),
            ('ING-DBA2', 'Speaking and Writing Communication', 'Intercambia información sobre temas familiares y cotidianos estructurando oraciones gramaticalmente correctas.'),
        ]
    },
    'COL-TIC': {
        'desc': 'Tecnología e informática, alfabetización digital, seguridad en internet, pensamiento computacional y uso ético de herramientas ofimáticas y software.',
        'norms': [
            ('TIC-DBA1', 'Pensamiento Computacional y Lógica', 'Diseña secuencias lógicas y algoritmos básicos para resolver problemas con tecnologías digitales.'),
            ('TIC-DBA2', 'Uso Ético de Herramientas Digitales', 'Aplica normas de seguridad informática, derechos de autor y netiqueta en entornos virtuales.'),
        ]
    },
    'COL-ECO': {
        'desc': 'Ciencias económicas y políticas: estudio de los mercados, la inflación, el empleo, el presupuesto público y los modelos de desarrollo económico.',
        'norms': [
            ('ECO-DBA1', 'Dinámicas Económicas y Mercado', 'Comprende el funcionamiento de los agentes económicos, la oferta, la demanda y las políticas fiscales.'),
        ]
    },
    'COL-FIL': {
        'desc': 'Iniciación al pensamiento filosófico, epistemología, lógica clásica y contemporánea, ética filosófica y corrientes del pensamiento occidental.',
        'norms': [
            ('FIL-DBA1', 'Argumentación Crítica y Pregunta Filosófica', 'Analiza problemas éticos y del conocimiento humano formulando argumentos rigurosos y sustentados.'),
        ]
    },
}

updated_subjs = 0
created_norms = 0

SubjectNorm.objects.all().delete()

for code, data in SUBJECT_DATA.items():
    s = Subject.objects.filter(code=code).first()
    if s:
        s.description = data['desc']
        s.save(update_fields=['description'])
        updated_subjs += 1
        for idx, (n_code, n_title, n_desc) in enumerate(data['norms'], 1):
            SubjectNorm.objects.create(
                subject=s,
                code=n_code,
                title=n_title,
                description=n_desc,
                order=idx
            )
            created_norms += 1

print(f"Updated {updated_subjs} subjects with descriptions.")
print(f"Created {created_norms} SubjectNorms.")
