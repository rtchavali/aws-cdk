from global_config import GlobalConfig
from constructs import Construct
from aws_cdk import Stack
from myconstructs.waf.webacl.WebAclConstruct import WafWebACLGroupConstruct  # Assuming the construct is in a separate file


class WafWebACLStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        global_config = GlobalConfig()
        webacl_global_config = global_config.get_config()['waf']['webacl']
        rg_global_config = global_config.get_config()['waf']['rulegroup']


        # Create a WAF RuleGroup using the custom construct
        for name, value in list(webacl_global_config.items()):
            value['rulegroup'] = {}
            value['rulegroup']['arn'] = rg_global_config[name].get('arn')
            webacl_op = WafWebACLGroupConstruct(
                self,
                value['name'],
                value
            )
            global_config.update_config(f'waf.webacl.{name}.arn',
                                        webacl_op.web_acl.attr_arn)

            # Output the RuleGroup ARN
            # CfnOutput(
            #     self,
            #     "WafRuleGroupArn",
            #     value=waf_rule_group.rule_group.attr_arn
            # )
