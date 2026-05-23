import cv2
import numpy as np
import os
from rembg import remove
from PIL import Image

def run(image_path, params=None, output_dir='data/output/mod6'):
    if params is None:
        params = {}
        
    if not os.path.exists(image_path):
        return None
        
    # Usando PIL para compatibilidade fácil com o rembg que já converte para RGBA
    try:
        input_img = Image.open(image_path)
    except Exception as e:
        print(f"Erro ao abrir imagem com PIL: {e}")
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Remover Fundo (Alpha Channel)
    # remove() do rembg aceita PIL Image e retorna PIL Image (RGBA)
    output_bg_removed = remove(input_img)
    alpha_path = os.path.join(output_dir, '1_fundo_removido.png')
    output_bg_removed.save(alpha_path)
    results["Fundo Removido (Alpha)"] = alpha_path.replace('\\', '/')
    
    # Converter PIL RGBA para NumPy CV2
    img_rgba = np.array(output_bg_removed)
    # Converter RGB para BGR do OpenCV
    img_rgba = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGRA)
    
    # 2. Composição com Chroma Key (Fundo Verde)
    # Criar um fundo verde do mesmo tamanho
    h, w = img_rgba.shape[:2]
    green_bg = np.zeros((h, w, 3), dtype=np.uint8)
    green_bg[:] = (0, 255, 0) # BGR verde
    
    # Separar canais
    alpha_channel = img_rgba[:, :, 3] / 255.0
    fg = img_rgba[:, :, :3]
    
    # Fazer o blend (alpha compositing)
    composite = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(3):
        composite[:, :, c] = (alpha_channel * fg[:, :, c] + (1 - alpha_channel) * green_bg[:, :, c])
        
    green_path = os.path.join(output_dir, '2_composicao_verde.jpg')
    cv2.imwrite(green_path, composite)
    results["Composição (Fundo Verde)"] = green_path.replace('\\', '/')

    return {
        "original": image_path,
        "results": results
    }
