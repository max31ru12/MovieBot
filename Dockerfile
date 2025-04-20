FROM python:3.13-alpine

RUN apk update && apk add --no-cache build-base gcc musl-dev libffi-dev

RUN pip install poetry

ENV PATH="/root/.local/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY entrypoint.sh pyproject.toml poetry.lock alembic.ini ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

ENV PYTHONPATH=/bot

RUN chmod +x entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
