- [Concepts](#concepts)
  - [Introduction](#introduction)
- [Parts of Terraform](#parts-of-terraform)
  - [Terraform Version](#terraform-version)
  - [Main.tf](#maintf)
    - [Import Section](#import-section)
    - [Provider Section](#provider-section)
    - [Child Module Section](#child-module-section)
  - [Variables.tf](#variablestf)
  - [Definitions](#definitions)
- [Page](#page)

---

## Concepts

### Introduction

1. What is [Terraform](https://www.terraform.io)?
    * open-source tool by [HashiCorp](https://www.hashicorp.com), used for provisioning infrastructure resources
    * supports DevOps best practices for change management
    * Managing configuration files in source control to maintain an ideal provisioning state
      for testing and production environments
2. What is IaC?
    * Infrastructure-as-Code
    * build, change, and manage your infrastructure in a safe, consistent, and repeatable way
      by defining resource configurations that you can version, reuse, and share.
3. Some advantages
    * Infrastructure lifecycle management
    * Version control commits
    * Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
    * State-based approach to track resource changes throughout deployments

---

## Parts of Terraform

Terraform consists of 3 main files, 2 main file and 1 terraform version.

### Terraform Version

Just basically state what Terraform version you have installed, or alternatively you can use
TFEnv https://github.com/tfutils/tfenv, so we don't have to create a Terraform version file.

---

### Main.tf

This is where the configuration of resources of your Terraform files.

[Link to the file](main.tf)

#### Import Section

```terraform
terraform {
  required_version = ">= 1.0"
  backend "local" {}
  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}
```

**required_version**

This tells us the Terraform version or what it is compatbile to and compatible from.

**backend**

We also have the backend here, the default here is local, usually in the production it will be pointed to the cloud
environment itself of where to get the files

**required_providers**

This is where your Terraform registry picking publicly available providers from, and it allows to create resources based
from predefined resources, this is usually optional because we will declare it again later.

#### Provider Section

This is the **_implicit provider inheritance_**, this is very useful when there are multiple provider configurations, or
a child module may need to use a different provider settings.

```terraform
provider "google" {
  project = var.project
  region  = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}
```

Terraform relies on plugins called **_providers_** to interact with the cloud providers. It adds a pre-defined resource
type that Terraform can manage just like having the child module.

If you can notice here, the _**credentials**_ was commented out, it was done so that we don't have to upload the
credentials part

If you also notice, there is **var** here, this one comes from the `variables.tf` file

#### Child Module Section

**Resource**

This is a physical component such as storagebucket or database, and it contains argument to configure the resource.

This is an example of cloud storage bucket definition

```terraform
# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location = var.region

  # Optional, but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}
```

This is the example from the website

https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

![](https://i.imgur.com/0DQPeTT.png)

The resource name of the bucket must be unique to all the Google cloud storage

---

There is also an example with the BigQuery

```terraform
# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

```

### Variables.tf

It will contain the variable definitions for your module. When your module is used by others, the variables will be
configured as arguments in the module block. Since all Terraform values must be defined, any variables that are not
given a default value will become required arguments. Variables with default values can also be provided as module
arguments, overriding the default value.

Input variables let you customize aspects of Terraform modules without altering the module's own source code. This
functionality allows you to share modules across different Terraform configurations, making your module composable and
reusable.

```terraform
locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "europe-west6"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "trips_data_all"
}

```

The variables are passed during runtime, those variables with `default` will be passed through but variables without
default parameter will need a mandatory runtime arguments.

For the location, we can refer to this webpage https://cloud.google.com/about/locations in order to find out where is
the GCP server closest to us

It is a good practice to get all the resources inside one region.

### Definitions

* `terraform`: configure basic Terraform settings to provision your infrastructure
    * `required_version`: minimum Terraform version to apply to your configuration
    * `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
        * `local`: stores state file locally as `terraform.tfstate`
    * `required_providers`: specifies the providers required by the current module
* `provider`:
    * adds a set of resource types and/or data sources that Terraform can manage
    * The Terraform Registry is the main directory of publicly available providers from most major infrastructure
      platforms.
* `resource`
    * blocks to define components of your infrastructure
    * Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
* `variable` & `locals`
    * runtime arguments and constants

---

## Page

| Previous                                                                                                                      | Return to table of contents |
|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| [Introduction to Terraform Concepts & GCP Pre-Requisites](1_3_1_Introduction_to_Terraform_Concepts_and_GCP_Pre-Requisites.md) | [Readme.md](README.md)      |