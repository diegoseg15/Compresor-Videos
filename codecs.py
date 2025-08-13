# Parámetros por códec (CRF/preset)

def quality_to_crf(codec: str, quality: str) -> int:
    """
    CRF recomendado por códec y nivel de calidad.
    Menor CRF = más calidad (y más peso).
    """
    q = quality.lower()
    if codec == "h264":
        return {"high": 18, "medium": 21, "low": 24}[q]
    if codec == "hevc":
        return {"high": 20, "medium": 23, "low": 26}[q]
    if codec == "av1":
        return {"high": 22, "medium": 28, "low": 32}[q]
    return 23

def codec_to_args(codec: str, crf: int, preset: str, tune_grain: bool = False) -> list:
    """
    Devuelve los argumentos de FFmpeg para el códec elegido.
    Soporta: h264 (libx264), hevc (libx265), av1 (libaom-av1).
    """
    if codec == "h264":
        args = ["-c:v","libx264","-crf",str(crf),"-preset",preset]
        if tune_grain:
            args += ["-tune","film"]
        return args

    if codec == "hevc":
        args = ["-c:v","libx265","-crf",str(crf),"-preset",preset,"-tag:v","hvc1"]
        if tune_grain:
            args += ["-tune","grain"]
        return args

    if codec == "av1":
        # Mapeo simple de preset -> cpu-used para libaom-av1
        cpu_used = {"veryslow":0, "slower":1, "slow":2, "medium":4, "fast":6, "faster":8}.get(preset, 4)
        args = ["-c:v","libaom-av1","-crf",str(crf),"-b:v","0","-cpu-used",str(cpu_used)]
        if tune_grain:
            args += ["-enable-tpl","1","-tune","ssim"]
        return args

    raise ValueError("Códec no soportado")
