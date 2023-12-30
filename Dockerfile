FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip install -r requirements.txt

ENTRYPOINT /usr/local/bin/python3