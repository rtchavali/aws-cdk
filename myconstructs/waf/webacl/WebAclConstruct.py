from constructs import Construct
from aws_cdk.aws_wafv2 import CfnWebACL
from global_config import GlobalConfig


class WafWebACLGroupConstruct(Construct):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define the rules for the WAF RuleGroup
        # Create the WAFv2 RuleGroup
        print('-------------')
        print(config['rulegroup'].get('arn', ''))
        print('-------------')
        self.web_acl = CfnWebACL(
            self,
            config['name'],
            name=config['name'],
            scope=config['scope'],  # or "CLOUDFRONT"
            default_action=CfnWebACL.DefaultActionProperty(
                allow={}
            ),
            rules=[
                CfnWebACL.RuleProperty(
                    name=config['name'],
                    priority=0,
                    action=CfnWebACL.RuleActionProperty(
                        allow={}
                    ),
                    statement=CfnWebACL.StatementProperty(
                        rule_group_reference_statement=CfnWebACL.RuleGroupReferenceStatementProperty(
                            arn=config['rulegroup'].get('arn', '')
                        )
                    ),
                    visibility_config=CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=False,
                        cloud_watch_metrics_enabled=False,
                        metric_name="RuleGroupReferenceMetric"
                    )
                )
            ],
            visibility_config=CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name=config['visibility']['metric-name']
            )
        )