# syntax=docker/dockerfile:experimental
#----------------------------
FROM python:3.11 AS base-stage

ENV NEW_RELIC_MONITOR_MODE=false
ENV LOGGING_PATH /tmp/logs/
ENV FLASK_APP=radpair.health.api:app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

RUN apt-get update \
    && apt-get -y install \
        gcc \
        python3-dev \
        libpcre3 \
        libpcre3-dev \
        libpq-dev \
        tox \
        postgresql-server-dev-all \
    && pip install -U --no-cache-dir pip poetry \
    && pip install lockfile \
    && pip install Flask \
    && pip install python-dotenv \
    && pip install pytest \
    && pip install faker

# Set the working directory
WORKDIR /app

# Install dependencies
COPY . .
COPY pyproject.toml poetry.lock ./


# Create the directory for logs
RUN mkdir -p /tmp/logs/ && \
    touch /tmp/logs/{info.log, errors.log, debug.log, critical.log, warn.log}

# Expose the necessary port
EXPOSE 5000

CMD tail -f /dev/null

