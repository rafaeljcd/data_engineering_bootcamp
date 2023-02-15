- [Introduction to Prefect Concepts](#introduction-to-prefect-concepts)
  - [Pre-requirements](#pre-requirements)
  - [Ingest Data Python Script](#ingest-data-python-script)
  - [Scenario explanation](#scenario-explanation)
  - [Transform the python script into a Prefect flow](#transform-the-python-script-into-a-prefect-flow)
  - [Resources](#resources)
  - [Page](#page)

# Introduction to Prefect Concepts

## Pre-requirements

- Postgres database running
    - Make that the docker is running(Docker desktop for windows).
    - We can use docker compose to run this one and then use `docker compose up -d`.

  ```yaml
  version: "1.0"
  services:
    postgres_database:
      image: postgres:13
      container_name: postgres_container
      environment:
        - POSTGRES_USER=root
        - POSTGRES_PASSWORD=root
        - POSTGRES_DB=ny_taxi
      volumes:
        - postgres_data:/var/lib/postgresql/data
      ports:
        - '5432:5432'
    pgadmin_container:
      container_name: pgadmin_container
      image: dpage/pgadmin4
      environment:
        - PGADMIN_DEFAULT_EMAIL=admin@admin.com
        - PGADMIN_DEFAULT_PASSWORD=root
      volumes:
        - pgadmin_data:/var/lib/pgadmin
      ports:
        - '8080:80'
  
  volumes:
    pgadmin_data:
    postgres_data:
  ```

- Conda installed
    - [We already have the instructions for install of conda in another documentation](1_4_1_Setting_up_the_Environment_on_Google_Cloud.md#set-up-the-virtual-machine-instance)
    - Change to not auto activate the conda environment
    - In order to manually activate the conda environment

      ```shell
      source ~/anaconda3/bin/activate
      ```
    - Create a conda environment.

      ```shell
      conda create -n zoom python=3.9
      ```
    - Activate the conda environment

      ```
      conda activate zoom
      ```

    - Install the `requirements.txt`. There is also a copy of it from
      this [course repository](https://github.com/discdiver/prefect-zoomcamp/blob/main/requirements.txt)

      `requirements.txt`

      ```
      pandas==1.5.2
      prefect==2.7.7
      prefect-sqlalchemy==0.2.2
      prefect-gcp[cloud_storage]==0.2.4
      protobuf==4.21.11
      pyarrow==10.0.1
      pandas-gbq==0.18.1
      psycopg2-binary==2.9.5
      sqlalchemy==1.4.46
      ```
      shell to install the `requirements.txt`

      ```
      pip install -r requirements.txt
      ```

    - Typed in `prefect version` to check if it is installed properly.

## Ingest Data Python Script

This is the Initial script for adding the csv to the database

```shell
python3 src/week2/ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

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
    while True:
        try:
            df = next(df_iter)
            if hasattr(df, "tpep_dropoff_datetime"):
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            if hasattr(df, "tpep_pickup_datetime"):
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            print("Inserted new chunk")
        except StopIteration:
            break

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

---

## Scenario explanation

The above is the program we have written before for the writing of the csv to the postgres database.

Now we are going to transform this file into be orchestrated with prefect.

Prefect is the modern open source data flow automation platform that allows to add observability and orchestration by
using python to write codes as workflows and let us run, build and monitor this pipeline at scale.

---

## Transform the python script into a Prefect flow

First we need to import flow from the prefect module.

```python
from prefect import flow
```

**Flows** are the most basic Prefect object. Flows are the only Prefect abstraction that can be interacted with, displayed, and run without needing to reference any other aspect of the Prefect engine. 

A **flow** is a container for workflow logic and allows users to interact with and reason about the state of their workflows. It is represented in Python as a single function.

A **Flow** is the most basic Prefect object that's a container of workflow logic that allows to interact and understand the state of the workflow 

```python
@flow(name="Ingest Flow", retries=3)
def main():
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = "yellow_taxi_data"
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    csv_file_path = download_csv(url=url)

    ingest_data(
        user=user,
        host=host,
        port=port,
        db=db,
        table_name=table_name,
        csv_file_path=csv_file_path
    )
```

Now we need to add the python decorator `flow` to the `main` function in order to create our main flow.

## Resources

- [Youtube - 2.2.2 - Introduction to Prefect Concepts](https://www.youtube.com/watch?v=cdtN6dhp708)
- [GitHub - Prefect zoomcamp](https://github.com/discdiver/prefect-zoomcamp)

## Page

| Previous                                                                                  | table of contents      |
|-------------------------------------------------------------------------------------------|------------------------|
| [Introduction to Workflow orchestration](2_2_1_Introduction_to_Workflow_orchestration.md) | [Readme.md](README.md) |
