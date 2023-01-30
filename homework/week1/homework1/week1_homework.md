## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`
- `--idimage string`
- `--idfile string`

```shell
docker build --help
```

![](https://i.imgur.com/hgmrQAQ.png)


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

[] 1
[] 6
[x] 3
[] 7

```shell
docker build -t homework:v001 .
```

```shell
docker run --name homework_container -it homework:v001
```

![](https://i.imgur.com/vhATSMx.png)

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

```shell
docker compose up -d
```

## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

```postgresql
select
    count(1)
from green_trip_data
where cast(lpep_pickup_datetime as date) = '2019-01-15' and cast(lpep_dropoff_datetime as date) = '2019-01-15'
```

![](https://i.imgur.com/2VA5aA1.png)

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

```postgresql
select
    cast(lpep_dropoff_datetime as date),
    max(trip_distance)
from green_trip_data
group by cast(lpep_dropoff_datetime as date), trip_distance
order by trip_distance desc 
```

![](https://i.imgur.com/yEJI1Af.png)

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

```postgresql
select
    passenger_count,
    count(passenger_count)
from green_trip_data
where cast(lpep_pickup_datetime as date) = '2019-01-01'
group by passenger_count
```
![](https://i.imgur.com/15rJhuj.png)

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

```postgresql
select
    z."Zone",
    g.tip_amount
from green_trip_data g join zones z on z."LocationID" = g."DOLocationID"
where g."PULocationID" = 7
group by z."Zone", g.tip_amount
order by g.tip_amount desc 
```

![](https://i.imgur.com/xZXf2Yn.png)

## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET


## Solution

We will publish the solution here
