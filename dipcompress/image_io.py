import numpy as np
from PIL import Image


def load_image(path:str)->tuple[np.ndarray,dict]:

    img = Image.open(path)
    
    if img.mode not in ['RGB', 'L']:
       img  = img.convert('RGB')

    pixels = np.array(img, dtype = np.uint8)

    metadata = {
        'width': img.width,
        'height': img.height,
        'mode': img.mode,
        'channels': 1 if img.mode == 'L' else 3

    }
    return pixels, metadata

def save_image(pixels:np.ndarray, path:str, mode: str = 'L'):
    img = Image.fromarray(pixels, mode=mode)
    img.save(path)

def pixels_to_bytes(pixels:np.ndarray) -> bytes:
    return pixels.tobytes()

def bytes_to_pixels(data:bytes, width:int, height:int, channels:int):
    arr = np.frombuffer(data, dtype=np.uint8)
    if channels == 1:
        return arr.reshape((height, width))
    else:
        return arr.reshape((height, width, channels))

