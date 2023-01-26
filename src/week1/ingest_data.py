import argparse
import requests
import pandas as pd
import gzip
import shutil
from os.path import splitext
from urllib.parse import urlparse
from sqlalchemy import create_engine
from pathlib import Path

engine = create_engine(
    'postgresql://root:root@localhost:5432/ny_taxi'
)


def download_csv():
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

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

    with open(Path(__file__).parent / extensions[0], "wb") as csv_file:
        with gzip.open(file_path, "rb") as gz_file:
            shutil.copyfileobj(gz_file, csv_file)


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Ingest CSV to postgres")
#
#     parser.add_argument("user", help="username for postgres")
#     parser.add_argument("password", help="password for postgres")
#     parser.add_argument("host", help="host for postgres")
#     parser.add_argument("port", help="port for postgres", type=int)
#     parser.add_argument("db", help="database name for postgres")
#     parser.add_argument("table_name", help="name of the table where we will write the results")
#     parser.add_argument("url", help="url of the csv file")
#
#     args = parser.parse_args()
