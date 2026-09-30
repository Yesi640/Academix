# -*- coding: utf-8 -*-
"""
Poblamiento de Mallas Curriculares completas estructuradas según el modelo pedagógico del cliente:
- Área de Conocimiento
- Asignatura / Materia
- Competencias, Dominios, Dimensiones e Indicadores
- RAPs (Resultados de Aprendizaje) con Saber, Hacer, Ser y Evidencia de Elaboración.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.subjects.models import Subject, SubjectNorm

RAP_CURRICULAR_DATA = {
    'COL-MAT': {
        'competency': 'Razonamiento lógico y modelación matemática en contextos cotidianos y científicos.',
        'domain': 'Cognitivo y Resolución de Problemas',
        'dimension': 'Pensamiento Cuantitativo y Lógico-Espacial',
        'raps': [
            {
                'order': 1,
                'code': 'MAT-RAP1',
                'title': 'Pensamiento Numérico y Estructuras Aritméticas',
                'description': 'Aplica el sistema numérico y sus operaciones para resolver problemas de la vida cotidiana y científica.',
                'indicator': 'Resuelve y formula problemas cuantitativos utilizando operaciones y propiedades numéricas.',
                'saber': 'Propiedades de los números reales, teoría de conjuntos, proporcionalidad directa e inversa.',
                'hacer': 'Ejecuta algoritmos de cálculo, simplificación y estimación en problemas reales.',
                'ser': 'Demuestra rigor, precisión y persistencia en el análisis y verificación de resultados.',
                'evidence': 'Taller de problemas aplicados con sustentación de procedimientos matemáticos.'
            },
            {
                'order': 2,
                'code': 'MAT-RAP2',
                'title': 'Pensamiento Espacial y Geometría Aplicada',
                'description': 'Modela situaciones espaciales y transformaciones bidimensionales y tridimensionales.',
                'indicator': 'Calcula áreas, perímetros y volúmenes justificando el uso de fórmulas e instrumentos métricos.',
                'saber': 'Teoremas de semejanza, congruencia, trigonometría básica y figuras geométricas planas y sólidas.',
                'hacer': 'Construye figuras geométricas y modelos espaciales a escala usando regla, compás o software.',
                'ser': 'Valora el orden visual, la creatividad y la limpieza en el trazo y presentación gráfica.',
                'evidence': 'Maqueta o plano a escala con memoria de cálculo métrico.'
            },
            {
                'order': 3,
                'code': 'MAT-RAP3',
                'title': 'Pensamiento Variacional y Modelación Algebraica',
                'description': 'Representa regularidades, patrones y variaciones mediante ecuaciones y funciones.',
                'indicator': 'Identifica relaciones de dependencia entre variables y formula expresiones algebraicas correspondientes.',
                'saber': 'Concepto de función, ecuaciones lineales y cuadráticas, interpretación de pendientes.',
                'hacer': 'Tabula y grafica funciones lineales y no lineales analizando su comportamiento gráfico.',
                'ser': 'Muestra apertura al trabajo colaborativo para interpretar modelos algebraicos.',
                'evidence': 'Informe de modelación de un fenómeno físico o financiero con gráficas y ecuaciones.'
            },
            {
                'order': 4,
                'code': 'MAT-RAP4',
                'title': 'Pensamiento Aleatorio y Análisis Estadístico',
                'description': 'Recolecta, organiza e interpreta datos para la toma fundamentada de decisiones.',
                'indicator': 'Calcula e interpreta medidas de tendencia central y dispersión en muestras estadísticas.',
                'saber': 'Población, muestra, frecuencias, media, mediana, moda y probabilidades simples.',
                'hacer': 'Construye histogramas, diagramas circulares y tablas de frecuencia a partir de datos reales.',
                'ser': 'Asume una postura crítica y ética frente al manejo e interpretación de la información estadística.',
                'evidence': 'Encuesta escolar con informe estadístico, gráficos explicativos y conclusiones.'
            },
        ]
    },
    'COL-LEN': {
        'competency': 'Comunicación integral, comprensión lectora crítica y producción discursiva.',
        'domain': 'Lingüístico y Comunicativo',
        'dimension': 'Dimensión Comunicativa y Estética',
        'raps': [
            {
                'order': 1,
                'code': 'LEN-RAP1',
                'title': 'Comprensión e Interpretación Textual Crítica',
                'description': 'Analiza textos continuos y discontinuos identificando intenciones, posturas y estructuras.',
                'indicator': 'Identifica la tesis central, argumentos y puntos de vista en textos expositivos y argumentativos.',
                'saber': 'Estructura textual, tipologías de textos, niveles de lectura (literal, inferencial, crítico-intertextual).',
                'hacer': 'Extrae ideas principales, sintetiza argumentos y contrasta fuentes diversas de información.',
                'ser': 'Escucha activamente y respeta puntos de vista discrepantes durante la deliberación de textos.',
                'evidence': 'Ficha analítica de lectura crítica con mapa conceptual y postura argumentada.'
            },
            {
                'order': 2,
                'code': 'LEN-RAP2',
                'title': 'Producción Textual Escrita con Cohesión y Coherencia',
                'description': 'Redacta textos expositivos y ensayos con rigor semántico, gramatical y ortográfico.',
                'indicator': 'Produce textos estructurados con introducción, desarrollo argumentativo y conclusión fundamentada.',
                'saber': 'Reglas ortográficas, marcadores textuales, conectores lógicos, normas de citación APA.',
                'hacer': 'Planifica, redacta, revisa y reescribe borradores aplicando corrección de estilo.',
                'ser': 'Manifiesta honestidad académica citando adecuadamente las fuentes consultadas.',
                'evidence': 'Ensayo de dos páginas con bibliografía referenciada y rúbrica de corrección aplicada.'
            },
            {
                'order': 3,
                'code': 'LEN-RAP3',
                'title': 'Comunicación Oral y Argumentación en Público',
                'description': 'Expone ideas con elocuencia, dominio temático y adecuado uso de lenguaje no verbal.',
                'indicator': 'Participa en debates, mesas redondas y exposiciones orales estructurando argumentos persuasivos.',
                'saber': 'Técnicas de oratoria, elementos paralingüísticos, estructura del debate formal.',
                'hacer': 'Sustenta proyectos oralmente adaptando el registro formal al público objetivo.',
                'ser': 'Demuestra seguridad, empatía y tolerancia al confrontar argumentos contrarios.',
                'evidence': 'Participación grabada en debate o mesa redonda con rúbrica de desempeño oral.'
            },
            {
                'order': 4,
                'code': 'LEN-RAP4',
                'title': 'Apreciación Literaria y Pensamiento Poético',
                'description': 'Valora las obras literarias como patrimonio cultural y expresión de la condición humana.',
                'indicator': 'Relaciona obras literarias con sus contextos históricos, culturales y filosóficos.',
                'saber': 'Movimientos literarios, figuras retóricas, géneros lírico, narrativo y dramático.',
                'hacer': 'Crea textos literarios propios (cuentos, poemas, guiones teatrales) con recursos poéticos.',
                'ser': 'Sensibilidad ante la belleza artística y empatía con las realidades expresadas en la literatura.',
                'evidence': 'Antología creativa escolar con texto propio y comentario crítico de una obra leída.'
            },
        ]
    },
    'COL-CNT': {
        'competency': 'Indagación científica, explicación de fenómenos y comprensión del entorno ambiental.',
        'domain': 'Científico y Ecológico',
        'dimension': 'Dimensión Bioética y Pensamiento Científico',
        'raps': [
            {
                'order': 1,
                'code': 'CNT-RAP1',
                'title': 'Entorno Vivo y Dinámica Ecosistémica',
                'description': 'Comprende el flujo de materia y energía en los ecosistemas y la interdependencia biológica.',
                'indicator': 'Modela redes tróficas y explica el impacto de la alteración biológica en el equilibrio ecológico.',
                'saber': 'Niveles de organización biológica, ciclos biogeoquímicos, cadenas y redes tróficas.',
                'hacer': 'Diseña diagramas de flujo de energía y clasifica especies nativas según su nicho ecológico.',
                'ser': 'Compromiso activo con la preservación de la flora, fauna y fuentes hídricas de la región.',
                'evidence': 'Informe de campo o terrario experimental con bitácora de observaciones ecológicas.'
            },
            {
                'order': 2,
                'code': 'CNT-RAP2',
                'title': 'Entorno Físico, Materia y Energía',
                'description': 'Explica las transformaciones físicas y químicas de la materia en la vida diaria.',
                'indicator': 'Diferencia estados de la materia, mezclas y soluciones mediante experimentación guiada.',
                'saber': 'Propiedades generales y específicas de la materia, leyes de la termodinámica elemental.',
                'hacer': 'Realiza experimentos de laboratorio aplicando normas de bioseguridad y registro de datos.',
                'ser': 'Precaución y cuidado en el uso de materiales de laboratorio y sustancias químicas.',
                'evidence': 'Reporte de laboratorio con hipótesis, tablas de datos, análisis de resultados y conclusiones.'
            },
            {
                'order': 3,
                'code': 'CNT-RAP3',
                'title': 'Ciencia, Tecnología y Sostenibilidad Ambiental',
                'description': 'Evalúa el impacto de la actividad humana en el cambio climático y la sostenibilidad.',
                'indicator': 'Propone alternativas sostenibles para el manejo de residuos y el consumo energético responsable.',
                'saber': 'Huella de carbono, energías renovables, gestión integral de residuos sólidos (PRAE).',
                'hacer': 'Formula un proyecto escolar de reciclaje, huerta escolar o eficiencia energética.',
                'ser': 'Liderazgo cívico y corresponsabilidad ambiental en la comunidad educativa.',
                'evidence': 'Propuesta de proyecto PRAE documentada con plan de acción y métricas de impacto.'
            }
        ]
    },
    'COL-BIO': {
        'competency': 'Análisis de la vida a nivel molecular, celular, organísmico y poblacional.',
        'domain': 'Biológico y Genético',
        'dimension': 'Dimensión Científica y Salud',
        'raps': [
            {
                'order': 1,
                'code': 'BIO-RAP1',
                'title': 'Biología Celular y Fisiología Molecular',
                'description': 'Explica los procesos de respiración, nutrición y síntesis de biomoléculas en la célula.',
                'indicator': 'Describe la estructura y función de los organelos celulares y el transporte a través de membranas.',
                'saber': 'ADN, ARN, síntesis proteica, glucólisis, ciclo de Krebs y transporte pasivo/activo.',
                'hacer': 'Observa e identifica células eucariotas y procariotas al microscopio óptico.',
                'ser': 'Paciencia y rigurosidad técnica en la preparación de placas y muestras biológicas.',
                'evidence': 'Álbum microscópico ilustrado con esquemas celulares y descripción de funciones.'
            },
            {
                'order': 2,
                'code': 'BIO-RAP2',
                'title': 'Genética Clásica y Molecular',
                'description': 'Resuelve problemas de herencia biológica aplicando las leyes mendelianas y genómica moderna.',
                'indicator': 'Construye cuadros de Punnett e interpreta árboles genealógicos familiares.',
                'saber': 'Genotipo, fenotipo, alelos dominantes y recesivos, mutaciones genéticas y biotecnología.',
                'hacer': 'Predice probabilidades fenotípicas y genotípicas en cruces monohíbridos y dihíbridos.',
                'ser': 'Reflexión ética sobre la manipulación genética, clonación y bioética.',
                'evidence': 'Taller de resolución de casos genéticos y debate sobre biotecnología aplicada.'
            },
            {
                'order': 3,
                'code': 'BIO-RAP3',
                'title': 'Evolución y Diversidad de los Seres Vivos',
                'description': 'Relaciona la selección natural con la biodiversidad y la adaptación biológica.',
                'indicator': 'Explica evidencias anatómicas, fósiles y moleculares de la teoría sintética de la evolución.',
                'saber': 'Teoría de Darwin-Wallace, aislamiento reproductivo, filogenia y taxonomía de reinos.',
                'hacer': 'Construye árboles filogenéticos sencillos e interpreta registros fósiles.',
                'ser': 'Respeto profundo por todas las formas de vida y su trayectoria evolutiva.',
                'evidence': 'Línea de tiempo evolutiva comparada o póster científico de biodiversidad colombiana.'
            }
        ]
    },
    'COL-FIS': {
        'competency': 'Modelación matemática de las leyes del universo físico y la mecánica clásica.',
        'domain': 'Físico-Matemático',
        'dimension': 'Pensamiento Científico e Ingeniería',
        'raps': [
            {
                'order': 1,
                'code': 'FIS-RAP1',
                'title': 'Cinemática y Dinámica Newtoniana',
                'description': 'Modela el movimiento rectilíneo, parabólico y circular aplicando las Leyes de Newton.',
                'indicator': 'Calcula variables de velocidad, aceleración y fuerza en situaciones mecánicas concretas.',
                'saber': 'MRU, MRUA, vectores de fuerza, diagramas de cuerpo libre (DCL), leyes de Newton.',
                'hacer': 'Traza diagramas vectoriales y resuelve sistemas de ecuaciones de movimiento.',
                'ser': 'Perseverancia en el análisis metódico de variables físicas.',
                'evidence': 'Práctica experimental de caída libre o plano inclinado con cálculo de error porcentual.'
            },
            {
                'order': 2,
                'code': 'FIS-RAP2',
                'title': 'Trabajo, Potencia y Conservación de la Energía',
                'description': 'Aplica el principio de conservación de la energía mecánica a sistemas cerrados.',
                'indicator': 'Determina la energía cinética y potencial en sistemas con y sin fricción.',
                'saber': 'Trabajo mecánico, energía cinética, potencial gravitacional y elástica, teorema trabajo-energía.',
                'hacer': 'Calcula la eficiencia energética en máquinas simples y prototipos mecánicos.',
                'ser': 'Conciencia sobre el consumo eficiente y sostenible de fuentes de energía.',
                'evidence': 'Prototipo de máquina simple (catapulta, montaña rusa en miniatura) con memoria física.'
            },
            {
                'order': 3,
                'code': 'FIS-RAP3',
                'title': 'Termodinámica, Fluidos y Fenómenos Ondulatorios',
                'description': 'Analiza el comportamiento de fluidos, calor, ondas sonoras y electromagnéticas.',
                'indicator': 'Aplica el principio de Pascal, Arquímedes y las leyes de gases ideales.',
                'saber': 'Presión hidrostática, principio de Bernouilli, calor latente, frecuencia y longitud de onda.',
                'hacer': 'Construye circuitos de fluidos o simula ondas mecánicas midiendo resonancia.',
                'ser': 'Curiosidad científica y espíritu inquisitivo ante fenómenos de la naturaleza.',
                'evidence': 'Informe experimental sobre prensa hidráulica o diapasón acústico.'
            }
        ]
    },
    'COL-QUI': {
        'competency': 'Comprensión estructural de la materia, transformaciones químicas y estequiometría.',
        'domain': 'Químico y Experimental',
        'dimension': 'Pensamiento Científico y Ambiental',
        'raps': [
            {
                'order': 1,
                'code': 'QUI-RAP1',
                'title': 'Estructura Atómica y Enlace Químico',
                'description': 'Relaciona la configuración electrónica con las propiedades periódicas y tipos de enlace.',
                'indicator': 'Determina el tipo de enlace (iónico, covalente, metálico) según electronegatividades.',
                'saber': 'Modelos atómicos, números cuánticos, tabla periódica, estructuras de Lewis.',
                'hacer': 'Dibuja geometrías moleculares y predice propiedades físicas de sustancias.',
                'ser': 'Atención a los detalles y capacidad de abstracción de modelos submicroscópicos.',
                'evidence': 'Cuadro comparativo de sustancias cotidianas y sus tipos de enlace con demostración de conductividad.'
            },
            {
                'order': 2,
                'code': 'QUI-RAP2',
                'title': 'Nomenclatura y Reacciones Químicas',
                'description': 'Formula compuestos inorgánicos y balancea ecuaciones químicas por diversos métodos.',
                'indicator': 'Clasifica reacciones químicas y balancea por tanteo y óxido-reducción.',
                'saber': 'Óxidos, hidróxidos, ácidos, sales, números de oxidación, leyes ponderales.',
                'hacer': 'Escribe y balancea reacciones químicas prediciendo productos de reacción.',
                'ser': 'Disciplina y rigurosidad en la aplicación de normas IUPAC.',
                'evidence': 'Guía de laboratorio de síntesis inorgánica con ecuaciones químicas balanceadas.'
            },
            {
                'order': 3,
                'code': 'QUI-RAP3',
                'title': 'Estequiometría y Soluciones Químicas',
                'description': 'Calcula cantidades de reactivos y productos en moles, gramos y volúmenes molares.',
                'indicator': 'Calcula reactivo límite, porcentaje de rendimiento y concentraciones molares de soluciones.',
                'saber': 'Mol, masa molar, reactivo límite, Molaridad, Normalidad, ppm.',
                'hacer': 'Prepara soluciones valoradas en el laboratorio utilizando material volumétrico.',
                'ser': 'Responsabilidad ambiental en el manejo y disposición final de reactivos químicos.',
                'evidence': 'Preparación real de una solución patrón con reporte de titulación ácido-base.'
            }
        ]
    },
    'COL-SOC': {
        'competency': 'Pensamiento social crítico, comprensión del espacio geográfico y convivencia democrática.',
        'domain': 'Social y Ciudadano',
        'dimension': 'Dimensión Histórica y Ciudadana',
        'raps': [
            {
                'order': 1,
                'code': 'SOC-RAP1',
                'title': 'Espacio Geográfico, Territorio y Población',
                'description': 'Analiza las dinámicas demográficas, urbanas y rurales y el uso del suelo en Colombia y el mundo.',
                'indicator': 'Interpreta mapas temáticos y pirámides poblacionales identificando problemáticas territoriales.',
                'saber': 'Geografía física y humana, cartografía, demografía, ordenamiento territorial.',
                'hacer': 'Elabora e interpreta cartografía social de su barrio o municipio identificando riesgos y recursos.',
                'ser': 'Sentido de pertenencia y valoración del patrimonio territorial y ambiental.',
                'evidence': 'Mapa de cartografía social comunitaria con diagnóstico de necesidades locales.'
            },
            {
                'order': 2,
                'code': 'SOC-RAP2',
                'title': 'Procesos Históricos y Transformaciones Sociales',
                'description': 'Comprende las causas y consecuencias de los grandes procesos políticos y económicos mundiales y nacionales.',
                'indicator': 'Contrasta diversas perspectivas historiográficas sobre un mismo evento histórico.',
                'saber': 'Revoluciones modernas, colonialismo, guerras mundiales, historia de Colombia en el siglo XIX y XX.',
                'hacer': 'Redacta ensayos históricos analizando fuentes primarias y secundarias.',
                'ser': 'Pensamiento crítico frente a versiones hegemónicas del pasado histórico.',
                'evidence': 'Línea de tiempo analítica con contraste de fuentes documentales históricas.'
            },
            {
                'order': 3,
                'code': 'SOC-RAP3',
                'title': 'Competencias Ciudadanas y Derechos Humanos',
                'description': 'Ejerce la ciudadanía democrática reconociendo la pluralidad y la defensa de los DDHH.',
                'indicator': 'Propone soluciones pacíficas a conflictos basadas en el respeto irrestricto de los DDHH.',
                'saber': 'Declaración Universal de DDHH, DIH, mecanismos de participación democrática.',
                'hacer': 'Participa en simulaciones de foros ciudadanos, modelos ONU y deliberación pública.',
                'ser': 'Empatía, solidaridad con poblaciones vulnerables y rechazo absoluto a la violencia.',
                'evidence': 'Simulación de audiencia pública o proyecto de mediación escolar de conflictos.'
            }
        ]
    },
    'COL-HIS': {
        'competency': 'Investigación histórica, memoria colectiva y análisis de coyunturas sociopolíticas.',
        'domain': 'Historiográfico',
        'dimension': 'Dimensión Histórica y Crítica',
        'raps': [
            {
                'order': 1,
                'code': 'HIS-RAP1',
                'title': 'Metodología Historiográfica y Manejo de Fuentes',
                'description': 'Distingue fuentes primarias de secundarias aplicando crítica histórica.',
                'indicator': 'Evalúa la veracidad, contexto e intención de testimonios y archivos históricos.',
                'saber': 'Concepto de fuente, archivo, memoria histórica, heurística y hermenéutica histórica.',
                'hacer': 'Entrevista a testigos de eventos contemporáneos y analiza recortes de prensa antiguos.',
                'ser': 'Compromiso con la verdad histórica y el respeto a la memoria de las víctimas.',
                'evidence': 'Informe de historia oral con transcripción de entrevista y análisis contextual.'
            },
            {
                'order': 2,
                'code': 'HIS-RAP2',
                'title': 'Historia Republicana de Colombia y Conflicto Armado',
                'description': 'Explica los orígenes, desarrollo y caminos hacia la paz del conflicto armado colombiano.',
                'indicator': 'Identifica los actores, causas estructurales y acuerdos de paz en la historia reciente.',
                'saber': 'Violencia bipartidista, Frente Nacional, insurgencias, paramilitarismo, Acuerdo de Paz de 2016.',
                'hacer': 'Construye matrices comparativas de períodos presidenciales y procesos de paz.',
                'ser': 'Vocación de paz, reconciliación y no repetición de la violencia.',
                'evidence': 'Páginas de un libro de memoria colectiva escolar sobre la paz en Colombia.'
            }
        ]
    },
    'COL-CON': {
        'competency': 'Comprensión y ejercicio práctico de la Constitución Política y la estructura del Estado.',
        'domain': 'Jurídico-Ciudadano',
        'dimension': 'Dimensión Constitucional y Ético-Política',
        'raps': [
            {
                'order': 1,
                'code': 'CON-RAP1',
                'title': 'Derechos Fundamentales y Acciones Constitucionales',
                'description': 'Conoce y redacta acciones de tutela y derechos de petición para la defensa de derechos civiles.',
                'indicator': 'Diligencia correctamente un derecho de petición y sustenta la pertinencia de una tutela.',
                'saber': 'Constitución de 1991, derechos de 1a, 2a y 3a generación, bloque de constitucionalidad.',
                'hacer': 'Redacta un derecho de petición y una acción de tutela según casos hipotéticos reales.',
                'ser': 'Empoderamiento cívico y respeto a la legalidad y al debido proceso.',
                'evidence': 'Minuta jurídica redactada de Derecho de Petición y Acción de Tutela con sustentación.'
            },
            {
                'order': 2,
                'code': 'CON-RAP2',
                'title': 'Estructura del Estado Colombiano y Mecanismos de Participación',
                'description': 'Diferencia las ramas del poder público, órganos de control y mecanismos de participación ciudadana.',
                'indicator': 'Explica las funciones del ejecutivo, legislativo, judicial y entes de control fiscal y disciplinario.',
                'saber': 'Ramas del poder público, Fiscalía, Procuraduría, Contraloría, Defensoría, referendo, plebiscito, voto.',
                'hacer': 'Diseña un flujograma de trámite de una ley en el Congreso de la República.',
                'ser': 'Interés activo en la rendición de cuentas y vigilancia transparente de los recursos públicos.',
                'evidence': 'Simulación de debate legislativo o juicio de control político con roles asignados.'
            }
        ]
    },
    'COL-ETI': {
        'competency': 'Deliberación moral, construcción de autonomía ética y convivencia democrática.',
        'domain': 'Axiológico y Socio-Emocional',
        'dimension': 'Dimensión Ética, Moral y Afectiva',
        'raps': [
            {
                'order': 1,
                'code': 'ETI-RAP1',
                'title': 'Dilemas Morales y Autonomía Ética',
                'description': 'Analiza situaciones dilemáticas cotidianas fundamentando juicios morales autónomos.',
                'indicator': 'Distingue entre normas morales, sociales y jurídicas asumiendo consecuencias de sus actos.',
                'saber': 'Teorías éticas (deontología, utilitarismo, ética del cuidado), dilemas morales.',
                'hacer': 'Participa en círculos dialógicos analizando casos reales de conflicto ético.',
                'ser': 'Honestidad, coherencia personal, integridad y responsabilidad por los propios actos.',
                'evidence': 'Diario reflexivo personal con resolución argumentada de tres dilemas morales.'
            },
            {
                'order': 2,
                'code': 'ETI-RAP2',
                'title': 'Cultura de Paz, Empatía y Convivencia Escolar',
                'description': 'Promueve ambientes de respeto, inclusión y resolución pacífica de diferencias interpersonales.',
                'indicator': 'Aplica técnicas de asertividad y mediación de pares ante desacuerdos en el aula.',
                'saber': 'Habilidades socioemocionales, comunicación asertiva, empatía, pactos de convivencia.',
                'hacer': 'Ejerce como mediador escolar aplicando protocolos de concertación no punitiva.',
                'ser': 'Inclusión, valoración de la diversidad de género, etnia y pensamiento.',
                'evidence': 'Pacto de aula consensuado y ejecutado con evidencias de mediación pacífica.'
            }
        ]
    },
    'COL-REL': {
        'competency': 'Reflexión trascendente, espiritualidad y diálogo interreligioso respetuoso.',
        'domain': 'Espiritual y Fenomenológico',
        'dimension': 'Dimensión Espiritual y Antropológica',
        'raps': [
            {
                'order': 1,
                'code': 'REL-RAP1',
                'title': 'Fenomenología Religiosa y Grandes Tradiciones Espirituales',
                'description': 'Comprende el fenómeno religioso en las culturas mundiales y el respeto a la libertad de cultos.',
                'indicator': 'Compara los principios éticos compartidos por las principales tradiciones religiosas de la humanidad.',
                'saber': 'Judaísmo, Cristianismo, Islam, Hinduismo, Budismo, cosmovisiones indígenas ancestrales.',
                'hacer': 'Elabora cuadros comparativos de textos sagrados, símbolos y ritos universales.',
                'ser': 'Tolerancia ecuménica y respeto por las convicciones religiosas ajenas.',
                'evidence': 'Cuadro comparativo interreligioso con ensayo sobre la libertad de culto en Colombia.'
            }
        ]
    },
    'COL-EFI': {
        'competency': 'Desarrollo motriz, condición física para la salud y trabajo colaborativo deportivo.',
        'domain': 'Motriz y Biofísico',
        'dimension': 'Dimensión Corporal y Hábitos Saludables',
        'raps': [
            {
                'order': 1,
                'code': 'EFI-RAP1',
                'title': 'Condición Física, Resistencia y Salud Corporal',
                'description': 'Evalúa y mejora sus capacidades físicas condicionales mediante planes de entrenamiento adaptado.',
                'indicator': 'Realiza pruebas de resistencia cardiovascular, fuerza y flexibilidad registrando sus progresos.',
                'saber': 'Frecuencia cardíaca, gasto calórico, capacidades condicionales y coordinativas, hidratación.',
                'hacer': 'Ejecuta circuitos funcionales y rutinas de calentamiento y estiramiento correctos.',
                'ser': 'Disciplina, autocuidado y constancia en la práctica de actividad física regular.',
                'evidence': 'Ficha antropométrica y test de Cooper / Course-Navette con plan individual de mejora.'
            },
            {
                'order': 2,
                'code': 'EFI-RAP2',
                'title': 'Fundamentos Técnicos y Tácticos Deportivos',
                'description': 'Domina fundamentos técnicos en deportes individuales y de conjunto respetando el juego limpio.',
                'indicator': 'Ejecuta pases, lanzamientos, recepciones y desplazamientos tácticos en el terreno de juego.',
                'saber': 'Reglamento oficial deportivo (fútbol, voleibol, baloncesto, atletismo), táctica básica.',
                'hacer': 'Aplica esquemas de ataque y defensa cooperativa en partidos escolares.',
                'ser': 'Espíritu deportivo, juego limpio (fair play), respeto a rivales y jueces arbitrales.',
                'evidence': 'Evaluación práctica de destreza motriz y desempeño táctico en torneo interclases.'
            }
        ]
    },
    'COL-ART': {
        'competency': 'Sensibilidad estética, expresión creativa visual y apreciación del patrimonio artístico.',
        'domain': 'Estético y Visual',
        'dimension': 'Dimensión Artística y Creativa',
        'raps': [
            {
                'order': 1,
                'code': 'ART-RAP1',
                'title': 'Elementos del Lenguaje Visual y Composición Plástica',
                'description': 'Aplica punto, línea, plano, color, textura y perspectiva en creaciones bidimensionales.',
                'indicator': 'Combina gamas cromáticas y puntos de fuga en obras pictóricas y dibujos estructurados.',
                'saber': 'Teoría del color, círculo cromático, claroscuro, leyes de la Gestalt, perspectiva cónica.',
                'hacer': 'Mezcla pigmentos y aplica técnicas secas y húmedas (lápiz, carboncillo, témpera, acrílico).',
                'ser': 'Creatividad, originalidad y paciencia en los acabados plásticos.',
                'evidence': 'Lámina de composición cromática con aplicación de perspectiva a dos puntos de fuga.'
            },
            {
                'order': 2,
                'code': 'ART-RAP2',
                'title': 'Apreciación del Arte Colombiano e Historia Visual',
                'description': 'Analiza obras de artistas emblemáticos interpretando sus contextos estéticos y sociales.',
                'indicator': 'Compara propuestas estéticas de diferentes épocas y corrientes del arte plástico.',
                'saber': 'Arte precolombino, colonial, republicano y contemporáneo (Botero, Negret, Grau, Salcedo).',
                'hacer': 'Diseña una curaduría virtual o física de una exhibición artística temática.',
                'ser': 'Sensibilidad y aprecio por las expresiones culturales y la identidad plástica nacional.',
                'evidence': 'Póster de curaduría artística o reinterpretación plástica de una obra colombiana.'
            }
        ]
    },
    'COL-MUS': {
        'competency': 'Percepción auditiva, expresión vocal e instrumental y apreciación del ritmo.',
        'domain': 'Auditivo y Musical',
        'dimension': 'Dimensión Artística y Sonora',
        'raps': [
            {
                'order': 1,
                'code': 'MUS-RAP1',
                'title': 'Lectoescritura Musical y Percepción Sonora',
                'description': 'Lee e interpreta partituras básicas con figuras de tiempo, notas y compases en pentagrama.',
                'indicator': 'Solfea rítmicamente y entona intervalos melódicos sencillos en clave de sol.',
                'saber': 'Pentagrama, figuras rítmicas (redonda, blanca, negra, corchea), silencios, escalas mayores.',
                'hacer': 'Transcribe dictados rítmicos sencillos y ejecuta percusión corporal coordinada.',
                'ser': 'Concentración, afinación auditiva y escucha activa del entorno acústico.',
                'evidence': 'Lectura rítmico-melódica individual grabada o ejecutada ante el grupo.'
            },
            {
                'order': 2,
                'code': 'MUS-RAP2',
                'title': 'Práctica Instrumental, Vocal y Ensamble Colectivo',
                'description': 'Interpreta obras del folclor colombiano e internacional en ensamble vocal e instrumental.',
                'indicator': 'Toca un instrumento escolar (flauta dulce, percusión, teclado) o canta en coro armónico.',
                'saber': 'Técnica de emisión vocal, respiración diafragmática, digitación instrumental, ritmos folclóricos.',
                'hacer': 'Ensambla piezas musicales a dos o más voces instrumentales manteniendo el tempo constante.',
                'ser': 'Coordinación colectiva, puntualidad y sincronía en el trabajo de ensamble musical.',
                'evidence': 'Presentación en ensamble coral o instrumental de una pieza folclórica colombiana.'
            }
        ]
    },
    'COL-ING': {
        'competency': 'Comunicación en lengua inglesa según estándares del MCER (A1 a B1+).',
        'domain': 'Bilingüe y Comunicativo',
        'dimension': 'Dimensión Comunicativa Global',
        'raps': [
            {
                'order': 1,
                'code': 'ING-RAP1',
                'title': 'Comprensión Auditiva y Lectora en Inglés (Listening & Reading)',
                'description': 'Comprende información explícita e implícita en textos orales y escritos en inglés.',
                'indicator': 'Extrae ideas principales y detalles específicos de audios y lecturas temáticas en inglés.',
                'saber': 'Vocabulario contextualizado, tiempos verbales (present, past, future), conectores en inglés.',
                'hacer': 'Responde preguntas de comprensión literal e inferencial tras escuchar audios nativos.',
                'ser': 'Pérdida del miedo al error y disposición positiva hacia el aprendizaje de una segunda lengua.',
                'evidence': 'Prueba de comprensión auditiva y lectura con resumen escrito en lengua inglesa.'
            },
            {
                'order': 2,
                'code': 'ING-RAP2',
                'title': 'Producción Escrita en Inglés (Writing)',
                'description': 'Redacta párrafos estructurados, correos y ensayos cortos con adecuada gramática y léxico.',
                'indicator': 'Produce textos de 150-250 palabras organizados con coherencia y cohesión básica.',
                'saber': 'Estructura del párrafo en inglés (topic sentence, supporting sentences, conclusion), puntuación.',
                'hacer': 'Redacta descripciones personales, anécdotas en pasado y opiniones sobre temas juveniles.',
                'ser': 'Cuidado con la ortografía y uso de diccionarios bilingües como herramienta de consulta.',
                'evidence': 'Composición escrita de dos párrafos revisada bajo rúbrica de writing.'
            },
            {
                'order': 3,
                'code': 'ING-RAP3',
                'title': 'Interacción y Fluidez Oral en Inglés (Speaking)',
                'description': 'Sostiene conversaciones sencillas y realiza exposiciones orales sobre temas cotidianos.',
                'indicator': 'Participa en diálogos fluidos respondiendo preguntas espontáneas con entonación adecuada.',
                'saber': 'Pronunciación estándar, fonemas clave, expresiones idiomáticas cotidianas, conectores orales.',
                'hacer': 'Realiza monólogos de 2 minutos y role-plays en parejas simulando situaciones reales.',
                'ser': 'Seguridad personal, espontaneidad y entusiasmo al comunicarse en otro idioma.',
                'evidence': 'Video o grabación de conversación en pareja (role-play) evaluado por rúbrica de speaking.'
            }
        ]
    },
    'COL-TIC': {
        'competency': 'Pensamiento computacional, alfabetización digital avanzada y uso ético de la tecnología.',
        'domain': 'Tecnológico y Digital',
        'dimension': 'Dimensión Digital e Innovación',
        'raps': [
            {
                'order': 1,
                'code': 'TIC-RAP1',
                'title': 'Pensamiento Computacional, Algoritmos y Programación',
                'description': 'Diseña secuencias lógicas y escribe código para resolver problemas computacionales.',
                'indicator': 'Crea diagramas de flujo y programas funcionales utilizando variables, condicionales y ciclos.',
                'saber': 'Algoritmos, estructuras de control (if/else, for, while), funciones, lenguajes visuales o de texto.',
                'hacer': 'Programa un software o juego educativo en Scratch, Python o JavaScript con lógica estructurada.',
                'ser': 'Pensamiento analítico, depuración paciente de errores y perseverancia ante bugs.',
                'evidence': 'Proyecto de software ejecutable con repositorio y documentación del código fuente.'
            },
            {
                'order': 2,
                'code': 'TIC-RAP2',
                'title': 'Gestión de Información, Bases de Datos y Herramientas Ofimáticas',
                'description': 'Procesa y modela datos mediante hojas de cálculo avanzadas y bases de datos relacionales.',
                'indicator': 'Aplica fórmulas lógicas, tablas dinámicas y macros básicas en la resolución de problemas de gestión.',
                'saber': 'Fórmulas avanzadas (BUSCARV, SI), tablas dinámicas, diseño de tablas relacionales en SQL.',
                'hacer': 'Diseña un tablero de control (dashboard) con gráficos interactivos y filtros dinámicos.',
                'ser': 'Rigor en la validación de datos y confidencialidad en el tratamiento de información sensible.',
                'evidence': 'Libro de cálculo con modelo de datos, macros o fórmulas y dashboard ejecutivo funcional.'
            },
            {
                'order': 3,
                'code': 'TIC-RAP3',
                'title': 'Ciberseguridad, Ciudadanía Digital y Ética en la IA',
                'description': 'Aplica normas de ciberseguridad, protección de datos y uso ético de inteligencia artificial.',
                'indicator': 'Identifica amenazas informáticas (phishing, malware) y cita fuentes digitales con rigor ético.',
                'saber': 'Huella digital, privacidad en redes sociales, derechos de autor, licencias Creative Commons, sesgos de IA.',
                'hacer': 'Configura parámetros de seguridad y redacta una guía escolar de buen uso de tecnologías emergentes.',
                'ser': 'Comportamiento ético en internet, respeto a la propiedad intelectual y empatía digital.',
                'evidence': 'Campaña multimedia escolar de ciberseguridad o decálogo de uso ético de la IA.'
            }
        ]
    },
    'COL-ECO': {
        'competency': 'Comprensión macro y microeconómica, finanzas personales y políticas de desarrollo.',
        'domain': 'Económico y Político',
        'dimension': 'Dimensión Económica y Toma de Decisiones',
        'raps': [
            {
                'order': 1,
                'code': 'ECO-RAP1',
                'title': 'Principios Económicos, Mercados y Finanzas Personales',
                'description': 'Analiza el funcionamiento de los mercados, la oferta y demanda y la gestión del presupuesto.',
                'indicator': 'Elabora un presupuesto personal y familiar calculando ahorro, inversión y endeudamiento responsable.',
                'saber': 'Oferta, demanda, inflación, tasa de interés, costo de oportunidad, presupuesto y crédito.',
                'hacer': 'Diseña un simulador de presupuesto personal con metas de ahorro a corto y mediano plazo.',
                'ser': 'Responsabilidad financiera y consumo consciente y solidario.',
                'evidence': 'Plan financiero personal a 12 meses con proyección de ingresos, gastos y ahorro.'
            },
            {
                'order': 2,
                'code': 'ECO-RAP2',
                'title': 'Políticas Públicas, Modelos de Desarrollo y Globalización',
                'description': 'Evalúa los modelos de desarrollo económico y su impacto en la equidad social y el empleo.',
                'indicator': 'Contrasta políticas fiscales y monetarias y su efecto en la calidad de vida ciudadana.',
                'saber': 'PIB, desempleo, política fiscal, comercio internacional, sostenibilidad y desarrollo humano (IDH).',
                'hacer': 'Redacta un informe comparativo entre el crecimiento económico y los índices de pobreza.',
                'ser': 'Sensibilidad frente a la inequidad económica y compromiso con el desarrollo inclusivo.',
                'evidence': 'Ensayo analítico sobre las consecuencias socioeconómicas de la inflación en Colombia.'
            }
        ]
    },
    'COL-FIL': {
        'competency': 'Argumentación crítica, reflexión ontológica, epistemológica y ética filosófica.',
        'domain': 'Filosófico y Crítico',
        'dimension': 'Dimensión Filosófica y Metafísica',
        'raps': [
            {
                'order': 1,
                'code': 'FIL-RAP1',
                'title': 'Epistemología, Lógica y Filosofía del Conocimiento',
                'description': 'Cuestiona los fundamentos del conocimiento humano diferenciando doxa de episteme.',
                'indicator': 'Construye silogismos lógicos válidos e identifica falacias argumentativas en discursos cotidianos.',
                'saber': 'Racionalismo, empirismo, idealismo trascendental, lógica formal, falacias informales.',
                'hacer': 'Analiza un discurso político o mediático identificando falacias y sesgos cognitivos.',
                'ser': 'Amor por la verdad, honestidad intelectual y tolerancia ante la incertidumbre.',
                'evidence': 'Matriz de análisis crítico de un discurso público con desmontaje de falacias argumentativas.'
            },
            {
                'order': 2,
                'code': 'FIL-RAP2',
                'title': 'Antropología Filosófica, Sentido de la Vida y Ética Contemporánea',
                'description': 'Reflexiona sobre la existencia humana, la libertad, el poder y la justicia en el mundo contemporáneo.',
                'indicator': 'Sustenta ensayos filosóficos confrontando autores clásicos y contemporáneos con su realidad.',
                'saber': 'Existencialismo, teoría crítica, biopolítica, nihilismo, ética del otro (Levinas, Foucault, Sartre).',
                'hacer': 'Escribe una disertación filosófica fundamentando una respuesta a una pregunta existencial.',
                'ser': 'Profundidad de pensamiento, autoexamen socrático y apertura mental.',
                'evidence': 'Disertación filosófica escrita y defendida en simposio o café filosófico escolar.'
            }
        ]
    },
}

def seed_raps():
    total_subjects = 0
    total_raps = 0

    # Limpiar SubjectNorms previos para recargar el esquema completo con RAPs
    SubjectNorm.objects.all().delete()

    for code, data in RAP_CURRICULAR_DATA.items():
        s = Subject.objects.filter(code=code).first()
        if not s:
            print(f"Warning: Subject with code {code} not found.")
            continue

        total_subjects += 1
        for r in data['raps']:
            SubjectNorm.objects.create(
                subject=s,
                code=r['code'],
                title=r['title'],
                description=r['description'],
                competency=data['competency'],
                domain=data['domain'],
                dimension=data['dimension'],
                indicator=r['indicator'],
                saber=r['saber'],
                hacer=r['hacer'],
                ser=r['ser'],
                evidence=r['evidence'],
                order=r['order']
            )
            total_raps += 1

    print(f"[OK] Pobladas exitosamente {total_subjects} asignaturas con {total_raps} RAPs completos (Saber, Hacer, Ser y Evidencias).")

if __name__ == '__main__':
    seed_raps()
