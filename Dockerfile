FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/scripts /app/data

COPY scripts/ /app/scripts/

# Set environment variables for SQLite database location
#ENV DB_FILE=/app/data/exchange_rates.db

# Make sure SQLite persistent
VOLUME /app/data

CMD ["python", "/app/scripts/main.py"]