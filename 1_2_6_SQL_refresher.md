- [Setup](#setup)
  - [Pgadmin volume persist](#pgadmin-volume-persist)
  - [Inserting of the data to the database](#inserting-of-the-data-to-the-database)
- [Lesson](#lesson)
  - [Initial lesson](#initial-lesson)
  - [Concat](#concat)
  - [Inner join](#inner-join)
  - [Left Join](#left-join)
  - [Right Join](#right-join)
  - [Outer join](#outer-join)
  - [Group by and order by](#group-by-and-order-by)
    - [Casting the date by date\_trunc](#casting-the-date-by-date_trunc)
    - [Casting the date by cast](#casting-the-date-by-cast)
    - [Group by example](#group-by-example)
    - [Group by with order by](#group-by-with-order-by)
    - [With max](#with-max)
    - [Group by their position](#group-by-their-position)
    - [Chain order by](#chain-order-by)
- [Resources](#resources)
- [Pages](#pages)


---

## Setup

This is the csv data that is going to be used for this session

```shell
cd files/week1
wget https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/taxi_rides_ny/data/taxi_zone_lookup.csv
```

You won't be able to download it this way, since it will download the html page of the csv

The solution for this is to add `?raw=true` at the end of the link

[Solution Source](https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas)

And then you'll be redirected to the `raw.githubusercontent.com` where you can then directly insert it to your data

```shell
cd files/week1
wget https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/week_4_analytics_engineering/taxi_rides_ny/data/taxi_zone_lookup.csv
```

---

### Pgadmin volume persist

From the course so far, we didn't have any way to persist the settings of the `pgadmin` container.

In order to combat this, we make use of the `docker volumes` in order to persist the data

`docker-compose.yaml`

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
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    ports:
      - '8080:80'

volumes:
  pgadmin_data:
```

[Solution Source](https://stackoverflow.com/a/57176413/14859274)

---

### Inserting of the data to the database

Have used a jupyter notebook to insert to create the database and insert the data

[Jupyter for creating db and inserting data](files/week1/sql_refresher_upload.ipynb)

---

## Lesson

### Initial lesson

This is a normal sql query

```postgresql
select *
from yellow_taxi_data
limit 100
```

You can cast the table as following

```postgresql
select *
from yellow_taxi_data t
limit 100
```

And now you can use the `yellow_taxi_data` by calling the cast `t` followed by the `.<column name>` like for example
`t."total_amount"`

---

Now you can also call multiple tables with the `from` statement

```postgresql
select *
from yellow_taxi_data t,
     zones zpu,
     zones zdo
where t."PULocationID" = zpu."locationid"
  and t."DOLocationID" = zdo."locationid"
limit 100
```

where `zpu` is zones pick up and
`zdo` is zones drop off

Now in the example above, it will fetch all the data that matches the `where` statement

---

### Concat

This is an example of wrong type of concating text

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       zpu."borough" + '/' + zpu."zone" AS "pick_up_location",
       zdo."borough" + '/' + zdo."zone" AS "drop_off_location"
from yellow_taxi_data t,
     zones zpu,
     zones zdo
where t."PULocationID" = zpu."locationid"
  and t."DOLocationID" = zdo."locationid"
limit 100
```

![](https://i.imgur.com/pgzvnuW.png)

Postgres got a function to concat string properly

[Postgres sql](https://www.postgresql.org/docs/9.1/functions-string.html)

 ```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       concat(zpu."borough", '/', zpu."zone") AS "pick_up_location",
       concat(zdo."borough", '/', zdo."zone") AS "drop_off_location"
from yellow_taxi_data t,
     zones zpu,
     zones zdo
where t."PULocationID" = zpu."locationid"
  and t."DOLocationID" = zdo."locationid"
limit 100
```

![](https://i.imgur.com/gL3qdNB.png)

---

### Inner join

We can also write in a different way with `inner join`

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       concat(zpu."borough", '/', zpu."zone") AS "pick_up_location",
       concat(zdo."borough", '/', zdo."zone") AS "drop_off_location"
from yellow_taxi_data t
         JOIN zones zpu on t."PULocationID" = zpu."locationid"
         JOIN zones zdo on t."DOLocationID" = zdo."locationid"
limit 100
```

`Table 1` JOIN `table 2` `<as cast as>`

If you want to add a condition statement it will become

`Table 1` JOIN `table 2` `<as cast as>` on `CONDITION`

![](https://i.imgur.com/m7pgxch.png)

![](https://i.imgur.com/A5Ew0oq.png)

---

Now we will simulate when some data are not present from one table to another table

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       "PULocationID",
       "DOLocationID"
from yellow_taxi_data t
where "PULocationID" NOT IN (SELECT "locationid" from zones)
limit 100
```

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       "PULocationID",
       "DOLocationID"
from yellow_taxi_data t
where "DOLocationID" NOT IN (SELECT "locationid" from zones)
limit 100
```

![](https://i.imgur.com/9cSXDru.png)

Since our data is pretty good, we need to simulate some data missing by deleting it.

```postgresql
delete
from zones
where "locationid" = 142
```

![](https://i.imgur.com/HZiCijq.png)

And now we successfully delete some data

We need to re-run the query from above again, and see the results.

![](https://i.imgur.com/8xnNQi2.png)

And now, it will show the `PULocationID` that doesn't exist in the `zones` table

---

### Left Join

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       "PULocationID",
       "DOLocationID",
       concat(zpu."borough", '/', zpu."zone") AS "pick_up_location",
       concat(zdo."borough", '/', zdo."zone") AS "drop_off_location"
from yellow_taxi_data t
         LEFT JOIN zones zpu on t."PULocationID" = zpu."locationid"
         LEFT JOIN zones zdo on t."DOLocationID" = zdo."locationid"
```

![](https://i.imgur.com/NTlp49x.png)

This will return all records from `table 1` and the records that is also present in `table 2`

---

### Right Join

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       "PULocationID",
       "DOLocationID",
       concat(zpu."borough", '/', zpu."zone") AS "pick_up_location",
       concat(zdo."borough", '/', zdo."zone") AS "drop_off_location"
from yellow_taxi_data t
         RIGHT JOIN zones zpu on t."PULocationID" = zpu."locationid"
         RIGHT JOIN zones zdo on t."DOLocationID" = zdo."locationid"
```

![](https://i.imgur.com/ZXoECel.png)

This will return all records from `table 2` and the records that is also present in `table 1`

---

### Outer join

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       total_amount,
       "PULocationID",
       "DOLocationID",
       concat(zpu."borough", '/', zpu."zone") AS "pick_up_location",
       concat(zdo."borough", '/', zdo."zone") AS "drop_off_location"
from yellow_taxi_data t
         FULL OUTER JOIN zones zpu on t."PULocationID" = zpu."locationid"
         FULL OUTER JOIN zones zdo on t."DOLocationID" = zdo."locationid"
```

![](https://i.imgur.com/ioXBf3c.png)

This is like the combination of the `right inner join` and `left inner join`

---

### Group by and order by

#### Casting the date by date_trunc

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       date_trunc('DAY', tpep_dropoff_datetime),
       total_amount
from yellow_taxi_data
```

![](https://i.imgur.com/eX17zaO.png)

---

#### Casting the date by cast

```postgresql
select tpep_pickup_datetime,
       tpep_dropoff_datetime,
       cast(tpep_dropoff_datetime as date),
       total_amount
from yellow_taxi_data
```

![](https://i.imgur.com/vDgcVf9.png)

---

#### Group by example

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       count(1)
from yellow_taxi_data
group by cast(tpep_dropoff_datetime as date)
```

![](https://i.imgur.com/2t7PeGH.png)

---

#### Group by with order by

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       count(1)
from yellow_taxi_data
group by cast(tpep_dropoff_datetime as date)
order by "Day"
```

![](https://i.imgur.com/tIKMTSH.png)

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       count(1) as "count"
from yellow_taxi_data
group by cast(tpep_dropoff_datetime as date)
order by "count" desc
```

![](https://i.imgur.com/7s3dvUc.png)

#### With max

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       count(1) as "count",
       max(total_amount),
       max(passenger_count)
from yellow_taxi_data
group by cast(tpep_dropoff_datetime as date)
order by "count" desc
```

![](https://i.imgur.com/mJgv4W6.png)

#### Group by their position

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       "DOLocationID",
       count(1) as "count",
       max(total_amount),
       max(passenger_count)
from yellow_taxi_data
group by 1, 2
order by "count" desc
```

As you can see here `cast(tpep_dropoff_datetime as date) as "Day"` is on the position `1` and
`"DOLocationID"` is on the position `2`

This is roughly the same as the 

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       "DOLocationID",
       count(1) as "count",
       max(total_amount),
       max(passenger_count)
from yellow_taxi_data
group by "Day", "DOLocationID"
order by "count" desc
```

![](https://i.imgur.com/zC3Y228.png)

#### Chain order by

```postgresql
select cast(tpep_dropoff_datetime as date) as "Day",
       "DOLocationID",
       count(1) as "count",
       max(total_amount),
       max(passenger_count)
from yellow_taxi_data
group by 1, 2
order by 
    "Day" asc, 
    2 asc
```

![](https://i.imgur.com/I2sSJzJ.png)

---

## Resources

- [Youtube - 1 .2.6 - SQL Refresher](https://www.youtube.com/watch?v=QEcps_iskgg)
- [Images for this session](./files/week1/1.2.6_files)

---

## Pages

| Previous Page                                                                                                 | table of contents      | Next page                                                                                                                     |
|---------------------------------------------------------------------------------------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| [Running Postgres and pgAdmin with Docker-Compose](1_2_5_Running_Postgres_and_pgAdmin_with_Docker-Compose.md) | [Readme.md](README.md) | [Introduction to Terraform Concepts & GCP Pre-Requisites](1_3_1_Introduction_to_Terraform_Concepts_and_GCP_Pre-Requisites.md) |