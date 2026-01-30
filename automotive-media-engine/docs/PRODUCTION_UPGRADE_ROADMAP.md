# Automotive Media Engine - Production Upgrade Roadmap
## Objetivo: Estándar ByCloud AI (Videos 10-15 min, Calidad Profesional)

**Fecha de Inicio:** 25 Enero 2026  
**Timeline Total:** 3-4 semanas  
**Inversión:** $5/mes (ElevenLabs Voice Cloning)

---

## 🎯 Estado Actual vs Objetivo

| Aspecto | Actual | Objetivo ByCloud | Prioridad |
|---------|--------|------------------|-----------|
| Duración video | 60-90s | 10-15 min | 🔴 CRÍTICO |
| Voz | Edge-TTS robótico | Tu voz clonada (ElevenLabs) | 🔴 CRÍTICO |
| Visuales | Manim básico + fotos | Grid animado + AI blueprints + B-roll | 🟡 ALTO |
| Ritmo | Cambio cada 8-10s | Cambio cada 2-4s | 🟡 ALTO |
| Estructura | Sin capítulos | 6 capítulos marcados | 🟢 MEDIO |
| Branding | Sin identidad | Avatar + intro/outro | 🟢 MEDIO |

---

## Fase 1: Voice Cloning con ElevenLabs (Semana 1)

### Objetivo
Reemplazar Edge-TTS con tu voz clonada para máxima autenticidad y personalidad.

### 1.1 Setup ElevenLabs

**Acción:**
```bash
# Instalar SDK
pip install elevenlabs

# Configurar API key
export ELEVENLABS_API_KEY="tu_api_key_aqui"
```

**Pasos:**
1. Crear cuenta en https://elevenlabs.io
2. Suscripción Creator ($5/mes)
   - 30,000 caracteres/mes (~20 videos de 10 min)
   - Voice cloning incluido
3. Obtener API key desde dashboard

### 1.2 Grabar Muestra de Voz

**Requisitos de grabación:**
- **Duración:** 5-10 minutos mínimo
- **Formato:** MP3 o WAV, 44.1kHz
- **Calidad:** Ambiente silencioso, sin ruido de fondo
- **Contenido:** Lee guiones técnicos variados (emociones diferentes)

**Script de grabación sugerido:**
```
# script_sample.txt
El Ferrari 296 GTB representa una revolución en la ingeniería híbrida.
[Pausa dramática]
Con 830 caballos de potencia, este V6 biturbo desafía todas las expectativas.

Hablemos de aerodinámica activa...
[Tono energético]
¡Las cifras son impresionantes! 860 kilos de carga aerodinámica a 285 km/h.

[Tono reflexivo]
Pero, ¿qué significa esto realmente para el piloto?
```

**Herramienta de grabación:**
```bash
# Usando Audacity (gratuito)
sudo apt install audacity
audacity
# Grabar, limpiar ruido, exportar como voice_sample.mp3
```

### 1.3 Implementar Módulo de Clonación

**Archivo:** `core/voice_cloner.py`

```python
from elevenlabs import clone, generate, set_api_key
from pathlib import Path

class ElevenLabsVoiceCloner:
    """
    Voice cloning con ElevenLabs.
    """
    
    def __init__(self, api_key: str):
        set_api_key(api_key)
        self.voice_id = None
    
    def clone_voice(self, sample_path: Path, voice_name: str = "Ruben") -> str:
        """
        Clona voz desde muestra de audio.
        
        Returns: voice_id para usar en generate()
        """
        voice = clone(
            name=voice_name,
            files=[str(sample_path)]
        )
        
        self.voice_id = voice.voice_id
        print(f"✓ Voz clonada: {voice_id}")
        
        return voice.voice_id
    
    def generate_narration(
        self, 
        text: str, 
        output_path: Path,
        voice_settings: dict = None
    ) -> Path:
        """
        Genera narración con voz clonada.
        
        Args:
            text: Texto con tags SSML ([PAUSE], [SHORT_PAUSE])
            voice_settings: {stability, similarity_boost, style}
        """
        # Convertir SSML tags a formato ElevenLabs
        processed_text = self._convert_ssml(text)
        
        settings = voice_settings or {
            "stability": 0.5,        # 0-1: más estable = menos variación
            "similarity_boost": 0.75, # 0-1: qué tan similar a muestra
            "style": 0.5              # 0-1: expresividad
        }
        
        audio = generate(
            text=processed_text,
            voice=self.voice_id,
            model="eleven_multilingual_v2",
            **settings
        )
        
        with open(output_path, "wb") as f:
            f.write(audio)
        
        return output_path
    
    def _convert_ssml(self, text: str) -> str:
        """
        Convierte tags SSML a formato ElevenLabs.
        
        [PAUSE] → ... (3 puntos)
        [SHORT_PAUSE] → , (coma)
        """
        text = text.replace("[PAUSE]", "...")
        text = text.replace("[SHORT_PAUSE]", ",")
        return text
```

### 1.4 Integrar en AudioFactory

**Modificar:** `core/audio_factory.py`

```python
# Añadir al inicio del archivo
from .voice_cloner import ElevenLabsVoiceCloner
import os

class AudioFactory:
    def __init__(self, use_elevenlabs: bool = True):
        self.use_elevenlabs = use_elevenlabs
        
        if use_elevenlabs:
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                raise ValueError("ELEVENLABS_API_KEY no configurado")
            
            self.voice_cloner = ElevenLabsVoiceCloner(api_key)
            # Cargar voice_id desde config
            self.voice_cloner.voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    
    def generate_audio(
        self, 
        script: VideoScript,
        output_filename: Optional[str] = None
    ) -> Path:
        """Genera audio con voz clonada o Edge-TTS."""
        
        if self.use_elevenlabs:
            return self._generate_elevenlabs(script, output_filename)
        else:
            return self._generate_edge_tts(script, output_filename)
    
    def _generate_elevenlabs(self, script, filename):
        """Genera con ElevenLabs."""
        output_path = self.audio_dir / (filename or f"narration_{timestamp}.mp3")
        
        self.voice_cloner.generate_narration(
            text=script.script_text,
            output_path=output_path,
            voice_settings={
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.6  # Más expresivo para automotive
            }
        )
        
        return output_path
```

### 1.5 Validación Fase 1

**Test:**
```bash
# Generar video test con voz clonada
python -m core.cli generate \
  --topic "Test Voice Cloning - Lamborghini Aventador" \
  --duration 60
```

**Checklist:**
- [ ] Cuenta ElevenLabs activa ($5/mes)
- [ ] Muestra de voz grabada (5-10 min)
- [ ] Voz clonada en ElevenLabs dashboard
- [ ] API key configurada en `.env`
- [ ] `voice_cloner.py` implementado
- [ ] AudioFactory integrado
- [ ] Test generado con tu voz
- [ ] Calidad de voz: 8/10 mínimo (subjetivo)

**Criterio de éxito:**  
Audio suena natural, con tu voz, pausas SSML funcionan, sin roboticidad.

---

## Fase 2: Sistema Visual Cinematográfico (Semana 2)

### Objetivo
Gráficos técnicos animados + B-roll cinematográfico + grid dinámico estilo ByCloud.

### 2.1 Dynamic Technical Grid Background

**Archivo:** `core/visual_assembly.py`

**Implementar:**
```python
class DynamicGridBackground(Scene):
    """
    Fondo oscuro con grid técnico animado.
    Emula estética ByCloud AI.
    """
    def construct(self):
        # Grid principal
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": "#1A2332",
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={"stroke_opacity": 0}
        )
        
        # Líneas de acento (grid secundario)
        accent_grid = NumberPlane(
            x_range=[-20, 20, 5],
            y_range=[-12, 12, 5],
            background_line_style={
                "stroke_color": "#2A4A6A",
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )
        
        # Animación sutil de pulso
        self.play(
            grid.animate.set_opacity(0.3),
            accent_grid.animate.set_opacity(0.5),
            rate_func=there_and_back_with_pause,
            run_time=2
        )
        
        self.add(grid, accent_grid)
```

**Aplicar a todas las escenas:**
```python
class TechnicalScene(Scene):
    def construct(self):
        # 1. Fondo grid SIEMPRE
        bg = DynamicGridBackground()
        self.add(bg)
        
        # 2. Contenido específico
        self.build_scene_content()
```

### 2.2 AI Image Generation (Flux API)

**Opción:** Usar Replicate API (gratis tier: 50 generaciones/mes)

**Setup:**
```bash
pip install replicate
export REPLICATE_API_TOKEN="tu_token"
```

**Archivo:** `core/ai_image_generator.py`

```python
import replicate
from pathlib import Path

class AIBlueprintGenerator:
    """
    Genera imágenes técnicas con IA on-demand.
    """
    
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    def generate_blueprint(
        self, 
        topic: str, 
        style: str = "technical_blueprint"
    ) -> Path:
        """
        Genera diagrama técnico de alta calidad.
        
        Styles:
        - technical_blueprint: Plano técnico azul oscuro
        - cutaway_realistic: Vista en corte fotorrealista
        - schematic_minimal: Esquema vectorial limpio
        """
        prompts = {
            "technical_blueprint": f"""
            Professional automotive engineering blueprint of {topic}.
            Dark blue background, white/cyan technical lines,
            precise measurements, annotations, aerospace grade,
            isometric view, 8K resolution
            """,
            "cutaway_realistic": f"""
            Photorealistic technical cutaway illustration of {topic}.
            Internal components visible, engineering photography style,
            studio lighting, white background, extremely detailed
            """,
            "schematic_minimal": f"""
            Minimalist technical schematic of {topic}.
            Clean vector lines, dark background, key components labeled,
            professional CAD style, high contrast
            """
        }
        
        output = self.client.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompts[style],
                "num_outputs": 1,
                "aspect_ratio": "16:9",
                "output_quality": 90
            }
        )
        
        # Descargar imagen
        image_url = output[0]
        image_path = Path(f"./assets/generated/{topic.replace(' ', '_')}.png")
        self._download(image_url, image_path)
        
        return image_path
```

**Integrar en VisualAssembly:**
```python
class ImageTechnicalScene(TechnicalScene):
    def build_scene_content(self):
        # En lugar de buscar en assets, generar con IA
        topic = self.data.visual_config.get("topic", "generic engine")
        
        generator = AIBlueprintGenerator()
        image_path = generator.generate_blueprint(
            topic=topic,
            style="technical_blueprint"
        )
        
        # Resto del código igual...
```

### 2.3 B-Roll Integration (Stock Footage)

**API:** Pexels (gratis, 200 requests/hora)

**Setup:**
```bash
pip install pexels-api
export PEXELS_API_KEY="tu_api_key"
```

**Archivo:** `core/broll_manager.py`

```python
from pexelsapi.pexels import Pexels
import requests

class BRollManager:
    """
    Descarga clips de stock para B-roll.
    """
    
    def __init__(self):
        self.pexels = Pexels(os.getenv("PEXELS_API_KEY"))
    
    def fetch_clips(
        self, 
        keywords: list[str], 
        count: int = 3,
        duration: str = "medium"  # short/medium/long
    ) -> list[Path]:
        """
        Busca y descarga clips relacionados.
        
        Returns: Lista de paths a clips MP4
        """
        clips = []
        
        for keyword in keywords:
            # Buscar videos
            results = self.pexels.search_videos(
                query=keyword,
                per_page=count,
                size=duration
            )
            
            for video in results["videos"]:
                # Descargar versión HD
                hd_url = video["video_files"][0]["link"]
                clip_path = Path(f"./assets/broll/{keyword}_{video['id']}.mp4")
                
                self._download(hd_url, clip_path)
                clips.append(clip_path)
        
        return clips
    
    def _download(self, url: str, path: Path):
        """Descarga video."""
        response = requests.get(url, stream=True)
        with open(path, "wb") as f:
            f.write(response.content)
```

**Lógica de inserción:**
```python
# En video_assembler.py
def assemble_video_with_broll(self, config, audio_path, visual_paths):
    """
    Inserta B-roll cada 15-20s.
    """
    timeline = []
    
    for i, scene_path in enumerate(visual_paths):
        timeline.append(scene_path)
        
        # Cada 3 escenas (~15-20s), insertar B-roll
        if (i + 1) % 3 == 0:
            keywords = self._extract_keywords(config.script.scenes[i])
            broll_clips = BRollManager().fetch_clips(keywords, count=1)
            
            if broll_clips:
                timeline.append(broll_clips[0])
    
    # Concatenar todo con ffmpeg
    final_video = self._concatenate(timeline, audio_path)
    return final_video
```

### 2.4 Validación Fase 2

**Checklist:**
- [ ] Grid dinámico en todas las escenas
- [ ] AI genera imágenes técnicas coherentes
- [ ] B-roll se inserta cada 15-20s
- [ ] Cambios visuales cada 2-4s
- [ ] Resolución Full HD 1920x1080 @ 60 FPS

---

## Fase 3: Contenido Extendido (Semana 3)

### Objetivo
Scripts de 10-12 minutos con estructura de capítulos profesional.

### 3.1 Extended Script Prompt

**Modificar:** `core/script_engine.py`

```python
EXTENDED_SYSTEM_PROMPT = """
Eres un guionista técnico experto en contenido automotriz de larga duración.

OBJETIVO: Generar guion de {duration} minutos ({words} palabras aprox) estructurado en capítulos.

ESTRUCTURA OBLIGATORIA:

[HOOK] (30s - 75 palabras)
Pregunta intrigante que enganche desde el segundo 1.
Ejemplo: "¿Cómo un V6 de 3.0L humilla a motores V8 de 5.0L?"

[INTRODUCCIÓN] (1 min - 150 palabras)
- Contexto histórico
- Por qué este tema importa AHORA
- Qué aprenderá el espectador

[CAPÍTULO 1: FUNDAMENTOS] (3 min - 450 palabras)
Explicación técnica accesible:
- Conceptos básicos con analogías
- 3-4 datos técnicos específicos
- [VISUAL: blueprint] indicators donde sea relevante

[CAPÍTULO 2: ANÁLISIS PROFUNDO] (4 min - 600 palabras)
Detalles avanzados:
- Física / Ingeniería / Telemetría
- Comparativas con competencia
- Casos de uso reales
- [VISUAL: graph] para datos numéricos

[CAPÍTULO 3: IMPACTO Y FUTURO] (2 min - 300 palabras)
- Implicaciones en la industria
- Tendencias futuras
- Opinión experta

[CONCLUSIÓN] (1 min - 150 palabras)
- Resumen puntos clave (3 bullets max)
- Pregunta para engagement
- CTA: "Si quieres análisis como este..."

PROSODY CRÍTICA:
- [SHORT_PAUSE] antes de CADA cifra técnica
- [PAUSE] para crear suspense antes de reveals
- Máximo 1 [PAUSE] por párrafo

TONO: Mentor experimentado, no profesor aburrido. Usa metáforas, analogías motorizadas.

Genera AHORA el guion completo.
"""
```

### 3.2 Capítulos en YouTube

**Implementar:** `core/video_assembler.py`

```python
def add_youtube_chapters(self, script: VideoScript, output_path: Path):
    """
    Extrae timestamps de capítulos y los escribe en descripción.
    """
    chapters = []
    current_time = 0
    
    for section in script.sections:
        timestamp = self._format_timestamp(current_time)
        chapters.append(f"{timestamp} {section.title}")
        current_time += section.duration
    
    # Escribir chapters.txt para YouTube
    chapters_file = output_path.parent / f"{output_path.stem}_chapters.txt"
    with open(chapters_file, "w") as f:
        f.write("\n".join(chapters))
    
    return chapters_file
```

**Output ejemplo:**
```
0:00 Hook - El V6 que Cambió Todo
0:30 Introducción
1:30 Fundamentos del Motor Híbrido
4:30 Análisis Profundo de Potencia
8:30 Impacto en la Industria
10:30 Conclusión
```

### 3.3 Validación Fase 3

**Checklist:**
- [ ] Scripts generan 1500-1800 palabras
- [ ] 6 secciones claras (Hook, Intro, 3 capítulos, Conclusión)
- [ ] Archivo chapters.txt generado
- [ ] Duración objetivo: 10-12 min

---

## Fase 4: Brand Identity (Semana 4)

### Objetivo
Avatar, intro/outro, identidad visual consistente.

### 4.1 Avatar "El Ingeniero"

**Opción simple:** Ilustración estática con animación sutil

**Herramienta:** Canva Pro (gratis 30 días) → Diseñar silueta de piloto

**Implementación Manim:**
```python
class AvatarOverlay(Scene):
    """
    Avatar en esquina inferior durante explicaciones.
    """
    def construct(self):
        # Cargar imagen del avatar
        avatar = ImageMobject("./assets/branding/avatar.png")
        avatar.scale(0.3).to_corner(DR, buff=0.5)
        
        # Animación idle (respiración sutil)
        self.play(
            avatar.animate.scale(1.05).set_opacity(0.9),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.add(avatar)
```

### 4.2 Intro Template (5s)

```python
def create_intro(topic: str) -> VideoClip:
    """
    Intro de 5s:
    - Logo del canal con efecto glitch
    - Título del video
    - Avatar aparece
    """
    intro = Scene()
    
    # Logo
    logo = Text("AUTOMOTIVE\nENGINEERING", font="Orbitron").scale(1.5)
    intro.play(FadeIn(logo, scale=0.5), run_time=1)
    
    # Título
    title = Text(topic, font="Roboto Condensed", color=HIGHLIGHT_COLOR)
    intro.play(TransformFromCopy(logo, title), run_time=1.5)
    
    # Avatar
    avatar = ImageMobject("avatar.png").to_corner(DR)
    intro.play(FadeIn(avatar, shift=LEFT), run_time=1.5)
    
    return intro.render()
```

### 4.3 Outro Template (10s)

- CTA: "Suscríbete para más análisis técnicos"
- Próximo video teaser
- Links a redes sociales
- Música de cierre

### 4.4 Validación Fase 4

**Checklist:**
- [ ] Avatar diseñado y exportado
- [ ] Intro template funcional
- [ ] Outro template funcional
- [ ] Marca consistente en todos los videos

---

## Timeline y Milestones

### Semana 1: Voice (CRÍTICO)
- [x] Día 1-2: Setup ElevenLabs + grabar muestra
- [ ] Día 3-4: Implementar `voice_cloner.py`
- [ ] Día 5-7: Integrar en AudioFactory + test

**Milestone:** Video test con tu voz (60s)

### Semana 2: Visuales (ALTO)
- [ ] Día 8-10: Grid dinámico + AI images
- [ ] Día 11-13: B-roll integration
- [ ] Día 14: Test visual completo

**Milestone:** Video con grid + AI images + B-roll (90s)

### Semana 3: Contenido (MEDIO)
- [ ] Día 15-17: Extended script prompt
- [ ] Día 18-20: YouTube chapters
- [ ] Día 21: Video largo test (10 min)

**Milestone:** Primer video de 10 min completo

### Semana 4: Branding (PULIDO)
- [ ] Día 22-24: Diseño avatar + templates
- [ ] Día 25-27: Integración completa
- [ ] Día 28: Video final production-ready

**Milestone:** Video completo estilo ByCloud

---

## Configuración de Entorno

### Variables de Entorno (.env)

```bash
# ElevenLabs
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=xxxxxxxxxxxxxx

# Replicate (AI Images)
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx

# Pexels (B-Roll)
PEXELS_API_KEY=xxxxxxxxxxxxxxxxxxxxx

# Gemini (LLM)
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxx
```

### Dependencias Nuevas

```bash
# requirements.txt - AÑADIR:
elevenlabs==0.2.27
replicate==0.15.0
pexels-api==1.0.1
```

**Instalar:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Métricas de Éxito Final

| Métrica | Actual | Objetivo | Validación |
|---------|--------|----------|------------|
| Duración | 60-90s | 10-12 min | ✓ Script 1500-1800 palabras |
| Voz | Edge-TTS | Tu voz clonada | ✓ Test subjetivo 8/10 |
| Cambios visuales/min | 6-8 | 20-30 | ✓ B-roll cada 15s |
| Resolución | 1920x1080 | 1920x1080 @ 60 FPS | ✓ FFmpeg metadata |
| Identidad | No | Avatar + templates | ✓ Branding visible |
| Estructura | Plana | 6 capítulos | ✓ YouTube chapters |

---

## Próximo Paso Inmediato

### ACCIÓN 1: Setup ElevenLabs (HOY)
```bash
# 1. Crear cuenta
# https://elevenlabs.io/sign-up

# 2. Suscribirse a Creator ($5/mes)
# Dashboard → Subscriptions → Creator

# 3. Obtener API key
# Dashboard → Profile → API Keys → Create

# 4. Configurar
echo 'ELEVENLABS_API_KEY=sk_xxxxxx' >> .env

# 5. Instalar SDK
pip install elevenlabs
```

### ACCIÓN 2: Grabar Muestra de Voz (HOY/MAÑANA)
- Abrir Audacity
- Grabar 10 min leyendo `scripts/voice_sample.txt`
- Exportar como `voice_sample.mp3`
- Subir a ElevenLabs dashboard

### ACCIÓN 3: Implementar `voice_cloner.py` (DÍA 3-4)
- Copiar código de este roadmap
- Test: Generar audio de 30s
- Validar calidad

---

## Recursos y Referencias

- **ElevenLabs Docs:** https://docs.elevenlabs.io/api-reference
- **Replicate Flux:** https://replicate.com/black-forest-labs/flux-schnell
- **Pexels API:** https://www.pexels.com/api/
- **ByCloud AI (Referencia):** https://www.youtube.com/@bycloudAI
- **Manim Docs:** https://docs.manim.community/

---

## Notas Importantes

⚠️ **Costos mensuales estimados:**
- ElevenLabs Creator: $5/mes (fijo)
- Replicate (AI images): ~$0-2/mes (50 gratis/mes)
- **Total: ~$5-7/mes**

💡 **Optimizaciones futuras:**
- Batch processing de videos
- Templates personalizados por tema
- Análisis de retención para mejorar ritmo
- Monetización ($100-500/mes objetivo con AdSense + afiliados)
