# GUIÓN DE EXPOSICIÓN — FASE 1: MARCO CONCEPTUAL
## Gestión de Configuración del Software y Calidad (ISO/IEC 25010 · IEEE 730 · IEEE 828 · CMMI)
### Proyecto ACADEMIX — SENA ADSO Ficha 3173430

---

## PORTADA DE LA PRESENTACIÓN

**Título:** Marco Normativo de Calidad y Gestión de Configuración del Software  
**Subtítulo:** Investigación Fase 1 — Proyecto Formativo ACADEMIX  
**Institución:** SENA — Centro de Servicios Empresariales y Turismo  
**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)  
**Ficha:** 3173430  
**Fecha:** Noviembre 2026  

---

## TABLA DE DISTRIBUCIÓN DE EXPOSITORES

| # Diapositiva | Título | Expositor | Tiempo |
|---|---|---|---|
| D1 | Portada y Objetivo | Expositor 1 | 1 min |
| D2 | ¿Qué es ISO/IEC 25010 y SQuaRE? | Expositor 1 | 2 min |
| D3 | Las 8 Características de Calidad | Expositor 1 | 2.5 min |
| D4 | Métricas ISO/IEC 25010 en ACADEMIX | Expositor 1 | 2 min |
| D5 | IEEE 730 — Aseguramiento de Calidad (SQA) | Expositor 2 | 2 min |
| D6 | Anatomía del Plan de Calidad (SQAP) | Expositor 2 | 2.5 min |
| D7 | Marco Regulatorio Colombiano | Expositor 2 | 2 min |
| D8 | SCM — IEEE 828 y Procesos Nucleares | Expositor 3 | 2 min |
| D9 | CMMI-DEV — Área de Práctica CM | Expositor 3 | 2 min |
| D10 | GitFlow, Baselines y Control de Cambios | Expositor 3 | 2 min |
| D11 | Conclusiones y Relación con ACADEMIX | Todo el equipo | 1.5 min |
| D12 | Banco de Preguntas — Apertura al Instructor | Todo el equipo | 1 min |
| **TOTAL** | | | **~22 min** |

---

---

## DIAPOSITIVA 1 — PORTADA Y OBJETIVO

### Contenido visual sugerido
- Logo SENA + Logo ACADEMIX
- Título y subtítulo
- Integrantes del equipo, Ficha 3173430, Fecha
- Frase de motivación: *"La calidad no es un acto, es un hábito." — Aristóteles*

### Speech — Expositor 1

> "Buenos días / tardes. Mi nombre es [Nombre], soy parte del equipo de desarrollo del proyecto ACADEMIX de la ficha 3173430.
>
> En esta presentación vamos a exponer los resultados de nuestra investigación de la Fase 1 del trabajo de Gestión de Configuración del Software. El objetivo central de esta investigación fue comprender y documentar los marcos normativos internacionales y nacionales que rigen la calidad del software: la norma ISO/IEC 25010, el estándar IEEE 730, el estándar de gestión de configuración IEEE 828, el modelo de madurez CMMI-DEV, y la normativa colombiana vigente.
>
> Todo esto lo aplicamos y conectamos directamente con nuestro proyecto formativo ACADEMIX, que es una plataforma web de gestión escolar desarrollada en Django, actualmente en uso institucional.
>
> Vamos a dividir la exposición en tres bloques: primero, el modelo de calidad del producto; segundo, el aseguramiento de calidad y la normativa colombiana; y tercero, la gestión de configuración del software. Comencemos."

---

## DIAPOSITIVA 2 — ¿QUÉ ES ISO/IEC 25010 Y SQUARE?

### Contenido visual sugerido
- Diagrama de la familia SQuaRE (25000–25099)
- Línea de tiempo: ISO 9126 (2001) → ISO/IEC 25010:2011 → ISO/IEC 25010:2023
- Cuadro: 5 divisiones de la serie 25000
- Definición de "Calidad del Producto de Software"

### Speech — Expositor 1

> "Para entender ISO/IEC 25010, primero hay que ubicarla dentro de su familia: la serie SQuaRE, que son las siglas de *Systems and Software Quality Requirements and Evaluation*. Es una familia de más de 20 normas, organizadas en cinco divisiones:
>
> Primera, la división de Gestión de Calidad, normas 25000 a 25010, que define los conceptos y modelos generales. Segunda, la división de Requisitos de Calidad, normas 25020 a 25030, que guía cómo especificar los requisitos de calidad. Tercera, la división de Evaluación de Calidad, normas 25040 a 25050, que define cómo evaluar un producto. Cuarta, los Modelos de Calidad, especialmente nuestra norma: la 25010. Y quinta, la división de Herramientas de Evaluación, norma 25060 en adelante.
>
> La ISO/IEC 25010 tiene dos modelos: el Modelo de Calidad del Producto, que es el que más trabajamos nosotros, y el Modelo de Calidad en Uso, que evalúa la experiencia del usuario final en contexto real.
>
> ¿Por qué usamos esta norma? Porque nos da un lenguaje común y medible para hablar de calidad. En vez de decir 'el software funciona bien', podemos decir 'tiene un 97% de disponibilidad y un MTBF de 48 horas'. Eso es lo que busca SQuaRE: convertir la calidad en algo que se puede medir, verificar y mejorar."

---

## DIAPOSITIVA 3 — LAS 8 CARACTERÍSTICAS DE CALIDAD DEL PRODUCTO

### Contenido visual sugerido
- Tabla o rueda con las 8 características + sus subcaracterísticas principales
- Destacar con color las 4 que aplica ACADEMIX: Usabilidad, Seguridad, Fiabilidad, Mantenibilidad

| # | Característica | Subcaracterísticas clave |
|---|---|---|
| 1 | Adecuación Funcional | Completitud, Corrección, Pertinencia |
| 2 | Eficiencia de Desempeño | Comportamiento temporal, Uso de recursos |
| 3 | Compatibilidad | Coexistencia, Interoperabilidad |
| **4** | **Usabilidad** | **Reconocibilidad, Aprendizabilidad, Operabilidad, Accesibilidad** |
| **5** | **Fiabilidad** | **Madurez, Disponibilidad, Tolerancia a fallos, Recuperabilidad** |
| **6** | **Seguridad** | **Confidencialidad, Integridad, No repudio, Autenticidad, Trazabilidad** |
| **7** | **Mantenibilidad** | **Modularidad, Reusabilidad, Analizabilidad, Modificabilidad, Capacidad de prueba** |
| 8 | Portabilidad | Adaptabilidad, Instalabilidad, Reemplazabilidad |

### Speech — Expositor 1

> "ISO/IEC 25010 define ocho características principales para evaluar la calidad de un producto de software. Voy a repasarlas brevemente:
>
> La Adecuación Funcional pregunta: ¿el software hace lo que debe hacer? ¿Hace todo lo que prometió? ¿Lo hace correctamente?
>
> La Eficiencia de Desempeño evalúa qué tan rápido responde y qué tan eficientemente usa los recursos del servidor.
>
> La Compatibilidad analiza si puede coexistir con otros sistemas e intercambiar información.
>
> La Usabilidad pregunta: ¿el usuario puede aprender a usarlo fácilmente? ¿Es accesible para personas con discapacidad?
>
> La Fiabilidad mide qué tan estable es el sistema bajo carga real y cuánto tiempo funciona sin fallar.
>
> La Seguridad cubre confidencialidad de datos, integridad, autenticidad de usuarios y trazabilidad de acciones.
>
> La Mantenibilidad evalúa qué tan fácil es para un desarrollador entender, modificar y probar el código.
>
> Y finalmente, la Portabilidad analiza si el sistema puede desplegarse en diferentes entornos sin problemas.
>
> Para ACADEMIX seleccionamos cuatro de estas características — las que están resaltadas en la tabla — porque son las más críticas para un sistema escolar que maneja datos de menores de edad y que debe estar disponible durante el año lectivo."

---

## DIAPOSITIVA 4 — MÉTRICAS ISO/IEC 25010 APLICADAS A ACADEMIX

### Contenido visual sugerido
- Tabla de 4 filas: Característica | Métrica/Fórmula | Resultado obtenido | Estado

| Característica | Métrica | Fórmula | Resultado | Estado |
|---|---|---|---|---|
| Fiabilidad (Disponibilidad) | Uptime Render | (T_total − T_caído) / T_total × 100% | 99.1% | ✅ OK |
| Seguridad (Autenticidad) | Cobertura Hash | Usuarios con hash Argon2/PBKDF2 / Total | 100% | ✅ OK |
| Usabilidad (Accesibilidad) | ARIA en errores | Alerts con aria-live / Total alerts críticos | 40% | ⚠️ Brecha |
| Mantenibilidad (Modularidad) | Acoplamiento vistas | Líneas en views.py > 200 | 1000+ líneas | ⚠️ Brecha |

### Speech — Expositor 1

> "Esta diapositiva es clave porque muestra cómo pasamos de la teoría a los números reales de nuestro proyecto.
>
> Para la Fiabilidad, medimos la disponibilidad del servidor Render durante el último mes usando la fórmula estándar: tiempo total menos tiempo caído, dividido entre tiempo total, por cien. El resultado fue 99.1%, lo cual está dentro del umbral aceptable para un sistema institucional.
>
> Para la Seguridad, verificamos que el 100% de los usuarios en base de datos tienen contraseñas hasheadas con Argon2id o PBKDF2, que son los algoritmos que Django usa por defecto. Eso es un punto fuerte de ACADEMIX.
>
> Para la Usabilidad y Accesibilidad, revisamos el template de login y encontramos que solo el 40% de los mensajes de error críticos tienen atributos ARIA correctos. Esto viola la Resolución 1519 de 2020 de MinTIC, que exige accesibilidad WCAG 2.1 nivel AA en plataformas de servicios públicos. Esto lo registramos como hallazgo HAL-02 en nuestra auditoría.
>
> Para la Mantenibilidad, encontramos que el archivo views.py del módulo de autenticación tiene más de mil líneas de código, lo cual indica un problema de modularidad conocido como 'vista gorda'. Esto se documentó como observación de mejora HAL-04."

---

## DIAPOSITIVA 5 — IEEE 730: ASEGURAMIENTO DE CALIDAD DEL SOFTWARE (SQA)

### Contenido visual sugerido
- Logo IEEE + número de norma
- Diagrama comparativo: SQA (preventivo) vs. Testing (reactivo)
- Frase clave: *"SQA no encuentra bugs — los previene desde el proceso"*

### Speech — Expositor 2

> "Muy buenos días. Soy [Nombre]. A partir de aquí voy a presentar el segundo bloque de nuestra investigación: el aseguramiento de calidad y la normativa colombiana.
>
> La IEEE 730, o *Standard for Software Quality Assurance Processes*, es el estándar del Instituto de Ingenieros Eléctricos y Electrónicos para aseguramiento de calidad de software. Fue actualizado en 2014 y es el referente global para crear Planes de Calidad de Software, conocidos como SQAP por sus siglas en inglés.
>
> La distinción más importante que debemos entender es la diferencia entre SQA y Testing. El Testing es reactivo: ejecuta el software para encontrar errores que ya existen. El SQA es preventivo: define, desde antes de escribir la primera línea de código, qué procesos, estándares, revisiones y auditorías se deben seguir para que los errores no lleguen a existir.
>
> Dicho de otro modo: el Testing le pregunta al software '¿estás funcionando bien?' El SQA le pregunta al equipo de desarrollo '¿estamos trabajando bien?'
>
> IEEE 730 establece que el SQA debe ser un proceso sistemático y planificado que cubre todo el ciclo de vida del software: desde los requisitos hasta el mantenimiento. No es una actividad de una sola persona — es una responsabilidad de todo el equipo."

---

## DIAPOSITIVA 6 — ANATOMÍA DEL PLAN DE CALIDAD (SQAP)

### Contenido visual sugerido
- Lista numerada de las 10 secciones del SQAP
- Tabla: Sección del SQAP → Equivalente en ACADEMIX

| # | Sección IEEE 730 | En ACADEMIX |
|---|---|---|
| 1 | Propósito y alcance | Sistema escolar Django, módulos activos |
| 2 | Documentos de referencia | ISO 25010, IEEE 828, NTC-ISO/IEC 25010 ICONTEC |
| 3 | Gestión del SQA | Roles: Tech Lead, QA, Dev Team |
| 4 | Documentación SQA | Informe de auditoría, matriz de calidad, checklist |
| 5 | Estándares de código | PEP 8, naming conventions Django |
| 6 | Revisiones e inspecciones | Code Review en PR, checklist de fusión |
| 7 | Pruebas | django.test, pytest, Selenium (propuesto) |
| 8 | Reportes de problemas | Formato CR-ACAD-2026-00X |
| 9 | Herramientas y métodos | Git, GitHub Actions, Black, Flake8 |
| 10 | Gestión de riesgos | Tabla de riesgos técnicos (HAL-01 a HAL-04) |

### Speech — Expositor 2

> "IEEE 730 define que un Plan de Calidad de Software debe tener al menos diez secciones. Vamos a verlas aplicadas a ACADEMIX:
>
> La sección uno define el propósito: nuestro SQAP cubre la plataforma ACADEMIX, específicamente los módulos de autenticación, boletines, asistencia y carga masiva.
>
> La sección dos lista los documentos de referencia: ISO/IEC 25010, IEEE 828, y en el contexto colombiano, la NTC-ISO/IEC 25010 adoptada por ICONTEC.
>
> La sección tres define la gestión del SQA: quién es responsable de qué. En ACADEMIX el rol de Tech Lead asume las funciones de CCB, el Comité de Control de Cambios.
>
> Las secciones cuatro a diez cubren la documentación generada, los estándares de código que seguimos — PEP 8 y las convenciones de Django —, las revisiones de código que hacemos antes de cada merge, las pruebas automatizadas con django.test, el formato oficial de reporte de cambios, las herramientas como Git y GitHub Actions, y la gestión de riesgos técnicos que documentamos en nuestra auditoría.
>
> Lo importante es que el SQAP no es un documento que se crea una sola vez. Es un documento vivo que se actualiza con cada sprint y con cada hallazgo encontrado."

---

## DIAPOSITIVA 7 — MARCO REGULATORIO COLOMBIANO

### Contenido visual sugerido
- Mapa de Colombia con íconos representando: MinTIC, SIC, iNNpulsa, ICONTEC, colCERT
- Tabla de normas con nombre, entidad y aplicación a ACADEMIX

| Norma / Entidad | Tipo | Aplicación en ACADEMIX |
|---|---|---|
| NTC-ISO/IEC 25010 (ICONTEC) | Técnica nacional | Adopción oficial de la norma de calidad |
| Ley 1581/2012 (Congreso) | Ley de datos personales (Habeas Data) | Protección de datos de estudiantes y acudientes menores |
| Res. 1519/2020 (MinTIC) | Accesibilidad web WCAG 2.1 AA | Interfaz accesible — brecha ARIA detectada (HAL-02) |
| CONPES 3975/2019 (DNP) | Política Nacional de IA | Marco ético para sistemas educativos digitales |
| colCERT (MinDefensa) | Ciberseguridad nacional | Protocolos de respuesta a incidentes |
| Circular 002/2021 (SIC) | Seguridad de datos | Cifrado y controles de acceso documentados |

### Speech — Expositor 2

> "Un aspecto que muchos proyectos de software ignoran es que Colombia tiene un marco regulatorio propio que complementa los estándares internacionales. Vamos a repasarlo.
>
> Primero, ICONTEC, el Instituto Colombiano de Normas Técnicas, adoptó oficialmente la ISO/IEC 25010 como la NTC-ISO/IEC 25010. Esto significa que en Colombia esta norma tiene carácter de norma técnica nacional.
>
> Segundo, la Ley 1581 de 2012, conocida como la Ley de Habeas Data, es de obligatorio cumplimiento para cualquier sistema que almacene datos personales. ACADEMIX almacena datos de estudiantes, muchos de ellos menores de edad, por lo que el cifrado de contraseñas y el control de acceso no son opcionales: son requisitos legales.
>
> Tercero, la Resolución 1519 de 2020 del MinTIC exige que los sistemas digitales que prestan servicios públicos cumplan con el nivel AA de las pautas de accesibilidad WCAG 2.1. Esto fue precisamente lo que detectamos como brecha en ACADEMIX: los mensajes de error del login no tienen atributos ARIA completos.
>
> Y cuarto, el CONPES 3975 establece la política de IA del país, relevante para la evolución futura de plataformas educativas.
>
> La conclusión de este análisis es que cumplir con ISO/IEC 25010 en Colombia no es suficiente: debemos alinear nuestro sistema con la Ley 1581 y la Resolución 1519, que tienen fuerza de ley."

---

## DIAPOSITIVA 8 — SCM: IEEE 828 Y LOS CINCO PROCESOS NUCLEARES

### Contenido visual sugerido
- Diagrama de flujo con los 5 procesos SCM en ciclo
- Definición de CI (Ítem de Configuración)
- Icono de Git como herramienta de SCM

### Speech — Expositor 3

> "Muy buenos días. Soy [Nombre] y voy a presentar el tercer bloque: Gestión de Configuración del Software.
>
> IEEE 828 es el *Standard for Configuration Management in Systems and Software Engineering*. Su propósito es establecer los mínimos que debe cumplir un proceso de Gestión de Configuración de Software, conocido como SCM por sus siglas en inglés.
>
> IEEE 828 define cinco procesos nucleares:
>
> Primero: Identificación de la Configuración. Consiste en catalogar todos los Ítems de Configuración del sistema, o CIs. Un CI es cualquier elemento del proyecto que necesita ser controlado: código fuente, archivos de configuración, base de datos, documentación. En ACADEMIX identificamos como CIs principales los módulos de Django, el archivo settings.py, el esquema de base de datos, los requirements.txt y los templates.
>
> Segundo: Control de Cambios. Define cómo se propone, evalúa, aprueba y registra cualquier modificación a un CI. Nosotros implementamos esto con nuestro Formato de Solicitud de Cambio, con campos como ID del cambio, justificación, impacto técnico y nivel de riesgo.
>
> Tercero: Contabilidad del Estado de Configuración, o CSA. Es el registro formal de qué versión está activa en cada ambiente — desarrollo, staging, producción.
>
> Cuarto: Auditorías de Configuración, que verifican que lo que está en producción coincide exactamente con lo que está documentado y aprobado.
>
> Y quinto: Gestión de Releases, que controla qué versiones del software se entregan y cuándo."

---

## DIAPOSITIVA 9 — CMMI-DEV: ÁREA DE PRÁCTICA CM

### Contenido visual sugerido
- Pirámide de niveles CMMI (1 Inicial → 5 En Optimización)
- Tabla: SG 1, SG 2, SG 3 con sus prácticas específicas
- Autoevaluación: ¿Dónde está ACADEMIX?

| Nivel CMMI | Descripción | ACADEMIX |
|---|---|---|
| 1 — Inicial | Procesos impredecibles, reactivos | — |
| **2 — Gestionado** | **Proyectos planificados y gestionados** | **← Actual (estimado)** |
| 3 — Definido | Procesos organizacionales estandarizados | Meta del semestre |
| 4 — Gestionado cuantitativamente | Control estadístico de procesos | Futuro |
| 5 — En Optimización | Mejora continua basada en datos | Futuro |

| Objetivo Específico | Prácticas en ACADEMIX |
|---|---|
| SG 1: Establecer Baselines | Tag `v2.5.0-baseline` en Git como línea base |
| SG 2: Seguir y Controlar Cambios | Formato CR-ACAD-2026-00X para toda modificación |
| SG 3: Establecer Integridad | Pull Requests + Code Review + Checklist antes de merge |

### Speech — Expositor 3

> "CMMI, el *Capability Maturity Model Integration*, es un modelo de mejora de procesos desarrollado por el Software Engineering Institute de Carnegie Mellon. Tiene cinco niveles de madurez, que van desde el nivel 1 Inicial, donde los procesos son caóticos y dependen de personas individuales, hasta el nivel 5 de Optimización, donde los procesos se mejoran continuamente con base en datos estadísticos.
>
> Para la Gestión de Configuración del Software, CMMI-DEV define el área de práctica CM con tres objetivos específicos:
>
> SG 1, Establecer Baselines, exige que existan líneas base identificadas y controladas. En ACADEMIX esto lo implementamos creando el tag de Git `v2.5.0-baseline` al commit `d97d7a6`, que corresponde al módulo de recuperación de contraseña completamente implementado.
>
> SG 2, Seguir y Controlar Cambios, exige que toda modificación pase por un proceso formal de solicitud y aprobación. Nosotros usamos el Formato de Solicitud de Cambio con ID único, descripción, impacto técnico, nivel de riesgo y aprobación del Tech Lead.
>
> SG 3, Establecer Integridad, exige verificar que los ítems de configuración en producción son los que fueron aprobados, sin modificaciones no autorizadas. Lo implementamos con Pull Requests obligatorios en GitHub y el Checklist de revisión de código que debe completarse antes de todo merge a main.
>
> Nuestra estimación es que ACADEMIX se encuentra actualmente en el nivel 2 de CMMI — Gestionado — y que la meta del semestre es alcanzar el nivel 3 estandarizando los procesos a nivel organizacional."

---

## DIAPOSITIVA 10 — GITFLOW, BASELINES Y CONTROL DE CAMBIOS EN ACADEMIX

### Contenido visual sugerido
- Diagrama de ramas GitFlow: main, develop, feature/*, hotfix/*
- Tabla de commits reales del repositorio
- Ciclo de vida de un Change Request

| Commit | Rama | Descripción |
|---|---|---|
| `d97d7a6` | main | Implementar módulo de recuperación de contraseña |
| `0ac921a` | main | Blindar carga masiva con savepoints atómicos |
| `25a46f7` | main | Eliminar sección Estado SCRUM del dashboard |
| `4cdeb2d` | main | Poblar catálogo oficial de asignaturas |
| `3829cb0` | main | Configurar usuarios institucionales para Render |

**Baselines establecidas:**
- `v2.5.0-baseline` → commit `d97d7a6` (Línea base módulo autenticación)
- `v2.5.1-baseline` → commit `f4b82e1` (Línea base con correcciones CR-005)

### Speech — Expositor 3

> "La Gestión de Configuración no es teoría — es algo que ya estamos haciendo en ACADEMIX con Git y GitHub. Pero la investigación de la Fase 1 nos permitió formalizar y dar nombre correcto a las prácticas que ya teníamos.
>
> En la tabla pueden ver los cinco commits más recientes de nuestro repositorio. Cada uno de estos commits representa un cambio controlado en el código fuente. Lo que antes hacíamos de manera informal — crear una rama, desarrollar, hacer merge — ahora lo entendemos como la implementación del proceso de Control de Cambios de IEEE 828.
>
> El flujo formal que establecimos es: primero, se detecta la necesidad de un cambio. Segundo, el desarrollador llena el Formato CR con el ID único, descripción, impacto técnico y nivel de riesgo. Tercero, el Tech Lead — quien actúa como CCB, Comité de Control de Cambios — evalúa y aprueba o rechaza. Si se aprueba, el desarrollador crea una rama `feature/CR-00X-descripcion`, implementa el cambio, y abre un Pull Request en GitHub. Antes de hacer el merge a main, otro miembro del equipo debe completar el Checklist de revisión de código. Finalmente, una vez en main, se registra en la Contabilidad del Estado de Configuración.
>
> Esta es la diferencia entre un equipo de nivel 1 CMMI — que hace commits directamente a main sin proceso — y un equipo de nivel 2 — que tiene un proceso planificado y gestionado para cada cambio."

---

## DIAPOSITIVA 11 — CONCLUSIONES Y RELACIÓN CON ACADEMIX

### Contenido visual sugerido
- Mapa visual conectando: ISO/IEC 25010 → IEEE 730 → IEEE 828 → CMMI → Normativa CO → ACADEMIX
- Lista de 5 conclusiones clave

### Speech — Todo el equipo (rotación de frases)

**Expositor 1:**
> "Como conclusión del bloque de Calidad del Producto: ISO/IEC 25010 nos dio el vocabulario preciso para dejar de decir 'el software funciona' y empezar a decir 'el módulo de autenticación tiene una disponibilidad del 99.1% y una cobertura de hash del 100%'. Sin métricas, la calidad es solo una opinión."

**Expositor 2:**
> "En cuanto al Aseguramiento de Calidad y la normativa colombiana: IEEE 730 nos enseñó que la calidad se planifica antes de escribir código, no se verifica después de terminar. Y la Resolución 1519 de MinTIC nos recordó que en Colombia el cumplimiento de accesibilidad web no es opcional: es obligación legal para sistemas que atienden al ciudadano."

**Expositor 3:**
> "Sobre la Gestión de Configuración: IEEE 828 y CMMI-DEV nos dieron la estructura formal para lo que ya hacíamos con Git de manera intuitiva. Ahora cada commit, cada rama, cada Pull Request y cada tag de versión hace parte de un proceso documentado, auditable y reproducible. Ese es el salto de un proyecto estudiantil a un sistema de calidad profesional."

**Todos (cierre conjunto):**
> "La investigación de la Fase 1 no fue solo leer normas: fue aplicarlas a nuestro código real, encontrar las brechas, y tener el lenguaje técnico para documentarlas y corregirlas. Eso es lo que diferencia al Tecnólogo en ADSO del programador autodidacta: la capacidad de trabajar con estándares internacionales y regulación nacional. Gracias."

---

## DIAPOSITIVA 12 — BANCO DE PREGUNTAS

### Contenido visual sugerido
- Diapositiva en blanco con título "Preguntas del Instructor"
- Subtítulo: "Estamos listos para la auditoría externa"

---

### BANCO DE PREGUNTAS Y RESPUESTAS PREPARADAS

---

**P1: ¿Cuál es la diferencia entre ISO/IEC 25010 e ISO 9126?**

> **Respuesta:** ISO 9126 fue el predecesor de ISO/IEC 25010. Tenía 6 características de calidad. La ISO/IEC 25010 de 2011 la reemplazó y amplió a 8 características, añadiendo Compatibilidad y Seguridad como características separadas. La versión 2023 de la norma hizo ajustes menores en la nomenclatura de algunas subcaracterísticas. La SQuaRE es la familia completa de normas, de la que 25010 es solo una de las piezas.

---

**P2: ¿Por qué seleccionaron esas 4 características de calidad y no otras?**

> **Respuesta:** Seleccionamos Fiabilidad, Seguridad, Usabilidad y Mantenibilidad porque son las características con mayor impacto de riesgo en un sistema escolar. La Fiabilidad porque ACADEMIX debe estar disponible durante el año lectivo sin interrupciones. La Seguridad porque almacena datos de menores de edad, lo que la Ley 1581 protege especialmente. La Usabilidad porque la Resolución 1519 de MinTIC exige accesibilidad. Y la Mantenibilidad porque el equipo debe poder extender el sistema en el tiempo.

---

**P3: ¿Qué es una línea base de configuración y cuál es la que tienen en ACADEMIX?**

> **Respuesta:** Una línea base, o baseline, es un snapshot aprobado formalmente de uno o más ítems de configuración en un momento del tiempo. Sirve como punto de referencia para controlar los cambios futuros. En ACADEMIX establecemos la línea base `v2.5.0-baseline` en el commit `d97d7a6` de Git, que corresponde al momento en que el módulo de recuperación de contraseña quedó completamente implementado. A partir de esa baseline, cualquier cambio debe pasar por el proceso formal de Change Request.

---

**P4: ¿Qué es el CCB y quién lo forma en su proyecto?**

> **Respuesta:** El CCB, Comité de Control de Cambios, es el órgano responsable de evaluar y aprobar o rechazar las solicitudes de cambio al software. En proyectos grandes puede ser un comité formal con representantes de negocio, arquitectura y QA. En nuestro caso, por el tamaño del equipo, el Tech Lead del proyecto actúa como CCB. Su responsabilidad es revisar el formulario CR, evaluar el impacto técnico y el nivel de riesgo, y firmar la aprobación antes de que el cambio se implemente.

---

**P5: ¿Cuál es el hallazgo más crítico que encontraron y cómo lo van a corregir?**

> **Respuesta:** El hallazgo más crítico es HAL-01: la ausencia de rate limiting en el endpoint de login. Técnicamente, el sistema permite intentos ilimitados de autenticación, lo que abre la puerta a ataques de fuerza bruta contra las credenciales de los usuarios. Esto viola el control A07 de OWASP Top 10 2021, que es "Fallas de Identificación y Autenticación". La corrección planificada en el Change Request CR-ACAD-2026-005 consiste en implementar django-ratelimit con un límite de 5 intentos por IP cada 15 minutos, y bloquear la cuenta tras 10 intentos fallidos.

---

**P6: ¿En qué nivel CMMI está su proyecto y cómo lo saben?**

> **Respuesta:** Estimamos que ACADEMIX está en el nivel 2 de CMMI, Gestionado. Lo sabemos porque cumplimos con los criterios del nivel 2: tenemos un proceso planificado de desarrollo por sprints, usamos Git para control de versiones, tenemos formatos de Change Request, los proyectos se gestionan con requisitos documentados, y hay métricas básicas de seguimiento. Sin embargo, aún no alcanzamos el nivel 3 porque los procesos no están estandarizados a nivel organizacional — cada desarrollador puede tener variaciones en cómo documenta o hace el commit. El nivel 3 requiere que los procesos estén definidos en una biblioteca organizacional y todos los apliquen de la misma manera.

---

**P7: ¿Qué dice IEEE 730 sobre las responsabilidades del equipo de QA?**

> **Respuesta:** IEEE 730 establece que el aseguramiento de calidad es una función independiente del equipo de desarrollo. El grupo SQA debe tener autoridad para identificar problemas y escalarlos a la gerencia si no se resuelven. En proyectos pequeños como el nuestro, esta independencia se implementa de forma pragmática: el revisor de un Pull Request nunca es el mismo desarrollador que escribió el código. Además, la revisión con el Checklist de código es obligatoria y debe completarse antes del merge, no después.

---

**P8: ¿Cuál es la diferencia entre una auditoría funcional de configuración (FCA) y una auditoría física de configuración (PCA)?**

> **Respuesta:** Ambas son tipos de auditorías definidas en el contexto de SCM. La FCA, Functional Configuration Audit, verifica que el software cumple con todos los requisitos funcionales documentados — básicamente que hace lo que dice que hace. La PCA, Physical Configuration Audit, verifica que la documentación de configuración — el código, los scripts, los archivos de despliegue — coincide exactamente con la versión que está en producción. En ACADEMIX simulamos una FCA revisando el módulo de autenticación contra sus requisitos de login, recuperación de contraseña y control de acceso por roles. Una PCA compararía el tag `v2.5.0-baseline` en Git con exactamente lo que está corriendo en el servidor de Render.

---

## NOTAS FINALES PARA EL EQUIPO

### Distribución de Material de Apoyo
- Cada expositor debe tener su sección del guión impresa o en pantalla secundaria
- Se recomienda proyectar las tablas y diagramas — usar fondo claro, letra oscura mínimo 24pt
- Llevar impreso el informe técnico completo para consultas del instructor

### Tiempo de Ensayo Recomendado
- Ensayo completo en voz alta: mínimo 2 veces antes de la exposición
- Cronometrar cada sección para ajustar el ritmo
- Practicar las transiciones entre expositores para que fluyan naturalmente

### Durante la Exposición
- Mantener contacto visual con el instructor y los compañeros
- Señalar los elementos de las tablas mientras se habla de ellos
- No leer directamente del guión — el texto es una guía, no un script literal
- Si hay una pregunta que no se sabe responder: "Excelente pregunta, la hemos investigado parcialmente — lo que sabemos es X, y lo que necesitaríamos investigar más a fondo es Y."

---

## REFERENCIAS ACADÉMICAS (APA 7)

ISO/IEC 25010:2023. (2023). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. International Organization for Standardization.

IEEE Std 730-2014. (2014). *IEEE Standard for Software Quality Assurance Processes*. IEEE Computer Society.

IEEE Std 828-2012. (2012). *IEEE Standard for Configuration Management in Systems and Software Engineering*. IEEE Computer Society.

CMMI Institute. (2018). *CMMI for Development, Version 2.0*. Carnegie Mellon University.

Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). *Resolución 1519 de 2020: Lineamientos de accesibilidad web para entidades del Estado colombiano*. Gobierno de Colombia.

Congreso de Colombia. (2012). *Ley Estatutaria 1581 de 2012: Protección de datos personales*. Diario Oficial.

Departamento Nacional de Planeación [DNP]. (2019). *CONPES 3975: Política Nacional para la Transformación Digital e Inteligencia Artificial*. Gobierno de Colombia.

ICONTEC. (2015). *NTC-ISO/IEC 25010: Ingeniería de sistemas y software — Requisitos y evaluación de calidad de sistemas y software (SQuaRE) — Modelo de calidad del sistema y del software*. Instituto Colombiano de Normas Técnicas y Certificación.

---

*Documento elaborado para el Programa ADSO — Ficha 3173430 — SENA Colombia*  
*Proyecto Formativo: ACADEMIX — Plataforma de Gestión Escolar*  
*Versión 1.0 — Noviembre 2026*

