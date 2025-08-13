# Utilidades FFmpeg/ffprobe, validación de extensiones

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Tuple

SUPPORTED_EXTS = {".mp4", ".mov", ".mkv", ".m4v", ".ts", ".avi", ".webm"}

def run(cmd: list) -> Tuple[int, str, str]:
    """Ejecuta un comando y devuelve (rc, stdout, stderr)."""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def has_ffmpeg() -> bool:
    """Verifica si ffmpeg y ffprobe están disponibles en PATH."""
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))

def valid_ext(p: Path) -> bool:
    """Extensiones de video soportadas."""
    return p.suffix.lower() in SUPPORTED_EXTS

def probe_video(in_path: Path) -> Dict:
    """
    Obtiene metadatos clave del video con ffprobe.
    Devuelve dict con: width, height, pix_fmt, color_* , is_hdr, duration, has_audio
    """
    cmd = [
        "ffprobe","-v","error","-print_format","json",
        "-show_streams","-show_format", str(in_path)
    ]
    rc, out, err = run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffprobe error: {err}")

    info = json.loads(out)
    vstreams = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
    astreams = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    vs = vstreams[0] if vstreams else {}

    return {
        "width": int(vs.get("width", 0) or 0),
        "height": int(vs.get("height", 0) or 0),
        "pix_fmt": vs.get("pix_fmt"),
        "color_space": vs.get("color_space"),
        "color_transfer": vs.get("color_transfer"),
        "color_primaries": vs.get("color_primaries"),
        "is_hdr": str(vs.get("color_transfer","")).lower() in {"smpte2084","arib-std-b67"},  # PQ/HLG
        "duration": float((info.get("format") or {}).get("duration", 0) or 0),
        "has_audio": bool(astreams),
    }
