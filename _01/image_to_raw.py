from PIL import Image
import numpy as np
import os

def image_to_raw(image_path, output_path):
    img = Image.open(image_path)
    arr = np.array(img)


    with open(output_path, 'wb') as f:
        h,w,c = arr.shape
        f.write(h.to_bytes(2, 'big'))
        f.write(w.to_bytes(2, 'big'))
        f.write(c.to_bytes(1, 'big'))
        f.write(arr.tobytes())


    original = os.path.getsize(image_path)
    raw = os.path.getsize(output_path)
    

    print(f"Original size: {original} bytes")
    print(f"Raw size: {raw} bytes")
    print(f"PNG is {raw/original:.2f} times the size of the raw data")

def raw_to_image(raw_path, output_path):

    with open(raw_path, 'rb') as f:
        h = int.from_bytes(f.read(2), 'big')
        w = int.from_bytes(f.read(2), 'big')
        c = int.from_bytes(f.read(1), 'big')
        data = f.read()

    arr = np.frombuffer(data, dtype=np.uint8).reshape(h, w, c)
    img = Image.fromarray(arr)
    img.save(output_path)
    print(f"Restored: {output_path}")
    
if __name__ == "__main__":
    image_to_raw("media/cat.png", "media/cat.raw")
    raw_to_image("media/cat.raw", "media/cat_restored.png")


