FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]