FROM python:latest
LABEL authors="ts1x"

WORKDIR /app
COPY . .
EXPOSE 8999
RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python", "main.py"]