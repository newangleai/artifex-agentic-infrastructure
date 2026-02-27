FROM python:3.13-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando para iniciar o servidor ADK
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000"]
