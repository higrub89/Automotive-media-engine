# Guía Rápida: Zero-Cost Automotive Engine 🏎️

Genera videos técnicos de alta calidad sin costo alguno.

## 1. Setup Express (5 minutos)

### A. Instalar Dependencias
```bash
# Sistema
sudo apt update && sudo apt install -y libcairo2-dev libpango1.0-dev ffmpeg texlive-base

# Python
cd ~/Automatitation/automotive-media-engine
source venv/bin/activate
pip install -r requirements.txt
```

### B. Configurar Gemini
Crea un archivo `.env` y añade tu clave de Google AI Studio:
```bash
GEMINI_API_KEY=AIza...
```

**Nota:** No necesitas configurar ElevenLabs ni Claude. Usamos Edge-TTS y Manim (Gratis).

## 2. Generar Primer Video

```bash
python tests/generate_demo_video.py
```

Esto creará: `sf90_hybrid_demo.mp4`

- **Script**: Generado por Gemini Pro
- **Voz**: Christopher Neural (Microsoft)
- **Visuales**: Animaciones vectoriales generadas por Manim

## 3. Crear Tu Propio Contenido

1. Copia el template:
   ```bash
   cp templates/content_brief_template.md content/mi_video.md
   ```

2. Edítalo con tu tema técnico.

3. Genera (usando CLI, pendiente de implementación final o script custom):
   ```bash
   # Por ahora, modifica tests/generate_demo_video.py para apuntar a tu brief
   # O espera a la implementación del CLI completo en el siguiente paso.
   ```

## Calidad vs Velocidad

- **Audio**: Calidad estudio, generación instantánea.
- **Visuales**: Calidad vector (infinita), renderizado lento (~2x tiempo real).
- **Coste**: CERO.

¡Disfruta produciendo contenido de ingeniería pura!
