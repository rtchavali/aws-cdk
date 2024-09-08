from constructs import Construct
from aws_cdk.aws_wafv2 import CfnRuleGroup

class WafRuleGroupConstruct(Construct):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define the rules for the WAF RuleGroup
         # Create the WAFv2 RuleGroup
        self.rule_group = CfnRuleGroup(
            self,
            id,
            name=config.get('name'),
            scope=config.get('scope', 'REGIONAL'),  # or "CLOUDFRONT" for global resources
            capacity=config.get('capacity',10),  # WCU (WebACL capacity unit) required for this rule group
            rules=config.get('rules'),
            visibility_config={
                "sampledRequestsEnabled": config['visibility']['sampledRequestsEnabled'],
                "cloudWatchMetricsEnabled": config['visibility']['cloudWatchMetricsEnabled'],
                "metricName": config.get('metric-name')
            }
        )
