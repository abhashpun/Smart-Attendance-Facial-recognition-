import base64
import io
from PIL import Image

def base64_to_image(base64_string: str) -> Image.Image:
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]
    img_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(img_data))
