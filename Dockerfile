FROM python:3.11-slim

WORKDIR /app

# Apply available Debian security updates in the image rather than shipping the
# package snapshot baked into the base tag.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.1" "setuptools>=78.1.1" wheel \
    && python -m pip install --no-cache-dir -r requirements.txt \
    # Remove stale vendored distribution metadata from the base image. Trivy
    # otherwise reports the old setuptools 70.3.0 metadata even though the
    # active setuptools installation is upgraded above.
    && rm -rf /usr/local/lib/python3.11/site-packages/setuptools/_vendor/wheel-*.dist-info

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import stock_intelligence_engine; print('OK')" || exit 1

ENTRYPOINT ["python", "stock_intelligence_engine.py"]
