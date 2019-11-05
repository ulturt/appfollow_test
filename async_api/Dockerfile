FROM python:3.7.3-alpine3.9

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /pysetup
COPY poetry.lock ./pyproject.toml /pysetup/
RUN pip install poetry
RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-interaction

WORKDIR /app
COPY . /app

CMD python -u app.py
