import json;
import boto3;

client = boto3.client('emr', region_name='us-east-1',aws_access_key_id='AKIAVJ77NPSARFFO4JPE',aws_secret_access_key='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')

#function to create the emr cluster

def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    bucketName=event['Records'][0]['s3']['bucket']['name']
    print("File Name : ",file_name)
    print("Bucket Name : ",bucketName)
    backend_code="s3://irisseta-bucket/scripts/transform.py"
    spark_submit = [
    'spark-submit',
    '--master', 'yarn',
    '--deploy-mode', 'cluster',
    backend_code,
    bucketName,
    file_name
    ]
    print("Spark Submit : ",spark_submit)
    cluster_id = client.run_job_flow(
    Name="transient_demo_testing",
    Instances={
    'InstanceGroups': [
    {
    'Name': "Master",
    'Market': 'ON_DEMAND',
    'InstanceRole': 'MASTER',
    'InstanceType': 'm1.xlarge',
    'InstanceCount': 1,
    },
    {
    'Name': "Slave",
    'Market': 'ON_DEMAND',
    'InstanceRole': 'CORE',
    'InstanceType': 'm1.xlarge',
    'InstanceCount': 2,
    }
    ],
    'Ec2KeyName': 'EC2_cluster',
    'KeepJobFlowAliveWhenNoSteps': False,
    'TerminationProtected': False,
    'Ec2SubnetId': 'subnet-0082b7ce164c586e8',
    },
    LogUri="s3://aws-logs-365071006849-us-east-1/elasticmapreduce",
    ReleaseLabel= 'emr-5.33.0',
    Steps=[{"Name": "testJobGURU",
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
    'Jar': 'command-runner.jar',
    'Args': spark_submit
    }
    }],
    BootstrapActions=[],
    VisibleToAllUsers=True,
    JobFlowRole="EMR_EC2_DefaultRole",
    ServiceRole="EMR_DefaultRole",
    Applications = [ {'Name': 'Spark'},{'Name':'Hive'}])
