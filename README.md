# Docker

----

## Starting with docker

To build the docker image

```shell
docker build -t name:tag .
```

`-t or --tag` the syntax for the following to be the name and tag

`first:tag`

The <u>_**name**_</u> signifies the name of the docker image

The <u>**_tag_**</u> is the tag image it can be used to give version names

![image](https://i.imgur.com/i0RNJ5j.png)

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./src ./src

ENTRYPOINT ["bash"]
```

----

To create the container

```shell
docker run --name image_test_container -it name:tag
```

With this, after running this with the dockerfile, it will run the container with the name of `image_test_container`
from the image `name:tag`

![](https://i.imgur.com/XVc68zC.png)

---

typing `exit` will exit the docker

---

|    command     |                  description                  |
|:--------------:|:---------------------------------------------:|
|  `docker ps`   |       show all of the active container        |
| `docker ps -a` | show all of the active and inactive container |

---

## Running the python program

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]
```

----

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]
```

---

## installing pip

source ../docker_venv/bin/activate

```shell
source ../docker_venv/bin/activate
pip freeze > requirements.txt
```

-----

## Postgresql

### postgresql at docker

```shell
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \ 
  -e POSTGRES_DB="ny_taxi" \
  postgres:13
```

`-e` or `--env` for setting the environmental variables

This is the normal setup for basic postgres at docker

----

#### Postgres with the configured env

```shell
docker run -d \
  --name postgres_container \
  -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

`-v` or `--volume` for mounting a volume

`-p` or `--publish` mapping the port from the host machine to the container

`/var/lib/postgresql/data` this is where the postgresql will save the local data for postgres

`-v /home/arthur/docker_test/ny_taxi_postgres_data:/var/lib/postgresql/data`

Need to map the data from the docker to the host machine

`-d` or `--detach` to be able to run in detach mode

Also added some name to the container, so it won't be random name 

![](https://i.imgur.com/4rmyjKg.png)

![](https://i.imgur.com/uS1m3gZ.png)

The finished setup for the postgres