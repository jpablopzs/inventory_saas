# Usar la imagen base oficial de Python
FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

COPY start.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
