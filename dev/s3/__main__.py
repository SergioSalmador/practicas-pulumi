import pulumi
import pulumi_aws as aws

config = pulumi.Config()

# Acceder a las variables
env = config.require("env")
region = config.require("region")
svc = config.require("svc")
company = config.require("company")
day = config.require("day")

bucket_name = company + "-" + svc + "-" + region + "-" + env

def create_s3_bucket(name, env, region, company):
    return aws.s3.Bucket(name,
                         bucket=name,
                         acl="private",
                         tags={
                             "Environment": env,
                             "Region": region,
                             "Company": company,
                             "Name": name
                         })

def set_bucket_lifecycle(bucket_arn, day):
    return aws.s3control.BucketLifecycleConfiguration("bucketLifecycleConfiguration",
        bucket=bucket_arn,
        rules=[
            aws.s3control.BucketLifecycleConfigurationRuleArgs(
                expiration=aws.s3control.BucketLifecycleConfigurationRuleExpirationArgs(
                    days=day,
                ),
                id="example-rule",
                filter=aws.s3control.BucketLifecycleConfigurationRuleFilterArgs(
                    prefix="*",
                ),
            )
        ])
    
bucket = create_s3_bucket(bucket_name, env, region, company)
bucket_lifecycle_configuration = set_bucket_lifecycle(bucket.arn, day)