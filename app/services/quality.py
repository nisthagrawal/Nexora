"""Measured image-quality evidence, never a fraud classifier."""
from __future__ import annotations

from io import BytesIO
from PIL import Image, ImageStat


def assess_image_quality(content: bytes) -> dict[str, object]:
    image = Image.open(BytesIO(content)).convert("L")
    width, height = image.size
    stat = ImageStat.Stat(image)
    brightness = round(stat.mean[0], 1)
    contrast = round(stat.stddev[0], 1)
    # A lightweight, deterministic texture proxy; OpenCV Laplacian can replace it.
    pixels = image.resize((min(width, 512), min(height, 512))).load()
    w, h = image.resize((min(width, 512), min(height, 512))).size
    differences = [abs(pixels[x, y] - pixels[x - 1, y]) for y in range(1, h) for x in range(1, w)]
    sharpness = round(sum(differences) / max(1, len(differences)), 2)
    usable = width >= 800 and height >= 500 and contrast >= 20 and sharpness >= 5
    return {"width": width, "height": height, "brightness": brightness, "contrast": contrast, "sharpness_proxy": sharpness, "overall": "USABLE" if usable else "INSUFFICIENT IMAGE QUALITY", "explanation": "Measured image properties support screening." if usable else "Image properties are insufficient for reliable extraction; request a clearer capture."}
