- [Introduction to Prefect Concepts](#introduction-to-prefect-concepts)
  - [Pre-requirements](#pre-requirements)
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
  
  - Install the `requirements.txt`. There is also a copy of it from this [course repository](https://github.com/discdiver/prefect-zoomcamp/blob/main/requirements.txt)
    
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



## Resources

- [Youtube - 2.2.2 - Introduction to Prefect Concepts](https://www.youtube.com/watch?v=cdtN6dhp708)
- [GitHub - Prefect zoomcamp](https://github.com/discdiver/prefect-zoomcamp)

## Page

| Previous                                                                                  | table of contents      |
|-------------------------------------------------------------------------------------------|------------------------|
| [Introduction to Workflow orchestration](2_2_1_Introduction_to_Workflow_orchestration.md) | [Readme.md](README.md) |
