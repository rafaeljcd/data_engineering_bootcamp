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
- [Terraform commands](#terraform-commands)
  - [Summary](#summary)
  - [Terraform Init](#terraform-init)
  - [Terraform Plan](#terraform-plan)
  - [Terraform Apply](#terraform-apply)
    - [Check the project in GCP for the changes](#check-the-project-in-gcp-for-the-changes)
  - [Terraform Destroy](#terraform-destroy)
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

[Link to the file](files/week1/terraform/main.tf)

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

## Terraform commands

### Summary

1. `terraform init`:
    * Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a
      version control
2. `terraform plan`:
    * Matches/previews local changes against a remote state, and proposes an Execution Plan.
    * This detects when there is new resource or updated resource and tells the user about it.
3. `terraform apply`:
    * Asks for approval to the proposed plan, and applies changes to cloud
4. `terraform destroy`
    * Removes your stack from the Cloud. This is often neglected but equally important function.

### Terraform Init

![](https://i.imgur.com/E4R58UE.png)

The function is now importing the plugins from the official repository of the HashiCorp.

Invoking the `ls -la` command to check for all the file and directories including the hidden files will show this.

![](https://i.imgur.com/Xe3O0Ma.png)

You can see it created new files and directories here.

`.terraform`

It packages all of your code into a more compressed version in your `.terraform` directory and it is use to store the
state of the terraform and the providers associated with it.

![](https://i.imgur.com/hIs46Xl.png)

### Terraform Plan

![](https://i.imgur.com/7wCOI1z.png)

```terraform
variable "project" {
  description = "Your GCP Project ID"
}
```

This is the only argument that is mandated here because for this course each students are using different project IDs,
so in order to accommodate for that it was removed from the `variables.tf` file

This is also common problem in the companies when there are multiple people working on the same project in the
development environment which causes an overlap in the same resources so for this reason it is advisable to use your own
project.

![](https://i.imgur.com/4eycvmF.png)

![](https://i.imgur.com/e0DV15I.png)

![](https://i.imgur.com/UKH8nXu.png)

What we see now is the `terraform plan` which is planning to created this resources.

`terraform plan` is like a dry run, it won't create the resources immediately, it asks for your approval by showing what
are the changes that will be made, like updating or deleting resources, and if approved with `terraform apply` and `yes`

### Terraform Apply

![](https://i.imgur.com/HNXonrU.png)

![](https://i.imgur.com/Kaxq5Q1.png)

![](https://i.imgur.com/VEtds3j.png)

This is now the terraform function in which it will show you the changes in the resources, and will then asked you for a
`yes` or `no` value.

![](https://i.imgur.com/k54J8Lb.png)

After saying `yes`, you can quickly see how fast it immediately created the resources.

#### Check the project in GCP for the changes

To check for the Cloud Storage

1. Go to the hamburger menu on the left side and then click `Cloud Storage` > `Buckets`.

   ![](https://i.imgur.com/pA6AqLK.png)

2. And then you can finally see the bucket created by the Terraform.

   ![](https://i.imgur.com/3CzNFbW.png)

In order to make the bucket unique, it was created with the bucket name and project name

```terraform
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location = var.region
  ...
}
```

To check for the BigQuery

1. Go to the hamburger menu on the left side and then click `BigQuery`.

   ![](https://i.imgur.com/S5qTpJH.png)

2. And then you can finally see the database table created by the Terraform.

   ![](https://i.imgur.com/bAUwx78.png)

### Terraform Destroy

![](https://i.imgur.com/kZw3BFo.png)

![](https://i.imgur.com/ZkYvDoP.png)

![](https://i.imgur.com/2tzCzaW.png)

After invoking the `terraform destroy` it will then show you like the `terraform apply` the details of the update that will be done and you must give approval in the end.

![](https://i.imgur.com/75pJrt1.png)

And upon checking in the GCP, the resources created are indeed gone.

---

## Page

| Previous                                                                                                                      | Return to table of contents |
|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| [Introduction to Terraform Concepts & GCP Pre-Requisites](1_3_1_Introduction_to_Terraform_Concepts_and_GCP_Pre-Requisites.md) | [Readme.md](README.md)      |