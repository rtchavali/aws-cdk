from global_config import GlobalConfig
from constructs import Construct
from aws_cdk import Stack
from myconstructs.waf.rulegroup.RuleGroupConstruct import WafRuleGroupConstruct  # Assuming the construct is in a separate file
from .rules.rules import get_rules


class WafRuleGroupStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        global_config = GlobalConfig()
        rg_global_config = global_config.get_config()['waf']['rulegroup']

        # Create a WAF RuleGroup using the custom construct
        for rg, value in list(rg_global_config.items()):
            rules = get_rules()
            value['rules'] = [rules[rg]]
            rg_op = WafRuleGroupConstruct(
                self,
                value['name'],
                value
            )
            global_config.update_config(f'waf.rulegroup.{rg_op}.arn',
                                        rg_op.rule_group.attr_arn)

            # Output the RuleGroup ARN
            # CfnOutput(
            #     self,
            #     "WafRuleGroupArn",
            #     value=waf_rule_group.rule_group.attr_arn
            # )
