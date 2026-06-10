from PIL import Image
import numpy as np

def main():
    img = Image.open("media/cat.png")   # Change path if needed
    arr = np.array(img)
    
    print("Image mode (from PIL):", img.mode)
    print("Array shape:", arr.shape)
    print("Data type:", arr.dtype)
    print("Min/Max pixel value:", arr.min(), arr.max())
    
    print("\nTop-left 3x3 pixels (RGB):")
    print(arr[0:3, 0:3])

    # gray scale 

    gr_img = img.convert("L")
    gr_arr = np.array(gr_img)

    print("\nGrayscale image mode (from PIL):", gr_img.mode)
    print("Grayscale array shape:", gr_arr.shape)
    print("Grayscale sample pixels:", gr_arr[0:5, 0:5])


    #RGB Channels 

    if len(arr.shape) == 3:

        r = arr[:,:,0]
        g = arr[:,:,1]
        b = arr[:,:,2]

        print("\nRed channel sample pixels:")
        print(r[0:5, 0:5])  
        print("\nGreen channel sample pixels:")
        print(g[0:5, 0:5])  
        print("\nBlue channel sample pixels:")
        print(b[0:5, 0:5])  
        
if __name__ == "__main__":
    main()