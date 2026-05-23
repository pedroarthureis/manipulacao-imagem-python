import cv2
import os

def run(image_path, params=None, output_dir='data/output/mod1'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Aumentar/Reduzir Resolução (Escala)
    scale = float(params.get('scale', 0.5)) # Padrão: reduz pela metade
    height, width = img.shape[:2]
    new_w, new_h = int(width * scale), int(height * scale)
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
    scaled_path = os.path.join(output_dir, '1_escala.jpg')
    cv2.imwrite(scaled_path, scaled_img)
    results[f"Escala ({scale}x)"] = scaled_path.replace('\\', '/')
    
    # 2. Thumbnail (Tamanho fixo, cropando se necessário ou apenas resize)
    thumb_size = int(params.get('thumb_size', 128))
    thumb_img = cv2.resize(img, (thumb_size, thumb_size), interpolation=cv2.INTER_AREA)
    thumb_path = os.path.join(output_dir, '2_thumbnail.jpg')
    cv2.imwrite(thumb_path, thumb_img)
    results[f"Thumbnail ({thumb_size}x{thumb_size})"] = thumb_path.replace('\\', '/')
    
    # 3. Resize Proporcional por Largura
    target_width = int(params.get('target_width', 800))
    ratio = target_width / width
    prop_h = int(height * ratio)
    prop_img = cv2.resize(img, (target_width, prop_h), interpolation=cv2.INTER_AREA)
    prop_path = os.path.join(output_dir, '3_proporcional.jpg')
    cv2.imwrite(prop_path, prop_img)
    results[f"Proporcional (W:{target_width})"] = prop_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
