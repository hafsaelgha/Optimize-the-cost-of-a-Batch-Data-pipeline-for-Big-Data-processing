import sys
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import *

#Creating SparkSession
spark = SparkSession \
        .builder \
        .appName("airflow_with_emr") \
        .getOrCreate()
        
#Defining the main function
def main():
    s3_location="s3://irisseta-bucket/input_folder/"
    #Adding column's name
    iris = spark.read.format("csv").option("inferSchema","true").load(s3_location).toDF('SEPAL_LENGTH','SEPAL_WIDTH','PETAL_LENGTH','PETAL_WIDTH','CLASS_NAME')
    ms=iris.groupBy("CLASS_NAME").count()
    #Partinioning into one single frame and save it into output_folder
    ms.coalesce(1).write.format("parquet").mode('overwrite').save("s3://irisseta/output_folder/") #destination bucket in emr 

main()


