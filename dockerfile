FROM python:3.8
WORKDIR /app
RUN  pip install --upgrade pip
RUN  pip install poetry
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
ENTRYPOINT ["rasa"]
EXPOSE 5005
