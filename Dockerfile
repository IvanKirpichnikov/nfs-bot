FROM python:3.11.8-alpine3.19

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && apk add file && apk add git && pip3 install uv
COPY pyproject.toml /app/pyproject.toml
COPY ./src /app/src

WORKDIR /app

RUN python3 -m uv pip install -e .
RUN apk del git

CMD nft-bot-cli --run telegram_bot --config nft_bot.toml
