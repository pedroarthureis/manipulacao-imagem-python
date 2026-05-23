import cv2
import numpy as np
import os
import random

def run(image_path, params=None, output_dir='data/output/mod5'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Blur (Gaussian)
    blur_img = cv2.GaussianBlur(img, (15, 15), 0)
    blur_path = os.path.join(output_dir, '1_gaussian_blur.jpg')
    cv2.imwrite(blur_path, blur_img)
    results["Gaussian Blur"] = blur_path.replace('\\', '/')
    
    # 2. Sharpen (Nitidez)
    kernel_sharpen = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen_img = cv2.filter2D(img, -1, kernel_sharpen)
    sharpen_path = os.path.join(output_dir, '2_sharpen.jpg')
    cv2.imwrite(sharpen_path, sharpen_img)
    results["Sharpen (Nitidez)"] = sharpen_path.replace('\\', '/')
    
    # 3. Cartoon
    color = cv2.bilateralFilter(img, 9, 250, 250)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    cartoon_img = cv2.bitwise_and(color, color, mask=edges)
    cartoon_path = os.path.join(output_dir, '3_cartoon.jpg')
    cv2.imwrite(cartoon_path, cartoon_img)
    results["Efeito Cartoon"] = cartoon_path.replace('\\', '/')

    # 4. Sketch (Desenho)
    inv_gray = 255 - gray
    blurred_inv = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    sketch_img = cv2.divide(gray, 255 - blurred_inv, scale=256)
    sketch_path = os.path.join(output_dir, '4_sketch.jpg')
    cv2.imwrite(sketch_path, sketch_img)
    results["Efeito Sketch"] = sketch_path.replace('\\', '/')

    # 5. Pixel Art
    h, w = img.shape[:2]
    pixel_size = 16
    temp = cv2.resize(img, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    pixel_img = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    pixel_path = os.path.join(output_dir, '5_pixel_art.jpg')
    cv2.imwrite(pixel_path, pixel_img)
    results["Efeito Pixel Art"] = pixel_path.replace('\\', '/')

    # 6. Glitch
    glitch_img = img.copy()
    shift = 15
    glitch_img[:, :-shift, 2] = img[:, shift:, 2] # Shift Red channel
    glitch_img[:, shift:, 0] = img[:, :-shift, 0] # Shift Blue channel
    
    # Add some random lines
    for _ in range(5):
        y = random.randint(0, h-1)
        thickness = random.randint(1, 5)
        glitch_img[y:y+thickness, :] = glitch_img[y:y+thickness, :] * random.uniform(0.5, 1.5)
        
    glitch_path = os.path.join(output_dir, '6_glitch.jpg')
    cv2.imwrite(glitch_path, np.clip(glitch_img, 0, 255).astype(np.uint8))
    results["Efeito Glitch"] = glitch_path.replace('\\', '/')

    # 7. Vintage (Sépia)
    kernel_sepia = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(img, kernel_sepia)
    sepia_path = os.path.join(output_dir, '7_vintage.jpg')
    cv2.imwrite(sepia_path, sepia_img)
    results["Vintage (Sépia)"] = sepia_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
