# Construcción de filtros (downscale, tonemap, formato)

def build_filters(meta: dict, cap_height: int = 1080, force_sdr: bool = True) -> str:
    """
    Crea la cadena de filtros:
    - Downscale a <=1080p con Lanczos (si aplica)
    - Tonemapping HDR -> SDR BT.709 (si aplica y hay soporte)
    - Formato yuv420p para compatibilidad
    """
    filters = []

    # Reescalar si excede altura tope
    if meta.get("height") and meta["height"] > cap_height:
        filters.append(f"scale=-2:{cap_height}:flags=lanczos")

    # HDR -> SDR BT.709 con zscale + tonemap (Hable)
    if force_sdr and meta.get("is_hdr"):
        filters.append("zscale=t=linear,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709")
        filters.append("format=yuv420p")
    else:
        filters.append("format=yuv420p")

    return ",".join(filters)

def color_tags(force_sdr: bool = True) -> list:
    """Etiqueta de color BT.709 para máxima compatibilidad."""
    if force_sdr:
        return [
            "-colorspace","bt709",
            "-color_primaries","bt709",
            "-color_trc","bt709",
        ]
    return []
