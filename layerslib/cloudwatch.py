import json

from .logs import filter_events, metric_filter
from .sns import get_sns_message_from_event


def get_metric_filter_alarmevent(alarmevent, **kwargs):
    trigger = alarmevent.get("Trigger", None)
    mf = trigger and metric_filter(
        trigger["MetricName"],
        trigger["Namespace"],
        **kwargs,
    )
    return mf


def filter_events_for_alarmevent(alarmevent, **kwargs):
    mf = get_metric_filter_alarmevent(alarmevent, **kwargs)
    return mf and filter_events(mf["logGroupName"], mf["filterPattern"])


def filter_events_for_sns(event, **kwargs):
    sns = get_sns_message_from_event(event)
    alarmevent = json.loads(sns["Message"])
    return filter_events_for_alarmevent(alarmevent, **kwargs)
