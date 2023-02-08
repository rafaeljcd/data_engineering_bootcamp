- [Initial setup](#initial-setup)
- [Build and run the python script](#build-and-run-the-python-script)
  - [Code](#code)
  - [Terminal](#terminal)
- [Add the python script to the docker](#add-the-python-script-to-the-docker)
- [Pages](#pages)


---

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

### Code
```python

import argparse
import requests
import pandas as pd
import gzip
import shutil
from os.path import splitext
from urllib.parse import urlparse
from sqlalchemy import create_engine
from pathlib import Path
from tqdm import tqdm


def download_csv(
        url: str
) -> Path:
    # Getting the file name with extensions
    path = urlparse(url=url).path
    file_name = path.split("/")[-1]

    file_path = Path(__file__).parent / file_name

    # If file is not yet downloaded, proceed to download the file
    if not file_path.exists():
        print(f"downloading {file_name}...")
        r = requests.get(url=url)

        print("download complete")

        print(f"{file_path}")
        print(f"saving file")
        with open(file_path, 'wb') as file:
            file.write(r.content)

    # Since we need to extract the csv file from the gz file, we must know the base name with extension
    extensions = splitext(file_name)

    # https://docs.python.org/3.11/library/gzip.html#examples-of-usage
    # we must now open the base name of gz file in the write bytes mode and,
    # open the gz file in the read bytes mode.
    # Use the shutil to copy the contents from the gz file to the base file
    # Note: that if you wanted to compress the file to gz file just do everything in reverse.

    csv_file_path = Path(__file__).parent / extensions[0]
    print(f"extracting {extensions[0]}...")
    with open(csv_file_path, "wb") as csv_file:
        with gzip.open(file_path, "rb") as gz_file:
            shutil.copyfileobj(gz_file, csv_file)

    return csv_file_path


def main(
        params: argparse.Namespace
):
    user = params.user if hasattr(params, "user") else None
    password = params.password if hasattr(params, "password") else None
    host = params.host if hasattr(params, "host") else None
    port = params.port if hasattr(params, "port") else None
    db = params.db if hasattr(params, "db") else None
    table_name = params.table_name if hasattr(params, "table_name") else None
    url = params.url if hasattr(params, "url") else None

    if any(item is None for item in [user, password, host, port, db, table_name, url]):
        print("Empty arguments")
        return

    # Download CSV
    csv_file_path = download_csv(url=url)

    print("creating engine")
    # Initialized the engine
    engine = create_engine(
        f"postgresql://{user}:{user}@{host}:{port}/{db}"
    )

    print("reading csv")
    df_iter = pd.read_csv(csv_file_path, iterator=True, chunksize=100_000, low_memory=False)

    print("now saving to database")
    with tqdm(iterable=df_iter) as t:
        df: pd.DataFrame
        for df in t:
            if hasattr(df, "tpep_dropoff_datetime"):
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            if hasattr(df, "tpep_pickup_datetime"):
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t.update()

    print("done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV to postgres")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres", type=int)
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--table_name", help="name of the table where we will write the results")
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)

```

### Terminal

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

## Pages

| Previous Page                                                               | table of contents      | Next page                                                                                                     |
|-----------------------------------------------------------------------------|------------------------|---------------------------------------------------------------------------------------------------------------|
| [Connecting pgAdmin and Postgres](1_2_3_Connecting_pgAdmin_and_Postgres.md) | [Readme.md](README.md) | [Running Postgres and pgAdmin with Docker-Compose](1_2_5_Running_Postgres_and_pgAdmin_with_Docker-Compose.md) |