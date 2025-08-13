# Lógica de compresión de un archivo

from pathlib import Path
from .ffutils import probe_video, run
from .filters import build_filters, color_tags
from .codecs import quality_to_crf, codec_to_args

def compress_one(in_path: Path, out_path: Path, codec: str, quality: str,
                 preset: str, tune_grain: bool, cap_height: int) -> None:
    """
    Comprime un único archivo de video manteniendo audio original:
    - Filtros: downscale <=1080p, tonemap HDR->SDR si aplica, yuv420p
    - CRF/preset por códec
    - Audio: -c:a copy siempre que exista
    """
    meta = probe_video(in_path)
    vf = build_filters(meta, cap_height=cap_height, force_sdr=True)
    crf = quality_to_crf(codec, quality)
    v_args = codec_to_args(codec, crf, preset, tune_grain)

    a_args = ["-c:a", "copy"] if meta.get("has_audio") else []

    cmd = ["ffmpeg","-y","-i",str(in_path),
           "-vf", vf,
           *v_args,
           *color_tags(True),
           *a_args,
           "-movflags","+faststart",
           str(out_path)]

    rc, _, err = run(cmd)
    # Fallback si falta zscale/tonemap
    if rc != 0:
        if "No such filter: 'zscale'" in err:
            vf_fb = vf.replace(
                "zscale=t=linear,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709,",""
            ).replace(
                "zscale=t=linear,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709",""
            )
            cmd_fb = ["ffmpeg","-y","-i",str(in_path),
                      "-vf", vf_fb,
                      *v_args, *color_tags(True), *a_args,
                      "-movflags","+faststart", str(out_path)]
            rc2, _, err2 = run(cmd_fb)
            if rc2 != 0:
                raise RuntimeError(f"FFmpeg falló:\n{err2}")
        else:
            raise RuntimeError(f"FFmpeg falló:\n{err}")
