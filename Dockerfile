FROM python:3.10-slim

# Copy workspace
WORKDIR /enphase-home-api-client
COPY . /enphase-home-api-client

RUN pip install -r requirements.txt

ENTRYPOINT /bin/bash