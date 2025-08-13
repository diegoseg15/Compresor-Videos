# Punto de entrada CLI

import argparse
import sys
from pathlib import Path
from .ffutils import has_ffmpeg, valid_ext
from .compress import compress_one

def main():
    if not has_ffmpeg():
        print("❌ Necesitas ffmpeg y ffprobe en el PATH.", file=sys.stderr)
        sys.exit(1)

    ap = argparse.ArgumentParser(
        description="Comprime videos (<=1080p, SDR BT.709, CRF) manteniendo SIEMPRE el audio original."
    )
    ap.add_argument("input", help="Archivo o carpeta de entrada")
    ap.add_argument("-o","--output", help="Archivo o carpeta de salida")
    ap.add_argument("--codec", choices=["h264","hevc","av1"], default="hevc",
                    help="Códec de salida (hevc por defecto).")
    ap.add_argument("--quality", choices=["high","medium","low"], default="medium",
                    help="Nivel de calidad perceptual (CRF).")
    ap.add_argument("--preset", default="medium",
                    help="Preset del códec (velocidad/calidad). Ej: veryslow, slow, medium, fast.")
    ap.add_argument("--tune-grain", action="store_true", help="Mejor preservación de grano/película.")
    ap.add_argument("--cap-height", type=int, default=1080, help="Altura máxima de salida.")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print("❌ Entrada no existe.", file=sys.stderr)
        sys.exit(1)

    out_base = Path(args.output) if args.output else None

    # Archivo único
    if in_path.is_file():
        if not valid_ext(in_path):
            print("❌ Extensión no soportada.", file=sys.stderr)
            sys.exit(1)
        out_path = out_base if (out_base and out_base.suffix) else (out_base or in_path.with_suffix(".compressed.mp4"))
        print(f"⏳ Procesando: {in_path.name}")
        compress_one(in_path, out_path, args.codec, args.quality, args.preset,
                     args.tune_grain, args.cap_height)
        print(f"✅ Listo: {out_path}")
        return

    # Carpeta: procesar recursivamente
    out_dir = out_base if out_base else in_path / "compressed_out"
    out_dir.mkdir(parents=True, exist_ok=True)

    videos = [p for p in in_path.rglob("*") if p.is_file() and valid_ext(p)]
    if not videos:
        print("⚠️ No se encontraron videos en la carpeta.", file=sys.stderr)
        sys.exit(1)

    for v in videos:
        rel = v.relative_to(in_path)
        target_dir = out_dir / rel.parent
        target_dir.mkdir(parents=True, exist_ok=True)
        out_path = target_dir / (v.stem + ".mp4")
        print(f"⏳ Procesando: {rel}")
        compress_one(v, out_path, args.codec, args.quality, args.preset,
                     args.tune_grain, args.cap_height)
        print(f"✅ Listo: {out_path}")
