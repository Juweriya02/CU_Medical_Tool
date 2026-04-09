# Dockerfile
# Builds a container for the CU Pharmaceutical Data Tool

FROM python:3.11-slim

LABEL maintainer="Centrala University Medical Tool"
LABEL description="Pharmaceutical Data Management Tool"
LABEL version="1.0"

WORKDIR /app

COPY csv_validator.py .
COPY ftp_client.py .
COPY logger.py .
COPY cli.py .
COPY gui.py .
COPY main.py .
COPY generate_test_data.py .
COPY demo_api.py .
COPY test_csv_validator.py .
COPY test_singleton.py .

RUN mkdir -p /app/logs
RUN mkdir -p /app/test_data
RUN mkdir -p /app/archived_data

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python3", "main.py"]