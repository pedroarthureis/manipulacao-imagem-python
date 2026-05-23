import cv2
import os

def run(image_path, params=None, output_dir='data/output/mod4'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. JPG com Compressão (Qualidade 50)
    jpg_path = os.path.join(output_dir, '1_comprimido.jpg')
    cv2.imwrite(jpg_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    results["JPG (Alta Compressão)"] = jpg_path.replace('\\', '/')
    
    # 2. PNG Otimizado (Compressão zlib max: 9)
    png_path = os.path.join(output_dir, '2_otimizado.png')
    cv2.imwrite(png_path, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    results["PNG (Lossless Otimizado)"] = png_path.replace('\\', '/')
    
    # 3. WEBP (Formato Web Moderno)
    webp_path = os.path.join(output_dir, '3_moderno.webp')
    cv2.imwrite(webp_path, img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
    results["WEBP (Para Web)"] = webp_path.replace('\\', '/')

    # 4. TIFF (Formato Print/Profissional)
    tiff_path = os.path.join(output_dir, '4_profissional.tiff')
    cv2.imwrite(tiff_path, img)
    results["TIFF (Qualidade Máxima)"] = tiff_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
