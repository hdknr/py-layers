from datetime import datetime, timedelta

import boto3


def client():
    return boto3.client("logs")


def all_groups():
    return client().describe_log_groups()


def metric_filter(name, namespace):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_metric_filters
    res = client().describe_metric_filters(
        metricName=name,
        metricNamespace=namespace,
    )
    filters = res.get("metricFilters", None)
    if filters and len(filters) > 0:
        return filters[0]


def filter_events(group_name, pattern, dt_to=None, seconds=3000, limit=10):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.filter_log_events
    # Pattern:
    #   https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

    dt_to = dt_to or datetime.now()
    dt_from = dt_to - timedelta(seconds=int(seconds))

    dt_to = int(dt_to.timestamp() * 1000)  # msec
    dt_from = int(dt_from.timestamp() * 1000)  # msec

    return client().filter_log_events(
        logGroupName=group_name,
        startTime=dt_from,
        endTime=dt_to,
        filterPattern=pattern,
        limit=limit,
    )


def get_triger(message):
    node = "Trigger"
    if node in message:
        return message[node]
