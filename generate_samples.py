import cv2
import numpy as np
import os
import urllib.request

def create_sample():
    # 1. sample.jpg (Colorida)
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    img[:] = (200, 200, 200) # fundo cinza
    cv2.rectangle(img, (50, 50), (150, 150), (255, 0, 0), -1) # Quadrado Azul
    cv2.circle(img, (250, 100), 50, (0, 255, 0), -1) # Círculo Verde
    cv2.fillPoly(img, [np.array([[200, 250], [150, 200], [250, 200]])], (0, 0, 255)) # Triângulo Vermelho
    cv2.imwrite('data/input/sample.jpg', img)
    print("sample.jpg gerada.")

    # 2. parafusos.jpg (Simulando parafusos)
    img_parafusos = np.ones((400, 400, 3), dtype=np.uint8) * 255 # fundo branco
    for pt in [(100, 100), (300, 150), (200, 300), (150, 200), (320, 320)]:
        cv2.circle(img_parafusos, pt, 15, (50, 50, 50), -1) # Parafusos cinza escuro
        # Adicionar ranhura no parafuso
        cv2.line(img_parafusos, (pt[0]-10, pt[1]-10), (pt[0]+10, pt[1]+10), (20, 20, 20), 2)
    cv2.imwrite('data/input/parafusos.jpg', img_parafusos)
    print("parafusos.jpg gerada.")

    # 3. documento_inclinado.jpg
    img_doc = np.ones((500, 500, 3), dtype=np.uint8) * 255
    text_img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(text_img, "DOCUMENTO OFICIAL", (50, 100), font, 1, (0, 0, 0), 2)
    cv2.putText(text_img, "Este texto esta inclinado", (50, 150), font, 0.8, (0, 0, 0), 2)
    cv2.putText(text_img, "para testar o modulo 5.", (50, 200), font, 0.8, (0, 0, 0), 2)
    
    # Rotacionar a imagem de texto
    M = cv2.getRotationMatrix2D((250, 250), 15, 1.0) # Inclinação de 15 graus
    img_doc = cv2.warpAffine(text_img, M, (500, 500), borderValue=(255, 255, 255))
    
    # Adicionar uma borda retangular que também é rotacionada
    cv2.rectangle(text_img, (30, 50), (450, 250), (0, 0, 0), 2)
    img_doc = cv2.warpAffine(text_img, M, (500, 500), borderValue=(255, 255, 255))
    cv2.imwrite('data/input/documento_inclinado.jpg', img_doc)
    print("documento_inclinado.jpg gerada.")

    # 4. cena.jpg (Segmentação semântica)
    img_cena = np.zeros((400, 600, 3), dtype=np.uint8)
    img_cena[:] = (255, 255, 255) # Fundo branco
    # Céu
    cv2.rectangle(img_cena, (0, 0), (600, 200), (255, 200, 100), -1) # Azul claro (BGR)
    # Via
    cv2.rectangle(img_cena, (0, 200), (600, 400), (100, 100, 100), -1) # Cinza
    # Árvores
    cv2.circle(img_cena, (100, 150), 40, (0, 150, 0), -1) # Verde escuro
    cv2.circle(img_cena, (500, 160), 50, (0, 180, 0), -1)
    # Carros
    cv2.rectangle(img_cena, (200, 250), (280, 290), (0, 0, 200), -1) # Vermelho
    cv2.rectangle(img_cena, (400, 300), (450, 330), (0, 0, 180), -1)
    cv2.imwrite('data/input/cena.jpg', img_cena)
    print("cena.jpg gerada.")
    
    # 5. Vídeo de pessoas
    # Vamos baixar um vídeo curto para testes, ou criar um vídeo sintético se o download falhar
    video_path = 'data/input/pessoas.mp4'
    url = "https://www.w3schools.com/html/mov_bbb.mp4" # Vídeo de exemplo genérico (big buck bunny)
    # Para o YOLO identificar pessoas, big buck bunny não é ideal, mas vamos baixar e testar.
    # Outra opção é baixar uma imagem com pessoas e replicar frames
    try:
        print("Baixando vídeo de exemplo...")
        urllib.request.urlretrieve("https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4", video_path)
        print("pessoas.mp4 baixado.")
    except Exception as e:
        print("Não foi possível baixar o vídeo. Gerando um vídeo sintético (YOLO pode não detectar nada útil).")
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
        for i in range(30):
            frame = np.ones((300, 400, 3), dtype=np.uint8) * 200
            cv2.circle(frame, (100 + i*5, 150), 30, (0, 0, 0), -1) # Círculo andando
            out.write(frame)
        out.release()
        print("pessoas.mp4 sintético gerado.")

if __name__ == "__main__":
    os.makedirs('data/input', exist_ok=True)
    create_sample()
