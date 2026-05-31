FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import stock_intelligence_engine; print('OK')" || exit 1

ENTRYPOINT ["python", "stock_intelligence_engine.py"]