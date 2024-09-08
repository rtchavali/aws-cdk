#!/usr/bin/env python3
import os
import yaml
import aws_cdk as cdk
from global_config import GlobalConfig
from aws_cdk_code.aws_cdk_stack import AwsCdkStack
from stacks.s3.bucket.s3bucketstack import S3BucketStack
from stacks.waf.ipset.IpSetStack import WafIpSetStack
from stacks.waf.rulegroup.RuleGroupStack import WafRuleGroupStack
from stacks.waf.webacl.WebACLStack import WafWebACLStack

def get_properties(file_path: str) -> dict:
    """
    get environment variables
    """
    with open(file_path, 'r', encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)
    

app = cdk.App()

environment = app.node.try_get_context('env')
region = app.node.try_get_context('region')

config_file = os.path.join(
    'vars',
    environment,
    f'{region}.yaml'
)

config = get_properties(config_file)
global_config = GlobalConfig()
global_config.append_config(new_config=config)


AwsCdkStack(app, "AwsCdkStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )


S3BucketStack(
    app, 
    f"{environment}-{region}-s3BucketStack"
    )

waf_ip_stack = WafIpSetStack(app,
              f"{environment}-{region}-WafIpSetStack"
            )

waf_rulegroup_stack = WafRuleGroupStack(app,
              f"{environment}-{region}-WafRuleGroupStack"
            )


waf_webacl_stack = WafWebACLStack(app,
              f"{environment}-{region}-WafWebACLStack"
            )

waf_rulegroup_stack.add_dependency(waf_ip_stack)
waf_webacl_stack.add_dependency(waf_rulegroup_stack)
app.synth()
