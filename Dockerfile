FROM python:3.11.0rc1

WORKDIR /code

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]