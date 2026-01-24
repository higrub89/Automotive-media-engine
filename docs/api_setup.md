# Configuración del Sistema Zero-Cost 🛠️

Esta arquitectura utiliza exclusivamente herramientas gratuitas de alta calidad ("Ingeniería de Coste Cero").

## Componentes del Stack

| Componente | Herramienta | Coste | Notas |
|------------|-------------|-------|-------|
| **Cerebro** | **Gemini Pro** | **Gratis** | Via API (Free Tier 42 Madrid / Personal) |
| **Audio** | **Edge-TTS** | **Gratis** | Voces neurales de Microsoft (sin API Key) |
| **Visuales** | **Manim** | **Gratis** | Animaciones matemáticas vectoriales (Python) |
| **Búsqueda** | **Web-Search** | **Gratis** | MCP server via npx (sin API Key) |
| **Assembler** | **FFmpeg** | **Gratis** | Procesamiento de video industrial |

---

## 1. Gemini API (El único Key necesario)

1. Visita: https://aistudio.google.com/
2. Crea tu API Key.
3. Agrégala a tu `.env`:

```bash
GEMINI_API_KEY=AIza...
```

---

## 2. Dependencias del Sistema

Para que Manim (visuales) y Edge-TTS (audio) funcionen, necesitas instalar estas librerías en Ubuntu:

```bash
sudo apt update
sudo apt install -y libcairo2-dev libpango1.0-dev ffmpeg texlive-base
```

* `texlive-base` es opcional pero recomendado para fórmulas matemáticas en Manim.

---

## 3. Verificar Instalación

Ejecuta el test suite automatizado:

```bash
python tests/test_apis.py
```

Deberías ver:
```
============================================================
TEST RESULTS
============================================================
Gemini API (LLM).................. ✅ PASS
Edge-TTS (Audio).................. ✅ PASS
Manim (Visuals)................... ✅ PASS
FFmpeg (Assembly)................. ✅ PASS
============================================================
```

---

## 4. Generar Video Demo

Para probar el pipeline completo (Script → Narración Neural → Animación Vectorial → Video):

```bash
python tests/generate_demo_video.py
```

El proceso tardará unos 2-3 minutos debido al renderizado de alta calidad de Manim.

---

## Notas de Rendimiento

- **Audio**: Edge-TTS es instantáneo y no tiene límites estrictos.
- **Visuales**: Manim usa CPU intensivamente. Un video de 60s puede tardar 60-120s en renderizarse en 1080p.
- **Coste**: €0.00 garantizado.

---

**¡Sistema listo para producción masiva sin factura a fin de mes!**
