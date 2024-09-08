from global_config import GlobalConfig
from aws_cdk.aws_wafv2 import CfnRuleGroup

def get_rules():

    get_global_config = GlobalConfig().get_config()
    ipset_config = get_global_config['waf']['ipset']
    rulegroup_config = get_global_config['waf']['rulegroup']
    print(rulegroup_config)
    print(rulegroup_config['test-1'])
    print(rulegroup_config['test-1']['rule_config'])
    print(rulegroup_config['test-1']['rule_config']['priority'])
    rules = {
            'test-1': CfnRuleGroup.RuleProperty(
            name=rulegroup_config['test-1']['name'],
            priority=rulegroup_config['test-1']['rule_config']['priority'],
            action=CfnRuleGroup.RuleActionProperty(
                block={}
            ),
            statement=CfnRuleGroup.StatementProperty(
                rate_based_statement=CfnRuleGroup.RateBasedStatementProperty(
                    limit=rulegroup_config['test-1']['rule_config']['limit'],
                    aggregate_key_type="IP"
                )
            ),
            visibility_config=CfnRuleGroup.VisibilityConfigProperty(
                sampled_requests_enabled=rulegroup_config['test-1']['visibility']['sampledRequestsEnabled'],
                cloud_watch_metrics_enabled=rulegroup_config['test-1']['visibility']['cloudWatchMetricsEnabled'],
                metric_name=rulegroup_config['test-1']['metric-name']
            )
        ),

        'test-2': CfnRuleGroup.RuleProperty(
            name=rulegroup_config['test-2']['name'],
            priority=rulegroup_config['test-1']['rule_config']['priority'],  # Higher priority than rate limit rule
            action=CfnRuleGroup.RuleActionProperty(
                block={}  # Can also use "allow" or "count" as needed
            ),
            statement=CfnRuleGroup.StatementProperty(
                ip_set_reference_statement=CfnRuleGroup.IPSetReferenceStatementProperty(
                    arn=ipset_config['test-2'].get('arn', '') # Reference the IPSet's ARN
                )
            ),
            visibility_config=CfnRuleGroup.VisibilityConfigProperty(
                sampled_requests_enabled=rulegroup_config['test-2']['visibility']['sampledRequestsEnabled'],
                cloud_watch_metrics_enabled=rulegroup_config['test-2']['visibility']['cloudWatchMetricsEnabled'],
                metric_name=rulegroup_config['test-2']['metric-name']
            )
        )
    }
    
    return rules