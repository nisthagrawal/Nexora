from io import BytesIO
from PIL import Image, ImageOps


def preprocess(content: bytes) -> bytes:
    """Normalise orientation and apply lightweight OpenCV enhancement when present."""
    image = ImageOps.exif_transpose(Image.open(BytesIO(content))).convert("RGB")
    image.thumbnail((2400, 2400))
    out = BytesIO()
    try:
        import cv2
        import numpy as np
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        frame = cv2.fastNlMeansDenoisingColored(frame, None, 3, 3, 7, 21)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
        image = Image.fromarray(cv2.cvtColor(cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2RGB))
    except ImportError:
        pass
    image.save(out, format="JPEG", quality=94)
    return out.getvalue()
