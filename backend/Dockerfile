FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend /app
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend /app

# uvicorn needs 0.0.0.0:8000 so caddy can reach it
CMD ["uvicorn", "numerology_app.main:app", "--host", "0.0.0.0", "--port", "8000"]