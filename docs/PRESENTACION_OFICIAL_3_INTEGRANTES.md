# GUION Y ESTRUCTURA MAESTRA DE PRESENTACIÓN DE PROYECTO: ACADEMIX
## Sustentación Oficial — Tecnología en Análisis y Desarrollo de Software (ADSO) - SENA
**Proyecto:** Plataforma de Gestión Escolar y Multi-Colegio — ACADEMIX  
**Ficha SENA:** 3173430 • Centro de Tecnologías de la Información  
**Duración Total Estimada:** 25 a 30 Minutos (8 minutos por pilar temático + 5 minutos de apertura, conclusiones y preguntas)  
**Estructura:** 16 Diapositivas Exactas • Enfoque 100% Colegios (Básica y Media) y Multi-Colegio • 3 Pilares Temáticos con Igualdad de Contenido y Tiempo

---

## 📋 Resumen de Pilares Temáticos y Distribución Equitativa (16 Diapositivas)

| Pilar Temático | Diapositivas Asignadas | Enfoque de Exposición | 2 Documentos Oficiales Respaldados |
| :--- | :--- | :--- | :--- |
| **APERTURA (Equipo)** | **Diapositiva 1** | Contexto formativo SENA, ficha, misión y estructura de la sustentación. | [Documento Técnico APA 7 (SENA)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md) |
| **PILAR 1: Gestión Académica, Modelo Pedagógico & UX** | **Diapositivas 2, 3, 4, 5** (4 Diapositivas) | • Planteamiento del Problema Escolar<br>• Arquitectura Multi-Colegio (SaaS Escolar)<br>• Motor Curricular por RAPs al 100% (Decreto 1290)<br>• Módulos UX: Asistencia, Observador y Tareas | 1. [**Manual de Navegación Paso a Paso**](file:///c:/Academix/docs/MANUAL_DE_NAVEGACION_PASO_A_PASO.md)<br>2. [**Manual de Creación de Usuarios y Roles**](file:///c:/Academix/docs/MANUAL_CREACION_USUARIOS_Y_ROLES.md) |
| **PILAR 2: Arquitectura de Software & Base de Datos** | **Diapositivas 6, 7, 8, 9** (4 Diapositivas) | • Patrón MVT y 15 Micro-Apps Django<br>• Modelado Relacional 3FN e Integridad PROTECT<br>• Optimización ORM (N+1, select_related, prefetch)<br>• Motor de Boletines Oficiales PDF y Certificados | 3. [**Documento Técnico APA 7 (SENA)**](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)<br>4. [**Diccionario de Código y Carpetas**](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md) (y [.docx](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.docx)) |
| **PILAR 3: Infraestructura, Seguridad & Entrega** | **Diapositivas 10, 11, 12, 13** (4 Diapositivas) | • Control de Acceso RBAC y 6 Roles Institucionales<br>• Auditoría Inmutable (AuditLog) y Ley 1581 (Menores)<br>• Servidores On-Premise, Nginx, Gunicorn y VLANs<br>• Puesta en Marcha, Backups (pg_dump), SLAs y Garantía | 5. [**Guía de Auditoría Cruzada y Matriz RBAC**](file:///c:/Academix/docs/GUIA_AUDITORIA_CRUZADA_ACCESO_Y_ROLES.md)<br>6. [**Manual de Entrega al Cliente**](file:///c:/Academix/docs/MANUAL_DE_ENTREGA_CLIENTE.md) |
| **CIERRE (Equipo)** | **Diapositivas 14, 15, 16** (3 Diapositivas) | • Ecosistema Documental Oficial (6 Manuales)<br>• Conclusiones y Métricas de Calidad ISO/IEC 25010<br>• Ronda de Preguntas de los Jurados Técnicos | Todos los documentos oficiales del ecosistema. |

---

# GUION DETALLADO POR DIAPOSITIVA (16 DIAPOSITIVAS)

---

### Diapositiva 1: Portada y Apertura del Proyecto (Apertura Conjunta)
- **Badge:** `🏛️ APERTURA — EQUIPO DE DESARROLLO`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Plataforma de Gestión Escolar y Multi-Colegio ACADEMIX
- **Subtítulo:** Sustentación de Proyecto Formativo — Tecnología en Análisis y Desarrollo de Software (ADSO) SENA
- **Puntos Clave:**
  - Ficha SENA 3173430 — Centro de Tecnologías de la Información.
  - Software enfocado exclusivamente en Colegios de Educación Básica y Media Técnica.
  - Modelo de Entrega SaaS Multi-Colegio con posibilidad de despliegue On-Premise local.
- **Guión Sugerido (Speech):**
  > *"Buenos días estimados instructores y jurados evaluadores. En representación de nuestro equipo de desarrollo, damos apertura a la sustentación oficial del proyecto ACADEMIX. Diseñamos una solución integral de software enfocada exclusivamente en Colegios de Educación Básica y Media, con capacidad de operar en red local o en la nube bajo un modelo Multi-Colegio. Nuestra presentación está estructurada en tres pilares temáticos de igual rigor técnico y profundidad: Gestión Académica y Experiencia de Usuario, Arquitectura de Software y Base de Datos, e Infraestructura, Seguridad y Entrega Formal."*

---

## BLOQUE 1: GESTIÓN ACADÉMICA, MODELO PEDAGÓGICO & UX (Expositora 1)
**Tiempo:** 7 a 8 minutos • 4 Diapositivas

### Diapositiva 2: Planteamiento del Problema y Justificación Escolar
- **Badge:** `📘 GESTIÓN ACADÉMICA & UX`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md (Cap. 1)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Planteamiento del Problema y Justificación Escolar
- **Subtítulo:** De la dispersión de planillas en papel a la centralización digital en tiempo real
- **Puntos Clave:**
  - Uso de planillas Excel desarticuladas propensas a pérdida y desincronización.
  - Semanas de retraso en secretaría para consolidar actas de periodo y generar boletines.
  - Desconexión informativa con acudientes, conociendo el bajo rendimiento al final del año.
  - Solución Academix: Plataforma web unificada, cálculo automático y seguimiento continuo.
- **Guión Sugerido (Speech):**
  > *"Al diagnosticar la operación de las instituciones escolares en Colombia, identificamos una problemática crítica: la desconexión operativa. Las notas se manejaban en libros físicos o plantillas de Excel desconectadas, provocando semanas de caos en secretaría para consolidar periodos, y dejando a los acudientes sin enterarse a tiempo del riesgo de reprobación de sus hijos. ACADEMIX resuelve este problema unificando la planilla docente, el control diario de asistencia, el observador de conducta y las tareas escolares en un solo software escolar en tiempo real."*

---

### Diapositiva 3: Arquitectura Multi-Colegio y Estructura Organizacional
- **Badge:** `📘 GESTIÓN ACADÉMICA & UX`
- **Documento de Referencia:** [MANUAL_DE_NAVEGACION_PASO_A_PASO.md](file:///c:/Academix/docs/MANUAL_DE_NAVEGACION_PASO_A_PASO.md)
- **Título en Pantalla:** Arquitectura Multi-Colegio y Estructura Organizacional
- **Subtítulo:** Aislamiento institucional completo y gestión de sedes dentro de un mismo núcleo de software
- **Puntos Clave:**
  - Enfoque exclusivo en Colegios (Básica Primaria, Secundaria y Media Técnica).
  - Entidad `School`: Cada institución posee código DANE, resolución, escudo y colores propios.
  - Aislamiento estricto: Docentes y alumnos del 'Colegio A' no acceden al 'Colegio B'.
  - Niveles educativos: Grados, Cursos (601, 1102), Asignaturas y Directores de Grupo asignados.
- **Guión Sugerido (Speech):**
  > *"Uno de los mayores requerimientos definidos en nuestro proyecto fue descartar modelos ajenos como universidades o institutos técnicos para concentrarnos 100% en colegios de Básica y Media. Pero fuimos más allá: implementamos un patrón Multi-Colegio donde una sola instancia del software puede albergar diferentes colegios o sedes de forma totalmente aislada. Cada colegio cuenta con su propio código DANE, sus directivas, sus colores e insignia oficial, organizando a sus alumnos en grados, grupos y periodos escolares sin mezclar expedientes."*

---

### Diapositiva 4: Motor de Evaluación Curricular y Cálculo Ponderado
- **Badge:** `📘 GESTIÓN ACADÉMICA & UX`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md (Cap. 2)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Motor de Evaluación Curricular y Cálculo Ponderado
- **Subtítulo:** Estructura pedagógica por RAPs con validación estricta al 100% y Decreto 1290
- **Puntos Clave:**
  - Jerarquía Pedagógica: Área → Asignatura → Competencias → RAPs (Resultados de Aprendizaje).
  - Regla Matemática del 100%: Los RAPs deben sumar exactamente 100%; validado en JS y en método `clean()` de Django.
  - Escala Nacional Decreto 1290: Superior (4.6-5.0), Alto (4.0-4.5), Básico (3.0-3.9) y Bajo (1.0-2.9).
  - Histórico inmutable al ejecutar el cierre formal del periodo lectivo por directivas.
- **Guión Sugerido (Speech):**
  > *"El núcleo pedagógico de Academix se apega rigurosamente al Decreto 1290 de evaluación escolar en Colombia. Estructuramos la jerarquía en Área, Asignatura, Competencias y Resultados de Aprendizaje o RAPs. Para blindar la exactitud matemática del sistema, implementamos una regla estricta: los porcentajes de evaluación deben sumar exactamente el 100%. Si un docente intenta asignar 90% o 110%, el sistema no solo lo avisa en pantalla en tiempo real mediante JavaScript, sino que el método clean() del modelo en Django rechaza la transacción protegiendo la integridad del boletín."*

---

### Diapositiva 5: Experiencia de Usuario (UX/UI): Asistencia, Observador y Tareas
- **Badge:** `📘 GESTIÓN ACADÉMICA & UX`
- **Documento de Referencia:** [MANUAL_DE_NAVEGACION_PASO_A_PASO.md](file:///c:/Academix/docs/MANUAL_DE_NAVEGACION_PASO_A_PASO.md)
- **Título en Pantalla:** Experiencia de Usuario (UX/UI): Asistencia, Observador y Tareas
- **Subtítulo:** Interfaces adaptativas y herramientas formativas para el trabajo diario en el aula
- **Puntos Clave:**
  - Asistencia en 1 Clic: Asistió, Falla Injustificada, Falla Justificada y Retardo.
  - Semáforo de Deserción: Alertas automáticas al superar el 20% y 25% de ausencias.
  - Observador Pedagógico Digital: Faltas Leves, Graves y Gravísimas con debido proceso y descargos.
  - Aula de Tareas: Asignación con fecha límite, entrega de adjuntos y calificación integrada a planilla.
- **Guión Sugerido (Speech):**
  > *"Para garantizar que el software sea adoptado con agrado por los profesores, priorizamos la experiencia de usuario con interfaces intuitivas y limpias. Desarrollamos la toma de asistencia en un solo clic, incorporando un semáforo que detecta riesgo de deserción o pérdida por fallas. Asimismo, digitalizamos el Observador del Estudiante garantizando el debido proceso escolar y creamos el aula de tareas, permitiendo recibir trabajos digitales sin recurrir a correos dispersos o grupos de WhatsApp."*

---

## BLOQUE 2: ARQUITECTURA DE SOFTWARE, BACKEND & BASE DE DATOS (Expositora 2)
**Tiempo:** 7 a 8 minutos • 4 Diapositivas

### Diapositiva 6: Patrón Arquitectónico MVT y 15 Micro-Apps Django
- **Badge:** `⚙️ ARQUITECTURA & BASE DE DATOS`
- **Documento de Referencia:** [DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md)
- **Título en Pantalla:** Patrón Arquitectónico MVT y 15 Micro-Apps Django
- **Subtítulo:** Diseño modular de software con desacoplamiento funcional y alta mantenibilidad
- **Puntos Clave:**
  - Patrón MVT: Modelos ORM, Vistas transaccionales y Plantillas Bootstrap 5 responsivas.
  - Desacoplamiento en 15 micro-apps: `accounts`, `courses`, `grades`, `attendance`, `tasks`, `bulletins`, etc.
  - Principio de Responsabilidad Única (SRP): Cada módulo aísla su lógica, URLs y servicios.
- **Guión Sugerido (Speech):**
  > *"Pasando al segundo pilar, la ingeniería de software y backend de ACADEMIX se diseñó sobre Python y Django utilizando el patrón Modelo-Vista-Template. Para evitar código monolítico o acoplado, dividimos el sistema en 15 micro-aplicaciones especializadas dentro de la carpeta apps. Cada micro-app tiene una responsabilidad única: accounts gestiona la identidad institucional, courses administra la malla curricular, grades se encarga del cálculo evaluativo, y bulletins genera los informes oficiales. Esto facilita el mantenimiento, las pruebas unitarias y la escalabilidad del sistema."*

---

### Diapositiva 7: Modelado Relacional en 3FN e Integridad Referencial
- **Badge:** `⚙️ ARQUITECTURA & BASE DE DATOS`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md (Cap. 3)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Modelado Relacional en 3FN e Integridad Referencial
- **Subtítulo:** Estructura de datos normalizada para erradicar redundancias y proteger el histórico escolar
- **Puntos Clave:**
  - 1FN, 2FN y 3FN aplicadas rigurosamente: Eliminación de anomalías y dependencias transitivas.
  - Protección con `on_delete=models.PROTECT`: Blindaje contra borrado de calificaciones y matrículas históricas.
  - Restricciones `UniqueConstraint` para impedir matrículas o asignaciones docentes duplicadas.
- **Guión Sugerido (Speech):**
  > *"En la base de datos aplicamos una normalización rigurosa en Tercera Forma Normal (3FN). Descompusimos la información para que no exista redundancia de nombres o materias, evitando anomalías de inserción y borrado. Un aspecto fundamental de nuestra defensa técnica es la integridad referencial: configuramos cláusulas on_delete=models.PROTECT en las calificaciones. Esto significa que si un directivo intenta eliminar a un estudiante que ya tiene notas registradas, la base de datos rechaza la operación protegiendo la validez legal del historial académico."*

---

### Diapositiva 8: Optimización de Consultas ORM y Alta Concurrencia
- **Badge:** `⚙️ ARQUITECTURA & BASE DE DATOS`
- **Documento de Referencia:** [DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md)
- **Título en Pantalla:** Optimización de Consultas ORM y Alta Concurrencia
- **Subtítulo:** Eliminación del problema N+1, agregaciones a nivel SQL y transacciones atómicas
- **Puntos Clave:**
  - Solución al problema N+1: `select_related()` en ForeignKeys directas y `prefetch_related()` en relaciones Many-to-Many.
  - Reducción de decenas de queries individuales a 1 o 2 consultas SQL consolidadas.
  - Agregaciones `Avg()` y `Sum()` calculadas en PostgreSQL sin saturar la RAM de Python.
  - Transacciones atómicas (`transaction.atomic`) para garantizar consistencia total en cierres.
- **Guión Sugerido (Speech):**
  > *"Para que el software responda velozmente cuando 50 profesores ingresan notas al mismo tiempo, optimizamos el ORM de Django resolviendo el problema N+1. Si consultamos un curso sin optimizar, Django ejecuta decenas de consultas innecesarias. Con select_related y prefetch_related unificamos esas consultas en uno o dos viajes al motor SQL. Además, el cálculo de los promedios no satura la memoria del servidor porque se ejecuta directamente en PostgreSQL mediante funciones de agregación SQL dentro de transacciones atómicas seguras."*

---

### Diapositiva 9: Motor de Boletines Oficiales PDF y Certificados
- **Badge:** `⚙️ ARQUITECTURA & BASE DE DATOS`
- **Documento de Referencia:** [MANUAL_DE_ENTREGA_CLIENTE.md](file:///c:/Academix/docs/MANUAL_DE_ENTREGA_CLIENTE.md)
- **Título en Pantalla:** Motor de Boletines Oficiales PDF y Certificados
- **Subtítulo:** Generación de documentos imprimibles de alta fidelidad estética y memoria optimizada
- **Puntos Clave:**
  - Estructura oficial del boletín: Escudo, notas, equivalencia cualitativa, fallas, puesto y concepto del tutor.
  - Renderizado con WeasyPrint en tamaño Carta con saltos de página inteligentes.
  - Procesamiento por lotes (Batch): Generación masiva de cursos completos en un solo archivo PDF para impresión.
  - Streaming con `FileResponse` que previene el desbordamiento de memoria RAM en el servidor.
- **Guión Sugerido (Speech):**
  > *"El producto final más visible para la comunidad escolar es el Boletín de Calificaciones. Desarrollamos un motor de generación de boletines PDF basado en plantillas HTML y WeasyPrint que cumple con todos los requisitos del Ministerio de Educación: muestra el promedio ponderado, el puesto en el curso, el conteo de fallas, la escala cualitativa y el concepto del director de grupo. El motor cuenta con procesamiento por lotes para generar el curso completo en un solo PDF listo para imprimir sin bloquear el servidor web."*

---

## BLOQUE 3: INFRAESTRUCTURA, SEGURIDAD & ENTREGA FORMAL (Expositora 3)
**Tiempo:** 7 a 8 minutos • 4 Diapositivas

### Diapositiva 10: Control de Acceso Basado en Roles (RBAC)
- **Badge:** `🛡️ INFRAESTRUCTURA & SEGURIDAD`
- **Documento de Referencia:** [GUIA_AUDITORIA_CRUZADA_ACCESO_Y_ROLES.md](file:///c:/Academix/docs/GUIA_AUDITORIA_CRUZADA_ACCESO_Y_ROLES.md)
- **Título en Pantalla:** Control de Acceso Basado en Roles (RBAC)
- **Subtítulo:** Aislamiento estricto de privilegios y blindaje de seguridad en todos los endpoints
- **Puntos Clave:**
  - 6 Roles Institucionales: Super-Admin, Rector, Secretaría, Docente, Estudiante y Acudiente.
  - Blindaje con `@login_required` y verificación estricta de rol y escuela en cada vista.
  - Protección nativa contra OWASP: Tokens CSRF, escape XSS y protección Clickjacking.
- **Guión Sugerido (Speech):**
  > *"Al ingresar al tercer pilar de infraestructura y seguridad, el pilar central es nuestro modelo RBAC. Definimos 6 roles claramente delimitados: Administrador, Rector, Secretaría, Docente, Estudiante y Acudiente. Ningún usuario puede invadir la vista o funciones de otro rol. Los docentes solo pueden calificar las asignaturas que secretaría les asignó, los estudiantes no pueden modificar sus notas y los acudientes solo ven el expediente de sus propios hijos. Todo endpoint está protegido contra ataques CSRF, XSS e inyecciones SQL según las directrices de OWASP."*

---

### Diapositiva 11: Auditoría Inmutable y Cumplimiento Ley 1581
- **Badge:** `🛡️ INFRAESTRUCTURA & SEGURIDAD`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md (Cap. 4)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Auditoría Inmutable y Cumplimiento Ley 1581
- **Subtítulo:** Trazabilidad forense de operaciones y custodia legal de datos personales de menores
- **Puntos Clave:**
  - Tabla `AuditLog` Append-Only: No admite modificaciones ni borrados; registro forense estricto.
  - Registro de usuario, IP, timestamp, tabla y campo alterado con Diff JSON (antes y después).
  - Cumplimiento de la Ley 1581 de 2012 (Habeas Data): Protección reforzada de datos de menores de edad.
- **Guión Sugerido (Speech):**
  > *"Dado que el sistema custodia información sensible de niños y jóvenes, implementamos un módulo de Auditoría Inmutable llamado AuditLog. Cada vez que alguien crea, modifica o borra un registro —por ejemplo, si se rectifica una nota— el sistema guarda quién lo hizo, desde qué dirección IP, a qué hora y el valor exacto anterior y posterior en formato JSON. Esta tabla no se puede alterar ni borrar, cumpliendo a cabalidad con la Ley Estatutaria 1581 de Habeas Data para proteger la responsabilidad civil y legal de la institución."*

---

### Diapositiva 12: Infraestructura On-Premise y Despliegue en Red Local
- **Badge:** `🛡️ INFRAESTRUCTURA & SEGURIDAD`
- **Documento de Referencia:** [MANUAL_DE_ENTREGA_CLIENTE.md](file:///c:/Academix/docs/MANUAL_DE_ENTREGA_CLIENTE.md)
- **Título en Pantalla:** Infraestructura On-Premise y Despliegue en Red Local
- **Subtítulo:** Arquitectura autónoma de servidores, segmentación por VLANs y viabilidad financiera
- **Puntos Clave:**
  - Servidor de aplicación Gunicorn/WSGI con proxy inverso Nginx y base de datos local.
  - Segmentación por VLANs: VLAN 10 (Servidores), VLAN 20 (Rectoría/Secretaría), VLAN 30 (Aulas/Docentes).
  - Viabilidad Financiera (CAPEX vs OPEX): Cero costos de licencias en la nube y funcionamiento autónomo sin Internet.
- **Guión Sugerido (Speech):**
  > *"En la infraestructura técnica diseñamos un modelo On-Premise de alta disponibilidad. El sistema se aloja en un servidor físico dentro del colegio utilizando Nginx como proxy inverso y Gunicorn como servidor de aplicaciones. La red se segmenta en tres VLANs para que los dispositivos de las aulas no tengan acceso indebido a la base de datos de administración. Este enfoque On-Premise ofrece dos ventajas contundentes: funciona en red local sin depender de que haya Internet y le ahorra al colegio pagos mensuales recurrentes en la nube."*

---

### Diapositiva 13: Protocolo de Puesta en Marcha, Respaldos y Soporte
- **Badge:** `🛡️ INFRAESTRUCTURA & SEGURIDAD`
- **Documento de Referencia:** [MANUAL_CREACION_USUARIOS_Y_ROLES.md](file:///c:/Academix/docs/MANUAL_CREACION_USUARIOS_Y_ROLES.md)
- **Título en Pantalla:** Protocolo de Puesta en Marcha, Respaldos y Soporte
- **Subtítulo:** Garantía de continuidad operativa, políticas de backup y entrega formal al cliente
- **Puntos Clave:**
  - Aprovisionamiento escalonado e importación masiva de alumnos y docentes desde Excel.
  - Backups automatizados diarios con `pg_dump` y tiempo de recuperación (RTO < 2 horas).
  - Acta formal de entrega para Rectoría con 6 meses de garantía técnica y SLA de atención.
- **Guión Sugerido (Speech):**
  > *"El ciclo de ingeniería culmina con la entrega y puesta en marcha del sistema. Documentamos el protocolo exacto para cargar las listas de estudiantes desde Excel sin errores de duplicados, asignando credenciales institucionales automáticas. Adicionalmente, entregamos una política de copias de seguridad automatizadas que respalda la base de datos todas las noches con un tiempo de recuperación ante desastres menor a 2 horas, respaldado por un acta formal de entrega con 6 meses de garantía técnica."*

---

## BLOQUE DE CIERRE: DOCUMENTACIÓN, CONCLUSIONES Y PREGUNTAS (Equipo Completo)
**Tiempo:** 5 minutos • 3 Diapositivas

### Diapositiva 14: Ecosistema Documental y Manuales del Sistema
- **Badge:** `📚 ECOSISTEMA DOCUMENTAL COMPLETO`
- **Documento de Referencia:** Directorio Oficial de los 6 Documentos
- **Título en Pantalla:** Biblioteca Documental y Manuales del Sistema
- **Subtítulo:** Los 6 documentos oficiales y definitivos que respaldan la sustentación ante el jurado
- **Puntos Clave:**
  - **Pilar 1:** [Manual de Navegación Paso a Paso](file:///c:/Academix/docs/MANUAL_DE_NAVEGACION_PASO_A_PASO.md) y [Manual de Creación de Usuarios y Roles](file:///c:/Academix/docs/MANUAL_CREACION_USUARIOS_Y_ROLES.md).
  - **Pilar 2:** [Documento Técnico APA 7 (SENA)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md) y [Diccionario de Código y Carpetas](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.md) (con versión en [.docx para Word](file:///c:/Academix/docs/DICCIONARIO_DE_CODIGO_Y_CARPETAS_ACADEMIX.docx)).
  - **Pilar 3:** [Guía de Auditoría Cruzada y Matriz RBAC](file:///c:/Academix/docs/GUIA_AUDITORIA_CRUZADA_ACCESO_Y_ROLES.md) y [Manual de Entrega al Cliente](file:///c:/Academix/docs/MANUAL_DE_ENTREGA_CLIENTE.md).
- **Guión Sugerido (Speech):**
  > *"En esta diapositiva presentamos el ecosistema documental definitivo de ACADEMIX: exactamente 6 documentos maestros, depurados y sin versiones repetidas. Cada pilar temático está respaldado por dos documentos exhaustivos: el pilar de Gestión cuenta con los manuales de Navegación y Creación de Usuarios; el pilar de Software cuenta con el Documento Técnico APA 7 y el Diccionario de Código (disponible en Word); y el pilar de Infraestructura cuenta con la Guía de Auditoría RBAC y el Manual de Entrega al Cliente con acta formal."*

---

### Diapositiva 15: Conclusiones y Validación de Calidad (ISO/IEC 25010)
- **Badge:** `👥 EQUIPO COMPLETO — CONCLUSIONES`
- **Documento de Referencia:** [DOCUMENTO_TECNICO_APA7_SENA.md (Cap. 5)](file:///c:/Academix/docs/DOCUMENTO_TECNICO_APA7_SENA.md)
- **Título en Pantalla:** Conclusiones y Validación de Calidad (ISO/IEC 25010)
- **Subtítulo:** Cumplimiento del 100% de los requisitos formativos y madurez de la ingeniería de software
- **Puntos Clave:**
  - Adecuación Funcional al 100% bajo estándar internacional ISO/IEC 25010.
  - Precisión matemática y fiabilidad en calificaciones sin margen de error humano.
  - Cumplimiento de requerimientos de egreso del programa ADSO SENA.
- **Guión Sugerido (Speech):**
  > *"Como equipo de desarrollo, concluimos que ACADEMIX superó con éxito todas las metas del proyecto formativo ADSO. Evaluamos el sistema bajo la norma internacional ISO/IEC 25010 alcanzando el 100% en adecuación funcional, precisión matemática y seguridad de la información. Demostramos que es posible construir una plataforma de alta gama tecnológica, adaptada a la legislación colombiana y financieramente viable para los colegios de nuestro país."*

---

### Diapositiva 16: Ronda de Preguntas de los Jurados Técnicos
- **Badge:** `👥 EQUIPO COMPLETO — CIERRE`
- **Documento de Referencia:** Matriz de Defensa y Simulación de Jurados
- **Título en Pantalla:** Ronda de Preguntas de los Jurados Técnicos
- **Subtítulo:** El equipo se encuentra preparado para resolver las inquietudes de la mesa evaluadora
- **Puntos Clave:**
  - **Pilar 1:** Algoritmo ponderado de RAPs al 100%, semáforos de asistencia y observador de conducta.
  - **Pilar 2:** Normalización 3FN, transacciones atómicas, resolución de consultas N+1 y WeasyPrint.
  - **Pilar 3:** Matriz RBAC, auditoría inmutable AuditLog, Ley 1581 y segmentación de red On-Premise.
- **Guión Sugerido (Speech):**
  > *"Agradecemos profundamente el tiempo y la atención de nuestros instructores y jurados técnicos. Cada una de nosotras se encuentra totalmente capacitada y lista para profundizar en el código fuente, la base de datos o la documentación técnica. Abrimos formalmente el espacio para sus preguntas."*

---

## 🎯 Guía Rápida para la Sustentación Presencial o Virtual
1. **Abrir la Presentación:** Abrir el archivo [presentacion_academix.html](file:///c:/Academix/docs/presentacion_academix.html) en Chrome o Edge y presionar `F11` (o el botón de Pantalla Completa).
2. **Navegación:** Usar las flechas del teclado `⬅️` y `➡️` o la barra espaciadora.
3. **Ver el Guión en Vivo:** Presionar la tecla `N` o hacer clic en `Notas / Speech` para leer los guiones sugeridos durante el ensayo.
4. **Documentos de Soporte:** Desde la Diapositiva 14 se puede abrir cualquiera de los 6 documentos o descargar el Diccionario en Word (.docx).
