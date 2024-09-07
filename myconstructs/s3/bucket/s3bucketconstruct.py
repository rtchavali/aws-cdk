#  https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3.html

from constructs import Construct
from aws_cdk.aws_s3 import CfnBucket
from global_config import GlobalConfig


class s3BucketConstruct(Construct):
    def __init__(self, scope: Construct, id: str, bkt_name: str, config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)
        global_config = GlobalConfig()
        get_global_config = global_config.get_config()
        s3_global_config = get_global_config['s3']
        # Define the S3 bucket using CfnBucket (low-level CloudFormation resource)
        self.bucket = CfnBucket(self, 
                                config['name'],
                                bucket_name=config['name'],
                                versioning_configuration={
                                    "status": config['versioning']['status']
                                })