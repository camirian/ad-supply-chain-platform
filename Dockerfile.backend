FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Seed the database during build so that ephemeral Cloud Run instances 
# boot with the required snapshot data
RUN python backend/db_init.py

# Cloud Run defines the PORT environment variable natively
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
