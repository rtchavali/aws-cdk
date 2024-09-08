from global_config import GlobalConfig
from myconstructs.waf.ipset.IpSetConstruct import WafIPSetConstruct  # Assuming you saved the construct in a separate file
from aws_cdk import (
    CfnOutput, 
    Stack
)
from constructs import Construct


class WafIpSetStack(Stack):  # Or cdk.Stack for CDK v2
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        global_config = GlobalConfig()
        get_global_config = global_config.get_config()

        ipset_config = get_global_config['waf']['ipset']
        for ipset, values in list(ipset_config.items()):
            ip_op = WafIPSetConstruct(self, ipset, values)
            global_config.update_config(f'waf.ipset.{ipset}.arn',
                                        ip_op.ip_set.attr_arn)

        # Output the IP Set ARN
        # CfnOutput(
        #     self,
        #     "WafIPSetArn",
        #     value=waf_ip_set.ip_set.attr_arn
        # )
