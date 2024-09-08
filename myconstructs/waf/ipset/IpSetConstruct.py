from constructs import Construct  # or aws_cdk as cdk for CDK v2
from aws_cdk.aws_wafv2 import CfnIPSet

class WafIPSetConstruct(Construct):  # Or cdk.Construct for CDK v2
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create the WAFv2 IPSet
        self.ip_set = CfnIPSet(
            self,
            id,
            name=config.get('name'),
            scope=config.get('scope'),  # Use "CLOUDFRONT" for CloudFront distributions
            ip_address_version=config.get('ip_address_version'),  # Can be "IPV6" if needed
            addresses=config.get('addresses')
        )
