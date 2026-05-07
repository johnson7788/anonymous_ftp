FROM python:3.11-slim

RUN pip install --no-cache-dir pyftpdlib

WORKDIR /app

COPY ftp_server.py .

EXPOSE 21
EXPOSE 30000-30009

CMD ["python", "ftp_server.py"]
