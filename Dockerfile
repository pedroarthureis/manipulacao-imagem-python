# Usar imagem oficial do Python
FROM python:3.10-slim

# Instalar dependências do sistema necessárias para o OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para o container
COPY . .

# Variável de ambiente para a porta (o Hugging Face Spaces usa a porta 7860 por padrão)
ENV PORT=7860
EXPOSE 7860

# Comando para rodar a aplicação Flask
CMD ["python", "app.py"]
