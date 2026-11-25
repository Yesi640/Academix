# GESTIÓN CONTRACTUAL Y EVALUACIÓN DE PROVEEDORES TECNOLÓGICOS
## Cuadro Comparativo de Cotizaciones Ponderadas y Minuta de Contrato Informático con Acuerdo de Nivel de Servicio (SLA)
### Proyecto Formativo: Plataforma Web de Gestión Académica y Control Escolar ACADEMIX v2.5.1

---

**Programa de Formación:** Tecnología en Análisis y Desarrollo de Software (ADSO)  
**Institución:** Servicio Nacional de Aprendizaje (SENA) — Centro de Formación en Tecnologías de la Información  
**Ficha de Caracterización:** 3173430  
**Competencia:** 220501096 — Desarrollar el sistema informático según requisitos y diseño tecnológico  
**Resultado de Aprendizaje:** Formalizar los aspectos contractuales, legales, financieros y de nivel de servicio para el despliegue, operación y mantenimiento de la solución informática  
**Empresa / Proveedor del Servicio:** Academix Software Solutions (Equipo Formativo SENA ADSO)  
**Entidad Beneficiaria / Contratante Modelo:** Institución Educativa Distrital / Colegio Técnico Piloto  
**Fecha de Emisión:** Noviembre de 2026  
**Línea Base del Software:** Versión 2.5.1 (Commit `f4b82e1` / Tag `v2.5.1-baseline`)  

---

## TABLA DE CONTENIDO

1. [Parte I: Cuadro Comparativo de Cotizaciones de Infraestructura Cloud](#parte-i-cuadro-comparativo-de-cotizaciones-de-infraestructura-cloud)
   - 1.1 Contexto y Necesidades de Infraestructura de ACADEMIX
   - 1.2 Identificación de Proveedores Reales Evaluados (Render, AWS, DigitalOcean)
   - 1.3 Criterios de Selección y Matriz de Ponderación
   - 1.4 Tabulación Detallada de Costos y Especificaciones Técnicas
   - 1.5 Matriz de Evaluación Ponderada Cuantitativa
   - 1.6 Justificación Técnica, Operativa y Financiera de la Elección
2. [Parte II: Minuta de Contrato Informático de Suministro, Despliegue y Mantenimiento de Software](#parte-ii-minuta-de-contrato-informático-de-suministro-despliegue-y-mantenimiento-de-software)
   - Encabezado y Partes Intervinientes
   - Cláusula Primera: Objeto del Contrato
   - Cláusula Segunda: Alcance Funcional y Arquitectura de la Plataforma
   - Cláusula Tercera: Especificaciones Técnicas y Despliegue Cloud
   - Cláusula Cuarta: Valor del Contrato, Tarifas y Modalidad de Pago
   - Cláusula Quinta: Obligaciones del Contratista (Proveedor)
   - Cláusula Sexta: Obligaciones del Contratante (Institución Educativa)
   - Cláusula Séptima: Propiedad Intelectual y Licenciamiento (Ley 23 de 1982)
   - Cláusula Octava: Confidencialidad y Protección de Datos de Menores (Ley 1581 de 2012)
   - Cláusula Novena: Garantías Técnicas y Mitigación de Vulnerabilidades (OWASP / IEEE 730)
   - Cláusula Décima: Procedimiento de Gestión de Cambios (SCM / IEEE 828)
   - Cláusula Undécima: Vigencia, Renovación y Terminación Anticipada
   - Cláusula Duodécima: Ley Aplicable y Solución de Controversias
3. [Parte III: Anexo Técnico — Acuerdo de Nivel de Servicio (SLA / Service Level Agreement)](#parte-iii-anexo-técnico--acuerdo-de-nivel-de-servicio-sla--service-level-agreement)
   - 3.1 Métrica de Disponibilidad Mensual (Uptime $\ge 99.50\%$)
   - 3.2 Clasificación de Incidentes y Tiempos Máximos de Respuesta (MTTR / MTTA)
   - 3.3 Régimen de Penalizaciones y Compensaciones por Incumplimiento (Service Credits)
   - 3.4 Políticas de Copias de Seguridad (Backups) y Recuperación ante Desastres (RTO / RPO)
   - 3.5 Ventanas de Mantenimiento Preventivo Programado
4. [Firmas y Formalización Legal](#firmas-y-formalización-legal)
5. [Referencias Normativas (Norma APA 7.ª Edición)](#referencias-normativas-norma-apa-7ª-edición)

---

# PARTE I: CUADRO COMPARATIVO DE COTIZACIONES DE INFRAESTRUCTURA CLOUD

## 1.1 Contexto y Necesidades de Infraestructura de ACADEMIX
La plataforma **ACADEMIX v2.5.1** es una solución web integral para la gestión escolar desarrollada bajo el framework **Django 5.x** (Python 3.14), con una base de datos relacional transaccional (PostgreSQL 16) y un frontend estructurado en Bootstrap 5.3, Tailwind CSS y componentes reactivos HTMX.

Para garantizar su óptima prestación como servicio (*Software as a Service - SaaS*) a colegios con una población promedio de **1,200 estudiantes**, **60 docentes** y **1,000 padres de familia concurrentes** en épocas pico (entrega de boletines y cierre de periodos), la infraestructura de hosting y computación en la nube debe satisfacer los siguientes requerimientos mínimos:
- **Capa Web/Backend:** 1 a 2 vCPU dedicadas o elásticas, mínimo 2 GB de memoria RAM, soporte nativo de Python 3.14 con servidores WSGI/ASGI (`Gunicorn`), y capacidad de terminación segura de certificados SSL/TLS 1.3 automáticos.
- **Capa de Base de Datos:** PostgreSQL 16 administrado (*Managed Database*) con mínimo 10 GB de almacenamiento SSD NVMe de alta velocidad, soporte de transacciones concurrentes ACID, conexiones cifradas SSL y copias de seguridad continuas automatizadas con retención mínima de 7 días.
- **Red y Ancho de Banda:** Conectividad internacional de baja latencia hacia Colombia ($\le 85\text{ ms}$), con transferencia de datos mínima de 100 GB mensuales y CDN perimetral para distribución ágil de recursos estáticos.

---

## 1.2 Identificación de Proveedores Reales Evaluados

Se seleccionaron tres proveedores de clase mundial con presencia consolidada en el mercado latinoamericano, evaluando sus ofertas específicas para el perfil arquitectónico de ACADEMIX:

1. **Proveedor 1: RENDER CLOUD (Render Services Inc.)**  
   Plataforma como Servicio (*PaaS*) moderna, ágil y centrada en desarrolladores, con despliegue nativo impulsado por Git mediante archivos `render.yaml`, integración continua (CI/CD) inmediata y administración simplificada de base de datos PostgreSQL.
2. **Proveedor 2: AMAZON WEB SERVICES - AWS (Amazon Web Services Inc.)**  
   Líder global en Infraestructura como Servicio (*IaaS/PaaS*). Se cotizó una arquitectura basada en **AWS Elastic Beanstalk** (instancia EC2 t4g.small con arquitectura ARM Graviton2) acoplada a una base de datos administrada **AWS RDS for PostgreSQL** (db.t4g.micro) con almacenamiento elástico EBS gp3.
3. **Proveedor 3: DIGITALOCEAN (DigitalOcean Holdings Inc.)**  
   Proveedor enfocado en desarrolladores y pequeñas/medianas empresas. Se cotizó el servicio gestionado **DigitalOcean App Platform** (Basic/Professional Web Service con 2 GB RAM) integrado a **DigitalOcean Managed Database for PostgreSQL** (1 GB RAM, 10 GB SSD con copias de seguridad automáticas diarias).

---

## 1.3 Criterios de Selección y Matriz de Ponderación

Para realizar una selección objetiva, técnica y financieramente responsable, el equipo de ingeniería de software definió **cinco criterios de evaluación ponderados**, sumando un total del **100%**:

```
+----------------------------------------------------------------------------------------------------+
|                         MATRIZ DE CRITERIOS DE EVALUACIÓN Y PONDERACIÓN                            |
+----------------------------------------------------------------------------------------------------+
```

| Criterio de Selección | Ponderación (%) | Justificación del Peso Técnico |
| :--- | :---: | :--- |
| **1. Costo Total de Propiedad (TCO) y Previsibilidad Financiera** | **25%** | Crucial para la viabilidad de contratación en instituciones educativas con presupuestos públicos o tarifas escolares reguladas por el Ministerio de Educación Nacional (MEN). |
| **2. Rendimiento, Latencia y Uptime Garantizado (SLA)** | **25%** | ACADEMIX procesa boletines oficiales y registros de notas en vivo. La indisponibilidad en cierres de periodo genera traumatismo institucional severo. |
| **3. Seguridad, Cifrado y Cumplimiento Normativo (Ley 1581)** | **20%** | Almacena datos confidenciales de menores de edad (NNA). Requiere cifrado TLS 1.3 en tránsito, cifrado AES-256 en reposo y certificaciones ISO 27001 / SOC 2. |
| **4. Facilidad de Despliegue, CI/CD y Mantenibilidad** | **15%** | Mide el tiempo y esfuerzo de DevOps requerido para actualizar el software desde el repositorio GitHub institucional sin tiempos de caída (*Zero Downtime*). |
| **5. Soporte Técnico, Monitoreo y Facilidad de Recuperación (DR)** | **15%** | Disponibilidad de mesa de ayuda, alertas automáticas de caída, métricas de consumo de CPU/RAM y restauración inmediata de bases de datos (*Point-in-Time Recovery*). |
| **TOTAL PONDERADO** | **100%** | **Evaluación integral de viabilidad técnica y contractual.** |

---

## 1.4 Tabulación Detallada de Costos y Especificaciones Técnicas

*Nota de Conversión Financiera:* Tasa Representativa del Mercado (TRM) promedio estimada: **$4,250 COP por 1.00 USD**.

```
+----------------------------------------------------------------------------------------------------+
|                         TABLA COMPARATIVA DE COTIZACIONES COMERCIALES REALES                       |
+----------------------------------------------------------------------------------------------------+
```

| Componente Técnico / Comercial | PROVEEDOR 1: RENDER CLOUD | PROVEEDOR 2: AMAZON WEB SERVICES (AWS) | PROVEEDOR 3: DIGITALOCEAN |
| :--- | :--- | :--- | :--- |
| **Servicio de Cómputo Web** | Web Service Standard (2 GB RAM, 1 vCPU compartida) | EC2 t4g.small en Elastic Beanstalk (2 GB RAM, 2 vCPU Graviton2) | App Platform Professional (2 GB RAM, 1 vCPU) |
| **Costo Computación Web** | $25.00 USD / mes | $14.60 USD / mes (Bajo demanda) | $25.00 USD / mes |
| **Servicio de Base de Datos** | Managed PostgreSQL Standard (1 GB RAM, 10 GB SSD) | Managed RDS PostgreSQL db.t4g.micro (1 GB RAM, 20 GB gp3) | Managed PostgreSQL (1 Node, 1 GB RAM, 10 GB NVMe) |
| **Costo Base de Datos** | $20.00 USD / mes | $18.25 USD / mes | $15.00 USD / mes |
| **Costos Adicionales de Red** | $0.00 (Incluye 100 GB salida y SSL gratis) | $12.50 USD / mes (ALB Load Balancer + Salida datos) | $0.00 (Incluye 100 GB ancho de banda y SSL) |
| **Costo Mensual Total (USD)** | **$45.00 USD / mes** | **$45.35 USD / mes** | **$40.00 USD / mes** |
| **Costo Mensual Estimado (COP)**| **$191,250 COP / mes** | **$192,738 COP / mes** | **$170,000 COP / mes** |
| **Costo Anual Proyectado (COP)**| **$2,295,000 COP / año** | **$2,312,856 COP / año** | **$2,040,000 COP / año** |
| **Uptime Garantizado por SLA** | 99.90% mensual | 99.95% mensual | 99.90% mensual |
| **Latencia Promedio a Colombia**| 85 ms – 105 ms (Región Oregon / Frankfurt) | 65 ms – 75 ms (Región Virginia us-east-1) | 75 ms – 90 ms (Región NYC / Miami) |
| **Cifrado en Tránsito y Reposo**| TLS 1.3 automático + Cifrado en disco SSD | TLS 1.3 con AWS Certificate Manager + KMS AES-256 | TLS 1.3 automático + Cifrado LUKS en volumen |
| **Copias de Seguridad (Backups)**| Diarias automáticas con retención de 7 días | Automatizadas continuas con retención hasta 35 días | Diarias automáticas con retención de 7 días |
| **Integración CI/CD con GitHub**| Nativa e inmediata (`render.yaml` / Auto-deploy) | Requiere AWS CodePipeline, IAM Roles y scripts | Nativa con GitHub Apps / Despliegue automático |
| **Soporte Técnico Incluido** | Soporte por tickets comunitario / Email básico | Soporte básico a nivel de cuenta (Dev Support: +$29) | Soporte por tickets estándar 24/7 |

---

## 1.5 Matriz de Evaluación Ponderada Cuantitativa

Cada proveedor fue calificado en una escala de **1.0 a 5.0 puntos** en cada criterio, multiplicando su calificación por el porcentaje de ponderación asignado:

```
+----------------------------------------------------------------------------------------------------+
|                         MATRIZ CUANTITATIVA DE EVALUACIÓN MULTICRITERIO                            |
+----------------------------------------------------------------------------------------------------+
```

| Criterio de Selección | Peso | PROVEEDOR 1: RENDER | PROVEEDOR 2: AWS | PROVEEDOR 3: DIGITALOCEAN |
| :--- | :---: | :---: | :---: | :---: |
| **1. Costo Total y Previsibilidad** | 25% | **4.6** (1.15) | **3.5** (0.88) | **4.8** (1.20) |
| **2. Rendimiento, Latencia y Uptime** | 25% | **4.5** (1.13) | **4.9** (1.23) | **4.4** (1.10) |
| **3. Seguridad y Ley 1581 (Menores)** | 20% | **4.7** (0.94) | **5.0** (1.00) | **4.5** (0.90) |
| **4. Facilidad CI/CD y Mantenibilidad**| 15% | **5.0** (0.75) | **3.2** (0.48) | **4.6** (0.69) |
| **5. Soporte y Recuperación ante Fallos**| 15%| **4.4** (0.66) | **4.6** (0.69) | **4.3** (0.65) |
| **CALIFICACIÓN TOTAL FINAL** | **100%** | **4.63 / 5.00** | **4.28 / 5.00** | **4.54 / 5.00** |
| **POSICIÓN OBTENIDA** | — | 🥇 **PRIMER PUESTO (GANADOR)** | 🥉 TERCER PUESTO | 🥈 SEGUNDO PUESTO |

---

## 1.6 Justificación Técnica, Operativa y Financiera de la Elección

### Dictamen de Selección Oficial: PROVEEDOR SELECCIONADO — RENDER CLOUD
Con un puntaje final ponderado de **4.63 sobre 5.00**, el Comité Técnico y Financiero de ACADEMIX seleccionó a **RENDER CLOUD** como el proveedor oficial de infraestructura en la nube, fundamentado en los siguientes pilares:

1. **Previsibilidad Presupuestal sin Costos Ocultos:**  
   A diferencia de AWS, donde la facturación por concepto de balanceadores de carga (ALB), transferencias de datos salientes e IOPS variables suele desbordar los presupuestos escolares de forma impredecible, Render Cloud opera bajo un modelo de tarifa plana predecible de **$45.00 USD mensuales** (~$191,250 COP), ajustándose con exactitud milimétrica al presupuesto institucional aprobado.
2. **Compatibilidad Nativa con la Arquitectura de ACADEMIX:**  
   El repositorio oficial de ACADEMIX ya cuenta con el archivo de configuración declarativa [render.yaml](file:///C:/Academix/render.yaml) y scripts de construcción automáticos [build.sh](file:///C:/Academix/build.sh), permitiendo que cada commit o Pull Request aprobado en la rama `main` de GitHub se compile, migre la base de datos relacional y se publique en producción en menos de 3 minutos sin intervención manual de un administrador de sistemas.
3. **Cero Sobrecarga de Operaciones (DevOps Overhead):**  
   Mientras AWS exige la administración compleja de políticas IAM, Virtual Private Clouds (VPC) y subredes públicas/privadas, Render gestiona de forma transparente la renovación de certificados SSL/TLS, la rotación de certificados de PostgreSQL y la mitigación de ataques distribuidos de denegación de servicio (DDoS).
4. **Cumplimiento de Seguridad y Protección de Datos (Ley 1581):**  
   La base de datos PostgreSQL en Render se ejecuta en una red privada aislada (*Private Network*), inaccesible desde internet público salvo mediante túneles autenticados con credenciales criptográficas, garantizando que los registros académicos de los menores de edad permanezcan confinados y protegidos contra accesos no autorizados.

---

# PARTE II: MINUTA DE CONTRATO INFORMÁTICO DE SUMINISTRO, DESPLIEGUE Y MANTENIMIENTO DE SOFTWARE

```
+----------------------------------------------------------------------------------------------------+
|                         CONTRATO INFORMÁTICO DE PRESTACIÓN DE SERVICIOS Y SAAS                     |
|                                       CONTRATO No. ACAD-SENA-2026-088                              |
+----------------------------------------------------------------------------------------------------+
```

Entre los suscritos a saber:
- Por una parte, **ACADEMIX SOFTWARE SOLUTIONS**, iniciativa de base tecnológica del programa de formación Tecnología en Análisis y Desarrollo de Software (ADSO) del Servicio Nacional de Aprendizaje (SENA), representada legalmente por la Aprendiz **SOFIA HELENA TORRES**, identificada con Cédula de Ciudadanía No. 1.118.234.567 expedida en Buga (Valle), domiciliada en la ciudad de Guadalajara de Buga, quien en adelante y para los efectos de este contrato se denominará **EL CONTRATISTA**; y
- Por la otra parte, el **COLEGIO TÉCNICO PILOTO INSTITUCIONAL**, establecimiento educativo oficial con personería jurídica reconocida y NIT No. 890.123.456-7, representado legalmente por su Rector(a) **DR. CARLOS EDUARDO RAMÍREZ HOYOS**, identificado con Cédula de Ciudadanía No. 16.789.012 de Cali, en calidad de Ordenador del Gasto, quien en adelante se denominará **EL CONTRATANTE**;

Hemos convenido celebrar el presente **CONTRATO INFORMÁTICO DE SUMINISTRO, DESPLIEGUE CLOUD, LICENCIAMIENTO DE SOFTWARE COMO SERVICIO (SaaS) Y ACUERDO DE NIVEL DE SERVICIO (SLA)**, el cual se regirá por las leyes de la República de Colombia (Código de Comercio, Ley 23 de 1982, Ley 1581 de 2012, Ley 527 de 1999) y por las siguientes cláusulas:

---

### CLÁUSULA PRIMERA: OBJETO DEL CONTRATO
**EL CONTRATISTA** se compromete para con **EL CONTRATANTE** a suministrar, aprovisionar, desplegar en infraestructura de nube segura, configurar, poner en marcha, capacitar y prestar el soporte técnico integral y mantenimiento correctivo/preventivo de la plataforma web de gestión escolar, matrícula y control académico denominada **ACADEMIX (Versión 2.5.1)**, garantizando los estándares de calidad del producto software según la norma técnica **ISO/IEC 25010** y el Acuerdo de Nivel de Servicio adjunto.

---

### CLÁUSULA SEGUNDA: ALCANCE FUNCIONAL Y MÓDULOS DE LA PLATAFORMA
El software suministrado por **EL CONTRATISTA** comprende la operatividad del 100% de los siguientes módulos funcionales estructurados en arquitectura desacoplada:
1. **Módulo de Identidades y Control de Acceso (`apps.accounts`):** Control de acceso basado en roles (RBAC: Rector, Secretaría, Docente, Estudiante, Acudiente), autenticación cifrada resistente a ataques de fuerza bruta mediante limitación de tasa (*rate limiting*) y portal de recuperación segura de credenciales.
2. **Módulo de Admisiones y Carga Masiva Transaccional (`apps.students`):** Importación masiva de expedientes de matrícula desde archivos Excel/CSV con transacciones atómicas (*savepoints*) garantizando cero inconsistencias en base de datos.
3. **Módulo de Malla Curricular y Calificaciones por RAPs (`apps.grades`):** Registro de notas cuantitativas de 1.00 a 5.00 con redondeo financiero y cómputo ponderado estricto al 100.00% de los Resultados de Aprendizaje Previsto (RAPs) según el Decreto 1290 de 2009 del MEN.
4. **Módulo de Boletines Oficiales y Verificación QR (`apps.reports`):** Renderizado de boletines escolares consolidados en PDF de alta fidelidad, con incorporación de código QR dinámico criptográfico que permite la verificación pública de autenticidad sin divulgar datos sensibles de menores.
5. **Módulo de Control de Calendario Escolar (`apps.periods`):** Cierre y bloqueo de periodos lectivos (`is_locked`) para preservar la inmutabilidad de las calificaciones.
6. **Módulo de Asistencia y Observador Disciplinario (`apps.attendance` / `apps.discipline`):** Llamado a lista diario y seguimiento convivencial según el manual de convivencia escolar.
7. **Módulo de Auditoría Institucional (`apps.audit`):** Bitácora inmutable de eventos críticos que almacena fecha, hora, dirección IP, usuario y modificaciones de notas.

---

### CLÁUSULA TERCERA: ESPECIFICACIONES TÉCNICAS Y DESPLIEGUE CLOUD
El software operará en modalidad **Cloud SaaS** desplegado sobre la infraestructura certificada de **Render Cloud** (o la infraestructura designada por el equipo de ingeniería), utilizando el motor relacional **PostgreSQL 16**, con terminación de cifrado SSL/TLS 1.3 y una copia de respaldo (*backup*) diario automatizado. Asimismo, **EL CONTRATISTA** entregará una suite de ejecución en red local (*On-Premise*) mediante el script `iniciar_servidor_red.py` para garantizar la continuidad del servicio educativo ante contingencias de conectividad a internet en la sede física del colegio.

---

### CLÁUSULA CUARTA: VALOR DEL CONTRATO, TARIFAS Y FORMA DE PAGO
1. **Valor Total Anual:** El valor total acordado para el licenciamiento SaaS, infraestructura en la nube, soporte técnico y mantenimiento del software durante el año lectivo asciende a la suma de **DOS MILLONES SEISCIENTOS MIL PESOS MONEDA CORRIENTE ($2,600,000 COP)**, exento de IVA en virtud de los incentivos para servicios de software y computación en la nube en Colombia (Estatuto Tributario Art. 476 Numeral 21).
2. **Forma de Pago:**
   - Un anticipo del **30%** a la firma del presente contrato y configuración inicial del entorno cloud ($780,000 COP).
   - Un segundo pago del **40%** contra entrega del Acta de Recibido a Satisfacción tras la carga masiva de estudiantes y capacitación a docentes ($1,040,000 COP).
   - Un pago final del **30%** al cierre del cuarto periodo académico y emisión exitosa de boletines finales ($780,000 COP).

---

### CLÁUSULA QUINTA: OBLIGACIONES DEL CONTRATISTA
1. Garantizar la disponibilidad mensual de la plataforma conforme al **Acuerdo de Nivel de Servicio (SLA)** estipulado en el Anexo Técnico ($\ge 99.5\%$).
2. Ejecutar las actividades de mantenimiento preventivo y correctivo para subsanar cualquier fallo, bug o inconsistencia técnica reportada.
3. Asegurar la inmutabilidad y resguardo de las copias de seguridad de la base de datos del colegio.
4. Capacitar al personal directivo, docente y administrativo en el uso eficiente de las herramientas de la plataforma.
5. Aplicar parches de seguridad y mantener las dependencias de software libres de vulnerabilidades críticas según los lineamientos de colCERT y OWASP.

---

### CLÁUSULA SEXTA: OBLIGACIONES DEL CONTRATANTE
1. Pagar el valor del contrato en los plazos y condiciones acordadas.
2. Designar un enlace institucional (Coordinador Académico o de Sistemas) para la recepción y trámite de incidencias.
3. Suministrar la información fidedigna de estudiantes, docentes y asignaturas requerida para el aprovisionamiento.
4. Velar por la custodia y buen uso de las credenciales de acceso administrativas entregadas a los rectores y coordinadores.
5. Contar con el consentimiento informado de los padres de familia para el tratamiento de datos personales de los estudiantes.

---

### CLÁUSULA SÉPTIMA: PROPIEDAD INTELECTUAL Y LICENCIAMIENTO
1. **Titularidad del Software:** En concordancia con la **Ley 23 de 1982**, la **Decisión Andina 351 de 1993** y la jurisprudencia de la Dirección Nacional de Derecho de Autor (DNDA), los derechos morales y patrimoniales de autor sobre el código fuente, arquitectura, diseño de base de datos, marcas y desarrollos de la plataforma **ACADEMIX** pertenecen exclusivamente a sus creadores (**EL CONTRATISTA** / Aprendices ADSO SENA).
2. **Licencia de Uso Concedida:** **EL CONTRATISTA** otorga a **EL CONTRATANTE** una **Licencia de Uso no exclusiva, intransferible, revocable y limitada en el tiempo**, circunscrita única y exclusivamente a la gestión académica del colegio beneficiario durante la vigencia del contrato.
3. **Propiedad de los Datos:** **EL CONTRATANTE** es el único, absoluto y exclusivo propietario de los datos, expedientes, notas, historiales disciplinarios y registros de estudiantes almacenados en la plataforma. **EL CONTRATISTA** no adquiere ningún derecho sobre dicha información y se compromete a entregar un volcado íntegro de la base de datos (`.sql` / CSV) al término de la relación contractual.

---

### CLÁUSULA OCTAVA: CONFIDENCIALIDAD Y PROTECCIÓN DE DATOS DE MENORES (LEY 1581 DE 2012)
1. **Régimen Especial de Protección de Menores:** Ambas partes reconocen que la base de datos de ACADEMIX almacena información de **Niños, Niñas y Adolescentes (NNA)**, sujeta a la protección reforzada del **Artículo 7 de la Ley Estatutaria 1581 de 2012**, el Decreto 1377 de 2013 y la Circular Externa 002 de 2021 de la Superintendencia de Industria y Comercio (SIC).
2. **Medidas Técnicas de Seguridad Exigidas:**
   - Todas las contraseñas de acceso deben residir cifradas mediante algoritmos de derivación robustos (`Argon2id` o `PBKDF2-SHA256`).
   - El canal de comunicación debe forzar HTTPS con cifrado TLS 1.3.
   - La verificación pública de boletines mediante código QR jamás expondrá números de documento de identidad, direcciones ni teléfonos de menores de edad.
3. **Deber de Secreto:** **EL CONTRATISTA** y su personal técnico suscriben acuerdo estricto de confidencialidad, quedando prohibida la venta, comercialización, cesión o divulgación de la información de los estudiantes bajo pena de sanciones penales y administrativas de la SIC.

---

### CLÁUSULA NOVENA: GARANTÍAS TÉCNICAS Y REVISIÓN DE CÓDIGO
**EL CONTRATISTA** garantiza que el software ha sido desarrollado y auditado bajo estándares formales de ingeniería de software (**ISO/IEC 25010**, **IEEE 730** e **IEEE 1028**), encontrándose libre de virus, troyanos, puertas traseras (*backdoors*) o código malicioso destinado a interrumpir el servicio. Toda modificación al código fuente se tramita mediante el procedimiento de Control de Cambios estandarizado en **IEEE 828** (Formato Change Request y verificación previa al Merge en GitHub).

---

### CLÁUSULA DÉCIMA: GESTIÓN DE CONFIGURACIÓN Y SOLICITUDES DE CAMBIO
Cualquier requerimiento de personalización o nueva funcionalidad solicitado por **EL CONTRATANTE** que exceda el alcance de la versión 2.5.1 deberá tramitarse formalmente a través del Comité de Control de Cambios (CCB) mediante una **Solicitud de Cambio (Change Request - SCM)**, donde se evaluará su impacto técnico, viabilidad y cotización adicional si a ello hubiere lugar.

---

### CLÁUSULA UNDÉCIMA: VIGENCIA, RENOVACIÓN Y TERMINACIÓN
1. **Vigencia:** El presente contrato tendrá una duración de **DOCE (12) MESES** contados a partir de la firma del acta de inicio, prorrogable automáticamente por periodos iguales mediante acuerdo suscrito entre las partes.
2. **Causales de Terminación:**
   - Incumplimiento grave y reiterado de las cláusulas contractuales o de los niveles de servicio (SLA).
   - Mutuo acuerdo formalizado por escrito.
   - Fuerza mayor o caso fortuito debidamente comprobado que impida la prestación del servicio por más de 30 días.
3. **Protocolo de Salida (Offboarding):** A la terminación del contrato, **EL CONTRATISTA** suministrará a **EL CONTRATANTE** una copia completa y verificada de la base de datos en formato abierto (PostgreSQL `.sql` y archivos Excel) y procederá al borrado seguro de la instancia institucional en la nube en un lapso no superior a treinta (30) días calendario.

---

### CLÁUSULA DUODÉCIMA: LEY APLICABLE Y SOLUCIÓN DE CONTROVERSIAS
El presente contrato se rige íntegramente por las leyes de la República de Colombia. Cualquier diferencia o controversia que surja con ocasión de la interpretación, ejecución o liquidación del contrato que no pueda ser resuelta de común acuerdo entre las partes en un término de quince (15) días hábiles, se someterá a un Centro de Conciliación legalmente constituido en la ciudad de Guadalajara de Buga o Cali (Valle del Cauca).

---

# PARTE III: ANEXO TÉCNICO — ACUERDO DE NIVEL DE SERVICIO (SLA / SERVICE LEVEL AGREEMENT)

```
+----------------------------------------------------------------------------------------------------+
|                         ANEXO TÉCNICO: ACUERDO DE NIVEL DE SERVICIO (SLA)                          |
|                                       ACADEMIX v2.5.1 SAAS SERVICES                                |
+----------------------------------------------------------------------------------------------------+
```

El presente Acuerdo de Nivel de Servicio (SLA) establece los compromisos de disponibilidad, tiempos de respuesta, escalamiento y penalizaciones operativas asumidos por **EL CONTRATISTA**:

## 3.1 Métrica de Disponibilidad Mensual (Uptime)
**EL CONTRATISTA** se compromete a garantizar una **Disponibilidad Mensual del Servicio $\ge 99.50\%$** durante las 24 horas del día, los 7 días de la semana, calculada mediante la fórmula:

$$\text{Disponibilidad (\%)} = \left( \frac{\text{Minutos Totales del Mes} - \text{Minutos de Indisponibilidad no Programada}}{\text{Minutos Totales del Mes}} \right) \times 100$$

*Ejemplo:* En un mes de 30 días (43,200 minutos), el tiempo máximo acumulado de indisponibilidad imprevista no superará **216 minutos (3.6 horas)** al mes.

---

## 3.2 Clasificación de Incidentes y Tiempos de Respuesta
Las incidencias reportadas a través del canal oficial de soporte (`soporte@academix.edu.co` / WhatsApp institucional) se clasificarán según su criticidad técnica y de negocio:

```
+----------------------------------------------------------------------------------------------------+
|                         MATRIZ DE TIEMPOS DE ATENCIÓN Y SOLUCIÓN DE INCIDENTES                     |
+----------------------------------------------------------------------------------------------------+
```

| Nivel de Severidad | Criterio de Impacto Operativo | Tiempo Máximo de Respuesta (MTTA) | Tiempo Máximo de Solución (MTTR) | Protocolo de Escalamiento Técnico |
| :---: | :--- | :---: | :---: | :--- |
| **SEVERIDAD 1 (Crítica)** | **Caída Total del Sistema:** La plataforma no responde (Error HTTP 500/502/503 general), la base de datos está inaccesible o existe bloqueo total del proceso de autenticación institucional. | $\le \mathbf{30\text{ minutos}}$ | $\le \mathbf{2\text{ horas}}$ | Notificación inmediata a Líder Técnico y DevOps. Activación de servidor espejo On-Premise si excede 1 hora. |
| **SEVERIDAD 2 (Alta)** | **Degradación de Módulo Crítico:** El sistema opera pero un módulo nuclear falla (ej. los docentes no pueden guardar notas de RAPs, falla la generación masiva de boletines PDF o hay lentitud severa $> 3\text{ seg}$). | $\le \mathbf{1\text{ hora}}$ | $\le \mathbf{4\text{ horas}}$ | Asignación a Desarrollador Backend Senior. Reinicio de workers WSGI e inspección de logs. |
| **SEVERIDAD 3 (Media)** | **Afectación Parcial Menor:** Fallo funcional localizado que no impide la operación global (ej. error en filtros del observador, inconsistencia visual en plantillas o reporte estadístico desalineado). | $\le \mathbf{2\text{ horas}}$ | $\le \mathbf{12\text{ horas}}$ | Tramitación mediante rama `fix/` y solución en ciclo ordinario de soporte. |
| **SEVERIDAD 4 (Baja)** | **Consultas y Requerimientos Menores:** Solicitud de cambio de textos, creación de nuevos usuarios administrativos o dudas de manejo de interfaz. | $\le \mathbf{4\text{ horas}}$ | $\le \mathbf{24\text{ horas}}$ | Atención por mesa de ayuda en horario laboral ordinario (Lunes a Viernes 7:00 am - 5:00 pm). |

---

## 3.3 Régimen de Compensaciones y Créditos de Servicio (Service Credits)
Si en cualquier mes calendario **EL CONTRATISTA** no alcanza el nivel de disponibilidad pactado por causas imputables exclusivamente a su infraestructura o código, **EL CONTRATANTE** tendrá derecho a aplicar descuentos compensatorios (*Service Credits*) sobre la siguiente factura o período de liquidación:

| Disponibilidad Mensual Alcanzada | Porcentaje de Compensación / Descuento |
| :---: | :---: |
| **$99.00\% - 99.49\%$** | **10%** de descuento sobre la tarifa mensual |
| **$97.00\% - 98.99\%$** | **25%** de descuento sobre la tarifa mensual |
| **Inferior al $97.00\%$** | **50%** de descuento sobre la tarifa mensual y causal de revisión contractual |

---

## 3.4 Políticas de Copias de Seguridad y Recuperación (RTO / RPO)
- **Frecuencia de Copias de Seguridad:** Diaria automática a las 02:00 horas (Zona Horaria `America/Bogota`), almacenada en almacenamiento cifrado geo-redundante independiente.
- **Punto Objetivo de Recuperación (RPO - Recovery Point Objective):** Máximo **24 horas** de pérdida potencial de datos ante catástrofe total.
- **Tiempo Objetivo de Recuperación (RTO - Recovery Time Objective):** Máximo **2 horas** para restaurar el servicio en su totalidad a partir del último respaldo verificado.

---

## 3.5 Ventanas de Mantenimiento Programado
Cualquier actualización de arquitectura o mantenimiento mayor que requiera indisponibilidad temporal deberá notificarse a **EL CONTRATANTE** con mínimo **cuarenta y ocho (48) horas de anticipación**. Dichos mantenimientos se ejecutarán exclusivamente en horarios no lectivos: **días domingos o festivos entre las 22:00 horas y las 04:00 horas**, no computándose como tiempo de indisponibilidad dentro del SLA.

---

# FIRMAS Y FORMALIZACIÓN LEGAL

Para constancia de lo acordado y en señal de aceptación expresa de todas y cada una de las cláusulas y anexos técnicos del presente contrato, se firma en dos (2) ejemplares de idéntico tenor en la ciudad de Guadalajara de Buga, Departamento del Valle del Cauca, a los veinticinco (25) días del mes de Noviembre del año 2026.

```
_____________________________________________          _____________________________________________
EL CONTRATISTA:                                        EL CONTRATANTE:
SOFIA HELENA TORRES                                    DR. CARLOS EDUARDO RAMÍREZ HOYOS
C.C. No. 1.118.234.567 de Buga                         C.C. No. 16.789.012 de Cali
Representante Legal Academix Software                  Rector y Ordenador del Gasto
Líder de Aseguramiento de Calidad (SQA Lead)           Colegio Técnico Piloto Institucional
Programa ADSO — Ficha 3173430                          NIT: 890.123.456-7
```

---

# REFERENCIAS NORMATIVAS (NORMA APA 7.ª EDICIÓN)

- Amazon Web Services. (2026). *AWS Service Level Agreement and RDS Pricing Calculator*. Seattle: AWS Inc.
- Congreso de la República de Colombia. (1982). *Ley 23 de 1982 sobre derechos de autor y propiedad intelectual en obras de software*. Diario Oficial No. 35.939.
- Congreso de la República de Colombia. (1999). *Ley 527 de 1999: Por medio de la cual se define y reglamenta el acceso y uso de los mensajes de datos, del comercio electrónico y de las firmas digitales*. Diario Oficial No. 43.673.
- Congreso de la República de Colombia. (2012). *Ley Estatutaria 1581 de 2012: Por la cual se dictan disposiciones generales para la protección de datos personales*. Diario Oficial No. 48.587.
- Comunidad Andina de Naciones [CAN]. (1993). *Decisión 351: Régimen Común sobre Derecho de Autor y Derechos Conexos para Programas de Ordenador*. Comisión del Acuerdo de Cartagena.
- DigitalOcean. (2026). *App Platform and Managed Databases SLA and Pricing Structure*. Nueva York: DigitalOcean Holdings.
- Institute of Electrical and Electronics Engineers [IEEE]. (2012). *IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering*. Nueva York: IEEE Computer Society.
- Institute of Electrical and Electronics Engineers [IEEE]. (2014). *IEEE Std 730-2014: IEEE Standard for Software Quality Assurance Processes*. Nueva York: IEEE Computer Society.
- International Organization for Standardization [ISO]. (2023). *ISO/IEC 25010:2023: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. Ginebra: ISO.
- Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2020). *Resolución 1519 de 2020: Lineamientos de accesibilidad web universal (WCAG 2.1 AA)*. Bogotá: MinTIC.
- Render Services. (2026). *Render Cloud Platform Pricing and Master Service Agreement*. San Francisco: Render Inc.
- Superintendencia de Industria y Comercio [SIC]. (2021). *Circular Externa 002 de 2021: Deberes y directrices de seguridad técnica en el tratamiento de datos de niños, niñas y adolescentes*. Bogotá: SIC.
