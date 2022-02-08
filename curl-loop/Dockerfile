FROM python:3.8-alpine3.15
LABEL maintainer="henrikengstrom.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app ./app
WORKDIR /app

# Install gcc
RUN apk add --update build-base && \
    apk add --no-cache curl

# Install venv, requirements and user 
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

USER app