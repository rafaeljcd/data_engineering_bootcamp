In this session, we need to convert the jupyter notebook into a python script

## Initial setup

In order to ensure that we have successfully copied the csv to the database. We are going to delete all of the rows in
the database

```postgresql
delete from yellow_taxi_data
```

---

## Build and run the python script

Run the python script with the args

The script is also design that if there are no args inserted then it will not continue.

[Python script](src/week1/ingest_data.py)

```shell
python3 src/week1/ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

---

## Add the python script to the docker

Update the dockerfile with the name of the script

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "src/week1/ingest_data.py"]
```

Now build a new docker image

```shell
docker build -t name:v001 .
```

Now run the new docker container from the docker image

```shell
docker run -d \
    -it \
    --network=pg-network \
      name:v001 --user=root \
      --password=root \
      --host=postgres_container \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_data \
      --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

Also be sure to add the docker network `pg-network` and set the `host` into the `postgres_container`

---

Notice in the docker run above, that the argument are split into two parts

```
docker run -d \
    -it \
    --network=pg-network \
```

Any arguments before the docker image are considered as docker arguments

```
    name:v001 --user=root \
      --password=root \
      --host=postgres_container \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_data \
      --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

While arguments after the docker image are now considered arguments for the docker image.

And this arguments will be pass into the entrypoint.

Similar to how we did above at the python script

---

From the course we can also do it like this to be able to easily change the url

```shell
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -d \
    -it \
    --network=pg-network \
      name:v001 --user=root \
      --password=root \
      --host=postgres_container \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_data \
      --url=${URL}
```

---

| Return to table of contents | Next page                                                                                                     |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|
| [Readme.md](README.md)      | [Running Postgres and pgAdmin with Docker-Compose](1_2_5_Running_Postgres_and_pgAdmin_with_Docker-Compose.md) |