FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN pip install poetry --no-cache-dir

COPY pyproject.toml poetry.lock entrypoint.sh ./

RUN poetry config virtualenvs.create false && poetry install

COPY . /app

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
