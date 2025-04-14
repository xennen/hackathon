FROM python:3.11-slim

# Установка системных зависимостей (без cython)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка cython через pip (совместимая версия)
RUN pip install --no-cache-dir cython

# Копируем проект и устанавливаем зависимости
WORKDIR /hackathon
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/result.py"]
