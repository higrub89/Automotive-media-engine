# Roadmap para el Proyecto Automotive Media Engine

## Resumen Ejecutivo

El proyecto Automotive Media Engine busca reconstruir un sistema automatizado para la generación de contenido técnico sobre automoción, basado en el prototipo validado en GitHub. Con el cofundador Alex, se formará la primera empresa para escalar la producción de videos en múltiples plataformas (YouTube, TikTok, Facebook, Instagram, LinkedIn), con el objetivo de generar al menos 5 cuentas temáticas y alcanzar ingresos recurrentes de ~3000 € al mes para mayo de 2026. 

Este roadmap detalla un plan estructurado en fases, desde enero de 2026 hasta diciembre de 2026, cubriendo desarrollo técnico (en Python), despliegue en Google Cloud Platform (GCP), creación de la empresa, setup de correos corporativos, y estrategia de contenido. El enfoque es ágil, con hitos mensuales para minimizar riesgos y optimizar costos. Se estima un presupuesto inicial de ~500-1000 € (herramientas, cloud, legal), asumiendo un equipo de 2 personas (Ruben y Alex).

El timeline se divide en 4 fases principales: Preparación (Ene-Feb), Desarrollo y Lanzamiento (Mar-Abr), Escalado y Monetización (May-Jun), y Optimización Continua (Jul-Dic). Se prioriza la modularidad del sistema para iteraciones rápidas, integrando APIs como Anthropic Claude y ElevenLabs, con opciones de bajo costo (Gemini, Edge-TTS, Manim).

## Fase 1: Preparación (Enero - Febrero 2026)

Objetivo: Establecer las bases legales, técnicas y estratégicas para evitar bloqueos posteriores. Duración: 2 meses. Responsables: Ruben (técnico), Alex (negocios/legal).

### Hitos Principales
- **Semana 1-2 (Ene 26 - Feb 9)**: Formación de la empresa.
  - Registrar SL (Sociedad Limitada) en España vía gestoría online (e.g., Lanzame). Costo: ~300-500 €.
  - Redactar Pacto de Socios para definir roles, equity (50/50 asumido) y salida.
  - Obtener CIF y setup bancario (e.g., N26 Business).

- **Semana 3-4 (Feb 10-23)**: Setup de herramientas colaborativas.
  - Configurar correo corporativo con Google Workspace (dominio automotivemediaengine.com). Costo: ~12 €/mes para 2 usuarios.
  - Crear repositorio privado en GitHub para el nuevo código (basado en prototipo).
  - Definir nichos para las 5 cuentas: e.g., 1. EVs, 2. Mecánica Básica, 3. Historia Auto, 4. Reviews Técnicos, 5. Tips Mantenimiento.

- **Semana 5-8 (Feb 24 - Mar 23, solapado con Fase 2)**: Planificación técnica.
  - Elegir stack: Python principal, con híbrido C++ para módulos intensivos si needed (e.g., video render via pybind11).
  - Configurar entorno local: Instalar dependencias (FFmpeg, bibliotecas IA).
  - Crear briefs iniciales para pruebas (10-20 Markdowns).

### Recursos y Riesgos
- Presupuesto: ~400 € (legal + tools).
- Riesgos: Demoras legales; mitigar con asesoría rápida.
- Métricas: Empresa registrada, 5 nichos definidos, entorno dev listo.

| Tarea | Responsable | Fecha Inicio | Fecha Fin | Dependencias |
|-------|-------------|--------------|-----------|--------------|
| Registrar SL | Alex | 26 Ene | 9 Feb | Ninguna |
| Setup Workspace | Ruben | 10 Feb | 16 Feb | Dominio comprado |
| Definir nichos | Ambos | 17 Feb | 23 Feb | Brainstorming |

## Fase 2: Desarrollo y Lanzamiento (Marzo - Abril 2026)

Objetivo: Reconstruir el pipeline en Python, desplegar en GCP, y lanzar sitio web básico. Duración: 2 meses. Enfoque: MVP (Minimum Viable Product) para generar 10 videos/semana.

### Hitos Principales
- **Semana 1-4 (Mar 1-31)**: Desarrollo del core.
  - Reconstruir módulos: script_engine (IA guiones), audio_factory (TTS), visual_assembly (imágenes/animaciones), video_assembler (FFmpeg).
  - Implementar paralelismo (asyncio para audio/visuales simultáneos).
  - Integrar APIs: Claude para guiones, ElevenLabs para voz, Pexels/Replicate para visuales.
  - Modo bajo costo: Gemini + Edge-TTS + Manim.

- **Semana 5-6 (Abr 1-14)**: Despliegue en GCP.
  - Setup Cloud Run/Functions para pipeline serverless.
  - Implementar colas (Cloud Tasks) para procesamiento batch.
  - Monitoreo: Cloud Monitoring para costos/APIs (~50-75 €/mes inicial).

- **Semana 7-8 (Abr 15-30)**: Sitio web y pruebas.
  - Build sitio básico con Flask/Streamlit (deploy en App Engine). Contenido: Demos, contacto.
  - Pruebas end-to-end: Generar 20 videos, adaptar formatos (vertical TikTok, horizontal YouTube).
  - Lanzamiento alpha: Publicar primeros videos en 1 cuenta de prueba.

### Recursos y Riesgos
- Presupuesto: ~300 € (GCP créditos gratis iniciales).
- Riesgos: Latencias APIs; mitigar con reintentos y modos offline.
- Métricas: Pipeline funcional, 20 videos generados, sitio online.

| Tarea | Responsable | Fecha Inicio | Fecha Fin | Dependencias |
|-------|-------------|--------------|-----------|--------------|
| Reconstruir módulos | Ruben | 1 Mar | 31 Mar | Entorno local |
| Despliegue GCP | Ruben | 1 Abr | 14 Abr | Core desarrollado |
| Sitio web | Alex | 15 Abr | 30 Abr | GCP setup |

## Fase 3: Escalado y Monetización (Mayo - Junio 2026)

Objetivo: Lanzar 5 cuentas, generar contenido masivo y activar monetización. Duración: 2 meses. Meta: ~3000 €/mes (ads, patrocinios).

### Hitos Principales
- **Semana 1-4 (May 1-31)**: Lanzamiento de cuentas.
  - Crear/verificar 5 canales por plataforma (YouTube Partner, TikTok Creator Fund).
  - Automatizar posting con Hootsuite (~149 €/mes).
  - Generar 50 videos/semana (batch processing en GCP).

- **Semana 5-8 (Jun 1-30)**: Estrategia de engagement.
  - Publicar 3-5 videos/día/cuenta, con SEO/hashtags.
  - Monitorear analytics: Apuntar 10k views/video.
  - Buscar patrocinios (sitio web como lead gen).
  - Alcanzar meta económica: Ads + fondos creadores.

### Recursos y Riesgos
- Presupuesto: ~300 € (tools posting).
- Riesgos: Bajo engagement; mitigar con A/B testing contenidos.
- Métricas: 5 cuentas activas, 100k views totales, ingresos iniciales.

| Tarea | Responsable | Fecha Inicio | Fecha Fin | Dependencias |
|-------|-------------|--------------|-----------|--------------|
| Crear canales | Alex | 1 May | 15 May | Pipeline listo |
| Automatizar posting | Ruben | 16 May | 31 May | Cuentas creadas |
| Monetización | Ambos | 1 Jun | 30 Jun | Contenido publicado |

## Fase 4: Optimización Continua (Julio - Diciembre 2026)

Objetivo: Mejorar escalabilidad, reducir costos y expandir. Duración: 6 meses. Enfoque: Sostenibilidad post-meta.

### Hitos Principales
- **Jul-Ago**: Optimizaciones técnicas (híbrido C++ si needed, abstracciones APIs).
- **Sep-Oct**: Expansión (multi-idioma, más plataformas, SaaS beta).
- **Nov-Dic**: Revisión anual (auditoría costos, nuevos nichos).

### Recursos y Riesgos
- Presupuesto: ~200 €/mes (mantenimiento).
- Riesgos: Cambios APIs; mitigar con backups y alternativas.
- Métricas: Ingresos estables >3000 €, 100 videos/semana.

| Tarea | Responsable | Fecha Inicio | Fecha Fin | Dependencias |
|-------|-------------|--------------|-----------|--------------|
| Optimizaciones | Ruben | 1 Jul | 31 Ago | Fase 3 completa |
| Expansión | Alex | 1 Sep | 31 Oct | Optimizaciones |
| Revisión | Ambos | 1 Nov | 31 Dic | Todo previo |

## Conclusiones y Recomendaciones

Este roadmap es flexible; revisar mensualmente con reuniones Ruben-Alex. Priorizar MVP para validación rápida. Si se alcanza la meta en mayo, reinvertir en growth. Para generar el PDF real, copia este contenido en un editor como Google Docs o Markdown-to-PDF tool (e.g., Pandoc) y exporta. Contacta para ajustes.
