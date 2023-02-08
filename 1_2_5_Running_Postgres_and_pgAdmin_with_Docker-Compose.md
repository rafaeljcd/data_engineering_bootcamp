# Docker Compose

It is a utility to allow to put multiple configurations of a docker in a single file

- [Docker Compose](#docker-compose)
  - [Configuration](#configuration)
    - [Error when running](#error-when-running)
    - [Solution](#solution)
    - [Correct configuration](#correct-configuration)
  - [How it looks like](#how-it-looks-like)
  - [Pages](#pages)


---

## Configuration

```yaml
version: "1.0"
services:
  postgres_container:
    image: postgres:13
    environment:
      -POSTGRES_USER=root
      -POSTGRES_PASSWORD=root
      -POSTGRES_DB=ny_taxi
    volumes:
      - './ny_taxi_postgres_data:/var/lib/postgresql/data:rw'
    ports:
      - '5432:5432'
  pgadmin_container:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - '8080:80'
```

There is no longer need to add docker network here like the previous individual example, because they are automatically
became part of the same network

```shell
docker run -d \
  --name postgres_container \
  -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  postgres:13

sudo chmod a+rwx ny_taxi_postgres_data
```

```shell
docker run -it \
 -d \
 --name pgadmin_container \
 -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 -p 8080:80 \
 --network=pg-network \
 dpage/pgadmin4
```

To Start the docker compose we must use the following command

```shell
docker compose up
```

Also in order to stop a docker compose this is the command

```shell
docker compose down
```

---

### Error when running

Error when runnning the `docker compose up` encountered this error

![](https://i.imgur.com/HjTUSrc.png)

---

### Solution

Upon checking the `docker-compose.yaml` It turns out that the problem was on spacing

This is the wrong configuration

```yaml
    environment:
      -POSTGRES_USER=root
      -POSTGRES_PASSWORD=root
      -POSTGRES_DB=ny_taxi
```

And this is the correct configuration

```yaml
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
```

---

### Correct configuration

It is very important to note that spacing was very important in the docker compose

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
      - './ny_taxi_postgres_data:/var/lib/postgresql/data:rw'
    ports:
      - '5432:5432'
  pgadmin_container:
    container_name: pgadmin_container
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - '8080:80'
```

## How it looks like

This is what it looks like when the docker compose is running `docker_test` is the name of the project folder

![](https://i.imgur.com/tV7oOk4.png)

![](https://i.imgur.com/1JSqidD.png)

---

You can also run the docker compose in detach mode using this command

`docker compose up -d`

![](https://i.imgur.com/bV6vXB0.png)

---

This is what it looks like when stopping the docker compose

`docker compose down`

![](https://i.imgur.com/bploamG.png)

---

## Pages

| Previous Page                                                                         | table of contents      | Next page                               |
|---------------------------------------------------------------------------------------|------------------------|-----------------------------------------|
| [Putting the ingestion script into Docker](1_2_4_Dockerizing_the_Ingestion_Script.md) | [Readme.md](README.md) | [SQL Refresher](1_2_6_SQL_refresher.md) |