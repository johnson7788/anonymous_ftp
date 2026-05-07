FROM python:3.11-slim

WORKDIR /app

COPY http_server.py .

EXPOSE 8080

CMD ["python", "http_server.py"]
