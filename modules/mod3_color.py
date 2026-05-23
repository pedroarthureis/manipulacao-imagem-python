import cv2
import numpy as np
import os

def run(image_path, params=None, output_dir='data/output/mod3'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Brilho e Contraste
    alpha = float(params.get('contrast', 1.3)) # > 1 aumenta
    beta = int(params.get('brightness', 30))  # > 0 aumenta
    bc_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    bc_path = os.path.join(output_dir, '1_brilho_contraste.jpg')
    cv2.imwrite(bc_path, bc_img)
    results["Brilho e Contraste"] = bc_path.replace('\\', '/')
    
    # 2. Saturação (via HSV)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
    h, s, v = cv2.split(hsv)
    sat_factor = float(params.get('saturation', 1.5)) # Aumentar 50%
    s = s * sat_factor
    s = np.clip(s, 0, 255)
    hsv = cv2.merge([h, s, v]).astype("uint8")
    sat_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    sat_path = os.path.join(output_dir, '2_saturacao.jpg')
    cv2.imwrite(sat_path, sat_img)
    results["Saturação (Boost)"] = sat_path.replace('\\', '/')
    
    # 3. Temperatura (Quente/Frio alterando canal Red/Blue)
    # Aumentar vermelho, diminuir azul = quente
    temp_img = img.copy().astype(np.int16)
    temp_factor = int(params.get('temperature', 30))
    temp_img[:,:,2] = np.clip(temp_img[:,:,2] + temp_factor, 0, 255) # R
    temp_img[:,:,0] = np.clip(temp_img[:,:,0] - temp_factor, 0, 255) # B
    temp_img = temp_img.astype(np.uint8)
    temp_path = os.path.join(output_dir, '3_temperatura.jpg')
    cv2.imwrite(temp_path, temp_img)
    results["Temperatura (Quente)"] = temp_path.replace('\\', '/')

    # 4. Tons RGB (Apenas Vermelho)
    r_img = img.copy()
    r_img[:,:,0] = 0 # B
    r_img[:,:,1] = 0 # G
    r_path = os.path.join(output_dir, '4_tonalidade_rgb.jpg')
    cv2.imwrite(r_path, r_img)
    results["Apenas Vermelho (RGB)"] = r_path.replace('\\', '/')

    # 5. Preto e Branco
    bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw_path = os.path.join(output_dir, '5_preto_e_branco.jpg')
    cv2.imwrite(bw_path, bw_img)
    results["Preto e Branco"] = bw_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
