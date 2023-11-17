FROM python:3.11-slim

RUN apt update && apt install libpq-dev apt-utils python-dev-is-python3 gcc ffmpeg -y

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
