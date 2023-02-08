- [Data Lake](#data-lake)
  - [Introduction](#introduction)
  - [Data Lake vs Data Warehouse](#data-lake-vs-data-warehouse)
  - [How did Data Lake started](#how-did-data-lake-started)
  - [ETL vs ELT](#etl-vs-elt)
  - [Challenges on Data Lake](#challenges-on-data-lake)
  - [Cloud Provider for data lake](#cloud-provider-for-data-lake)
  - [Resources](#resources)
  - [Page](#page)

---

# Data Lake

## Introduction

![](https://i.imgur.com/cd7vjxo.png)

Data lake is a central repository that holds big data from multiple sources generally the data can be structured,
semi-structured, or unstructured.

The idea is to ingest data as quickly as possible and make it available or accessible to other team members like data
scientists, data analysts data engineers

Data lake is being used extensively for machine learning as well as analytical solutions.

Generally when you are storing data into your data lake, you would associate some sort of metadata for faster access

A data lake solution generally has to be secure and can scale the idea also consists that the hardware should be
inexpensive the reason being that you want to store as much of data as quickly as possible.

---

## Data Lake vs Data Warehouse

![](https://i.imgur.com/Vmjpf4n.png)

**Data lake**

It is an unstructured data, the target users are data scientists or data analysts. It stores huge amount of data
sometimes in the size of petabytes or also data coming in every day in terabytes

The use cases which are covered by data lake are basically:

- stream processing
- machine learning and
- real-time analytics

**Data Warehouse**

The data is generally structured, the users are business analysts the data size is generally small and the use case
consists of batch processing or bi reporting.

Typically, contain quantitative metrics, the attributes describing them, and data derived from transactional systems. Web
server logs, social network activity, sensor data, images, and text are all examples of non-traditional data sources
which are ignored.

---

## How did Data Lake started

Companies realize the value of data which then started developing projects and products which are totally revolving
around data, and they have made huge amount of revenues based upon that.

The idea also consists that they want to store and access the data quickly. They don't want to wait to developer teams
to develop a structure of data, to develop relationships and then the data being useful.

The idea is to store the data as quickly as possible and make it useful for other team members or other parts of the
company.

Generally it was also realized that the data is not really useful when the project starts but later in the project life
cycle.

With this, they have also seen an increase in data scientists and R&D on products.

This all came down to storing this data as cheaply as possible and these are the one of the few reasons why data
lake came into the picture

---

## ETL vs ELT

ETL(Export, Transform and Load) vs ELT(Export, Load and Transform)

ETL is used for small amount of data

ELT is used for large amounts of data

This is a very typical example of data warehouse versus data lake. ETL is a data warehouse solution whereas ELT is a
data lake solution

The idea of an ETL is schema on write that defines a well-defined schema, define the relationships and then write the data

ELT is based upon schema on read where you write the data first and determine the schema on the read

---

## Challenges on Data Lake

It's well known that data lake starts with a good intention but soon converts into a data swamp which makes it very hard to be useful by data scientists or analysts

A **data swamp** is the degenerative state of a data lake. Tables within the lake either return inaccurate data or files become corrupted and queries stop running altogether.

Some of the reasons that a data lake converts into data swamp is that there is generally no versioning.

There is incompatible schemas for the same data without versioning like for example: today you are writing trip data using [AVRO](https://avro.apache.org/) and tomorrow in the same path in the same folder you are writing data as [parquet](https://parquet.apache.org/). This will be this will make it very hard for the consumers to consume this data and that's why the whole data set becomes useless.

Generally if you do not associate any metadata to your data it becomes really hard for a person or a data scientist to use your data to figure out what's the usefulness for the data for the project.

Generally data lake also becomes useless when there is not a possibility to join different data sets it is because there is no foreign key available or there is no other possibility to join different data sets

---

## Cloud Provider for data lake

- GCP - Cloud Storage
- AWS - S3
- Azure - Azure Blob

---

## Resources

- [Youtube - 2.1.1 - Data Lake](https://www.youtube.com/watch?v=W3Zm6rjOq70)
- [Blog - Data Lake](https://lakefs.io/blog/data-lakes/)
- [Blog - Data Lake vs Data Warehouse](https://vmblog.com/archive/2022/05/30/7-key-differences-between-data-lake-and-data-warehouse-do-you-need-both.aspx)

---

## Page

| Previous                                                                                          | table of contents      |
|---------------------------------------------------------------------------------------------------|------------------------|
| [Setting up the Environment on Google Cloud](1_4_1_Setting_up_the_Environment_on_Google_Cloud.md) | [Readme.md](README.md) |