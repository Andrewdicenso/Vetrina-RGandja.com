FROM python:3.10-slim

# Crea un utente non-privilegiato per sicurezza (Best Practice Production)
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Installa le dipendenze di sistema necessarie (se richieste)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=appuser:appuser requirements.txt .

USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=appuser:appuser . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]