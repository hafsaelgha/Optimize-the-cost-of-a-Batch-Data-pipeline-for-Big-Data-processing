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
## Ingestion
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
6- Airflow : to orchestrate this process and to make **our previous solution possible**, we define each step of this project as an airflow task (PythonOperator and SnowflakeOperator) within the DAG, starting from creating emr cluster, ingestion  layer, waiting for the step to complete, then transformation layer, then waiting fot this step to complete too, then terminating the cluster, and finally snowflake loading. Airflow is installed on EC2 instance. 

# Steps and Remarks

## 1- Ingestion 
Creating the S3 bucket and uploading the **ingest.sh** file on "input_folder" bucket.
![S3 bucket](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/f03ab328-b2ae-4569-949b-9897dd97ce9c)

## 2-Lambda Function and Trigger (S3) 
 connecting the S3 bucket to our lambda function
![lambda and S3](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/5e249586-ca34-457e-8bff-ace4ed3c94e8)

but before, we deploy the lambda function code which you can find on "lambda_function.py" file, and define the IAM role for our function, here's is the configuration : 
*Amazon EMR Full Access Policy v2" and "Amazon S3 full access"
![IAM role for lambda function](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/3b456611-ff0f-41fa-80d5-5c00301f1847)

and also created new roles : 

![IAM role used ](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/496d45b1-6007-4147-a423-63ac84f1f707)

## 3- Installing Airflow on EC2 instance 

![EC2 config](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/d906c6fa-500c-494d-803d-c297fc2cb9d3)

**Packages required :** python3-pip, sqlite3, libpq-dev, awscli, boto3, virtualenv. 
Then activate our virtual environnement and install Apache Airflow on it (including postgresql).
To launch our airflow as known, we should launch the **webserver and the scheduler** in separated sessions : 

![airflow on EC2 ](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/b1759224-14c2-4971-8b7c-85800ddcf7bc)
![airflow webserver1](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/11bca46b-6f5d-4f86-8b7d-9fa169500cf9)

## 4-Connecting Snowflake to Airflow

install apache-airflow-providers-snowflake==2.1.0 snowflake-connector-python==2.5.1 snowflake-sqlalchemy==1.2.5
After that we can add a new connection to Snowflake from the airflow UI and extract our snowflake_conn_id="snowflake_conn" that we need for the last task on the DAG.

![airflow DAG ](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/5b1f32af-6002-4942-a1f9-05c6702eb032)

 see the DAG file on "hello_world.py" 
 
## 5-


















