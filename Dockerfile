FROM python:3.12-slim

# Install system dependencies for security tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    curl \
    netcat-openbsd \
    procps \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv
RUN uv sync

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
