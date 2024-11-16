FROM python:3.12-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
 && apt-get install --no-install-recommends -y curl

RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev


FROM python-base

ENV PYTHONPATH=/app

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/

WORKDIR /app

CMD [ \
    "uvicorn", \
    "--host", "0.0.0.0", \
    "--port", "80", \
    "--workers", "1", \
    "--log-level", "critical", \
    "app:app" \
]
