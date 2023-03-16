FROM python:3.10.10-alpine3.17

COPY . /app

WORKDIR /app

RUN pip install poetry \
    && poetry install -q

CMD ["sh", "entrypoint.sh"]
