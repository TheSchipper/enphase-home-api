FROM python:3.9-slim

# Copy workspace
WORKDIR /enphase-home-api-client
COPY . /enphase-home-api-client

# Install Curl
RUN apt-get update && apt-get install curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry install

ENTRYPOINT /bin/bash