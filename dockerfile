# 1. start from a lightweight Python base image
FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
