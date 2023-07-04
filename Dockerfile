# Imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . .

# Instale as dependências especificadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que o aplicativo Dash estará em execução
EXPOSE 8050

# Execute o aplicativo Dash quando o contêiner for iniciado
CMD ["python", "main.py"]