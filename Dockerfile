FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV AIOHTTP_NO_EXTENSIONS=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Устанавливаем все зависимости
RUN pip install --no-cache-dir \
    --no-binary aiohttp \
    --no-binary yarl \
    --no-binary multidict \
    --no-binary frozenlist \
    aiohttp==3.8.6 \
    yarl==1.9.4 \
    multidict==6.0.5 \
    frozenlist==1.4.1 \
    aiogram==2.25.1

COPY . .

RUN python --version

CMD ["python", "main.py"]
