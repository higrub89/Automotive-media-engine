# 🏗️ Automotive Media Engine - Actualización Visual V2.0

**Fecha:** 26/01/2026
**Estado:** Producción Híbrida

## 🌟 Resumen Ejecutivo
El motor de generación de video ha evolucionado de un sistema puramente basado en animaciones vectoriales (Manim) a un **Motor Híbrido Multi-Modal**. Ahora tiene la capacidad de decidir dinámicamente qué recurso visual es el mejor para cada escena, integrando inteligencia artificial generativa, stock footage cinematográfico y renderizado de código en tiempo real.

---

## 🔧 Arquitectura Técnica Implementada

### 1. El Cerebro (ScriptEngine)
El sistema ahora inyecta "triggers" visuales en el guion generado por Gemini:
- `technical_component`: Activa el generador de planos (AI Blueprints).
- `broll_query`: Activa el buscador de video HD (Pexels).
- `visual_type="code"`: Activa el renderizador de sintaxis (Manim Code).

### 2. El Cuerpo (VisualAssembly)
El archivo `core/visual_assembly.py` ha sido refactorizado para actuar como un "Orquestador Visual".

#### A. Módulo de Grid Dinámico
En lugar de renderizar siempre gráficos, el sistema evalúa la metadata de la escena:
```python
if visual_config.get("broll_query"):
    return _generate_broll_video()  # -> Pexels API
elif visual_config.get("technical_component"):
    return _generate_ai_blueprint_video() # -> Pollinations AI
elif visual_type == "code":
    return CodeScene() # -> Manim Highlighting
else:
    return ManimGraph() # -> Fallback clásico
```

#### B. Capacidades Nuevas
1.  **AI Blueprints (Pollinations)**
    *   Genera diagramas técnicos estilo "blueprint" (azul/blanco).
    *   Post-procesado con FFmpeg para añadir efecto "Ken Burns" (zoom lento) para convertir la imagen estática en video dinámico.
    
2.  **B-Roll Manager (Pexels Integration)**
    *   Conecta con la API de Pexels para buscar stock footage HD.
    *   Filtrado inteligente por orientación (Landscape/Portrait).
    *   Recorte automático (`ffmpeg -t duration`) para coincidir con la narración.

3.  **Code Renderer (Manim CodeScene)**
    *   Renderiza código C/C++/Python con tema "Monokai".
    *   **Solución Técnica Crítica Implementation**: Debido a limitaciones en la versión de Manim Community, se implementó un sistema de *File Buffering*: el código se escribe en tiempo real a un archivo temporal (`/tmp/temp.c`) para que Manim pueda leerlo y renderizarlo con `pygments`, evitando errores de parsing de strings directos.

### 3. La Voz (AudioFactory)
*   **Failover System**: Se detectó agotamiento de cuota en ElevenLabs (API Premium). Se validó el uso de **Edge-TTS** (Microsoft Neural Voices) como alternativa gratuita de alta calidad, permitiendo producción ilimitada sin costes.

---

## 🧪 Validación y Pruebas
Se han generado 3 "Golden Samples" para validar la estabilidad:

| Tipo | Script de Test | Resultado | Módulos Usados |
|------|----------------|-----------|----------------|
| **Técnico** | `generate_abs_video.py` | ✅ Éxito | Manim Base, Gemini, ElevenLabs |
| **Cinemático** | `generate_cybertruck.py` | ✅ Éxito | **Pexels**, Gemini, Edge-TTS |
| **Coding** | `generate_c_code_video.py` | ✅ Éxito | **CodeScene (Fix)**, Edge-TTS |

## 🚀 Próximos Pasos (Roadmap)
1.  **Automated Audio Failover**: Implementar lógica `try/except` en `AudioFactory` para switch automático ElevenLabs -> EdgeTTS.
2.  **Smart Caching**: Cachear descargas de Pexels y Blueprints para no regenerar/descargar lo mismo dos veces (ahorro de ancho de banda y tiempo).
