# Batch-Data-Pipeline

# Introduction

In most business use case of cloud data engineering, we tends to design powerful architectures that meet their business needs, ensure **Availability, Scalability and Cost effectivness**, combining these 3 constraints proves difficult sometimes. 

**Persistent EMR Clusters** remain alive **all the time**, even when a job has completed, they have 2 major problems : 
- [ ] 1)It may result into **huge cost** due to idle time
- [ ] 2)when lot of heavy jobs run together then due to resource issue , the Spark Jobs might take **huge time** to complete in **Persistent EMR Cluster** , which might impact business ...

In this project, I'm gonna introduce the **Transient Cluster**  to resolve both issues: 
**launch fresh EMR Cluster when needed to run Spark Jobs & when the step is complete, the cluster get terminated automatically !** 

**Let's embark on the project to discover this solution !** 

# Architecture 
![Blank diagram](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/ec68c67a-a18f-4bc5-b10b-5da37baab97d)
# Ingestion
1- As a first step I downloaded the data from the internet using the wget command, the dataset I used is just a modelilzation for this project in order to reuse the same architecture in any other Batch pipeline use case. Here's the link of the dataset https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data .
2- Upload the data into S3 bucket, this is the landing layer of our architecture that will **trigger** the lambda function.

## Transform 
1- Lambda Function : is used to deploy code that is responsible of creating the **emr cluster** and it uses **boto3** to create it. (See the section about IAM role attahed to this service)
2- EMR cluster : is the cluster that will be launched by the lambda function triggered by the S3 bucket. Master and Slaves (2 instances) are the simple configuratioin I used in this project. 
3- PySpark : we create a Spark session in order to partition our dataset into one single frame and save it into output_folder.
4- S3 bucket : 2 S3 buckets, one as a **landing layer** and the other one as **curated layer**.

## Loading 
5- Snowflake :  setting up an external table in Snowflake involves defining the table's schema and specifying the location and format of the data in the external source. Snowflake then provides SQL commands to query and manipulate this data seamlessly as if it were a regular table within Snowflake.

## Orchestrating 
6- Airflow : to orchestrate this process and to make **our previous solution possible**, we define each step of this project as an airflow task (PythonOperator and SnowflakeOperator) within the DAG, starting from creating emr cluster, ingestion  layer, waiting for the step to complete, then transformation layer, then waiting fot this step to complete too, then terminating the cluster, and finally snowflake loading.








