from io import BytesIO
from PIL import Image, ImageOps


def preprocess(content: bytes) -> bytes:
    """Normalise orientation and colour; keep this adapter replaceable with OpenCV deskewing."""
    image = ImageOps.exif_transpose(Image.open(BytesIO(content))).convert("RGB")
    image.thumbnail((2400, 2400))
    out = BytesIO()
    image.save(out, format="JPEG", quality=94)
    return out.getvalue()
