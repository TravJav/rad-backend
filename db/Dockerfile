FROM .ca-central-1.amazonaws.com/db-migrations.base:v2 AS base-stage

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
USER liquibase

COPY --chown=liquibase ./ ./

ENV CHANGELOG_FILE=changelog.yaml

## these stages are required for test execution
FROM base-stage AS development-stage
FROM base-stage AS production-stage