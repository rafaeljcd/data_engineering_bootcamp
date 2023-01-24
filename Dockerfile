FROM python:3.11.0rc1

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]