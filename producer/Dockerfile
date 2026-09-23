FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY producer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY producer ./producer
COPY schemas ./schemas

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "producer.event_generator"]
