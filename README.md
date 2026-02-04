# 🎥 Video Compressor CLI

Herramienta **CLI en Python** para **comprimir videos de forma eficiente y compatible**, basada en **FFmpeg**, con soporte para **H.264, HEVC (H.265) y AV1**, preservando **siempre el audio original** y garantizando salida **SDR BT.709 ≤1080p**.

Incluye:
- Barra de progreso con ETA
- Procesamiento de archivos o carpetas completas
- Fallback automático si falla el tonemapping HDR
- Soporte opcional para **GPU (NVIDIA / Intel / AMD)**
- Ejecución nativa o vía **Docker**

---

## 🚀 Características principales

- ✅ Compresión perceptual por **CRF**
- ✅ Downscale automático a resolución máxima configurable
- ✅ Conversión HDR → SDR BT.709
- ✅ Audio sin recomprimir (`copy`)
- ✅ Procesamiento recursivo de carpetas
- ✅ Progreso en tiempo real (TTY y no-TTY)
- ✅ Soporte CPU y GPU (NVENC / QSV / AMF)
- ✅ Docker-ready (ideal para Windows)

---

## 📦 Requisitos

### Opción A – Uso local
- Python **3.9+**
- `ffmpeg` y `ffprobe` en el `PATH`

### Opción B – Docker (recomendado)
- Docker
- (Opcional) GPU NVIDIA con drivers y `nvidia-container-toolkit`

---

## 📥 Instalación

### 🔹 Local
```bash
pip install -e .
````

Verifica FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

---

### 🔹 Docker

```bash
docker build -t video_compressor .
```

O desde Windows:

```bat
compress_video.bat --install
```

---

## ▶️ Uso básico

### Archivo único

```bash
video-compressor input.mp4 -o output.mp4
```

### Carpeta completa

```bash
video-compressor ./videos -o ./videos_compressed
```

---

## ⚙️ Opciones disponibles

| Opción         | Descripción                        |
| -------------- | ---------------------------------- |
| `--codec`      | `h264`, `hevc` (default), `av1`    |
| `--quality`    | `high`, `medium`, `low`, `verylow` |
| `--preset`     | veryslow, slow, medium, fast       |
| `--cap-height` | Altura máxima (default 1080)       |
| `--tune-grain` | Mejor preservación de grano        |
| `--threads`    | Hilos FFmpeg (0 = auto)            |
| `--hw-enc`     | `nvidia`, `intel`, `amd`           |
| `--hw-decode`  | Decodificación por hardware        |
| `--dry-run`    | Solo lista videos                  |
| `--verbose`    | Muestra comandos FFmpeg            |

Ejemplo avanzado:

```bash
video-compressor ./input \
  -o ./output \
  --codec hevc \
  --quality medium \
  --preset slow \
  --cap-height 720 \
  --hw-enc nvidia \
  --verbose
```

---

## 🎨 Lógica de calidad (CRF)

| Códec | High | Medium | Low | Very Low |
| ----- | ---- | ------ | --- | -------- |
| H.264 | 18   | 21     | 24  | 30       |
| HEVC  | 20   | 23     | 26  | 32       |
| AV1   | 22   | 28     | 32  | 38       |

---

## 🧠 Pipeline de procesamiento

1. `ffprobe` → detección de metadatos
2. Downscale si excede altura máxima
3. HDR → SDR (zscale + Hable)
4. Video → CRF (CPU o GPU)
5. Audio → copy
6. `faststart` para streaming
7. Barra de progreso + ETA

---

## 🛡️ Compatibilidad garantizada

* Formato: `yuv420p`
* Color: `BT.709`
* Contenedor: `.mp4`
* Ideal para:

  * TVs
  * Web
  * Móviles
  * Redes sociales

---

## 📂 Extensiones soportadas

```
.mp4 .mov .mkv .m4v .ts .avi .webm
```

---

## 🧩 Estructura del proyecto

```
video_compressor/
├── cli.py
├── compress.py
├── codecs.py
├── ffutils.py
├── filters.py
Dockerfile
compress_video.bat
```

---

## 📜 Licencia

MIT License – úsalo, modifícalo y mejóralo sin miedo 🚀
