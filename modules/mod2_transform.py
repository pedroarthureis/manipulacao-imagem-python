import cv2
import numpy as np
import os

def run(image_path, params=None, output_dir='data/output/mod2'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Crop (Corte Central Quadrado)
    height, width = img.shape[:2]
    min_dim = min(height, width)
    start_x = width//2 - min_dim//2
    start_y = height//2 - min_dim//2
    crop_img = img[start_y:start_y+min_dim, start_x:start_x+min_dim]
    crop_path = os.path.join(output_dir, '1_crop.jpg')
    cv2.imwrite(crop_path, crop_img)
    results["Crop Central 1:1"] = crop_path.replace('\\', '/')
    
    # 2. Rotação (Arbitrária ou fixa)
    angle = float(params.get('angle', 45)) # Padrão: 45 graus
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Evitar cortar as bordas calculando o novo tamanho
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((height * sin) + (width * cos))
    new_h = int((height * cos) + (width * sin))
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    rot_img = cv2.warpAffine(img, M, (new_w, new_h), borderValue=(0,0,0))
    rot_path = os.path.join(output_dir, '2_rotacao.jpg')
    cv2.imwrite(rot_path, rot_img)
    results[f"Rotação ({angle}°)"] = rot_path.replace('\\', '/')
    
    # 3. Espelhar (Horizontal e Vertical)
    flip_h = cv2.flip(img, 1)
    flip_h_path = os.path.join(output_dir, '3_espelho_h.jpg')
    cv2.imwrite(flip_h_path, flip_h)
    results["Espelhado Horizontal"] = flip_h_path.replace('\\', '/')

    flip_v = cv2.flip(img, 0)
    flip_v_path = os.path.join(output_dir, '4_espelho_v.jpg')
    cv2.imwrite(flip_v_path, flip_v)
    results["Espelhado Vertical"] = flip_v_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
