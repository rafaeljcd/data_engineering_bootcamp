import requests
import pandas as pd
import gzip
import shutil
from os.path import splitext
from urllib.parse import urlparse
from sqlalchemy import create_engine
from pathlib import Path
from prefect import flow, task


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

@task(log_prints=True, retries=3)
def ingest_data(
        user: str,
        host: str,
        port: str,
        db: str,
        table_name: str,
        csv_file_path: Path
):
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
        except StopIteration:
            break

    print("done")


@flow(name="Ingest Flow")
def main():
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = "yellow_taxi_data"
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz "

    # Download CSV
    csv_file_path = download_csv(url=url)

    ingest_data(
        user=user,
        host=host,
        port=port,
        db=db,
        table_name=table_name,
        csv_file_path=csv_file_path
    )


if __name__ == '__main__':
    main()
