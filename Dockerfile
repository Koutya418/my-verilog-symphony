FROM python:3.13

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
  iverilog && \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

ENV LANG=ja_JP.UTF-8
ENV TZ=Asia/Tokyo