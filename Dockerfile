FROM python:3.12-slim

# OCR ve görüntü kütüphaneleri
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 ghostscript && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
