import base64
from PIL import Image
from io import BytesIO

def image_to_base64(image_file) -> str:
    """Convert image file to base64 string."""
    image = Image.open(image_file)
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
