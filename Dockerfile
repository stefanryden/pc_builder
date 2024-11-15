# Använd en officiell Python-bild
FROM python:3.9-slim

# Ställ in arbetskatalogen
WORKDIR /app

# Kopiera requirements-filen till containern
COPY requirements.txt requirements.txt

# Installera systemberoenden och Python-paket
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt

# Kopiera resten av applikationen till containern
COPY . .

# Exponera porten där Streamlit kommer att köras
EXPOSE 8501

# Startkommandot för att köra Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
