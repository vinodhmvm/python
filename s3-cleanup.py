import logging
import boto3
import datetime
import time
from botocore.exceptions import ClientError

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')
    bucket_name = 'vinodhtestbucket'
    objects = list_bucket_objects(bucket_name)
    if objects is not None:
        # List the object names
        logging.info(f'Objects in {bucket_name}')
        count = len(objects)
        print(f'Length of Object: {count}')
   
        for obj in objects:
            count = count - 1 # For not deleting from the last 7 days!  
            # Start Policy for everything older then one week
            
            timestampobj = obj["LastModified"].timestamp()
            seven_days_ago = time.time() - 7 * 86400
            if (timestampobj > seven_days_ago):
                print("Deleting the Objects older than 7 days:" , obj["Key"])
                #s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
    
def list_bucket_objects(bucket_name):
    # Retrieve the list of bucket objects
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return None
    return response['Contents']
