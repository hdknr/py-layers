# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html
import json
import urllib.request

import boto3

from .utils import create_ref_id


def client():
    return boto3.client("cloudfront")


def resource():
    return boto3.resource("cloudfront")


def list_distributions():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client.list_distributions
    return client().list_distributions()


def invalidate(distribution_id, *files, ref_id=None):
    # Clear Cache
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client.create_invalidation
    # Invalidation: https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html
    CallerReference = ref_id or create_ref_id()
    Items = [f"/{f}" for f in files]
    Quantity = len(Items)
    if Quantity < 1:
        return []

    InvalidationBatch = dict(
        Paths=dict(
            Quantity=Quantity,
            Items=Items,
        ),
        CallerReference=CallerReference,
    )
    return client().create_invalidation(DistributionId=distribution_id, InvalidationBatch=InvalidationBatch)


def edge_server_cidrs():
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    ip_ranges = json.loads(urllib.request.urlopen(url).read())
    ips = [item["ip_prefix"] for item in ip_ranges["prefixes"] if item["service"] == "CLOUDFRONT"]
    ips_v6 = [item["ipv6_prefix"] for item in ip_ranges["ipv6_prefixes"] if item["service"] == "CLOUDFRONT"]
    return (ips, ips_v6)
