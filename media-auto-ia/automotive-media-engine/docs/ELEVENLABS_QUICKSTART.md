# ElevenLabs Quick Start - Pre-Made Voice Test

## Objetivo
Validar integración de ElevenLabs usando una voz predeterminada antes de clonar tu propia voz.

---

## Paso 1: Obtener API Key

1. **Ir a ElevenLabs Dashboard:**
   https://elevenlabs.io/app/settings/api-keys

2. **Crear nueva API key:**
   - Click en "Create API Key"
   - Copiar la key (empieza con `sk_...`)

3. **Configurar en el proyecto:**
   ```bash
   cd ~/Automatitation/automotive-media-engine
   
   # Crear archivo .env si no existe
   cp .env.example .env
   
   # Editar .env y añadir tu API key
   nano .env
   ```

4. **Añadir a .env:**
   ```bash
   ELEVENLABS_API_KEY=sk_tu_api_key_aqui
   ```

---

## Paso 2: Ejecutar Test

```bash
cd ~/Automatitation/automotive-media-engine
source venv/bin/activate

# Ejecutar script de test
python tests/test_elevenlabs.py
```

**Output esperado:**
```
======================================================================
🎙️  ELEVENLABS VOICE TEST - Pre-made Voice
======================================================================
✅ API key found: sk_12345...
✅ ElevenLabs client initialized

📝 Test text:
   El Ferrari 296 GTB representa una revolución en la ingeniería híbrida...
   (232 characters)

🎭 Available pre-made voices:
   (Using first available voice for test)
   Voice ID: ErXwobaYiN019PkySvjV

🎵 Generating audio...
✓ Audio: assets/audio/elevenlabs_test.mp3
✓ Duration: X.Xs

✅ SUCCESS!
📁 Audio saved: assets/audio/elevenlabs_test.mp3

🎧 Listen to test:
   mpv assets/audio/elevenlabs_test.mp3
```

---

## Paso 3: Escuchar el Audio

```bash
# Reproducir audio generado
mpv assets/audio/elevenlabs_test.mp3

# O con cualquier reproductor
vlc assets/audio/elevenlabs_test.mp3
```

**Evalúa:**
- ✅ Calidad de voz (natural vs robótica)
- ✅ Pronunciación en español
- ✅ Entonación y pausas
- ✅ Claridad del audio

---

## Paso 4: Integrar en el Pipeline (Opcional)

Si la voz predeterminada te satisface, puedes usarla directamente sin clonar:

```bash
# Editar .env
nano .env
```

**Añadir:**
```bash
# Voice ID de Antoni (multilingual Spanish male)
ELEVENLABS_VOICE_ID=ErXwobaYiN019PkySvjV

# O explorar otras voces:
# - "Matias": Spanish male, technical calm
# - "Valentino": Spanish male, energetic  
# - "AZnzlk1XvdvUeBnXmlld": Spanish female
```

---

## Voces Predeterminadas Recomendadas (Español)

| Voice ID | Nombre | Características | Mejor Para |
|----------|--------|-----------------|------------|
| `ErXwobaYiN019PkySvjV` | Antoni | Multilingual, cálido | Contenido técnico profesional |
| `yoZ06aMxZJJ28mfd3POQ` | Matias | Spanish nativo, calmado | Análisis detallados |
| `onwK4e9ZLuTAKqWW03F9` | Valentino | Energético, juvenil | Content dinámico |

Para ver todas las voces disponibles:
https://elevenlabs.io/voice-library

---

## Limites de Free Tier

- **Caracteres/mes:** 10,000
- **Videos 60s:** ~6-7 por mes
- **Videos 10 min:** ~2-3 por mes

**Upgrade a Creator ($5/mes):**
- 30,000 caracteres/mes
- ~20 videos de 10 min
- Voice cloning incluido

---

## Troubleshooting

### Error: "API key invalid"
```bash
# Verificar que la key está en .env
cat .env | grep ELEVENLABS

# Recargar variables de entorno
source .env
```

### Error: "Quota exceeded"
- Has usado tus 10,000 caracteres del mes
- Espera al próximo mes o upgrade a Creator

### Error: "Network connection"
```bash
# Test conectividad
ping api.elevenlabs.io
```

---

## Próximos Pasos

### Opción A: Usar Voz Predeterminada
Si estás satisfecho con Antoni o Matias:
1. Configurar `ELEVENLABS_VOICE_ID` en `.env`
2. Modificar `audio_factory.py` para usar ElevenLabs
3. Generar primer video con CLI

### Opción B: Clonar Tu Voz
Si quieres personalización máxima:
1. Grabar `scripts/voice_sample.md` (10 min)
2. Usar `voice_cloner.clone_voice_from_sample()`
3. Obtener tu Voice ID personalizado

---

## Comandos Rápidos

```bash
# Test completo
cd ~/Automatitation/automotive-media-engine && source venv/bin/activate && python tests/test_elevenlabs.py

# Escuchar resultado
mpv assets/audio/elevenlabs_test.mp3

# Ver configuración actual
cat .env | grep ELEVENLABS
```
