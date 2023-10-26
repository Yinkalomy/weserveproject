# We Serve Company

## Introduction
- WeServe is a call service agency that outsources personnel to other companies
- the personnel, located in one centre, receive and make calls to customers to get feedback on the various products and services, and to resolve complaints as soon as possible.
- the calls are recorded on call log sheets while extra details are recorded in the call detail sheet.

### The Task
The managers of the company would like to evaluate the performance of the agents by looking at key performance indicators (KPI) 

## Tools Used
The following tools were used for this project:

- boto3==1.28.48
- botocore==1.31.48
- configparser==6.0.0
- fsspec==2023.9.0
- greenlet==3.0.0
- jmespath==1.0.1
- numpy==1.25.2
- pandas==2.1.0
- psycopg2==2.9.7
- python-dateutil==2.8.2
- pytz==2023.3.post1
- s3fs==0.4.2
- s3transfer==0.6.2
- six==1.16.0
- SQLAlchemy==2.0.22
- typing_extensions==4.8.0
- tzdata==2023.3
- urllib3==1.26.16
- redshift-connector

## Warehouse Schema used

The final schema used is a star schema that contains 
- Fact table of the call log
- Dimension table of the call details
- Dimension table of the agents
- Aggregate table (KPI1) containing the total Number of Calls Resolved against the Total Number of Calls Received
- Aggregate table (KPI2) containing the total Number of calls received against the Total Number of calls assigned/resolved
- Aggregate table (KPI3) containing the total and average call duration for each agent and the grade level of these agents
- Aggregate table (KPI4) containing the earliest and latest closed and resolved calls, and the grade levels of the agents who resolved these cases

This schema was chosen to allow ease of retrieving data for each agent and optimizing the time without having to join tables.

## Description of processes involved in the execution of the project. 
    The following steps were taken to execute the project
- step 1: the files were read into the script through pandas library, using the 'read_csv' module
- step 2: each file was cleaned and transformed by writing python functions that handled null cells, difference in capitalization, and difference in datatypes. Two uniform files were produced. Both the raw and transformed files were stored in postgresql database
- step 3: A Data lake was created in AWS S3 bucket. 
- step 4: A connection was established and the transformed tables were transferred from postgresql to the AWS S3 bucket
- step 5: A warehouse was created in AWS Redshift cluster and a development schema was created. Tables were created in the cluster and data copied from the S3 datalake to the redshift raw data schema.
- step 6: the star schema was created which included the four aggregate and data was copied to the tables. The connection was closed.

## Conclusion
The project was concluded successfully.