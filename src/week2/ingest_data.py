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