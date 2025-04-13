# Imagem base com Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para rodar o Flask em modo dev
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
