"""A Python Pulumi program"""

import pulumi
from pulumi_aws import s3 
import yaml

# Leer el archivo YAML
with open('variables.yaml', 'r') as file:
    variables = yaml.safe_load(file)

# Acceder a las variables
env = variables['env']
region = variables['region']
company = variables['company']

bucket_name = company + "-" + "s3" + "-" + region + "-" + env

bucket = s3.Bucket(bucket_name,
                       bucket=bucket_name,  # Esto establece el nombre exacto del bucket en S3
                       acl="private",
                       tags={
                           "Environment": env,
                           "Region": region,
                           "Company": company,
                           "Name": bucket_name
                       })



