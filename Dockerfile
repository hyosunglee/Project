FROM python:3.11-slim

WORKDIR /app

COPY server_render.py .
COPY requirements_render.txt .

RUN pip install --no-cache-dir fastapi uvicorn httpx

EXPOSE 8000

CMD ["uvicorn", "server_render:app", "--host", "0.0.0.0", "--port", "8000"]
