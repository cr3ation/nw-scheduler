FROM python:3.12-alpine3.21
LABEL maintainer="henrikengstrom.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app ./app

WORKDIR /app
EXPOSE 8000

# Install gcc
RUN apk add --update build-base

# Install TimeZone support
RUN apk add --no-cache tzdata

# Install venv, requirements and user 
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache git && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    apk add --no-cache gcc && \
    apk add --no-cache musl-dev && \
    apk add --no-cache postgresql-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

# USER app

