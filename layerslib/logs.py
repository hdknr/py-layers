import boto3
from datetime import datetime, timedelta


def client():
    return boto3.client('logs')


def metric_filter(name, namespace):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_metric_filters
    return client().describe_metric_filters(
        metricName=name,
        metricNamespace=namespace,
    )


def filter_events(group_name, pattern, dt_to=None, seconds=3000, limit=10):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.filter_log_events
    # Pattern:
    #   https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

    dt_to = dt_to or datetime.now() 
    dt_from = dt_to - timedelta(seconds=seconds) 
    dt_to = int(dt_to.timestamp() * 1000)        # msec
    dt_from = int(dt_from.timestamp() * 1000)    # msec

    return client().filter_log_events(
        logGroupName=group_name,
        startTime=dt_from,
        endTime=dt_to,
        filterPattern=pattern,
        limit=limit,
    )
