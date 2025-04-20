#!/bin/sh
set -e

poetry run alembic upgrade head
poetry run python3 ./app/main.py
