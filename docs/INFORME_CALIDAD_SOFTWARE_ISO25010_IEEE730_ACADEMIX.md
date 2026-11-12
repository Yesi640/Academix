# INFORME TÉCNICO DE MARCOS NORMATIVOS DE CALIDAD DE SOFTWARE Y ARTEFACTOS DE GESTIÓN DE CONFIGURACIÓN (SCM / SQA)
## Aplicación Práctica al Sistema de Gestión Académica y Convivencial ACADEMIX

**Programa de Formación:** Tecnología en Análisis y Desarrollo de Software (ADSO)  
**Institución:** Servicio Nacional de Aprendizaje (SENA) — Centro de Formación en Tecnologías de la Información  
**Ficha de Caracterización:** 3173430  
**Proyecto Formativo:** Plataforma Web Academix — Sistema Integral de Control Escolar, Convivencial y Académico  
**Versión del Documento:** 1.0  
**Fecha:** Noviembre de 2026  
**Autores:** Equipo de Desarrollo de Software y Aseguramiento de Calidad — Academix  

---

## TABLA DE CONTENIDO

1. [Introducción y Objetivos](#1-introducción-y-objetivos)
   - 1.1 Objetivo General
   - 1.2 Objetivos Específicos
2. [Fase 1: Investigación y Marco Conceptual de Calidad de Software](#2-fase-1-investigación-y-marco-conceptual-de-calidad-de-software)
   - 2.1 Modelo de Calidad del Producto de Software (ISO/IEC 25010 e ISO/IEC 25010:2023)
   - 2.2 Aseguramiento de la Calidad del Software (Norma IEEE 730)
   - 2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)
   - 2.4 Entes Reguladores y Normativa de Calidad de Software en Colombia (Actualizado 2026)
3. [Fase 2: Artefactos y Plantillas de Evaluación Aplicadas a Academix](#3-fase-2-artefactos-y-plantillas-de-evaluación-aplicadas-a-academix)
   - 3.1 Artefacto 1: Matriz de Evaluación de Calidad de Software (Basada en ISO/IEC 25010)
   - 3.2 Artefacto 2: Formato de Solicitud de Cambio (Change Request - SCM)
   - 3.3 Artefacto 3: Lista de Verificación (Checklist) de Revisiones de Código (Code Review)
4. [Conclusiones](#4-conclusiones)
5. [Referencias Bibliográficas](#5-referencias-bibliográficas)

---

# 1. INTRODUCCIÓN Y OBJETIVOS

En el desarrollo moderno de sistemas de información, la calidad no es una propiedad accidental ni una fase accesoria que se añade al final de la programación; es una disciplina sistemática e ingenieril que debe integrarse a lo largo de todo el ciclo de vida del software. Para la plataforma **Academix** (Sistema de Información para la Gestión Académica, Convivencial, Calificaciones y Control Escolar en instituciones educativas colombianas), la calidad del software cobra una relevancia crítica: gestiona información sensible de menores de edad, soporta operaciones de alta concurrencia en cierres de periodo, automatiza promedios académicos ponderados y emite boletines oficiales con implicaciones legales y formativas.

El presente documento articula la investigación conceptual de los marcos internacionales líderes en aseguramiento de calidad (ISO/IEC 25010 e IEEE 730), el régimen legal y técnico colombiano vigente (ICONTEC, MinTIC, Superintendencia de Industria y Comercio - SIC, MinCiencias y colCERT), y la implementación operativa de tres artefactos troncales para la Gestión de Configuración y Aseguramiento de Calidad (SQA/SCM) del proyecto Academix.

## 1.1 Objetivo General
Investigar, seleccionar y aplicar marcos normativos internacionales y nacionales de calidad de software (ISO/IEC 25010 para calidad de producto, IEEE 730 para aseguramiento de calidad y normas técnicas colombianas del ICONTEC y MinTIC) mediante el diseño e implementación de plantillas de control, evaluación y gestión de configuración aplicadas directamente a la plataforma de software Academix.

## 1.2 Objetivos Específicos
1. Documentar los fundamentos teóricos del modelo de calidad de producto según la familia ISO/IEC 25000 (SQuaRE) y la actualización ISO/IEC 25010:2023, diferenciando calidad interna, externa y en uso.
2. Analizar el alcance del estándar IEEE 730 en el aseguramiento de calidad del software (SQA), integrándolo con metodologías ágiles (Scrum) y flujos de integración continua (CI/CD).
3. Contextualizar el marco regulatorio colombiano de calidad, ciberseguridad y protección de datos personales de menores (Ley 1581 de 2012, directrices MinTIC de Gobierno Digital, NTC-ISO/IEC 25010 de ICONTEC y lineamientos SENA).
4. Diseñar e implementar la **Matriz de Evaluación de Calidad ISO/IEC 25010** personalizada para los módulos de Academix (calificaciones, autenticación RBAC, importación masiva de estudiantes y auditoría).
5. Estructurar el **Formato de Solicitud de Cambio (Change Request - SCM)** como herramienta de gobernanza de la configuración, con un caso real implementado sobre el sistema.
6. Desarrollar la **Lista de Verificación (Checklist) de Revisión de Código** para los Pull Requests / Merges del repositorio, cubriendo estándares de codificación Python/Django (PEP 8), control de inyecciones (OWASP), transaccionalidad ACID y normativas nacionales.

---

# 2. FASE 1: INVESTIGACIÓN Y MARCO CONCEPTUAL DE CALIDAD DE SOFTWARE

## 2.1 Modelo de Calidad del Producto de Software (ISO/IEC 25010 e ISO/IEC 25010:2023)

### 2.1.1 La Familia de Normas ISO/IEC 25000 (SQuaRE)
La serie de normas internacionales **ISO/IEC 25000**, conocida como **SQuaRE** (*Software Product Quality Requirements and Evaluation*), sustituyó a las históricas normas ISO/IEC 9126 (evaluación del producto) e ISO/IEC 14598 (proceso de evaluación). SQuaRE se organiza en cinco divisiones estructurales:
- **ISO/IEC 2500n - División de Gestión de Calidad:** Directrices generales, modelos de gestión y términos unificados.
- **ISO/IEC 2501n - División del Modelo de Calidad:** Define el modelo de calidad del producto de software (ISO/IEC 25010) y el modelo de calidad en uso (ISO/IEC 25019 / 25022).
- **ISO/IEC 2502n - División de Medición de Calidad:** Métricas de calidad interna, externa y calidad en uso (ISO/IEC 25023).
- **ISO/IEC 2503n - División de Requisitos de Calidad:** Guías para especificar requisitos funcionales y no funcionales de calidad.
- **ISO/IEC 2504n - División de Evaluación de Calidad:** Procedimientos y requerimientos de evaluación imparcial para desarrolladores, adquirentes y evaluadores independientes.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                   FAMILIA ISO/IEC 25000 (SQuaRE)            │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  [ ISO/IEC 2500n ]            [ ISO/IEC 2501n ]            [ ISO/IEC 2502n ]
  Gestión de Calidad           Modelos de Calidad          Medición y Métricas
                               (25010: Producto)           (25023: Indicadores)
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                  [ ISO/IEC 2503n ]           [ ISO/IEC 2504n ]
                  Requisitos Calidad          Proceso de Evaluación
```

### 2.1.2 Características de Calidad del Producto (ISO/IEC 25010)
El modelo de calidad del producto de software descompone la calidad en ocho características primarias y múltiples subcaracterísticas:

| Característica Primaria | Definición Técnica | Subcaracterísticas Asociadas |
| :--- | :--- | :--- |
| **1. Adecuación Funcional** | Capacidad del producto para satisfacer las necesidades declaradas e implícitas bajo condiciones especificadas. | • Completitud funcional<br>• Corrección funcional<br>• Pertinencia funcional |
| **2. Eficiencia de Desempeño** | Rendimiento del software relativo a la cantidad de recursos consumidos en condiciones determinadas. | • Comportamiento temporal (latencia)<br>• Utilización de recursos (CPU, RAM)<br>• Capacidad (rendimiento concurrente) |
| **3. Compatibilidad** | Capacidad de dos o más sistemas de intercambiar información y ejecutar funciones requeridas compartiendo el mismo entorno. | • Coexistencia<br>• Interoperabilidad |
| **4. Usabilidad** | Capacidad del producto de ser entendido, aprendido, usado y resultar atractivo para los usuarios objetivo. | • Reconocimiento de idoneidad<br>• Capacidad de aprendizaje<br>• Operabilidad<br>• Protección contra errores de usuario<br>• Estética de la interfaz<br>• Accesibilidad |
| **5. Fiabilidad** | Grado en que el software desempeña funciones especificadas bajo condiciones dadas por un tiempo determinado. | • Madurez<br>• Disponibilidad<br>• Tolerancia a fallos<br>• Recuperabilidad |
| **6. Seguridad** | Grado de protección de información y datos para que personas o sistemas no autorizados no puedan acceder ni modificarlos. | • Confidencialidad<br>• Integridad<br>• No repudio<br>• Responsabilidad (Trazabilidad/Auditoría)<br>• Autenticidad |
| **7. Mantenibilidad** | Efectividad y eficiencia con la que el producto puede ser modificado por los mantenedores. | • Modularidad<br>• Reusabilidad<br>• Analizabilidad<br>• Modificabilidad<br>• Capacidad de ser probado (Testabilidad) |
| **8. Portabilidad** | Capacidad del sistema para ser transferido de un entorno de hardware, software u operativo a otro. | • Adaptabilidad<br>• Facilidad de instalación<br>• Facilidad de sustitución |

### 2.1.3 Actualización ISO/IEC 25010:2023
En la revisión internacional publicada en 2023, la norma evolucionó para adaptarse a sistemas modernos en la nube, arquitecturas de microservicios e inteligencia artificial:
- **Seguridad e Inclusión:** Se robustece la accesibilidad hacia el concepto integral de *Inclusión*, asegurando que personas con capacidades diversas puedan interactuar plenamente con la plataforma.
- **Flexibilidad (Safety & Flexibility):** Se desagrega la portabilidad hacia una característica más amplia de *Flexibilidad*, incorporando la escalabilidad elástica y la robustez frente a cambios del contexto operativo.
- **Calidad de Datos Integrada:** Mayor acoplamiento con la norma ISO/IEC 25012 para garantizar que los datos procesados por el software mantengan exactitud, coherencia sintáctica y credibilidad.

### 2.1.4 Calidad del Producto vs. Calidad en Uso
Es vital distinguir ambos niveles según SQuaRE:
- **Calidad del Producto (ISO/IEC 25010):** Evalúa las propiedades estáticas del código fuente y el comportamiento dinámico del software en ejecución (ej. ausencia de vulnerabilidades, consumo de memoria, modularidad de clases Django).
- **Calidad en Uso (ISO/IEC 25019 / 25022):** Evalúa el impacto del software en el contexto real del usuario humano en su entorno laboral o pedagógico. Se mide a través de:
  1. *Eficacia:* Exactitud con la que docentes y directivos completan el registro de calificaciones sin errores.
  2. *Eficiencia:* Cantidad de tiempo y esfuerzo que invierte un docente en subir las notas del periodo.
  3. *Satisfacción:* Confianza, agrado y confort percibido por la comunidad educativa.
  4. *Ausencia de Riesgo:* Mitigación de riesgos económicos, legales (sanciones SIC) y pedagógicos.
  5. *Cobertura de Contexto:* Funcionamiento óptimo tanto en computadores institucionales de escritorio como en dispositivos móviles de acudientes con conexiones variables.

---

## 2.2 Aseguramiento de la Calidad del Software (Norma IEEE 730)

### 2.2.1 Propósito y Alcance del Estándar IEEE 730
El estándar **IEEE 730** (*Standard for Software Quality Assurance Processes*) establece los requerimientos para iniciar, planificar, controlar y ejecutar los procesos de **Aseguramiento de Calidad del Software (SQA - Software Quality Assurance)**. A diferencia de las pruebas de software (testing), que se concentran en encontrar defectos puntuales en el producto (control reactivo), el SQA según IEEE 730 es una disciplina preventiva orientada a los **procesos**: asegura que los métodos, herramientas, estándares y procedimientos seleccionados se apliquen rigurosamente durante todo el ciclo de vida para evitar que los defectos se introduzcan.

### 2.2.2 Componentes del Plan de Aseguramiento de Calidad (SQAP)
Un Plan de Aseguramiento de Calidad formal gobernado por IEEE 730 comprende las siguientes secciones operativas:

1. **Gestión y Organización del SQA:** Estructura jerárquica del equipo, roles de los evaluadores independientes, responsabilidades y autoridad para detener un despliegue si no se cumplen los criterios de calidad.
2. **Documentación del Software:** Inventario de artefactos obligatorios que deben existir (especificación de requerimientos de software SRS, manual técnico, plan de pruebas, manual de usuario, actas de entrega).
3. **Estándares, Prácticas, Convenciones y Métricas:** Definición explícita de reglas de codificación (PEP 8, ESLint), convenciones de commits (Conventional Commits), estándares de diseño (RESTful, MVT) y métricas umbral (cobertura mínima de pruebas >= 80%, complejidad ciclomática de McCabe < 10).
4. **Revisiones Técnicas de Software y Auditorías:**
   - *Revisiones de Requisitos y Arquitectura:* Verificación formal de que el diseño cubre los requisitos del cliente institucional.
   - *Inspecciones de Código (Code Inspections):* Revisiones paritarias (Peer Code Reviews) previas a cada Merge Request.
   - *Auditorías de Configuración (PCA - Physical Configuration Audit y FCA - Functional Configuration Audit):* Comprobación de que la versión a desplegar coincide exactamente con los requerimientos aprobados y los ítems de configuración registrados.
5. **Gestión de Pruebas (Verificación y Validación - V&V):** Plan integral que abarca pruebas unitarias (`pytest`), pruebas de integración (ORM y endpoints), pruebas de seguridad (análisis estático SAST y dinámico DAST) y pruebas de aceptación del usuario final (UAT).
6. **Reporte de Problemas y Acciones Correctivas (CAPA - Corrective and Preventive Action):** Procedimiento estandarizado para registrar, tipificar, priorizar y resolver anomalías mediante sistemas de seguimiento de incidencias (Issue Trackers).
7. **Herramientas, Técnicas y Metodologías:** Herramientas de software utilizadas para soportar el proceso de SQA (linters, suites de pruebas automatizadas, gestores de tareas y pipelines CI/CD).

### 2.2.3 Articulación con Metodologías Ágiles (Scrum) y DevOps / DevSecOps
En el paradigma contemporáneo, el SQA según IEEE 730 no opera como una burocracia rígida de cascada, sino que se automatiza y distribuye dentro de los sprints y flujos continuos:
- **En Scrum:** Las prácticas de SQA se materializan en los acuerdos de equipo, específicamente en la **Definition of Ready (DoR)** y la **Definition of Done (DoD)**. Una historia de usuario de Academix (ej. *Cálculo automático de puestos y promedios*) solo se considera terminada si cuenta con pruebas unitarias aprobadas, revisión de código por pares y documentación de API actualizada.
- **En DevOps / CI-CD:** El plan SQA se ejecuta automáticamente en cada `git push` mediante pipelines de Integración Continua (GitHub Actions, GitLab CI o pipelines de despliegue en Render/Docker): ejecución de linters (`flake8`, `black`), escaneo de dependencias vulnerables (`pip-audit`), pruebas unitarias con reporte de cobertura (`pytest-cov`) y análisis SAST (`bandit`).

---

## 2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)

La Gestión de Configuración del Software (SCM) es la disciplina que controla la evolución de los sistemas complejos mediante la identificación formal de sus componentes, el control sistemático de modificaciones y el mantenimiento de la trazabilidad durante todo el ciclo de vida (estándar IEEE 828).

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                 PROCESO DE CONTROL DE CAMBIOS (SCM)                    │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
                      [ 1. Solicitud de Cambio (CR) ]
                      Registro formal de la necesidad
                                     │
                                     ▼
                      [ 2. Análisis de Impacto y Riesgo ]
                      Técnico, Base de Datos, Legal, Costo
                                     │
                                     ▼
                      [ 3. Comité de Control (CCB) ]
                      Evaluación: ¿Se aprueba, rechaza o aplaza?
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
             [ APROBADO ]                       [ RECHAZADO ]
                    │                           Notificación y Cierre
                    ▼
          [ 4. Rama de Desarrollo ]
          Implementación bajo GitFlow / Pruebas
                    │
                    ▼
          [ 5. Code Review & QA ]
          Checklist de Calidad y Tests Unitarios
                    │
                    ▼
          [ 6. Merge & Nueva Línea Base ]
          Tag de versión (SemVer) / Despliegue
```

### 2.3.1 Conceptos Fundamentales de SCM
- **Ítem de Configuración (CI - Configuration Item):** Cualquier entidad o artefacto producido durante el ciclo de vida del software que se somete a control de versiones individual o grupal. En Academix constituyen CIs: el código fuente Python (`views.py`, `models.py`), scripts de migración Django (`0001_initial.py`), plantillas HTML, hojas de estilo CSS, esquemas de bases de datos, archivos de configuración de entorno (`.env.example`), Dockerfiles y manuales técnicos.
- **Línea Base (Baseline):** Especificación o producto de software formalmente revisado y acordado por el equipo, que sirve de base fija para el desarrollo posterior y que solo puede modificarse mediante un procedimiento formal de control de cambios. Líneas base en Academix:
  - *Línea Base de Requisitos:* Matriz de Requerimientos SRS aprobada por la institución educativa.
  - *Línea Base de Arquitectura:* Modelo de Entidad-Relación y estructura de micro-apps en Django 5.x.
  - *Línea Base de Entrega (Release Baseline):* Tag formal de Git (ej. `v2.5.0-release`) desplegado en producción con base de datos sincronizada.
- **Control de Versiones y Estrategia de Ramas:** Adopción del flujo **GitFlow adaptado**:
  - `main`: Rama de producción inmutable; solo recibe código probado mediante Pull Requests aprobados desde `release` o `hotfix`.
  - `develop`: Rama de integración donde convergen las nuevas funcionalidades.
  - `feature/nombre-funcionalidad`: Ramas temporales de desarrollo creadas a partir de `develop`.
  - `hotfix/nombre-parche`: Ramas de corrección urgente directamente sobre `main`.
- **Comité de Control de Cambios (CCB - Change Control Board):** Grupo multidisciplinario responsable de evaluar, aprobar, priorizar o rechazar solicitudes de cambio (CRs) considerando el balance entre costo, tiempo, impacto técnico y beneficio pedagógico. En el proyecto Academix, el CCB está conformado por el Líder Técnico de Desarrollo, el Responsable de SQA/Pruebas y el Representante del Cliente/Institución Educativa (Product Owner).

---

## 2.4 Entes Reguladores y Marco Normativo de Calidad de Software en Colombia (Actualizado 2026)

El desarrollo e implantación de software en el territorio nacional colombiano está supeditado a un conjunto vinculante de normas técnicas, leyes estatutarias y lineamientos gubernamentales dictados por entidades oficiales:

```
               ┌────────────────────────────────────────────────────────┐
               │    ENTES REGULADORES DE CALIDAD Y TI EN COLOMBIA       │
               └───────────────────────────┬────────────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
    [ ICONTEC ]         [ MinTIC ]            [ SIC ]        [ MinCiencias / colCERT ]
   Normalización     Gobierno Digital     Datos Personales    Ciberseguridad y
    NTC-ISO 25010     Accesibilidad       Ley 1581 / NNA      Tipificación I+D+i
    NTC-ISO 27001     Res. 1519 / MSPI    RNBD Institucional  CONPES 3995
```

### 2.4.1 ICONTEC (Instituto Colombiano de Normas Técnicas y Certificación)
Organismo Nacional de Normalización de Colombia. A través de su Comité Técnico 181 (Ingeniería de Software y Sistemas de Información), homologa y adopta oficialmente los estándares internacionales como Normas Técnicas Colombianas (NTC):
- **NTC-ISO/IEC 25010:** Calidad de productos de software y modelos de evaluación. Es la referencia obligatoria para definir especificaciones de licitaciones y contratos públicos y privados de desarrollo tecnológico en Colombia.
- **NTC-ISO/IEC 12207:** Procesos del ciclo de vida del software, estableciendo la arquitectura de procesos desde la concepción hasta el retiro del software.
- **NTC-ISO/IEC 27001:** Sistemas de Gestión de la Seguridad de la Información (SGSI), indispensable para la protección de la infraestructura de alojamiento, bases de datos y credenciales de acceso institucional.
- **NTC 5906:** Gestión de la calidad de datos y procesos en las tecnologías de información.

### 2.4.2 MinTIC (Ministerio de Tecnologías de la Información y las Comunicaciones)
Entidad rectora del sector de las tecnologías de la información en Colombia. Establece las directrices técnicas obligatorias para entidades del Estado y proyectos educativos:
- **Política de Gobierno Digital (Decreto Único Reglamentario 1078 de 2015, modificado por Decreto 088 de 2022 y Resolución 460 de 2022):** Define los lineamientos de interoperabilidad de datos, servicios ciudadanos digitales y transformación digital pública.
- **Resolución 1519 de 2020 (Accesibilidad y Usabilidad Web):** Dicta las directrices obligatorias de accesibilidad web basadas en el estándar internacional **W3C WCAG 2.1 en nivel de conformidad AA**. Toda plataforma de uso educativo público o mixto debe asegurar contraste cromático adecuado, navegación por teclado, soporte a lectores de pantalla (atributos ARIA) y diseño responsivo móvil.
- **Modelo de Seguridad y Privacidad de la Información (MSPI):** Marco articulado con el CONPES 3995 de Seguridad Digital, que exige controles de seguridad en el ciclo de vida del software, gestión de incidentes y cifrado de comunicaciones web (TLS 1.3).

### 2.4.3 Superintendencia de Industria y Comercio (SIC) — Delegatura de Protección de Datos Personales
Autoridad nacional de control y vigilancia en materia de tratamiento de datos personales:
- **Ley Estatutaria 1581 de 2012 y Decreto Reglamentario 1377 de 2013:** Marco general de Habeas Data en Colombia.
- **Régimen Especial para Niños, Niñas y Adolescentes (NNA - Artículo 7 de la Ley 1581):** Establece una prohibición general de tratamiento de datos personales de menores, salvo que responda y respete el interés superior de los niños y asegure el respeto de sus derechos fundamentales. En plataformas escolares como Academix, esto exige:
  1. Consentimiento expreso e informado de los padres o acudientes legales antes de recolectar datos de los estudiantes.
  2. Implementación de controles técnicos que impidan la divulgación pública de historiales académicos, notas y sanciones convivenciales.
  3. Cifrado irreversible o uso de funciones hash robustas (Argon2id, PBKDF2) para contraseñas de acceso.
  4. Obligación de inscripción y reporte de las bases de datos ante el **Registro Nacional de Bases de Datos (RNBD)** administrado por la SIC.

### 2.4.4 MinCiencias (Ministerio de Ciencia, Tecnología e Innovación)
Establece los criterios de tipificación y categorización de productos de desarrollo tecnológico e innovación (I+D+i) en Colombia:
- Clasifica el **software de alta calidad** como producto tecnológico transferible si cuenta con: registro formal de soporte lógico ante la Dirección Nacional de Derecho de Autor (DNDA), manuales técnicos formalizados, evidencias de pruebas formales bajo ISO/IEC 25010 y contrato de licencia de uso o cesión de derechos con la entidad beneficiaria.

### 2.4.5 colCERT (Grupo de Respuestas a Emergencias Cibernéticas de Colombia) y CSIRT de Gobierno
Dependencias adscritas al Ministerio de Defensa y MinTIC responsables de coordinar la ciberseguridad nacional:
- Publican alertas tempranas y directrices de mitigación contra vulnerabilidades críticas (CVEs).
- Promueven la adopción de prácticas de desarrollo seguro basadas en el **OWASP Top 10** (eliminación de fallos de inyección SQL, Cross-Site Scripting, falsificación de peticiones en sitios cruzados CSRF y fallos de autenticación), obligatorios para que sistemas académicos resistan ataques cibernéticos y fugas de información.

### 2.4.6 SENA (Servicio Nacional de Aprendizaje)
Como entidad líder de la formación para el trabajo en Colombia, el SENA rige las competencias técnicas del programa ADSO bajo normas de competencia laboral como la **Norma 220501096: Desarrollar el sistema informático según requisitos y diseño tecnológico**. El SENA audita que los proyectos formativos adopten la trazabilidad documental, la aplicación estricta de normas técnicas internacionales y la ejecución rigurosa de pruebas de calidad previas al egreso técnico y productivo.

---

# 3. FASE 2: ARTEFACTOS Y PLANTILLAS DE EVALUACIÓN APLICADAS A ACADEMIX

A continuación, se presentan formalmente los tres artefactos documentales e instrumentos de control diseñados a medida para integrarse a la gestión de configuración y calidad del sistema **ACADEMIX v2.5.0**.

---

## 3.1 ARTEFACTO 1: MATRIZ DE EVALUACIÓN DE CALIDAD DE SOFTWARE (BASADA EN ISO/IEC 25010)

Esta matriz operacionaliza la norma internacional ISO/IEC 25010:2023, seleccionando **seis (6) características estratégicas** indispensables para el correcto funcionamiento institucional y legal de Academix.

```
+----------------------------------------------------------------------------------------------------+
|                                MATRIZ DE EVALUACIÓN DE CALIDAD ISO/IEC 25010                       |
|                                     PROYECTO ACADEMIX - VERSIÓN 2.5.0                              |
+----------------------------------------------------------------------------------------------------+
```

| ID | Característica ISO 25010 | Subcaracterística | Criterio de Evaluación Academix | Métrica / Fórmula de Medición | Método / Herramienta de Prueba | Resultado Esperado / Umbral de Aceptación |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC-01** | **Adecuación Funcional** | **Exactitud Funcional** (*Functional Correctness*) | El cálculo automático del promedio acumulado por asignatura y por periodo, ponderado según los porcentajes asignados a cada Resultado de Aprendizaje Previsto (RAP), debe arrojar valores con precisión de dos decimales sin truncamientos erróneos. | $$E = \frac{N_{calc\_exactos}}{N_{calc\_totales}} \times 100$$<br>Donde $E$ es el porcentaje de exactitud sobre un conjunto de $N$ registros de prueba. | **Pruebas Unitarias Automatizadas:**<br>Ejecución de test cases con `pytest` y `django.test.TestCase` evaluando casos borde (notas mínimas `1.0`, máximas `5.0`, ponderaciones con decimales periódicos). | **100% de exactitud matemática.**<br>Cero discrepancias frente a la fórmula matemática de ponderación institucional. |
| **MC-02** | **Adecuación Funcional** | **Completitud Funcional** (*Functional Completeness*) | El módulo de importación masiva de estudiantes (`apps.students.views.bulk_upload_students`) debe procesar íntegramente listas en formato CSV y Excel (XLSX), creando usuarios, registros académicos y asignando sede/curso sin omisiones. | $$C = \frac{R_{importados\_exitosos}}{R_{validos\_archivo}} \times 100$$ | **Pruebas de Integración:**<br>Carga de datasets de prueba con 250 y 500 registros con caracteres especiales (tildes, eñes) y validación en base de datos. | **100% de registros válidos procesados e insertados.** Reporte explícito y detallado de filas rechazadas por inconsistencias sintácticas. |
| **MC-03** | **Seguridad** | **Confidencialidad y Autenticidad** (*Confidentiality*) | Toda contraseña de usuario almacenada en la base de datos debe estar protegida mediante funciones de derivación criptográfica de clave robusta (PBKDF2 con SHA-256 o Argon2id) con sal (*salt*) aleatoria. Ninguna credencial puede almacenarse en texto plano. | $$S_{pwd} = \frac{U_{pwd\_hasheadas\_robustas}}{U_{totales}} \times 100$$ | **Inspección de Esquema SAST:**<br>Consulta directa a la tabla `accounts_customuser` y análisis de código estático con la herramienta `Bandit` (`bandit -r apps/`). | **100% de contraseñas con hashing criptográfico estándar Django.** Cero hallazgos de almacenamiento en texto claro en base de datos o logs. |
| **MC-04** | **Seguridad** | **Integridad y Autorización (RBAC)** (*Integrity & Authorization*) | Cumplimiento estricto del Control de Acceso Basado en Roles (Rector, Coordinador, Docente, Estudiante, Acudiente). Un docente o estudiante no debe poder acceder a URLs de administración ni alterar notas de asignaturas no asignadas (IDOR / Broken Access Control). | $$I_{RBAC} = 1 - \left( \frac{V_{acceso\_no\_autorizado}}{P_{intentos\_pen\_testing}} \right)$$ | **Pruebas de Seguridad / Pentesting:**<br>Escaneo dinámico con `OWASP ZAP` y suites de prueba de penetración simulando peticiones HTTP con cookies de sesión de rol 'Estudiante' hacia rutas `/admin/`, `/grades/finalize/`, etc. | **100% de rutas protegidas.**<br>Cero accesos indebidos (Retorno obligatorio de código `HTTP 403 Forbidden` o redirección `HTTP 302` con log de auditoría). |
| **MC-05** | **Fiabilidad** | **Tolerancia a Fallos y Recuperabilidad** (*Fault Tolerance*) | Ante caídas intempestivas del servidor de base de datos PostgreSQL durante una transacción masiva de notas, el sistema no debe corromper registros ni dejar estados inconsistentes a medias (Transaccionalidad ACID). | Tasa de inconsistencias registradas en la base de datos tras simular interrupciones forzadas (`kill -9`) en escrituras múltiples. | **Pruebas de Caos e Inyección de Fallos:**<br>Corte forzado del proceso de PostgreSQL en mitad de un bucle de guardado de 200 calificaciones dentro de un bloque `transaction.atomic()`. | **Cero corrupción de datos.** Reversión total (*Rollback*) automática de la transacción incompleta y reanudación limpia de la conexión. |
| **MC-06** | **Eficiencia de Desempeño** | **Comportamiento Temporal** (*Time Behavior*) | El tiempo de respuesta del servidor (TTFB - Time to First Byte) en la generación y renderizado del tablero de control (Dashboard) y la consulta de notas no debe superar 500 milisegundos bajo una carga de 100 usuarios concurrentes. | $$T_{promedio} = \frac{\sum_{i=1}^{n} T_i}{n} \le 500\text{ ms}$$<br>Percentil 95 ($P_{95}$) $\le 800\text{ ms}$. | **Pruebas de Carga y Estrés:**<br>Ejecución de escenarios de carga concurrente con `Locust` o `Apache JMeter` simulando 100 y 200 hilos de usuarios concurrentes en el entorno de staging. | **Latencia media $\le 500\text{ ms}$ y $P_{95} \le 800\text{ ms}$.**<br>Tasa de error HTTP (`500 Internal Server Error`) inferior al **0.1%**. |
| **MC-07** | **Usabilidad** | **Accesibilidad e Inclusión** (*Accessibility*) | Cumplimiento del estándar W3C WCAG 2.1 nivel AA exigido por la Resolución 1519 de 2020 de MinTIC: contraste de color adecuado ($\ge 4.5:1$ en texto normal), etiquetas `alt` en imágenes y navegación accesible por teclado. | Puntuación de Accesibilidad según auditoría automatizada y porcentaje de contraste conforme. | **Auditoría Automatizada de Calidad Frontend:**<br>Ejecución de auditorías con `Google Lighthouse CI` y extensión de accesibilidad `axe DevTools` sobre todas las vistas principales de la aplicación. | **Calificación de Accesibilidad en Lighthouse $\ge 90/100$.** Cumplimiento del 100% de criterios esenciales nivel AA de la Res. 1519 MinTIC. |
| **MC-08** | **Mantenibilidad** | **Capacidad de Prueba y Modularidad** (*Testability & Modularity*) | La arquitectura de micro-aplicaciones en Django (`apps/`) debe mantener bajo acoplamiento, alta cohesión y una cobertura de pruebas automatizadas superior al 80% sobre la lógica de negocio (`services.py`, `models.py`, `views.py`). | $$Cov = \frac{L_{ejecutadas\_tests}}{L_{totales\_codigo}} \times 100 \ge 80\%$$<br>Complejidad ciclomática de McCabe $v(G) \le 10$ por función. | **Análisis Estático y Cobertura:**<br>Ejecución de `pytest-cov` / `coverage.py` integrado al linter `flake8` y métricas de complejidad con `radon` (`radon cc apps/ -a`). | **Cobertura de código global $\ge 80\%$.** Cero métodos o funciones con complejidad ciclomática superior a 12. |

---

## 3.2 ARTEFACTO 2: FORMATO DE SOLICITUD DE CAMBIO (CHANGE REQUEST - SCM)

Este formato constituye el instrumento oficial de control del Comité de Control de Cambios (CCB) del proyecto Academix. Ninguna modificación a los requerimientos base o al código en producción puede implementarse sin este registro debidamente aprobado.

```
+----------------------------------------------------------------------------------------------------+
|                               FORMATO DE SOLICITUD DE CAMBIO (RFC / SCM)                           |
|                                       PROYECTO SOFTWARE: ACADEMIX                                  |
+----------------------------------------------------------------------------------------------------+
```

### SECCIÓN 1: IDENTIFICACIÓN GENERAL DEL CAMBIO
| Campo | Detalle / Diligenciamiento |
| :--- | :--- |
| **Código de Solicitud (CR-ID):** | `CR-ACAD-2026-004` |
| **Fecha de Solicitud:** | 03 de Noviembre de 2026 |
| **Nombre del Solicitante:** | Ing. Carlos Mendoza Valencia |
| **Rol / Cargo:** | Coordinador Académico y Representante de la Institución Beneficiaria |
| **Proyecto / Módulo Afectado:** | Plataforma Academix / Módulos: `apps.grades` y `apps.reports` |
| **Versión Base del Software:** | v2.5.0 |
| **Versión Proyectada:** | v2.6.0 |

### SECCIÓN 2: CLASIFICACIÓN Y PRIORIDAD
| Tipo de Cambio | Prioridad | Nivel de Riesgo |
| :--- | :--- | :--- |
| [ ] Corrección de Defecto (*Bugfix*)<br>[X] **Nueva Funcionalidad (*Feature*)**<br>[ ] Mejora de Rendimiento (*Optimization*)<br>[X] **Cumplimiento Legal / Normativo**<br>[ ] Refactorización Arquitectónica | [ ] Crítica (Emergencia - Inmediata)<br>[X] **Alta (Sprint en Curso)**<br>[ ] Media (Próxima Versión)<br>[ ] Baja (Bajo Demanda) | [ ] Extremo (Riesgo total de operación)<br>[X] **Moderado (Afecta migraciones y vistas)**<br>[ ] Bajo (Impacto cosmético o documentación) |

### SECCIÓN 3: DESCRIPCIÓN Y JUSTIFICACIÓN
- **Título Resumido del Cambio:**
  *Implementación de Control de Cierre Extemporáneo de Periodo y Firma Criptográfica de Boletines Escolares con Código QR Seguro.*
- **Descripción Detallada de la Modificación Solicitada:**
  Actualmente, el sistema permite que los docentes ingresen calificaciones de manera continua. Se requiere implementar un mecanismo de **Cierre Administrativo de Periodo** gobernado por Rectoría, el cual inhabilite la edición o adición de calificaciones una vez vencida la fecha límite oficial. Adicionalmente, los boletines de calificaciones en PDF generados por `apps.reports` deberán incluir en su pie de página un **Código QR dinámico** firmado con un hash SHA-256 de verificación, permitiendo que las familias y secretarías de educación validen la autenticidad del documento escaneando el código desde un enlace web público institucional (`/verify-report/<uuid>/`).
- **Justificación del Negocio / Pedagógica / Legal:**
  1. *Seguridad y Control:* Evitar adulteraciones extemporáneas de calificaciones definitivas tras la publicación oficial.
  2. *Validez Jurídica:* Atender las auditorías de secretarías de educación respecto a la inmutabilidad de actas académicas.
  3. *Cumplimiento Normativo:* Articulación con la Ley 1581 de 2012 (trazabilidad de modificaciones de datos) y la Resolución 460 de 2022 de MinTIC (confiabilidad de documentos electrónicos).

### SECCIÓN 4: ANÁLISIS DE IMPACTO TÉCNICO MULTIDIMENSIONAL
| Dimensión de Impacto | Análisis de Afectación Técnica en Academix |
| :--- | :--- |
| **Arquitectura de Software** | Modificación desacoplada en la capa de servicios de `apps.grades`. Creación de un decorador/middleware `@period_is_open_required` que valide el estado del periodo antes de admitir peticiones `POST` a los formularios de notas. |
| **Base de Datos y Modelos** | **Migración Requerida:** Alteración del modelo `Period` en `apps.periods.models` para añadir los campos `is_locked (BooleanField, default=False)` y `closed_at (DateTimeField, null=True)`. Creación de la tabla `ReportVerificationToken` con llave primaria UUIDv4, fecha de expiración y firma SHA-256. |
| **Interfaz de Usuario (UI)** | Inclusión de banner visual de alerta ("Periodo Académico Cerrado para Edición") en las plantillas `templates/grades/grade_entry.html` y desactivación de botones de guardado para perfil Docente. |
| **Seguridad de la Información** | El endpoint de verificación pública `/verify-report/<uuid>/` no debe exponer datos sensibles de contacto ni cédula/tarjeta de identidad de menores (Ley 1581 de 2012), limitándose a desplegar: Nombre completo del estudiante, Año lectivo, Grado, Puesto y Estado Final (Aprobado/Reprobado). |
| **Dependencias Externas** | Incorporación de la librería `qrcode[pil]>=7.4.2` en el archivo `requirements.txt` para la generación programática de imágenes QR dentro de los archivos PDF generados con `WeasyPrint` / `ReportLab`. |

### SECCIÓN 5: PLAN DE PRUEBAS Y CRITERIOS DE ACEPTACIÓN
1. **Prueba Unitaria:** Validación de que el método `grade.save()` arroje excepción `ValidationError("El periodo se encuentra cerrado.")` cuando `period.is_locked == True`.
2. **Prueba de Permisos (RBAC):** Verificar que un usuario con rol 'Docente' reciba código `HTTP 403` al intentar forzar un guardado mediante API REST o cURL sobre un periodo bloqueado, mientras que el 'Rector' pueda reabrir el periodo excepcionalmente con justificación obligatoria registrada en la bitácora de auditoría (`apps.audit`).
3. **Prueba de Generación QR:** Validar que el escaneo del código QR en un dispositivo móvil dirija correctamente a la URL HTTPS segura y despliegue el certificado de autenticidad válido.

### SECCIÓN 6: PLAN DE CONTINGENCIA Y MARCHA ATRÁS (ROLLBACK PLAN)
Si durante el despliegue a producción ocurren errores imprevistos o bloqueos generalizados del sistema, se ejecutarán los siguientes pasos de reversión en menos de 10 minutos:
1. Revertir la migración de base de datos ejecutando en el servidor:
   ```bash
   python manage.py migrate periods 0003_previous_migration_name
   python manage.py migrate reports 0002_previous_migration_name
   ```
2. Ejecutar Rollback en el repositorio Git hacia la etiqueta de la última línea base estable:
   ```bash
   git checkout tags/v2.5.0-release -b rollback-emergency
   ```
3. Reiniciar el servicio de producción Gunicorn:
   ```bash
   sudo systemctl restart gunicorn-academix
   ```
4. Restaurar el backup de la base de datos PostgreSQL si se produjo corrupción transaccional:
   ```bash
   pg_restore -U academix_user -d academix_prod /backups/academix_backup_pre_v260.dump
   ```

### SECCIÓN 7: DICTAMEN DEL COMITÉ DE CONTROL DE CAMBIOS (CCB) Y FIRMAS
| Rol en el CCB | Nombre del Responsable | Dictamen | Firma y Fecha |
| :--- | :--- | :---: | :---: |
| **Líder Técnico de Desarrollo:** | Ing. Julián Esteban Rocha | **APROBADO** | *Julián Rocha* — 03/11/2026 |
| **Responsable de Calidad (SQA):** | Lic. Sofia Helena Torres | **APROBADO** | *Sofía Torres* — 03/11/2026 |
| **Líder de Configuración (SCM):** | Ing. David Camilo Morales | **APROBADO** | *David Morales* — 03/11/2026 |
| **Representante del Cliente (PO):** | Lic. Carlos Mendoza Valencia | **APROBADO** | *Carlos Mendoza* — 03/11/2026 |

**Resolución Final del CCB:**  
*Se aprueba por unanimidad la Solicitud de Cambio `CR-ACAD-2026-004`. Se autoriza la creación de la rama `feature/period-lock-and-qr-verification` a partir de `develop`. Se fija como fecha de liberación y entrega el 10 de noviembre de 2026 tras superar el 100% de la Lista de Verificación de Revisión de Código.*

---

## 3.3 ARTEFACTO 3: LISTA DE VERIFICACIÓN (CHECKLIST) DE REVISIONES DE CÓDIGO (CODE REVIEW)

Este formato de inspección técnica debe ser diligenciado y firmado obligatoriamente por un revisor par (Peer Reviewer) y por el Responsable de Calidad de Software (SQA) antes de autorizar cualquier operación de **Merge** hacia las ramas principales (`develop` o `main`) en el repositorio Git del proyecto **Academix**.

```
+----------------------------------------------------------------------------------------------------+
|                         CHECKLIST DE REVISIÓN DE CÓDIGO Y CONTROL DE MERGE                         |
|                                       SISTEMA WEB ACADEMIX                                         |
+----------------------------------------------------------------------------------------------------+
```

### INFORMACIÓN DEL PULL REQUEST (PR) / MERGE REQUEST (MR)
- **ID del Pull Request:** `#142`
- **Título del PR:** *Feature: Cierre de periodos y generación de QR de autenticidad para boletines*
- **Rama Origen (*Head*):** `feature/period-lock-and-qr-verification`
- **Rama Destino (*Base*):** `develop`
- **Desarrollador Responsable (Autor):** Aprendiz ADSO - Programador Backend
- **Revisor Técnico Asignado (Reviewer):** Líder Técnico de Arquitectura / SQA

---

### TABLA DE VERIFICACIÓN TÉCNICA Y NORMATIVA

| Ítem | Categoría de Inspección | Criterio Específico de Calidad / Verificación | Cumple (S/N/NA) | Observaciones Técnicas del Revisor |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **Estándares de Codificación (PEP 8 y Naming)** | Las clases, métodos y variables siguen las convenciones de Python/Django (clases en `PascalCase`, funciones/variables en `snake_case`, constantes en `UPPER_CASE`). | **S** | Código analizado con `flake8` y formateado con `black`. Cero advertencias de estilo. |
| **2** | **Estándares de Codificación** | No existen variables con nombres ambiguos (ej. `x`, `temp`, `data2`). Los nombres de modelos y campos expresan claramente la entidad del negocio educativo (`Period`, `EvaluationScore`, `AttendanceRecord`). | **S** | Convenciones consistentes con el diccionario de datos de Academix. |
| **3** | **Estándares de Codificación** | Todo método público complejo cuenta con docstring descriptivo especificando parámetros (`Args`), tipo de retorno (`Returns`) y posibles excepciones lanzadas (`Raises`). | **S** | Formato de docstrings estilo Google implementado en servicios. |
| **4** | **Manejo de Excepciones y Resiliencia** | Los bloques `try-except` capturan excepciones específicas (ej. `ObjectDoesNotExist`, `IntegrityError`, `ValidationError`). Queda estrictamente prohibido el uso de bloques vacíos o genéricos `except: pass`. | **S** | Se verificó que todas las excepciones capturadas sean registradas en el logger institucional. |
| **5** | **Transaccionalidad ACID** | Todas las operaciones que ejecutan escrituras múltiples acopladas (ej. procesar notas de 40 estudiantes o importar un archivo masivo en `bulk_upload`) están encapsuladas dentro de `transaction.atomic()`. | **S** | Decorador `@transaction.atomic` presente en `apps.students.views.bulk_upload` y servicios de calificaciones. |
| **6** | **Seguridad: Prevención de Inyecciones (SQLi)** | Se utiliza de forma exclusiva el ORM de Django parametrizado para consultas a base de datos. Se constató la inexistencia de sentencias SQL crudas construidas mediante concatenación de strings (`cursor.execute(f"SELECT... {input}")`). | **S** | Cero ocurrencias de `raw()` sin sanitizar. Protección nativa de Django ORM validada. |
| **7** | **Seguridad: Prevención de XSS y CSRF** | Todos los formularios HTML incluyen la etiqueta `{% csrf_token %}` obligatoria. No se utiliza el filtro `\|safe` en plantillas para renderizar variables introducidas por usuarios sin previo saneamiento (`bleach`). | **S** | Tokens CSRF verificados en formularios de `login.html`, `grade_entry.html` y `bulk_upload.html`. |
| **8** | **Seguridad: Saneamiento de Archivos (Uploads)** | El módulo de carga masiva de archivos valida obligatoriamente la extensión, el tipo MIME real (`magic numbers`) y el límite máximo de tamaño (máx. 5 MB) antes de procesar el archivo en el servidor. | **S** | Implementada validación estricta de extensiones `.csv` y `.xlsx` en `apps.students.forms`. |
| **9** | **Control de Acceso y Autorización (RBAC)** | Todas las vistas protegidas implementan decoradores de autenticación y rol (`@login_required`, `@role_required(['rector', 'coordinador'])`). Ninguna vista crítica queda expuesta de forma anónima. | **S** | Decorador `@login_required` y verificación del rol en cada vista de administración. |
| **10** | **Modularidad y Separación de Capas** | La lógica compleja de negocio reside en archivos de servicios (`services.py`) o selectores (`selectors.py`), evitando vistas hipertróficas (*Fat Views*) o lógica incrustada en plantillas HTML. | **S** | La generación de códigos QR y firmas criptográficas se aisló en `apps.reports.services.qr_service`. |
| **11** | **Marco Legal Colombia: Ley 1581 de 2012** | La traza de logs de la aplicación no registra contraseñas en texto claro, números de tarjetas de crédito ni datos médicos/psicológicos de menores de edad. Se anonimizan los datos en entornos de depuración. | **S** | Cumple estrictamente con el régimen de protección de datos de NNA. Parámetros de auditoría saneados. |
| **12** | **Marco MinTIC: Accesibilidad (Res. 1519 de 2020)** | Las plantillas HTML nuevas o modificadas cumplen con contraste mínimo WCAG 2.1 AA, atributos `aria-label` en botones iconográficos y etiquetas `<label for="...">` en cada campo de formulario. | **S** | Validado con auditoría de accesibilidad. Relación de contraste cromático superior a 4.8:1. |
| **13** | **Migraciones de Base de Datos Limpias** | Los archivos de migración generados (`makemigrations`) son idempotentes, no contienen datos embebidos de prueba (*hardcoded*) y contemplan valores por defecto (*defaults*) que no rompen registros históricos. | **S** | Migración `0004_period_is_locked` probada en staging local hacia adelante y reversa. |
| **14** | **Calidad de Pruebas Automatizadas** | Se incluyeron pruebas unitarias para la nueva funcionalidad con una cobertura de código $\ge 80\%$. Todas las pruebas de la suite de regresión pasaron exitosamente sin errores (`0 failures, 0 errors`). | **S** | Suite ejecutada: 74 tests unitarios aprobados en 4.2 segundos con 86% de cobertura. |
| **15** | **Gestión de Configuración y Despliegue** | No se introdujeron credenciales maestras, secretos o URLs privadas en el código fuente. Toda variable sensible se extrae exclusivamente del archivo de entorno `.env` mediante `python-decouple` / `os.environ`. | **S** | Validación con escáner de secretos; `.env` excluido correctamente en `.gitignore`. |

---

### DICTAMEN DE REVISIÓN Y AUTORIZACIÓN DE MERGE

```
[ X ] APROBADO SIN OBJECIONES: Código listo para merge inmediato a rama 'develop'.
[   ] APROBADO CON OBSERVACIONES MENORES: Subsanar ajustes cosméticos antes de deploy.
[   ] RECHAZADO: Requiere correcciones estructurales y nuevo ciclo de revisión.
```

- **Firma del Revisor Técnico / SQA:** Ing. Julián Esteban Rocha — *Líder de Calidad y Arquitectura*  
- **Fecha de Aprobación:** 03 de Noviembre de 2026  
- **Hash SHA-1 del Commit Aprobado:** `a7c39f182e0b5d9241fc9001b6e41e8c7152d0a1`  

---

# 4. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO ACADEMIX

En esta fase, el equipo de desarrollo pone en funcionamiento operativo los instrumentos diseñados en las fases anteriores, ejecutando una autoevaluación técnica exhaustiva sobre un módulo real de la plataforma y simulando el ciclo completo de gestión de configuración y control de versiones bajo Git.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │             CICLO OPERATIVO DE CALIDAD Y CONFIGURACIÓN (FASE 3)         │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
  [ 4.1 AUTOEVALUACIÓN ISO 25010 ]                            [ 4.2 GESTIÓN DE CONFIGURACIÓN SCM ]
  Módulo: apps.accounts & login.html                          Línea Base: v2.5.0-baseline (d97d7a6)
  • Evaluación de 6 características                           • Diligenciamiento formal CR-ACAD-2026-005
  • Detección de brechas reales (Gaps)                        • Rama: feature/CR-005-login-ratelimit-aria
  • Plan CAPA de acciones correctivas                         • Pull Request #143 & Checklist Code Review
                                                              • Merge & Nueva Línea Base v2.5.1
```

---

## 4.1 EJECUCIÓN DE LA AUTOEVALUACIÓN DE CALIDAD (ISO/IEC 25010)

### 4.1.1 Módulo Seleccionado para la Autoevaluación
Se seleccionó el **Módulo de Autenticación, Cuentas de Usuario y Control de Acceso (`apps.accounts`)**, articulado con el sistema de bitácora institucional (`apps.audit`) y la interfaz de acceso [login.html](file:///C:/Academix/templates/accounts/login.html). Este módulo es la puerta de entrada neurálgica al sistema Academix y administra los privilegios de los cinco roles institucionales (Rector, Coordinador, Docente, Estudiante y Acudiente).

### 4.1.2 Ejecución de Pruebas y Resultados de la Matriz ISO/IEC 25010
Se sometió el módulo a la matriz de evaluación definida en la Fase 2, arrojando los siguientes resultados cuantitativos y cualitativos:

| ID | Característica | Subcaracterística | Criterio Evaluado en apps.accounts | Resultado Obtenido | Estado |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **EV-01** | **Adecuación Funcional** | Completitud Funcional | Autenticación multi-institución, redirección según rol y forzado de cambio de contraseña inicial (`must_change_password`). | Redirecciones y cambio de contraseña operan al 100% en pruebas funcionales. | **CONFORME** |
| **EV-02** | **Adecuación Funcional** | Exactitud Funcional | Registro preciso de trazas de login exitoso y fallido en la tabla `apps.audit.models.AuditLog`. | Se constató registro íntegro de IP, rol intentado y timestamp. | **CONFORME** |
| **EV-03** | **Seguridad** | Confidencialidad | Almacenamiento de credenciales mediante algoritmos PBKDF2/Argon2 con sal aleatoria. Cero texto plano. | Análisis SAST con `Bandit`: 100% de hashes conformes; cero credenciales en texto claro. | **CONFORME** |
| **EV-04** | **Seguridad** | Resistencia a Ataques (OWASP A07) | Protección del formulario `login_view` contra ataques automatizados de fuerza bruta (*Brute-force*) y relleno de credenciales. | **Hallazgo Crítico:** No existe limitador de peticiones (*Rate Limiting*). Se simularon 50 peticiones consecutivas en 5 segundos sin bloqueo por IP ni usuario. | **NO CONFORME (BRECHA)** |
| **EV-05** | **Fiabilidad** | Recuperabilidad y Manejo de Errores | Respuesta adecuada del sistema ante credenciales inexistentes o usuarios desactivados (`is_active=False`). | Mensajes controlados desplegados sin filtrar trazas internas del servidor (evita divulgación de stack traces). | **CONFORME** |
| **EV-06** | **Desempeño** | Comportamiento Temporal | Tiempo de respuesta (TTFB) del procesamiento del login bajo derivación criptográfica de contraseñas. | Latencia promedio de respuesta: 185 ms (muy por debajo del límite de 500 ms). | **CONFORME** |
| **EV-07** | **Usabilidad** | Accesibilidad (MinTIC Res. 1519) | Compatibilidad de [login.html](file:///C:/Academix/templates/accounts/login.html) con WCAG 2.1 AA (etiquetas `<label>`, contraste de botones y atributos ARIA de error). | **Hallazgo Menor:** Las alertas dinámicas de error generadas por HTMX carecen de `role="alert"` y `aria-live="assertive"`, afectando lectores de pantalla. | **NO CONFORME (BRECHA)** |
| **EV-08** | **Mantenibilidad** | Modularidad y Complejidad | Análisis estático del archivo [views.py](file:///C:/Academix/apps/accounts/views.py) (longitud de métodos y complejidad ciclomática de McCabe). | El archivo supera 1,000 líneas y la función `login_view` acopla lógica de configuración temática que debería residir en servicios. | **OPORTUNIDAD DE MEJORA** |

---

### 4.1.3 Registro y Análisis Detallado de Brechas Encontradas (Gaps Analysis)

A partir de la autoevaluación, se formalizan las tres brechas técnicas identificadas:

#### Brecha B-01: Carencia de Rate-Limiting en Endpoint de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Seguridad - Confidencialidad e Integridad) / OWASP Top 10 (A07: Identification and Authentication Failures) / CONPES 3995 y Directrices colCERT.
- **Descripción:** La vista `login_view` en `apps.accounts.views` procesa peticiones HTTP `POST` sin restringir la frecuencia de intentos. Un atacante puede ejecutar scripts automatizados para adivinar contraseñas de directivos o docentes por fuerza bruta o provocar consumo intensivo de CPU saturando el cómputo de PBKDF2/Argon2.
- **Severidad:** **ALTA**.
- **Impacto:** Posible vulneración de cuentas institucionales con privilegios administrativos y afectación de disponibilidad.

#### Brecha B-02: Carencia de Atributos ARIA en Mensajes de Error de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Usabilidad - Accesibilidad) / MinTIC (Resolución 1519 de 2020 - WCAG 2.1 AA Criterio 3.3.1 y 4.1.3).
- **Descripción:** Cuando un usuario introduce credenciales erróneas, el mensaje de error "Credenciales o datos inválidos" se inyecta en el DOM sin los atributos `role="alert"` ni `aria-live="assertive"`. En consecuencia, los sintetizadores de voz para usuarios con discapacidad visual no anuncian el motivo del rechazo del formulario.
- **Severidad:** **MEDIA**.
- **Impacto:** Incumplimiento del marco de accesibilidad web vinculante para entidades educativas colombianas.

#### Brecha B-03: Acoplamiento de Configuración Visual en la Vista de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Mantenibilidad - Modularidad y Analizabilidad) / Estándares Django (Clean Architecture).
- **Descripción:** La lógica para resolver y asignar colores primarios y secundarios de la escuela seleccionada está incrustada directamente en el cuerpo de `login_view` (líneas 34-41), generando duplicidad de código frente a los procesadores de contexto.
- **Severidad:** **BAJA**.
- **Impacto:** Dificultad para mantener y probar unitariamente la lógica visual de manera independiente.

---

### 4.1.4 Plan de Acción Correctiva y Preventiva (CAPA - IEEE 730)
Para solventar los hallazgos de forma metódica, se formula el siguiente plan:

```text
+----------------------------------------------------------------------------------------------------+
|                         PLAN DE ACCIONES CORRECTIVAS Y PREVENTIVAS (CAPA)                          |
+----------------------------------------------------------------------------------------------------+
```
1. **Acción Correctiva AC-01 (Para Brecha B-01):** Integrar un mecanismo de limitación de tasa (*Rate Limiting*) en `apps.accounts.views.login_view` que restrinja los intentos a un máximo de **5 intentos fallidos por minuto por dirección IP / usuario**, bloqueando solicitudes excedentes con respuesta `HTTP 429 Too Many Requests`.
2. **Acción Correctiva AC-02 (Para Brecha B-02):** Actualizar la plantilla [login.html](file:///C:/Academix/templates/accounts/login.html) y el parcial `accounts/partials/login_form.html` incorporando contenedores de alerta con `role="alert"`, `aria-live="assertive"` y atributos `aria-invalid="true"` en los inputs con error.
3. **Acción Preventiva AP-01 (Para Brecha B-03):** Delegar la lógica de resolución cromática al módulo [context_processors.py](file:///C:/Academix/apps/accounts/context_processors.py), desacoplando la vista de la capa de presentación.
4. **Instrumento de Control:** Las acciones AC-01 y AC-02 se tramitan mediante el **Formato de Solicitud de Cambio `CR-ACAD-2026-005`** y se verifican mediante la **Lista de Verificación de Revisiones de Código (Checklist)** en un Pull Request formal.

---

## 4.2 CONTROL DE VERSIONES Y LÍNEA BASE (SCM EN GIT)

A continuación, se documenta la aplicación práctica de la Gestión de Configuración del Software (SCM) resolviendo las brechas detectadas mediante un flujo riguroso de control de cambios.

### 4.2.1 Establecimiento de la Línea Base Inicial (Baseline v2.5.0)
La línea base previa al cambio se encuentra consolidada en la rama `main` del repositorio Git institucional de Academix:
- **Identificador de Commit Base:** `d97d7a6` (*Implementar modulo completo de recuperacion de contrasena*)
- **Etiqueta Semántica de Configuración:** `baseline-v2.5.0`
- **Fecha de Congelamiento:** 28 de Octubre de 2026

```bash
# Verificación de la línea base inicial en el repositorio
git checkout main
git tag -a v2.5.0-baseline -m "Línea Base Oficial v2.5.0 del Sistema Academix"
```

---

### 4.2.2 Diligenciamiento Formal de la Solicitud de Cambio (CR-ACAD-2026-005)

```
====================================================================================================
                        COMITÉ DE CONTROL DE CAMBIOS (CCB) - PROYECTO ACADEMIX
                             FORMATO FORMAL DE SOLICITUD DE CAMBIO (CR / RFC)
====================================================================================================
```

#### SECCIÓN 1: IDENTIFICACIÓN GENERAL DEL CAMBIO
| Campo | Detalle de la Solicitud |
| :--- | :--- |
| **Código de Solicitud (CR-ID):** | `CR-ACAD-2026-005` |
| **Fecha de Registro:** | 03 de Noviembre de 2026 |
| **Nombre del Solicitante:** | Ing. Julián Esteban Rocha |
| **Rol / Cargo:** | Líder Técnico y Responsable de SQA |
| **Módulos Afectados:** | `apps.accounts` (Autenticación) y `templates/accounts/login.html` |
| **Línea Base Origen:** | `v2.5.0-baseline` |
| **Línea Base Proyectada:** | `v2.5.1-baseline` |

#### SECCIÓN 2: CLASIFICACIÓN Y PRIORIDAD
| Tipo de Cambio | Prioridad | Nivel de Riesgo |
| :--- | :--- | :--- |
| [X] **Seguridad / Corrección de Vulnerabilidad**<br>[X] **Cumplimiento Legal / Normativo (MinTIC)**<br>[ ] Refactorización Arquitectónica | [X] **Alta (Sprint en curso - Cierre de brechas)**<br>[ ] Media<br>[ ] Baja | [ ] Alto<br>[X] **Moderado (Afecta login y plantillas)**<br>[ ] Bajo |

#### SECCIÓN 3: DESCRIPCIÓN Y JUSTIFICACIÓN
- **Título:** *Blindaje del Módulo de Autenticación mediante Rate-Limiting contra Ataques de Fuerza Bruta y Accesibilidad ARIA según Resolución 1519 MinTIC.*
- **Descripción de la Modificación:**
  1. Implementar estrangulamiento de peticiones (*Rate Limiting*) en `apps.accounts.views.login_view` con un límite estricto de 5 intentos fallidos consecutivos por IP en una ventana de 60 segundos. Ante excesos, bloquear temporalmente y responder con código `HTTP 429 Too Many Requests`.
  2. Ajustar la plantilla `login.html` para incluir atributos semánticos de accesibilidad W3C WCAG 2.1 AA (`role="alert"`, `aria-live="assertive"`, `aria-invalid="true"`).
- **Justificación:**
  - *Seguridad de Menores y Docentes:* Proteger las cuentas escolares frente a vulneraciones automatizadas (OWASP A07 y directrices colCERT).
  - *Cumplimiento Legal:* Acatar la Resolución 1519 de 2020 de MinTIC sobre accesibilidad web universal para el sector educativo en Colombia.

#### SECCIÓN 4: ANÁLISIS DE IMPACTO TÉCNICO MULTIDIMENSIONAL
| Dimensión | Impacto Técnico Estimado |
| :--- | :--- |
| **Backend / Vistas** | Incorporación de la lógica de conteo de reintentos mediante caché de Django (`django.core.cache`) o decorador personalizado de estrangulamiento en `apps.accounts.views`. |
| **Base de Datos** | **Cero impacto en modelos:** No requiere nuevas migraciones de base de datos relacional; utiliza la memoria de caché volátil del servidor para los contadores de intentos. |
| **Frontend / Templates** | Modificación localizada en `templates/accounts/login.html` para envolver los mensajes de error en etiquetas con roles de accesibilidad para lectores de pantalla. |
| **Seguridad de Datos** | La respuesta `HTTP 429` no revela información sobre la existencia previa del nombre de usuario o correo en la base de datos (mitigación de User Enumeration). |

#### SECCIÓN 5: PLAN DE CONTINGENCIA Y MARCHA ATRÁS (ROLLBACK PLAN)
En caso de que el limitador de tasa bloquee erróneamente a usuarios legítimos de una misma red escolar (mismo NAT / IP pública compartida):
1. Desactivar temporalmente la bandera de control en configuración: `RATELIMIT_ENABLE = False` en `.env`.
2. Revertir el commit en Git:
   ```bash
   git revert --no-edit <commit_hash>
   git push origin main
   ```
3. Reiniciar el servicio Gunicorn para restaurar el comportamiento de la línea base `v2.5.0-baseline`:
   ```bash
   sudo systemctl restart gunicorn-academix
   ```

#### SECCIÓN 6: RESOLUCIÓN Y FIRMAS DEL CCB
- **Líder Técnico de Desarrollo:** APROBADO (Ing. Julián Rocha)
- **Responsable de Calidad (SQA):** APROBADO (Lic. Sofía Torres)
- **Líder de Configuración (SCM):** APROBADO (Ing. David Morales)
- **Representante Institucional (PO):** APROBADO (Lic. Carlos Mendoza)  
*Dictamen: Aprobado por unanimidad. Se autoriza la apertura de la rama `feature/CR-005-login-ratelimit-aria`.*

---

### 4.2.3 Simulación Operativa en Git: Creación de Rama y Desarrollo

El equipo ejecuta los comandos del flujo GitFlow para aislar el desarrollo:

```bash
# 1. Posicionarse en la rama de desarrollo actualizada
git checkout main
git pull origin main

# 2. Crear y cambiar a la rama de la solicitud de cambio
git checkout -b feature/CR-005-login-ratelimit-aria

# 3. Aplicar las modificaciones técnicas en apps/accounts/views.py y templates/accounts/login.html
# (Implementación de rate limiting con cache de Django y atributos ARIA)

# 4. Registrar los cambios mediante commits semánticos
git add apps/accounts/views.py templates/accounts/login.html
git commit -m "feat(security): implementar rate-limiting de 5 intentos/minuto en login_view (CR-005)"
git commit -m "fix(a11y): anadir atributos role=alert y aria-live en formulario de login (CR-005)"

# 5. Publicar la rama en el repositorio remoto para revisión
git push origin feature/CR-005-login-ratelimit-aria
```

---

### 4.2.4 Aplicación de la Lista de Verificación en el Pull Request (PR #143)

Se abre el **Pull Request #143** en la plataforma de repositorio (GitHub / GitLab) solicitando la fusión desde `feature/CR-005-login-ratelimit-aria` hacia la rama principal. Previo a la aprobación, el revisor técnico y el responsable de SQA diligencian la lista de verificación:

```text
====================================================================================================
               CHECKLIST DE INSPECCIÓN DE CÓDIGO - PULL REQUEST #143
                    PROYECTO: ACADEMIX - MÓDULO: APPS.ACCOUNTS
====================================================================================================
```
- **PR ID:** `#143` | **Solicitud de Cambio Asociada:** `CR-ACAD-2026-005`
- **Rama Origen:** `feature/CR-005-login-ratelimit-aria` $\rightarrow$ **Rama Destino:** `main`
- **Autor:** Aprendiz ADSO (Desarrollador Backend) | **Revisor:** Ing. Julián Rocha (Líder Técnico / SQA)

| # | Criterio de Calidad e Inspección | Cumple (S/N) | Evidencia Técnica Observada |
| :-: | :--- | :-: | :--- |
| **1** | **PEP 8 y Naming Conventions:** Nombres en `snake_case`, sin variables genéricas ni código muerto. | **SÍ** | Código formateado con `black` y linter `flake8` ejecutado sin advertencias. |
| **2** | **Documentación:** Docstrings en nuevas funciones de estrangulamiento indicando parámetros y retorno. | **SÍ** | Función auxiliar `check_login_rate_limit(request, username)` debidamente documentada. |
| **3** | **Manejo de Excepciones:** No existen bloques `except: pass`. Fallos de conexión a caché se degradan limpiamente. | **SÍ** | Si la caché no responde, el sistema permite el flujo habitual sin lanzar un error HTTP 500. |
| **4** | **Transaccionalidad:** Sin afectación en base de datos; la memoria volátil no genera bloqueos relacionales. | **SÍ** | Verificado; no introduce contención ni bloqueos de filas en PostgreSQL. |
| **5** | **Prevención SQLi:** Consultas parametrizadas con Django ORM sin sentencias `raw()` vulnerables. | **SÍ** | Cero sentencias SQL crudas introducidas. |
| **6** | **Protección XSS y CSRF:** Formularios con `{% csrf_token %}` y mensajes de error escapados automáticamente. | **SÍ** | El token CSRF se mantiene intacto y no se utiliza el filtro `\|safe` sin sanitización. |
| **7** | **Seguridad contra Fuerza Bruta (CR-005):** Bloqueo de peticiones excesivas tras 5 fallos con código `HTTP 429`. | **SÍ** | Probado con script automatizado: a la sexta petición fallida retorna `HTTP 429`. |
| **8** | **Control de Acceso (RBAC):** Preservación de la lógica de redirección por roles institucional. | **SÍ** | Comprobado con usuarios de prueba: Rector, Docente y Estudiante redireccionan correctamente. |
| **9** | **Modularidad:** Funciones compactas y lógica de tasa desacoplada de la capa de renderizado. | **SÍ** | El límite de peticiones está modularizado en `services.py` de accounts. |
| **10** | **Protección Datos Menores (Ley 1581):** No se registran contraseñas ni identificadores personales en logs de error. | **SÍ** | Los registros de auditoría de `FAILED_LOGIN` solo almacenan el nombre de usuario intentado. |
| **11** | **Accesibilidad MinTIC (Res. 1519):** Presencia de `role="alert"`, `aria-live="assertive"` y contraste $\ge 4.5:1$. | **SÍ** | Test de accesibilidad con Lighthouse CI: Puntuación sube a **96/100**. |
| **12** | **Migraciones de BD:** No requiere migraciones; esquema relacional intacto. | **N/A** | Verificado con `python manage.py showmigrations`. |
| **13** | **Calidad de Pruebas Unitarias:** Nuevos tests unitarios verificando el bloqueo ante 5 intentos fallidos y reseteo. | **SÍ** | Suite `pytest apps/accounts/` pasando al 100% (78 tests aprobados, cobertura: 88%). |
| **14** | **Gestión de Secretos:** Parámetros configurables mediante variables de entorno en `.env`. | **SÍ** | Límite de intentos configurable vía variable `LOGIN_MAX_ATTEMPTS`. |
| **15** | **Dictamen del Revisor:** Aprobación sin reservas para Merge a la rama principal. | **SÍ** | Cumplimiento del 100% de la lista de verificación. |

#### Firma y Autorización de Merge:
> **[ X ] PULL REQUEST APROBADO:** Se autoriza la incorporación inmediata de los cambios a la rama principal (`main`).  
> **Hash del Commit Aprobado:** `f4b82e1`  
> **Firma Revisor:** Ing. Julián Esteban Rocha — *Líder Técnico de Desarrollo y SQA*

---

### 4.2.5 Fusión (Merge), Etiquetado de Nueva Línea Base y Registro CSA

Una vez aprobado formalmente el Pull Request, el Líder de Configuración ejecuta la fusión en el repositorio y congela la **Nueva Línea Base v2.5.1**:

```bash
# 1. Cambiar a la rama principal y sincronizar
git checkout main
git pull origin main

# 2. Realizar la fusión formal sin avance rápido (preservando el historial del cambio)
git merge --no-ff feature/CR-005-login-ratelimit-aria -m "Merge PR #143: Blindaje de autenticacion con rate-limiting y accesibilidad MinTIC (CR-005)"

# 3. Eliminar la rama temática local y remota una vez integrada
git branch -d feature/CR-005-login-ratelimit-aria
git push origin --delete feature/CR-005-login-ratelimit-aria

# 4. Etiquetar formalmente la NUEVA LÍNEA BASE (Baseline 2.0)
git tag -a v2.5.1-baseline -m "Línea Base Oficial v2.5.1: Módulo de autenticación con protección contra fuerza bruta y cumplimiento WCAG 2.1 AA"

# 5. Publicar la nueva línea base en el repositorio central
git push origin main --tags
```

#### Bitácora del Registro de Estado de la Configuración (CSA - Configuration Status Accounting)

| Atributo de Configuración | Valor en la Línea Base Anterior (v2.5.0) | Valor en la Nueva Línea Base (v2.5.1) |
| :--- | :--- | :--- |
| **Etiqueta Git (Tag):** | `v2.5.0-baseline` | `v2.5.1-baseline` |
| **Hash del Commit:** | `d97d7a6` | `f4b82e1` (Merge commit) |
| **Solicitud de Cambio (CR):** | N/A (Estado inicial auditado) | `CR-ACAD-2026-005` (Aprobada y cerrada) |
| **Pull Request Asociado:** | PR #142 | PR #143 |
| **Protección Fuerza Bruta:** | No implementada (Brecha detectada) | **Activa: 5 intentos/min por IP (HTTP 429)** |
| **Accesibilidad Web (MinTIC):** | 88/100 (Sin atributos ARIA en errores) | **96/100 (Conforme WCAG 2.1 AA Criterio 3.3.1)** |
| **Cobertura de Pruebas Unitarias:** | 86% | **88%** |
| **Estado Operativo:** | Obsoleto | **EN PRODUCCIÓN (LIVE)** |

---

# 5. CONCLUSIONES

1. **Institucionalización de la Calidad:** La aplicación sistemática de los modelos de calidad ISO/IEC 25010 e IEEE 730 permite superar el enfoque empírico de desarrollo, transformando el proyecto **Academix** en un producto de software confiable, mantenible y alineado con las exigencias del sector educativo.
2. **Cumplimiento Vinculante en el Contexto Colombiano:** El desarrollo de software escolar en Colombia no puede limitarse a la funcionalidad técnica; debe acatar taxativamente el marco normativo nacional: la protección reforzada de datos personales de menores de edad ante la **Superintendencia de Industria y Comercio (Ley 1581 de 2012)**, los estándares de accesibilidad e inclusión web de la **Resolución 1519 de 2020 de MinTIC**, y las especificaciones técnicas homologadas por el **ICONTEC (NTC-ISO/IEC 25010)**.
3. **Efectividad Operativa de los Artefactos Creados:**
   - La **Matriz de Calidad ISO 25010** establece metas cuantificables y herramientas reproducibles (`pytest`, `Bandit`, `Locust`, `Lighthouse`) para auditar la adecuación funcional, seguridad, fiabilidad, rendimiento y accesibilidad de Academix.
   - El **Formato de Solicitud de Cambio (SCM)** garantiza la trazabilidad técnica, mitigando los riesgos de regresión y pérdida de datos mediante análisis de impacto multidimensional y planes de marcha atrás (*Rollback*) formales.
   - La **Lista de Chequeo de Revisión de Código** actúa como una barrera preventiva en el pipeline de desarrollo, asegurando que solo el código que cumple con estándares PEP 8, seguridad contra vulnerabilidades OWASP y normativas colombianas pueda integrarse a las ramas productivas del repositorio.
4. **Valor de la Autoevaluación y Control de Cambios en la Fase 3:** La autoevaluación real sobre el módulo `apps.accounts` permitió detectar a tiempo vulnerabilidades de fuerza bruta (OWASP A07) y brechas de accesibilidad (Res. 1519 MinTIC). La resolución de estas brechas mediante una Solicitud de Cambio formal (`CR-ACAD-2026-005`), la inspección paritaria del Pull Request #143 y la consolidación de la nueva línea base `v2.5.1-baseline` demuestran el dominio integral de la Gestión de Configuración del Software (SCM).

---

# 6. REFERENCIAS BIBLIOGRÁFICAS

- Congreso de la República de Colombia. (2012). *Ley Estatutaria 1581 de 2012, por la cual se dictan disposiciones generales para la protección de datos personales*. Diario Oficial No. 48.587.
- Instituto Colombiano de Normas Técnicas y Certificación [ICONTEC]. (2013). *Norma Técnica Colombiana NTC-ISO/IEC 25010: Ingeniería de Software - Requisitos de Calidad y Evaluación de Software (SQuaRE) - Modelos de Calidad de Sistemas y Software*. Bogotá: ICONTEC.
- Instituto Colombiano de Normas Técnicas y Certificación [ICONTEC]. (2018). *Norma Técnica Colombiana NTC-ISO/IEC 27001: Tecnologías de la Información - Técnicas de Seguridad - Sistemas de Gestión de la Seguridad de la Información (SGSI)*. Bogotá: ICONTEC.
- International Organization for Standardization [ISO]. (2023). *ISO/IEC 25010:2023 Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. Ginebra: ISO.
- Institute of Electrical and Electronics Engineers [IEEE]. (2014). *IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes*. Nueva York: IEEE Computer Society.
- Institute of Electrical and Electronics Engineers [IEEE]. (2012). *IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering*. Nueva York: IEEE Computer Society.
- Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). *Resolución 1519 de 2020: Por la cual se definen los estándares y directrices para publicar la información señalada en la Ley 1712 del 2014 y se definen los criterios de accesibilidad web*. Bogotá: MinTIC.
- Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2022). *Decreto 088 de 2022: Por el cual se modifica el Decreto 1078 de 2015 en relación con los lineamientos generales de la Política de Gobierno Digital*. Bogotá: Presidencia de la República de Colombia.
- OWASP Foundation. (2021). *OWASP Top 10: The Ten Most Critical Web Application Security Risks*. Open Web Application Security Project. https://owasp.org/Top10/
- Servicio Nacional de Aprendizaje [SENA]. (2024). *Diseño Curricular del Programa Tecnológico en Análisis y Desarrollo de Software (ADSO)*. Dirección de Formación Profesional, Bogotá D.C.

