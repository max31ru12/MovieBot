FROM python:3.10-alpine

RUN apk update && apk add --no-cache build-base gcc musl-dev libffi-dev

WORKDIR /bot

COPY requirements.txt .
COPY alembic.ini .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=/bot

ENTRYPOINT ["python3", "/bot/app/main.py"]
