FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TOKEN_FILE=/data/token.txt

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY config ./config
COPY frontend ./frontend

RUN mkdir -p /data && useradd -r -u 10001 remote && chown remote /data
USER remote

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"FLASK_PORT\",\"5000\")}/health', timeout=2)"

# 1 seul worker : la connexion WebSocket vers la TV est partagée en mémoire.
CMD ["sh", "-c", "gunicorn --workers 1 --threads 8 --bind 0.0.0.0:${FLASK_PORT:-5000} --access-logfile - backend.app:app"]
