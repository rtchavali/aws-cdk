from global_config import GlobalConfig
from constructs import Construct
from aws_cdk import (
    Stack
)
from aws_cdk.aws_wafv2 import CfnWebACL
from myconstructs.waf.webacl.WebAclConstruct import WafWebACLGroupConstruct  # Assuming the construct is in a separate file


class WafWebACLStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        global_config = GlobalConfig()
        webacl_global_config = global_config.get_config()['waf']['webacl']
        # rg_global_config = global_config.get_config()['waf']['rulegroup']


        # Create a WAF RuleGroup using the custom construct
        for name, value in list(webacl_global_config.items()):
            rg_global_config = global_config.get_config()['waf']['rulegroup'][name]
            value['rules'] = [
                CfnWebACL.RuleProperty(
                    name=rg_global_config['name'],
                    priority=0,
                    override_action=CfnWebACL.OverrideActionProperty(
                        none={}
                    ),
                    statement=CfnWebACL.StatementProperty(
                        rule_group_reference_statement=CfnWebACL.RuleGroupReferenceStatementProperty(
                            arn=rg_global_config.get('arn', '') # This should be a valid ARN
                            )
                    ),
                    visibility_config=CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=False,
                        cloud_watch_metrics_enabled=False,
                        metric_name=rg_global_config['metric-name']
                    )
                )
            ]
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
