# my_stack.py
from aws_cdk import Stack
from global_config import GlobalConfig
from constructs import Construct
from myconstructs.s3.bucket.s3bucketconstruct import s3BucketConstruct


class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        global_config = GlobalConfig()
        get_global_config = global_config.get_config()
        # Instantiate the MyS3Construct inside the stack
        for bucket, info in list(get_global_config['s3']['bucket'].items()):
            # print(info)
            s3_op = s3BucketConstruct(self, bucket, bkt_name=info['name'], config=info)

            global_config.update_config(f"s3.bucket.{info}.arn", 
                                        f"arn:aws:s3:::{s3_op.bucket.bucket_name}")
            