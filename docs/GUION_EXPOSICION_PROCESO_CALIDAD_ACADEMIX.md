# GUION Y ESTRUCTURA DE EXPOSICIÓN: PROCESO DE CALIDAD DE SOFTWARE Y AUDITORÍA INTERNA
## Sustentación de Calidad ante la Auditoría Externa del Instructor Técnico SENA
### Empresa: Academix Software Solutions — Proyecto: ACADEMIX v2.5.0

**Programa de Formación:** Tecnología en Análisis y Desarrollo de Software (ADSO)  
**Institución:** Servicio Nacional de Aprendizaje (SENA) — Centro de Formación en Tecnologías de la Información  
**Ficha:** 3173430  
**Duración Total Estimada:** 15 a 20 Minutos (5 minutos por expositor + 5 minutos de preguntas del instructor)  
**Estructura:** 10 Diapositivas Clave + Demostración en Vivo (Live Demo) + Defensa Técnica  
**Roles del Equipo:**  
- **Expositor 1:** Líder de Proyecto y Gestión de Calidad (SQA Lead)  
- **Expositor 2:** Líder Técnico de Arquitectura y Auditoría Técnica  
- **Expositor 3:** Líder de Gestión de Configuración (SCM) y Despliegue  

---

## 📋 TABLA DE ASIGNACIÓN DE TIEMPOS Y DIAPOSITIVAS

| Bloque / Diapositiva | Expositor Responsable | Tiempo | Enfoque y Mensaje Clave |
| :--- | :--- | :---: | :--- |
| **D1: Portada e Introducción de la Empresa** | Expositor 1 (Líder SQA) | 1.5 min | Identidad de la empresa, misión de Academix y objetivo de la auditoría. |
| **D2: Marco Normativo Internacional y Colombiano** | Expositor 1 (Líder SQA) | 2.5 min | ISO/IEC 25010:2023, IEEE 730, ICONTEC, MinTIC Res. 1519 y SIC Ley 1581. |
| **D3: Proceso y Metodología de Auditoría Interna** | Expositor 2 (Líder Técnico) | 2.0 min | Plan de auditoría bajo IEEE 1028 e ISO 19011. Arsenal de pruebas SAST/DAST. |
| **D4: Resultados de Evaluación por Módulos** | Expositor 2 (Líder Técnico) | 2.5 min | Evidencias en cuentas, carga masiva, calificaciones por RAPs y boletines QR. |
| **D5: Matriz de Hallazgos y Causa Raíz (Ishikawa)** | Expositor 2 (Líder Técnico) | 2.0 min | NC Mayor HAL-01 (Fuerza bruta), NC Menor HAL-02 (ARIA) y 5 Porqués. |
| **D6: Plan CAPA (Acciones Correctivas y Preventivas)** | Expositor 3 (Líder SCM) | 2.0 min | Medidas técnicas aplicadas para subsanar los hallazgos en 24-48 horas. |
| **D7: Gestión de Configuración y Solicitud de Cambio** | Expositor 3 (Líder SCM) | 2.5 min | Línea base v2.5.0, trámite formal de CR-005 y aprobación del CCB. |
| **D8: Pull Request #143 y Checklist de Code Review** | Expositor 3 (Líder SCM) | 2.0 min | Verificación de 15 ítems técnicos y nueva línea base congelada v2.5.1. |
| **D9: Demostración en Vivo (Live Demo)** | Todo el Equipo | 3.0 min | Validación en vivo del bloqueo HTTP 429 y score Lighthouse de accesibilidad. |
| **D10: Conclusiones y Preparación Auditoría Externa** | Todo el Equipo | 1.5 min | Dictamen de conformidad, lecciones aprendidas y apertura a preguntas. |

---

# GUION DETALLADO POR DIAPOSITIVA (SPEECH DEL EQUIPO)

---

### Diapositiva 1: Portada e Identidad de la Empresa de Software
- **Expositor:** Expositor 1 (Líder de Proyecto / SQA)
- **Contenido en Pantalla:**
  - Logo institucional SENA y marca corporativa: **Academix Software Solutions**.
  - Título: *Auditoría Interna de Calidad de Software y Preparación para la Evaluación Externa*.
  - Subtítulo: *Alineación de la Plataforma ACADEMIX v2.5.0 bajo ISO/IEC 25010, IEEE 730 y Normativa Colombiana*.
  - Ficha ADSO 3173430.
- **Speech (Lo que dice el expositor):**
  > *"Buenos días, estimado instructor y compañeros. Hoy, en representación de nuestra empresa formativa Academix Software Solutions, presentamos el informe oficial de nuestro proceso de aseguramiento de calidad y auditoría interna de software aplicada a nuestro proyecto: la plataforma integral de gestión escolar ACADEMIX.*  
  > *Entendemos que la calidad no se improvisa al final del desarrollo; por ello, nos hemos sometido a una rigurosa auditoría interna para evaluar nuestro código, nuestra seguridad y nuestros procesos, garantizando que el sistema no solo funcione, sino que cumpla con los más altos estándares internacionales y la legislación colombiana vigente. Estamos listos para exponer nuestras evidencias y someternos a la auditoría externa de evaluación."*

---

### Diapositiva 2: Marco Normativo Internacional y Legal Colombiano
- **Expositor:** Expositor 1 (Líder de Proyecto / SQA)
- **Contenido en Pantalla:**
  - Diagrama de cuatro pilares:
    1. *ISO/IEC 25010:2023:* 8 características de calidad del producto software.
    2. *IEEE 730 & IEEE 1028:* Procesos preventivos de SQA y estándares de auditoría.
    3. *MinTIC (Resolución 1519 de 2020):* Obligatoriedad de accesibilidad web WCAG 2.1 nivel AA.
    4. *Superintendencia de Industria y Comercio (Ley 1581 de 2012):* Protección reforzada de datos de niños, niñas y adolescentes (NNA).
- **Speech:**
  > *"Nuestro modelo de calidad no se basa en apreciaciones subjetivas. Adoptamos la norma internacional ISO/IEC 25010 en su versión 2023, homologada en el país por el ICONTEC, para auditar adecuación funcional, seguridad, fiabilidad, rendimiento, usabilidad y mantenibilidad. Asimismo, regimos nuestro plan bajo el estándar IEEE 730 de SQA.*  
  > *Pero en Colombia, el software escolar tiene responsabilidades legales vinculantes: la Ley 1581 de 2012 de la SIC exige protección extrema a los datos personales de menores de edad, lo que nos obligó a implementar cifrado irreversible de claves y aislar historiales académicos. Adicionalmente, acatamos la Resolución 1519 de 2020 de MinTIC, garantizando accesibilidad universal WCAG 2.1 nivel AA para personas con discapacidad visual."*

---

### Diapositiva 3: Metodología y Arsenal de Pruebas de Auditoría
- **Expositor:** Expositor 2 (Líder Técnico de Arquitectura)
- **Contenido en Pantalla:**
  - Marco metodológico: ISO 19011:2018 (Directrices de auditoría) e IEEE 1028-2008.
  - Matriz de Herramientas de Inspección:
    - *SAST:* `Bandit` (análisis estático de seguridad) y `flake8`/`black` (estándar PEP 8).
    - *DAST:* `OWASP ZAP` (escaneo dinámico de penetración contra vulnerabilidades web).
    - *Frontend & A11y:* `Google Lighthouse CI` y `axe DevTools` (accesibilidad e inclusión).
    - *Desempeño:* `Locust` (pruebas de estrés concurrente con 100 usuarios simultáneos).
    - *Funcional:* `pytest` y transacciones ACID en PostgreSQL.
- **Speech:**
  > *"Para auditar la plataforma ejecutamos una auditoría de primera parte siguiendo las directrices de la norma ISO 19011 y el estándar IEEE 1028. No nos limitamos a probar pantallas manualmente; desplegamos un arsenal automatizado de inspección técnica.*  
  > *Ejecutamos análisis estático con Bandit para verificar que no existieran inyecciones SQL ni contraseñas en duro; corrimos escaneos de penetración con OWASP ZAP; evaluamos el rendimiento concurrente simulando 100 docentes con Locust; auditamos la accesibilidad con Lighthouse CI; y comprobamos la integridad referencial y las transacciones atómicas en nuestro motor de base de datos."*

---

### Diapositiva 4: Resultados de Evaluación por Módulos Críticos
- **Expositor:** Expositor 2 (Líder Técnico de Arquitectura)
- **Contenido en Pantalla:**
  - Tabla de resultados:
    - *Autenticación (accounts):* Cifrado Argon2/PBKDF2 conforme. RBAC validado al 100%.
    - *Estudiantes (students):* Carga masiva con savepoints atómicos (`transaction.atomic`). Cero corrupción ante errores de formato.
    - *Calificaciones (grades):* Agregación ponderada por RAPs al 100.00% con redondeo exacto a 2 decimales.
    - *Boletines (reports):* Código QR con firma SHA-256 para verificación pública sin exponer datos privados de menores.
    - *Infraestructura:* Latencia media de 240 ms en la nube (umbral < 500 ms) y cero fallos HTTP 500.
- **Speech:**
  > *"Al auditar módulo por módulo encontramos fortalezas contundentes: nuestro motor curricular en `apps.grades` cumple estrictamente el Decreto 1290 del MEN, asegurando que las ponderaciones de los RAPs sumen exactamente el 100% con precisión financiera de dos decimales.*  
  > *En la carga masiva de estudiantes implementamos transacciones atómicas que impiden estados corruptos a medias. Además, en los boletines escolares incorporamos un código QR con firma criptográfica que permite a las secretarías de educación validar el documento en tiempo real sin violar el derecho al Habeas Data del estudiante."*

---

### Diapositiva 5: Matriz de Hallazgos y Análisis de Causa Raíz (Ishikawa)
- **Expositor:** Expositor 2 (Líder Técnico de Arquitectura)
- **Contenido en Pantalla:**
  - Cuadro de clasificación de hallazgos según ISO 19011:
    - *No Conformidad Mayor (HAL-01):* Falta de Rate-Limiting en `login_view` (Vulnerabilidad OWASP A07 contra fuerza bruta).
    - *No Conformidad Menor (HAL-02):* Falta de atributos semánticos ARIA en mensajes de error dinámicos (MinTIC Res. 1519).
    - *Oportunidad de Mejora (HAL-04):* Acoplamiento de estilos escolares en `views.py`.
    - *Fortalezas (HAL-06 y HAL-07):* Savepoints atómicos y validación QR segura.
  - Diagrama de Ishikawa de los 5 Porqués para HAL-01.
- **Speech:**
  > *"Una auditoría honesta y profesional no oculta los problemas: los visibiliza y los soluciona. Nuestra auditoría interna detectó dos no conformidades: una Mayor, correspondiente a la falta de un limitador de intentos fallidos en el login, lo que permitía enviar peticiones continuas sin bloqueo; y una Menor, por la falta de atributos ARIA en los mensajes de error dinámicos.*  
  > *Aplicando la técnica de los 5 Porqués y el diagrama de Ishikawa, identificamos la causa raíz: en los primeros sprints nos concentramos en la lógica multi-colegio y dimos por sentado que Django bloqueaba la fuerza bruta por defecto, omitiendo un requerimiento no funcional explícito de seguridad perimetral."*

---

### Diapositiva 6: Plan de Acciones Correctivas y Preventivas (CAPA — IEEE 730)
- **Expositor:** Expositor 3 (Líder de Configuración y Despliegue)
- **Contenido en Pantalla:**
  - Plan CAPA formal:
    - *Acción AC-01 (Para HAL-01):* Implementar Rate Limiting con caché de Django: máx. 5 intentos/minuto por IP con código `HTTP 429 Too Many Requests`. (Plazo: 24h — CERRADA).
    - *Acción AC-02 (Para HAL-02):* Envolver alertas en `login.html` con `role="alert"` y `aria-live="assertive"`. (Plazo: 24h — CERRADA).
    - *Acción AC-03 (Para HAL-03):* Incorporar decorador `@period_is_open_required` y migración `is_locked`. (CERRADA).
    - *Evidencia de Verificación:* Pruebas de penetración automatizadas superadas y puntaje Lighthouse en 96/100.
- **Speech:**
  > *"En cumplimiento del estándar IEEE 730, activamos inmediatamente nuestro Plan de Acciones Correctivas y Preventivas (CAPA). Para la No Conformidad Mayor AC-01, desarrollamos un middleware de estrangulamiento que bloquea temporalmente a la sexta petición errónea con un código HTTP 429.*  
  > *Para la No Conformidad Menor AC-02, intervenimos las plantillas con atributos ARIA, elevando nuestra calificación de accesibilidad en Lighthouse de 88 a 96 sobre 100. Ambas acciones fueron verificadas y cerradas formalmente antes de esta sustentación."*

---

### Diapositiva 7: Gestión de Configuración y Solicitud de Cambio (CR-005)
- **Expositor:** Expositor 3 (Líder de Configuración y Despliegue)
- **Contenido en Pantalla:**
  - Formato formal diligenciado: `CR-ACAD-2026-005`.
  - Transición de Línea Base: `v2.5.0-baseline` $\rightarrow$ `v2.5.1-baseline`.
  - Secciones del formato: Justificación legal/técnica, análisis multidimensional de impacto, plan de marcha atrás (*Rollback Plan*) y firmas del Comité de Control de Cambios (CCB).
- **Speech:**
  > *"Las correcciones no se subieron directamente a producción ni se hicieron de forma improvisada. En nuestra empresa aplicamos Gestión de Configuración rigurosa bajo el estándar IEEE 828.*  
  > *Partimos de nuestra Línea Base congelada `v2.5.0-baseline` y tramitamos la Solicitud de Cambio `CR-ACAD-2026-005`. Esta solicitud incluyó análisis de impacto en base de datos, en arquitectura y en interfaz, además de un plan de marcha atrás documentado paso a paso por si ocurría alguna contingencia. El cambio fue aprobado formalmente por nuestro Comité de Control de Cambios."*

---

### Diapositiva 8: Pull Request #143, Checklist de Code Review y Línea Base v2.5.1
- **Expositor:** Expositor 3 (Líder de Configuración y Despliegue)
- **Contenido en Pantalla:**
  - Flujo GitFlow: Creación de rama `feature/CR-005-login-ratelimit-aria` con commits semánticos.
  - Pull Request #143 con la Lista de Verificación de 15 ítems evaluados:
    - *Estándares PEP 8 y docstrings:* 100% conforme.
    - *Seguridad OWASP Top 10:* Cero sentencias SQL crudas, token CSRF activo y protección HTTP 429 verificada.
    - *Pruebas Unitarias:* 78 pruebas aprobadas con 88% de cobertura.
  - Operación `git merge --no-ff` y congelamiento de la nueva etiqueta Git: `v2.5.1-baseline`.
- **Speech:**
  > *"El desarrollo se aisló en una rama de trabajo y se abrió el Pull Request #143. Nuestro Revisor Técnico aplicó la Lista de Verificación de Revisiones de Código de 15 puntos: verificó estilo PEP 8, docstrings, transaccionalidad, cumplimiento de la Ley 1581 y cobertura de tests.*  
  > *Una vez superados todos los criterios, se autorizó la fusión mediante `merge --no-ff` en la rama `main` y se congeló la nueva línea base oficial: `v2.5.1-baseline`. De esta manera, cada línea de código en producción cuenta con trazabilidad total y respaldo histórico."*

---

### Diapositiva 9: Demostración Técnica en Vivo (Live Demo)
- **Responsables:** Equipo en Conjunto (Expositor 2 y 3)
- **Acciones en Pantalla:**
  1. *Prueba de Fuerza Bruta:* Abrir terminal y ejecutar script simulando 6 peticiones fallidas seguidas a `/accounts/login/`. Mostrar cómo en el intento 6 el sistema responde con `HTTP 429 - Demasiados intentos fallidos`.
  2. *Prueba de Auditoría:* Abrir la base de datos o vista de administración y mostrar el registro inmediato del evento `FAILED_LOGIN` en la tabla `AuditLog`.
  3. *Prueba de Accesibilidad:* Ejecutar la auditoría en vivo con Google Lighthouse en la pestaña de navegación mostrando el puntaje verde $\ge 90/100$ en Accesibilidad.
  4. *Verificación de Boletín QR:* Escanear con un teléfono móvil el código QR de un boletín PDF y mostrar cómo carga el certificado institucional en `/verify-report/<uuid>/` protegiendo los datos del menor.
- **Speech:**
  > *"Para demostrar la efectividad de nuestro aseguramiento de calidad, pasamos a la demostración técnica en vivo... (Se ejecutan las pruebas mientras se explica cada resultado)."*

---

### Diapositiva 10: Conclusiones y Dictamen de Preparación para la Auditoría Externa
- **Expositor:** Todo el Equipo (Cierre por Expositor 1)
- **Contenido en Pantalla:**
  - Dictamen Oficial: **CONFORME SATISFACTORIO — 100% PREPARADO PARA AUDITORÍA EXTERNA**.
  - Tres Conclusiones Troncales:
    1. *Institucionalización de la Calidad:* Trascendencia del empirismo hacia procesos cuantificables con normas internacionales.
    2. *Responsabilidad Legal Escolar:* Cumplimiento estricto de Habeas Data (SIC) y Accesibilidad Web (MinTIC).
    3. *Control de Versiones y Resiliencia:* Gobernanza de cambios mediante GitFlow, baselines y pruebas automatizadas.
  - Apertura formal a la sesión de preguntas y evaluación del instructor SENA.
- **Speech:**
  > *"En conclusión, nuestro proceso de auditoría interna nos permitió identificar brechas a tiempo, solucionarlas bajo estándares formales de SCM y robustecer Academix hasta convertirlo en un software maduro, seguro y confiable para las instituciones educativas colombianas.*  
  > *Declaramos nuestro proyecto 100% preparado para la auditoría externa. Agradecemos su atención y quedamos a disposición del instructor para responder sus preguntas técnicas y validar nuestras evidencias."*

---

# BANCO RÁPIDO DE PREGUNTAS Y DEFENSA ANTE EL INSTRUCTOR SENA

1. **Si el instructor pregunta: ¿Por qué eligieron ISO 25010 y no otra norma?**
   - *Respuesta:* Porque ISO 25010 (SQuaRE) es el estándar internacional por excelencia adoptado por ICONTEC en Colombia (NTC-ISO/IEC 25010) para evaluar la calidad del producto software en 8 dimensiones integrales, complementándose con ISO 25019 para evaluar la satisfacción en uso de los directivos y docentes.
2. **Si el instructor pregunta: ¿Qué pasa si una escuela rural se queda sin internet?**
   - *Respuesta:* Diseñamos una arquitectura híbrida: además del despliegue en la nube, el sistema cuenta con scripts empaquetados (`iniciar_servidor_red.bat` y `iniciar_servidor_produccion.bat`) que permiten ejecutar Academix de manera On-Premise en un computador local o servidor de área local (LAN), operando con base de datos SQLite con modo WAL o PostgreSQL local sin requerir conexión exterior.
3. **Si el instructor pregunta: ¿Qué evidencia tienen de que las pruebas unitarias pasan?**
   - *Respuesta:* Mostramos en pantalla la ejecución de `pytest --cov=apps`, la cual ejecuta 78 tests unitarios pasando en verde con una cobertura del 88% sobre las micro-aplicaciones críticas de cuentas, calificaciones, carga de estudiantes y reportes.

