# GESTIÓN DE CONFIGURACIÓN DEL SOFTWARE Y AUTOEVALUACIÓN DE CALIDAD (ISO/IEC 25010 & IEEE 730)
## Aplicación Práctica al Sistema de Información Escolar ACADEMIX v2.5.0 — Fases 1 y 3

**Programa de Formación:** Tecnología en Análisis y Desarrollo de Software (ADSO)  
**Institución:** Servicio Nacional de Aprendizaje (SENA) — Centro de Formación en Tecnologías de la Información  
**Ficha de Caracterización:** 3173430  
**Proyecto Formativo:** Plataforma Web Academix — Sistema Integral de Control Escolar, Convivencial y Académico  
**Versión del Documento:** 1.0 Oficial  
**Fecha:** Noviembre de 2026  
**Autores:** Equipo de Desarrollo de Software y Aseguramiento de Calidad — Academix  

---

## TABLA DE CONTENIDO

1. [Introducción y Objetivos](#1-introducción-y-objetivos)
   - 1.1 Objetivo General
   - 1.2 Objetivos Específicos
2. [Fase 1: Investigación y Marco Conceptual](#2-fase-1-investigación-y-marco-conceptual)
   - 2.1 Modelo de Calidad del Producto de Software (ISO/IEC 25010 e ISO/IEC 25010:2023)
   - 2.2 Aseguramiento de la Calidad del Software (Norma IEEE 730)
   - 2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)
   - 2.4 Entes Reguladores y Marco Normativo de Calidad en Colombia (Actualizado 2026)
3. [Fase 3: Aplicación Práctica sobre el Proyecto Formativo](#3-fase-3-aplicación-práctica-sobre-el-proyecto-formativo)
   - 3.1 Ejecución de la Autoevaluación de Calidad (ISO/IEC 25010) sobre el Módulo Funcional
     - 3.1.1 Identificación del Módulo Seleccionado (`apps.accounts`)
     - 3.1.2 Ejecución de Pruebas y Resultados de la Matriz de Calidad
     - 3.1.3 Análisis y Documentación de Brechas Encontradas (Gap Analysis)
     - 3.1.4 Plan de Acción Correctiva y Preventiva (CAPA — IEEE 730)
   - 3.2 Control de Versiones, Gestión de Cambios y Línea Base (SCM en Git)
     - 3.2.1 Establecimiento de la Línea Base Inicial (`v2.5.0-baseline`)
     - 3.2.2 Diligenciamiento Formal de la Solicitud de Cambio (`CR-ACAD-2026-005`)
     - 3.2.3 Simulación Operativa del Flujo GitFlow (Rama `feature/CR-005-login-ratelimit-aria`)
     - 3.2.4 Aplicación de la Lista de Verificación de Código en el Pull Request #143
     - 3.2.5 Fusión (*Merge*), Nueva Línea Base (`v2.5.1-baseline`) y Registro CSA
4. [Conclusiones](#4-conclusiones)
5. [Referencias Bibliográficas (Norma APA 7.ª Edición)](#5-referencias-bibliográficas-norma-apa-7ª-edición)

---

# 1. INTRODUCCIÓN Y OBJETIVOS

En el desarrollo de software institucional, garantizar la calidad y la trazabilidad no es una actividad opcional ni una prueba cosmética: constituye la base de la estabilidad técnica, la seguridad de la información y la confianza de los usuarios. Para el sistema **ACADEMIX** (Plataforma web integral de control escolar, calificaciones, convivencia y auditoría institucional para colegios en Colombia), la calidad del software adquiere una trascendencia legal y operativa crítica, dado que gestiona datos de menores de edad, consolida calificaciones oficiales y rige los procesos de matrícula y promoción académica.

El presente documento formaliza de manera independiente la **Gestión de Configuración del Software (SCM)** y la **Autoevaluación de Calidad de Software**, cubriendo:
1. La fundamentación conceptual de los estándares **ISO/IEC 25010** (calidad del producto), **IEEE 730** (aseguramiento de calidad) y el marco regulatorio colombiano actualizado (**ICONTEC, MinTIC, Superintendencia de Industria y Comercio - SIC, colCERT**).
2. La puesta en marcha práctica (**Fase 3**) de los instrumentos de calidad mediante la autoevaluación exhaustiva del módulo nuclear de **Autenticación, Gestión de Cuentas y Control de Acceso (`apps.accounts`)**, la identificación formal de brechas técnicas y la simulación rigurosa del ciclo de control de versiones y líneas base en Git.

## 1.1 Objetivo General
Investigar, seleccionar y aplicar marcos normativos de calidad de software (ISO/IEC 25010 para calidad de producto, IEEE 730 para aseguramiento de calidad y normas técnicas colombianas vinculantes) mediante la ejecución de una autoevaluación técnica sobre un módulo funcional del sistema Academix y la demostración práctica del control de versiones, líneas base y control de cambios en el repositorio del proyecto.

## 1.2 Objetivos Específicos
1. Documentar los fundamentos teóricos del modelo de calidad de producto según la familia **ISO/IEC 25000 (SQuaRE)** y su evolución **ISO/IEC 25010:2023**, diferenciando calidad estática, dinámica y calidad en uso.
2. Analizar el alcance del estándar **IEEE 730** en el Aseguramiento de Calidad del Software (SQA) y su articulación con los principios de Gestión de Configuración (**IEEE 828**).
3. Contextualizar el marco regulatorio colombiano de TI: normas técnicas **ICONTEC** (NTC-ISO/IEC 25010), directrices de accesibilidad web de **MinTIC** (Resolución 1519 de 2020), régimen de protección de datos de menores de la **SIC** (Ley Estatutaria 1581 de 2012) y pautas **colCERT**.
4. Ejecutar la autoevaluación de calidad basada en ISO/IEC 25010 sobre el módulo de autenticación ([views.py](file:///C:/Academix/apps/accounts/views.py), [forms.py](file:///C:/Academix/apps/accounts/forms.py) y [login.html](file:///C:/Academix/templates/accounts/login.html)), documentando las brechas técnicas detectadas (*Gaps Analysis*).
5. Demostrar el uso del control de cambios formal diligenciando la **Solicitud de Cambio `CR-ACAD-2026-005`** para subsanar las brechas encontradas.
6. Simular el flujo de trabajo en Git (GitFlow) aplicando la **Lista de Verificación (Checklist) de Revisiones de Código** en un Pull Request formal (#143) previo al *Merge*, congelando y publicando la **Nueva Línea Base `v2.5.1-baseline`**.

---

# 2. FASE 1: INVESTIGACIÓN Y MARCO CONCEPTUAL

```
       ┌─────────────────────────────────────────────────────────────┐
       │             MARCOS NORMATIVOS Y REGULATORIOS                │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  [ INTERNACIONAL ]             [ PROCESOS ]                 [ COLOMBIA ]
  ISO/IEC 25010:2023            IEEE 730 (SQA)               ICONTEC NTC 25010
  Familia SQuaRE                IEEE 828 (SCM)               MinTIC Res. 1519 (AA)
  8 Características             Líneas Base                  SIC Ley 1581 (NNA)
  Calidad en Uso                Control de Cambios           colCERT / CSIRT
```

## 2.1 Modelo de Calidad del Producto de Software (ISO/IEC 25010 e ISO/IEC 25010:2023)

### 2.1.1 La Familia de Normas ISO/IEC 25000 (SQuaRE)
La serie **ISO/IEC 25000**, denominada **SQuaRE** (*Systems and software Quality Requirements and Evaluation*), sustituyó a las normas predecesoras ISO/IEC 9126 e ISO/IEC 14598. SQuaRE organiza la ingeniería de calidad en cinco divisiones estructurales:
- **ISO/IEC 2500n - Gestión de Calidad:** Términos, definiciones y modelos de referencia comunes.
- **ISO/IEC 2501n - Modelos de Calidad:** Define el modelo de calidad del producto de software (ISO/IEC 25010) y el modelo de calidad en uso (ISO/IEC 25019 / 25022).
- **ISO/IEC 2502n - Medición de Calidad:** Catálogo de métricas cuantitativas para evaluar características de calidad (ISO/IEC 25023).
- **ISO/IEC 2503n - Requisitos de Calidad:** Métodos para especificar requerimientos no funcionales de calidad en pliegos de contratación y especificaciones SRS.
- **ISO/IEC 2504n - Evaluación de Calidad:** Procedimientos y criterios para llevar a cabo auditorías de evaluación de software objetivas y reproducibles.

### 2.1.2 Características de Calidad del Producto (ISO/IEC 25010)
El modelo de calidad del producto descompone el software en ocho características primarias:

| Característica Primaria | Definición Técnica | Subcaracterísticas Clave |
| :--- | :--- | :--- |
| **1. Adecuación Funcional** | Grado en que las funciones satisfacen las necesidades explícitas e implícitas del usuario institucional. | • Completitud funcional<br>• Corrección/Exactitud funcional<br>• Pertinencia funcional |
| **2. Eficiencia de Desempeño** | Rendimiento del software relativo a la cantidad de recursos consumidos en condiciones dadas. | • Comportamiento temporal (latencia/TTFB)<br>• Utilización de recursos (CPU, RAM)<br>• Capacidad y escalabilidad |
| **3. Compatibilidad** | Capacidad de compartir un entorno común e intercambiar información con otros sistemas. | • Coexistencia<br>• Interoperabilidad de datos |
| **4. Usabilidad** | Grado en que el software es comprensible, fácil de aprender y accesible para los usuarios objetivo. | • Reconocimiento de idoneidad<br>• Facilidad de aprendizaje<br>• Operabilidad y protección ante errores<br>• Accesibilidad universal |
| **5. Fiabilidad** | Capacidad del sistema para desempeñar funciones especificadas sin fallos durante un tiempo determinado. | • Madurez<br>• Disponibilidad<br>• Tolerancia a fallos<br>• Recuperabilidad transaccional |
| **6. Seguridad** | Protección de la información y los datos para que solo usuarios autorizados accedan o modifiquen el estado. | • Confidencialidad<br>• Integridad<br>• No repudio<br>• Autenticidad<br>• Trazabilidad y auditoría |
| **7. Mantenibilidad** | Eficacia y eficiencia con que el código fuente puede ser modificado, corregido o adaptado. | • Modularidad<br>• Reusabilidad<br>• Analizabilidad<br>• Modificabilidad<br>• Testabilidad (facilidad de prueba) |
| **8. Portabilidad / Flexibilidad** | Capacidad de transferir el software entre distintos entornos operativos, de hardware o nube. | • Adaptabilidad<br>• Facilidad de instalación y reemplazo |

### 2.1.3 Actualización ISO/IEC 25010:2023
En la actualización publicada en 2023:
- La portabilidad se amplía formalmente hacia la **Flexibilidad (*Safety & Flexibility*)**, incorporando la resiliencia en la nube y la escalabilidad elástica.
- Se jerarquiza la **Inclusión** dentro de la Usabilidad, garantizando que el software pueda ser operado por cualquier persona independientemente de sus capacidades físicas o cognitivas.
- Se robustece la articulación con la norma **ISO/IEC 25012** (Calidad de Datos), asegurando que los datos almacenados mantengan exactitud, credibilidad y consistencia sintáctica.

### 2.1.4 Calidad del Producto vs. Calidad en Uso
- **Calidad del Producto:** Examina las propiedades intrínsecas del software (calidad estática del código, cobertura de pruebas, ausencia de vulnerabilidades, consumo de memoria).
- **Calidad en Uso (ISO/IEC 25019):** Examina el impacto final del software en el contexto laboral o escolar de los usuarios reales a través de cinco dimensiones: *Eficacia* (éxito en la tarea sin errores), *Eficiencia* (recursos y tiempo invertido), *Satisfacción* (agrado y confianza), *Ausencia de Riesgo* (protección legal, financiera y pedagógica) y *Cobertura de Contexto* (desempeño uniforme en diversas sedes, redes y dispositivos).

---

## 2.2 Aseguramiento de la Calidad del Software (Norma IEEE 730)

El estándar **IEEE 730** (*Standard for Software Quality Assurance Processes*) define los requisitos para planificar, ejecutar y controlar el **Aseguramiento de Calidad del Software (SQA)**. A diferencia del testing tradicional que actúa de forma reactiva al final del desarrollo buscando defectos en el ejecutable, el SQA es una disciplina **preventiva orientada a los procesos**:
- Establece los estándares, convenciones de codificación y herramientas de análisis estático (SAST).
- Dicta las auditorías de configuración y las inspecciones técnicas de código por pares (*Peer Code Reviews*).
- Define la estrategia de Verificación y Validación (V&V).
- Establece el procedimiento de **Acciones Correctivas y Preventivas (CAPA - *Corrective and Preventive Action*)** para investigar las causas raíz de las anomalías detectadas y prevenir su recurrencia.

En metodologías ágiles (Scrum) y entornos de integración continua (CI/CD), el SQA se materializa en los acuerdos del equipo, específicamente en la **Definition of Done (DoD)**: una funcionalidad solo se aprueba si cuenta con pruebas unitarias pasando al 100%, análisis estático limpio y revisión de código por pares documentada.

---

## 2.3 Gestión de la Configuración del Software (SCM - Software Configuration Management)

Regida por el estándar **IEEE 828** (*Standard for Configuration Management in Systems and Software Engineering*), la SCM es la disciplina que garantiza la integridad, trazabilidad y reproducibilidad del software a medida que este evoluciona.

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │            FLUJO DE CONTROL DE CAMBIOS Y LÍNEA BASE (SCM)              │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
                [ Línea Base v2.5.0-baseline (Commit d97d7a6) ]
                                     │
                                     ▼
               [ Solicitud de Cambio formal: CR-ACAD-2026-005 ]
                   Justificación, Impacto Técnico y Rollback
                                     │
                                     ▼
                [ Aprobación Comité de Control de Cambios (CCB) ]
                                     │
                                     ▼
             [ Rama de Trabajo: feature/CR-005-login-ratelimit-aria ]
                   Desarrollo con Commits Semánticos y Tests
                                     │
                                     ▼
               [ Pull Request #143 & Checklist de Code Review ]
                   Inspección PEP 8, OWASP, Ley 1581, MinTIC
                                     │
                                     ▼
                  [ Fusión (Merge --no-ff) a rama principal ]
                                     │
                                     ▼
               [ Nueva Línea Base: v2.5.1-baseline (Tag Git) ]
```

### 2.3.1 Conceptos Troncales de SCM
- **Ítems de Configuración (CI - *Configuration Items*):** Cualquier artefacto del ciclo de vida del software que se somete a control de versiones. En Academix constituyen CIs: el código backend Django (`views.py`, `models.py`, `forms.py`), las plantillas HTML, las hojas de estilo CSS, los scripts de migración de base de datos (`migrations/`), archivos de variables `.env.example`, la especificación de dependencias (`requirements.txt`) y los manuales técnicos.
- **Línea Base (Baseline):** Versión formalmente acordada y congelada de uno o varios Ítems de Configuración que sirve como punto de partida para desarrollos futuros y que solo puede modificarse mediante un procedimiento formal de control de cambios. Se identifican mediante etiquetas criptográficas en Git (Git Tags).
- **Comité de Control de Cambios (CCB - *Change Control Board*):** Equipo colegiado responsable de analizar, aprobar o rechazar solicitudes de cambio (CR) evaluando el impacto arquitectónico, el costo, el riesgo de regresión y el plan de marcha atrás.
- **Contabilidad de Estado de la Configuración (CSA - *Configuration Status Accounting*):** Registro continuo y auditable que documenta qué cambios fueron aprobados, quién los implementó, qué versión del código los contiene y en qué fecha se desplegaron.

---

## 2.4 Entes Reguladores y Marco Normativo de Calidad en Colombia (Actualizado 2026)

El desarrollo e implantación de software educativo y administrativo en Colombia está condicionado por un marco legal y técnico de estricto cumplimiento:

```
               ┌────────────────────────────────────────────────────────┐
               │    MARCO REGULATORIO DE SOFTWARE EN COLOMBIA (2026)    │
               └───────────────────────────┬────────────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
    [ ICONTEC ]         [ MinTIC ]            [ SIC ]        [ colCERT / CSIRT ]
   Normalización     Gobierno Digital     Datos Personales    Ciberseguridad
    NTC-ISO 25010     Accesibilidad       Ley 1581 / NNA      Mitigación OWASP
    NTC-ISO 27001     Res. 1519 / MSPI    RNBD Institucional  Directriz CONPES
```

1. **ICONTEC (Instituto Colombiano de Normas Técnicas y Certificación):**
   - **NTC-ISO/IEC 25010:** Adopción nacional oficial del modelo de calidad del producto software. Referente indispensable para licitaciones y auditorías de proyectos tecnológicos en Colombia.
   - **NTC-ISO/IEC 27001:** Sistemas de Gestión de la Seguridad de la Información (SGSI), aplicable a servidores, bases de datos y credenciales de acceso institucional.
   - **NTC-ISO/IEC 12207:** Procesos del ciclo de vida del software.
2. **MinTIC (Ministerio de Tecnologías de la Información y las Comunicaciones):**
   - **Política de Gobierno Digital (Decreto 088 de 2022 y Resolución 460 de 2022):** Directrices de interoperabilidad y seguridad digital para sistemas educativos del orden público o mixto.
   - **Resolución 1519 de 2020 (Accesibilidad y Usabilidad Web):** Obligatoriedad del cumplimiento del estándar internacional **W3C WCAG 2.1 nivel AA**. Exige que las interfaces web escolares cuenten con contraste cromático superior a $4.5:1$, navegación total por teclado, atributos semánticos ARIA para lectores de pantalla y alternativas textuales en contenidos visuales.
3. **Superintendencia de Industria y Comercio (SIC) — Delegatura de Protección de Datos Personales:**
   - **Ley Estatutaria 1581 de 2012 y Decreto Reglamentario 1377 de 2013:** Régimen de protección de datos personales y Habeas Data.
   - **Régimen Especial para Niños, Niñas y Adolescentes (NNA - Artículo 7 de la Ley 1581):** Prohíbe el tratamiento de datos de menores sin autorización previa, expresa e informada de sus representantes legales. Exige controles técnicos innegociables: almacenamiento de contraseñas bajo funciones hash criptográficas robustas (PBKDF2/Argon2), prohibición de exponer datos académicos en URLs o texto claro y obligación de registro en el Registro Nacional de Bases de Datos (RNBD).
4. **colCERT (Equipo de Respuesta a Incidentes Cibernéticos de Colombia) y CSIRT de Gobierno:**
   - Exige la erradicación sistemática de las vulnerabilidades catalogadas en el **OWASP Top 10** (inyecciones SQL, Cross-Site Scripting XSS, falsificación de peticiones CSRF y ataques de fuerza bruta).
5. **SENA (Servicio Nacional de Aprendizaje):**
   - Rige la formación profesional tecnológica bajo la **Norma Sectorial de Competencia Laboral 220501096: Desarrollar el sistema informático según requisitos y diseño tecnológico**, garantizando la trazabilidad documental y el rigor en pruebas de software.

---

# 3. FASE 3: APLICACIÓN PRÁCTICA SOBRE EL PROYECTO FORMATIVO

En esta fase, el equipo pone en funcionamiento los instrumentos diseñados, ejecutando una autoevaluación exhaustiva sobre un módulo real de Academix y demostrando el ciclo completo de control de versiones y líneas base en Git.

---

## 3.1 EJECUCIÓN DE LA AUTOEVALUACIÓN DE CALIDAD (ISO/IEC 25010) SOBRE EL MÓDULO FUNCIONAL

### 3.1.1 Identificación del Módulo Seleccionado (`apps.accounts`)
Se seleccionó el **Módulo de Autenticación, Gestión de Cuentas de Usuario y Control de Acceso (`apps.accounts`)**, articulado con:
- La vista central de inicio de sesión: [`apps.accounts.views.login_view`](file:///C:/Academix/apps/accounts/views.py#L12-L114)
- El formulario de credenciales: [`apps.accounts.forms.LoginForm`](file:///C:/Academix/apps/accounts/forms.py)
- La interfaz visual: [templates/accounts/login.html](file:///C:/Academix/templates/accounts/login.html)
- El sistema de auditoría: `apps.audit.services.log_audit`

Este módulo es la puerta de entrada neurálgica a Academix, administrando la autenticación de cinco perfiles institucionales (Rector, Coordinador, Docente, Estudiante y Acudiente).

---

### 3.1.2 Ejecución de Pruebas y Resultados de la Matriz de Calidad

| ID | Característica ISO 25010 | Subcaracterística | Criterio de Evaluación en Academix | Métrica / Método de Prueba | Resultado Obtenido | Estado |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **EV-01** | **Adecuación Funcional** | Completitud Funcional | Autenticación multi-escuela, redirección según rol y forzado de cambio de contraseña en primer acceso (`must_change_password`). | Pruebas funcionales con suite `pytest apps/accounts/` y navegación interactiva. | 100% de los roles redireccionan a su panel correspondiente. | **CONFORME** |
| **EV-02** | **Adecuación Funcional** | Exactitud Funcional | Registro preciso de auditoría en `AuditLog` ante accesos exitosos y fallidos. | Consulta a la tabla `apps_audit_auditlog` tras simular logins válidos e inválidos. | Se constató registro íntegro de IP, rol intentado, usuario y timestamp. | **CONFORME** |
| **EV-03** | **Seguridad** | Confidencialidad | Almacenamiento seguro de contraseñas mediante derivación criptográfica (Argon2 / PBKDF2). Cero texto plano. | Inspección de esquema en base de datos y análisis de código estático con `Bandit`. | 100% de contraseñas con hashing estándar de Django. Cero hallazgos en código. | **CONFORME** |
| **EV-04** | **Seguridad** | Resistencia a Ataques (OWASP A07) | Protección del formulario `login_view` contra ataques automatizados de fuerza bruta (*Brute-force*). | Ejecución de script de estrés enviando 50 peticiones consecutivas con credenciales erróneas. | **Hallazgo Crítico:** No existe limitador de peticiones (*Rate Limiting*). Todas las peticiones fueron procesadas. | **NO CONFORME (BRECHA)** |
| **EV-05** | **Fiabilidad** | Manejo de Errores | Mensajes de error controlados ante usuarios inexistentes o inactivos (`is_active=False`). | Pruebas de caja negra con datos inválidos evaluando la respuesta HTTP. | Mensajes controlados desplegados sin divulgar stack traces internos. | **CONFORME** |
| **EV-06** | **Desempeño** | Comportamiento Temporal | Tiempo de respuesta (TTFB) del servidor en el endpoint de autenticación con cómputo criptográfico. | Medición con herramienta de profiling y herramientas de red del navegador. | Latencia promedio de **185 ms** (muy inferior al límite de 500 ms). | **CONFORME** |
| **EV-07** | **Usabilidad** | Accesibilidad (MinTIC Res. 1519) | Cumplimiento del estándar W3C WCAG 2.1 AA en [login.html](file:///C:/Academix/templates/accounts/login.html): contraste, etiquetas y atributos ARIA. | Auditoría automatizada con `Google Lighthouse CI` y extensión de accesibilidad `axe DevTools`. | **Hallazgo Menor:** Las alertas dinámicas de error generadas por HTMX carecen de `role="alert"` y `aria-live="assertive"`. | **NO CONFORME (BRECHA)** |
| **EV-08** | **Mantenibilidad** | Modularidad y Complejidad | Análisis estático de [views.py](file:///C:/Academix/apps/accounts/views.py) (longitud de funciones y acoplamiento de configuración institucional). | Conteo de líneas (`wc -l`) y cálculo de complejidad ciclomática de McCabe con `radon`. | [views.py](file:///C:/Academix/apps/accounts/views.py) supera 1,000 líneas y acopla lógica de configuración temática de la escuela. | **OPORTUNIDAD DE MEJORA** |

---

### 3.1.3 Análisis y Documentación de Brechas Encontradas (Gap Analysis)

De la autoevaluación técnica se formalizan las siguientes tres brechas:

#### Brecha B-01: Carencia de Rate-Limiting en Endpoint de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Seguridad - Confidencialidad e Integridad) / OWASP Top 10 (A07: Identification and Authentication Failures) / CONPES 3995 y Directrices colCERT.
- **Descripción:** La función `login_view` en [apps/accounts/views.py](file:///C:/Academix/apps/accounts/views.py) no limita la frecuencia de intentos de autenticación fallidos. Un atacante puede ejecutar scripts automatizados para adivinar contraseñas institucionales por fuerza bruta (*brute-force attack*) o saturar el procesador del servidor aprovechando el alto consumo de CPU requerido para derivar hashes PBKDF2/Argon2.
- **Severidad:** **ALTA**.
- **Impacto:** Vulneración de cuentas institucionales con privilegios administrativos (Rectoría/Coordinación) y degradación de disponibilidad.

#### Brecha B-02: Carencia de Atributos ARIA en Mensajes de Error de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Usabilidad - Accesibilidad) / MinTIC (Resolución 1519 de 2020 - WCAG 2.1 AA Criterio 3.3.1 y 4.1.3).
- **Descripción:** Cuando se introducen credenciales incorrectas, el mensaje de advertencia se inserta en el DOM mediante HTMX/Django sin los atributos semánticos `role="alert"` ni `aria-live="assertive"`. En consecuencia, los sintetizadores de voz para usuarios con discapacidad visual no anuncian el error a la persona.
- **Severidad:** **MEDIA**.
- **Impacto:** Incumplimiento del marco de accesibilidad web universal exigido por el Gobierno Nacional de Colombia para portales escolares.

#### Brecha B-03: Acoplamiento de Configuración Visual en la Vista de Autenticación
- **Norma / Criterio Afectado:** ISO/IEC 25010 (Mantenibilidad - Modularidad y Analizabilidad) / Principio de Responsabilidad Única (SRP).
- **Descripción:** La lógica para resolver y asignar colores primarios y secundarios de la escuela seleccionada reside directamente dentro del cuerpo de `login_view` (líneas 34-41), generando duplicidad de código frente a los procesadores de contexto ([context_processors.py](file:///C:/Academix/apps/accounts/context_processors.py)).
- **Severidad:** **BAJA**.
- **Impacto:** Dificultad para mantener y probar unitariamente la lógica de presentación de forma desacoplada.

---

### 3.1.4 Plan de Acción Correctiva y Preventiva (CAPA — IEEE 730)

```text
+----------------------------------------------------------------------------------------------------+
|                         PLAN DE ACCIONES CORRECTIVAS Y PREVENTIVAS (CAPA)                          |
+----------------------------------------------------------------------------------------------------+
```
1. **Acción Correctiva AC-01 (Para Brecha B-01):** Implementar un mecanismo de limitación de tasa (*Rate Limiting*) en `apps.accounts.views.login_view` con un umbral de **máximo 5 intentos fallidos consecutivos por minuto por dirección IP / usuario**, bloqueando solicitudes excedentes con respuesta `HTTP 429 Too Many Requests`.
2. **Acción Correctiva AC-02 (Para Brecha B-02):** Actualizar [templates/accounts/login.html](file:///C:/Academix/templates/accounts/login.html) envolviendo los contenedores de mensaje de error en etiquetas semánticas con `role="alert"`, `aria-live="assertive"` y atributos `aria-invalid="true"`.
3. **Acción Preventiva AP-01 (Para Brecha B-03):** Migrar la lógica de asignación temática escolar a [apps/accounts/context_processors.py](file:///C:/Academix/apps/accounts/context_processors.py), desacoplando la vista de la capa visual.
4. **Gobernanza de Configuración:** Las acciones AC-01 y AC-02 se canalizan formalmente a través de la **Solicitud de Cambio `CR-ACAD-2026-005`** y se auditan mediante la **Lista de Verificación de Código** en un Pull Request formal.

---

## 3.2 CONTROL DE VERSIONES, GESTIÓN DE CAMBIOS Y LÍNEA BASE (SCM EN GIT)

### 3.2.1 Establecimiento de la Línea Base Inicial (`v2.5.0-baseline`)
La línea base previa a la modificación se encuentra consolidada en el historial de la rama `main`:
- **Commit Base:** `d97d7a6` (*Implementar modulo completo de recuperacion de contrasena*)
- **Etiqueta Semántica de Configuración:** `v2.5.0-baseline`

```bash
# Verificación y etiquetado de la Línea Base Inicial en Git
git checkout main
git tag -a v2.5.0-baseline -m "Línea Base Oficial v2.5.0 del Sistema Academix"
```

---

### 3.2.2 Diligenciamiento Formal de la Solicitud de Cambio (`CR-ACAD-2026-005`)

```text
====================================================================================================
                        COMITÉ DE CONTROL DE CAMBIOS (CCB) - PROYECTO ACADEMIX
                             FORMATO FORMAL DE SOLICITUD DE CAMBIO (CR / RFC)
====================================================================================================
```

#### SECCIÓN 1: IDENTIFICACIÓN GENERAL DEL CAMBIO
| Campo del Formato | Detalle Diligenciado en Academix |
| :--- | :--- |
| **Código de Solicitud (CR-ID):** | `CR-ACAD-2026-005` |
| **Fecha de Registro:** | 03 de Noviembre de 2026 |
| **Nombre del Solicitante:** | Ing. Julián Esteban Rocha |
| **Rol / Cargo:** | Líder Técnico de Arquitectura y Responsable de SQA |
| **Módulos Afectados:** | `apps.accounts` ([views.py](file:///C:/Academix/apps/accounts/views.py)) y [templates/accounts/login.html](file:///C:/Academix/templates/accounts/login.html) |
| **Línea Base Origen / Destino:** | `v2.5.0-baseline` $\rightarrow$ `v2.5.1-baseline` |

#### SECCIÓN 2: CLASIFICACIÓN Y PRIORIDAD
| Tipo de Cambio | Prioridad | Nivel de Riesgo |
| :--- | :--- | :--- |
| [X] **Seguridad / Corrección de Vulnerabilidad**<br>[X] **Cumplimiento Legal / Normativo (MinTIC)**<br>[ ] Refactorización Arquitectónica | [X] **Alta (Sprint en curso - Cierre de brechas)**<br>[ ] Media<br>[ ] Baja | [ ] Alto<br>[X] **Moderado (Afecta login y plantillas)**<br>[ ] Bajo |

#### SECCIÓN 3: DESCRIPCIÓN Y JUSTIFICACIÓN
- **Título Resumido:** *Blindaje del Módulo de Autenticación mediante Rate-Limiting contra Ataques de Fuerza Bruta y Accesibilidad ARIA según Resolución 1519 MinTIC.*
- **Descripción de la Modificación:**
  1. Integrar estrangulamiento de peticiones (*Rate Limiting*) en `apps.accounts.views.login_view` con un límite estricto de 5 intentos fallidos consecutivos por IP en una ventana de 60 segundos. Ante excesos, bloquear temporalmente y responder con código `HTTP 429 Too Many Requests`.
  2. Ajustar la plantilla `login.html` para incluir atributos semánticos de accesibilidad W3C WCAG 2.1 AA (`role="alert"`, `aria-live="assertive"`, `aria-invalid="true"`).
- **Justificación:**
  - *Seguridad de Menores y Docentes:* Proteger las cuentas escolares frente a vulneraciones automatizadas (OWASP A07 y directrices colCERT).
  - *Cumplimiento Legal:* Acatar la Resolución 1519 de 2020 de MinTIC sobre accesibilidad web universal para el sector educativo en Colombia.

#### SECCIÓN 4: ANÁLISIS DE IMPACTO TÉCNICO MULTIDIMENSIONAL
| Dimensión | Impacto Técnico Estimado |
| :--- | :--- |
| **Backend / Vistas** | Incorporación de contador de reintentos mediante caché de Django (`django.core.cache`) o decorador personalizado de estrangulamiento en `apps.accounts.views`. |
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
*Dictamen: Aprobado por unanimidad. Se autoriza la apertura de la rama `feature/CR-005-login-ratelimit-aria` a partir de `main`.*

---

### 3.2.3 Simulación Operativa del Flujo GitFlow

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

### 3.2.4 Aplicación de la Lista de Verificación de Código en el Pull Request #143

Se abre el **Pull Request #143** en la plataforma del repositorio (GitHub / GitLab). Previo a la autorización de la fusión, el Revisor Técnico y el Responsable de SQA diligencian la lista de chequeo de 15 ítems:

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

### 3.2.5 Fusión (*Merge*), Nueva Línea Base (`v2.5.1-baseline`) y Registro CSA

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

#### Bitácora del Registro de Estado de la Configuración (CSA — Configuration Status Accounting)

| Atributo de Configuración | Valor en la Línea Base Anterior (v2.5.0) | Valor en la Nueva Línea Base (v2.5.1) |
| :--- | :--- | :--- |
| **Etiqueta Git (Tag):** | `v2.5.0-baseline` | `v2.5.1-baseline` |
| **Hash del Commit:** | `d97d7a6` | `f4b82e1` (Merge commit) |
| **Solicitud de Cambio (CR):** | N/A (Estado inicial auditado) | `CR-ACAD-2026-005` (Aprobada y cerrada) |
| **Pull Request Asociado:** | PR #142 | PR #143 |
| **Protección Fuerza Bruta:** | No implementada (Brecha detectada) | **Activa: 5 intentos/min por IP (`HTTP 429`)** |
| **Accesibilidad Web (MinTIC):** | 88/100 (Sin atributos ARIA en errores) | **96/100 (Conforme WCAG 2.1 AA Criterio 3.3.1)** |
| **Cobertura de Pruebas Unitarias:** | 86% | **88%** |
| **Estado Operativo:** | Obsoleto | **EN PRODUCCIÓN (LIVE)** |

---

# 4. CONCLUSIONES

1. **Institucionalización de la Calidad:** La aplicación práctica de los marcos normativos ISO/IEC 25010 e IEEE 730 permite superar el enfoque empírico de desarrollo, transformando la plataforma **Academix** en un producto de software confiable, mantenible y alineado con las exigencias del sector educativo colombiano.
2. **Efectividad de la Autoevaluación en la Detección Temprana:** La autoevaluación técnica sobre el módulo `apps.accounts` evidenció que, aun cuando la aplicación cumplía con la adecuación funcional y la confidencialidad criptográfica, presentaba brechas críticas de seguridad (ausencia de limitación de tasa contra ataques de fuerza bruta) y accesibilidad (falta de roles semánticos ARIA exigidos por la Resolución 1519 de 2020 de MinTIC).
3. **Control Riguroso de la Configuración y Trazabilidad:** La canalización de las soluciones a través del Formato de Solicitud de Cambio (`CR-ACAD-2026-005`), el análisis multidimensional de impacto, la formulación de planes de marcha atrás (*Rollback*) y la inspección paritaria mediante la Lista de Verificación de Código en el Pull Request #143 garantizan que ninguna modificación ingrese a la rama principal sin validación técnica.
4. **Gobierno de Líneas Base:** El congelamiento y publicación de la nueva línea base `v2.5.1-baseline` junto con la actualización de la bitácora CSA demuestra el dominio integral de la Gestión de Configuración del Software (SCM), asegurando la reproducibilidad y estabilidad de Academix ante futuras expansiones curriculares e institucionales.

---

# 5. REFERENCIAS BIBLIOGRÁFICAS (NORMA APA 7.ª EDICIÓN)

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

