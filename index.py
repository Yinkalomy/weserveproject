import pandas as pd
import configparser
from utils.helper import create_bucket, connect_to_dwh
import psycopg2
import logging
from sqlalchemy import create_engine
import redshift_connector
from sql_statements.create import dev_tables, transformed_tables
from sql_statements.transform import transformation_queries


config = configparser.ConfigParser()
config.read('.env')

access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']
bucket_name = config['AWS']['bucket_name']
region = config['AWS']['region']
role = config['AWS']['arn']

db_host = config['DB_CONN']['host']
db_user = config['DB_CONN']['user']
db_password = config['DB_CONN']['password']
db_database = config['DB_CONN']['database']

dwh_host = config['DWH_CONN']['host']
dwh_user = config['DWH_CONN']['username']
dwh_password = config['DWH_CONN']['password']
dwh_database = config['DWH_CONN']['database']

# Step 1: Extraction of files and read them as csv
call_log = pd.read_csv('call log.csv')
call_details = pd.read_csv('call details.csv')


# Step 2: Clean and transform files
def cleaning(df):
    df['assignedTo'].fillna(df['agentID'], inplace=True)
    df['resolutionDurationInHours'].fillna(0, inplace=True)
    df['status'] = df['status'].str.lower()
    df['assignedTo'] = df['assignedTo'].astype(int)
    df['resolutionDurationInHours'] = df['resolutionDurationInHours'].astype(int)
    return df


dev_call_log = cleaning(call_log)


def cleaning_call_details(df):
    call_details['callID'] = call_details['callID'].replace('ageentsGradeLevel', 1)
    call_details['callType'] = call_details['callType'].replace('in-bound', 'inbound').str.lower()
    return df


dev_call_details = cleaning_call_details(call_details)


def extract_to_csv(df, filename):
    df.to_csv(filename, sep=',', index=False, header=True)
    return filename


extract_to_csv(dev_call_log, 'dev_call_log.csv')
extract_to_csv(dev_call_details, 'dev_call_details.csv')


# Step 3: Create a bucket using boto3
create_bucket(access_key, secret_key, bucket_name, region)

# Step 4:  Extract data from Database(postgreSql) to Data Lake (S3)
conn = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_database}')
s3_path = 's3://{}/{}.csv'
db_tables = ['dev_call_details', 'dev_call_log']

for table in db_tables:
    query = f'SELECT * FROM {table}'
    df = pd.read_sql_query(query, conn)
    logging.info(f'======== Executing {query}')
    df.to_csv(
        s3_path.format(bucket_name, table),
        index=False,
        storage_options={
            'key': access_key,
            'secret': secret_key
        }
    )

# Step 5: Create the Raw Schema in DWH
conn_details = {
                'host': dwh_host,
                'user': dwh_user,
                'password': dwh_password,
                'database': dwh_database
}

dwh_conn = connect_to_dwh(conn_details)
print('connection successful')
raw_schema = 'raw_data'
staging_schema = 'staging'

cursor = dwh_conn.cursor()

# ----- Create the dev schema
create_dev_schema_query = 'CREATE SCHEMA raw_data;'
cursor.execute(create_dev_schema_query)

# ---- Create the tables
for query in dev_tables:
    print(f'------------------ {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()


# ----- Copy from S3 to Redshift
for table in db_tables:
    query = f'''
            copy {raw_schema}.{table}
            from '{s3_path.format(bucket_name, table)}'
            iam_role '{role}'
            delimiter ','
            ignoreheader 1;
    '''
    cursor.execute(query)
    dwh_conn.commit()


# step 6: Transform to a star schema

# ------Create schema
create_staging_schema_query = f'''CREATE SCHEMA {staging_schema};'''
cursor.execute(create_staging_schema_query)
dwh_conn.commit()

# -----Create facts and dimensions
for query in transformed_tables:
    print(f'---------------- {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()


# ------Insert the data into the facts and dimensions
for query in transformation_queries:
    print(f'---------------- {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()


cursor.close()
dwh_conn.close()