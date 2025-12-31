FROM python:3.11-slim

LABEL maintainer="Md. Tanvir Hossain <tanvir.eece.mist@gmail.com>"
LABEL description="ChainSense-AI ML Service"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN groupadd -r chainsense && useradd -r -g chainsense chainsense

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=chainsense:chainsense . .

# Create models directory
RUN mkdir -p /app/models && chown chainsense:chainsense /app/models

USER chainsense

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
