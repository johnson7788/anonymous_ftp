FROM python:3.11-slim

WORKDIR /app

COPY http_server.py .

RUN mkdir -p /data && chmod 777 /data

EXPOSE 8088

CMD ["python", "http_server.py"]
