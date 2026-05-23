import sys
from modules import mod1_basic, mod2_transform, mod3_color, mod4_format, mod5_filters, mod6_alpha

def print_menu():
    print("\n" + "="*50)
    print("SISTEMA DE EDIÇÃO PROFISSIONAL DE IMAGEM")
    print("="*50)
    print("1. Edição Básica (Redimensionar, Thumbnails)")
    print("2. Transformações (Crop, Rotação, Espelho)")
    print("3. Cores (Brilho, Contraste, Temperatura)")
    print("4. Formatos (Conversão e Compressão)")
    print("5. Filtros e Efeitos (Blur, Cartoon, Sépia)")
    print("6. Transparência (Remoção de Fundo, Alpha)")
    print("0. Sair")
    print("="*50)

def main():
    while True:
        print_menu()
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod1_basic.run(img_path)
        elif escolha == '2':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod2_transform.run(img_path)
        elif escolha == '3':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod3_color.run(img_path)
        elif escolha == '4':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod4_format.run(img_path)
        elif escolha == '5':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod5_filters.run(img_path)
        elif escolha == '6':
            img_path = input("Caminho da imagem [data/input/sample.jpg]: ") or 'data/input/sample.jpg'
            mod6_alpha.run(img_path)
        elif escolha == '0':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
