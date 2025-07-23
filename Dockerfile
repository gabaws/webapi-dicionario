FROM python:3.11.8-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN useradd -m appuser && mkdir -p /app/logs && chown appuser:appuser /app/logs

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]