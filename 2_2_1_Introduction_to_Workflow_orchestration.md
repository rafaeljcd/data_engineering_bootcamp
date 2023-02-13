- [What is workflow orchestration](#what-is-workflow-orchestration)
- [What is data flow](#what-is-data-flow)
- [Workflow orchestration tool](#workflow-orchestration-tool)
- [Core Features of workflow orchestration](#core-features-of-workflow-orchestration)
- [Different type of workflow tools](#different-type-of-workflow-tools)
- [Resources](#resources)
- [Page](#page)

---

## What is workflow orchestration

Workflow orchestration means governing your data flow in a way that respects orchestration rules and your business
logic.

## What is data flow

Data flow is what binds and otherwise disparate set of applications together.

## Workflow orchestration tool

Workflow orchestration tool is going to allow you to turn any code into a workflow that you can schedule run and observe

![](https://i.imgur.com/MST4i89.png)

For example, the analogy of a delivery system each order in the shopping cart is your workflow and each delivery is a
workflow run.

Adding items to your cart and functions to your workflows can be done effortlessly with a few python decorators.

Each order consists of multiple products packaged in boxes, similar to how tasks are contained within a workflow.

The products in the order can come in different forms, such as hand soap and dish soap, or soda and water. This is
similar to data transformations using DBT or data cleansing with Pandas, or even a machine learning use case.

The contents of your boxes can originate from a variety of suppliers, and you have the flexibility to choose the size of
your boxes to fit your workflow design needs.

The delivery addresses you specify can vary, whether it's your own address, a friend's address, or any other
destination. These can be thought of as different data warehouses or databases, ultimately affecting the output of your
workflow.

When checking out, you have the option to choose the delivery method for your order, either all at once or sequentially.
This is equivalent to configuring the order of execution for the tasks within your workflow.

You also have the option to have your delivery gift-wrapped, which is similar to packaging it into a sub-process, Docker
container, or Kubernetes job.

You could also choose the delivery type you know do you want express delivery imagine having multiple trucks delivering
your packages or do you want some speed up execution with a single thread using concurrency and async that would be like
having one driver who's faster and more efficient

Workflow orchestration is taking care of the delivery so that really means the execution of the workflow run and this is
ensuring that your products are getting packaged as desired, shipped at the schedule that you specified, and with the
right delivery type.

With Delivery Systems, a good orchestration service should scale and be highly available. We need to ensure that your
order is getting shipped, even if for example supplier is sick or there's a weather storm delay that should not be
affecting your package delivery system, as should a good orchestration system should be scalable and highly available as
well.

It is a fact that issues can arise during a delivery, such as damaged boxes that need to be returned. In workflows, this
can translate to retrying, restarting, or the need to reschedule the entire delivery process.

Workflow orchestration focuses on managing the flow of data and ensuring reliable execution. It provides visibility into
the delivery duration, shipment updates, similar to workflow execution logs, and confirms the successful completion of
the shipment, which is the final state of the workflow.

A delivery service should prioritize your privacy and only access metadata, such as the shipment address, delivery type,
and packaging form. Its role is limited to transporting and executing the data flow, without infringing on the contents
of the box, or your data. Privacy should be respected.

---

## Core Features of workflow orchestration

- Remote Execution
- Scheduling
- Retries
- Caching
- Integration with external systems (APIs, databases)
- Ad-hoc runs
- Parameterization
- Alert you when something fails

---

## Different type of workflow tools

![](https://i.imgur.com/vhiuX75.jpeg)

There are numerous tools available for data engineering and orchestration, as demonstrated in the 2022 State of Data
Engineering Map by LakeFS. While many tools have orchestration capabilities, such as Snowflake's data pipelines, a
comprehensive workflow orchestration tool offers the ability to manage data flow across all tools available in the
market.

In the following lectures we're going to be using open source prefect as the workflow orchestration tool

Prefect is a modern workflow orchestration tool that's going to deliver all those capabilities that makes a great
workflow orchestration tool and continues to drive Innovation

With that said it's always recommended to find the tool that works best for you and your specific use case

## Resources

- [Youtube - 2.2.1 - Introduction to Workflow orchestration](https://www.youtube.com/watch?v=8oLs6pzHp68)
- [Blog - State of the Data Engineering 2022](https://lakefs.io/blog/the-state-of-data-engineering-2022/)
- [Blog - Core Features of workflow orchestration](https://towardsdatascience.com/workflow-orchestration-vs-data-orchestration-are-those-different-a661c46d2e88)

---

## Page

| Previous                        | table of contents      |
|---------------------------------|------------------------|
| [Data Lake](2_1_1_Data_Lake.md) | [Readme.md](README.md) |