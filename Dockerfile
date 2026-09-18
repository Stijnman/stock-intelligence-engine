FROM python:3.11-slim

WORKDIR /app

# Apply available Debian security updates in the image rather than shipping the
# package snapshot baked into the base tag.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import stock_intelligence_engine; print('OK')" || exit 1

ENTRYPOINT ["python", "stock_intelligence_engine.py"]
